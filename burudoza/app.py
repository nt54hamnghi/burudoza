import pandas as pd
import streamlit as st

from burudoza.directories import DATA_DIR
from burudoza.stages import eda, intro, models
from burudoza.stages.stages import STAGES, Stage


@st.cache_data(show_spinner=False)
def _load_data(filename: str):
    return pd.read_feather(DATA_DIR / filename)


def _preload():
    # Raw data
    raw = _load_data("raw_train.feather")

    # Processed data
    X_train, y_train = (
        _load_data("xtrn.feather"),
        _load_data("ytrn.feather").iloc[:, 0],
    )
    X_test, y_test = (
        _load_data("xval.feather"),
        _load_data("yval.feather").iloc[:, 0],
    )

    processed = (X_train, X_test, y_train, y_test)

    return raw, processed


def setup():
    st.set_page_config(page_title="Burudoza", layout="wide")
    st.title("Bulldozers Auction Price Predicting")


def main():
    stage = st.sidebar.selectbox("Select Stage", options=STAGES) or "_"

    # load data
    raw_train, (X_train, X_test, y_train, y_test) = _preload()

    # match page/stage
    match stage.lower():
        case Stage.INTRO:
            intro.run(raw_train)
        case Stage.EDA:
            eda.run(raw_train)
        case Stage.MODELS:
            models.run((X_train, y_train), (X_test, y_test))
        case _:
            raise KeyError("Stage not available")


if __name__ == "__main__":
    setup()
    main()
