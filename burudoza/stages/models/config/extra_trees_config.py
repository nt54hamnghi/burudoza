from burudoza.stages.models.config.config import (
    ModelConfig,
    Param,
    RadioArgs,
    SliderArgs,
    WidgetType,
)

ExtraTreesConfig = ModelConfig(
    default={
        "bootstrap": True,
        "min_samples_leaf": 3,
        "min_samples_split": 5,
        "n_jobs": -1,
    },
    description="""
    _For the explanation on __Random Forest__ and base models, please choose __Random Forest__ under \"Select Model\"_.
    
    __Extra Trees__ is a variant of __Random Forest__. One substantial difference between the two models is the choice of base models. While __Random Forest__ uses the conventional __Decision Tree__, __Extra Trees__ takes advantage of another tree-based learner, also called __Extra Tree__ but in the singular form.
    
    __Extra Tree__ selects the split condition for a node randomly instead of exhaustively. Thanks to this random nature, its execution time is significantly faster. The short processing time comes with the cost of low accuracy. Randomly picking a decision means neglecting the difference between data points. To compensate, an __Extra Tree__ learns on all data points (a __Decision Tree__ in __Random Forest__ fits on only a subset). However, the implementation below allows changing the fraction of data points to make it flexible.
    
    Finally, empirical evidence shows that in cases where __Random Forest__ overfits severely, __Extra Trees__ is more resilient.
    
    [More information](https://quantdare.com/what-is-the-difference-between-extra-trees-and-random-forest/)
    """,
    params=dict(
        bootstrap=Param(
            args=RadioArgs(
                label="Bootstrap Condition",
                options=[True, False],
                index=1,
                help='Whether subset samples for each tree. If "No", each tree will use all samples.',
            ),
            column=1,
            widget=WidgetType.radio,
            depend=False,
        ),
        max_depth=Param(
            args=SliderArgs(
                label="Depth of each tree",
                value=35,
                min_value=0,
                max_value=50,
                step=5,
                help="Higher values increase accuracy but slow down the execution time and is prone to overfit. Setting to 0 means you let the algorithm choose the optimal depth. Hence, trees won't have the same depth.",
            ),
            column=0,
            widget=WidgetType.slider,
            depend=False,
        ),
        max_features=Param(
            args=SliderArgs(
                label="Maximum fraction of variables used at each node",
                value=0.5,
                min_value=0.3,
                max_value=1.0,
                step=0.1,
                help="How many features to consider as a split candidate at each node. Fewer features can increase randomness, making the model resilient to overfitting. More features can increase accuracy but is prone to overfitting.",
            ),
            column=0,
            widget=WidgetType.slider,
            depend=False,
        ),
        max_samples=Param(
            args=SliderArgs(
                label="Maximum fraction of samples for each tree",
                value=0.5,
                min_value=0.3,
                max_value=1.0,
                step=0.1,
                help="Higher values increase accuracy but slow down the execution time and is prone to overfitting.",
            ),
            column=1,
            widget=WidgetType.slider,
            depend=True,
        ),
        n_estimators=Param(
            args=SliderArgs(
                label="Number of trees",
                value=30,
                min_value=1,
                max_value=100,
                step=1,
                help="The more trees, the higher accuracy, but the slower training time. Setting to 1 simulates one single tree",
            ),
            column=0,
            widget=WidgetType.slider,
            depend=False,
        ),
    ),
)
