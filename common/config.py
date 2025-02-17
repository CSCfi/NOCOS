NOCOSDIR="/home/ubuntu/NOCOS"
DATA_DIR ="/media/volume/NOCOS_WRK/data/"
OUTPUT_DIR ="/media/volume/NOCOS_WRK/output/"
request_cacb_IFSNEMO_o2d = {
    "url": "https://cacheb.dcms.destine.eu/d1-climate-dt/ScenarioMIP-SSP3-7.0-IFS-NEMO-0001-high-o2d-v0.zarr",
    "format": "zarr",
}

request_template_m1 = {
    'activity': 'ScenarioMIP',
    'class': 'd1',
    'dataset': 'climate-dt',
    'experiment': 'SSP3-7.0',
    'expver': '0001',
    'generation': '1',
    'levtype': 'o2d',
    'model': 'IFS-NEMO',
    'param': '263000/263001',
    'realization': '1',
    'resolution': 'high',
    'stream': 'clte',
    'time': '0000',
    'type': 'fc'
}

request_template_m2 = {
    'activity': 'ScenarioMIP',
    'class': 'd1',
    'dataset': 'climate-dt',
    'experiment': 'SSP3-7.0',
    'expver': '0001',
    'generation': '1',
    'levtype': 'o2d',
    'model': 'IFS-NEMO',
    'param': '263000/263001',
    'realization': '1',
    'resolution': 'high',
    'stream': 'clte',
    'time': '0000',
    'type': 'fc'
}