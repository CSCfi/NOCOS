"""Script to download ClimateDT data as forcing for iceberg drift simulations

download_ClimateDT-for-icebergdrift.py

Download variables like wind and ocean currents from ClimateDT and save them as
NetCDF files. After some processing, these files can later be used as input
to the iceberg drift model OpenDrift/OpenBerg (https://opendrift.github.io/)

Sections in this script:
    a) User settings
       The user can specify certain settings like the ClimateDT model, the time
       range, the output directory and the geographic area.
    b) List of parameters
       The user can comment-out parameters that are not needed for their case.
       As default, this scripts downloads the following:
       Wind (u and v), Sea ice (u, v, SIC, SIT) and Ocean (u, v, T, S)
    c) Download data from ClimateDT
       For each year in the requested range, this script downloads data for the
       requested days (defined by start date and number of days).
       A Polytope request is created based on user settings. Data is downloaded
       and NetCDF files for each year and for each parameter type (sfc, o2d, o3d)
       are saved into the directory specified in `datastoragedir`.


Example
-------

Activate the conda environment containing your polytope-examples code (see Notes).
Edit this script according to your user needs.
Execute the script::

    $ python download_ClimateDT-for-icebergdrift.py


Notes
-----

This script requires a valid DESP token. This can be created by running 
python3 ~/polytope_examples_GIT/desp-authentication.py
in a conda environment with Polytope installed
(https://github.com/destination-earth-digital-twins/polytope-examples)


Attributes
----------

List of parameters needed for the iceberg drift simulation and according ClimateDT parameters:

sea_water_salinity
  263500 	Time-mean sea water practical salinity (o3d)	avg_so  g kg**-1 ICON/IFS-NEMO/IFS-FESOM

sea_water_temperature
  263501 Time-mean sea water potential temperature (o3d)	avg_thetao K    ICON/IFS-NEMO/IFS-FESOM

x_sea_water_velocity
  263506 Time-mean eastward sea water velocity(o3d)	    avg_uoe m s**-1 ICON/IFS-NEMO/IFS-FESOM

y_sea_water_velocity
  263505 Time-mean northward sea water velocity(o3d)	    avg_von m s**-1 ICON/IFS-NEMO/IFS-FESOM

sea_ice_area_fraction
  263001 Time-mean sea ice area fraction	 (o2d)          avg_siconc Fraction ICON/IFS-NEMO/IFS-FESOM

sea_ice_thickness
  263000 Time-mean sea ice thickness	 (o2d)              avg_sithick m   	ICON/IFS-NEMO/IFS-FESOM

sea_ice_x_velocity
  263003 Time-mean eastward sea ice velocity	 (o2d)      avg_siue m s**-1    ICON/IFS-NEMO/IFS-FESOM

sea_ice_y_velocity
  263004 Time-mean northward sea ice velocity  (o2d)      avg_sivn m s**-1    ICON/IFS-NEMO/IFS-FESOM
  
x_wind
  165     10 metre U wind component (sfc)       10u m s**-1 	    ICON/IFS-NEMO/IFS-FESOM

y_wind
  166     10 metre V wind component (sfc)         10v m s**-1     ICON/IFS-NEMO/IFS-FESOM

Not yet implemented:
172	    Land-sea mask	             (sfc)     lsm	(0 - 1)    	IFS-NEMO/IFS-FESOM (Both models in Phase 2)



Author, copyright and license
-----------------------------

Author: Andrea Gierisch, DMI

Copyright 2025 CSC – IT Center for Science (CSC),
               Danish Meteorological Institute (DMI),
               Finnish Meteorological Institute (FMI),
               Norwegian Meteorological Institute (MetNo),
               Swedish Meteorological and Hydrological Institute (SMHI),
               Tallinn University of Technology (TalTech).

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

License: Apache-2.0



"""

import datetime
import pandas as pd


################
## User settings
################

## ClimateDT model (ICON or IFS-NEMO)
# climateDTmodel='IFS-NEMO'
climateDTmodel='ICON' # ICON does not have sos and tos in Phase 1

## Simulation period ( historical or SSP3-7.0 future scenario)
simulationperiod='historical'
#simulationperiod='future'

## Name of the region to be downloaded (Greenland, BaffinLabra, or CoburgLabra)
## 'subareas' are pre-defined in the request-function below
# mapregion='Greenland'
# mapregion='BaffinLabra'
mapregion='CoburgLabra'

## Time period to download, defined by start date and lenth of period.
## e.g. Download data between 14. August and 01. October
startmonth=8 # August
startday=14
numdays=49 # number of days to download

## Range of years to download (every year is saved into a separate file)
yearfirst=2010
yearlast=2020

## Directory to store data files
datastoragedir='/tmp/'

################
## End of user settings
################


