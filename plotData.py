#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 11:46:15 2023

@author: javiert
"""
import matplotlib.pyplot as plt
import numpy as np

table = [["AB",	"R",	"H",	"BB",	"SO",	"Str",	"HR"], 
         [0.2073170732,	0.07317073171,	0.04268292683,	0.01219512195,	0.04268292683,	0.6036585366	 ,0.01829268293]]

table_transposed = np.array(table).T.tolist()
print(table_transposed)

xs = [i for i in range(len(table[0]))]

table_transposed.sort(key=lambda x: x[1])

plt.bar(xs,table[:][1] )
plt.xticks(xs,table[:][0])



