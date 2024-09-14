"""
Examen Primer Parcial, Machine Learning

Daniel Alejandro Osornio López
0244685@up.edu.mx

Instrucciones:
- Lee cuidadosamente cada pregunta antes de contestar.
- No se resuelven dudas durante el examen.
- Se permite consultar apuntes, ejercicios previos e internet para contestar el examen.
- Cualquier uso de IA Generativa (ChatGPT, Google Gemini, entre otros) deberá poder ser defendido por el alumno. I.E. El alumno deberá poder explicar claramente lo que el codigo hace durante la clase de revisión de examen. De lo contrario, dicha pregunta quedará anulada.
- Queda prohibido el consultar/apoyar a otros compañeros durante la realizacion del examen.
- El examen debe estar subido a moodle a mas tardar el dia Sabado 2 de Marzo de 2024 a las 11:59 de la noche.
- El unico formato valido para el examen es .ipynb. Es decir, una vez terminen, deberán guardar cambios y descargar su Notebook (File/Download/Download .ipynb) Para posteriormente subir dicho archivo a Moodle NO SE ADMITEN OTROS FORMATOS
- Recordar que la copia en examenes es una falta grave al codigo de la Universidad Panamericana. La acumulación de 2 amonestaciones de este tipo devendrá en la expulsión del alumn@ / alumn@s involucrados
- Cualquier caso de falta disciplinaria será turnado al Comité correspondiente de acuerdo a lo marcado en el Reglamento General de la Universidad Panamericana (Artículos 206 y 207), al Reglamento de la Facultad de Ingeniería (Artículos 86, 206, 207 y 209 ) y al Código de Ética de la Facultad de Ingeniería.

En esta ocasion, intentaremos crear un modelo que prediga la cantidad de seguidores que un influencer podria tener basandonos en los siguientes features:
- Avg_watch_time: La cantidad de minutos promedio que el contenido de dicho influencer es visto en todas las plataformas
- Posts_per_week: La cantidad de publicaciones del influencer por semana
- Avg_likes_per_post: Cantidad promedio de likes por post
- Avg_comments_per_post: Cantidad promedio de comentarios por post
- Account_age_months: Edad de la cuenta del influencer en meses
- Num_collaborations: Numero de colaboraciones de este influencer con otros influencers
- Content_type: El tipo de contenido por el que se le conoce al influencer
- Primary_platform: Plataforma primaria del influencer
- Region: Region donde mas se le conoce al influencer
- Followers: Seguidores del influencer (Variable a Predecir)
- Verificado: Si las cuentas del influencer han sido verificadas

Instrucciones: Cargar el Set de datos "Follower Pred.csv" utilizando la libreria Pandas y realizar lo indicado a continuacion:
1. Determinar si existen valores nulos en los datos provistos
2. Calcular el rango de todas las variables numericas
3. Generar un grafico de caja de la variable a predecir
4. Interpretando los datos del grafico de caja, indicar si existen outliers. Y comentar el potencial efecto que esto podria tener en el modelo de regresion
5. Crear graficos de caja de la variable objetivo divididos por tipo de contenido. Existe una diferencia en terminos de followers con base en el tipo de contenido que generan? (Justificar respuesta mas alla de un "si" o un "no")
6. Crear graficos de caja de la variable objetivo divididos por plataforma primaria. Existe una diferencia en terminos de followers con base en la plataforma? (Justificar respuesta mas alla de un "si" o un "no")
7. Crear graficos de caja de la variable objetivo divididos por region. Existe una diferencia en terminos de followers con base en la region? (Justificar respuesta mas alla de un "si" o un "no")
8. Generar un pairplot coloreado por plataforma principal. Analizar y comentar la aparente relacion entre los features numericos y la variable objetivo (es lineal, no lo es?, etc)
9. Analiza los datos en busca de features constantes o quasi-constantes. En caso de encontrar alguno, tomar nota y considerar ello para el posterior entrenamiento del modelo. Usar value_counts() para variables categoricas
10. Generar una matriz de correlacion para los features numericos. Crear un comentario interpretando los resultados
11. Es hora de buscar multicolinearidad. Analiza el factor de inflacion de varianza de todos los features menos el feature a predecir. Crea un comentario interpretando los resultados observados
12. Busca pares de Features Multicolineales. Consideraremos cualquier par con correlacion mayor a 0.7 como altamente colinear
13. Con esta informacion, deberas entrenar un modelo de regresion lineal. Recuerda justificar (dejando un comentario) la razon/razones por la que consiideraste/ decidiste no considerar ciertos features para el entrenamiento. No olvides escalar varables y codificar categorias
14. Obten las metricas de desempenio del modelo (RMSE, MSE, R2) Interpretar tus resultados
15. Validaremos el modelo generando una grafica de residuos. Interpreta los resultados obtenidos (dejando un comentario de que es lo que crees que implica el ver lo que estas viendo)
16. Genera un histograma de los residuos. Interpreta los resultados obtenidos (dejando un comentario de que es lo que crees que implica el ver lo que estas viendo)
17. Genera un Q-Q Plot de los residuos. Interpreta los resultados obtenidos (dejando un comentario de que es lo que crees que implica el ver lo que estas viendo)
18. Realiiza una prueba de hipotesis Shapiro Wilk sobre la normalidad de los residuos Interpreta los resultados obtenidos (dejando un comentario de que es lo que crees que implica el ver lo que estas viendo)
19. Con base en todo lo desarrollado, explica si tu modelo es valido o no, y las razones por la cuales lo es (o no)
20. Predice la cantidad de followers para un influencer con los siguientes datos: (IMPORTANTE, solo considera los features que utilizaste para entrenar tu modelo para la nueva prediccion. Es decir, si alguna de las columnas aqui mostrada corresponde a un feature que no consideraste, ignorala)
"""

