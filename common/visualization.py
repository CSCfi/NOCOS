import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cf
import xarray as xr
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import os
import numpy as np
import matplotlib.colors as mcolors
from common import config
from common.utils import ensure_directory_exists

def PlotMeanSIC(datax, title="Mean sea ice concentration",  save=True):
    """
    Plots the ridged ice probability on a map using Cartopy.

    Parameters:
    rid_prob (xarray.Dataset or xarray.DataArray): Processed dataset containing ridged ice probability.
    title (str): Plot title.
    save (bool): Whether to save the plot as a PNG file.
    """   
    # Convert dataset to DataArray (assumes multiple variables exist)
#    if isinstance(rid_prob, xr.Dataset):
#        rid_prob = rid_prob.to_array().sum(dim="variable")  # Sum across all variables if needed
    fig, ax = plt.subplots(figsize=(8, 6), subplot_kw={"projection": ccrs.Mercator()})
    original_cmap = plt.cm.Purples
    colors = original_cmap(np.linspace(0.1, 1.0, 256))  # Exclude the first 10% of the colormap
    colors[0] = [1, 1, 1, 1]  # Set the last color to white (RGBA)
    new_cmap = mcolors.LinearSegmentedColormap.from_list("Purples_truncated", colors)
    vmax=0.5
    # Plot the ridged ice probability
    datax.plot(
        ax=ax,
        transform=ccrs.PlateCarree(),
        cmap=new_cmap,
        vmax=vmax,
        cbar_kwargs={"label": "SIC"}
    )

    # Set plot features
    ax.coastlines(color=(0.7, 0.7, 0.7))
    ax.add_feature(cf.BORDERS, color=(0.7, 0.7, 0.7))

    # Load and add the logo
    logo_path = os.path.join(config.NOCOSDIR, "logos/NOCOS-DT_logo_RGB_fullcolour.png")
    
    if os.path.exists(logo_path):
        logo = plt.imread(logo_path)
        imagebox = OffsetImage(logo, zoom=0.08)  # Adjust zoom for size
        ab = AnnotationBbox(imagebox, (0.23, 0.95), frameon=False, xycoords="axes fraction")
        ax.add_artist(ab)
    else:
        print(f"Warning: Logo not found at {logo_path}")

    # Set title
    ax.set_title(title)

    # Ensure the output directory exists
    output_dir = os.path.join(config.OUTPUT_DIR, "fig")
    ensure_directory_exists(output_dir)

    # Save the plot
    if save:
        output_path = os.path.join(output_dir, f"{title.replace(' ', '_').lower()}.png")
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        print(f"Plot saved to: {output_path}")

    plt.show()
