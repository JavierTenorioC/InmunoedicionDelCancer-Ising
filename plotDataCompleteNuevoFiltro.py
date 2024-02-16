#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 11:36:30 2023

@author: javiert
"""

# # El [3] es el número de días
# # Protumoral

# import pandas
# import numpy as np
# import matplotlib.pyplot as plt
# import colorsys
# import matplotlib.colors as mc
# import matplotlib as mpl

# # mpl.style.use(sty)

# df = pandas.read_csv('/home/jatec/Desktop/InmunoedicionDelCancer-Ising/DatosSimulaciones/model_data.csv')


# # ax.set_title('style: {!r}'.format(sty), color='C0')
# plt.figure()
# # plt.xlabel("Iteration(days)")
# # plt.ylabel("Number of cells")
# plt.plot(df['Step'][:],df['AntiCancer'][:],label="Anticancer",color = "#eab676" )
# # plt.legend()

# # plt.figure()
# plt.xlabel("Iteration(days)")
# plt.ylabel("Number of cells")
# plt.plot(df['Step'][:],df['ProCancer'][:],label="ProCancer", color = "#76b5c5")
# plt.legend()

# # Step100 = df[df['Step' > 0]]

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 11:36:30 2023

@author: javiert
"""

# El [3] es el número de días
# Protumoral
# 13579

import pandas
import numpy as np
import matplotlib.pyplot as plt
import colorsys
import matplotlib.colors as mc
import matplotlib as mpl
import os

# mpl.style.use(sty)
# from cancerInmunoediting.agents import CancerCell, CellNK, CellM, CellN,\
    # TCell, ThCell, TregCell, dendriticCells, CellGammaDeltaT

