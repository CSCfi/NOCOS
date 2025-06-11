
## Plotting fastice for multiple days

# This script requires a valid DESP token. This can be created by running 
# python3 ~/polytope_examples_GIT/desp-authentication.py
# in the conda env polytope2025May

readin=True

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

configs=read_configfile('config_LFI_calc_REF.yml')
fasticeduration= 4 # days
climateDTmodel= 'ICON' # "IFS-NEMO" or "ICON"
# climateDTmodel=configs['climateDT']['model'] # "IFS-NEMO" or "ICON"
date_start=configs['LFI']['startdate']
date_end=configs['LFI']['enddate']

# Process user input
REQ_date_start=date_start-datetime.timedelta(days=fasticeduration-1) # For fasticeduration of 1 day we do not need to download "yesterday"
REQ_date_end=date_end
REQ_daterange= REQ_date_start.strftime("%Y%m%d")+"/to/"+REQ_date_end.strftime("%Y%m%d")

# request and download ice data
import os
os.chdir('/home/andreag/nocoscode/NOCOS-gitv1/')
import sys
sys.path.append(os.getcwd())
from common.download_icedata_c import request_icedata_subarea


if readin:
    # dataICE=request_icedata_subarea(activity="ScenarioMIP",experiment="SSP3-7.0",model=climateDTmodel,date=REQ_daterange,
                                # param="263001/263003/263004")
    dataICE=request_icedata_subarea(activity="CMIP6",experiment="hist",model=climateDTmodel,date=REQ_daterange,
                                subarea="greenland", param="263001/263003/263004")


dataICExr=dataICE.to_xarray() # Needed for date in plot title


##### Extract data from grib object

siconc=dataICE[0::3].values
siu=dataICE[1::3].values
siv=dataICE[2::3].values

##### Calculate drift speed

import numpy as np
speed=np.sqrt(siu**2+siv**2)

##### Calculate areas covered by fast ice"

canvaswithland=speed.copy()
fasticemask=np.logical_and(np.less(speed,5e-4),np.greater(siconc,0.90))
landmask=np.isnan(canvaswithland)
watermask=np.logical_and(np.logical_not(landmask),np.logical_not(fasticemask))
canvaswithland[watermask]=0.
canvaswithland[fasticemask]=1. # Number of time stamps: user defined date range + fasticeduration

def fastice_for_x_days(fasticeN,daysN):
    # fasticeN shape [days,healpixcells]
    if daysN==1:
        return fasticeN
    else:
        # fasticeNm1=np.logical_and(fasticeN[0:-1,:],fasticeN[1:,:]) # Has there been fastice today and yesterday?
        fasticeNm1=np.logical_and(fasticeN[0:-1],fasticeN[1:]) # Has there been fastice today and yesterday?
        daysNm1=daysN - 1
        return fastice_for_x_days(fasticeNm1,daysNm1) # Call again for one day less


fasticedata=fastice_for_x_days(canvaswithland,fasticeduration) # Number of time stamps: user defined date range\n"


##########################################
### Make plot of fastice conditions on a specific day
###########################################


#### The field to plot
plottimestamp=15
fasticetoplot=dataICE[0].clone(values=fasticedata[plottimestamp,:]) # Clone something random to make the field into a grib field again

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

# Set up the plot
chart = earthkit.plots.Map(domain=greenland_domain)
# chart = earthkit.plots.Map(domain=qaanaaq_domain)

# Pcolormesh plot
chart.grid_cells(fasticetoplot,interpolate=dict(method='nearest'),
                 style=earthkit.plots.styles.Style(colors="RdYlBu_r",
                                                   levels=[0,1,1.001]))

# Elements on the plot
chart.coastlines(resolution='high',zorder=3)
chart.land(resolution='high',zorder=2)
chart.gridlines(zorder=4)
chart.legend(label="Landfast ice [yes/no]") # This is the colorbar

# Title of the plot
plotdate=str(dataICExr.avg_siconc.forecast_reference_time[plottimestamp+fasticeduration-1].values)[0:10]
chart.title(str(fasticeduration)+"-day fastice persistence on "+ plotdate +", "+climateDTmodel)

# Save the plot as png
import os
os.chdir('/home/andreag/nocoscode/NOCOS-gitv1/usecases/landfastice_occurrence/testing')
import sys
sys.path.append(os.getcwd())
import matplotlib.pyplot as plt
plt.savefig('./plots/fastice-'+str(fasticeduration)+'day_'+climateDTmodel+'_'+plotdate+'.png', bbox_inches = 'tight')

chart.show()


##########################################
# ### Plot average fast ice coverage
########################################

# The field to plot
endtimestamp=canvaswithland.shape[0]-fasticeduration
mean_fasticecover=np.mean(canvaswithland[:,:],axis=0) # average over time -> percentage of fast ice coverage
fasticeOCCtoplot=dataICE[((fasticeduration-1)+endtimestamp)*3].clone(values=mean_fasticecover, name="Avg. fast ice coverage", shortName="fastice", units="") # Check metadata with e.g.: fastice.metadata("name")
print(fasticeOCCtoplot.ls())


chart = earthkit.plots.Map(domain=greenland_domain)
# chart = earthkit.plots.Map(domain=qaanaaq_domain)
chart.grid_cells(fasticeOCCtoplot,interpolate=dict(method='nearest'),
                 style=earthkit.plots.styles.Style(colors="jet",
                                                   levels=[0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1,1.001]))

chart.coastlines(resolution='high',zorder=3)
chart.land(resolution='high',zorder=2)
chart.gridlines(zorder=4)
chart.legend(label="time-average fast ice coverage [fraction]")

chart.title("Average "+str(fasticeduration)+"-day fastice occurrence\n between "+ date_start.strftime("%Y-%m-%d") +" and " + date_end.strftime("%Y-%m-%d")  +", "+climateDTmodel)

daterange=date_start.strftime("%Y-%m-%d") +"_" + date_end.strftime("%Y-%m-%d")

import os
os.chdir('/home/andreag/nocoscode/NOCOS-gitv1/usecases/landfastice_occurrence/testing')
import sys
sys.path.append(os.getcwd())
import matplotlib.pyplot as plt
plt.savefig('./plots/AVGfastice-'+str(fasticeduration)+'day_'+climateDTmodel+'_'+daterange+'.png', bbox_inches = 'tight')

chart.show()
