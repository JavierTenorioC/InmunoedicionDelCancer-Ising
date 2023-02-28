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

df = pandas.read_csv('model_data.csv')


# ax.set_title('style: {!r}'.format(sty), color='C0')
plt.figure()
# plt.xlabel("Iteration(days)")
# plt.ylabel("Number of cells")
plt.plot(df['Step'][:],df['AntiCancer'][:],label="Anticancer",color = "#eab676" )
# plt.legend()

# plt.figure()
plt.xlabel("Iteration(days)")
plt.ylabel("Number of cells")
plt.plot(df['Step'][:],df['ProCancer'][:],label="ProCancer", color = "#76b5c5")
plt.legend()

Step100 = df[df['Step' > 0]]