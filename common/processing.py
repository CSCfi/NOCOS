# common/processing.py
import xarray as xr
import numpy as np

def normalize_data(dataset: xr.DataArray):
    """Normalize data between 0 and 1."""
    return (dataset - dataset.min()) / (dataset.max() - dataset.min())

def apply_mask(dataset: xr.DataArray, mask: np.ndarray):
    """Apply a binary mask to an xarray dataset."""
    return dataset.where(mask)
def do_calc_smth(ds):

    fds=ds
    return fds




def MeanSic(ds):
    """
    Process the dataset to extract Mean Sea Ice Concentration (MeanSic).
    Selects data within a geographical range and applies a mask to filter thick ice with voids.

    Parameters:
    ds (xarray.Dataset): Input dataset containing ice concentration and thickness.

    Returns:
    xarray.Dataset: Processed dataset with the mean sea ice concentration.
    """

    # Define the selection variables
    lon1, lon2 = 9, 30  # Longitude range
    lat1, lat2 = 53, 66  # Latitude range
    start_date = "2024-11-01"  # Start date
    end_date = "2025-05-31"  # End date

    # Select the spatial and temporal region
    ds_t_reg = ds.sel(
        latitude=slice(lat1, lat2), 
        longitude=slice(lon1, lon2),
        time=slice(start_date, end_date)
    )

    # Apply the conditions for masking
#    masked_data = ds_t_reg.where(
#        (ds_t_reg.avg_sithick > 0.5) & 
#        (ds_t_reg.avg_siconc > 0.975) & 
#        (ds_t_reg.avg_siconc <= 0.999)
#    )
    masked_data = ds_t_reg.where(
        (ds_t_reg.avg_siconc > 0.5) 
    )

    # Compute the mean over time
    mean_sic = masked_data.avg_siconc.mean(dim="time", skipna=True)
    #rid_prob = masked_data.avg_siconc.count(dim="time")/num_days

    return mean_sic