# Download ClimateDT data for each year
######################################
for year in range(yearfirst,yearlast+1):
  print("Starting with year: "+str(year))

  # The start of the downloading period
  REQ_date_start=datetime.date(year,startmonth,startday) 
  # The end of downloading period
  REQ_date_end=REQ_date_start+pd.DateOffset(days=numdays-1)# Add numdays-1 days to the start day 
  # The download request string for the dates
  REQ_daterange= REQ_date_start.strftime("%Y%m%d")+"/to/"+REQ_date_end.strftime("%Y%m%d")

  print("Going to download data from "+  REQ_date_start.strftime("%Y%m%d") + " to "+REQ_date_end.strftime("%Y%m%d"))

  # Warn if download periods are likely not available
  if simulationperiod=='historical':
      # ICON (resolution=high) starts "1991-03-01" ends 2019-12-31
      if climateDTmodel=='ICON' and not(year in range (1991,2020)):
          raise RuntimeWarning("Historical data for ICON is currently only available between 1991-03-01 and 2019-12-31")
      # IFS-NEMO (resolution=standard) starts "1990-01-01" ends "2002-02-28"
      if climateDTmodel=='IFS-NEMO' and not(year in range (1990,2003)):
          raise RuntimeWarning("Historical data for IFS-NEMO is currently only available between 1990-01-01 and 2002-02-28 and in standard resolution!")
  elif simulationperiod=='future':
      # ICON ("resolution": "high") starts "2020-09-01" ends "2039-12-31"
      if climateDTmodel=='ICON' and not(year in range (2020,2040)):
          raise RuntimeWarning("Future data for ICON is currently only available between 2020-09-01 and 2039-12-31")
      # IFS-NEMO ("resolution": "high") starts "2020-01-01" ends on "2039-12-31"
      if climateDTmodel=='IFS-NEMO' and not(year in range (2020,2040)):
          raise RuntimeWarning("Future data for IFS-NEMO is currently only available between 2020-01-01 and 2039-12-31")


  # Set activity and experiment according to user input
  if simulationperiod=='historical':
      REQ_activity="CMIP6"
      REQ_experiment="hist"
  elif simulationperiod=='future':
      REQ_activity="ScenarioMIP"
      REQ_experiment="SSP3-7.0"

  # Parameters to download: 
  #########################
  varlist={}
  varlist['sfc']=""
  varlist['o2d']=""
  varlist['o3d']=""

  ## sfc (Wind)
  #  10u m s**-1 	 
  varlist['sfc']+="165/"
  # 10v m s**-1  
  varlist['sfc']+="166/"
  # #	  lsm	(0 - 1)    	IFS-NEMO/IFS-FESOM (Both models in Phase 2)
  # varlist['sfc']+="172/" # Not for ICON!

  ## o2d (Sea ice)
  # avg_siconc  
  varlist['o2d']+="263001/"
  # avg_sithick   
  varlist['o2d']+="263000/"
  # avg_siue m s**-1  
  varlist['o2d']+="263003/"
  # avg_sivn m s**-1  
  varlist['o2d']+="263004/"
  ### 2D ocean temp and salt. Not used
  ## # Parameters: avg_sos # o2d, no ICON
  ## varlist+="263100"
  ## # Parameters: avg_tos  # o2d, no ICON
  ## varlist+="263101/"

  ## o3d (Ocean)
  # avg_uoe
  varlist['o3d']+="263506/" #Needs o3d !!!
  # # # Parameters: avg_von
  varlist['o3d']+="263505/" #Needs o3d !!!
  # avg_so
  varlist['o3d']+="263500/" # o3d
  # avg_thetao
  varlist['o3d']+="263501/" #(o3d)	 

  # Make a list of all requested parameters
  REQ_vars={}
  for levtype in varlist.keys():
    REQ_vars[levtype]=varlist[levtype][:-1] # Remove last slash
  print(REQ_vars)
  # e.g.: REQ_vars="263100/263101/263506/263505"


  # The request function
  ######################
  def request_icebergforcing(activity,experiment,levtype,model,date,subarea,param,datadir=None):
      import earthkit.data
      # Set pre-defined download areas
      if subarea in ["Greenland","greenland"]:
          area='85/-80/67/5'
      elif subarea in ["BaffinLabra","baffinlabra"]:
          area='78.1/-73.9/56.9/-47.5' # e.g. '85/-80/67/5' # maxLAT, minLON, minLAT, maxLON
      elif subarea in ["CoburgLabra","coburglabra"]:
          area='78.1/-80.7/56.0/-47.5' # e.g. '85/-80/67/5' # maxLAT, minLON, minLAT, maxLON
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
              'grid' : 'O2560', #'F2000', #'O2560', # currently O, F, N grids are supported (maybe also H?)
              'area' : area # e.g. '85/-80/67/5' # maxLAT, minLON, minLAT, maxLON
          }
      if levtype=='sfc':
        request["time"]="0000/to/2300" # For historical ICON there is only 6-hourly data. But doesn't hurt to request everything.
      elif levtype=='o2d':
        request["time"]="0000"
      elif levtype=='o3d':
        request["levelist"]= "1" #"1/to/2" # Only download surface currents because ClimateDT currently does not provide info on the depth of each level.
        request["time"]= "0000"
  
      print(request)
      dataICE = earthkit.data.from_source("polytope", "destination-earth", request, 
                      address="polytope.lumi.apps.dte.destination-earth.eu", stream=False)
      return(dataICE)

  # Retrieve and save data 
  ########################
  datarawdict={}
  # for REQ_levtype in ["sfc", "o2d", "o3d"]: 
  # Loop through all levtypes for which we have requested at least 1 variable, i.e. REQ_vars[x] in not None
  for REQ_levtype in  [x for x in REQ_vars.keys() if REQ_vars[x]]:
    datarawdict[REQ_levtype]=request_icebergforcing(activity=REQ_activity,experiment=REQ_experiment,levtype=REQ_levtype,model=climateDTmodel,
                                  date=REQ_daterange,subarea=mapregion, param=REQ_vars[REQ_levtype],)
    # Save as netcdf
    datarawdict[REQ_levtype].to_xarray().earthkit.to_netcdf(datastoragedir+'/icebergforcing_'+mapregion+'_'+climateDTmodel+'_'+REQ_date_start.strftime("%Y%m%d") + "-"+REQ_date_end.strftime("%Y%m%d")+'_'+REQ_levtype+'_healpix.nc')


