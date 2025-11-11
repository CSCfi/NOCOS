#! /usr/bin/env python
"""Script to calculate monthly climatologies of marginal ice zones from ClimateDT simulations.

This module demonstrates documentation as specified by the `NumPy
Documentation HOWTO`_. Docstrings may extend over multiple lines. Sections
are created with a section header followed by an underline of equal length.

Notes
-----
    
    This script requires a valid DESP token. This can be created by running 
    python3 desp-authentication.py
    in a conda environment with Polytope installed
    (https://github.com/destination-earth-digital-twins/polytope-examples)
      

Available ClimateDT data (until 12.2025)
----------------------------------------
    1) Future projection
    #####################
    #ScenarioMIP/SSP3-7.0 ICON ("resolution": "high") starts on "2020-09-01"
    #ScenarioMIP/SSP3-7.0 ICON ("resolution": "high") ends on "2039-12-31"
    #ScenarioMIP/SSP3-7.0 IFS-NEMO ("resolution": "high") starts on "2020-01-01"
    #ScenarioMIP/SSP3-7.0 IFS-NEMO ("resolution": "high") ends on "2039-12-31"
    # Example:
    # dataICE=request_icedata_subarea(activity="ScenarioMIP",experiment="SSP3-7.0",
              model=climateDTmodel,date=REQ_daterange,param="263001/263003/263004")
    
    2) Historical
    ##################
    ##CMIP6/hist  ICON (resolution=high) starts "1991-03-01"
    ##CMIP6/hist  ICON (resolution=high) ends 2019-12-31
    ##CMIP6/hist IFS-NEMO (resolution=standard) starts "1990-01-01"
    ##CMIP6/hist IFS-NEMO (resolution=standard) ends "2002-02-28"
    # Example:
    #  dataICE=request_icedata_subarea(activity="CMIP6",experiment="hist",model=climateDTmodel,
               date=REQ_daterange,subarea="greenland", param="263001/263003/263004",
               datadir=datastoragedir)

    3) Storyline
    #################
    ##story-nudging/{cont|hist|Tplus2.0K} IFS-FESOM (resolution=standard) starts "2017-01-01"
    ##story-nudging/{cont|hist|Tplus2.0K} IFS-FESOM (resolution=high) starts "2017-03-01"
    ##story-nudging/{cont|hist|Tplus2.0K} IFS-FESOM (resolution={standard|high}) ends  "2024-10-31",
    ## cont: Control-1950, hist: Present day, Tplus2.0K: 2K warmer than pre-industrial, about 2040
    # Example:
    # dataICE=request_icedata_subarea(activity="story-nudging",experiment=REQexperiment,
              model=climateDTmodel,date=REQ_daterange,subarea="greenland", 
              param="263001/263003/263004",datadir=datastoragedir)


.. _NumPy docstring standard:
   https://numpydoc.readthedocs.io/en/latest/format.html#docstring-standard

"""
#=====================================================================
import os
import numpy as np
import earthkit.data
import earthkit.plots
import earthkit.regrid
from datetime import datetime, timedelta

from read_config import read_configfile
from utils.calculate_MIZ import calc_MIZ
from utils.download_icedata import request_icedata_subarea


#=====================================================================
# User settings
#=====================================================================

dataSource = 'ClimateDT'

# Read config file
configs = read_configfile(dataSource)

# Directory to store data files (temporarily):
user = os.environ.get('USER')
data_dir = '/nobackup/forsk/' + user + '/data/ClimateDT/' 

# Region to be processed (Greenland or Arctic)
mapregion = configs['selectdata']['domain']

# set years for the dataset
year_start = int(configs['selectdata']['year_start'])
year_end   = int(configs['selectdata']['year_end'])

if year_end <= 2019:
   simulationPeriod = 'historical'
   REQactivity="CMIP6"
   REQexperiment="hist"
elif year_start >= 2020:
   simulationPeriod = 'future'
   REQactivity="ScenarioMIP"
   REQexperiment="SSP3-7.0"
  

#=====================================================================
for climateDTmodel in configs['selectdata']['datasets']:
    for year in range(year_start,year_end+1):
        for month in range(1,13):
            print()
    
            # The start of the month
            date_start = datetime(year,month,1).strftime("%Y%m%d") 
            if month == 12:
               date_end = datetime(year,month,31).strftime("%Y%m%d") 
            else:
               date_end = (datetime(year,month+1,1) - timedelta(days=1)).strftime("%Y%m%d")
    
            # The download request string for the dates
            REQ_daterange= date_start + "/to/" + date_end
            print("Downloading data from "+ date_start + " to " + date_end)
    
            # Warn if download periods are likely not available
            if simulationPeriod=='historical':
               # ICON (resolution=high) starts "1991-03-01" ends 2019-12-31
               if climateDTmodel=='ICON' and not(year in range (1991,2020)):
                  raise RuntimeWarning("ICON historical data currently only available from 1991-03-01 to 2019-12-31")
               # IFS-NEMO (resolution=standard) starts "1990-01-01" ends "2002-02-28"
               if climateDTmodel=='IFS-NEMO' and not(year in range (1990,2003)):
                  raise RuntimeWarning("IFS-NEMO Historical data currently only available from 1990-01-01 to 2002-02-28 and in standard resolution!")
            elif simulationPeriod=='future':
               # ICON ("resolution": "high") starts "2020-09-01" ends "2039-12-31"
               if climateDTmodel=='ICON' and not(year in range (2020,2040)):
                  raise RuntimeWarning("ICOIN future data currently only available from 2020-09-01 to 2039-12-31")
               # IFS-NEMO ("resolution": "high") starts "2020-01-01" ends on "2039-12-31"
               if climateDTmodel=='IFS-NEMO' and not(year in range (2020,2040)):
                 raise RuntimeWarning("IFS-NEMO Future data for IFS-NEMO currently only available between 2020-01-01 and 2039-12-31")


            # Retrieve data (SIC, sea ice velocity u, sea ice velocity v)
            try:
               datastoragedir = os.path.join(data_dir,climateDTmodel+'_'+simulationPeriod)
               
               if not os.path.exists(datastoragedir): os.makedirs(datastoragedir)

               dataICE1month = request_icedata_subarea(activity=REQactivity,experiment=REQexperiment,
                               model=climateDTmodel, date=REQ_daterange,subarea=mapregion, 
                               param="263001/263000", datadir=datastoragedir)

               # After read in:
               dataICExr = dataICE1month.to_xarray() # Needed for date in plot title
               #print(dataICExr)

               data_monthly = dataICExr.mean(dim='forecast_reference_time')

               fname = datastoragedir + '/' + climateDTmodel + '_monthly_mean_' + str(year*100 + month) + '.nc'
               data_monthly.to_netcdf(fname)

            except:
               print('data unavailable for ' + str(year*100 + month))


