def request_icedata_subarea(activity,experiment,model,date,subarea,param,datadir=None,gridtype=None):
	"""
	This function retrieves ClimateDT data
	#####
	- If a datadir is given, the function checks whether the desired data is already existing there.
	- Otherwise it will send a request to Polytope.
	- If a datadir is given and data was not existing there, the downloaded data will be saved for later use.
    
    Example usage:
    dataICE=request_icedata_subarea(activity="CMIP6",experiment="hist",model="ICON",
                                    date="2002-02-28",subarea="greenland", param="263001/263003/263004",
                                    datadir="/media/volume/")

    """
	
	# Set pre-defined download areas
	import earthkit.data
	print('subarea = ',subarea)
	if subarea in ["Greenland","greenland"]:
		area='85/-80/67/5'
		# Use default gridtype if not specified by the user
		if not(gridtype):
			gridtype='F2000'
	elif subarea in ["Arctic","arctic"]:
		area='90/-180/55/180'
		# Use default gridtype if not specified by the user
		if not(gridtype):
			gridtype='F512'
	else:
		raise RuntimeError("Unknown subarea: "+ subarea+". Cannot create request.")
	
	# Check if data is already existing on disk
	filename='icedata_'+activity+'_'+experiment+'_'+model+'_'+date.replace("/","-")+'_'+subarea+'_'+gridtype+'_'+param.replace("/","-")+'.grb'
	if datadir:
		print("Looking for previously downloaded data in: "+datadir)
		print("File name to look for: "+filename)
		try:
			dataICE=earthkit.data.from_source("file",datadir+"/"+filename)
		except FileNotFoundError:
			# File is not existing, hence download the data
			requestdata=True
		else:
			# No error, hence file was found, hence we don't need to download it
			print("Loading data from file:"+datadir+"/"+filename)
			requestdata=False
	else:
		requestdata=True
	
	# Request data from Polytope
	if requestdata==True: # No datadir given or file not existing in datadir => Will download data
		print("No datadir given or no existing data file found. I will request data from Polytope...")
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
				'grid' : gridtype, # e.g. 'O2560' (octahedral reduced gaussian) or 'F512' (regular gaussian), # currently O, F, N grids are supported
				'area' : area # e.g. '85/-80/67/5' # maxLAT, minLON, minLAT, maxLON
			}
		print(request)

		# Execute the download request
		#    data is an earthkit streaming object but with stream=False will download data immediately 
		dataICE = earthkit.data.from_source("polytope", "destination-earth", request, 
										address="polytope.lumi.apps.dte.destination-earth.eu", stream=False)
	
		# Save data to disk for later use , if "datadir" is given
		if datadir:
			print("Saving data to: "+datadir+"/"+filename)
			dataICE.to_target("file",datadir+"/"+filename)
	
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

# request = {
# 	    "activity": "story-nudging",
# 	    "class": "d1",
# 	    "dataset": "climate-dt",
# 	    "date": "2024-10-31",
# 	    #"experiment": "hist",
# 	    "experiment": "cont",
# 	    #"experiment": "Tplus2.0K",
# 	    "expver": "0001",
# 	    "generation": "1",
# 	    "levtype": "o2d",
# 	    "model": "IFS-FESOM",	 
# 	    "param": "263001",
# 	    "realization": "1",
# 	    "resolution": "high",
# 	    #"resolution": "standard",
# 	    "stream": "clte",
# 	    "time": "0000",
# 	    "type": "fc",
#     'grid' : 'O2560', # currently O, F, N grids are supported 
#    'area' : '85/-80/67/5', # maxLAT, minLON, minLAT, maxLON
#     }
