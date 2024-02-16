"""
Este script de Python se utiliza para graficar las figuras del comportamiento del Hamiltoniano para los 3 experimentos.

Se debe de modificar la ruta de cada uno de los archivos a graficar.

Se ejecuta escribiendo `python3 hamiltonianoFiguras.py` 

Autor: Javier Tenorio
Fecha: 01/2024
Versión: 1.0
"""
import pandas
import numpy as np
import matplotlib.pyplot as plt
import colorsys
import matplotlib.colors as mc
import matplotlib as mpl

def plotOverride(df, title):
    plt.figure()
    plt.title(title)
    plt.grid(True)
    plt.plot(df['Step'][:], df['HTME'][:], label="HTME", color="green")
    plt.plot(df['Step'][:], df['HAntiCancer'][:], label="HAntiCancer", color="blue")
    plt.plot(df['Step'][:], df['HProCancer'][:], label="HProCancer", color="red")
    plt.xlabel("Iteración(días)")
    plt.ylabel("Número de células")
    plt.legend()
    plt.savefig(f'H{title}New.pdf', format="pdf", bbox_inches="tight")

#df = pandas.read_csv('/home/jatec/Desktop/InmunoedicionDelCancer-Ising/DatosSimulaciones/Figuras Paper/Escape/model_data[Thu Jun  8 23_54_04 2023].csv')
# df = pandas.read_csv('/home/jatec/Desktop/InmunoedicionDelCancer-Ising/condInitiales118.csv')
df = pandas.read_csv('/home/jatec/Desktop/InmunoedicionDelCancer-Ising/CondicionesIniciales/condInitiales118.csv')
title = "Fase de eliminación"

plt.figure()
plt.title(title)

for i in range(0, len(df) - 101, 101):
    plt.plot(df['Step'][i + 1:i + 101], df['HTME'][i + 1:i + 101], color="green")
    plt.plot(df['Step'][i + 1:i + 101], df['HAntiCancer'][i + 1:i + 101], color="blue")
    plt.plot(df['Step'][i + 1:i + 101], df['HProCancer'][i + 1:i + 101], color="red")

plt.plot(df['Step'][len(df) - 101 + 1:], df['HTME'][len(df) - 101 + 1:], label="HTME", color="green")
plt.plot(df['Step'][len(df) - 101 + 1:], df['HAntiCancer'][len(df) - 101 + 1:], label="HAntiCancer", color="blue")
plt.plot(df['Step'][len(df) - 101 + 1:], df['HProCancer'][len(df) - 101 + 1:], label="HProCancer", color="red")

df_filtered = df[df['Step'] != 0]

promedio_pc = df_filtered.groupby('Step')['HProCancer'].mean()
promedio_ac = df_filtered.groupby('Step')['HAntiCancer'].mean()
promedio_htme = df_filtered.groupby('Step')['HTME'].mean()

maximos = df_filtered.groupby('Step')[['HProCancer', 'HAntiCancer', 'HTME']].max()
minimos = df_filtered.groupby('Step')[['HProCancer', 'HAntiCancer', 'HTME']].min()

print(f"{title}")
print(f"promedio_htme = {promedio_htme.tolist()}")
print(f"promedio_pc = {promedio_pc.tolist()}")
print(f"promedio_ac = {promedio_ac.tolist()}")


plt.grid(True)
plt.xlabel("Iteración(días)")
plt.ylabel("Energía")
plt.legend()
plt.savefig(f'H{title}ElimSim.pdf', format="pdf", bbox_inches="tight")
plt.show()

plt.figure()
plt.plot(promedio_pc.index, promedio_pc, label='Promedio HProCancer', color='red')
plt.plot(promedio_ac.index, promedio_ac, label='Promedio HAntiCancer', color='blue')
plt.plot(promedio_htme.index, promedio_htme, label='Promedio HTME', color='green')
plt.fill_between(maximos.index, maximos['HProCancer'], minimos['HProCancer'], alpha=0.3, color='red')
plt.fill_between(maximos.index, maximos['HAntiCancer'], minimos['HAntiCancer'], alpha=0.3, color='blue')
plt.fill_between(maximos.index, maximos['HTME'], minimos['HTME'], alpha=0.3, color='green')
plt.xlabel('Iteración(días)')
plt.ylabel('Energía')
plt.grid(True)
plt.title('Promedio del Hamiltoniano y su variabilidad en la etapa de eliminación')
plt.legend()
plt.savefig(f'H{title}ElimProm.pdf', format="pdf", bbox_inches="tight")
plt.show()

# --------------------------
# df = pandas.read_csv('/home/jatec/Desktop/InmunoedicionDelCancer-Ising/equil.csv')
df = pandas.read_csv('/home/jatec/Desktop/InmunoedicionDelCancer-Ising/CondicionesIniciales/equilcondInitiales222.csv')
title = "Fase de equilibrio"

plt.figure()
plt.title(title)

for i in range(0, len(df) - 101, 101):
    plt.plot(df['Step'][i + 1:i + 101], df['HTME'][i + 1:i + 101], color="green")
    plt.plot(df['Step'][i + 1:i + 101], df['HAntiCancer'][i + 1:i + 101], color="blue")
    plt.plot(df['Step'][i + 1:i + 101], df['HProCancer'][i + 1:i + 101], color="red")

