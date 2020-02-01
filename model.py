import numpy as np
import pandas as pd
from mord import LogisticAT
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.metrics import make_scorer, mean_absolute_error, mean_squared_error


df = pd.read_csv('/Users/bharathc/Desktop/Projects/Econometrics/final_regression_data.csv')

# instantiate models
model_linear = LinearRegression()
model_1vR = LogisticRegression(multi_class='ovr', class_weight='balanced', solver='lbfgs')
model_multi = LogisticRegression(multi_class='multinomial', solver='lbfgs', class_weight='balanced', max_iter=1000)
model_ordinal = LogisticAT(alpha=0)  # alpha parameter set to zero to perform no regularisation

# divide df into features matrix and target vector
features = df.iloc[:, :-1]  #all except quality
target = df['TIER']

MAE = make_scorer(mean_squared_error)
folds = 5

print('Mean absolute error:' )
MAE_linear = cross_val_score(model_linear,
    features,
    target,
    cv=folds,
    scoring=MAE)
print('Linear regression: ', np.mean(MAE_linear))
MAE_1vR = cross_val_score(model_1vR,
    features,
    target,
    cv=folds,
    scoring=MAE)
print('Logistic regression (one versus rest): ', np.mean(MAE_1vR))
MAE_multi = cross_val_score(model_multi,
    features,
    target,
    cv=folds,
    scoring=MAE)
print('Logistic regression (multinomial): ', np.mean(MAE_multi))
MAE_ordinal = cross_val_score(model_ordinal,
    features,
    target,
    cv=folds,
    scoring=MAE)
print('Ordered logistic regression: ', np.mean(MAE_ordinal))
