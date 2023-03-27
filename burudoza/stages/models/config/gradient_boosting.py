from burudoza.stages.models.config.config import (
    ModelConfig,
    Param,
    RadioArgs,
    SliderArgs,
    WidgetType,
)

GradientBoostingConfig = ModelConfig(
    default={
        "max_features": "log2",
        "min_samples_leaf": 9,
        "subsample": 0.7,
        "validation_fraction": 0.25,
    },
    description="""
    __Random Forest__ and __Extra Trees__ belong to the __Bagging__ class of the ensemble method. Another type of ensemble is __Boosting__, with a well-known implementation called __Gradient Boost__.
    
    Trees in __Gradient Boost__ are sequential instead of independent. Training starts with a naive model, usually predicting the mean for all samples. The model calculates the residuals using the predictions, i.e., the difference between an actual value and a predicted one.
    
    Next, __Gradient Boost__ fits a new base model on these residuals, usually a tree-based one. To re-emphasize, this new model learns from the residuals of the previous one (the naive one) instead of the actual target values.
    
    This newly trained model produces predicted residuals. These values are scaled by the __learning rate__, a faction used to avoid overfitting. Then, __Gradient Boost__ computes new predictions by adding the naive model's result to the predicted residuals.
    
    The process is repeated—each subsequent tree attempts to optimize the residuals of its predecessor. Training stops when adding more trees does not improve the performance or when the requested number of trees is satisfied.
    
    For a thorough explanation: <https://www.youtube.com/watch?v=3CC4N4z3GJc>
    
    For a mathematical walk-through: <https://www.youtube.com/watch?v=2xudPOBz-vs&t=1077s>
    """,
    params=dict(
        learning_rate=Param(
            args=SliderArgs(
                label="Learning rate",
                value=0.05,
                min_value=0.01,
                max_value=1.0,
                step=0.01,
                help="Learning rate determines how to scale the resulting trees. A high learning rate converges faster but easily overfits.",
            ),
            column=0,
            widget=WidgetType.slider,
            depend=False,
        ),
        max_depth=Param(
            args=SliderArgs(
                label="Depth of each tree",
                value=16,
                min_value=3,
                max_value=30,
                step=1,
                help="Higher values increase accuracy but slow down the execution time and is prone to overfit.",
            ),
            column=0,
            widget=WidgetType.slider,
            depend=False,
        ),
        n_estimators=Param(
            args=SliderArgs(
                label="Number of iterations",
                value=150,
                min_value=100,
                max_value=200,
                step=10,
                help="Higher values increase accuracy but slow down the execution time and is prone to overfit.",
            ),
            column=0,
            widget=WidgetType.slider,
            depend=False,
        ),
        subsample=Param(
            args=SliderArgs(
                label="Fraction of samples for each tree",
                value=0.7,
                min_value=0.0,
                max_value=1.0,
                step=0.1,
                help="Higher values increase accuracy but slow down the execution time and is prone to overfitting.",
            ),
            column=1,
            widget=WidgetType.slider,
            depend=False,
        ),
        n_iter_no_change=Param(
            args=SliderArgs(
                label="The number of rounds of without changes",
                value=10,
                min_value=5,
                max_value=30,
                step=5,
                help="How many iterations of no improvement to wait before interrupting.",
            ),
            column=1,
            widget=WidgetType.slider,
            depend=True,
        ),
        early_stopping=Param(
            args=RadioArgs(
                label="Early stopping conditions",
                index=0,
                options=[True, False],
                help="Whether to stop training if the evaluation score does not improve.",
            ),
            column=1,
            widget=WidgetType.radio,
            depend=False,
        ),
    ),
)
