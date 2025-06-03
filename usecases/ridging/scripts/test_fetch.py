NOCOSDIR='/home/ilja/NOCOS'
import sys
import os

# Add the path to sys.path
sys.path.append(os.path.abspath(NOCOSDIR))

from common.data_fetching import DataFetcher

# Initialize DataFetcher
broker = DataFetcher()
# Fetch data
dataset = broker.fetch_data()
# Print dataset summary
if dataset:
    print(dataset)

