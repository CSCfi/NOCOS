#! /usr/bin/env python

# -*- coding: utf-8 -*-
"""

@author: Keguang Wang, MetNO

"""

import sys, os
import numpy as np

# Load MIZ functions
from read_config import read_configfile
from read_ice_data import read_ice_data
from utils.save_MIZ_toNetCDF import save_toNetcdf
from utils.calculate_MIZ import calc_MIZ

usecase = 'ClimateDT'

# Read config file
configs=read_configfile(usecase)

# Read ice data
for sensor in configs['selectdata']['sensors']:
    print('Processing ' + sensor + ':')

    if 'future' in sensor:
       year_start, year_end = 2030, 2031
    elif 'hist' in sensor:
       year_start, year_end = 2010, 2019
    else:
       print('Sensor not available, exit ...')
       sys.exit()

    for year in range(year_start,year_end):
        for month in range(1,13):
            #print('   processing date ' + str(year*100 + month) + ' ...')
            #try:
                configs['date'] = str(year*100 + month)
                configs['sensor'] = sensor
                configs['ice_filename'] = os.path.join(configs['ice_folder'],sensor,
                   sensor.split('_')[0] + '_monthly_mean_' + configs['date'] + '.nc')
                icedata=read_ice_data(configs)
                
                # Calculate MIZ
                if configs['multiCAT'] == True:
                   raise NotImplementedError()
                elif configs['multiCAT']==False:
                   mizdata, miz_ext, mean_lat = calc_MIZ(icedata,configs)
                print(sensor, year, month, miz_ext, mean_lat)
           
                # Save MIZ data to netcdf file
                save_toNetcdf(mizdata,icedata,configs)

            #except:
            #    print('     No data in ' + str(year*100+month))

