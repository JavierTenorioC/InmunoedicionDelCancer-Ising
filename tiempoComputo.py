"""
Este script de Python se utiliza para calcular el tiempo de ejecución del programa al aumentar los procesos de 1 a 10.


Se fija la semilla del algoritmo pseudoaleatorio de la librería random a 100, con el fin de garantizar que se tengan 
las mismas condiciones iniciales. 

Se ejecuta escribiendo `python3 tiempoComputo.py` 

Autor: Javier Tenorio
Fecha: 01/2024
Versión: 1.0
"""
from mesa import *
from cancerInmunoediting.model import CancerInmunoediting
import pandas as pd
import numpy as np
import random 
import time

for i in range(1,11):

	start_time = time.time()
	random.seed(100)
	params = {"meanIS": np.linspace(0.01,1,10),
		  "stdIS": 0.05,
		  "meanCancer": np.linspace(0.01,1,10),
		  "stdCancer": 0.05,
		  }

	results = batch_run(
	    CancerInmunoediting,
	    parameters=params,
	    iterations=25, 
	    max_steps=100,
	    number_processes=i,
	    data_collection_period=1,
	    display_progress=True
	)

	end_time = time.time()

	execution_time = end_time - start_time
	print(f"Tiempo de ejecución: {execution_time} segundos")
	results_df = pd.DataFrame(results)
	results_df.to_csv(f"{end_time}-{i}-Barrido.csv")
