"""Script to calculate monthly climatologies of landfast ice coverage from ClimateDT simulations.

landfastice_climatology.py

Sections in this script:
    a) User settings
       The user can specify certain settings like the ClimateDT model, the time
       range, and output directories.
    b) Download data from ClimateDT
       A request is created based on user settings. Data is downloaded and saved
       into the directory given in `datastoragedir`. Next time the same data is
       requested, the script will use the saved data instead of downloading them
       again.
    c) Calculate landfast ice coverage
       Call to the function `avg_fasticecoverage`, which derives fast ice areas
       from ice drift speed and ice concentration.
    d) Plot landfast ice climatology
       The  user can choose between three pre-defined regions (Arctic-wide,
       Greenland, and Inglefield Bredning).
       Output is saved into the directory given in `plotdir`.


Example
-------

Activate the conda environment containing your polytope-examples code (see Notes).
Edit this script according to your user needs.
Execute the script::

    $ python landfastice_climatology.py


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

from utils.download_icedata_c import request_icedata_subarea
from utils.fastice import avg_fasticecoverage

################
## User settings
################

## Toggle plotting and saving of plots
plotting=True
saveplot=True

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

## For how many days does ice need to be stationary in order to be considered fastice?
## Default: 4 days
fasticeduration=4 # days; For how many days ice needs to be stationary to be considered fastice

## Region to be processed (Greenland or Arctic or Inglefield)
mapregion='Greenland'
# mapregion='Arctic'
# mapregion='Inglefield' # This will download/use data for Greenland

## Directory to store downloaded data files (temporarily):
datastoragedir='/media/volume/data_storage_andrea/'

## Directory to save plots:
plotdir='./images/'

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

# Process ClimateDT data for each year
######################################

fastice_forechyear=[] # Empty list to collect results for each year
for year in range(clima_fromyear,clima_toyear+1):

    print()
    print("Starting with year "+str(year))
    
    # The start of the month
    date_start=datetime.date(year,month,1) 
    # The start of the downloading period
    REQ_date_start=date_start-datetime.timedelta(days=fasticeduration-1) # For fasticeduration of 1 day we do not need to download "yesterday"
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

    # Retrieve data (SIC, sea ice velocity u, sea ice velocity v)
    dataICE1month=request_icedata_subarea(activity=REQactivity,experiment=REQexperiment,model=climateDTmodel,
                                    date=REQ_daterange,subarea=downloadregion, param="263001/263003/263004",
                                    datadir=datastoragedir)


    # Calculate average fastice coverage for this month
    avg_fasticecover_grb = avg_fasticecoverage(dataICE1month,speedthreshold=5e-4,fasticeduration=4)
    fastice_forechyear.append(avg_fasticecover_grb)

###
# End of year loop
####################


# Make climatology: Average over the monthly datasets of each year
fasticeclimatology_numpy=np.nanmean([grb.to_array() for grb in fastice_forechyear],axis=0)
# Put data into an empty/random grib object
fasticeclimatology=dataICE1month[0].clone(values=fasticeclimatology_numpy,
                                          dataDate=str(clima_fromyear)+"-"+str(clima_toyear),
                                          name="Avg. fast ice coverage", shortName="fastice", units="",
                                          stepRange='0') # Check metadata with e.g.: avg_fasticecover_grb.metadata("name")


#####################################
### Plotting fast ice climatology
#####################################

if plotting:
    from earthkit.plots.geo import domains
    import earthkit.data
    import earthkit.plots
    import numpy as np

    #### Plot domains
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


    # The field to plot
    fasticeOCCtoplot=fasticeclimatology
    print(fasticeOCCtoplot.ls())


    # Make the plot
    if mapregion in ["Greenland","greenland"]:
        chart = earthkit.plots.Map(domain=greenland_domain)
    elif mapregion in ["Arctic","arctic"]:
        chart = earthkit.plots.Map(domain=arctic_domain)
    elif mapregion in ["Qaanaaq","Inglefield"]:
        chart = earthkit.plots.Map(domain=qaanaaq_domain)
    
    chart.grid_cells(fasticeOCCtoplot,
                    style=earthkit.plots.styles.Style(colors="viridis", extend="both",
                                                    levels=[0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.]))
    #chart.grid_cells(fasticeOCCtoplot,interpolate=dict(method='nearest'),

    chart.coastlines(resolution='high',zorder=3)
    chart.land(resolution='high',zorder=2)
    # chart.coastlines(resolution='medium',zorder=3)
    # chart.land(resolution='medium',zorder=2)

    plt.rcParams.update({'font.size': plotfontsize})

    if not mapregion=="Inglefield":
        chart.gridlines(zorder=4)
        chart.legend(label="Average fast ice coverage [fraction]")

        # Long title
        # chart.title("Average "+str(fasticeduration)+"-day fastice occurrence\n " +
            # "Climatology for " + date_start.strftime("%B") +" "+str(clima_fromyear)+"-"+str(clima_toyear)+", "
            # +climateDTmodel+"-"+simulationperiod, fontsize=plotfontsize)
        # Short title
        chart.title("ClimateDT "+climateDTmodel+" ("+str(clima_fromyear)+"-"+str(clima_toyear)+") ",
                    fontsize=plotfontsize)

    if saveplot:
        import matplotlib.pyplot as plt
        if mapregion=="Inglefield":
            plt.savefig(plotdir+'/fasticeclimatology_'+date_start.strftime("%B")+"_"+str(clima_fromyear)+"-"+str(clima_toyear)+"_"+climateDTmodel+"-"+simulationperiod+'_'+mapregion+'.png', bbox_inches = 'tight', facecolor='k')
        else:
            plt.savefig(plotdir+'/fasticeclimatology_'+date_start.strftime("%B")+"_"+str(clima_fromyear)+"-"+str(clima_toyear)+"_"+climateDTmodel+"-"+simulationperiod+'_'+mapregion+'.png', bbox_inches = 'tight')

    chart.show()
