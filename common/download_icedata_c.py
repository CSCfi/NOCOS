def request_icedata(activity,experiment,model,date,param):
	import earthkit.data
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
	}
	print(request)
	#data is an earthkit streaming object but with stream=False will download data immediately 
	dataICE = earthkit.data.from_source("polytope", "destination-earth", request, address="polytope.lumi.apps.dte.destination-earth.eu", stream=False)
	return(dataICE)

def request_icedata_polygon(activity,experiment,model,date,param):
	import earthkit.data
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
        "feature": {
            "type": "polygon",
            "shape": [[41.870881288,-8.8791360], [41.694339317422646, -8.824238614026456], [40.171924585721314, -8.902386975546364], [38.75694209400925, -9.493088042617785], [38.42424252381525, -9.171674240710018], [38.49907333213173, -8.676525850529856], [37.057269459205145, -8.971873318897366], [37.162874354643776, -7.406745406502978], [38.19776118392036, -6.931663452624974], [38.4280922170291, -7.321584397020473], [39.011852875635526, -6.9787177479519755], [39.66227871551288, -7.5393956904523804], [39.66568774825791, -7.03915852435145], [40.0019453234905, -6.883203763416162], [40.20373392742229, -7.035724907677206], [40.350463990828985, -6.8135246275213035], [41.030499770212515, -6.905947651233703], [41.593647729084154, -6.22847017956974], [41.67712153119277, -6.544984134823352], [41.949682257268876, -6.567927092516641], [41.96960294343674, -7.1747800681640115], [41.88337981339092, -7.196871678410446], [41.81334515396762,-8.156666519264604], [42.14242723772878, -8.205142297350534], [41.870881288,-8.8791360]],
    },
	}
	print(request)
	#data is an earthkit streaming object but with stream=False will download data immediately 
	dataICE = earthkit.data.from_source("polytope", "destination-earth", request, address="polytope.lumi.apps.dte.destination-earth.eu", stream=False)
	return(dataICE)

def request_icedata_boundingbox(activity,experiment,model,date,param,bbox):
	import earthkit.data
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
        "feature": {
            "type": "boundingbox",
            #"points" : [[53.55, 2.76], [50.66, 7.86]],
            "points" : [[bbox[2], bbox[0]], [bbox[3], bbox[1]]],
            #geht nicht "points" : [[70., 290], [85., 355.]],
            # geht auch nicht "points" : [[70., -70.], [85., -5.]],
            #"points" : [[70., -5.], [85., -70.]],
  #  },
    },
	}
	print(request)
	#data is an earthkit streaming object but with stream=False will download data immediately 
	dataICE = earthkit.data.from_source("polytope", "destination-earth", request, address="polytope.lumi.apps.dte.destination-earth.eu", stream=False)
	return(dataICE)

