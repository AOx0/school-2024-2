import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
# Lo vamos a usar para escalar los datos
from sklearn.preprocessing import StandardScaler

from scipy import stats

plt.style.use('theme.mplstyle')

# Tiene 4 columnas y queremos ver cuál es la que tiene más relación
df = pd.read_csv("/home/ae/Downloads/Advertising.csv")
df.head()

# Tiene que existir una tendencia en la regresión lineal. Aqui vamos a hacer lo mismo con cada variable

# Ventas con tv pareciera tener una tendencia, por ejemplo. Las 3 variables en mayor o menor medida pueden ser
# modeladas como una linea
sns.pairplot(df)

# Nos da una matriz de correlación usando el coeficiente de correlación de pearson
df.corr()

# Nos da una escala de color, mientras más beige mejor correlación
# Intuición: Vale la pena tener ventas y Tele porque una unidad de tele sube 0.78 de ventas?
# Recordemos que va de -1 a 1. 0 es nulo.
# Las ventas parecen influir porque tienen correlaciones altas
sns.heatmap(df.corr(), annot=True)

# La distribución en ventas es más o menos una distribución normal y no hay valores atipicos
# (montes en los bordes de la distribución)
# No hay valores atípicos
sns.kdeplot(df, x='sales', fill=True)

# La gráfica de caja tampoco muestra valores atipicos en las ventas
sns.boxplot(df, y='sales')

# TV, radio y newspaper van a ser las variables independientes
# El valor a predecir es 'sales'. La columna a predecir se pone al final para
# poder separarla del resto de datos de forma sencilla
df.columns

# Quitamos la columna del final, de forma que las variables independientes quedan
# separadas
X = df.drop(df.columns[-1], axis=1)
y = df['sales']

# Dividimos
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.7, random_state=101)

# Estandarizamos
scaler = StandardScaler()

# Si calculamos la media y hacemos el escalamiento en base a ella
X_train_s = scaler.fit_transform(X_train)
# No volvemos a calcular la media de los datos de test para evitar leak
X_test_s = scaler.transform(X_test)
X_train_s[:3]

# Entrenamos
model = LinearRegression()
model.fit(X_train_s, y_train)
y_pred = model.predict(X_test_s)

# Evaluamos


# El periódico no tiene efecto para redecir las ventas
# Se puede eliminar en el negocio y aplicar ese dinero en otras áreas
# El error es += 1.51, esta prediciendo bien
# El R2 nos indica que el modelo cubre un 91.85 % de los datos, el otro 9 porciento
# de los datos se explican de otra forma, no con este modelo.
print(f"""
    Coeficientes: {model.coef_}
    Intercepto: {model.intercept_}
    RMSE: {np.sqrt(mean_squared_error(y_test, y_pred))}
    R2: {r2_score(y_test, y_pred)}
""")

# Se tiene que usar el mimso set de datos ya escalados
residuals = y_test - model.predict(X_test_s)
residuals.values
residuals

# Los residuos deben ser homonoseque y seguir la recta cuando se le haga la
# diferencia a los valores predecidos
#
# Si sigue un patrón aleatorio
# Si es homoes_no_se_que (no se abre/cierra)
plt.figure(figsize=(10, 6))
plt.scatter(y_test, residuals, color='purple', alpha=0.5)
plt.axhline(y=0, color='red', linestyle='--')
plt.title('Residuals Plot')
plt.xlabel('Predicted Values')
plt.ylabel('Residuals')
plt.show()

# Ahora hacemos el histograma
residuals = (y_test - model.predict(X_test_s)).values.reshape(1,-1)[0]
res_df = pd.DataFrame({'residuals': residuals})
sns.kdeplot(res_df, x='residuals', fill=True)
plt.show()

# Se abre un poco hacia las colas, lo que puede sugerir que no son completamente
# homoge_no_se_que
#
# Puede que necesitemos otro acercamiento más complejo
(osm, osr), (slope, intercept, r) = stats.probplot(residuals, dist='norm', plot=plt)
sns.set(style='whitegrid')
plt.title('Q-Q Plot')
plt.xlabel('Theoretical Quantiles')
plt.ylabel('Data Quantiles')
plt.show()

# Ahora vamos a hacer una prueba de hipótesis para ver si los datos provienen de
# una distribución normal
# Tenemos tantas herramientas como podamos para justificar si se debe o no usar un modelo
# lineal
#
# Prueba de hipótesis de correlación
statistic, p_value = stats.shapiro(residuals)
print(f"""
    Estadístico: {statistic}
    Valor P: {p_value}
""")

alpha = 0.05 # 95% de confianza

if p_value < alpha:
    print("Rechazamos la hipotesis nula: los datos no siguen una distribución normal")
else:
    print("Fallamos en rechazar la hipótesis nula. Los datos podrían seguir una \
distribución normal")

# Conclusión: La regresión lineal tiene sentido, estamos siguiendo todos los principios que hemos
# visto.

# El modelo es válido para los datos que nos dieron.
