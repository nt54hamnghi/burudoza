import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from burudoza.directories import CONTENT_DIR, DATA_DIR
from burudoza.utils import display_content, display_header, graph, styleit


def run(dataframe: pd.DataFrame) -> None:
    st.header("Introduction")
    # 1. overview
    overview()
    # 2. data information
    data_info(dataframe)


INTRO_DIR = CONTENT_DIR / "intro"


def overview():
    overview = st.container()
    with overview:
        st.subheader("1. Overview")
        display_content(INTRO_DIR / "overview.txt")


def data_info(data: pd.DataFrame):
    data_containter = st.container()

    with data_containter:
        st.subheader("2. Data Description")
        display_header("A look at the data", 4)

        st.markdown("The first 20 samples:")
        st.caption(
            "__NOTE__: Hover on the feature name to see its full name."
        )

        # load data description
        data_desc = load_data_description()
        styleit(st.dataframe)(data.head(10), height=400)

        # display shape
        st.write("Shape: ")
        st.write(f"Training Set: `{data.shape}`")
        st.write(f"Testing Set: `{(11573, 50)}`")

        # drop-down box for selecting feature to display description
        display_header("Feature Description", 4)
        feature_name = (
            st.selectbox("Select feature", options=data_desc.index) or ""
        )
        feature_desc = (
            data_desc.loc[feature_name].values[0].strip().capitalize()
        )
        display_header(f"Description:\n{feature_desc}", 6)

        # display summary of the chosen feature
        try:
            feature = data[feature_name]
        except KeyError:
            pass
        else:
            feature_summary(feature_name, feature)

        st.warning(
            "__WARNING__: The data is its raw form. The graph and summary statistics of some variables may not be reasonable."  # NOQA
        )


@st.cache_data(show_spinner=False)
def load_data_description() -> pd.DataFrame:
    description = pd.read_feather(DATA_DIR / "data_dict.feather")
    description.Variable.replace(
        {
            "ProductClassDesc": "fiProductClassDesc",
            "Saledate": "saledate",
            "Saleprice": "SalePrice",
            "State": "state",
            "Tip_control": "Tip_Control",
        },
        inplace=True,
    )
    description.set_index("Variable", inplace=True)

    return description


def feature_summary(feature_name: str, feature_data: pd.Series):
    info = feature_data.describe().to_dict()
    info["na count"] = feature_data.isna().sum()
    info["data type"] = feature_data.dtype

    display_header("Summary: ", 6)

    summary_col, plot_col = st.columns(spec=[1, 3])
    with summary_col:
        for k, v in info.items():
            st.write(f"{k.capitalize()}:`{v}`")

    with plot_col:
        histogram = go.Histogram(x=feature_data, nbinsx=45)
        graph.render(
            go.Figure(data=histogram),
            layout=dict(
                height=525,
                xaxis_title=feature_name,
                yaxis_title="Count",
            ),
        )
