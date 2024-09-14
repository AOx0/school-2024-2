# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# %%
# Años de una persona con el salario que tiene
df = pd.read_csv("/home/ae/Downloads/Salary.csv")
df.head()

# %%
# El proceso es un poco distinto porque tenemos que hacer un reshape de los datos.
X = np.array(df["YearsExperience"]).reshape(-1, 1)
y = np.array(df["Salary"]).reshape(-1, 1)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, train_size=0.7, random_state=101
)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

# Puede explical el 82% de la varianza?
print(f"""
MSE: {mean_squared_error(y_test, y_pred)}
RMSE: {np.sqrt(mean_squared_error(y_test, y_pred))}
R2: {r2_score(y_test, y_pred)}
""")

# %%
# Cada año de experiencia cuánto se mueve el valor del salario.
print(model.coef_)

# %%
# Valor de la intersección
print(model.intercept_)

# Es decir que:
# salario = 4482 * anos + 30582

# %%
# Hay un arreglo con los coeficientes
slope = model.coef_[0][0]
intercept = model.intercept_

# %%
# No es como wolfram donde solo le damos la función y la grafica
# tenemos que hacerlo a mano
X_line = np.linspace(X.min(), X.max(), 100).reshape(-1, 1)

# %%
# Evaluamos nuestra función dado ese número de datos generados
y_line = slope * X_line + intercept

plt.scatter(X, y, color="blue", label="Datos")
plt.plot(X_line, y_line, color="red", label="Regression line")

plt.xlabel("Years of experience")
plt.ylabel("Salary")
plt.title("Linear Regression Model")

plt.legend()
plt.show()

# %%
# Ahora graficamos también el promedio

plt.scatter(X, y, color="blue", label="Datos")

# %%
# Estamos mostrando el promedio. Cómo podemos cuantificar qué tan bueno es el promedio en comparación con el modelo?
# - El error de nuestro modelo es la suma de todos los errores evaluados al cuadrado
# - El error del primedio es igual la suma de las diferencias con el promedio
# - Dividimos las doc cifras como $R^2 = SSres/SStot$
#
# Mientras más cerca estemos al 0 peor, mientras más se acerque a 100 es mejor
#
# Reglas:
# - Si R^2 = 1 probablemente está mal, y sea un sobreajuste
# - Cercano a 1 el modelo es bueno
# - Si es cercano a 0, en lugar del modelo vale la pena solo reportar el promedio
# - Si da negativo está mal hecho
plt.axhline(y=y.mean(), color="g", linestyle="--", label="Average")
plt.plot(X_line, y_line, color="red", label="Regression line")

plt.xlabel("Years of experience")
plt.ylabel("Salary")
plt.title("Linear Regression Model")

plt.legend()
plt.show()


# %%
# La distribución de los residuos podría ser normal porque los puntos siguen un patrón
# aleotorio alrededor de 0
# Como el residuo no se abre ni cierra en forma de embudo podemos decir que es Homoscedatico?
residuals = y - model.predict(X)
plt.figure(figsize=(10, 6))
plt.scatter(X, residuals, color="purple", alpha=0.5)
plt.axhline(y=0, color="red", linestyle="--")
# plt.table('Residuals plot')
plt.xlabel("X")
plt.ylabel("Residuals")
plt.show()

# %%
# La distribución de los residuos parece estar un poco sesgada
residuals = residuals.reshape(1, -1)[0]
res_df = pd.DataFrame({"residuals": residuals})
sns.kdeplot(res_df, x="residuals")
plt.show()

# %%
(osm, osr), (slope, intercept, r) = stats.probplot(residuals, dist="norm", plot=plt)
sns.set(style="whitegrid")
plt.title("Q-Q Plot")
plt.xlabel("Teoretical quantiles")
plt.ylabel("Data quantiles")
plt.show()

# %%
# Los puntos parecen seguir la distribución normal, con un poco de separación lo que indica sesgo
statistics, p_value = stats.shapiro(residuals)

print(f"Estadistico: {statistics}")
print(f"Valor P: {p_value}")

# %%
# Los residuos podrían seguir una distribución normal
alpha = 0.05
if p_value < alpha:
    print("Rechazamos la hipótesis nula, los datos no siguen una distribución normal")
else:
    print(
        "Fallamos en rechazar la hipótesis nula. Los datos podrían seguir una distribución normal"
    )

# Por las pruebas que hicimos, donde:
# - visualizamos los datos gracias a que pueden ser mostrados en 1 sola dimensión
# - Los datos están aleatoriamente rodenando el 0 sin hacerse embudo
# - El histograma de los residuos muestra una especie de distribución normal
# - El Q-Q muestra a los residuos siguiendo la recta de la distribución normal
# - La prueba de Shapiro- no pueden negar que los datos no siguen una distribución normal


# Correlación de Pearson
df.corr()

sns.heatmap(df.corr(), annot=True)
