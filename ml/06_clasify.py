#t  %%
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, auc
from sklearn.linear_model import LogisticRegression
from sklearn.utils.validation import _get_feature_names

plt.style.use('theme.mplstyle')

# %%
df = pd.read_csv('/home/ae/Downloads/IRIS.csv')
df.head(5)

# %%
df['species'].unique()

# %%
df: pd.DataFrame = df[df['species'] != 'Iris-setosa']
df['species'].value_counts()

# %%
#
mapper = {
    'Iris-versicolor': 1,
    'Iris-virginica': 0,
}

df['species'] = df['species'].map(mapper)
df.head()

# %%
# Todos son features numericos, asi que vamos a comparar por especie. Podemos ver que
# hay algunos en los que parece que podemos partir con lineas rectas. Por lo tanto, en términos de
# dimensiones, se pueden separar a simple vista.
#
sns.pairplot(df, hue='species')

# %%
# Construimos un pipeline de procesamiento, todo completo aunque no se ocupe de todo, como
# lo de escalar
#
# queremos producir 'species', asi que va a se la Y
X = df.drop('species', axis=1)
y = df['species']

# %%
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.7, random_state=101)

# %%
numerical_features = X.select_dtypes(include=['int64', 'float64'])
categorical_features = X.select_dtypes(exclude=['int64', 'float64'])

numerical_transformer = StandardScaler()
categorical_transformer = OneHotEncoder(drop='first')

# %%

preprocesador = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, numerical_features.columns),
        ('cat', categorical_transformer, categorical_features.columns),
    ]
)

# %%
model = Pipeline(
    steps=[
        ('preprocessor', preprocesador),
        ('logreg', LogisticRegression()),
    ]
)

# %%
model.fit(X_train, y_train)

# %%
y_pred = model.predict(X_test)

# %%
# Vemos que es un modelo perfecto
print(classification_report(y_test, y_pred))

# %%
sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt='.2f')

# %%
# Ahora vamos a calcular las tasas de verdaderos positivos (tpr) y falsos positivos (fpr)
# para diferentes puntos de corte en el modelo de clasificación. Esto nos permitirá evaluar
# la capacidad del modelo para discriminar entre las clases a distintos umbrales.
# fpr = false positive rate
fpr, tpr, _ = roc_curve(y_test, y_pred)

# Área bajo la curva (AUC) es una métrica que indica la capacidad del modelo
# para clasificar correctamente las clases. Un valor más cercano a 1 implica un mejor desempeño.
roc_auc = auc(fpr, tpr)

plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, color='darkorange', label= f'ROC Curve (AUC = {roc_auc:.2f})')
plt.plot([0, 1], [0, 1], linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC')
plt.legend(loc='lower right')
plt.grid(True)
plt.show()

# %%
# Ahora vamos a extraer los coeficientes de las regresiones lineales (peso y valor del feature)

# Coeficientes de la regresión logística
coefficients = model.named_steps['logreg'].coef_[0]

feature_names = model.named_steps['preprocessor'].get_feature_names_out()
feature_names

#
coefficients = pd.DataFrame({
    'feature': feature_names,
    'coefficient': coefficients
})

coefficients.sort_values(by='coefficient', ascending=False, inplace=True)
coefficients.head()

# %%
