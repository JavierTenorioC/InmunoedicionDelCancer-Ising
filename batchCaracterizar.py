"""
Este script de Python se utiliza para caracterizar el sistema dentro de los rangos de los parámetros relacionados a 
la media de cada una de las distribuciones de probabilidad Gaussiana.

Se ejecuta escribiendo `python3 batchCaracterizar.py` 

Autor: Javier Tenorio
Fecha: 01/2024
Versión: 1.0
"""
from mesa import *
from cancerInmunoediting.model import CancerInmunoediting
import pandas as pd
import numpy as np
import time

start_time = time.time()

params = {"meanIS": np.linspace(0.01,1,10),
          "stdIS": 0.05,
          "meanCancer": np.linspace(0.01,1,10),
          "stdCancer": 0.05,
          }

results = batch_run(
    CancerInmunoediting,
    parameters=params,
    iterations=10, #25
    max_steps=100,
    number_processes=4,
    data_collection_period=1,
    display_progress=True
)

end_time = time.time()

execution_time = end_time - start_time
print(f"Tiempo de ejecución: {execution_time} segundos")
results_df = pd.DataFrame(results)
results_df.to_csv(f"{end_time}-caracterizar.csv")
