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








import utils.functions
import utils.num3

print(utils.functions.blafunc(5))
print(utils.num3.mal3(4))



readin=True
plotoneday=False
plotavg=False

saveplot=False


import earthkit.data
import earthkit.plots
import earthkit.regrid
import datetime
import pandas as pd

from utils.download_icedata_c import request_icedata_subarea

################
## User settings
################

# ClimateDT model (ICON or IFS-NEMO)
# model='IFS-NEMO'
climateDTmodel='ICON'

# Simulation period ( historical or SSP3-7.0 future scenario)
simulationperiod='historical'
# simulationperiod='future'

# For which month should the climatology be produced? (1-12)
month=1

# For how many days does ice need to be stationary in order to be considered fastice?
# Default: 4 days
fasticeduration=4 # days; For how many days ice needs to be stationary to be considered fastice

# Region to be processed (Greenland or Arctic)
mapregion='Greenland'
# mapregion='Arctic'

# Directory to store data files (temporarily):
datastoragedir='/media/volume/data_storage_andrea/'

################
## End of user settings
################

# Checking user input
######################
if not(month in range(1,13)):
    raise ValueError("MONTH must be between 1 and 12")
if not(mapregion=='Greenland'):
    raise NotImplementedError("Not implemented for mapregion: "+mapregion)

# Process ClimateDT data for each year
######################################

#for year in [2018]: # doesn't exist for hist???
for year in [2001]:
#for year in range(2019,2025):

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


    if readin:
        
        # Set activity and experiment according to user input
        if simulationperiod=='historical':
            REQactivity="CMIP6"
            REQexperiment="hist"
        elif simulationperiod=='future':
            REQactivity="ScenarioMIP"
            REQexperiment="SSP3-7.0"

        # Retrieve data (SIC, sea ice velocity u, sea ice velocity v)
        dataICE1month=request_icedata_subarea(activity=REQactivity,experiment=REQexperiment,model=climateDTmodel,
                                        date=REQ_daterange,subarea=mapregion, param="263001/263003/263004",
                                        datadir=datastoragedir)


        # Future projection
        #####################
        #ScenarioMIP/SSP3-7.0 ICON ("resolution": "high") starts on "2020-09-01"
        #ScenarioMIP/SSP3-7.0 ICON ("resolution": "high") ends on "2039-12-31"
        #ScenarioMIP/SSP3-7.0 IFS-NEMO ("resolution": "high") starts on "2020-01-01"
        #ScenarioMIP/SSP3-7.0 IFS-NEMO ("resolution": "high") ends on "2039-12-31"

        # dataICE=request_icedata_subarea(activity="ScenarioMIP",experiment="SSP3-7.0",model=climateDTmodel,date=REQ_daterange,
                                    # param="263001/263003/263004")
        
        # Historical
        ##################
        ##CMIP6/hist  ICON (resolution=high) starts "1991-03-01"
        ##CMIP6/hist  ICON (resolution=high) ends 2019-12-31
        ##CMIP6/hist IFS-NEMO (resolution=standard) starts "1990-01-01"
        ##CMIP6/hist IFS-NEMO (resolution=standard) ends "2002-02-28"

        # dataICE=request_icedata_subarea(activity="CMIP6",experiment="hist",model=climateDTmodel,date=REQ_daterange,
        #                             subarea="greenland", param="263001/263003/263004",
        #                             datadir=datastoragedir)

        # Storyline
        #################
        ##story-nudging/{cont|hist|Tplus2.0K} IFS-FESOM (resolution=standard) starts "2017-01-01"
        ##story-nudging/{cont|hist|Tplus2.0K} IFS-FESOM (resolution=high) starts "2017-03-01"
        ##story-nudging/{cont|hist|Tplus2.0K} IFS-FESOM (resolution={standard|high}) ends  "2024-10-31",
        ## cont: Control-1950, hist: Present day, Tplus2.0K: 2K warmer than pre-industrial, about 2040

        # dataICE=request_icedata_subarea(activity="story-nudging",experiment=REQexperiment,model=climateDTmodel,date=REQ_daterange,
        #                             subarea="greenland", param="263001/263003/263004",
        #                             datadir=datastoragedir)


    # After read in:
    dataICExr=dataICE1month.to_xarray() # Needed for date in plot title

    dataICE=dataICE1month

    # calc_fastice(dataICE,speedthreshold=5e-4,fasticeduration=4)
    """Calculate landfast ice areas.

    This function determines for each grid cell (vector/healpix) and for each day
    whether there has been ice with SIC>90% and with
    ice drift speed < speedthreshold (default 5e-4 m/s) for n days in a row (default 4 days).

    Assumptions about input data dataICE:
    - grb object retrieved from Polytope
    - 3 fields per day, provided in this order: 
       * daily average sea ice concentration (avg_siconc)
       * daily average ice drift speed u-component (avg_siue)
       * daily average ice drift speed v-component (avg_sivn)
    - number of daily fields available >= fasticeduration (=number of days for which the ice needs to be stationary in order to be considered fast ice)

    Parameters
    ----------
    dataICE : grb-object
        Dataset from Polytope, including the parameters:
        avg_siconc, avg_siue, and avg_sivn for several days
    speedthreshold : float , optional
        Daily mean ice drift speed must be below this limit for the ice to be considered 'fast ice'
        Default: 5e-4 m/s
    fasticeduration : int, optional
        For how many days in a row the speed criterion must be fulfilled.
        Default: 4 days

    Returns
    -------
    bool?????
        number of days in output = number of days in input - fasticeduration - 1
    """
    speedthreshold=5e-4
    ##### Extract data from grib object

    siconc=dataICE[0::3].values
    siu=dataICE[1::3].values
    siv=dataICE[2::3].values

    ##### Calculate drift speed

    import numpy as np
    speed=np.sqrt(siu**2+siv**2)

    ##### Calculate areas covered by fast ice"

    canvaswithland=speed.copy()
    fasticemask=np.logical_and(np.less(speed,speedthreshold),np.greater(siconc,0.90)) # True where speed<5e-4 and SIC>90%
    landmask=np.isnan(canvaswithland)
    watermask=np.logical_and(np.logical_not(landmask),np.logical_not(fasticemask))
    canvaswithland[watermask]=0.
    canvaswithland[fasticemask]=1. # e.g.: Number of time stamps = number of days in month + fasticeduration

    #### Recursive function to determine where there is fastice for daysN in a row
    def fastice_for_x_days(fasticeN,daysN):
        # shape of fasticeN: [days,healpixcells]
        if daysN==1:
            return fasticeN
        else:
            # fasticeNm1=np.logical_and(fasticeN[0:-1,:],fasticeN[1:,:]) # Has there been fastice today and yesterday?
            fasticeNm1=np.logical_and(fasticeN[0:-1],fasticeN[1:]) # Has there been fastice today and yesterday?
            daysNm1=daysN - 1
            return fastice_for_x_days(fasticeNm1,daysNm1) # Call again for one day less

    fasticedata=fastice_for_x_days(canvaswithland,fasticeduration) # e.g.: Number of time stamps = number of days in month"

    ### Averaging over all days
    avg_fasticecover_numpy=np.mean(fasticedata[:,:],axis=0)      # average over time -> percentage of fast ice coverage over time
    centertimestep=fasticeduration-1+int(fasticedata.shape[0]/2) # Number of day in dataICE representing mid of the month
    centertimestepidx=centertimestep*3                           # Index in dataICE representing mid of the month
    avg_fasticecover_grb=dataICE[centertimestep*3].clone(values=avg_fasticecover_numpy, name="Avg. fast ice coverage", shortName="fastice", units="") # Check metadata with e.g.: avg_fasticecover_grb.metadata("name")


