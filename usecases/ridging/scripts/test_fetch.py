NOCOSDIR='/home/ilja/NOCOS_locdev/NOCOS/'
import sys
import os

# Add the path to sys.path
sys.path.append(os.path.abspath(NOCOSDIR))

from common.data_fetching import DataFetcher

# Initialize DataFetcher
broker = DataFetcher()
# Fetch data
dataset = broker.fetch_data_polytope()
# Print dataset summary
if dataset:
    print(dataset)

