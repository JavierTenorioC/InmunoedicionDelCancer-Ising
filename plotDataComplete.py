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

import pandas
import numpy as np
import matplotlib.pyplot as plt
import colorsys
import matplotlib.colors as mc
import matplotlib as mpl

# mpl.style.use(sty)
def plotOverride(df,title):
    plt.figure()
    plt.title(title)
    plt.grid(True)
    plt.plot(df['Step'][:],df['AntiCancer'][:],label="Sistema Inmune",color = "blue" )
    plt.xlabel("Iteration(days)")
    plt.ylabel("Number of cells")
    plt.plot(df['Step'][:],df['ProCancer'][:],label="Cancer", color = "red")
    plt.legend()
    plt.savefig(f'{title}.pdf', format="pdf", bbox_inches="tight")

### Código para código que empieza inicializando todo a 0
df = pandas.read_csv('/home/jatec/Desktop/InmunoedicionDelCancer-Ising/model_data[Thu Jun  8 23:54:04 2023].csv')
plt.figure()
title = "Cancer: Medio, IS: Medio"
plt.title(title)
for i in range(0,len(df)-101,101):
    plt.plot(df['Step'][i+1:i+100],df['AntiCancer'][i+1:i+100],color = "blue" )
    plt.plot(df['Step'][i+1:i+100],df['ProCancer'][i+1:i+100], color = "red")
plt.plot(df['Step'][len(df)-101 + 1:],df['AntiCancer'][len(df)-101+1:],label="Sistema Inmune",color = "blue" )
plt.plot(df['Step'][len(df)-101 + 1:],df['ProCancer'][len(df)-101+1:],label="Cancer", color = "red")
plt.grid(True)
plt.xlabel("Iteration(days)")
plt.ylabel("Number of cells")
plt.legend()
plt.savefig(f'{title}.pdf', format="pdf", bbox_inches="tight")

# for i in range(0,len(df)-101,101):
#     print(i)

### Código para cuando empieza en poblaciones diferentes a 0
df = pandas.read_csv('/home/jatec/Desktop/InmunoedicionDelCancer-Ising/model_data[Thu Jun  8 21:42:16 2023].csv')
plt.figure()
title = "Cancer: Debil, IS: Debil"
plt.title(title)
for i in range(0,len(df)-101,101):
    plt.plot(df['Step'][i+1:i+101],df['AntiCancer'][i+1:i+100],color = "blue" )
    plt.plot(df['Step'][i+1:i+101],df['ProCancer'][i+1:i+100], color = "red")
plt.plot(df['Step'][len(df)-100 + 1:],df['AntiCancer'][len(df)-100+1:],label="Sistema Inmune",color = "blue" )
plt.plot(df['Step'][len(df)-100 + 1:],df['ProCancer'][len(df)-100+1:],label="Cancer", color = "red")
plt.grid(True)
plt.xlabel("Iteration(days)")
plt.ylabel("Number of cells")
plt.legend()
plt.savefig(f'{title}.pdf', format="pdf", bbox_inches="tight")


# cancer IS
debilDebil = df.query("`stdIS` <= 0.2 and `stdCancer` <= 0.2 and  `meanIS`  <= 0.35 and `meanCancer` <= 0.35 ")
debilMedio = df.query("`stdIS` <= 0.2 and `stdCancer` <= 0.2 and  `meanIS`  >= 0.35 and `meanIS`  <= 0.75 and `meanCancer` <= 0.35 ")
debilFuerte = df.query("`stdIS` <= 0.2 and `stdCancer` <= 0.2 and  `meanIS`  >= 0.75 and `meanCancer` <= 0.35 ")

# cancer IS
medioDebil = df.query("`stdIS` <= 0.2 and `stdCancer` <= 0.2 and  `meanIS`  <= 0.35 and `meanCancer` >= 0.35 and `meanCancer` <= 0.75 ")
medioMedio = df.query("`stdIS` <= 0.2 and `stdCancer` <= 0.2 and  `meanIS`  >= 0.35 and `meanIS`  <= 0.75 and `meanCancer` >= 0.35 and `meanCancer` <= 0.75 ")
medioFuerte = df.query("`stdIS` <= 0.2 and `stdCancer` <= 0.2 and `meanIS`  <= 0.75 and `meanCancer` >= 0.35 and `meanCancer` <= 0.75  ")

# cancer IS
fuerteDebil = df.query("`stdIS` <= 0.2 and `stdCancer` <= 0.2 and  `meanIS`  >= 0.75 and `meanCancer` <= 0.35")
fuerteMedio = df.query("`stdIS` <= 0.2 and `stdCancer` <= 0.2 and  `meanIS`  >= 0.75 and `meanCancer` >= 0.35 and `meanCancer` <= 0.75 ")
fuerteFuerte = df.query("`stdIS` <= 0.2 and `stdCancer` <= 0.2 and  `meanIS`  >= 0.75 and `meanCancer` >= 0.75 ")

plotOverride(debilDebil,"Cancer: Débil, IS: Débil")
plotOverride(debilMedio,"Cancer: Débil, IS: Medio")
plotOverride(debilFuerte,"Cancer: Débil, IS: Fuerte")

plotOverride(medioDebil,"Cancer: Medio, IS: Débil")
plotOverride(medioMedio,"Cancer: Medio, IS: Medio")
plotOverride(medioFuerte,"Cancer: Medio, IS: Fuerte")

plotOverride(fuerteDebil,"Cancer: Fuerte, IS: Débil")
plotOverride(fuerteMedio,"Cancer: Fuerte, IS: Medio")
plotOverride(fuerteFuerte,"Cancer: Fuerte, IS: Fuerte")
