from common.data_fetching import DataFetcher

# Initialize DataFetcher
broker = DataFetcher()
# Fetch data
dataset = broker.fetch_data()
# Print dataset summary
if dataset:
    print(dataset)