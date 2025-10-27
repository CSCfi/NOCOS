


import earthkit.data
import earthkit.plots
#import earthkit.regrid
import datetime
from earthkit.plots.geo import domains
import numpy as np
import matplotlib.pyplot as plt

################
## User settings
################

# ClimateDT model (ICON or IFS-NEMO)
datasource='icecharts'
# datasource='HYCOM-CICE'

saveplot=True

# Which month shall be plotted? (1-12)
month=3
monthname= datetime.datetime(2099,month,15).strftime("%B")

# First and last year of the climatology to be plotted
clima_fromyear=2010
clima_toyear=2019

# Region to be processed (Greenland or Arctic)
mapregion='Greenland'
# mapregion='Arctic'

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



# Font size for the plot
plotfontsize=16

################
## End of user settings
################

dataRAW=earthkit.data.from_source("file",filepath)
plotdata=dataRAW.to_xarray() 

##########################################
### Make plot of fastice conditions on a specific day
###########################################


#### Plot domains

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


##########################################
# ### Plot
########################################

chart = earthkit.plots.Map(domain=greenland_domain)

for mapregion in ["Greenland", "Inglefield"]:

    if mapregion in ["Greenland","greenland"]:
        chart = earthkit.plots.Map(domain=greenland_domain)
    elif mapregion in ["Arctic","arctic"]:
        chart = earthkit.plots.Map(domain=arctic_domain)
    elif mapregion in ["Qaanaaq","Inglefield"]:
        chart = earthkit.plots.Map(domain=qaanaaq_domain)

    # chart.grid_cells(plotdata,z=varLFI,
    #                 style=earthkit.plots.styles.Style(colors="jet",
    #                                                 levels=[0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.00001])) # If the last level is 1. instead of 1.000001, then areas with 100% covereage are plotted white instead of red.
    # chart.grid_cells(plotdata,x=varLON, y=varLAT,z=varLFI,
    #                 style=earthkit.plots.styles.Style(colors="jet",
    #                                                 levels=[0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.00001])) # If the last level is 1. instead of 1.000001, then areas with 100% covereage are plotted white instead of red.
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
            plt.savefig('./images/fasticeclimatology_'+monthname+'_'+str(clima_fromyear)+'-'+str(clima_toyear)+'_'+datasource+'_'+mapregion+'.png', bbox_inches = 'tight', facecolor='k')
        else:
            plt.savefig('./images/fasticeclimatology_'+monthname+'_'+str(clima_fromyear)+'-'+str(clima_toyear)+'_'+datasource+'_'+mapregion+'.png', bbox_inches = 'tight')


# end for mapregion




