from mesa import *
from cancerInmunoediting.model import CancerInmunoediting
import pandas as pd
import numpy as np
import random 
# 0.35 meanIS 0.01 stdIS
# 0.75 meanCancer 0.01 stdIS
# np.arange(0.1, 1, 0.4)
'''
params = {"meanIS": 0.4,
          "stdIS": 0.05,
          "meanCancer": 0.6,
          "stdCancer": 0.05,
          }
'''
import time

for i in range(1,11):

	# Guarda el tiempo de inicio
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
	    iterations=10, #25
	    max_steps=100,
	    number_processes=i,
	    data_collection_period=1,
	    display_progress=True
	)

	# Guarda el tiempo de finalización
	end_time = time.time()

	# Calcula el tiempo de ejecución en segundos
	execution_time = end_time - start_time
	print(f"Tiempo de ejecución: {execution_time} segundos")
	#results_df = pd.DataFrame(results)
	#results_df.to_csv(f"{end_time}-1-Barrido.csv")
