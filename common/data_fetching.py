# common/data_fetching.py
import xarray as xr
import numpy as np
from common import config
import earthkit.data

class DataFetcher:
    """Base class for fetching data for different applications."""

    def __init__(self, source=None, params=None):
        self.source = source or config.DATA_DIR  # Use default data directory if no source is provided
        self.params = params or config.request_cacb_IFSNEMO_o2d

    def fetch_data_cachb(self):
        """Fetch data from a Zarr store."""
        url = self.params.get("url")  # ✅ Correct dictionary access  
        try:
            print(f"Fetching dataset from {url}...")
            ds = xr.open_dataset(
                url,
                chunks={}, 
                engine="zarr",
                storage_options={"client_kwargs": {"trust_env": True}}
            )
            print("Dataset successfully loaded.")
            return ds
        except Exception as e:
            print(f"Error fetching dataset: {e}")
            return None

    def fetch_data_polytope(self):
        """Fetch data from a FDB? store."""
        month=1
        year=2025
        date_str = f"{year:04d}{month:02d}01"

        # Create a copy of the request template and update the date field
        request = config.request_template_m1.copy()
        request['date'] = date_str

        # Fetch data for the current request
        print(f"Fetching data for {date_str}...")
        data = earthkit.data.from_source(
            "polytope",
            "destination-earth",
            request,
            address="polytope.lumi.apps.dte.destination-earth.eu",
            stream=False
        )
        return data


    def preprocess_data(self, data):
        """Basic preprocessing, e.g., converting to xarray."""
        if isinstance(data, np.ndarray):
            return xr.DataArray(data)
        return data