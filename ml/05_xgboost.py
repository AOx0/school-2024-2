# %%
from pyexpat import features

import pandas as pd
import numpy as np
import xgboost as xgb
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_squared_error, r2_score

# %%
plt.style.use('theme.mplstyle')
df = pd.read_csv('/home/ae/Downloads/insurance_2.csv')

# %%
df.head()

# %%
df.info()

# %%
df.describe().T

# %%
sns.boxplot(x='charges', data=df)

# %%
X = df.drop('charges', axis=1)
y = df['charges']
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=101, train_size=0.7)

# %%
numerical_features = X.select_dtypes(include=["int64", "float64"])
categorical_features = X.select_dtypes(exclude=["int64", "float64"])

numerical_transformer = StandardScaler()
categorical_transformer = OneHotEncoder(drop="first")

# %%
procesador = ColumnTransformer(
    transformers=[
        ("numerical", numerical_transformer, numerical_features.columns),
        ("categorical", categorical_transformer, categorical_features.columns)

])
model = Pipeline(
    steps=[
        ("preprocessor", procesador),
        ("regressor", xgb.XGBRegressor(objective='reg:squarederror',
                                       learning_rate = 0.1,
                                       max_depth = 5,
                                       n_estimators=1000))
    ]
)
model.fit(X_train, y_train)

# %%
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print(f"""
METRICAS
MSE: {mse},
RMSE: {rmse},
R2 Score: {r2}
""")

# %%
feature_names = np.array(model.named_steps['preprocessor'].get_feature_names_out())
feature_names

# %%
feature_importances = model.named_steps['regressor'].feature_importances_
feature_importances

# %%
importance_df = pd.DataFrame(
    {
    'feature': feature_names,
    'importance':feature_importances
}
)
importance_df = importance_df.sort_values('importance', ascending=False)
importance_df


# %%
