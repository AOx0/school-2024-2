import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# No vamos a partir entre set de prueba y de entraniemnto.

df = pd.read_csv("/home/ae/Downloads/ansc.csv")
df = pd.DataFrame(df[["x123", "x4", "y1", "y2", "y3", "y4"]])
df.head()

# Los datos son medio lineales
sns.scatterplot(df, x="x123", y="y1")

# Los datos no son lineales. Es cuadrática. Una linea recta no pasa por todos los puntos.
# Intentar formar nua línea genera un error muy grande
sns.scatterplot(df, x="x123", y="y2")

# Hay un outlier que afcta el modelo, va a causar que la linea no pase por todos los puntos a pesar
# de su clara tendendencia lineal
sns.scatterplot(df, x="x123", y="y3")

# Definitivamente no es linea   l
sns.scatterplot(df, x="x4", y="y4")

# Vamos a crear 4 regresiones lineales entre todas las variables

datos = {
    "Nombre": [],
    "Media": [],
    "Std dev": [],
    "Coeficiente": [],
    "Intercepto": [],
    "RMSE": [],
    "R2": [],
}

# Entrenamos 4 modelos y vamos guardando los valores en el diccionario


def modelo(x, y):
    X = np.array(df[x]).reshape(-1, 1)
    y = np.array(df[y]).reshape(-1, 1)

    model = LinearRegression()
    model.fit(X, y)
    y_pred = model.predict(X)

    datos["Nombre"].append(f'Modelo {len(datos["Nombre"]) + 1}')
    datos["Media"].append(y.mean())
    datos["Std dev"].append(y.std())
    datos["Coeficiente"].append(model.coef_[0][0])
    datos["Intercepto"].append(model.intercept_)
    datos["RMSE"].append(np.sqrt(mean_squared_error(y, y_pred)))
    datos["R2"].append(r2_score(y, y_pred))

    # Vamos a  mostrar la gráfica de los residuos para ver si vale la pena hacer
    # una regresión
    residuals = y - model.predict(X)
    plt.figure(figsize=(10, 6))
    plt.scatter(X, residuals, color="purple", alpha=0.5)
    plt.axhline(y=0, color="red", linestyle="--")
    # plt.table('Residuals plot')
    plt.xlabel("X")
    plt.ylabel("Residuals")
    plt.show()

    residuals = residuals.reshape(1, -1)[0]
    res_df = pd.DataFrame({"residuals": residuals})
    sns.kdeplot(res_df, x="residuals")
    plt.show()

    # Nos permiten confirmar la distribución normal de los residuales, si es que los puntos de residuo
    # siguen la linea roja de distribución normal teórica
    (osm, osr), (slope, intercept, r) = stats.probplot(residuals, dist="norm", plot=plt)
    sns.set(style="whitegrid")
    plt.title("Q-Q Plot")
    plt.xlabel("Teoretical quantiles")
    plt.ylabel("Data quantiles")
    plt.show()

    statistics, p_value = stats.shapiro(residuals)

    print(f"Estadistico: {statistics}")
    print(f"Valor P: {p_value}")

    alpha = 0.05
    if p_value < alpha:
        print(
            "Rechazamos la hipótesis nula, los datos no siguen una distribución normal"
        )
    else:
        print(
            "Fallamos en rechazar la hipótesis nula. Los datos podrían seguir una distribución normal"
        )


# Si no hay un patrón si se puede hacer una regresión lineal
#
# La gráfica de los residuales muestra una campana simétrica.
#   res_df = pd.DataFrame({'residuals': residuals.reshape(1, -1)[0]})
#   sns.kdeplot(res_df, x='residuals')
#
# Como en la gráfica de los residuos se ve como una distribución normal, lo que nos
# dice que cumple como candidato para realizar una regresión lineal
modelo("x123", "y1")

# En cambio con estos otros datos se ve claro el patrón de la curva, lo que sugiere que no se puede
# moldearlo con una regresión lineal
#
# Grafica de residuales: Vemos una distribución sesgada a la izquierda
# Q-q Plot: La linea roja representa una distribución teórica, que es una distribución normal. Si los residuos
# fueran normales entonces estarían todos los puntos sobre la linea roja. Asi nos podemos dar cuenta de si son
# o no una distribución normal. Si los errores intentan seguir la linea sabemos que está más o menos
# normalmente destribuida.
modelo("x123", "y2")
# Gráfico de residuales: No es una distribución normal, sino que está sesgado
# No es simétrico
# Q-q Plot
modelo("x123", "y3")
# Grafica de residuos: Vemos que si es normal, pero el resto de gráficas nos muestran que, en conjunto,
# no se puede realizar una regresión lineal.
#
# Nota: Vale la pena quitar las variables que no cumplen con los requisitos para hacer una regresión
# lineal:
# - Puede que valga la pena hacer modelos distintos para los grupos que causan que no sea válido
# - Tal vez si vale la pena quitarlo, perdiendo un poco de la visión del _mundo_
# Q-q Plot
# Visualmente pareciera que sigue una distribución normal, la gráfica de Q-Q, la prueba de hipótesis, todo
# apunta a que debe ser moldeable con una regresión lineal excepto cuando vemos los datos
modelo("x4", "y4")

# El valor es el mismo para todos los modelos. Media, desviación, RMSE, etc.
# El mismo modelo de regresión lineal para 4 sets distintos de datos
metricas = pd.DataFrame(datos)

sns.regplot(df, x="x123", y="y1")

sns.regplot(df, x="x123", y="y2")

sns.regplot(df, x="x123", y="y3")

sns.regplot(df, x="x4", y="y4")

# Nuestras métricas no son confiables. Esto es peor cuando tenemos muchas dimensiones donde no podemos
# # visualizar la tendencia de los datos
metricas

# Paradoja de Simpson
# - El agregar más puntos de información como variables extras nos puede dar otra forma de interpretar
# los conjuntos de datos.
