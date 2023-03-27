import itertools
from typing import Any, Callable, NamedTuple, Optional

import colormap as cm
import numpy as np
import pandas as pd
import plotly.express as px
import seaborn as sns
import streamlit as st
from plotly.basedatatypes import BaseTraceType
from plotly.graph_objects import Figure
from plotly.subplots import make_subplots


class AxesLabel(NamedTuple):
    xlabel: str
    ylabel: str


class TraceContainer(NamedTuple):
    graph: BaseTraceType | list[BaseTraceType]
    labels: AxesLabel


BASE_LAYOUT = dict(
    autosize=False,
    height=600,
    margin=dict(l=1, r=1, b=1, t=1),
)


def render(fig: Figure, layout: dict[str, Any] | None = None) -> None:
    if layout is None:
        layout = BASE_LAYOUT
    else:
        layout = BASE_LAYOUT | layout  # dict merge

    fig.update_layout(**layout)
    st.plotly_chart(fig, use_container_width=True)


def subplots(
    trace_container: list[TraceContainer], nrows: int, ncols: int
) -> Figure:
    # check if the number of subplots is equal to the number of traces
    if len(trace_container) != ncols * nrows:
        raise ValueError(
            "Number of graphs is not compatible to number of subplots."
        )

    fig = make_subplots(rows=nrows, cols=ncols)
    axes = create_axes(nrows, ncols)

    for trace, (x, y) in zip(trace_container, axes):
        # if it's a single trace
        if isinstance(trace.graph, BaseTraceType):
            fig.add_trace(trace.graph, row=x, col=y)
        else:
            for graph in trace.graph:
                fig.add_trace(graph, row=x, col=y)

        fig.update_xaxes(title_text=trace.labels.xlabel, row=x, col=y)
        fig.update_yaxes(title_text=trace.labels.ylabel, row=x, col=y)

    return fig


def create_axes(nrows: int, ncols: int) -> np.ndarray:
    row = np.arange(1, nrows + 1)
    col = np.arange(1, ncols + 1)
    return np.array(list(itertools.product(row, col)))


def overlay_histogram(
    df: pd.DataFrame,
    x: str,
    hue: str,
    transform: Callable[..., Any],
    to_replace: dict | None = None,
    exclude: list = [],
    **kwds,
) -> list[BaseTraceType]:
    data = df[[x, hue]].dropna()
    hue_feature = data[hue].astype(str)

    if to_replace is not None:
        hue_feature = hue_feature.replace(to_replace)

    fig = px.histogram(
        x=transform(data[x]), color=hue_feature, nbins=30, **kwds
    )
    return list(fig.select_traces())


def overlay_boxplot(
    df: pd.DataFrame,
    x: str,
    hue: str,
    transform: Callable[..., Any],
    to_replace: dict | None = None,
    **kwds,
) -> list[BaseTraceType]:
    data = df[[x, hue]].dropna()
    hue_feature = data[hue].astype(str)

    if to_replace is not None:
        hue_feature = hue_feature.replace(to_replace)

    fig = px.box(
        x=transform(data[x]), y=hue_feature, color=hue_feature, **kwds
    )
    return list(fig.select_traces())


PRIMARY_COLOR = "#636efa"
BLUE_CMAP = sns.dark_palette(color=PRIMARY_COLOR, as_cmap=True)
PALETTES = dict(dark=sns.dark_palette, light=sns.light_palette)


def cmap2hexlist(
    color: str = PRIMARY_COLOR, tone: str = "dark", n_colors: int = 1500
) -> list[str]:
    palette = PALETTES[tone]
    cmap = palette(color, as_cmap=True)
    hex_values = []

    for i in range(n_colors + 1):
        rgb = (np.array(cmap(i)) * 255).astype(int)[:-1]
        hex = cm.rgb2hex(*rgb)
        hex_values.append(hex)

    return hex_values
