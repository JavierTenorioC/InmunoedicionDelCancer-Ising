"""
Este script de Python se utiliza para calcular la desviación estándar y el 
promedio de los datos extraídos de CIBERSORT

Cada uno de los datos se ingresa de forma manual.

Se ejecuta escribiendo `python3 extraccionCIBERSORT.py` 

Autor: Javier Tenorio
Fecha: 01/2024
Versión: 1.0
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Datos proporcionados
data = {
    'Mixture': ['W070517001156', 'W070517001157', 'W070517001159', 'W070517001160', 'W070517001161', 'W070517001162',
                'W070517102034', 'W070517102035', 'W070517102036', 'W070517102037', 'W070517102038', 'W070517102051'],
    'T cells CD8': [0.0994052817919677, 0.00527990725367415, 0.0906616043848564, 0.0481457433546999, 0.197760179181833,
                    0.0832578916464174, 0.117127890490844, 0.0527131307059709, 0.147618109789166, 0.123167208776208,
                    0.0907828220942317, 0.0661805515289682],
    'Monocytes': [0.641952285214034, 0.29530318243032, 0.513073440438276, 0.309528871605911, 0.474785892247029,
                  0.264256812229135, 0.240045891304107, 0.386301558177597, 0.435854317019387, 0.244000264754084,
                  0.265328022137937, 0.520168264902333],
    'T cells CD4': [0.190270103683331, 0.516917864163652, 0.137185202533945, 0.496720282704889, 0.135412692184424,
                    0.481552383564454, 0.492179710276872, 0.438062813223831, 0.315415406237907, 0.440929294652063,
                    0.412169896337822, 0.240289141948816],
    'NKT cells': [0, 0, 0, 0, 0.0354547151642914, 0, 0, 0, 0, 0, 0, 0],
    'B cells': [0.0232374457588736, 0.06128643404871, 0.0969411148726901, 0.0459285140796416, 0.0541958012459137,
                0.0661237758395307, 0.0621149508661442, 0.0347866378905779, 0.0435802900721626, 0.102823995813914,
                0.122589120848331, 0.035927073724623],
    'NK cells': [0.0451348835517936, 0.121212612103643, 0.162138637770233, 0.099676588254859, 0.102390719976509,
                  0.104809136720463, 0.0885315570620324, 0.0881358600020228, 0.0575318768813777, 0.0890792360037315,
                  0.109130138581678, 0.13743496789526],
    'P-value': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'Correlation': [0.846144443249005, 0.803825777612462, 0.776564365802116, 0.758696480828868, 0.874361348386671,
                    0.852018931728027, 0.836936396351752, 0.766467071072648, 0.872549504081871, 0.883169843166235,
                    0.798684977712978, 0.838509109237548],
    'RMSE': [0.802253589496056, 0.595358728893485, 0.767325399710124, 0.653164973133189, 0.5614199997749,
              0.537110275240318, 0.566414024852072, 0.668296614688979, 0.523580388039575, 0.502880703044595,
              0.604570900927732, 0.663599819361284]
}

# Crea un DataFrame
df = pd.DataFrame(data)

# Calcula el promedio y la desviación estándar de cada columna numérica
promedio = df.mean()
desviacion_estandar = df.std()

# Imprime los resultados
print("Promedio:")
print(promedio)
print("\nDesviación Estándar:")
print(desviacion_estandar)

# Gráfica de barras con barras de error (desviación estándar)
fig, ax = plt.subplots(figsize=(10, 6))

promedio.plot(kind='bar', yerr=desviacion_estandar, capsize=5, color='skyblue', edgecolor='black', ax=ax)

ax.set_ylabel('Valor')
ax.set_title('Promedio y Desviación Estándar de cada población celular')
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')

plt.tight_layout()
# plt.savefig('boxPlot.pdf', format='pdf')
plt.show()