def plotOverride(df,title):
    plt.figure()
    plt.figure()
    plt.title(title)
    step = 100
    for i in range(0,len(df)-step-1,step+1):
        # ISpoblaciones = df['NK'][i+1:i+step] + df['M1'][i+1:i+step] +df['CellsN1'][i+1:i+step] + df['T'][i+1:i+step] \
        #     + df['GDT'][i+1:i+step]
        ISpoblaciones = df['AntiCancer'][i+1:i+step]
        plt.plot(df['Step'][i+1:i+step],ISpoblaciones,color = "blue" )
        # plt.plot(df['Step'][i+1:i+step],df['ProCancer'][i+1:i+step], color = "red")
    # ISpoblaciones = df['NK'][len(df)-step -1 + 1:] + df['M1'][len(df)-step -1 + 1:] +df['CellsN1'][len(df)-step -1 + 1:] + df['T'][len(df)-step -1 + 1:] \
    #     + df['GDT'][len(df)-step -1 + 1:]
    ISpoblaciones = df['AntiCancer'][len(df)-step -1 + 1:]
    plt.plot(df['Step'][len(df)-step -1 + 1:],ISpoblaciones,label="Sistema Inmune",color = "blue" )
    # plt.plot(df['Step'][len(df)-step -1 + 1:],df['ProCancer'][len(df)-step-1+1:],label="Cancer", color = "red")
    plt.grid(True)
    plt.xlabel("Iteration(days)")
    plt.ylabel("Number of cells")
    plt.legend()
    # plt.savefig(f'{title}-IS.pdf', format="pdf", bbox_inches="tight")
    
    
    plt.figure()
    plt.title(title)
    step = 100
    for i in range(0,len(df)-step-1,step+1):
        # CancerPoblaciones = df['M2'][i+1:i+step] + df['M1'][i+1:i+step] +df['CellsN2'][i+1:i+step]+ \
        #     + df['Treg'][i+1:i+step] + df['Th2'][i+1:i+step] + df['Th17'][i+1:i+step]
        CancerPoblaciones = df['ProCancer'][i+1:i+step] 
        # plt.plot(df['Step'][i+1:i+step],df['SI'][i+1:i+step],color = "blue" )
        plt.plot(df['Step'][i+1:i+step],CancerPoblaciones, color = "red")
    # plt.plot(df['Step'][len(df)-step -1 + 1:],df['SI'][len(df)-step-1+1:],label="Sistema Inmune",color = "blue" )
    # CancerPoblaciones = df['M2'][len(df)-step -1 + 1:] + df['M1'][len(df)-step -1 + 1:] +df['CellsN2'][len(df)-step -1 + 1:]+ \
    #     + df['Treg'][len(df)-step -1 + 1:] + df['Th2'][len(df)-step -1 + 1:] + df['Th17'][len(df)-step -1 + 1:]
    CancerPoblaciones = df['ProCancer'][len(df)-step -1 + 1:]
    plt.plot(df['Step'][len(df)-step -1 + 1:],df['ProCancer'][len(df)-step-1+1:],label="Cancer", color = "red")
    plt.grid(True)
    plt.xlabel("Iteration(days)")
    plt.ylabel("Number of cells")
    plt.legend()
    # plt.savefig(f'{title}-Cancer.pdf', format="pdf", bbox_inches="tight")
    
    
    plt.figure()
    plt.title(title)
    step = 100
    for i in range(0,len(df)-step-1,step+1):
        # ISpoblaciones = df['NK'][i+1:i+step] + df['M1'][i+1:i+step] +df['CellsN1'][i+1:i+step] + df['T'][i+1:i+step] \
        #     + df['GDT'][i+1:i+step]
        ISpoblaciones = df['AntiCancer'][i+1:i+step]
        plt.plot(df['Step'][i+1:i+step],ISpoblaciones,color = "blue" )
        # CancerPoblaciones = df['M2'][i+1:i+step] + df['M1'][i+1:i+step] +df['CellsN2'][i+1:i+step]+ \
        #     + df['Treg'][i+1:i+step] + df['Th2'][i+1:i+step] + df['Th17'][i+1:i+step]
        CancerPoblaciones = df['ProCancer'][i+1:i+step] 
        # plt.plot(df['Step'][i+1:i+step],df['SI'][i+1:i+step],color = "blue" )
        plt.plot(df['Step'][i+1:i+step],CancerPoblaciones, color = "red")
        # plt.plot(df['Step'][i+1:i+step],df['SI'][i+1:i+step],color = "blue" )
        # plt.plot(df['Step'][i+1:i+step],df['ProCancer'][i+1:i+step], color = "red")
    CancerPoblaciones = df['ProCancer'][len(df)-step -1 + 1:]
    # CancerPoblaciones = df['M2'][len(df)-step -1 + 1:] + df['M1'][len(df)-step -1 + 1:] +df['CellsN2'][len(df)-step -1 + 1:]+ \
    #     + df['Treg'][len(df)-step -1 + 1:] + df['Th2'][len(df)-step -1 + 1:] + df['Th17'][len(df)-step -1 + 1:]
    plt.plot(df['Step'][len(df)-step -1 + 1:],df['ProCancer'][len(df)-step-1+1:],label="Cancer", color = "red")
    # ISpoblaciones = df['NK'][len(df)-step -1 + 1:] + df['M1'][len(df)-step -1 + 1:] +df['CellsN1'][len(df)-step -1 + 1:] + df['T'][len(df)-step -1 + 1:] \
    #     + df['GDT'][len(df)-step -1 + 1:]
    ISpoblaciones = df['AntiCancer'][len(df)-step -1 + 1:]
    plt.plot(df['Step'][len(df)-step -1 + 1:],ISpoblaciones,label="Sistema Inmune",color = "blue" )
    
    # plt.plot(df['Step'][len(df)-step -1 + 1:],df['SI'][len(df)-step-1+1:],label="Sistema Inmune",color = "blue" )
    # plt.plot(df['Step'][len(df)-step -1 + 1:],df['ProCancer'][len(df)-step-1+1:],label="Cancer", color = "red")
    plt.grid(True)
    plt.xlabel("Iteration(days)")
    plt.ylabel("Number of cells")
    plt.legend()
    
    promedio_pc = df.groupby('Step')['ProCancer'].mean()
    promedio_ac = df.groupby('Step')['AntiCancer'].mean()
    
    maximos = df.groupby('Step')[['ProCancer', 'AntiCancer']].max()
    minimos = df.groupby('Step')[['ProCancer', 'AntiCancer']].min()
    
    
    plt.figure()
    plt.plot(promedio_pc.index, promedio_pc, label='Promedio ProCancer', color='red')
    plt.plot(promedio_ac.index, promedio_ac, label='Promedio Sistema Inmune', color='blue')
    plt.fill_between(maximos.index, maximos['ProCancer'], minimos['ProCancer'], alpha=0.3, color='red')
    plt.fill_between(maximos.index, maximos['AntiCancer'], minimos['AntiCancer'], alpha=0.3, color='blue')
    plt.xlabel('Iteración(días)')
    plt.ylabel('Números de células')
    plt.grid(True)
    plt.title('Promedio de las poblaciones y su variabilidad')
    plt.legend()
    plt.savefig(f'{title}Prom.pdf', format="pdf", bbox_inches="tight")
    plt.show()
    
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
    
    plt.grid(True)
    plt.xlabel("Iteración(días)")
    plt.ylabel("Energía")
    plt.legend()
    plt.savefig(f'H{title}Sim.pdf', format="pdf", bbox_inches="tight")
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
    plt.title('Promedio del Hamiltoniano y su variabilidad')
    plt.legend()
    plt.savefig(f'H{title}Prom.pdf', format="pdf", bbox_inches="tight")
    plt.show()
    
    # plt.grid(True)
    # plt.plot(df['Step'][:-1],df['SI'][:-1],label="Sistema Inmune",color = "blue" )
    # plt.xlabel("Iteration(days)")
    # plt.ylabel("Number of cells")
    # plt.plot(df['Step'][:-1],df['ProCancer'][:-1],label="Cancer", color = "red")
    # plt.legend()
    # plt.savefig(f'{title}-IS-Cancer.pdf', format="pdf", bbox_inches="tight")

