import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from burudoza.directories import CONTENT_DIR
from burudoza.stages.models.config.setup import (
    SetupFunction,
    TreeBasedRegressor,
    extra_trees_setup,
    gradient_boosting_setup,
    random_forest_setup,
)
from burudoza.utils.display import (
    display_content,
    display_metric,
    display_note,
    styleit,
)
from burudoza.utils.evaluate import evalutate, get_feature_importances
from burudoza.utils.graph import BLUE_CMAP, cmap2hexlist, render
from burudoza.utils.helper import create_logger, timeit

MODEL_LOGGER = create_logger(name="models", logfile="fit.log")

MODELS: dict[str, SetupFunction] = {
    "Random Forest": random_forest_setup,
    "Extra Trees": extra_trees_setup,
    "Gradient Boost": gradient_boosting_setup,
}

MODELS_DIR = CONTENT_DIR / "models"


@timeit
def fit(
    estimator: TreeBasedRegressor, X: pd.DataFrame, y: pd.Series
) -> TreeBasedRegressor:
    return estimator.fit(X.values, y.values)


def run(
    train: tuple[pd.DataFrame, pd.Series],
    test: tuple[pd.DataFrame, pd.Series],
) -> None:
    st.header("Modeling")

    X_train, y_train = sample_partition(*train)
    X_test, y_test = sample_partition(*test)

    with st.container():
        st.subheader("1. Configurations")
        model_name = (
            st.selectbox("Select Model", options=MODELS.keys()) or "_"
        )
        # handle options
        estimator = MODELS[model_name]()

        display_note(
            """To speed up processing time, only 1/8 of the data samples is used for training and scoring.
            In practice, you might want to utilize all data available to achieve high performance scores"""
        )

        # handle button
        clicked = st.button("Click to fit")

        if clicked:
            with st.spinner("Training..."):
                estimator, time_taken = fit(estimator, X_train, y_train)

            st.success(f"Finished in {round(time_taken, 3)} second(s).")

            with st.container():
                Metrics(X_test, y_test, estimator)

            with st.container():
                FeatureImportances(X_train, estimator)


def sample_partition(X: pd.DataFrame, y: pd.Series):
    X_sampled = X.sample(frac=1 / 8, replace=False, random_state=0)
    y_sampled = y[X_sampled.index]

    return X_sampled, y_sampled


METRICS = ["rmse", "mae", "r2"]


def Metrics(X_test, y_test, estimator):
    st.subheader("2. Metrics")
    (first, second, third) = st.columns(3)
    rmse, mae, r2 = evalutate(estimator, X_test, y_test)

    with first:
        display_metric(
            rmse,
            "RMSE - Root Squared Mean Error",
            "rmse",
            smaller_better=True,
        )

    with second:
        display_metric(
            mae, "MAE - Mean Absolute Error", "mae", smaller_better=True
        )

    with third:
        display_metric(
            r2, "R2 - R-squared", "r2", help="The maximum value is 1."
        )


def FeatureImportances(X_train: pd.DataFrame, estimator):
    st.subheader("3. Feature Importances")

    fi = get_feature_importances(
        features=X_train.columns,
        importance=estimator.feature_importances_,
        threshold=0.95,
    )

    fi_styled = fi.style.background_gradient(
        cmap=BLUE_CMAP,
        subset=["Importance", "Normalized Cummulative"],
    )

    # table
    styleit(st.table)(data=fi_styled)

    with st.expander("NOTE: "):
        display_content(MODELS_DIR / "featimp-note.txt")

    # graph
    x, y = fi.Importance, fi.index
    barchart = go.Bar(
        x=x,
        y=y,
        orientation="h",
        text=x,
        texttemplate="%{x:.4f}",
        marker_color=fi.Importance,
    )

    render(
        go.Figure(data=barchart),
        layout=dict(
            colorscale_sequential=cmap2hexlist(),
            xaxis_title="Importance",
            yaxis_title="Variables",
        ),
    )
