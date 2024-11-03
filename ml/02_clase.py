# %%
import numpy as np
import pandas as pd
from scipy.stats import alpha
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor, plot_tree
from sklearn.metrics import mean_squared_error, r2_score


# %%

plt.style.use('theme.mplstyle')
df = pd.read_csv('/home/ae/Downloads/AnxietyPerf_V2.csv')
df.head()

# %%
sns.scatterplot(df, x='sleep_hours', y='performance')

# %%
sns.scatterplot(df, x='anxiety', y='sleep_hours', hue='performance', palette='magma')

# %%
X = df.drop('performance', axis=1)
y = df['performance']

X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.7, random_state=101)

regressor = DecisionTreeRegressor(max_depth=3)
regressor.fit(X_train, y_train)

# %%
y_train_pred = regressor.predict(X_train)
y_test_pred = regressor.predict(X_test)

# %%
# Si le subimos a el valor de max_depth podemos tener mejor rendimiento durante
# el entrenamiento pero peor rendimiento con los de prueba.
# Es decir, se sobreajustó. Tenemos que ver que estén a la par el rendimiento en
# entrenamiento y en prueba
print(f'''
MSE Test: {mean_squared_error(y_test, y_test_pred):.2f}
MSE Train: {mean_squared_error(y_train, y_train_pred):.2f}
R2 Test: {r2_score(y_test, y_test_pred):.2f}
''')

# %%
plt.figure(figsize=(12,8))
plot_tree(regressor, feature_names=['anxiety', 'sleep_hours'], filled=True, rounded=True)
plt.title('Model Reg Tree')
plt.show()

# %%
# Generamos una malla que pasa por todos los puntos de los datos originales
# Vamos a crear un arreglo que cubre todos los puntos
x_min, x_max = X.iloc[:, 0].min() - 1, X.iloc[:,0].max() + 1
y_min, y_max = X.iloc[:, 1].min() - 1, X.iloc[:,1].max() + 1

xx, yy = np.meshgrid(np.arange(x_min,x_max, (x_max-x_min)/100),
                     np.arange(y_min,y_max, (y_max-y_min)/100)
)
# %%
Z = regressor.predict(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)

# %%
# Mostramos la interpretación que generó, las fronteras de explicación. Similar a lo que
# mostraba el scatter del inicio
#
# Podemos ver cómo el cuadrante y su color indican más o menos cúanto ganaríamos
# Cuando aumentamos o disminuimos el nivel de profundidad podemos notar gráficamente el sobreajuste.
# En teoría los colores deberían estar de acuerdo a lo que indica el fondo.
# Pero en la práctica, los puntos tienen colores distintos al fondo. Y en el caso del sobreajust,
# el color del fondo y de la bola es muy diferente cuando es el set de prueba.
#
plt.figure(figsize=(12,9))
n_regions = len(np.unique(Z))
contour = plt.contour(xx, yy, Z, levels=n_regions, alpha=0.8, cmap='viridis')

cbar = plt.colorbar(contour, label='Predicted Value')

scatter_train = plt.scatter(X_train.iloc[:,0], X_train.iloc[:,1], c=y_train, cmap='viridis', edgecolor='black', label='Training Data')

plt.legend()
plt.tight_layout()
plt.show()


# %%
def get_leaf_nodes(tree, feature_names):
    leaf_nodes = []
    def recurse(node, depth, path):
        if tree.feature[node] != -2:
            feature = feature_names[tree.feature[node]]
            threshold = tree.threshold[node]
            recurse(tree.children_left[node], depth + 1, path + [(feature, threshold, '≤')])
            recurse(tree.children_right[node], depth + 1, path + [(feature, threshold, '>')])
        else:
            leaf_nodes.append((path, tree.value[node][0][0]))
    recurse(0, 0, [])
    return leaf_nodes

# %%

feature_names = X.columns.tolist()
leaf_node = get_leaf_nodes(regressor, )
