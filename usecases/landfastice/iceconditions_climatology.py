"""Script to calculate monthly climatologies of ice parameters from ClimateDT simulations.

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

readin=True
plotmap=True
saveplot=True


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

# Ice parameters to plot
plotSIC=True
plotSIT=False
plotSNOW=False
plotICEDRIFT=False

# Ice parameters to download
paramSIC=True
paramSIT=True
paramSNOW=True
paramICEDRIFT=True

# ClimateDT model (ICON or IFS-NEMO)
# climateDTmodel='IFS-NEMO'
climateDTmodel='ICON'

# Simulation period ( historical or SSP3-7.0 future scenario)
# simulationperiod='historical'
simulationperiod='future'

# For which month should the climatology be produced? (1-12)
month=3
# for month in [1,3,5,11]:

# First and last year of the climatology to be produced
# # ICON-historical
# clima_fromyear=2010
# clima_toyear=2019

# # IFS-NEMO historical, not available yet
# clima_fromyear=1990
# clima_toyear=1999

# ICON/IFS-future
clima_fromyear=2030
clima_toyear=2039


# Region to be processed (Greenland or Arctic or Inglefield)
# mapregion='Greenland'
# mapregion='Arctic'
mapregion='Inglefield' # This will download/use data for Greenland

# Directory to store data files (temporarily):
datastoragedir='/media/volume/data_storage_andrea/'

# Font size for the plot
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
    #for year in [2018]: # doesn't exist for hist???
    # for year in [2010]:
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
        # [-1400000, 800000, -2500000, -400000],
        # [-1300000, 800000, -2400000, -550000], # W, E, S, N
        [-1300000, 700000, -2200000, -600000], # W, E, S, N
        crs=ccrs.NorthPolarStereo(central_longitude=-35),
        name="Greenland",
    )
    qaanaaq_domain = domains.Domain(
        # [-300000, 100000, -1600000, -1200000],
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
        # fasticeOCCtoplot=icedata['avg_icespeed'][1,:,:]  
        # icetoplot=icedata_climatology['avg_icespeed']

        # Set up the map
        if mapregion in ["Greenland","greenland"]:
            chart = earthkit.plots.Map(domain=greenland_domain)
        elif mapregion in ["Arctic","arctic"]:
            chart = earthkit.plots.Map(domain=arctic_domain)
        elif mapregion in ["Qaanaaq","Inglefield"]:
            chart = earthkit.plots.Map(domain=qaanaaq_domain)

        # Plot the data
        # chart.grid_cells(fasticeOCCtoplot,interpolate=dict(method='nearest'),
        # chart.grid_cells(icetoplot,
        #                 style=earthkit.plots.styles.Style(colors="viridis", extend="both",
                                                        # levels=[0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.]))
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
                plt.savefig('./images/iceparameters/climatology-'+icevar[4:]+'_'+date_start.strftime("%B")+"_"+str(clima_fromyear)+"-"+str(clima_toyear)+"_"+climateDTmodel+"-"+simulationperiod+'_'+mapregion+'.png', bbox_inches = 'tight', facecolor='k')
            else:
                plt.savefig('./images/iceparameters/climatology-'+icevar[4:]+'_'+date_start.strftime("%B")+"_"+str(clima_fromyear)+"-"+str(clima_toyear)+"_"+climateDTmodel+"-"+simulationperiod+'_'+mapregion+'.png', bbox_inches = 'tight')

        chart.show()
