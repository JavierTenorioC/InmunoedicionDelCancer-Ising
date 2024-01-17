#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from mesa import *
from cancerInmunoediting.model import CancerInmunoediting
import pandas as pd
import numpy as np
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
params = {"meanIS": [0.7],
          "stdIS": 0.05,
          "meanCancer": [0.3],
          "stdCancer": 0.05,
          }

results = batch_run(
    CancerInmunoediting,
    parameters=params,
    iterations=25, #25
    max_steps=100,
    number_processes=1,
    data_collection_period=1,
    display_progress=True
)
import time

# seconds passed since epoch
seconds = time.time()

# convert the time in seconds since the epoch to a readable format
local_time = time.ctime(seconds)

print("Local time:", )

results_df = pd.DataFrame(results)
results_df.to_csv(f"elim.csv")

params = {"meanIS": [0.3],
          "stdIS": 0.05,
          "meanCancer": [0.15],
          "stdCancer": 0.05,
          }

results = batch_run(
    CancerInmunoediting,
    parameters=params,
    iterations=25, #25
    max_steps=100,
    number_processes=3,
    data_collection_period=1,
    display_progress=True
)
import time

# seconds passed since epoch
seconds = time.time()

# convert the time in seconds since the epoch to a readable format
local_time = time.ctime(seconds)

print("Local time:", )

results_df = pd.DataFrame(results)
results_df.to_csv(f"equil.csv")

params = {"meanIS": [0.4],
          "stdIS": 0.05,
          "meanCancer": [0.6],
          "stdCancer": 0.05,
          }

results = batch_run(
    CancerInmunoediting,
    parameters=params,
    iterations=25, #25
    max_steps=100,
    number_processes=3,
    data_collection_period=1,
    display_progress=True
)
import time

# seconds passed since epoch
seconds = time.time()

# convert the time in seconds since the epoch to a readable format
local_time = time.ctime(seconds)

print("Local time:", )

results_df = pd.DataFrame(results)
results_df.to_csv(f"escape.csv")
