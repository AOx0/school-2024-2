# %%
from __future__ import all_feature_names
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score

# %%
# Hay una columna que parece estar al azar. Vamos a ver si importa para
# el momento de modelar, deberían ser discriminados sin que hagamos nada
df = pd.read_csv('/home/ae/Downloads/Advertising Reloaded Regul.csv')
df['pais'] = np.random.choice(['USA', 'Mexico', 'Jamaica'], size=len(df))
df.head()

# %%
# Cuando tenemos categorías numéricas y categóricas tenemos que aislarlas para poder
# hacer la matriz de correlación
numerical = df.select_dtypes(include=['int64', 'float64']).columns
corr = df[numerical].corr()
sns.heatmap(corr, annot=True)

# %%
#
def pares_correlacionados():
    for i, j in ((i, j) for i in range(len(corr.columns)) for j in range(i)):
        if abs(corr.iloc[i,j]) > 0.7:
            yield (
                corr.columns[i],
                corr.columns[j],
                corr.iloc[i,j]
            )

for (f1, f2, c) in pares_correlacionados():
        print(f"Alta correlacion entre {f1} y {f2}: {c}")

# %%
X = df.drop('sales', axis=1)
y = df['sales']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.70, random_state=42)

# %%
numerical = X.select_dtypes(include=['int64', 'float64'])
categorical = X.select_dtypes(exclude=['int64', 'float64'])

numerical_transformer = StandardScaler()
categorical_transformer = OneHotEncoder(drop='first')

# %%
# Una función que recibe modelo y pipeline, y va a reconstruir la ecuación del
# modelo final para poder entender el modelo

def ecuacion_modelo(pipeline: Pipeline, feature_names):
    preprocessor = pipeline.named_steps['preprocessor']
    regressor = pipeline.named_steps['regressor']

    coef = regressor.coef_
    intercepto = regressor.intercept_

    # Porque tenemos que recontruir todo
    feature_names_out = preprocessor.get_feature_names_out()

    print(f'{type(regressor).__name__} Regression Model Equation: ')
    equation = f'y = {intercepto:.4f}'

    for i, feature in enumerate(feature_names_out):
        if coef[i] != 0:
            # En Ridge nunca llega a 0 el coef, pero si se queda cerquita
            equation += f'+ {coef[i]:.4f} x {feature}'
    print(equation)

    # Imprimir todo
    print()
    print("Feature coeficients:")
    for i, feature in enumerate(feature_names_out):
        print(f'{feature}: {coef[i]:.4f}')

# %%
# Tiene que tener el mismo nombre que los usados en la función
preprocesador = ColumnTransformer(transformers=[
    ("num", numerical_transformer, numerical.columns),
    ("cat", categorical_transformer, categorical.columns)
])

model = Pipeline(
    steps=[
        ("preprocessor", preprocesador),
        ("regressor", LinearRegression())
    ]
)

model.fit(X_train, y_train)

# %%
y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print(f"""
MSE: {mse}
RMSE: {rmse}
R2: {r2}
""")

# %%
# Ridge
preprocesador = ColumnTransformer(transformers=[
    ("num", numerical_transformer, numerical.columns),
    ("cat", categorical_transformer, categorical.columns)
])

model = Pipeline(
    steps=[
        ("preprocessor", preprocesador),
        ("regressor", Ridge())
    ]
)

model.fit(X_train, y_train)

all_features = numerical.columns + categorical.columns
ecuacion_modelo(model, all_features)

# %%
# Lasso
# Interpretable para negocios, pero aún tenemos matriz dispersa
# Justificación: Lo demás no importa según el modelo
preprocesador = ColumnTransformer(transformers=[
    ("num", numerical_transformer, numerical.columns),
    ("cat", categorical_transformer, categorical.columns)
])

model = Pipeline(
    steps=[
        ("preprocessor", preprocesador),
        ("regressor", Lasso())
    ]
)

model.fit(X_train, y_train)

all_features = numerical.columns + categorical.columns
ecuacion_modelo(model, all_features)

# Hay que hacer la misma verificación de los errores para asegurar que un modelo
# lineal hace sentido. Aunque sea reducido por Lasso
