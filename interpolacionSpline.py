"""
Este script de Python se utiliza para calcular 100 puntos de cada uno de las gráficas presentadas en el artículo a comparar.

Se ejecuta escribiendo `python3 interpolacionSpline.py` 

Autor: Javier Tenorio
Fecha: 01/2024
Versión: 1.0
"""
import numpy as np
from scipy.interpolate import CubicSpline

# Supongamos que tienes una lista de puntos en x e y
# Puedes cambiar esto con tus propios puntos
x = np.array([0, 1, 2, 3, 4])
y = np.array([0, 1, 4, 9, 16])

# Creamos el objeto spline cúbico
spline = CubicSpline(x, y)

# Definimos la cantidad de puntos a extraer
n_puntos = 10

# Generamos los puntos equiespaciados para la interpolación
x_interp = np.linspace(x.min(), x.max(), n_puntos)

# Obtenemos los valores interpolados en esos puntos
y_interp = spline(x_interp)

# Imprimimos los puntos interpolados
for i in range(n_puntos):
    print(f"Punto {i+1}: ({x_interp[i]}, {y_interp[i]})")

