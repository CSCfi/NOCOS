
## Plotting fastice for multiple days

# This script requires a valid DESP token. This can be created by running 
# python3 ~/polytope_examples_GIT/desp-authentication.py
# in the conda env polytope2025May


import earthkit.data
import earthkit.plots
import earthkit.regrid
import datetime

# Load user configurations from file
from read_config import read_configfile
configs=read_configfile('config_LFI_calc_REF.yml')

fasticeduration=configs['LFI']['fasticeduration'] # days
date_start=configs['LFI']['startdate']
date_end=configs['LFI']['enddate']
climateDTmodel=configs['climateDT']['model'] # "IFS-NEMO" or "ICON"

# Process user input
REQ_date_start=date_start-datetime.timedelta(days=fasticeduration-1) # For fasticeduration of 1 day we do not need to download "yesterday"
REQ_date_end=date_end
REQ_daterange= REQ_date_start.strftime("%Y%m%d")+"/to/"+REQ_date_end.strftime("%Y%m%d")



# request and download ice data
from download_icedata import request_icedata_polygon, request_icedata, request_icedata_boundingbox



#dataICE=request_icedata(activity="ScenarioMIP",experiment="SSP3-7.0",model=climateDTmodel,date=REQ_daterange,param="263001/263003/263004")
#dataICE=request_icedata_polygon(activity="ScenarioMIP",experiment="SSP3-7.0",model=climateDTmodel,date=REQ_daterange,param="263001/263003/263004")
dataICEbb=request_icedata_boundingbox(activity="ScenarioMIP",experiment="SSP3-7.0",model=climateDTmodel,date=REQ_daterange,param="263001/263003/263004")



# dataICE.ls()
dataICExr=dataICEbb.to_xarray()



# dataICExr.latitude.data


# ## List metatdata keys
# #[key for key in dataICE[0].metadata().keys()]

# ## Other potentially interesting commands:

# # Convert to xarray:
# #dataICE_XR_healpix=dataICE.to_xarray(engine="cfgrib")

# # Access units
# #dataICE[0].metadata()['units']



# #### Extract data from grib object



# siconc=dataICE[0::3].values
# siu=dataICE[1::3].values
# siv=dataICE[2::3].values


# #siconc=dataICE[0]
# #siu=dataICE[1]
# #siv=dataICE[2]


# siu



# #### Calculate drift speed



# import numpy as np
# #speed=np.sqrt(siu.values**2+siv.values**2)
# speed=np.sqrt(siu**2+siv**2)
# speed



# #### Calculate areas covered by fast ice"



# canvaswithland=speed.copy()
# fasticemask=np.logical_and(np.less(speed,5e-4),np.greater(siconc,0.90))
# landmask=np.isnan(canvaswithland)
# watermask=np.logical_and(np.logical_not(landmask),np.logical_not(fasticemask))
# canvaswithland[watermask]=0.
# canvaswithland[fasticemask]=1. # Number of time stamps: user defined date range + fasticeduration


# def fastice_for_x_days(fasticeN,daysN):
#     # fasticeN shape [days,healpixcells]
#     if daysN==1:
#         return fasticeN
#     else:
#         fasticeNm1=np.logical_and(fasticeN[0:-1,:],fasticeN[1:,:]) # Has there been fastice today and yesterday?
#         daysNm1=daysN - 1
#         return fastice_for_x_days(fasticeNm1,daysNm1) # Call again for one day less


# fasticedata=fastice_for_x_days(canvaswithland,fasticeduration) # Number of time stamps: user defined date range\n"



### Make plot for a specific day



# The field to plot
plottimestamp=3
fasticetoplot=dataICExr.avg_siconc[0,0,0,:]
# print(fasticetoplot.ls())




from earthkit.plots.geo import domains
import earthkit.data
import earthkit.plots
import numpy as np


import cartopy.crs as ccrs
crs = ccrs.NorthPolarStereo(central_longitude=10)


arctic_domain = domains.Domain(
    [-2800000, 2800000, -2800000, 2800000],
    crs=ccrs.NorthPolarStereo(),
    name="Arctic",
)


