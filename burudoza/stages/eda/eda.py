from enum import StrEnum, auto
import select
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


class Option(StrEnum):
    Overview = auto()
    Numerical = auto()
    Categorical = auto()


OPTIONS = Option._member_names_


def run(dataframe: pd.DataFrame) -> None:
    st.header("Explanatory Data Analysis")

    with st.container():
        selected = st.selectbox("Option", options=OPTIONS) or "_"

        match selected.lower():
            case Option.Overview:
                data = prepare(dataframe, False)
                overview(data)
            case Option.Numerical:
                data = prepare(dataframe)
                numerical(data)
            case Option.Categorical:
                data = prepare(dataframe)
                categorical(data)
            case _:
                raise KeyError(f"Invalid option {selected}")


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
        display_note(
            "This analysis use a random subset with 30,000 rows from the original data set."
        )
        return dataframe.sample(n=30_000)

    return dataframe
