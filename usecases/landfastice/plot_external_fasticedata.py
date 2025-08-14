

# This script requires a valid DESP token. This can be created by running 
# python3 ~/polytope_examples_GIT/desp-authentication.py
# in the conda env polytope2025May

import earthkit.data
import earthkit.plots
#import earthkit.regrid
import datetime
from earthkit.plots.geo import domains
import numpy as np

################
## User settings
################

# ClimateDT model (ICON or IFS-NEMO)
# datasource='icecharts'
datasource='HYCOM-CICE'

saveplot=True

# Which month shall be plotted? (1-12)
month=3
monthname= datetime.datetime(2099,month,15).strftime("%B")

# First and last year of the climatology to be plotted
clima_fromyear=2010
clima_toyear=2019

# Region to be processed (Greenland or Arctic)
mapregion='Greenland'
# mapregion='Arctic'

if datasource=="icecharts":
    # Filename to plot
    filepath='/media/volume/data_storage_andrea/icecharts/GreenlandTOPNW_fastice_mon'+str(month).zfill(2)+'_'+str(clima_fromyear)+'-'+str(clima_toyear)+'_ymonmean.nc'
    # Name of the landfastice variable in the data file
    varLFI='FA'
    # Name of latitude/longitude coordinates
    varLON='lon'
    varLAT='lat'
elif datasource=="HYCOM-CICE":
    # Filename to plot
    fasticeduration="4"
    filepath='/media/volume/data_storage_andrea/HYCOM-CICE/greentopnw_'+fasticeduration+'day-fastice_'+str(clima_fromyear)+'-'+str(clima_toyear)+'_climatology_mon'+str(month).zfill(2)+'.nc'
    # Name of the landfastice variable in the data file
    varLFI='ff'
    # Name of latitude/longitude coordinates
    varLON='ULON'
    varLAT='ULAT'

# Title to be shown on the plot
plottitle="Average fastice occurrence\n " +"Climatology for " + monthname+" "+str(clima_fromyear)+"-"+str(clima_toyear)+" from "+datasource

################
## End of user settings
################

dataRAW=earthkit.data.from_source("file",filepath)
plotdata=dataRAW.to_xarray() 

##########################################
### Make plot of fastice conditions on a specific day
###########################################


#### Plot domains

import cartopy.crs as ccrs
crs = ccrs.NorthPolarStereo(central_longitude=10)


arctic_domain = domains.Domain(
    [-2800000, 2800000, -2800000, 2800000],
    crs=ccrs.NorthPolarStereo(),
    name="Arctic",
)
greenland_domain = domains.Domain(
    [-1400000, 800000, -2500000, -400000],
    crs=ccrs.NorthPolarStereo(central_longitude=-35),
    name="Greenland",
)
qaanaaq_domain = domains.Domain(
    [-300000, 100000, -1600000, -1200000],
    crs=ccrs.NorthPolarStereo(central_longitude=-67),
    name="Qaanaaq",
)


##########################################
# ### Plot
########################################

chart = earthkit.plots.Map(domain=greenland_domain)
# chart.grid_cells(plotdata,z=varLFI,
#                 style=earthkit.plots.styles.Style(colors="jet",
#                                                 levels=[0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.00001])) # If the last level is 1. instead of 1.000001, then areas with 100% covereage are plotted white instead of red.
chart.grid_cells(plotdata,x=varLON, y=varLAT,z=varLFI,
                style=earthkit.plots.styles.Style(colors="jet",
                                                levels=[0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.00001])) # If the last level is 1. instead of 1.000001, then areas with 100% covereage are plotted white instead of red.

chart.coastlines(resolution='high',zorder=3)
chart.land(resolution='high',zorder=2)
chart.gridlines(zorder=4)
chart.legend(label="Average fast ice coverage [fraction]")

# chart.title("Average "+str(fasticeduration)+"-day fastice occurrence\n between "+ date_start.strftime("%Y-%m-%d") +" and " + date_end.strftime("%Y-%m-%d")  +", "+climateDTmodel)
chart.title(plottitle)


if saveplot:
    import matplotlib.pyplot as plt
    plt.savefig('./images/fasticeclimatology_'+monthname+'_'+str(clima_fromyear)+'-'+str(clima_toyear)+'_'+datasource+'.png', bbox_inches = 'tight')





