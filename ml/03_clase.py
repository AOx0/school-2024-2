# %%
# Bagging

# %%
# Recordemos que podíamos ver cómo se sobreajusta el arbol de decisión.
# Tienden a sobreajusterse muy facil con una profundidad muy grande
# Vamos a hacer una adaptación, vamos a sustituir nuestro arbol de decisión a
#
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor

plt.style.use('theme.mplstyle')

# %%
# Gastos medicos de una persona y sus características
# - Entender qué features pueden servir para predecir charges
df = pd.read_csv('/home/ae/Downloads/insurance_2.csv')
df.head()

# %%
# Tiene un sesgo
sns.kdeplot(df, x='charges', fill=True)

# %%
# Podemos ver que puede ser que fumar si afecte
# Sin embargo, es claro que hay un desbalance
sns.kdeplot(df, x='charges', fill=True, hue='smoker')

# %%
df['smoker'].value_counts()

# %%
# Edad numérica de la edad vs los cargos. O sea, afecta la edad en lo que gastas?
# Si parece que existe una correlación positiva. Pero sin embargo también hay 3 grupos
# en las categorías
sns.scatterplot(df, x='age', y='charges')

# %%
# No parece existir una distinción de gastos entre géneros
sns.scatterplot(df, x='age', y='charges', hue='sex')

# %%
# Los que fuman gastas más, y a medida que pasa la edad
sns.scatterplot(df, x='age', y='charges', hue='smoker')

# %%
# Indice de masa corporal puede afectar los gastos médicos? Por generar complicaciones?
# Pareciera que hay un grupo
sns.scatterplot(df, x='bmi', y='charges')

# %%
# El género no parece ser algo que afecte
sns.scatterplot(df, x='bmi', y='charges', hue='sex')

# %%
# En cambio, si fuma si afecta
sns.scatterplot(df, x='bmi', y='charges', hue='smoker')

# %%
# Las medianas son iguales, practicamente. Pareciera que si afecta un poco más si
# eres hombre, pero es nulo casi casi
sns.boxplot(df, y='charges', hue='sex')

# %%
# Si hacemos lo mismo con la de fumadores, vemos que si afecta mucho.
# Lo atipico de los que no fuman es gastar lo que gasta en promedio un fumador,
# es evidente el desplaso
sns.boxplot(df, y='charges', hue='smoker')

# %%
# Puede ser que si fumas no tienes hijos, porque hay más gasto.
sns.boxplot(df, y='charges', hue='children')

# %%
#
sns.kdeplot(df, x='charges', fill=True, hue='children')

# %%
sns.boxplot(df, y='charges', hue='region')

# %%
X = df.drop('charges', axis=1)
y = df['charges']

# %%
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.7, random_state=101)

# %%
numerical_features = X.select_dtypes(include=['int64', 'float64'])
categorical_features = X.select_dtypes(exclude=['int64', 'float64'])

numerical_transformer = StandardScaler()
categorical_transformer = OneHotEncoder(drop='first')

# %%
# Decision tree vs random forest:
    # - Uno es un bosque de árboles que se agarran de las manitas y dicen cuál es el mejor valor.
    # Hace muchos datasets para muchos árboles. De forma que ningún árbol ha visto el mismo set
    # de datos. No es tan interpretable, pero los árboles de

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, numerical_features.columns),
        ('cat', categorical_transformer, categorical_features.columns)
    ]
)

# %%
# Con decision trees todo era numérico, por eso no ocupamos un Pipeline
# En este caso los pre-procesamos y después se lo pasamos al árbol
model = Pipeline(
    steps= [
        ("preprocessor", preprocessor), # Preprocesamos todo
        ("regressor", RandomForestRegressor()),
    ]
)

model.fit(X_train, y_train)

# %%
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print(f'''
Metricas
MSE: {mse}
RMSE: {rmse}
R2: {r2}
''')

# %%
# No es posible un diagrama porque son muchos valores (arboles)
# Por defecto son 100 árboles que deciden.
# Ventajas:
    # - No se sobreajusta
    # - Como se hace split de features para reducir el error, se puede cuantificar qué features
    # reducen más el error (importan más, feature importance). Tal vez no podamos graficar y entenderlo
    # visualmente, pero podemos ver los features más importantes.

# Vamos las categorías que vió el modelo y sacamos el score de importancia
feature_names = np.array(model.named_steps['preprocessor'].get_feature_names_out()) # Extraer datos del pipeline
print(feature_names)

# %%
# Obtenemos los scores normalizados, la suma da 1. El valor más grande importa más porque
# reduce el error de forma más agresiva
feature_importances = model.named_steps['regressor'].feature_importances_
print(feature_importances)

# %%
# Es evidente que fumar si tiene importancia si fumas, seguido del indice de masa corporal y la edad
# Es de las formar más fáciles de explicar modelos, sin embargo va a afectarlo la carnalidad de la
# variable (cuántos valores posibles tiene).
# Limitante: la explicalidad es global, no nos permite exponer qué pasa para una sola persona (explicabilidad local)
idf = pd.DataFrame(
    {
        'feature': feature_names,
        'importance': feature_importances
    }
)

idf = idf.sort_values(by='importance', ascending=False)
print(idf)