# %%
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly_express as plx
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score
from scipy import stats

# %%
df: pd.DataFrame = pd.read_csv('/home/ae/Downloads/Follower Pred.csv')
df.head()

numerical = [
    'Posts_per_week', 'Avg_watch_time', 'Avg_likes_per_post',
    'Avg_comments_per_post', 'Account_age_months', 'Num_collaborations',
    'Followers'
]
categorical = ['Content_type', 'Region', 'Primary_platform', 'Verificado']

plt.style.use('theme.mplstyle')
pd.options.display.float_format = '{:.10f}'.format

# %%
# 1. Determinar si existen valores nulos en los datos provistos
#
# No existen valores nulos ni NaN
print(df.isna().sum(), end='\n\n')
print(df.isnull().sum())

# %%
# 2. Calcular el rango de todas las variables numericas
print(df[numerical].describe())

ranges: pd.DataFrame = df[numerical].describe()
fig, axes = plt.subplots(nrows=4, ncols=2, figsize=(10, 8), sharex=False, sharey=False)
axes = axes.ravel()  # array to 1D

# Ya sé que pudo ser un boxplot pero me gustó cómo se ve con las curvas de densidad
# Creditos a https://stackoverflow.com/a/63309583 por su excelente forma de graficar
# la distribución con media y desviación estándard
for feature, ax in zip(ranges, axes):
    mean = ranges[feature].iloc[1]
    sdev = ranges[feature].iloc[2]

    # Crear gráfica, es necesario fill=False para poder obtener la línea de datos
    sns.kdeplot(df, x=feature, fill=False, color='crimson', ax=ax)

    kdeline = ax.lines[0]
    xs = kdeline.get_xdata()
    ys = kdeline.get_ydata()

    left = mean - sdev
    right = mean + sdev
    # Dibujar la línea del promedio
    ax.vlines(mean, 0, np.interp(mean, xs, ys), ls=':', color='crimson')

    # Colorear área bajo la curva
    ax.fill_between(xs, 0, ys, color='crimson', alpha=0.2)

    # Colorear región de desviación estándard
    ax.fill_between(xs, 0, ys, where=(left <= xs) & (xs <= right), color='crimson', interpolate=True, alpha=0.2)

fig.tight_layout()
fig.delaxes(axes[7])
plt.show()



# %%
# 3. Generar un grafico de caja de la variable a predecir
#
# Podemos ver que existen muchos valores atípicos, puede que sean los creadores
# de contenido exageradamente grandes, como por ejemplo un MrBeast
sns.boxplot(df, y='Followers')
plt.show()


# %%
# 4. Interpretando los datos del grafico de caja, indicar si existen outliers.
# Y comentar el potencial efecto que esto podria tener en el modelo de regresion.
#
# El grafico de caja muestra una gran presencia de valore atípicos con cantidades enormes
# de seguidores. Estos valores atipicos afectan todas las métricas, como promedio y desviación estándard.
# Esto quiere decir que el intentar dibujar una línea que pase cerca de todos los puntos
# de nuestro _dataset_ se vuelve un poco más complicado.

