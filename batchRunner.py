#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 06:30:56 2023

@author: javiert
"""
from mesa import *
from cancerInmunoediting.model import CancerInmunoediting
import pandas as pd
import numpy as np

params = {"meanIS": np.arange(0.1, 1, 0.4),
          "stdIS": np.arange(0.1, 1, 0.4),
          "meanCancer": np.arange(0.1, 1, 0.4),
          "stdCancer": np.arange(0.1, 1, 0.4),
          }

results = batch_run(
    CancerInmunoediting,
    parameters=params,
    iterations=25,
    max_steps=100,
    number_processes=1,
    data_collection_period=1,
    display_progress=True
)


results_df = pd.DataFrame(results)
results_df.to_csv("model_data.csv")
