# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor

plt.style.use('theme.mplstyle')
np.random.seed(101)

# %%
X = np.linspace(-10, 10, 15000).reshape(-1, 1)
y = X ** 2 + np.random.normal(0, 10, size=X.shape)

# %%
df = pd.DataFrame({'X': X.flatten(), 'y': y.flatten()})

# %%
X_train, X_test, y_train, y_test = train_test_split(df[['X']], df[['y']], train_size=0.7, random_state=101)

# %%
plt.scatter(X_test, y_test, color='blue', label='Test data')
plt.axhline(y=y_test.mean().values[0], color='green', linestyle='--', label='average of y')
plt.xlabel('X')
plt.ylabel('y')
plt.legend()
plt.show()

# %%

linear_model = LinearRegression()
linear_model.fit(X_train, y_train)
y_pred_linear = linear_model.predict(X_test)

# %%
# El modelo de regresión lineal simplemente no es bueno. Vamos a hacer xgboost, para eso
# - Calculamos el promedio
# - Generamos un arbol que tenemos que usar para predecir el residuo
#
# Tenemos el promedio + el ajuste del arbol entrenado
plt.scatter(X_test, y_test, color='blue', label='Test data')
plt.scatter(X_test, y_pred_linear, color='red', linestyle='--', label='Regresión lineal')
plt.axhline(y=y_test.mean().values[0], color='green', linestyle='--', label='average of y')
plt.xlabel('X')
plt.ylabel('y')
plt.legend()
plt.show()

# %%
# Estimators: el numero de arboles, no se hace en paralelo con bagging sino
# que se usa boosting
model = XGBRegressor(objective='reg:squarederror', max_depth=3, learning_rate=0.1, n_estimators=1000)
model.fit(X_train, y_train)


fig, ax = plt.subplots(3, 4, figsize=(18, 10))
ax = ax.flatten()

trees_to_plot = [1, 2, 5, 10, 20, 30, 50, 100, 250, 300, 750, 1000]

for i, num_trees in enumerate(trees_to_plot):
    y_pred = model.predict(X, iteration_range=(0, num_trees))
    ax[i].scatter(X, y, label='Datos', color='lightblue')
    ax[i].plot(X, y_pred, color='red', label=f'Predicciones luego de {num_trees} arboles')
    ax[i].axhline(y=y_test.mean().values[0], color='green', linestyle='--', label='Average of y')

    rmse = np.sqrt(mean_squared_error(y, y_pred))
    r2 = r2_score(y, y_pred)
    ax[i].set_title(f'Arboles {num_trees} | RMSE {rmse:.2f} | R2 {r2:.2f}')
    ax[i].legend()

plt.tight_layout()
plt.show()

# XGBoost parte de predecir el promedio. Después va haciendo ajustes con learning rates



# %%
# Con el learning rate muy grande el modelo lo hace mucho más agresivo
# Boost: Tenemos secuencias de waek learners que van prediciendo sobre el error del weak
# learner pasado
model = XGBRegressor(objective='reg:squarederror', max_depth=3, learning_rate=0.5, n_estimators=1000)
model.fit(X_train, y_train)

fig, ax = plt.subplots(3, 4, figsize=(18, 10))
ax = ax.flatten()

trees_to_plot = [1, 2, 5, 10, 20, 30, 50, 100, 250, 300, 750, 1000]

for i, num_trees in enumerate(trees_to_plot):
    y_pred = model.predict(X, iteration_range=(0, num_trees))
    ax[i].scatter(X, y, label='Datos', color='lightblue')
    ax[i].plot(X, y_pred, color='red', label=f'Predicciones luego de {num_trees} arboles')
    ax[i].axhline(y=y_test.mean().values[0], color='green', linestyle='--', label='Average of y')

    rmse = np.sqrt(mean_squared_error(y, y_pred))
    r2 = r2_score(y, y_pred)
    ax[i].set_title(f'Arboles {num_trees} | RMSE {rmse:.2f} | R2 {r2:.2f}')
    ax[i].legend()

plt.tight_layout()
plt.show()
