# %%
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Nuevos imports
# No es una clasificación, sino que una regresión
from sklearn.tree import DecisionTreeRegressor, plot_tree

# %%
plt.style.use('theme.mplstyle')
df = pd.read_csv('/home/ae/Downloads/AnxietyPerformance_Univar.csv')

sns.scatterplot(df, x='anxiety', y='performance')

# %%
df.describe()

# %%
X_train, X_test, y_train, y_test = train_test_split(
    df[['anxiety']], # X ojo que tiene doble corchete
    df[['performance']], # y
    train_size=0.7,
    random_state=101
)

# %%
# Primero la regresión lineal
lreg = LinearRegression()
lreg.fit(X_train, y_train)

# Después la regresión con árboles
# Cortamos la profundidad del arbol
#
# Con más profundidad queda más ajustado el modelo final
# Podemos ver cómo casi casi como dibuja punto por punto. Entonces es necesario
# no tener una profundidad muy cañona
treg = DecisionTreeRegressor(max_depth=3)
treg.fit(X_train, y_train)

# %%
# Vamos a generar un espacio de números que nos deje ver exactamente qué hace el modelo
t_anisiedad = np.linspace(df['anxiety'].min(), df['anxiety'].max(), 500).reshape(-1, 1)

# Alimentamos nuestro modelo con los datos aleatorios generados
perf_lreg = lreg.predict(t_anisiedad)
perf_treg = treg.predict(t_anisiedad)

# %%
# Graficamos el comportamiento de los datos
# -- Hicmos un modelo que nos devuelve el promedio. Podemos extrapolar
# La gente que casi no ... tuvieron 15
# Ansiedad de 3-3.x van a tener un performance de
plt.figure(figsize=(10,6))
plt.scatter(df['anxiety'], df['performance'], edgecolors='black', label='Datos', color='gray', alpha=0.6)
plt.plot(t_anisiedad, perf_lreg, color='blue', label='Performance Reg Lineal', linewidth=2, linestyle='-')
plt.plot(t_anisiedad, perf_treg, color='crimson', label='Performance Reg Lineal', linewidth=2, linestyle='--')
plt.title('Reg tree vs Linear reg')
plt.xlabel('Nivel de ansiedad (1-10)')
plt.ylabel('Performance Score')
plt.legend()
plt.show()


# %%
plt.figure(figsize=(12,8))
plot_tree(treg, feature_names=['anxiety'], filled=True, rounded=True, fontsize=10)
plt.title('Model Reg Tree')
plt.show()

# %%
perf_rtree_datos = treg.predict(X_test)
perf_ltree_datos = lreg.predict(y_test)

mse_tree = mean_squared_error(y_test, perf_rtree_datos)
r2_tree = r2_score(y_test, perf_rtree_datos)
rmse_tree = np.sqrt(mse_tree)


mse_lin=mean_squared_error(y_test, performance_lin_reg_datos)
r2_lin = r2_score(y_test, performance_lin_reg_datos)
rmse_lin = np.sqrt(mse_lin)



print(f""""
Metricas Regresion Lineal
RMSE:{rmse_lin:2f}
MSE: {mse_lin:2f}
R2:{r2_lin:2f}


Metricas Regresion Tree
RMSE:{rmse_tree:2f} # use the correctly calculated rmse_tree
MSE: {mse_tree:2f}
R2:{r2_tree:2f}
""")

# %%
plt.figure(figsize=(10,6))
plt.scatter(df['anxiety'], df['performance'], edgecolors='black', label='Datos', color='gray', alpha=0.6)
plt.plot(t_anisiedad, perf_lreg, color='blue', label='Performance Reg Lineal', linewidth=2, linestyle='-')
plt.plot(t_anisiedad, perf_treg, color='crimson', label='Performance Reg Lineal', linewidth=2, linestyle='--')
for split_value in treg.tree_.threshold[treg.tree_.threshold > 0]:
