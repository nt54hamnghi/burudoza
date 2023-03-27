from burudoza.stages.models.config.config import (
    ModelConfig,
    Param,
    SliderArgs,
    WidgetType,
)

RandomForestConfig = ModelConfig(
    default={
        "bootstrap": True,
        "min_samples_leaf": 3,
        "min_samples_split": 5,
        "n_jobs": -1,
    },
    description="""
    __Random Forest__ is an ensemble model comprising several independent simple models, also called base model, and the typical base model of __Random Forest__ is __Decision Tree__.

    A tree consists of nodes and leaves connected by branches. A top node is called the root, the subsequent nodes are internal nodes, and the ones with no outcoming branches are leaves, short for leaf nodes. Each node has a binary split/decision that defines how to travel to the next node. This sequence of splits divides the data into multiple groups, each with a special pattern that can describe the target variable.
    
    __Decision Tree__ finds the best decision by iterating through all the values of an explanatory variable and repeats it for all variables. The metric determining the quality of a split depends on the users, but common ones for regression are squared error and absolute error, and for classification are impurity and entropy. _To simulate a __Decision Tree__, set \"Number of trees\" to 1_

    However, A __Decision Tree__ suffers from overfitting due to its exhaustive searching nature. __Random Forest__ solves this problem. Each tree in a __Random Forest__ learns on a random subset of data, usually called a bag, and it can overfit however it wants, and it will produce errors on other unseen bags. By aggregating these random errors, the overall forest does have severe biases for any specific data subsets. On a higher level, combining several trees means collecting and incorporating multiple aspects of the data.

    The final prediction is the average of the base models' outcomes. In other words, all base models have an equal say in the final result.

    For more information:
    * [Decision Tree](https://en.wikipedia.org/wiki/Decision_tree_learning)
    * [Random Forest](https://en.wikipedia.org/wiki/Random_forest)
    """,
    params=dict(
        max_depth=Param(
            args=SliderArgs(
                label="Depth of each tree",
                value=35,
                min_value=0,
                max_value=50,
                step=5,
                help="Higher values increase accuracy but slow down the execution time and is prone to overfit. Setting to 0 means you let the algorithm choose the optimal depth.\n Hence, trees won't have the same depth.",
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
            column=1,
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
            column=0,
            widget=WidgetType.slider,
            depend=False,
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
            column=1,
            widget=WidgetType.slider,
            depend=False,
        ),
    ),
)
