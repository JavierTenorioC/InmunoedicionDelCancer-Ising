"""
Este script de Python se utiliza para graficar las figuras correspondientes a:
        el tiempo de ejecución
        rendimiento
        aceleración
    para cada uno de los 3 ambientes: ambiente virtual, máquina virtual y contenedor.
    
    Los datos de cada uno de ellos se debe de ingresarlo de forma manual

Se ejecuta escribiendo `python3 paralelizacionMetricas.py` 

Autor: Javier Tenorio
Fecha: 01/2024
Versión: 1.0
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# Datos
num_procesos = [1,2,3,4,5,6,7,8,9,10]
# computadora
tiempo_computo2 = [653,315,228,183,181,181,179,179,181,180]
# Docker
tiempo_computo1 = [680.7326,376.0856,271.004,220.52,219.60,217.03,215.03,228.55,214.87,216.79]
# VM
tiempo_computo = [1448.57,766.96,525.98,420.69,408.74,419.05,414.46,414.53,419.15,418.48]
title = "VM"
# 0 VM
# 1 Docker
# 2 Ambientes virtuales
# Crear el gráfico con grid
plt.figure()
plt.plot(num_procesos, tiempo_computo, marker='o', label="Máquina virtual")
plt.plot(num_procesos, tiempo_computo1, marker='o', label="Contenedor")
plt.plot(num_procesos, tiempo_computo2, marker='o', label="Ambiente virtual")
plt.title('Rendimiento en función del número de procesos')
plt.xlabel('Número de Procesos')
plt.ylabel('Tiempo de Cómputo (segundos)')
plt.legend()
plt.grid(True)

# Guardar el gráfico en un archivo PDF
with PdfPages(f'grafico_resultante{title}.pdf') as pdf:
    pdf.savefig()
    plt.close()

plt.figure()
plt.plot(num_procesos[1::], np.array(tiempo_computo[0])/np.array(tiempo_computo[1::]), marker='o', \
          label = "Máquina virtual")
plt.plot(num_procesos[1::], np.array(tiempo_computo1[0])/np.array(tiempo_computo1[1::]), marker='o', \
          label = "Contenedor")
plt.plot(num_procesos[1::], np.array(tiempo_computo2[0])/np.array(tiempo_computo2[1::]), marker='o', \
          label = "Ambiente virtual")
plt.title('Aceleración en función del número de procesos')
plt.xlabel('Número de Procesos')
plt.ylabel('Aceleración')
plt.legend()
plt.grid(True)

# Guardar el gráfico en un archivo PDF
with PdfPages(f'Speedup{title}.pdf') as pdf:
    pdf.savefig()
    plt.close()

plt.figure()
plt.plot(num_procesos[1::], np.array(tiempo_computo[0])/(np.array(tiempo_computo[1::]) \
          * np.array(num_procesos[1::])), marker='o', label = "Máquina virtual")
plt.plot(num_procesos[1::], np.array(tiempo_computo1[0])/(np.array(tiempo_computo1[1::]) \
          * np.array(num_procesos[1::])), marker='o', label = "Contenedor")
plt.plot(num_procesos[1::], np.array(tiempo_computo2[0])/(np.array(tiempo_computo2[1::]) \
          * np.array(num_procesos[1::])), marker='o', label = "Ambiente virtual")
plt.title('Eficiencia en función del número de procesos')
plt.xlabel('Número de Procesos')
plt.ylabel('Eficiencia')
plt.legend()
plt.grid(True)

# Guardar el gráfico en un archivo PDF
with PdfPages(f'Eficiency{title}.pdf') as pdf:
    pdf.savefig()
    plt.close()

print("Gráfico guardado en 'grafico_resultante.pdf'")