# %%
# 5. Crear graficos de caja de la variable objetivo divididos por tipo de contenido.
# Existe una diferencia en terminos de followers con base en el tipo de contenido que generan?
#
# Pareciera que hay una mayor cantidad de seguidores en creadores de contenido orientados a la
# tecnología, seguido de los creadores enfocados en la moda. También podemos observar
# que hay una gran cantidad de valores atípicos, con muchos seguidores, para todos los tipos
# de contenido. Esto sugiere que hay unos pocos que tienen muchos seguidores sin importar
# el público objetivo.
sns.boxplot(df, y='Followers', hue='Content_type')
plt.show()

# %%
# 6. Crear graficos de caja de la variable objetivo divididos por plataforma primaria.
# Existe una diferencia en terminos de followers con base en la plataforma?
#
# TikTok tiene la fama de ser más explosivo en cuanto a las vistas y el alcance que tiene,
# a diferencia de otro tipo de plataformas, donde crecer la base de seguidores es más dificil.
# Lo anterior está reflejado en el grafico de caja, donde TikTok parece tener el rango más grande de
# valores atípicos en relación con el resto de plataformas y donde el promedio de seguidores en
# general es mayor que al del resto de plataformas.
# Por el contrario tenemos YouTube que pareciera tener muy pocos creadores de contenido con tantos
# seguidores, con todos los creadores teniendo menos seguidores que en el resto de plataformar
# y con valores atípicos que apenas _le llegan a los talones_ a un creador promedio en TikTok.
sns.boxplot(df, y='Followers', hue='Primary_platform')
plt.show()

# %%
# 7. Crear graficos de caja de la variable objetivo divididos por region.
# Existe una diferencia en terminos de followers con base en la region?
#
# Si parece existir una relación entre la región y el número de seguidores. Los creadores de contenido
# de Europa y Norteamerica tienen un promedio y rango de suscriptores mucho más grande que el resto
# de regiones.
# También se ve reflejado en los valores atípicos. Los seguidores con muchos seguidores son consistentemente
# más grandes que aquellos que no pertenecen a esas regiones. Si eres de Asia o América del Sur parece que
# estás determinado a no poder llegar al nivel de las otras dos regiones.
sns.boxplot(df, y='Followers', hue='Region')
plt.show()

# %%
# 8. Generar un pairplot coloreado por plataforma principal.
# Analizar y comentar la aparente relacion entre los features numericos
# y la variable objetivo (es lineal, no lo es?, etc)
#
# Pareciera, que en todos lados, la presencia de seguidores en TikTok es más fuerte.
# Por lo mismo, la relación es más marcada entre el número de seguidores y la actividad en las redes.
# Por ejemplo, en TikTok afecta mucho que tengas muchos posts, cosa que en YouTube e Instagram no es
# tan relevante, pues el crecimiento es menos marcado, es decir, que la relación lineal tiene una pendiente
# menos pronunciada.
#
# Esto sugiere que en TikTok, a más actividad, más seguidores. En esta plataforma parece existir una
# tendencia lineal entre los distintos features y followers, en especial los posts por semana, el tiempo
# de vista promedio.
#
# En cambio, YouTube e Instagram no tienen una relación tan fuerte entre actividad y followers.
# Esto hace sentido porque en YouTube no importa si subes un video diario, tu crecimiento no depende de eso.
#
# La gráfica de la densidad nos hace ver que es más común tener muchos seguidores en TikTok que en youtube,
# donde el número de persnonas con muchos seguidores es poco en comparación y la gran densidad está en la parte
# en X de pocos seguidores.
sns.pairplot(df, y_vars='Followers', hue='Primary_platform')
plt.show()



# %%
# 9. Analiza los datos en busca de features constantes o quasi-constantes.
# En caso de encontrar alguno, tomar nota y considerar ello para el posterior entrenamiento del modelo.
# Usar value_counts() para variables categoricas
#
#
# Entre los valores categóricos encontramos que verificado es constante, pues todos los valores en el dataset
# contienen ese campo con el valor True, lo que quiere decir que solo recolectaron información de creadores
# de contenido verficados.
#
# En cuanto a los valores continuos, los features numéricos, pareciera que no existe ninguna variable
# quasi-constante, pues su varianza/desviación estándard no es cercana al 0 y es considerablemente
# variable en relación con su correspondiente promedio.

# Feature categóricos
for feature in df[categorical]:
    print(df[feature].value_counts(), end='\n\n')

# Features numéricos
# print("Mean")
# print(df[numerical].mean())
# print()
# print("Std")
# print(df[numerical].std())
# print()
print("Var")
print(df[numerical].var())

# %%
# 10. Generar una matriz de correlacion para los features numericos.
# Crear un comentario interpretando los resultados
#
# Los feature numericos que parecen tener más correlación con la variable a predecir son:
    # - `Post_per_week`
    # - `Num_collaborations`
    # - `Avg_watch_time`