### Código para código que empieza inicializando todo a 
# file = "model_data[Wed Jul 12 00_38_59 2023].csv"
# df = pandas.read_csv(f'/home/jatec/Desktop/ModeloCargaMutacional-main/')
# plt.figure()
# title = "Cancer: Medio, IS: Medio"
# plt.title(title)
# for i in range(0,len(df)-101,101):
#     plt.plot(df['Step'][i+1:i+100],df['SI'][i+1:i+100],color = "blue" )
#     plt.plot(df['Step'][i+1:i+100],df['ProCancer'][i+1:i+100], color = "red")
# plt.plot(df['Step'][len(df)-101 + 1:],df['SI'][len(df)-101+1:],label="Sistema Inmune",color = "blue" )
# plt.plot(df['Step'][len(df)-101 + 1:],df['ProCancer'][len(df)-101+1:],label="Cancer", color = "red")
# plt.grid(True)
# plt.xlabel("Iteration(days)")
# plt.ylabel("Number of cells")
# plt.legend()
# plt.savefig(f'{title}.pdf', format="pdf", bbox_inches="tight")

# # for i in range(0,len(df)-101,101):
# #     print(i)

# ### Código para cuando empieza en poblaciones diferentes a 0
# df = pandas.read_csv('/home/jatec/Desktop/ModeloCargaMutacional-main/model_data[Wed Jul 12 00_38_59 2023].csv')
# plt.figure()
# title = "Cancer: Debil, IS: Debil"
# plt.title(title)
# for i in range(0,len(df)-101,101):
#     plt.plot(df['Step'][i+1:i+101],df['AntiCancer'][i+1:i+100],color = "blue" )
#     plt.plot(df['Step'][i+1:i+101],df['ProCancer'][i+1:i+100], color = "red")
# plt.plot(df['Step'][len(df)-100 + 1:],df['AntiCancer'][len(df)-100+1:],label="Sistema Inmune",color = "blue" )
# plt.plot(df['Step'][len(df)-100 + 1:],df['ProCancer'][len(df)-100+1:],label="Cancer", color = "red")
# plt.grid(True)
# plt.xlabel("Iteration(days)")
# plt.ylabel("Number of cells")
# plt.legend()
# plt.savefig(f'{title}.pdf', format="pdf", bbox_inches="tight")

file = "model_data[Tue Jul 25 04:32:22 2023]"
path = "/home/jatec/Desktop/InmunoedicionDelCancer-Ising/"
df = pandas.read_csv(f'{path}{file}.csv')
try:
    os.mkdir(f"./{file}")
except:
    print("Ya existe el directorio!")
os.chdir(f"{path}{file}")
# # cancer IS
# debilDebil = df.query("`stdIS` <= 0.2 and `stdCancer` <= 0.2 and  `meanIS`  <= 0.35 and `meanCancer` <= 0.35 ")
# debilMedio = df.query("`stdIS` <= 0.2 and `stdCancer` <= 0.2 and  `meanIS`  >= 0.35 and `meanIS`  <= 0.75 and `meanCancer` <= 0.35 ")
# debilFuerte = df.query("`stdIS` <= 0.2 and `stdCancer` <= 0.2 and  `meanIS`  >= 0.75 and `meanCancer` <= 0.35 ")

