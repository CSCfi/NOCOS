"""Script to....from ClimateDT simulations.

This module demonstrates documentation as specified by the `NumPy
Documentation HOWTO`_. Docstrings may extend over multiple lines. Sections
are created with a section header followed by an underline of equal length.

Output is saved into subdirectory "images"

Example
-------
Examples can be given using either the ``Example`` or ``Examples``
sections. Sections support any reStructuredText formatting, including
literal blocks::

    $ python example_numpy.py


Section breaks are created with two blank lines. Section breaks are also
implicitly created anytime a new section starts. Section bodies *may* be
indented:

Notes
-----
    
    This script requires a valid DESP token. This can be created by running 
    python3 ~/polytope_examples_GIT/desp-authentication.py
    in a conda environment with Polytope installed
    (https://github.com/destination-earth-digital-twins/polytope-examples)
    

If a section is indented, then a section break is created by
resuming unindented text.

Attributes
----------
module_level_variable1 : int
    Module level variables may be documented in either the ``Attributes``
    section of the module docstring, or in an inline docstring immediately
    following the variable.

    Either form is acceptable, but the two should not be mixed. Choose
    one convention to document module level variables and be consistent
    with it.


.. _NumPy docstring standard:
   https://numpydoc.readthedocs.io/en/latest/format.html#docstring-standard

  sea_water_salinity
263100  Time-mean sea surface practical salinity (o2d)  avg_sos g kg**-1 IFS-NEMO/IFS-FESOM (all models in Phase2)
263500 	Time-mean sea water practical salinity (o3d)	avg_so  g kg**-1 ICON/IFS-NEMO/IFS-FESOM
  sea_water_temperature
263101 Time-mean sea surface temperature (o2d)          avg_tos    K   	IFS-NEMO/IFS-FESOM (all models in Phase2)
263501 Time-mean sea water potential temperature (o3d)	avg_thetao K    ICON/IFS-NEMO/IFS-FESOM
  x_sea_water_velocity
263506 Time-mean eastward sea water velocity(o3d)	    avg_uoe m s**-1 ICON/IFS-NEMO/IFS-FESOM
  y_sea_water_velocity
263505 Time-mean northward sea water velocity(o3d)	    avg_von m s**-1 ICON/IFS-NEMO/IFS-FESOM


  sea_floor_depth_below_sea_level
  sea_ice_area_fraction
263001 Time-mean sea ice area fraction	 (o2d)          avg_siconc Fraction ICON/IFS-NEMO/IFS-FESOM
  sea_ice_thickness
263000 Time-mean sea ice thickness	 (o2d)              avg_sithick m   	ICON/IFS-NEMO/IFS-FESOM
  sea_ice_x_velocity
263003 Time-mean eastward sea ice velocity	 (o2d)      avg_siue m s**-1    ICON/IFS-NEMO/IFS-FESOM
  sea_ice_y_velocity
263004 Time-mean northward sea ice velocity  (o2d)      avg_sivn m s**-1    ICON/IFS-NEMO/IFS-FESOM
  sea_surface_wave_from_direction
  sea_surface_wave_significant_height
  sea_surface_wave_stokes_drift_x_velocity
  sea_surface_wave_stokes_drift_y_velocity
  sea_surface_x_slope
  sea_surface_y_slope
  x_wind
(228246 100 metre U wind component (level hl) 100u m s**-1 	    IFS-NEMO/IFS-FESOM)
165     10 metre U wind component (sfc)       10u m s**-1 	    ICON/IFS-NEMO/IFS-FESOM
  y_wind
(228247 100 metre V wind component (level hl)  100v m s**-1     IFS-NEMO/IFS-FESOM)
166     10 metre V wind component (sfc)         10v m s**-1     ICON/IFS-NEMO/IFS-FESOM

172	    Land-sea mask	             (sfc)     lsm	(0 - 1)    	IFS-NEMO/IFS-FESOM (Both models in Phase 2)



"""

import earthkit.data
import earthkit.plots
import earthkit.regrid
import datetime
import pandas as pd
import numpy as np

# from utils.download_icedata_c import request_icedata_subarea

################
## User settings
################

# ClimateDT model (ICON or IFS-NEMO)
# climateDTmodel='IFS-NEMO'
climateDTmodel='ICON' # ICON does not have sos and tos in Phase 1

# Simulation period ( historical or SSP3-7.0 future scenario)
simulationperiod='historical'
# simulationperiod='future'

# # For which month should the climatology be produced? (1-12)
# month=3
# # for month in [1,3,5,11]:

# # First and last year of the climatology to be produced
# # ICON-historical
# clima_fromyear=2010
# clima_toyear=2019
# # # ICON-future
# # clima_fromyear=2030
# # clima_toyear=2039


numdays=2 # number of days to download

