#! /usr/bin/env python

# -*- coding: utf-8 -*-
"""

@author: Keguang Wang, MetNO

"""

#=====================================================================
import sys, os
import numpy as np
import pandas as pd

# Load MIZ functions
from read_config import read_configfile
from read_ice_data import read_ice_data
from utils.save_MIZ_toNetCDF import save_toNetcdf
from utils.calculate_MIZ import calc_MIZ

#=====================================================================
dataSource = 'ClimateDT'

# Read config file
configs=read_configfile(dataSource)

# set start and end years for the dataset
year_start = int(configs['selectdata']['year_start'])
year_end   = int(configs['selectdata']['year_end'])

if year_end <= 2019:
   simulationPeriod = 'historical'
elif year_start >= 2020:
   simulationPeriod = 'future'

#=====================================================================
# Read ice data
for dataset in configs['selectdata']['datasets']:

    print('Processing ' + dataset + ':')
    
    dataset1 = dataset +'_' + simulationPeriod

    dates = []
    for year in range(year_start,year_end+1):
        for month in range(1,13):
            dates.append(str(year*100 + month))
    df = pd.DataFrame(np.zeros((12*(year_end-year_start+1),2)), index=dates,           
                      columns=['miz_ext','mean_lat'])
    
    for year in range(year_start,year_end+1):
        for month in range(1,13):
            print('   processing date ' + str(year*100 + month) + ' ...')
            try:
                configs['date'] = str(year*100 + month)
                configs['dataset'] = dataset1
                configs['ice_filename'] = os.path.join(configs['ice_folder'],dataset1,
                   dataset + '_monthly_mean_' + configs['date'] + '.nc')
                icedata=read_ice_data(configs)
                
                # Calculate MIZ
                if configs['multiCAT'] == True:
                   raise NotImplementedError()
                elif configs['multiCAT']==False:
                   mizdata, miz_ext, mean_lat = calc_MIZ(icedata,configs)
                print(dataset, year, month, miz_ext, mean_lat)
                df.loc[str(100*year+month),['miz_ext', 'mean_lat']] = [miz_ext, mean_lat]
           
                # Save MIZ data to netcdf file
                save_toNetcdf(mizdata,icedata,configs)

            except:
                print('     No data in ' + str(year*100+month))
                df.loc[str(100*year+month),['miz_ext', 'mean_lat']] = ['NaN', 'NaN']
            
    df.to_csv(os.path.join(configs['output']['output_folder'], dataset1+'_stats.txt'), 
              sep='\t', index=True,header=False)

