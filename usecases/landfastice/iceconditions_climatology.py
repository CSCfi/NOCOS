"""Script to calculate monthly climatologies of ice parameters from ClimateDT simulations.

iceconditions_climatology.py

Sections in this script:
    a) User settings
       The user choose ice parameters and specify certain settings like the
       ClimateDT model, the time range, and output directories.
    b) Download data from ClimateDT
       A request is created based on user settings. Data is downloaded and saved
       into the directory given in `datastoragedir`. Next time the same data is
       requested, the script will use the saved data instead of downloading them
       again.
    c) Calculate climatologies
       This part also calculates the ice drift speed from u and v components.
    d) Plot the ice climatology
       The  user can choose between three pre-defined regions (Arctic-wide,
       Greenland, and Inglefield Bredning).
       Output is saved into the directory given in `plotdir`.


Example
-------

Activate the conda environment containing your polytope-examples code (see Notes).
Edit this script according to your user needs.
Execute the script::

    $ python iceconditions_climatology.py


Notes
-----

This script requires a valid DESP token. This can be created by running 
python3 ~/polytope_examples_GIT/desp-authentication.py
in a conda environment with Polytope installed
(https://github.com/destination-earth-digital-twins/polytope-examples)


Attributes
----------

See explanation of user settings in the first part of the script. For some
variables, the user can comment-in and comment-out the different options.


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

import earthkit.data
import earthkit.plots
import earthkit.regrid
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import xarray as xr

from utils.download_icedata_c import request_icedata_subarea

################
## User settings
################

## Toggle reading, plotting and saving of plots
readin=True
plotmap=True
saveplot=True

## Ice parameters to plot
plotSIC=True
plotSIT=False
plotSNOW=False
plotICEDRIFT=False

## Ice parameters to download
paramSIC=True
paramSIT=True
paramSNOW=True
paramICEDRIFT=True

## ClimateDT model (ICON or IFS-NEMO)
# climateDTmodel='IFS-NEMO'
climateDTmodel='ICON'

## Simulation period ( historical or SSP3-7.0 future scenario)
simulationperiod='historical'
# simulationperiod='future'

## For which month should the climatology be produced? (1-12)
month=3

## First and last year of the climatology to be produced
clima_fromyear=2010 # ICON-historical
clima_toyear=2019   # ICON-historical
# clima_fromyear=1990 # IFS-NEMO historical
# clima_toyear=1999   # IFS-NEMO historical
# clima_fromyear=2030 # ICON/IFS-future
# clima_toyear=2039   # ICON/IFS-future


## Region to be processed (Greenland or Arctic or Inglefield)
mapregion='Greenland'
# mapregion='Arctic'
# mapregion='Inglefield' # This will download/use data for Greenland

## Directory to store downloaded data files (temporarily):
datastoragedir='/media/volume/data_storage_andrea/'

## Directory to save plots:
plotdir='./images/iceparameters/'

## Font size for the plot
plotfontsize=16

################
## End of user settings
################

# Checking user input
######################
if not(month in range(1,13)):
    raise ValueError("MONTH must be between 1 and 12")
if mapregion not in ('Greenland', 'Arctic','Inglefield'):
    raise NotImplementedError("Not implemented for mapregion: "+mapregion)

# Prepare list of ice parameters to download, scalar separately from u/v
################################
# We need SIC for icedrift:
if paramICEDRIFT==True: paramSIC=True

iceparamsscalar=[]
if paramSIT: iceparamsscalar.append('SIT')
if paramSIC: iceparamsscalar.append('SIC')
if paramSNOW: iceparamsscalar.append('snowvolume')
# e.g. iceparamsscalar=['SIT','SIC','snowvolume'] # Keep the same order, otherwise the data will be downloaded again.

parammapping={'SIT':'263000','SIC':'263001','snowvolume':'263009','icedrift':'263003/263004'}
param_numbers_scalar=[parammapping[iceparam] for iceparam in iceparamsscalar]
REQparamscalar='/'.join(param_numbers_scalar)
REQparamvector=parammapping['icedrift']

# Prepare list of ice parameters to plot
################################
iceparamstoplot=[]
if plotSIT: iceparamstoplot.append('avg_sithick')
if plotSIC: iceparamstoplot.append('avg_siconc')
if plotSNOW: iceparamstoplot.append('avg_snvol')
if plotICEDRIFT: iceparamstoplot.append('avg_icespeed')
    

if readin:

    # Process ClimateDT data for each year
    ######################################

    icedata_forechyear=[] # Empty list to collect results for each year
    # for year in range(2010,2020):
    for year in range(clima_fromyear,clima_toyear+1):

        print()
        print("Starting with year "+str(year))
        
        # The start of the month
        date_start=datetime.date(year,month,1) 
        # The start of the downloading period
        REQ_date_start=date_start
        # The end of the month = end of downloading period
        REQ_date_end=date_start+pd.DateOffset(months=1)-pd.DateOffset(days=1) # start + 1 month - 1 day -> 31.12.
        # The download request string for the dates
        REQ_daterange= REQ_date_start.strftime("%Y%m%d")+"/to/"+REQ_date_end.strftime("%Y%m%d")
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
            REQactivity="CMIP6"
            REQexperiment="hist"
        elif simulationperiod=='future':
            REQactivity="ScenarioMIP"
            REQexperiment="SSP3-7.0"

        # Set download area
        if mapregion in ['Qaanaaq','Inglefield']:
            downloadregion='Greenland'
        else:
            downloadregion=mapregion


        # Retrieve scalar ice data (SIT, SIC, snow
        dataICEscalar_daily=request_icedata_subarea(activity=REQactivity,experiment=REQexperiment,model=climateDTmodel,
                                    date=REQ_daterange,subarea=downloadregion, param=REQparamscalar,
                                    datadir=datastoragedir)
        
        # Retrieve sea ice velocity u, sea ice velocity v)
        dataICEvector_daily=request_icedata_subarea(activity=REQactivity,experiment=REQexperiment,model=climateDTmodel,
                                        date=REQ_daterange,subarea=downloadregion, param=REQparamvector,
                                        datadir=datastoragedir)


        
        # Convert scalar variable grb object to xarray
        dataICEscalar_daily_xr=dataICEscalar_daily.to_xarray()

        # Calculate ice drift speed from vector grb file, mask data where SIC<5%, and add the "icedrift" variable to the scalar file.
        dataICEvector_daily_xr=dataICEvector_daily.to_xarray()
        speedarray=np.sqrt(dataICEvector_daily_xr['avg_siue'].data*dataICEvector_daily_xr['avg_siue'].data+dataICEvector_daily_xr['avg_sivn'].data*dataICEvector_daily_xr['avg_sivn'].data )
        speedarray[dataICEscalar_daily_xr['avg_siconc'].data<0.05]=np.nan
        speedtmp=dataICEvector_daily_xr['avg_siue'].copy(data=speedarray)
        speedtmp.attrs={"param": 'avg_icespeed', 'long_name': 'Time-mean sea ice drift speed', "paramID": '263003/263004'}
        dataICEscalar_daily_xr['avg_icespeed']=speedtmp

        # Calculate average for this month
        dataICEscalar_monthly=dataICEscalar_daily_xr.mean(dim='forecast_reference_time')

        # Save monthly values for this year
        icedata_forechyear.append(dataICEscalar_monthly)

    ###
    # End of year loop
    ####################

    # Combine object from each year into one file
    icedata=xr.concat(icedata_forechyear,dim='forecast_reference_time')
    # Calculate climatology by averaging the monthly values of all years
    icedata_climatology=icedata.mean(dim='forecast_reference_time')


#####################################
### Plotting ice climatologies
#####################################

if plotmap:
    from earthkit.plots.geo import domains
    import earthkit.data
    import earthkit.plots
    import numpy as np
    import cartopy.crs as ccrs

    crs = ccrs.NorthPolarStereo(central_longitude=10)
    arctic_domain = domains.Domain(
        [-2300000, 2300000, -2300000, 2300000],
        crs=ccrs.NorthPolarStereo(),
        name="Arctic",
    )
    greenland_domain = domains.Domain(
        [-1300000, 700000, -2200000, -600000], # W, E, S, N
        crs=ccrs.NorthPolarStereo(central_longitude=-35),
        name="Greenland",
    )
    qaanaaq_domain = domains.Domain(
        [-180000, 50000, -1490000, -1330000], # W, E, S, N
        crs=ccrs.NorthPolarStereo(central_longitude=-67),
        name="Qaanaaq",
    )
    
    plotstyle={'avg_sithick': earthkit.plots.styles.Style(levels=np.arange(0, 3.5, 0.25), colors="inferno", units="m", extend="both"), 
               'avg_siconc': earthkit.plots.styles.Style(levels=np.arange(0, 1, 0.1), colors="magma", units="fraction", extend="both"), 
               'avg_snvol': earthkit.plots.styles.Style(levels=np.arange(0, 0.8, 0.1), colors="cividis", units="m3/m2", extend="both"), 
               'avg_icespeed': earthkit.plots.styles.Style(levels=np.arange(0, 0.5, 0.05), colors="plasma", units="m/s", extend="both"), 
               }
    plotlabel={'avg_sithick': 'Sea ice thickness [m]',
               'avg_siconc': 'Sea ice concentration [fraction]',
               'avg_snvol': 'Snow volume per area [m]',
               'avg_icespeed': "Mean of daily ice drift speed [m/s]"
               }


    for icevar in iceparamstoplot:

        # The field to plot
        icetoplot=icedata_climatology[icevar]

        # Set up the map
        if mapregion in ["Greenland","greenland"]:
            chart = earthkit.plots.Map(domain=greenland_domain)
        elif mapregion in ["Arctic","arctic"]:
            chart = earthkit.plots.Map(domain=arctic_domain)
        elif mapregion in ["Qaanaaq","Inglefield"]:
            chart = earthkit.plots.Map(domain=qaanaaq_domain)

        # Plot the data
        chart.grid_cells(icetoplot,
                        style=plotstyle[icevar])

        chart.coastlines(resolution='high',zorder=3)
        chart.land(resolution='high',zorder=2)
        # chart.coastlines(resolution='medium',zorder=3)
        # chart.land(resolution='medium',zorder=2)

        plt.rcParams.update({'font.size': plotfontsize})

        if not mapregion=="Inglefield":
            chart.gridlines(zorder=4)
            chart.legend(label=plotlabel[icevar])

            # Long title
            # chart.title(" "Climatology for " + date_start.strftime("%B") +" "+str(clima_fromyear)+"-"+str(clima_toyear)+", "
                # +climateDTmodel+"-"+simulationperiod, fontsize=plotfontsize)
            # Short title
            chart.title("ClimateDT "+climateDTmodel+" ("+str(clima_fromyear)+"-"+str(clima_toyear)+") ",
                        fontsize=plotfontsize)

        if saveplot:
            import matplotlib.pyplot as plt
            if mapregion=="Inglefield":
                plt.savefig(plotdir+'/climatology-'+icevar[4:]+'_'+date_start.strftime("%B")+"_"+str(clima_fromyear)+"-"+str(clima_toyear)+"_"+climateDTmodel+"-"+simulationperiod+'_'+mapregion+'.png', bbox_inches = 'tight', facecolor='k')
            else:
                plt.savefig(plotdir+'/climatology-'+icevar[4:]+'_'+date_start.strftime("%B")+"_"+str(clima_fromyear)+"-"+str(clima_toyear)+"_"+climateDTmodel+"-"+simulationperiod+'_'+mapregion+'.png', bbox_inches = 'tight')

        chart.show()
