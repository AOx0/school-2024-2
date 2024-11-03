# %%
import pandas as pd
import numpy as np
from pandas.core.common import random_state
import xgboost as xgb
import seaborn as sns
import matplotlib.pyplot as plt

pd.set_option("display.max_columns", None)

plt.style.use('theme.mplstyle')

df = pd.read_csv('/home/ae/Downloads/TelcoChurn.csv')
# df = pd.read_csv('Data set/TelcoChurn.csv')
df.head()
# %%
df.isnull().sum()
# %%
df.info()
# %%
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
# %%
df.isnull().sum()
# %%
df.dropna(inplace=True)
# %%
mapper = {
    0: "Non-Senior",
    1: "Senior"
}

df["SeniorCitizen"] = df["SeniorCitizen"].map(mapper)
df.head()

# %%
mapper = {
    "No": 0,
    "Yes":1,
}

df["Churn"] = df["Churn"].map(mapper)
df.head()

# %%
df.drop("customerID",axis=1, inplace=True)
# %%
sns.kdeplot(data=df,x="tenure", hue= "Churn", fill=True)
# %%
sns.kdeplot(data=df,x="MonthlyCharges", hue= "Churn", fill=True)
# %%
sns.pairplot(df, hue="Churn")
# %%
sns.countplot(x="gender",data = df, hue="Churn")

# %%
sns.countplot(x="Contract",data = df, hue="Churn")
# %%
sns.countplot(x="Dependents",data = df, hue="Churn")
# %%
sns.countplot(x="PaymentMethod",data = df, hue="Churn")

# %%
sns.countplot(x="SeniorCitizen",data = df, hue="Churn")

# %%
sns.boxplot(data = df, y ="tenure", hue = "Churn")
# %%
sns.boxplot(data = df, y ="MonthlyCharges", hue = "Churn")
# %%
sns.countplot(x="PaymentMethod",data = df, hue="Churn")

# %%
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, auc
import numpy as np

# %%
X = df.drop("Churn", axis=1)
y = df["Churn"]
X_train, X_test, y_train, y_test = train_test_split(X,y,train_size = 0.75,random_state = 101)
# %%
numerical_features = X.select_dtypes(include=["int64", "float64"])
categorical_features = X.select_dtypes(exclude=["int64", "float64"])

numerical_transformer = StandardScaler()
categorical_transformer = OneHotEncoder(drop="first")

# %%
from sklearn.ensemble import RandomForestClassifier
procesador = ColumnTransformer(
    transformers=[
        ("numerical", numerical_transformer, numerical_features.columns),
        ("categorical", categorical_transformer, categorical_features.columns)

])
model = Pipeline(
    steps=[
        ("preprocessor", procesador),
        ("rf", RandomForestClassifier(n_estimators=200))
    ]
)
model.fit(X_train, y_train)
# %%
y_pred = model.predict(X_test)
print(classification_report(y_test,y_pred))
#No son metricas tan buenas cuando es un problema binario mejor presicion en 0 que en 1
# %%
sns.heatmap(confusion_matrix(y_test,y_pred),annot=True, fmt = ".2f")


# %%
fpr, tpr, _ = roc_curve(y_test, y_pred)

roc_auc = auc(fpr, tpr)

plt.figure(figsize=(8,6))
plt.plot(fpr, tpr, color="darkorange", label = f"ROC Curve (AUC = {roc_auc:.2f}")
plt.plot([0,1],[0,1], color = "lightblue",linestyle="--")
plt.xlim([0.0,1.0])
plt.ylim([0.0,1.05])
plt.xlabel("False positive Rate")
plt.ylabel("True positive Rate")
plt.title("ROC")
plt.legend(loc = "lower right")
plt.grid(True)
plt.show()
# %%
coefficients = model.named_steps["logreg"].coef_[0]
coefficients

# %%
feature_names = model.named_steps["preprocessor"].get_feature_names_out()
feature_names

# %%
datos = {
    'feature': feature_names,
    'coefficient':coefficients
}

coeficientes = pd.DataFrame(datos)
coeficientes.sort_values(by='coefficient',ascending=False,inplace=True)
coeficientes


# %%
df.dtypes
