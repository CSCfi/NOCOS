import earthkit.data
request = {
       "activity": "story-nudging",
       "class": "d1",
       "dataset": "climate-dt",
       "date": "2020-01-01/to/2020-01-31",  #
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
       'area' : '10/30/67/53', # maxLAT, minLON, minLAT, maxLON
   }

dataICE = earthkit.data.from_source("polytope", "destination-earth", request, address="polytope.lumi.apps.dte.destination-earth.eu", stream=False)


request = {
    "activity": "CMIP6",
    "class":    "d1",
    "dataset":  "climate-dt",
    "experiment": "historical",
    "model":     "ICON",           # or another supported model
    "realization": "1",
    "generation":   "1",
    "resolution":   "high",        # or "standard"
    "date":         "19900101",    # YYYYMMDD – can be start or specific date
    "expver":       "0001",
    "levtype":      "o2d",
    "param":        "263001",         # variable code, e.g. 167=temperature
    "stream":       "clte",
    "time":         "0000",
    "type":         "fc",
	"feature": {
		"type": "boundingbox",
		"points": [[56, 21], [61, 30]]  # [lat_min, lon_min], [lat_max, lon_max]
	}
}

ds = earthkit.data.from_source(
    "polytope",
    "destination-earth",
    request,
    address="polytope.lumi.apps.dte.destination-earth.eu",
    stream=False  # download immediately
)



import earthkit.data

request = {
     "activity": "CMIP6",
    "class":    "d1",
    "dataset":  "climate-dt",
    "experiment": "historical",
    "model":     "IFS-NEMO",           # or another supported model
    "realization": "1",
    "generation":   "1",
    "resolution":   "high",        # or "standard"
    "date":         "19900101",    # YYYYMMDD – can be start or specific date
    "expver":       "0001",
    "levtype":      "o2d",
    "param":        "263001",         # variable code, e.g. 167=temperature
    "stream":       "clte",
    "time":         "0000",
    "type":         "fc",
    "feature": {
        "type": "boundingbox",
        "points": [[21.0, 57.0], [24.0, 59.0]]  # [W,S] and [E,N]
    }
}

ds = earthkit.data.from_source(
    "polytope",
    "destination-earth",
    request,
    address="polytope.lumi.apps.dte.destination-earth.eu",
    stream=False
)
