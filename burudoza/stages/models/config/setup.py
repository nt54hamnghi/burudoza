from typing import Any, Callable, TypeAlias

import streamlit as st
from sklearn.ensemble import (
    ExtraTreesRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor,
)
from streamlit.delta_generator import DeltaGenerator
from burudoza.stages.models.config.config import ModelConfig, WidgetType

from burudoza.stages.models.config.extra_trees_config import ExtraTreesConfig
from burudoza.stages.models.config.gradient_boosting import (
    GradientBoostingConfig,
)
from burudoza.stages.models.config.random_forest_config import (
    RandomForestConfig,
)
from burudoza.utils.display import display_note


def setup(config: ModelConfig, layout: list[DeltaGenerator]):
    description = config["description"]
    configurable = config["params"]
    default = config["default"]

    with st.expander("See explanation"):
        st.markdown(description)

    hyperparams: dict[str, Any] = dict()

    for param_name, value in configurable.items():
        args = value["args"]
        column = value["column"]

        if not value["depend"]:
            widget = layout[column]
            if value["widget"] == WidgetType.slider:
                hyperparams[param_name] = widget.slider(**args)
            elif value["widget"] == WidgetType.radio:
                hyperparams[param_name] = widget.radio(**args)

    return default | hyperparams


TreeBasedRegressor: TypeAlias = (
    RandomForestRegressor | ExtraTreesRegressor | GradientBoostingRegressor
)
SetupFunction: TypeAlias = Callable[[], TreeBasedRegressor]


def random_forest_setup():
    layout = st.columns(2)
    hyperparams = setup(RandomForestConfig, layout)
    # if max_depth is 0, then set it to None
    hyperparams["max_depth"] = hyperparams["max_depth"] or None

    return RandomForestRegressor(**hyperparams)


def extra_trees_setup():
    layout = st.columns(2)
    hyperparams = setup(ExtraTreesConfig, layout)
    # if max_depth is 0, then set it to None
    hyperparams["max_depth"] = hyperparams["max_depth"] or None

    if hyperparams["bootstrap"]:
        max_samples = ExtraTreesConfig["params"]["max_samples"]
        widget = layout[max_samples["column"]]
        hyperparams["max_samples"] = widget.slider(**max_samples["args"])

    return ExtraTreesRegressor(**hyperparams)


def gradient_boosting_setup():
    layout = st.columns(2)
    hyperparams = setup(GradientBoostingConfig, layout)

    if hyperparams["early_stopping"]:
        n_iter_no_change = GradientBoostingConfig["params"][
            "n_iter_no_change"
        ]
        widget = layout[n_iter_no_change["column"]]
        hyperparams["n_iter_no_change"] = widget.slider(
            **n_iter_no_change["args"]
        )

    hyperparams.pop("early_stopping")

    display_note(
        """Due to the sequential nature, Gradient Boost is relatively slow. For 200 iterations, it takes around 120 to 180 seconds to complete. You can decrease the iteration count to make it faster; however, you should also increase the learning rate to achieve a comparable accuracy."""
    )

    return GradientBoostingRegressor(**hyperparams)
