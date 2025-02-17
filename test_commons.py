from common.data_fetching import DataFetcher
from common.processing import MeanSic
from common.visualization import PlotMeanSIC
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt


from common import config

print(config.DATA_DIR)  # Output: data/
print(config.OUTPUT_DIR)  # Output: output/

# TODO  Authentication step :) !

import os
os.chdir(config.DATA_DIR)
print(os.getcwd())  # where are we ?

broker=DataFetcher()

#data=broker.fetch_data_cachb()
data=broker.fetch_data_polytope()


print(data)
# Test Processing
#normalized_data = normalize_data(data)
rid_data=MeanSic(data)
# Test Visualization
PlotMeanSIC(rid_data, title="dummy title")