# Aunque ninguna de estas correlaciones es extremadamente fuerte con respecto con la variable objetivo.
#
# Analizando las correlaciones entre estos 3 features podemos ver que `Num_collaborations` tiene una
# correlación muy alta de casi 1 con `Posts_per_week`. Hace sentido, pues si se suben muchos posts
# hay más ventada de posibilidad de que uno de estos posts tengan más colaboraciones.
#
# También existen correlaciones entre otros features no relevantes para determinar el número de followers
# como es la buena correlación entre `Avg_likes_per_post` y `Avg_comments_per_post`, lo cual también hace
# sentido: un video con muchas vistas obviamente tendrá más likes y más comentarios, estas dos variables
# tal vez se podrían resumir en solo un feature `interacción` o algo por el estilo.
sns.heatmap(df[numerical].corr(), annot=True)
plt.show()

# %%
# 11. Es hora de buscar multicolinearidad.
# Analiza el factor de inflacion de varianza de todos los features menos el feature a predecir.
# Crea un comentario interpretando los resultados observados
#
# Analizando los features correlacionados con la variable objetivo, es decir,
# `Post_per_week`, `Num_collaborations` y `Avg_watch_time`, podemos ver que:
    # - `Post_per_week` y `Num_collaborations`: Presentan multicolinearidad, esto puede deberse
    #   a que estos dos features están fuertemente correlacionados entre si.
    #
    # - `Avg_watch_time`: Presenta un colinearidad leve, quizá porque está considerablemente correlacionado
    # con `Avg_likes_per_post` y `Avg_comments_per_post`

datos = sm.add_constant(df[numerical])
datos = datos.drop(columns=['Followers'])
vif_data = pd.DataFrame()
vif_data['Feature'] = datos.columns
vif_data['VIF'] = [
    variance_inflation_factor(datos.values, i) for i in range(datos.shape[1])
]

vif_data


# %%
# 12. Busca pares de Features Multicolineales.
# Consideraremos cualquier par con correlacion mayor a 0.7 como altamente colinear
corr = df[numerical].drop('Followers', axis=1).corr()

# Me dió curiosidad usar un generador jaja
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
# 13. Con esta informacion, deberas entrenar un modelo de regresion lineal.
# Recuerda justificar (dejando un comentario) la razon/razones por la que consideraste/decidiste no considerar
# ciertos features para el entrenamiento.
# No olvides escalar varables y codificar categorias


# %%
wdf = df.copy(deep=True)

# Features que vamos a quitar
rnumerical = [
    'Account_age_months',
    'Avg_likes_per_post',
]

# Features que vamos a mantener
wnumerical = [
    'Posts_per_week',
    'Avg_watch_time',
    'Avg_comments_per_post',
    'Num_collaborations',
    'Followers'
]

# Tiramos las variables que no tienen correlación con nuestra variable objetivo
wdf.drop(
    columns=(
        rnumerical # Alta multicoleanidad/redundancia
        + ['Verificado'] # Es constante
    ),
    inplace=True
)

wdf.head()

# %%
datos = sm.add_constant(wdf[wnumerical]).drop(columns=['Followers'])
vif_data = pd.DataFrame()
vif_data['Feature'] = datos.columns
vif_data['VIF'] = [
    variance_inflation_factor(datos.values, i) for i in range(datos.shape[1])
]

print(f"VIF nuevo:\n {vif_data}")

# %%
mnumerical = wnumerical.copy()
mnumerical.remove("Followers") # Quitamos follower
mcategorical = categorical.copy()
mcategorical.remove("Verificado") # Quitamos verificado

X = wdf.drop('Followers',axis=1)
y = wdf['Followers']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.70, random_state=42)

# %%
numerical_transformer = StandardScaler()
categorical_transformer = OneHotEncoder(drop='first')

preprocesador = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, mnumerical),
        ('cat', categorical_transformer, mcategorical)
    ]
)

model = Pipeline(
    steps=[
        ('preprocesor',preprocesador),
        ('regresor',LinearRegression())
    ]
)

model.fit(X_train, y_train)

