import pathlib
from functools import singledispatch
from typing import Callable, Literal, TypeAlias, TypeVar, cast

import pandas as pd
import streamlit as st
from decorator import decorator
from pandas.io.formats.style import Styler

from burudoza.directories import CONTENT_DIR


def display_content(
    filename: str | pathlib.Path, default_dir: pathlib.Path | None = None
) -> None:
    if default_dir is None:
        default_dir = CONTENT_DIR
        filename = default_dir / filename

    with open(filename) as f:
        st.markdown(f.read())


def display_header(header: str, level: int = 1) -> None:
    prefix = "#" * level
    st.markdown(f"{prefix} {header}")


def display_note(note: str):
    st.caption(f"__NOTE__: {note}")


DeltaColor: TypeAlias = Literal["normal", "inverse", "off"]


def display_metric(
    metric: float,
    label: str,
    name: str | int,
    smaller_better: bool = False,
    help: str = "",
) -> None:
    if smaller_better:
        caption = "Smaller is better."
        delta_color = "inverse"
    else:
        caption = "Larger is better."
        delta_color = "normal"

    previous = st.session_state.get(name, 0)

    st.metric(
        label,
        metric,
        delta=round(metric - previous, 5),
        delta_color=cast(DeltaColor, delta_color),
    )

    caption += "\n" + help
    st.caption(caption)

    st.session_state[name] = metric


DATAFRAME_STYLE = {
    "border-width": "3px",
    "font-family": "system-ui",
    "font-size": "14.5px",
}


@singledispatch
def set_style(arg: pd.DataFrame | Styler) -> Styler:
    raise NotImplementedError(type(arg))


@set_style.register
def style_styler(styler: Styler) -> Styler:
    return styler.pipe(
        lambda s: s.format(precision=4, na_rep=" ").set_properties(
            **DATAFRAME_STYLE
        )
    )


@set_style.register
def style_dataframe(df: pd.DataFrame) -> Styler:
    return df.style.format(precision=4, na_rep=" ").set_properties(
        **DATAFRAME_STYLE
    )


R = TypeVar("R")


@decorator
def styleit(streamlit_func: Callable[..., R], *args, **kwargs) -> R:
    # copy to avoid modifying passed arguments
    kwds = kwargs.copy()
    try:
        data = kwds.pop("data")
    except KeyError:
        data, *rest = args
    else:
        rest = args  # type: ignore

    styled = set_style(data)

    return streamlit_func(styled, *rest, **kwds)
