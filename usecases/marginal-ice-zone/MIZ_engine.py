# -*- coding: utf-8 -*-
"""

@author: Andrea Gierisch, DMI
@author: Keguang Wang, MetNO

"""
# Load MIZ functions
from read_config import read_configfile
from read_ice_data import read_ice_data
from save_MIZ_toNetCDF import save_toNetcdf
from calculate_MIZ import calc_MIZ

# Read config file
#configs=read_configfile() # Reads config_MIZcalc_default.yml
configs=read_configfile('METROMS_obs')

# Read ice data
icedata=read_ice_data(configs)

# Calculate MIZ
if configs['multiCAT']==True:
    raise NotImplementedError()
elif configs['multiCAT']==False:
    mizdata=calc_MIZ(icedata,configs)
    
# Save MIZ data to netcdf file
save_toNetcdf(mizdata,icedata,configs)


