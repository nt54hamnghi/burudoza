import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from sklearn.preprocessing import minmax_scale

from burudoza.directories import CONTENT_DIR
from burudoza.utils.display import display_content, display_header
from burudoza.utils.graph import AxesLabel, TraceContainer, render, subplots

NUMERICAL_DIR = CONTENT_DIR / "eda" / "numerical"


def numerical(dataframe: pd.Series) -> None:
    st.subheader("2. Numerical Variables")
    target = dataframe["SalePrice"]

    YearMade(dataframe)
    MachineHoursCurrentMeter(dataframe, target)
    MachineID(dataframe, target)


def YearMade(dataframe: pd.DataFrame):
    display_header("`YearMade`", 4)
    display_content(NUMERICAL_DIR / "yearmade.txt")

    # box plot
    boxplot = TraceContainer(
        go.Box(
            x=dataframe["YearMade"],
            boxpoints="outliers",
            quartilemethod="inclusive",
            name="",
        ),
        AxesLabel("Year Made", ""),
    )

    # line plot
    year_grps = dataframe.groupby("YearMade")["SalePrice"].mean()
    lineplot = TraceContainer(
        go.Scatter(x=year_grps.index, y=year_grps, mode="lines"),
        AxesLabel("Year Made", "Mean Sale Price"),
    )

    fig = subplots([boxplot, lineplot], nrows=1, ncols=2)
    render(fig, layout=dict(height=400, showlegend=False))


def MachineHoursCurrentMeter(dataframe: pd.DataFrame, target: pd.Series):
    display_header("`MachineHoursCurrentMeter`", 4)
    display_content(NUMERICAL_DIR / "machinehour-p1.txt")

    with st.expander("Note"):
        display_content(NUMERICAL_DIR / "machinehour-p2.txt")

    x = dataframe["MachineHoursCurrentMeter"]
    violin_before = TraceContainer(
        go.Violin(x=x, name="Before"), AxesLabel("Hour", "")
    )
    violin_after = TraceContainer(
        go.Violin(x=np.log1p(x), name="After"),
        AxesLabel("Log of Hour", ""),
    )

    fig = subplots([violin_before, violin_after], nrows=1, ncols=2)
    render(fig, layout=dict(height=400, showlegend=False))

    scatter = go.Scattergl(
        x=np.log1p(x),
        y=target,
        mode="markers",
        marker=dict(line_width=0, size=4),
    )
    display_content(NUMERICAL_DIR / "machinehour-p3.txt")
    render(
        go.Figure(scatter),
        layout=dict(
            xaxis_title="Log of Hour", yaxis_title="Sale Price", height=400
        ),
    )


def MachineID(dataframe: pd.DataFrame, target: pd.Series):
    display_header("`MachineID`", 4)
    display_content(NUMERICAL_DIR / "machineid.txt")

    x = dataframe["MachineID"]
    scatter_before = TraceContainer(
        go.Scattergl(
            x=x,
            y=target,
            mode="markers",
            marker=dict(line_width=0, size=2),
        ),
        AxesLabel("Machine ID", "Sale Price"),
    )

    scatter_after = TraceContainer(
        go.Scattergl(
            x=minmax_scale(x.map(x.value_counts())),
            y=target,
            mode="markers",
            marker=dict(line_width=0, size=2),
        ),
        AxesLabel("Normalized Count by Machine ID", "Sale Price"),
    )
    fig = subplots([scatter_before, scatter_after], nrows=1, ncols=2)
    render(fig, layout=dict(height=400, showlegend=False))
