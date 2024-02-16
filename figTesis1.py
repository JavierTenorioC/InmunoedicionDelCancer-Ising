#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 00:58:33 2023

@author: jatec
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

# Datos de las distribuciones normales
mu_elim = 0  # Media de la fase de eliminación
sigma_elim = 1  # Desviación estándar de la fase de eliminación

mu_equilibrio = 2  # Media de la fase de equilibrio
sigma_equilibrio = 0.5  # Desviación estándar de la fase de equilibrio

mu_escape = 3  # Media de la fase de escape
sigma_escape = 1.5  # Desviación estándar de la fase de escape

# Valores para el eje x (nivel de fuerza)
x = np.linspace(0, 1, 100)

# Funciones de densidad de probabilidad para las distribuciones normales
pdf_elim = norm.pdf(x, mu_elim, sigma_elim)
pdf_equilibrio = norm.pdf(x, mu_equilibrio, sigma_equilibrio)
pdf_escape = norm.pdf(x, mu_escape, sigma_escape)

# Ajustar el rango de las funciones de probabilidad entre 0 y 1
pdf_elimCancer = norm.pdf(x, 0.3, 0.05) 
pdf_equilibrioCancer = norm.pdf(x, 0.15, 0.05)
pdf_escapeCancer = norm.pdf(x, 0.6, 0.05) 

pdf_elimIS = norm.pdf(x, 0.7, 0.05) 
pdf_equilibrioIS = norm.pdf(x, 0.3, 0.05) 
pdf_escapeIS = norm.pdf(x, 0.4, 0.05) 

# Estilo personalizado
plt.style.use('seaborn-whitegrid')

# Crear el subplot
fig, axs = plt.subplots(3, 1, figsize=(4, 5))

# Graficar las distribuciones normales en cada subplot
axs[0].plot(x, pdf_elimCancer,linestyle='dashed', color="red")
axs[0].plot(x, pdf_elimIS)
axs[1].plot(x, pdf_equilibrioIS, label='Sistema Inmune')
axs[1].plot(x, pdf_equilibrioCancer, label='Cáncer', linestyle='dashed', color="red")
axs[2].plot(x, pdf_escapeCancer, linestyle='dashed', color="red")
axs[2].plot(x, pdf_escapeIS)

# Etiquetas y títulos de los subplots
# axs[0].set_xlabel('Nivel de fuerza')
# axs[1].set_xlabel('Nivel de fuerza')
axs[2].set_xlabel('Nivel de fuerza')

axs[1].set_ylabel('Densidad de Probabilidad')
axs[1].legend()

# Ajustar los subplots para evitar superposición de títulos y etiquetas
plt.tight_layout()

title="hiper3fases"
plt.savefig(f'{title}.pdf', format="pdf", bbox_inches="tight")

# Mostrar la gráfica
plt.show()

