"""
Este script de Python se utiliza para calcular 100 puntos de cada uno de las gráficas presentadas en el artículo a comparar.

Se ejecuta escribiendo `python3 caracterizar.py` 

Autor: Javier Tenorio
Fecha: 01/2024
Versión: 1.0
"""
# Extracción de características
import pandas as pd

# Lee el archivo CSV
# archivo_csv = "1703199259.2367747-10-Barrido.csv"  # Reemplaza con el nombre de tu archivo
archivo_csv = "1708076028.5353734-1-Barrido.csv"  # Reemplaza con el nombre de tu archivo
df = pd.read_csv(archivo_csv)

# Filtra las filas donde el valor en la columna "Step" es igual a 100
filas_step_100 = df[df['Step'] == 100]

# Imprime las filas resultantes
print(filas_step_100)

# Visualización de datos
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

x_values = np.linspace(0.01,1,10)
y_values = np.linspace(0.01,1,10)

# Crea una malla 2D para los valores de x e y
x, y = np.meshgrid(x_values, y_values)

# Obtiene los valores de las otras columnas que deseas graficar en el eje z
z_values = np.zeros([10,10])
z_valuesSin = []


for fil in filas_step_100.itertuples():
    x_temp = fil.meanIS 
    y_temp = fil.meanCancer
    z_values[np.where( x_temp == x_values)[0][0]][np.where( y_temp == y_values)[0][0]] += fil.HTME
    z_valuesSin.append(fil.HTME)

z_values /= 25
    

# Crea la figura y los ejes 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Grafica la superficie 3D
surf = ax.plot_surface(x, y, z_values, cmap='plasma',
                       rstride=1, cstride=1, alpha=0.7, linewidth=0.5)

# Añade una barra de color
fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10, location= 'right', pad=0.2)

# Ajusta la vista
# ax.view_init(elev=45, azim=45)

# Etiqueta los ejes

ax.set_xlabel(r'$\sigma_1$', fontsize=10)
ax.set_ylabel(r'$\sigma_2$', fontsize=10)
ax.set_zlabel('HTME', fontsize=10)
plt.show()
plt.figure()
# Crea el gráfico de contornos
# fig, ax = plt.subplots()
# contour = plt.contour(x, y, z_values, cmap='plasma')
# ax.set_xlabel(r'$\sigma_1$', fontsize=10)
# ax.set_ylabel(r'$\sigma_2$', fontsize=10)
# ax.clabel(contour, inline=True, fontsize=10)
# ax.grid('on')

# plt.savefig('3dPlot.pdf', format='pdf')
# Muestra la gráfica




import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
from sklearn.metrics import silhouette_score

# Genera datos de ejemplo
X, _ = make_blobs(n_samples=300, centers=3, random_state=42)

# Calcula la inercia para diferentes valores de k
inertia = []
silhouette_scores = []
max_clusters = 10
X_unidimensional = filas_step_100['HTME'].to_numpy().reshape(-1, 1)

for k in range(2, max_clusters + 1):
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=20)
    kmeans.fit(X_unidimensional)
    inertia.append(kmeans.inertia_)

    if k > 1:
        silhouette_scores.append(silhouette_score(X_unidimensional, kmeans.labels_))

# Método del codo: grafica la inercia en función del número de clusters
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.plot(range(2, max_clusters + 1), inertia, marker='o')
plt.title('Método del Codo')
plt.xlabel('Número de clusters')
plt.ylabel('Inercia')

# Coeficiente de silueta: grafica el coeficiente de silueta en función del número de clusters
plt.subplot(1, 2, 2)
plt.plot(range(2, max_clusters + 1), silhouette_scores, marker='o')
plt.title('Coeficiente de Silueta')
plt.xlabel('Número de clusters')
plt.ylabel('Silueta Score')

plt.tight_layout()
# plt.savefig('silhouette.pdf', format='pdf')
plt.show()


# Realiza el clustering con el número óptimo de clusters
optimal_k = 3
kmeans_optimal = KMeans(n_clusters=optimal_k, random_state=42)
labels = kmeans_optimal.fit_predict(X_unidimensional)

# Visualiza los resultados
plt.scatter(X_unidimensional, np.zeros_like(X_unidimensional), c=labels, cmap='viridis', edgecolors='k', s=50)
plt.scatter(kmeans_optimal.cluster_centers_, np.zeros_like(kmeans_optimal.cluster_centers_), c='red', marker='X', s=200, label='Centroides')
plt.title(f'Clustering con {optimal_k} clusters')
plt.xlabel('Característica 1')
plt.legend()

plt.savefig('centroides2.pdf', format='pdf')
plt.show()




