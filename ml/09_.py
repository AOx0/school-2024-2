# %%
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, auc
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier

plt.style.use('theme.mplstyle')
pd.set_option('display.max_columns', None)

# %%
df = pd.read_csv('/home/ae/Downloads/TelcoChurn.csv')

df.head()

# %%
# Vamos a convertir No a 0 y yes a 1
# Lo hacemos para generar la curva ROC
mapper = {
    'No': 0,
    'Yes': 1,
}

df['Churn'] = df['Churn'].map(mapper)

# %%
# balanceo
df_majority = df[df['Churn'] == 0]
df_minority = df[df['Churn'] == 1]
df_majority_downsampled = df_majority.sample(n=len(df_minority), random_state=101)

# Tomamos el dataset ya balanceado
df_balanced = pd.concat([df_majority_downsampled, df_minority])
df_balanced = df_balanced.sample(frac=1, random_state=101).reset_index(drop=True)
df = df_balanced

df.head()

# %%
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
df.isnull().sum()

# %%
df.dropna(inplace=True)

# %%
mapper = {
    0: 'Non-senior',
    1: 'Senior',
}

df['SeniorCitizen'] = df['SeniorCitizen'].map(mapper)

#

# %%
# Tiramos la columna del ID
df.drop('customerID', axis=1, inplace=True)

df.head()

# %%
X = df.drop('Churn', axis=1)
y = df['Churn']

X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.75, random_state=101)

# %%
numerical_features = X.select_dtypes(include=['int64', 'float64'])
categorical_features = X.select_dtypes(exclude=['int64', 'float64'])

numerical_transformer = StandardScaler()
categorical_transformer = OneHotEncoder(drop='first')



# %%
preprocesador = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, numerical_features.columns),
        ('cat', categorical_transformer, categorical_features.columns)
    ]
)

model = Pipeline(
    steps=[
        ('preprocesor', preprocesador),
        ('class', XGBClassifier(n_estimators=400, learning_rate=0.01))
    ]
)
# %%
model.fit(X_train, y_train)
y_pred = model.predict(X_test)


# %%
# Si se ejecuta o no la celda de balanceo la métrica será mayor o menor, como vimos en la
# clase 07_clasify.py
#
# Con XGB con un learning rate más bajo podemos ver que si aumenta el poder de predicción
# sobre la clase no representada.
#
# Cuando balanceamos el set vemos que definitivamente sube el poder de predicción sobre ambas clases
print(classification_report(y_test, y_pred))


# %%
sns.heatmap(confusion_matrix(y_test,y_pred),annot=True, fmt = ".2f")


# %%
# Un modelo tiene que ser idealmente un ROC que es un triangulo
# Un 0.72 es mejor que ver el rendimiento sobre las dos clases
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
#



# %%
feature_names = model.named_steps["preprocesor"].get_feature_names_out()
feature_names

# %%
feature_importance = model.named_steps['class'].feature_importances_
feature_importance


# %%
importance_df = pd.DataFrame(
    {
        'feature': feature_names,
        'importance': feature_importance
    }
)

importance_df = importance_df.sort_values(by='importance', ascending=False)
importance_df
