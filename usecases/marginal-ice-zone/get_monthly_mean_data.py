"""Script to calculate monthly climatologies of landfastice coverage from ClimateDT simulations.

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

"""

plotavg=False
saveplot=True

import os
import earthkit.data
import earthkit.plots
import earthkit.regrid
from datetime import datetime, timedelta
import numpy as np

from utils.download_icedata import request_icedata_subarea
#from utils.fastice import avg_fasticecoverage

################
## User settings
################

# ClimateDT model (ICON or IFS-NEMO)
climateDTmodel='IFS-NEMO'
#climateDTmodel='ICON'

# Simulation period ( historical or SSP3-7.0 future scenario)
simulationperiod='historical'
#simulationperiod='future'

# For which month should the climatology be produced? (1-12)
# month=3
# for month in [1,3,5,11]:

# First and last year of the climatology to be produced
# ICON-historical
clima_fromyear=2010
clima_toyear=2019
# # ICON-future
#clima_fromyear=2030
#clima_toyear=2039


# For how many days does ice need to be stationary in order to be considered fastice?
# Default: 4 days
#fasticeduration=4 # days; For how many days ice needs to be stationary to be considered fastice

# Region to be processed (Greenland or Arctic)
#mapregion='Greenland'
mapregion='Arctic'

# Directory to store data files (temporarily):
user  = os.environ.get('USER')
datastoragedir='/nobackup/forsk/' + user + '/data/ClimateDT' 
if not os.path.exists(datastoragedir): os.makedirs(datastoragedir)

################
## End of user settings
################

# Process ClimateDT data for each year
######################################

fastice_forechyear=[] # Empty list to collect results for each year
#for year in [2018]: # doesn't exist for hist???
# for year in [2001]:
# for year in range(2010,2020):
for year in range(clima_fromyear,clima_toyear+1):

  for month in range(1,13):
    print()
    print("Starting with "+str(year) + str(month))
    
    # The start of the month
    date_start = datetime(year,month,1) 
    if month == 12:
       date_end = datetime(year,month,31) 
    else:
       date_end = datetime(year,month+1,1) - timedelta(days=1) 
    
    # The download request string for the dates
    REQ_daterange= date_start.strftime("%Y%m%d")+"/to/"+date_end.strftime("%Y%m%d")
    print("Going to download data from "+ date_start.strftime("%Y%m%d") + " to "+date_end.strftime("%Y%m%d"))
    
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

    # Retrieve data (SIC, sea ice velocity u, sea ice velocity v)
    try:
       dataICE1month=request_icedata_subarea(activity=REQactivity,experiment=REQexperiment,
                  model=climateDTmodel, date=REQ_daterange,subarea=mapregion, 
                  param="263001/263000", datadir=datastoragedir)


       # After read in:
       dataICExr=dataICE1month.to_xarray() # Needed for date in plot title
       #print(dataICExr)

       data_monthly = dataICExr.mean(dim='forecast_reference_time')

       fname = datastoragedir + '/' + climateDTmodel + '_monthly_mean_' + str(year*100 + month) + '.nc'
       data_monthly.to_netcdf(fname)
    except:
       print('data unavailable for ' + str(year*100 + month))

    # Calculate average fastice coverage for this month
    #avg_fasticecover_grb = avg_fasticecoverage(dataICE1month,speedthreshold=5e-4,fasticeduration=4)
    #fastice_forechyear.append(avg_fasticecover_grb)

###
# End of year loop
####################


# Make climatology: Average over the monthly datasets of each year
#fasticeclimatology_numpy=np.mean([grb.to_array() for grb in fastice_forechyear],axis=0)
# Put data into an empty/random grib object
#fasticeclimatology=dataICE1month[0].clone(values=fasticeclimatology_numpy,
#                                          dataDate=str(clima_fromyear)+"-"+str(clima_toyear),
#                                          name="Avg. fast ice coverage", shortName="fastice", units="",
#                                          stepRange='0') # Check metadata with e.g.: avg_fasticecover_grb.metadata("name")


#####################################
### Plotting fast ice climatology
#####################################

if plotavg:
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
        # [-1400000, 800000, -2500000, -400000],
        [-1300000, 800000, -2400000, -550000], # E, W, S, N
        crs=ccrs.NorthPolarStereo(central_longitude=-35),
        name="Greenland",
    )
    qaanaaq_domain = domains.Domain(
        [-300000, 100000, -1600000, -1200000],
        crs=ccrs.NorthPolarStereo(central_longitude=-67),
        name="Qaanaaq",
    )


    # The field to plot
    fasticeOCCtoplot=fasticeclimatology
    print(fasticeOCCtoplot.ls())


    chart = earthkit.plots.Map(domain=greenland_domain)
    # chart = earthkit.plots.Map(domain=qaanaaq_domain)
    # chart.grid_cells(fasticeOCCtoplot,interpolate=dict(method='nearest'),
    chart.grid_cells(fasticeOCCtoplot,
                    style=earthkit.plots.styles.Style(colors="viridis", extend="both",
                                                    levels=[0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.]))

    chart.coastlines(resolution='high',zorder=3)
    chart.land(resolution='high',zorder=2)
    # chart.coastlines(resolution='medium',zorder=3)
    # chart.land(resolution='medium',zorder=2)

    chart.gridlines(zorder=4)
    chart.legend(label="Average fast ice coverage [fraction]")

    # chart.title("Average "+str(fasticeduration)+"-day fastice occurrence\n between "+ date_start.strftime("%Y-%m-%d") +" and " + date_end.strftime("%Y-%m-%d")  +", "+climateDTmodel)
    chart.title("Average "+str(fasticeduration)+"-day fastice occurrence\n " +
         "Climatology for " + date_start.strftime("%B") +" "+str(clima_fromyear)+"-"+str(clima_toyear)+", "
         +climateDTmodel+"-"+simulationperiod)


    if saveplot:
        import matplotlib.pyplot as plt
        plt.savefig('./images/fasticeclimatology_'+date_start.strftime("%B")+"_"+str(clima_fromyear)+"-"+str(clima_toyear)+"_"+climateDTmodel+"-"+simulationperiod+'.png', bbox_inches = 'tight')

    chart.show()
