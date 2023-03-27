from enum import StrEnum, auto
from typing import TypedDict


class WidgetType(StrEnum):
    radio = auto()
    slider = auto()


class RadioArgs(TypedDict):
    label: str
    options: list[str | float | bool]
    index: int
    help: str


class SliderArgs(TypedDict):
    label: str
    value: float | None
    min_value: float | None
    max_value: float | None
    step: float | None
    help: str


class Param(TypedDict):
    args: RadioArgs | SliderArgs
    column: int
    widget: WidgetType
    depend: bool


class ModelConfig(TypedDict):
    default: dict[str, float | bool | str]
    description: str
    params: dict[str, Param]
