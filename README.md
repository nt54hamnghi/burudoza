# Introduction

Interactive Web Application is live at: <http://app.burudoza.com>

The project aims at analyzing and building a machine-learning model capable of predicting auction sales of industrial bulldozers. The data includes information about bulldozers, including model, capacity, measurements, date, etc. It is available on [Kaggle](https://www.kaggle.com/c/bluebook-for-bulldozers/data)

## Stage 1: Data Preprocessing

The first step is cleaning up the data so downstream models can process it.

### Categorical Encoding

A categorical variable has a finite set of possible values. Some examples are zip code, gender, and occupation, but most machine learning models do not have native support for categorical data.

One solution is to replace each category with the target means for that category. In simple words, for all samples with group `i`, we take the average of the target variable and replace `i` with that newly calculated mean. We repeat this for all groups of each categorical column. This approach may cause target leakage. To prevent it, we smooth out the encoded values. The algorithm for smooth is quite technical, but an intuitive explanation is available at: <https://maxhalford.github.io/blog/target-encoding/>

### Missing Value Handling

Missing values, also called NA values, cause the same problems, i.e., they are incompatible with models. There are various techniques to handle these NAs, but, in our case, simple imputing (filling) with the mean is sufficient. Simply put, for each column with missing values, we substitute those NA values with the column's average. We choose simple imputing because if a product (bulldozer) does not have a particular feature (e.g., air conditioner, enclosure, etc.), it makes no sense to seek a filled-in value. In other cases, for example, regarding the height or weight of a patient (everyone must have these measurements), using a model-based method to fill out missing values is preferable.

Also, missingness is sometimes meaningful. Hence, it is better to preserve it after imputing it. A viable way is to create a boolean column, called a missing indicator, for each column with missing values.

### Date Time Parsing

The date-time data in the data set is under the format of `mm/dd/yyyy hour: minute`. Besides, some samples even have timezone information but account for only .3% of the total count, so it is acceptable to ignore the timezone part.

One option is to express it in different columns. In other words, we divide the original column into five columns denoting month, day, year, hour, and minute. Moreover, we can extract other valuable features such as `day_in_week`, `is_month_start`, `is_month_end`, etc.

## Stage 2: Model Building

### Modeling

In this stage, we will build nine different tree-based models, compare them, and pick the best one. Tree models are favorable because they are complex enough to capture non-linear patterns and, at the same time, simple enough to not overfit too badly. Also, this complexity level is easily adjustable.

The nine models are:

- [Extra Trees](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.ExtraTreesRegressor.html#sklearn.ensemble.ExtraTreesRegressor)
- [Random Forest](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html)
- [Tranditional Gradient Boosting](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.GradientBoostingRegressor.html#sklearn.ensemble.GradientBoostingRegressor)
- [Histogram-baseed Gradient Boosting](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.HistGradientBoostingRegressor.html#sklearn.ensemble.HistGradientBoostingRegressor)
- [LightGBM](https://www.microsoft.com/en-us/research/wp-content/uploads/2017/11/lightgbm.pdf)
- [LightGBM with GOSS (Gradient One-sided Sampling)](https://www.microsoft.com/en-us/research/wp-content/uploads/2017/11/lightgbm.pdf)
- [LightGBM with DART (Dropouts Meet Multiple Additive Regression Tree)](https://arxiv.org/abs/1505.01866)
- [Catboost](https://arxiv.org/abs/1706.09516)
- [Catboost's Ordered Boosting](https://arxiv.org/abs/1706.09516)

### Evaluation Metric

Also, we need a metric to evaluate the performance, and for this use case, we will use **RMSLE** (Root Mean Squared Log Error). Its formula is:

$$\sqrt{\frac{1}{n}\sum_{i=1}^{n}(log(yh_{i}+1)-log(y_{i}+1))^{2}}$$

- List item

Where:

- n is the number of samples.
- y is the response value
- yh is the predicted value
- i is the sample index

**RMSLE** penalizes underestimation heavier than overestimation, making it suitable for the price-predicting task. Generally, although we prefer an accurate model, over-predicting is tolerable because it makes it somewhat flexible to manage the budget. On the other hand, underestimating the price could result in undesirable circumstances such as sale loss or failed purchases, thus should be avoided.

For more information: <https://medium.com/analytics-vidhya/root-mean-square-log-error-rmse-vs-rmlse-935c6cc1802a>

Another selling point of tree-based models is that they can produce feature importances, which is extremely useful in determining the contribution of each feature. These importances also help narrow down the features we should focus our analysis on in the next stage.

## Stage 3: EDA - Explonatory Data Analysis

Using the feature set filtered from the previous stage, we will plot different kinds of graphs to analyze the relationship between these features and the response.

### Univariate, Bivariate, and Trivariate plots

- Univariate graphs help determine the distribution and find outliers.
- Bivariate plots can make the relationships between features and the target variable transparent, which could be valuable in constructing new features.
- Trivariate graphs help find and remove co-linearity, i.e., feature redundancy.

### SHAP values

Shapley Additive exPlanation, abbreviated as SHAP, is an algorithm used to reverse-engineer and explain the model's output. The interpretability of SHAP also helps to pinpoint the patterns not revealed by conventional graphs. The SHAP paper is at: <https://arxiv.org/abs/1705.07874>
