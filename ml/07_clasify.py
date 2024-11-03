# %%
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier

plt.style.use('theme.mplstyle')
pd.set_option('display.max_columns', None)

# %%
df = pd.read_csv('/home/ae/Downloads/TelcoChurn.csv')
df.head()

# %%
# churn = que han cancelado su servicio/plan
df['Churn'].value_counts().plot(kind='bar')

# %%
# Pareciera que no hay columnas nulas pero despues vemos que hay una numerica
# que tiene valres ' '
df.isnull().sum()

# %%
df.info()

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

# %%
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
# Tiramos la columna del ID
df.drop('customerID', axis=1, inplace=True)

# %%
df.head()

# %%
# Hay personas que al mes pagaba mucho.
# Hay muchas personas que con el paso del tiempo pagan menos
sns.pairplot(df)

# %%
# Hay más personas cuyos contratos duran más.
# Las personas que se quedaron suelen tener contratos más altos.
# Los que no se quedaron suelen tener contratos más bajos
# La gente que se queda no paga tanto, pero muchos suelen pagar mucho
# No hay nada significativo, quiza por cuánto dura el contrato
sns.pairplot(df, hue='Churn')

# %%
# Más o menos hay mitad y mitad hombres y mujeres
sns.countplot(x='gender', data=df, hue='Churn')

# %%
# Parece que el contrato que más hace probable que las personas se vayan es el tipo de contrato,
# el mensual es más probable que deje los servicios
sns.countplot(x='Contract', data=df, hue='Churn')

# %%
# Cuánto dura tu contrato en meses influye en si te vas a ir o no. Si tu contrato es
# mensual es más probable que te vayas.
sns.boxplot(data=df, y='tenure', hue='Churn')

# %%
# Parece ser que las personas que se han ido tienen una media en la que pagan más
# que respecto con los clientes que si duran.
# Puede deberse a que sea porque los planes a largo plazo tengan descuentas con el
# precio final
sns.boxplot(data=df, y='MonthlyCharges', hue='Churn')
# %%
# Los cargos totales, basados en el pairplot de arriba, presenta correlación, es lo que esperamos.
# TODO: Fix
sns.boxplot(data=df, y='TotalCharges', hue='Churn')



# %%
# Si eres adulto mayor eres más propenso a irte
sns.countplot(x='SeniorCitizen', data=df, hue='Churn')

# %%
# Parece ser que las personas que no tienen hijos son más propensas a darse de baja
# O sea que a la empresa le toca ver cómo retener a los que no tienen hijos.
sns.countplot(x='Dependents', data=df, hue='Churn')
# %%
# Es evidente que las personas que usan cheques electrónicos suelen ser los que más
# abandonan el plan. Puede ser que es debido a que los cheques tienen que expedirse cada vez
sns.countplot(x='PaymentMethod', data=df, hue='Churn')

# %%

df.dtypes

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
        ('class', RandomForestClassifier(n_estimators=300))
    ]
)
# %%
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# %%
print(classification_report(y_test, y_pred))

# %%
feature_names = model.named_steps["preprocesor"].get_feature_names_out()
feature_names

# %%
coefficients = model.named_steps["class"].feature_importances_
coefficients

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

importance_df = importance_df.sort_values(by='importance', ascending=True)
importance_df

# %%
df_majority = df[df['Churn'] == 0]
df_minority = df[df['Churn'] == 1]
df_majority_downsampled = df_majority.sample(n=len(df_minority), random_state=101)

# Tomamos el dataset ya balanceado
df_balanced = pd.concat([df_majority_downsampled, df_minority])
df_balanced = df_balanced.sample(frac=1, random_state=101).reset_index(drop=True)
df = df_balanced


# %%

# %%
df['Churn'].value_counts().plot(kind='bar')

# %%
# Y ahora que está balanceado vuelve a mostrar todas las graficas
# Ve que definitivamente se van más los seniors
# Etc
#
# Volviendo a ejecutar el modelo vemos que perdimos precision en general
# pero sin embargo ahora es buena para las dos categorias
