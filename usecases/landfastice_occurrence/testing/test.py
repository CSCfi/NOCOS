import earthkit.data
import earthkit.plots
import earthkit.regrid
import datetime

readin=False

# Future projection
#####################

#ScenarioMIP/SSP3-7.0 ICON ("resolution": "high") starts on "2020-09-01"
#ScenarioMIP/SSP3-7.0 ICON ("resolution": "high") ends on "2039-12-31"

#ScenarioMIP/SSP3-7.0 IFS-NEMO ("resolution": "high") starts on "2020-01-01"
#ScenarioMIP/SSP3-7.0 IFS-NEMO ("resolution": "high") ends on "2039-12-31"


# request = {
# 	    "activity": "ScenarioMIP",
# 	    "class": "d1",
# 	    "dataset": "climate-dt",
# 	    "date": "2020-01-01",
# 	    "experiment": "SSP3-7.0",
# 	    "expver": "0001",
# 	    "generation": "1",
# 	    "levtype": "o2d",
# 	    "model": "IFS-NEMO",
# 	    #"model": "ICON",
# 	    "param": "263001",
# 	    "realization": "1",
# 	    "resolution": "high",
# 	    "stream": "clte",
# 	    "time": "0000",
# 	    "type": "fc",
#     'grid' : 'O2560', # currently O, F, N grids are supported 
#     #'area' : '75/-15/30/42.5',
#    'area' : '85/-80/67/5', # maxLAT, minLON, minLAT, maxLON
#     }

# Historical
##################

##CMIP6/hist  ICON (resolution=high) starts "1991-03-01"
##CMIP6/hist  ICON (resolution=high) ends 2019-12-31

##CMIP6/hist IFS-NEMO (resolution=standard) starts "1990-01-01"
##CMIP6/hist IFS-NEMO (resolution=standard) ends "2002-02-28"

# request = {
# 	    "activity": "CMIP6",
# 	    "class": "d1",
# 	    "dataset": "climate-dt",
# 	    "date": "2002-02-28",
# 	    "experiment": "hist",
# 	    "expver": "0001",
# 	    "generation": "1",
# 	    "levtype": "o2d",
# 	    "model": "IFS-NEMO",	 
# 		#"model": "ICON",
# 	    "param": "263001",
# 	    "realization": "1",
# 	    #"resolution": "high",
# 	    "resolution": "standard",
# 	    "stream": "clte",
# 	    "time": "0000",
# 	    "type": "fc",
#     'grid' : 'O2560', # currently O, F, N grids are supported 
#    'area' : '85/-80/67/5', # maxLAT, minLON, minLAT, maxLON
#     }

# Storyline
#################

##story-nudging/{cont|hist|Tplus2.0K} IFS-FESOM (resolution=standard) starts "2017-01-01"
##story-nudging/{cont|hist|Tplus2.0K} IFS-FESOM (resolution=high) starts "2017-03-01"

##story-nudging/{cont|hist|Tplus2.0K} IFS-FESOM (resolution={standard|high}) ends  "2024-10-31",

request = {
	    "activity": "story-nudging",
	    "class": "d1",
	    "dataset": "climate-dt",
	    "date": "2024-10-31",
	    #"experiment": "hist",
	    "experiment": "cont",
	    #"experiment": "Tplus2.0K",
	    "expver": "0001",
	    "generation": "1",
	    "levtype": "o2d",
	    "model": "IFS-FESOM",	 
	    "param": "263001",
	    "realization": "1",
	    "resolution": "high",
	    #"resolution": "standard",
	    "stream": "clte",
	    "time": "0000",
	    "type": "fc",
    'grid' : 'O2560', # currently O, F, N grids are supported 
   'area' : '85/-80/67/5', # maxLAT, minLON, minLAT, maxLON
    }

if readin:
	dataICE = earthkit.data.from_source("polytope", "destination-earth", request, address="polytope.lumi.apps.dte.destination-earth.eu", stream=False)


plotting= True
if plotting:
	dataICE.ls()
	dataXR=dataICE.to_xarray(engine='cfgrib')
	dataXR



	from earthkit.plots.geo import domains
	import earthkit.data
	import earthkit.plots
	import numpy as np


	import cartopy.crs as ccrs
	# crs = ccrs.NorthPolarStereo(central_longitude=-30)


	# arctic_domain = domains.Domain(
	#     [-2800000, 2800000, -2800000, 2800000],
	#     crs=ccrs.NorthPolarStereo(),
	#     name="Arctic",
	# )
	greenland_domain = domains.Domain(
		[-1400000, 800000, -2900000, -400000],
		crs=ccrs.NorthPolarStereo(central_longitude=-35),
		name="Greenland",
	)
	qaanaaq_domain = domains.Domain(
		[-300000, 100000, -1600000, -1200000],
		crs=ccrs.NorthPolarStereo(central_longitude=-67),
		name="Qaanaaq",
	)

	chart = earthkit.plots.Map(domain=greenland_domain)
	#chart = earthkit.plots.Map(domain=qaanaaq_domain)
	chart.grid_cells(dataICE, style=earthkit.plots.styles.Style(colors="Spectral_r"))
	chart.coastlines(resolution='high',zorder=3)
	chart.land(resolution='high',zorder=2)
	chart.gridlines(zorder=4)
	chart.legend(label="Ice concentration [Fraction]")
	chart.title("Title")
	chart.show()

	#chart.block(dataXR, x='y', y='x',levels=np.arange(0, 1, 0.1), colors="winter")

	#chart.quickplot(dataXR, levels=np.arange(0, 1, 0.1), colors="winter")

