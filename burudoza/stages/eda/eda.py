import numpy as np
import pandas as pd
import streamlit as st

from burudoza.directories import CONTENT_DIR
from burudoza.stages.eda.categorical_eda import categorical
from burudoza.stages.eda.numerical_eda import numerical
from burudoza.utils.display import (
    display_content,
    display_header,
    display_note,
    styleit,
)

EDA_DIR = CONTENT_DIR / "eda"


def run(dataframe: pd.DataFrame) -> None:
    st.header("Explanatory Data Analysis")

    display_note(
        "This analysis use a random subset with 45,000 rows from the original data set."
    )

    with st.container():
        first, second, third = st.tabs(
            ["Overview", "Numerical", "Categorical"]
        )

        with first:
            data = prepare(dataframe, False)
            overview(data)

        with second:
            data = prepare(dataframe)
            numerical(data)

        with third:
            data = prepare(dataframe)
            categorical(data)


def overview(dataframe: pd.DataFrame):
    st.subheader(f"1. Overview")
    display_header("Removing Unnecessary Variables", 4)
    display_content(EDA_DIR / "dropcols.txt")

    display_header("Investigating Feature Summary", 4)
    styleit(st.table)(summarize(dataframe))
    display_content(EDA_DIR / "summary.txt")


def summarize(dataframe: pd.DataFrame) -> pd.DataFrame:
    uniques = dataframe.select_dtypes(include=["number"]).nunique()
    uniques.name = "unique"

    return pd.concat([dataframe.describe(), uniques.to_frame().T])


@st.cache_data
def prepare(dataframe: pd.DataFrame, sample: bool = True) -> pd.DataFrame:
    dataframe.replace(
        {"YearMade": 1000, "MachineHoursCurrentMeter": 0},
        value=np.nan,
        inplace=True,
    )

    if sample:
        return dataframe.sample(frac=0.125, replace=True)

    return dataframe