# Region to be processed (Greenland or Arctic)
# mapregion='Greenland'
mapregion='BaffinLabra'

# Directory to store data files
datastoragedir='/media/volume/data_storage_andrea/icebergdriftforcing/'

################
## End of user settings
################

# Checking user input
######################
# if not(month in range(1,13)):
#     raise ValueError("MONTH must be between 1 and 12")
# if not(mapregion=='Greenland'):
#     raise NotImplementedError("Not implemented for mapregion: "+mapregion)

# Process ClimateDT data for each year
######################################

# fastice_forechyear=[] # Empty list to collect results for each year
# #for year in [2018]: # doesn't exist for hist???
# # for year in [2001]:
# # for year in range(2010,2020):
# for year in range(clima_fromyear,clima_toyear+1):

# print()
# print("Starting with year "+str(year))

# The start of the month
date_start=datetime.date(2001,7,1) 
# The start of the downloading period
REQ_date_start=date_start#-datetime.timedelta(days=fasticeduration-1) # For fasticeduration of 1 day we do not need to download "yesterday"
# The end of downloading period
REQ_date_end=date_start+pd.DateOffset(days=numdays-1)# Add numdays-1 days to the start day #-pd.DateOffset(days=1) # start + 1 month - 1 day -> 31.12.
# The download request string for the dates
REQ_daterange= REQ_date_start.strftime("%Y%m%d")+"/to/"+REQ_date_end.strftime("%Y%m%d")

# REQ_daterange="20010701"

print("Going to download data from "+  REQ_date_start.strftime("%Y%m%d") + " to "+REQ_date_end.strftime("%Y%m%d"))

# Future projection
#####################
#ScenarioMIP/SSP3-7.0 ICON ("resolution": "high") starts on "2020-09-01"
#ScenarioMIP/SSP3-7.0 ICON ("resolution": "high") ends on "2039-12-31"
#ScenarioMIP/SSP3-7.0 IFS-NEMO ("resolution": "high") starts on "2020-01-01"
#ScenarioMIP/SSP3-7.0 IFS-NEMO ("resolution": "high") ends on "2039-12-31"
# Example:
# dataICE=request_icedata_subarea(activity="ScenarioMIP",experiment="SSP3-7.0",model=climateDTmodel,date=REQ_daterange,
                            # param="263001/263003/263004")

# Historical
##################
##CMIP6/hist  ICON (resolution=high) starts "1991-03-01"
##CMIP6/hist  ICON (resolution=high) ends 2019-12-31
##CMIP6/hist IFS-NEMO (resolution=standard) starts "1990-01-01"
##CMIP6/hist IFS-NEMO (resolution=standard) ends "2002-02-28"
# Example:
# dataICE=request_icedata_subarea(activity="CMIP6",experiment="hist",model=climateDTmodel,date=REQ_daterange,
#                             subarea="greenland", param="263001/263003/263004",
#                             datadir=datastoragedir)

# Storyline
#################
##story-nudging/{cont|hist|Tplus2.0K} IFS-FESOM (resolution=standard) starts "2017-01-01"
##story-nudging/{cont|hist|Tplus2.0K} IFS-FESOM (resolution=high) starts "2017-03-01"
##story-nudging/{cont|hist|Tplus2.0K} IFS-FESOM (resolution={standard|high}) ends  "2024-10-31",
## cont: Control-1950, hist: Present day, Tplus2.0K: 2K warmer than pre-industrial, about 2040
# Example:
# dataICE=request_icedata_subarea(activity="story-nudging",experiment=REQexperiment,model=climateDTmodel,date=REQ_daterange,
#                             subarea="greenland", param="263001/263003/263004",
#                             datadir=datastoragedir)

# # Warn if download periods are likely not available
# if simulationperiod=='historical':
#     # ICON (resolution=high) starts "1991-03-01" ends 2019-12-31
#     if climateDTmodel=='ICON' and not(year in range (1991,2020)):
#         raise RuntimeWarning("Historical data for ICON is currently only available between 1991-03-01 and 2019-12-31")
#     # IFS-NEMO (resolution=standard) starts "1990-01-01" ends "2002-02-28"
#     if climateDTmodel=='IFS-NEMO' and not(year in range (1990,2003)):
#         raise RuntimeWarning("Historical data for IFS-NEMO is currently only available between 1990-01-01 and 2002-02-28 and in standard resolution!")
# elif simulationperiod=='future':
#     # ICON ("resolution": "high") starts "2020-09-01" ends "2039-12-31"
#     if climateDTmodel=='ICON' and not(year in range (2020,2040)):
#         raise RuntimeWarning("Future data for ICON is currently only available between 2020-09-01 and 2039-12-31")
#     # IFS-NEMO ("resolution": "high") starts "2020-01-01" ends on "2039-12-31"
#     if climateDTmodel=='IFS-NEMO' and not(year in range (2020,2040)):
#         raise RuntimeWarning("Future data for IFS-NEMO is currently only available between 2020-01-01 and 2039-12-31")


