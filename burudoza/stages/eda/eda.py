from typing import Callable, TypeAlias

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

    with st.container():
        section = st.selectbox(
            "Select Sections", options=SECTIONS_HANDLERS.keys()
        )

        display_note(
            """
            This analysis use a random sample from the original data set.
            It has 45,000 rows and stays static throughout multiple runs.
            To generate new sample set each run.
            Click the checkbox below.
            """
        )

        resampled = st.checkbox("Resample Each Time")

        handler = SECTIONS_HANDLERS[section or "_"]
        sampled = sample(dataframe, resampled)
        handler(sampled)


def pre_analysis(dataframe: pd.DataFrame):
    st.subheader(f"1. Pre-Analysis")
    display_header("Removing Unnecessary Variables", 4)
    display_content(EDA_DIR / "dropcols.txt")

    display_header("Investigating Feature Summary", 4)
    styleit(st.table)(summarize(dataframe))
    display_content(EDA_DIR / "summary.txt")


SectionHandler: TypeAlias = Callable[[pd.DataFrame], None]

SECTIONS_HANDLERS: dict[str, SectionHandler] = {
    "Pre-Analysis": pre_analysis,
    "Numerical": numerical,
    "Categorical": categorical,
}


def summarize(dataframe: pd.DataFrame) -> pd.DataFrame:
    uniques = dataframe.select_dtypes(include=["number"]).nunique()
    uniques.name = "unique"

    return pd.concat([dataframe.describe(), uniques.to_frame().T])


def sample(dataframe: pd.DataFrame, resampled: bool = False) -> pd.DataFrame:
    dataframe.replace(
        {"YearMade": 1000, "MachineHoursCurrentMeter": 0},
        value=np.nan,
        inplace=True,
    )
    random_state = None if resampled else int(resampled)

    return dataframe.sample(
        frac=0.125, replace=True, random_state=random_state
    )
