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
    plt.plot(df['Step'][:],df['AntiCancer'][:],label="Anticancer",color = "#eab676" )
    plt.xlabel("Iteration(days)")
    plt.ylabel("Number of cells")
    plt.plot(df['Step'][:],df['ProCancer'][:],label="ProCancer", color = "#76b5c5")
    plt.legend()
    plt.savefig(f'{title}.pdf', format="pdf", bbox_inches="tight")


df = pandas.read_csv('model_data.csv')
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

# ax.set_title('style: {!r}'.format(sty), color='C0')


# distr = { "d" : [0.25 , 0.075],
#               "m" : [0.5 , 0.075],
#               "f" : [0.75, 0.075]
#     }

# distr = { "d" : [0 , 0.05],
#               "m" : [0 , 0.075],
#               "f" : [0, 0.5]
#     }

# distr = { "d" : [25 , 15],
#               "m" : [45 , 5],
#               "f" : [75, 10]
#     }

# distr = { "d" : [.25 , .15],
#               "m" : [.45 , .075],
#               "f" : [.75, .10]
#     }

# distr = { "d" : [25 , 15],
#               "m" : [45 , 5],
#               "f" : [75, 10]
#     }


# import numpy as np
# import matplotlib.pyplot as plt
# from scipy.stats import norm

# x_axis = np.arange(0, 100, 1)
# # Mean = 0, SD = 2.
# plt.plot(x_axis, norm.pdf(x_axis,distr["d"][0],distr["d"][1]), label = f'μ: {distr["d"][0]}, σ: {distr["d"][1]}')
# plt.plot(x_axis, norm.pdf(x_axis,distr["m"][0],distr["m"][1]), label = f'μ: {distr["m"][0]}, σ: {distr["m"][1]}')
# plt.plot(x_axis, norm.pdf(x_axis,distr["f"][0],distr["f"][1]), label = f'μ: {distr["f"][0]}, σ: {distr["f"][1]}')
# plt.legend(title="Parámetros")
# plt.show()