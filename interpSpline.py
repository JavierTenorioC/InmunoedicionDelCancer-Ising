"""
Este script de Python se utiliza para calcular 100 puntos de cada uno de las gráficas presentadas en el artículo a comparar.

Se ejecuta escribiendo `python3 interpolacionSpline.py` 

Autor: Javier Tenorio
Fecha: 01/2024
Versión: 1.0
"""
import numpy as np
from scipy.interpolate import CubicSpline

x = np.array([1, 11, 21, 31, 41, 51, 61, 71, 81, 91,99])

# Fase de eliminación:
    #  pro tumoral Cells 
    # [60.491, 33.91, 22.606, 15.042, 10.675, 6.783, 5.088, 3.685, 1.935, 1.599,3.398]
    # anti tumoral cells
    # [181.845, 152.389, 101.183, 67.512, 45.219, 31.055, 19.891, 12.363, 7.841, 5.483,4.39] 
    # HTME
    # [-1316.7269999999999, -706.317, -308.366, -123.45400000000001, -25.153999999999996, 45.262, 82.06, 89.62, 116.07900000000001, 133.78,109.09] 
    # H Pro Tumoral
    # [1141.634, 52.61, 31.281, 28.084, 41.155, 61.984, 82.06, 94.315, 99.357, 100.335] 
    # H Anti Tumoral
    # [-2458.361, -758.927, -339.647, -151.538, -66.309, -16.722, 0, -4.695, 16.722, 33.445] 
    
# Fase de equilibrio
    # anti tumoral cells
    # [81.879, 56.904, 42.982, 32.966, 27.398, 23.205, 19.483, 16.351, 15.45, 14] 
    # pro tumoral
    # [23.771, 22.981, 15.519, 9.7, 8.633, 9.706, 9.118, 8.759, 10.334, 12.149] 
    # H Pro
    # [143.704, 213.573, 124.946, 74.406, 75.257, 35.236, 108.638, 70.52, 28.571, 91.499] 
    # HTME
    # [-268.439, -77.651, -49.083, -21.618, 45.755, 24.572, 20.137, 57.999, 120.852, 81.179] 
    
# Fase de escape
    # Anti tumoral cells
    # [99.668, 60.577, 44.773, 33.555, 31.222, 28.267, 27.591, 25.599, 25.49, 23.588] 
    # Pro tumoral cells
    # [84.425, 107.932, 97.13, 87.708, 70.01, 58.486, 57.011, 63.13, 68.671, 77.657] 
    # HTME
    # [2832.32, 3484.918, 2368.348, 1621.578, 1108.22, 773.419, 766.394, 822.247, 885.331, 978.671]
    # H anti tumoral
    # [-444.62, -26.732, 8.641, 24.918, 10.242, -6.443, 20.437, -35.435, 17.489, -40.082] 

y = np.array([60.491, 33.91, 22.606, 15.042, 10.675, 6.783, 5.088, 3.685, 1.935, 1.599,3.398])

# Creamos el objeto spline cúbico
spline = CubicSpline(x, y)

# Definimos la cantidad de puntos a extraer
n_puntos = 99

# Generamos los puntos equiespaciados para la interpolación
x_interp = np.linspace(x.min(), x.max(), n_puntos)

# Obtenemos los valores interpolados en esos puntos
y_interp = spline(x_interp)

# Imprimimos los puntos interpolados
for i in range(n_puntos):
    print(f"Punto {i+1}: ({x_interp[i]}, {y_interp[i]})")