if plotoneday or plotavg:
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

##########################################
### Make plot of fastice conditions on a specific day
###########################################

if plotoneday:

    #### The field to plot
    plottimestamp=15
    fasticetoplot=dataICE[0].clone(values=fasticedata[plottimestamp,:]) # Clone something random to make the field into a grib field again


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

    if saveplot:
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

if plotavg:

    # The field to plot
    # endtimestamp=canvaswithland.shape[0]-fasticeduration
    # # mean_fasticecover=np.mean(canvaswithland[:,:],axis=0) # average over time -> percentage of fast ice coverage
    # mean_fasticecover=np.mean(fasticedata[:,:],axis=0) # average over time -> percentage of fast ice coverage
    # fasticeOCCtoplot=dataICE[((fasticeduration-1)+endtimestamp)*3].clone(values=mean_fasticecover, name="Avg. fast ice coverage", shortName="fastice", units="") # Check metadata with e.g.: fastice.metadata("name")
    fasticeOCCtoplot=avg_fasticecover_grb
    print(fasticeOCCtoplot.ls())


    chart = earthkit.plots.Map(domain=greenland_domain)
    # chart = earthkit.plots.Map(domain=qaanaaq_domain)
    # chart.grid_cells(fasticeOCCtoplot,interpolate=dict(method='nearest'),
    chart.grid_cells(fasticeOCCtoplot,
                    style=earthkit.plots.styles.Style(colors="jet",
                                                    levels=[0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1,1.001]))

    chart.coastlines(resolution='high',zorder=3)
    chart.land(resolution='high',zorder=2)
    chart.gridlines(zorder=4)
    chart.legend(label="time-average fast ice coverage [fraction]")

    # chart.title("Average "+str(fasticeduration)+"-day fastice occurrence\n between "+ date_start.strftime("%Y-%m-%d") +" and " + date_end.strftime("%Y-%m-%d")  +", "+climateDTmodel)
    chart.title("Average "+str(fasticeduration)+"-day fastice occurrence\n " +
         "Climatology for" + date_start.strftime("%B") +", "+climateDTmodel+"-"+simulationperiod)

    # daterange=date_start.strftime("%Y-%m-%d") +"_" + date_end.strftime("%Y-%m-%d")

    if saveplot:
        import os
        os.chdir('/home/andreag/nocoscode/NOCOS-gitv1/usecases/landfastice_occurrence/testing')
        import sys
        sys.path.append(os.getcwd())
        import matplotlib.pyplot as plt
        # # plt.savefig('./plots/AVGfastice-'+str(fasticeduration)+'day_'+climateDTmodel+'_'+daterange+'.png', bbox_inches = 'tight')
        # plt.savefig('./plots/AVGfastice-'+str(fasticeduration)+'day_'+climateDTmodel+'-'+REQexperiment+'_'+daterange+'.png', bbox_inches = 'tight')

    chart.show()
