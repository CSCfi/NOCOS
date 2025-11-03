"""Script to plot landfast ice climatologies from icecharts or HYCOM-CICE model.

plot_external_fasticedata.py

This script can be used to create plots that look similar to the ones created
by landfastice_climatology.py but containing other data sources, for 
example for validation/comparison. The datasets need to be prepared 
beforehand and should contain landfast ice coverage climatology for the 
desired month and time range.

Sections in this script:
    a) User settings
       The user specifies which data should be plotted.
    b) Settings specific to the dataset
       Automatic settings like variable names depening on the chosen dataset.
    c) Plot the landfast ice climatology
       The  user can choose between two pre-defined regions
       (Greenland or Inglefield Bredning).
       Output is saved into the directory given in `plotdir`.


Example
-------

Edit this script according to your needs, and specify the path to the dataset
as the variable FILEPATH.
Execute the script::

    $ python plot_external_fasticedata.py


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
import datetime
from earthkit.plots.geo import domains
import numpy as np
import matplotlib.pyplot as plt

saveplot=True


################
## User settings
################

# Data source ('icecharts' or 'HYCOM-CICE')
datasource='icecharts'
# datasource='HYCOM-CICE'

# Which month shall be plotted? (1-12)
month=3
monthname= datetime.datetime(2099,month,15).strftime("%B")

# First and last year of the climatology to be plotted
clima_fromyear=2010
clima_toyear=2019

# Region to be processed (Greenland or Arctic)
mapregion='Greenland'
# mapregion='Arctic'

# Font size for the plot
plotfontsize=16

## Directory to save plots:
plotdir='./images/'


################
## End of user settings
################

# Settings depending on the input data

if datasource=="icecharts":
    # Filename to plot
    filepath='/media/volume/data_storage_andrea/icecharts/GreenlandTOPNW_fastice_mon'+str(month).zfill(2)+'_'+str(clima_fromyear)+'-'+str(clima_toyear)+'_ymonmean.nc'
    # Name of the landfastice variable in the data file
    varLFI='FA'
    # Name of latitude/longitude coordinates
    varLON='lon'
    varLAT='lat'
    # Title to be shown on the plot
    ## long version
    #plottitle="Average fastice occurrence\n " +"Climatology for " + monthname+" "+str(clima_fromyear)+"-"+str(clima_toyear)+" from "+datasource
    # short version
    plottitle="Ice charts ("+str(clima_fromyear)+"-"+str(clima_toyear)+")"
elif datasource=="HYCOM-CICE":
    # Filename to plot
    fasticeduration="4"
    filepath='/media/volume/data_storage_andrea/HYCOM-CICE/greentopnw_'+fasticeduration+'day-fastice_'+str(clima_fromyear)+'-'+str(clima_toyear)+'_climatology_mon'+str(month).zfill(2)+'.nc'
    # Name of the landfastice variable in the data file
    varLFI='ff'
    # Name of latitude/longitude coordinates
    varLON='ULON'
    varLAT='ULAT'
    # Title to be shown on the plot
    plottitle="Average fastice occurrence\n " +"Climatology for " + monthname+" "+str(clima_fromyear)+"-"+str(clima_toyear)+" from "+datasource
else:
    raise RuntimeError("DATASOURCE must be 'icecharts' or 'HYCOM-CICE'.")


dataRAW=earthkit.data.from_source("file",filepath)
plotdata=dataRAW.to_xarray() 


##########################################
### Make plot of fastice conditions on a specific day
###########################################


# Plot domains
import cartopy.crs as ccrs
crs = ccrs.NorthPolarStereo(central_longitude=10)


arctic_domain = domains.Domain(
    [-2800000, 2800000, -2800000, 2800000],
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

# Create the plot
chart = earthkit.plots.Map(domain=greenland_domain)

for mapregion in ["Greenland", "Inglefield"]:

    if mapregion in ["Greenland","greenland"]:
        chart = earthkit.plots.Map(domain=greenland_domain)
    elif mapregion in ["Arctic","arctic"]:
        chart = earthkit.plots.Map(domain=arctic_domain)
    elif mapregion in ["Qaanaaq","Inglefield"]:
        chart = earthkit.plots.Map(domain=qaanaaq_domain)

    chart.grid_cells(plotdata,x=varLON, y=varLAT,z=varLFI,
                     style=earthkit.plots.styles.Style(colors="viridis", extend="both",
                                                    levels=[0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.]))

    chart.coastlines(resolution='high',zorder=3)
    chart.land(resolution='high',zorder=2)

    plt.rcParams.update({'font.size': plotfontsize})

    if not mapregion=="Inglefield":
        chart.gridlines(zorder=4)
        chart.legend(label="Average fast ice coverage [fraction]")
        chart.title(plottitle, fontsize=plotfontsize)


    if saveplot:
        import matplotlib.pyplot as plt
        if mapregion=="Inglefield":
            plt.savefig(plotdir+'/fasticeclimatology_'+monthname+'_'+str(clima_fromyear)+'-'+str(clima_toyear)+'_'+datasource+'_'+mapregion+'.png', bbox_inches = 'tight', facecolor='k')
        else:
            plt.savefig(plotdir+'/fasticeclimatology_'+monthname+'_'+str(clima_fromyear)+'-'+str(clima_toyear)+'_'+datasource+'_'+mapregion+'.png', bbox_inches = 'tight')


# end for mapregion




