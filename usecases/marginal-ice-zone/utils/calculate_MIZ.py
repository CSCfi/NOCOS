# -*- coding: utf-8 -*-
"""

@author: Keguang Wang, MetNo

"""
#=====================================================================
import numpy as np
import warnings
import time # for sleep and cputime measurement
import sys # For flushing of buffer to stdout

#=====================================================================
def ice_classes(icedata,configs):

    siconc = icedata.siconc
    if 'obs' in configs['ice_filename']:
       siconc = siconc * 0.01
    
    levels = eval(configs['levels']['traditional'].split(','))
    
    ic = np.zeros(siconc.shape) + np.nan

    for k in range(len(levels)-1):
        ic[levels[k] <= siconc <= levels[k+1]] = 0.5 * (levels[k] + levels[k+1])

    return(ic)


#=====================================================================
def grid_area(icedata):

    lon = icedata.longitude
    lat = icedata.latitude
    
    if len(lon.shape) == 1: 
       Lon, Lat = np.meshgrid(lon,lat)
    else:
       Lon, Lat = lon, lat

    dlon, dlat = Lon[0,1] - Lon[0,0], Lat[1,0] - Lat[0,0]
        
    if 'degree' in lon.units:
       ldg = 6370 * 2 * np.pi / 360
       area = np.ones(Lon.shape) * dlon * np.abs(dlat) * np.cos(Lat*np.pi/180) * ldg**2
    else:
       area = np.ones(Lon.shape) * dlon * dlat

    return(area)

#=====================================================================
def traditional_MIZ(icedata,configs):

    siconc = icedata.siconc
    
    if 'obs' in configs['ice_filename']:
       siconc = siconc * 0.01

    miz = np.zeros(siconc.shape) + np.nan

    # open water
    miz[(siconc >= 0) & (siconc < 0.1)] = 0
    
    # miz
    miz[(0.1 <= siconc) & (siconc <= 0.8)] = 1
    
    # compacted pack ice
    miz[siconc > 0.8] = 2
    
    area = grid_area(icedata)[miz == 1].sum()    

    return miz, area

#=====================================================================
def dynamical_MIZ(icedata,configs):

    siconc  = icedata.siconc
    sithick = icedata.sithick

    if 'obs' in configs['ice_filename']:
       siconc = siconc * 0.01

    miz = np.zeros(siconc.shape) + np.nan

    # open water
    miz[(siconc >= 0) & (siconc < 0.1)] = 0
    
    # miz
    miz[(0.1 <= siconc) & (siconc <= 0.85) & (sithick <= 2.0)] = 1
    miz[(siconc > 0.85) & (sithick <= 10.5 - 10.*siconc)] = 1
    
    # compacted pack ice
    miz[(siconc >= 0.1) & (sithick > 2.0)] = 2
    miz[(siconc > 0.85) & (sithick > 10.5 - 10.*siconc)] = 2

    area = grid_area(icedata)[miz == 1].sum()    

    return(miz, area)

#=====================================================================
def calc_MIZ(icedata,configs):

    mizmethod=[i for i in configs['MIZmethod'] if configs['MIZmethod'][i]==True][0]

    if configs['MIZmethod']['Ltraditional'] == True:
       miz, mize = traditional_MIZ(icedata,configs)
    elif configs['MIZmethod']['Ldynamical'] == True:
       miz, mize = dynamical_MIZ(icedata,configs)
       
    return(miz,mize)
    
#=====================================================================
if __name__ == "__main__":
    # If this script is called directly without MIZengine_NOCOS-py, do everything necessary using config from config_MIZcalc.yml
    from read_config import read_configfile
    from read_ice_data import read_ice_data
    from save_MIZ_toNetCDF import save_toNetcdf
    
    configs=read_configfile('METROMS_obs')
    icedata=read_ice_data(configs)
    miz = calc_MIZ(icedata,configs)
    save_toNetcdf(miz,icedata,configs)    

