import logging
from inspect import getfullargspec
from typing import Any, Callable, Sequence

import numpy as np
import pandas as pd
from sklearn.exceptions import NotFittedError
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from .helper import create_logger


def rmse_score(y_true, y_pred):
    return mean_squared_error(y_true, y_pred) ** 0.5


EVAL_LOGGER = create_logger("evaluate", "evalutate.log", level=logging.ERROR)
DEFAULT_METRICS = [rmse_score, mean_absolute_error, r2_score]


def evalutate(
    estimator: Any,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    eval_fns: list[Callable[..., float]] = DEFAULT_METRICS,
    round_ndigits: int = 5,
) -> np.ndarray:
    try:
        y_pred = estimator.predict(X_test.values)
    except NotFittedError as err:
        EVAL_LOGGER.error(err)
        raise err
    else:
        scores = np.empty_like(eval_fns, dtype=float)

        for idx, score in enumerate(eval_fns):
            args_spec = getfullargspec(score).args

            if args_spec != ["y_true", "y_pred"]:
                message = f"{score.__name__} does not contain argument specifications: {args_spec}"  # NOQA
                EVAL_LOGGER.error(message)
                raise ValueError(message)

            scores[idx] = round(score(y_test.values, y_pred), round_ndigits)

    return scores


def get_feature_importances(
    features: Sequence[str],
    importance: list[float],
    threshold: float = 1.0,
) -> pd.DataFrame:
    if not 0 <= threshold < 1:
        raise ValueError(f"Invalid threshold {threshold}")

    fi = pd.DataFrame(dict(features=features, importance=importance))
    fi.set_index("features", inplace=True)

    # include pareto analysis
    fi.sort_values(by="importance", ascending=False, inplace=True)

    fi["rank"] = np.arange(1, len(fi) + 1)
    fi["norm_cummulative"] = fi["importance"].cumsum() / fi.importance.sum()

    # cut off base on pareto analysis
    fi = fi[fi.norm_cummulative <= threshold]
    fi.columns = ["Importance", "Rank", "Normalized Cummulative"]

    return fi
