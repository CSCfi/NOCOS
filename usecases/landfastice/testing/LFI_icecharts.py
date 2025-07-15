
## Plotting fastice for multiple days

# This script requires a valid DESP token. This can be created by running 
# python3 ~/polytope_examples_GIT/desp-authentication.py
# in the conda env polytope2025May

readin=True
saveplot=True

startyear='2018'
endyear='2024'

# Maybe these help in the Interactive window to reload modules?
# %reload_ext autoreload
# %autoreload 2

import earthkit.data
import earthkit.plots
import earthkit.regrid
import datetime



### Load user configurations from file
import os
os.chdir('/home/andreag/nocoscode/NOCOS-gitv1/usecases/landfastice_occurrence/testing')
import sys
sys.path.append(os.getcwd())
from read_config import read_configfile

#icechartsRAW=earthkit.data.from_source("file","/media/volume/data_storage_andrea/icecharts/GreenlandTOPNW_fasticeOCC_2019jan.nc")
icechartsRAW=earthkit.data.from_source("file",'/media/volume/data_storage_andrea/icecharts/GreenlandTOPNW_fastice_JAN_'+startyear+'-'+endyear+'_ymonmean_south.nc')
icecharts=icechartsRAW.to_xarray() # Needed for date in plot title



##########################################
### Make plot of fastice conditions on a specific day
###########################################


#### The field to plot
# plottimestamp=15
# fasticetoplot=dataICE[0].clone(values=fasticedata[plottimestamp,:]) # Clone something random to make the field into a grib field again

from earthkit.plots.geo import domains
import earthkit.data
import earthkit.plots
import numpy as np

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

# # Set up the plot
# chart = earthkit.plots.Map(domain=greenland_domain)
# # chart = earthkit.plots.Map(domain=qaanaaq_domain)

# # Pcolormesh plot
# chart.grid_cells(fasticetoplot,interpolate=dict(method='nearest'),
#                 style=earthkit.plots.styles.Style(colors="RdYlBu_r",
#                                                 levels=[0,1,1.001]))

# # Elements on the plot
# chart.coastlines(resolution='high',zorder=3)
# chart.land(resolution='high',zorder=2)
# chart.gridlines(zorder=4)
# chart.legend(label="Landfast ice [yes/no]") # This is the colorbar

# # Title of the plot
# plotdate=str(dataICExr.avg_siconc.forecast_reference_time[plottimestamp+fasticeduration-1].values)[0:10]
# chart.title(str(fasticeduration)+"-day fastice persistence on "+ plotdate +", "+climateDTmodel)

# # Save the plot as png
# import os
# os.chdir('/home/andreag/nocoscode/NOCOS-gitv1/usecases/landfastice_occurrence/testing')
# import sys
# sys.path.append(os.getcwd())
# import matplotlib.pyplot as plt
# # plt.savefig('./plots/fastice-'+str(fasticeduration)+'day_'+climateDTmodel+'_'+plotdate+'.png', bbox_inches = 'tight')

# chart.show()


##########################################
# ### Plot average fast ice coverage
########################################


# # The field to plot
# endtimestamp=canvaswithland.shape[0]-fasticeduration
# # mean_fasticecover=np.mean(canvaswithland[:,:],axis=0) # average over time -> percentage of fast ice coverage
# mean_fasticecover=np.mean(fasticedata[:,:],axis=0) # average over time -> percentage of fast ice coverage
# fasticeOCCtoplot=dataICE[((fasticeduration-1)+endtimestamp)*3].clone(values=mean_fasticecover, name="Avg. fast ice coverage", shortName="fastice", units="") # Check metadata with e.g.: fastice.metadata("name")
# print(fasticeOCCtoplot.ls())

fasticeOCCtoplot=icecharts

chart = earthkit.plots.Map(domain=greenland_domain)
# chart = earthkit.plots.Map(domain=qaanaaq_domain)
chart.grid_cells(fasticeOCCtoplot,z='FA',
                style=earthkit.plots.styles.Style(colors="jet",
                                                levels=[0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1,1.001]))

chart.coastlines(resolution='high',zorder=3)
chart.land(resolution='high',zorder=2)
chart.gridlines(zorder=4)
chart.legend(label="time-average fast ice coverage [fraction]")

# chart.title("Average "+str(fasticeduration)+"-day fastice occurrence\n between "+ date_start.strftime("%Y-%m-%d") +" and " + date_end.strftime("%Y-%m-%d")  +", "+climateDTmodel)
chart.title('Average fastice occurrence\n in Januaries (years '+startyear+'-'+endyear+') from icecharts')

# daterange=date_start.strftime("%Y-%m-%d") +"_" + date_end.strftime("%Y-%m-%d")

import os
os.chdir('/home/andreag/nocoscode/NOCOS-gitv1/usecases/landfastice_occurrence/testing')
import sys
sys.path.append(os.getcwd())
import matplotlib.pyplot as plt
if saveplot:
    plt.savefig('./plots/AVGfastice-icecharts_Jan_'+startyear+'-'+endyear+'.png', bbox_inches = 'tight')

chart.show()