plt.plot(df['Step'][len(df) - 101 + 1:], df['HTME'][len(df) - 101 + 1:], label="HTME", color="green")
plt.plot(df['Step'][len(df) - 101 + 1:], df['HAntiCancer'][len(df) - 101 + 1:], label="HAntiCancer", color="blue")
plt.plot(df['Step'][len(df) - 101 + 1:], df['HProCancer'][len(df) - 101 + 1:], label="HProCancer", color="red")

df_filtered = df[df['Step'] != 0]

promedio_pc = df_filtered.groupby('Step')['HProCancer'].mean()
promedio_ac = df_filtered.groupby('Step')['HAntiCancer'].mean()
promedio_htme = df_filtered.groupby('Step')['HTME'].mean()

maximos = df_filtered.groupby('Step')[['HProCancer', 'HAntiCancer', 'HTME']].max()
minimos = df_filtered.groupby('Step')[['HProCancer', 'HAntiCancer', 'HTME']].min()

print(f"{title}")
print(f"promedio_htme = {promedio_htme.tolist()}")
print(f"promedio_pc = {promedio_pc.tolist()}")
print(f"promedio_ac = {promedio_ac.tolist()}")

plt.grid(True)
plt.xlabel("Iteración(días)")
plt.ylabel("Energía")
plt.legend()
plt.savefig(f'H{title}EquilSim.pdf', format="pdf", bbox_inches="tight")
plt.show()

plt.figure()
plt.plot(promedio_pc.index, promedio_pc, label='Promedio HProCancer', color='red')
plt.plot(promedio_ac.index, promedio_ac, label='Promedio HAntiCancer', color='blue')
plt.plot(promedio_htme.index, promedio_htme, label='Promedio HTME', color='green')
plt.fill_between(maximos.index, maximos['HProCancer'], minimos['HProCancer'], alpha=0.3, color='red')
plt.fill_between(maximos.index, maximos['HAntiCancer'], minimos['HAntiCancer'], alpha=0.3, color='blue')
plt.fill_between(maximos.index, maximos['HTME'], minimos['HTME'], alpha=0.3, color='green')
plt.xlabel('Iteración(días)')
plt.ylabel('Energía')
plt.grid(True)
plt.title('Promedio del Hamiltoniano y su variabilidad en la etapa de equilibrio')
plt.legend()
plt.savefig(f'H{title}EquilProm.pdf', format="pdf", bbox_inches="tight")
plt.show()

# --------------------------
# df = pandas.read_csv('/home/jatec/Desktop/InmunoedicionDelCancer-Ising/escape.csv')
df = pandas.read_csv('/home/jatec/Desktop/InmunoedicionDelCancer-Ising/escapecondInitiales116.csv')
title = "Fase de escape"

plt.figure()
plt.title(title)

for i in range(0, len(df) - 101, 101):
    plt.plot(df['Step'][i + 1:i + 101], df['HTME'][i + 1:i + 101], color="green")
    plt.plot(df['Step'][i + 1:i + 101], df['HAntiCancer'][i + 1:i + 101], color="blue")
    plt.plot(df['Step'][i + 1:i + 101], df['HProCancer'][i + 1:i + 101], color="red")

plt.plot(df['Step'][len(df) - 101 + 1:], df['HTME'][len(df) - 101 + 1:], label="HTME", color="green")
plt.plot(df['Step'][len(df) - 101 + 1:], df['HAntiCancer'][len(df) - 101 + 1:], label="HAntiCancer", color="blue")
plt.plot(df['Step'][len(df) - 101 + 1:], df['HProCancer'][len(df) - 101 + 1:], label="HProCancer", color="red")

df_filtered = df[df['Step'] != 0]

promedio_pc = df_filtered.groupby('Step')['HProCancer'].mean()
promedio_ac = df_filtered.groupby('Step')['HAntiCancer'].mean()
promedio_htme = df_filtered.groupby('Step')['HTME'].mean()

maximos = df_filtered.groupby('Step')[['HProCancer', 'HAntiCancer', 'HTME']].max()
minimos = df_filtered.groupby('Step')[['HProCancer', 'HAntiCancer', 'HTME']].min()

print(f"{title}")
print(f"promedio_htme = {promedio_htme.tolist()}")
print(f"promedio_pc = {promedio_pc.tolist()}")
print(f"promedio_ac = {promedio_ac.tolist()}")

plt.grid(True)
plt.xlabel("Iteración(días)")
plt.ylabel("Energía")
plt.legend()
plt.savefig(f'H{title}EscaSim.pdf', format="pdf", bbox_inches="tight")
plt.show()

plt.figure()
plt.plot(promedio_pc.index, promedio_pc, label='Promedio HProCancer', color='red')
plt.plot(promedio_ac.index, promedio_ac, label='Promedio HAntiCancer', color='blue')
plt.plot(promedio_htme.index, promedio_htme, label='Promedio HTME', color='green')
plt.fill_between(maximos.index, maximos['HProCancer'], minimos['HProCancer'], alpha=0.3, color='red')
plt.fill_between(maximos.index, maximos['HAntiCancer'], minimos['HAntiCancer'], alpha=0.3, color='blue')
plt.fill_between(maximos.index, maximos['HTME'], minimos['HTME'], alpha=0.3, color='green')
plt.xlabel('Iteración(días)')
plt.ylabel('Energía')
plt.grid(True)
plt.title('Promedio del Hamiltoniano y su variabilidad en la etapa de escape')
plt.legend()
plt.savefig(f'H{title}EscaProm.pdf', format="pdf", bbox_inches="tight")
plt.show()