# %%
# 14. Obten las metricas de desempenio del modelo (RMSE, MSE, R2)
# Interpretar tus resultados
#
# Nuestro modelo cobre el ~78% de los datos, es mejor que solamente sacar el promedio.
# Aunque logramos pasar todas las pruebas para verificar que un modelo lineal es suficiente
# puede ser un modelo suficientemente sencillo y medianamente competente.
#
# Tiene un error al predecir de 85 mil seguidores, el cual es un error muy considerable, más
# tomando en cuenta que el promedio en el dataset original de seguidores era ~200 mil.
# Eso no quiere decir que no sea aceptable, aunque no valdrá la pena para creadores
# que estan en el umbral de pequeña base de seguidores
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
# 15. Validaremos el modelo generando una grafica de residuos.
# Interpreta los resultados obtenidos (dejando un comentario de que es lo que crees que implica el ver lo que estas viendo)
#
# Los residuos deberían de seguir un patrón aleatorio sin ninguna tendencia, siguiento el cero.
# En cambio, observamos en la gráfica, en forma de el logo de Nike, que los residuos claramente
# presentan un patrón y tienen una tendencia hacia arriba.

residuals = y_test - model.predict(X_test)

plt.figure(figsize=(10, 6))
plt.scatter(y_test, residuals, color='purple', alpha=0.5)
plt.axhline(y=0, color='red', linestyle='--')
plt.title('Residuals Plot')
plt.xlabel('Predicted Values')
plt.ylabel('Residuals')
plt.show()


# %%
# 16. Genera un histograma de los residuos.
# Interpreta los resultados obtenidos (dejando un comentario de que es lo que crees que implica el ver lo que estas viendo)
#
# Para que esta prueba de validez fuera exitosa la distribución de los residuos debería ser normal.
# Lo que se puede observar es un claro sesgo positivo, a la derecha.
# Esto quiere decir que el modelo no
residuals = (y_test - model.predict(X_test)).values.reshape(1,-1)[0]
res_df = pd.DataFrame({'residuals': residuals})
sns.kdeplot(res_df, x='residuals', fill=True)
plt.show()

# %%
# 17. Genera un Q-Q Plot de los residuos.
# Interpreta los resultados obtenidos (dejando un comentario de que es lo que crees que implica el ver lo que estas viendo)
#
# Los quantiles claramente se abren, para que esta prueba de validez para el modelo fuera exitosa los
# residuos deberían de seguir la línea de los quantiles teóricos. En cambio, es claro que los residuos
# no siguen los quantiles calculados téoricos, y por lo tanto, esta prueba es fallida.
(osm, osr), (slope, intercept, r) = stats.probplot(residuals, dist='norm', plot=plt)
sns.set(style='whitegrid')
plt.title('Q-Q Plot')
plt.xlabel('Theoretical Quantiles')
plt.ylabel('Data Quantiles')
plt.show()


# %%
# 18. Realiiza una prueba de hipotesis Shapiro Wilk sobre la normalidad de los residuos
# Interpreta los resultados obtenidos (dejando un comentario de que es lo que crees que implica el ver lo que estas viendo)
#
# De la prueba de hipótesis de Shapiro Wilk podemos afirmar con total seguridad, con un p-value de
# 0, que los residuos no siguen una distribución normal, y por lo tanto se falló en pasar esta prueba
# de validez para el modelo lineal.
statistic, p_value = stats.shapiro(residuals)
print(f"""
    Estadístico: {statistic:.10f}
        Valor P: {p_value:.10f}
""")

alpha = 0.05 # 95% de confianza

if p_value < alpha:
    print("Rechazamos la hipotesis nula: los datos no siguen una distribución normal")
else:
    print("Fallamos en rechazar la hipótesis nula. Los datos podrían seguir una \
distribución normal")



# %%
# 19. Con base en todo lo desarrollado, explica si tu modelo es valido o no,
# y las razones por la cuales lo es (o no)
#
# El modelo no es válido, los residuos no presentan homoelasticidad, sino que ciertamente son
# heteroelásticos. Para que se pueda usar un modelo lineal se necesita que pase las pruebas de
# verificación que se llevaron a cabo para demostrar que se tratan re residuos homoelásticos.

# %%
# 20. Predice la cantidad de followers para un influencer con los siguientes datos:
    # (IMPORTANTE, solo considera los features que utilizaste para entrenar tu modelo para la nueva prediccion.
    # Es decir, si alguna de las columnas aqui mostrada corresponde a un feature que no consideraste, ignorala)

model.predict(
    pd.DataFrame({
        "Posts_per_week": [15],
        "Avg_watch_time": [4.7],
        # "Avg_likes_per_post": [1423],
        "Avg_comments_per_post": [1819],
        # "Account_age_months": [46],
        "Num_collaborations": [7],
        "Content_type": ['Tech'],
        "Primary_platform": ['TikTok'],
        "Region": ['North America'],
    })
)
