"""
Este script de Python se utiliza para graficar las figuras de la dinámica 
poblacional para los 3 experimentos.

Se debe de modificar la ruta de cada uno de los archivos a graficar.

Se ejecuta escribiendo `python3 poblacionFiguras.py` 

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

def plotOverride(df,title):
    plt.figure()
    plt.title(title)
    plt.grid(True)
    plt.plot(df['Step'][:],df['AntiCancer'][:],label="Sistema Inmune",color = "blue" )
    plt.xlabel("Iteración(días)")
    plt.ylabel("Número de células")
    plt.plot(df['Step'][:],df['ProCancer'][:],label="Cancer", color = "red")
    plt.legend()
    plt.savefig(f'{title}New.pdf', format="pdf", bbox_inches="tight")

### Codigo que empieza inicializando todo a 0
#df = pandas.read_csv('/home/jatec/Desktop/InmunoedicionDelCancer-Ising/DatosSimulaciones/Figuras Paper/Eliminación/model_data[Thu Jun  8 21_19_21 2023].csv')
#df = pandas.read_csv('/home/jatec/Desktop/InmunoedicionDelCancer-Ising/elim.csv')
#df = pandas.read_csv('/home/jatec/Desktop/InmunoedicionDelCancer-Ising/equil.csv')
# df = pandas.read_csv('/home/jatec/Desktop/InmunoedicionDelCancer-Ising/escape.csv')
# df = pandas.read_csv('/home/jatec/Desktop/InmunoedicionDelCancer-Ising/escapecondInitiales116.csv')

df = pandas.read_csv('/home/jatec/Desktop/InmunoedicionDelCancer-Ising/escapecondInitiales116.csv')
plt.figure()
title = "Fase de escape"
plt.title(title)
# dataM = np.matrix(df)
# promedioCC = np.zeros([100,df.shape[0]])
# promedioCC = np.array(df['AntiCancer'][len(df)-101+1:])
# promedioIS = np.array(df['ProCancer'][len(df)-101+1:])
for i in range(0,len(df)-101,101):
    # promedioCC = np.insert(promedioCC,0,np.array(df['AntiCancer'][i+1:i+101]),axis=1)
    # promedioIS = np.append(promedioIS,np.array(df['ProCancer'][i+1:i+101]),axis=1)
    plt.plot(df['Step'][i+1:i+101],df['AntiCancer'][i+1:i+101],color = "blue" )
    plt.plot(df['Step'][i+1:i+101],df['ProCancer'][i+1:i+101], color = "red")
plt.plot(df['Step'][len(df)-101 + 1:],df['AntiCancer'][len(df)-101+1:],label="Sistema Inmune",color = "blue" )
plt.plot(df['Step'][len(df)-101 + 1:],df['ProCancer'][len(df)-101+1:],label="Cancer", color = "red")
# promedioCC.append(df['AntiCancer'][len(df)-101 + 1:])
# promedioIS.append(df['ProCancer'][len(df)-101 + 1:])
df_filtered = df[df['Step'] != 0]

promedio_pc = df_filtered.groupby('Step')['ProCancer'].mean()
promedio_ac = df_filtered.groupby('Step')['AntiCancer'].mean()

print(f"{title}")
print(f"promedio_pc = {promedio_pc.tolist()}")
print(f"promedio_ac = {promedio_ac.tolist()}")

maximos = df_filtered.groupby('Step')[['ProCancer', 'AntiCancer']].max()
minimos = df_filtered.groupby('Step')[['ProCancer', 'AntiCancer']].min()

plt.grid(True)
plt.xlabel("Iteración(días)")
plt.ylabel("Números de células")
plt.legend()
plt.savefig(f'{title}SimEsc.pdf', format="pdf", bbox_inches="tight")
plt.show


plt.figure()
plt.title(title)
plt.plot(promedio_pc.index, promedio_pc, label='Promedio ProCancer', color='red')
plt.plot(promedio_ac.index, promedio_ac, label='Promedio Sistema Inmune', color='blue')
plt.fill_between(maximos.index, maximos['ProCancer'], minimos['ProCancer'], alpha=0.3, color='red')
plt.fill_between(maximos.index, maximos['AntiCancer'], minimos['AntiCancer'], alpha=0.3, color='blue')
plt.xlabel('Iteración(días)')
plt.ylabel('Números de células')
plt.grid(True)
#plt.title('Promedio de las poblaciones y su variabilidad')
plt.legend()
plt.savefig(f'{title}PromEsc.pdf', format="pdf", bbox_inches="tight")
plt.show()


# -------------------------------------------

# df = pandas.read_csv('/home/jatec/Desktop/InmunoedicionDelCancer-Ising/elim.csv')
df = pandas.read_csv('/home/jatec/Desktop/InmunoedicionDelCancer-Ising/CondicionesIniciales/equilcondInitiales222.csv')
#df = pandas.read_csv('/home/jatec/Desktop/InmunoedicionDelCancer-Ising/equil.csv')
plt.figure()
title = "Fase de eliminación"
plt.title(title)
# dataM = np.matrix(df)
# promedioCC = np.zeros([100,df.shape[0]])
# promedioCC = np.array(df['AntiCancer'][len(df)-101+1:])
# promedioIS = np.array(df['ProCancer'][len(df)-101+1:])
for i in range(0,len(df)-101,101):
    # promedioCC = np.insert(promedioCC,0,np.array(df['AntiCancer'][i+1:i+101]),axis=1)
    # promedioIS = np.append(promedioIS,np.array(df['ProCancer'][i+1:i+101]),axis=1)
    plt.plot(df['Step'][i+1:i+101],df['AntiCancer'][i+1:i+101],color = "blue" )
    plt.plot(df['Step'][i+1:i+101],df['ProCancer'][i+1:i+101], color = "red")
plt.plot(df['Step'][len(df)-101 + 1:],df['AntiCancer'][len(df)-101+1:],label="Sistema Inmune",color = "blue" )
plt.plot(df['Step'][len(df)-101 + 1:],df['ProCancer'][len(df)-101+1:],label="Cancer", color = "red")
# promedioCC.append(df['AntiCancer'][len(df)-101 + 1:])
# promedioIS.append(df['ProCancer'][len(df)-101 + 1:])
df_filtered = df[df['Step'] != 0]

promedio_pc = df_filtered.groupby('Step')['ProCancer'].mean()
promedio_ac = df_filtered.groupby('Step')['AntiCancer'].mean()

maximos = df_filtered.groupby('Step')[['ProCancer', 'AntiCancer']].max()
minimos = df_filtered.groupby('Step')[['ProCancer', 'AntiCancer']].min()

print(f"{title}")
print(f"promedio_pc = {promedio_pc.tolist()}")
print(f"promedio_ac = {promedio_ac.tolist()}")

plt.grid(True)
plt.xlabel("Iteración(días)")
plt.ylabel("Números de células")
plt.legend()
plt.savefig(f'{title}SimElim.pdf', format="pdf", bbox_inches="tight")
plt.show


plt.figure()
plt.title(title)
plt.plot(promedio_pc.index, promedio_pc, label='Promedio ProCancer', color='red')
plt.plot(promedio_ac.index, promedio_ac, label='Promedio Sistema Inmune', color='blue')
plt.fill_between(maximos.index, maximos['ProCancer'], minimos['ProCancer'], alpha=0.3, color='red')
plt.fill_between(maximos.index, maximos['AntiCancer'], minimos['AntiCancer'], alpha=0.3, color='blue')
plt.xlabel('Iteración(días)')
plt.ylabel('Números de células')
plt.grid(True)
#plt.title('Promedio de las poblaciones y su variabilidad')
plt.legend()
plt.savefig(f'{title}PromElim.pdf', format="pdf", bbox_inches="tight")
plt.show()

# -------------------------------------------

# df = pandas.read_csv('/home/jatec/Desktop/InmunoedicionDelCancer-Ising/equil.csv')
df = pandas.read_csv('/home/jatec/Desktop/InmunoedicionDelCancer-Ising/CondicionesIniciales/condInitiales118.csv')
plt.figure()
title = "Fase de equilibrio"
plt.title(title)
# dataM = np.matrix(df)
# promedioCC = np.zeros([100,df.shape[0]])
# promedioCC = np.array(df['AntiCancer'][len(df)-101+1:])
# promedioIS = np.array(df['ProCancer'][len(df)-101+1:])
for i in range(0,len(df)-101,101):
    # promedioCC = np.insert(promedioCC,0,np.array(df['AntiCancer'][i+1:i+101]),axis=1)
    # promedioIS = np.append(promedioIS,np.array(df['ProCancer'][i+1:i+101]),axis=1)
    plt.plot(df['Step'][i+1:i+101],df['AntiCancer'][i+1:i+101],color = "blue" )
    plt.plot(df['Step'][i+1:i+101],df['ProCancer'][i+1:i+101], color = "red")
plt.plot(df['Step'][len(df)-101 + 1:],df['AntiCancer'][len(df)-101+1:],label="Sistema Inmune",color = "blue" )
plt.plot(df['Step'][len(df)-101 + 1:],df['ProCancer'][len(df)-101+1:],label="Cancer", color = "red")
# promedioCC.append(df['AntiCancer'][len(df)-101 + 1:])
# promedioIS.append(df['ProCancer'][len(df)-101 + 1:])
df_filtered = df[df['Step'] != 0]

promedio_pc = df_filtered.groupby('Step')['ProCancer'].mean()
promedio_ac = df_filtered.groupby('Step')['AntiCancer'].mean()

maximos = df_filtered.groupby('Step')[['ProCancer', 'AntiCancer']].max()
minimos = df_filtered.groupby('Step')[['ProCancer', 'AntiCancer']].min()

print(f"{title}")
print(f"promedio_pc = {promedio_pc.tolist()}")
print(f"promedio_ac = {promedio_ac.tolist()}")

plt.grid(True)
plt.xlabel("Iteración(días)")
plt.ylabel("Números de células")
plt.legend()
plt.savefig(f'{title}SimEquil.pdf', format="pdf", bbox_inches="tight")
plt.show


plt.figure()
plt.title(title)
plt.plot(promedio_pc.index, promedio_pc, label='Promedio ProCancer', color='red')
plt.plot(promedio_ac.index, promedio_ac, label='Promedio Sistema Inmune', color='blue')
plt.fill_between(maximos.index, maximos['ProCancer'], minimos['ProCancer'], alpha=0.3, color='red')
plt.fill_between(maximos.index, maximos['AntiCancer'], minimos['AntiCancer'], alpha=0.3, color='blue')
plt.xlabel('Iteración(días)')
plt.ylabel('Números de células')
plt.grid(True)
#plt.title('Promedio de las poblaciones y su variabilidad')
plt.legend()
plt.savefig(f'{title}PromEquil.pdf', format="pdf", bbox_inches="tight")
plt.show()
