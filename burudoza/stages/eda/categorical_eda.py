from typing import Any, Optional

import numpy as np
import pandas as pd
import streamlit as st

from burudoza.directories import CONTENT_DIR
from burudoza.utils.display import display_content, display_header
from burudoza.utils.graph import (
    AxesLabel,
    TraceContainer,
    overlay_boxplot,
    overlay_histogram,
    render,
    subplots,
)

CATEGORICAL_DIR = CONTENT_DIR / "eda" / "categorical"


def categorical(dataframe: pd.DataFrame) -> None:
    st.subheader("3. Categorical Variables")

    Enclosure(dataframe)
    UsageBand(dataframe)
    Drive_System(dataframe)


def Enclosure(dataframe: pd.DataFrame):
    display_header("`Enclosure`", 4)
    display_content(CATEGORICAL_DIR / "enclosure.txt")

    to_replace = {"EROPS AC": "EROPS w AC", "None or Unspecified": "NO ROPS"}
    overlay(dataframe, "Enclosure", to_replace)


def UsageBand(dataframe: pd.DataFrame):
    display_header("`UsageBand`", 4)
    display_content(CATEGORICAL_DIR / "usageband.txt")

    overlay(dataframe, "UsageBand")


def Drive_System(dataframe: pd.DataFrame):
    display_header("`Drive_System`", 4)
    display_content(CATEGORICAL_DIR / "drivesys.txt")

    overlay(dataframe, "Drive_System")


def overlay(
    dataframe: pd.DataFrame,
    cat: str,
    to_replace: Optional[dict[str, Any]] = None,
) -> None:
    hist = TraceContainer(
        overlay_histogram(
            dataframe,
            x="SalePrice",
            hue=cat,
            to_replace=to_replace,
            transform=np.log1p,
        ),
        AxesLabel("Log of Sale Price", "Count"),
    )

    box = TraceContainer(
        overlay_boxplot(
            dataframe,
            x="SalePrice",
            hue=cat,
            to_replace=to_replace,
            transform=np.log1p,
        ),
        AxesLabel("Log of Sale Price", ""),
    )

    fig = subplots([box, hist], nrows=1, ncols=2)

    render(fig, layout=dict(height=400))