# # cancer IS
# medioDebil = df.query("`stdIS` <= 0.2 and `stdCancer` <= 0.2 and  `meanIS`  <= 0.35 and `meanCancer` >= 0.35 and `meanCancer` <= 0.75 ")
# medioMedio = df.query("`stdIS` <= 0.2 and `stdCancer` <= 0.2 and  `meanIS`  >= 0.35 and `meanIS`  <= 0.75 and `meanCancer` >= 0.35 and `meanCancer` <= 0.75 ")
# medioFuerte = df.query("`stdIS` <= 0.2 and `stdCancer` <= 0.2 and `meanIS`  <= 0.75 and `meanCancer` >= 0.35 and `meanCancer` <= 0.75  ")

# # cancer IS
# fuerteDebil = df.query("`stdIS` <= 0.2 and `stdCancer` <= 0.2 and  `meanIS`  >= 0.75 and `meanCancer` <= 0.35")
# fuerteMedio = df.query("`stdIS` <= 0.2 and `stdCancer` <= 0.2 and  `meanIS`  >= 0.75 and `meanCancer` >= 0.35 and `meanCancer` <= 0.75 ")
# fuerteFuerte = df.query("`stdIS` <= 0.2 and `stdCancer` <= 0.2 and  `meanIS`  >= 0.75 and `meanCancer` >= 0.75 ")

# plotOverride(debilDebil,"Cancer: Débil, IS: Débil")
# plotOverride(debilMedio,"Cancer: Débil, IS: Medio")
# plotOverride(debilFuerte,"Cancer: Débil, IS: Fuerte")

# plotOverride(medioDebil,"Cancer: Medio, IS: Débil")
# plotOverride(medioMedio,"Cancer: Medio, IS: Medio")
# plotOverride(medioFuerte,"Cancer: Medio, IS: Fuerte")

# plotOverride(fuerteDebil,"Cancer: Fuerte, IS: Débil")
# plotOverride(fuerteMedio,"Cancer: Fuerte, IS: Medio")
# plotOverride(fuerteFuerte,"Cancer: Fuerte, IS: Fuerte")

# cancer IS
# debilDebil = df.query("`stdIS` <= 0.2 and `stdCancer` <= 0.2 and  `meanIS`  <= 0.35 and `meanCancer` <= 0.35 ")
debilMedio = df.query("`stdIS` <= 0.2 and `stdCancer` <= 0.2 and  `meanIS`  >= 0.29 and `meanIS`  <= 0.31 and `meanCancer` <= 0.16 ")
# debilFuerte = df.query("`stdIS` <= 0.2 and `stdCancer` <= 0.2 and  `meanIS`  >= 0.75 and `meanCancer` <= 0.35 ")

# cancer IS
# medioDebil = df.query("`stdIS` <= 0.2 and `stdCancer` <= 0.2 and  `meanIS`  <= 0.35 and `meanCancer` >= 0.35 and `meanCancer` <= 0.75 ")
medioMedio = df.query("`stdIS` <= 0.2 and `stdCancer` <= 0.2 and  `meanIS`  >= 0.39 and `meanIS`  <= 0.41 and `meanCancer` >= 0.59 and `meanCancer` <= 0.61 ")
medioFuerte = df.query("`stdIS` <= 0.2 and `stdCancer` <= 0.2 and `meanIS`  >= 0.69 and `meanCancer` >= 0.59 and `meanCancer` <= 0.61  ")

# cancer IS
# fuerteDebil = df.query("`stdIS` <= 0.2 and `stdCancer` <= 0.2 and  `meanIS`  >= 0.75 and `meanCancer` <= 0.35")
# fuerteMedio = df.query("`stdIS` <= 0.2 and `stdCancer` <= 0.2 and  `meanIS`  >= 0.75 and `meanCancer` >= 0.35 and `meanCancer` <= 0.75 ")
# fuerteFuerte = df.query("`stdIS` <= 0.2 and `stdCancer` <= 0.2 and  `meanIS`  >= 0.75 and `meanCancer` >= 0.75 ")

# plotOverride(debilDebil,"Cancer: Débil, IS: Débil")
plotOverride(debilMedio,"Cancer: Débil, IS: Medio")
# plotOverride(debilFuerte,"Cancer: Débil, IS: Fuerte")

# plotOverride(medioDebil,"Cancer: Medio, IS: Débil")
plotOverride(medioMedio,"Cancer: Medio, IS: Medio")
plotOverride(medioFuerte,"Cancer: Medio, IS: Fuerte")

# plotOverride(fuerteDebil,"Cancer: Fuerte, IS: Débil")
# plotOverride(fuerteMedio,"Cancer: Fuerte, IS: Medio")
# plotOverride(fuerteFuerte,"Cancer: Fuerte, IS: Fuerte")