chart = earthkit.plots.Map(domain=arctic_domain)
#chart = earthkit.plots.Map(domain=[-75,-60,75,80])
#chart = earthkit.plots.Map(domain=[20,25,59,60.5]) #Baltic
#chart = earthkit.plots.Map(domain="France")




#chart.block(dataICE[0], levels=np.arange(0, 1, 0.1), colors="Spectral_r")
# [0]: siconc, timestep 1
# [1]: siue, timestep 1
# [2]: sivn, timestep 1
# [3]: siconc, timestep 2
# [4]: siue, timestep 2
# [5]: sivn, timestep 2
#chart.block(speed, levels=np.arange(0, 0.2,0.01), colors="jet",units="m/s")
chart.block(fasticetoplot, x='y', y='x',levels=np.arange(0, 1, 0.1), colors="winter")




#chart.land()
chart.coastlines()
chart.gridlines()
chart.legend() #ANG This is the colorbar


# plotdate=fasticetoplot.datetimes.strftime("%Y-%m-%d")
plotdate=fasticetoplot.datetimes.values.item()[0:10]
chart.title(str(fasticeduration)+"-day fastice persistence on "+ plotdate +", "+climateDTmodel)
# import matplotlib.pyplot as plt
# #plt.savefig('fastice-'+str(fasticeduration)+'day_'+climateDTmodel+'_'+plotdate+'.png', bbox_inches = 'tight')
# chart.show()



# ### Plot average fast ice coverage


# # The field to plot
# endtimestamp=canvaswithland.shape[0]-fasticeduration
# mean_fasticecover=np.mean(canvaswithland[:,:],axis=0) # average over time -> percentage of fast ice coverage
# fasticetoplot=dataICE[((fasticeduration-1)+endtimestamp)*3].clone(values=mean_fasticecover, name="Avg. fast ice coverage", shortName="fastice", units="") # Check metadata with e.g.: fastice.metadata("name")
# print(fasticetoplot.ls())


# from earthkit.plots.geo import domains
# import earthkit.data
# import earthkit.plots
# import numpy as np


# import cartopy.crs as ccrs
# crs = ccrs.NorthPolarStereo(central_longitude=10)


# arctic_domain = domains.Domain(
#     [-2800000, 2800000, -2800000, 2800000],
#     crs=ccrs.NorthPolarStereo(),
#     name="Arctic",
# )


# chart = earthkit.plots.Map(domain=arctic_domain)
# #chart = earthkit.plots.Map(domain=[-75,-60,75,80])
# #chart = earthkit.plots.Map(domain=[20,25,59,60.5]) #Baltic
# #chart = earthkit.plots.Map(domain="France")




# #chart.block(dataICE[0], levels=np.arange(0, 1, 0.1), colors="Spectral_r")
# # [0]: siconc, timestep 1
# # [1]: siue, timestep 1
# # [2]: sivn, timestep 1
# # [3]: siconc, timestep 2
# # [4]: siue, timestep 2
# # [5]: sivn, timestep 2
# #chart.block(speed, levels=np.arange(0, 0.2,0.01), colors="jet",units="m/s")
# #chart.block(fasticetoplot, levels=np.arange(0, 1, 0.1), colors="winter")
# chart.block(fasticetoplot, levels=np.arange(0, 1, 0.1), colors="jet")




# #chart.land()
# chart.coastlines()
# chart.gridlines()
# chart.legend() #ANG This is the colorbar


# plotdate=fasticetoplot.datetime()['base_time'].strftime("%Y-%m-%d")
# chart.title("Average "+str(fasticeduration)+"-day fastice occurrence\n between "+ date_start.strftime("%Y-%m-%d") +" and " + date_end.strftime("%Y-%m-%d")  +", "+climateDTmodel)
# import matplotlib.pyplot as plt
# chart.save('AVGfastice-'+str(fasticeduration)+'day_'+climateDTmodel+'_'+plotdate+'.png', bbox_inches = 'tight')
# chart.show()
# #plt.savefig('AVGfastice-'+str(fasticeduration)+'day_'+climateDTmodel+'_'+plotdate+'.png', bbox_inches = 'tight')