# Set activity and experiment according to user input
if simulationperiod=='historical':
    REQ_activity="CMIP6"
    REQ_experiment="hist"
elif simulationperiod=='future':
    REQ_activity="ScenarioMIP"
    REQ_experiment="SSP3-7.0"

# Parameters to download: 
varlist={}
varlist['sfc']=""
varlist['o2d']=""
varlist['o3d']=""


## sfc
#  10u m s**-1 	 
varlist['sfc']+="165/"
# 10v m s**-1  
varlist['sfc']+="166/"
# #	  lsm	(0 - 1)    	IFS-NEMO/IFS-FESOM (Both models in Phase 2)
# varlist['sfc']+="172/" # Not for ICON!

## o2d
# avg_siconc  
varlist['o2d']+="263001/"
# avg_sithick   
varlist['o2d']+="263000/"
# avg_siue m s**-1  
varlist['o2d']+="263003/"
# avg_sivn m s**-1  
varlist['o2d']+="263004/"

## o3d
# avg_uoe
varlist['o3d']+="263506/" #Needs o3d !!!
# # # Parameters: avg_von
varlist['o3d']+="263505/" #Needs o3d !!!
# avg_so
varlist['o3d']+="263500/" # o3d
# avg_thetao
varlist['o3d']+="263501/" #(o3d)	 

### 2D ocean temp and salt. Not used
## # Parameters: avg_sos # o2d, no ICON
## varlist+="263100"
## # Parameters: avg_tos  # o2d, no ICON
## varlist+="263101/"

REQ_vars={}
for levtype in varlist.keys():
  REQ_vars[levtype]=varlist[levtype][:-1] # Remove last slash
print(REQ_vars)
# REQ_vars="263100/263101/263506/263505"



def request_icebergforcing(activity,experiment,levtype,model,date,subarea,param,datadir=None):
    # Set pre-defined download areas
    import earthkit.data
    if subarea in ["Greenland","greenland"]:
        area='85/-80/67/5'
    elif subarea in ["BaffinLabra","baffinlabra"]:
        area='78.1/-73.9/56.9/-47.5' # e.g. '85/-80/67/5' # maxLAT, minLON, minLAT, maxLON
    else:
        raise RuntimeError("Unknown subarea: "+ subarea+". Cannot create request.")

    request = {
            "activity": activity,
            "class": "d1",
            "dataset": "climate-dt",
            "date": date,
            "experiment": experiment,
            "expver": "0001",
            "generation": "1",
            "levtype": levtype,
            # "levelist": "1", #"1/to/2", # only used for o3d
            "model": model,
            "param": param,
            "realization": "1",
            "resolution": "high",
            "stream": "clte",
            # "time": "0000", # depends on atm or ocean model (sfc or o2d/o3d)
            "type": "fc",
            'grid' : 'O2560', # currently O, F, N grids are supported (maybe also H?)
            #does not work'grid' : [0.1, 0.1],
            #does not work'grid': "eORCA025_T",
            'area' : area # e.g. '85/-80/67/5' # maxLAT, minLON, minLAT, maxLON
        }
    if levtype=='sfc':
       request["time"]="0000/to/2300" # For historical ICON there is only 6-hourly data. But doesn't hurt to request everything.
    elif levtype=='o2d':
       request["time"]="0000"
    elif levtype=='o3d':
      request["levelist"]= "1" #"1/to/2"
      request["time"]= "0000"
 
    print(request)
    dataICE = earthkit.data.from_source("polytope", "destination-earth", request, 
										address="polytope.lumi.apps.dte.destination-earth.eu", stream=False)
    return(dataICE)

# Retrieve data 
datarawdict={}
# for REQ_levtype in ["sfc", "o2d", "o3d"]: 
# Loop through all levtypes for which we have requested at least 1 variable, i.e. REQ_vars[x] in not None
for REQ_levtype in  [x for x in REQ_vars.keys() if REQ_vars[x]]:
   datarawdict[REQ_levtype]=request_icebergforcing(activity=REQ_activity,experiment=REQ_experiment,levtype=REQ_levtype,model=climateDTmodel,
                                date=REQ_daterange,subarea=mapregion, param=REQ_vars[REQ_levtype],)
                                # datadir=datastoragedir)
   # Save as netcdf
   datarawdict[REQ_levtype].to_xarray().earthkit.to_netcdf(datastoragedir+'/icebergforcing_'+mapregion+'_'+climateDTmodel+'_'+REQ_date_start.strftime("%Y%m%d") + "-"+REQ_date_end.strftime("%Y%m%d")+'_'+REQ_levtype+'_healpix.nc')


