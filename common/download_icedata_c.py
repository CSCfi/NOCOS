def request_icedata_subarea(activity,experiment,model,date,subarea,param):
	import earthkit.data
	if subarea in ["Greenland","greenland"]:
		area='85/-80/67/5'
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
			"levtype": "o2d",
			"model": model,
			"param": param,
			"realization": "1",
			"resolution": "high",
			"stream": "clte",
			"time": "0000",
			"type": "fc",
		'grid' : 'O2560', # currently O, F, N grids are supported 
	'area' : area # e.g. '85/-80/67/5' # maxLAT, minLON, minLAT, maxLON
		}
	print(request)
	#data is an earthkit streaming object but with stream=False will download data immediately 
	dataICE = earthkit.data.from_source("polytope", "destination-earth", request, address="polytope.lumi.apps.dte.destination-earth.eu", stream=False)
	return(dataICE)




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
