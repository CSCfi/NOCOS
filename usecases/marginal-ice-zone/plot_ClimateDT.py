
plotavg=False
saveplot=True

import os
import numpy as np
import pandas as pd
import earthkit.data
import earthkit.plots
import earthkit.regrid
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from read_config import read_configfile

#=====================================================================
dataSource = 'ClimateDT'

# Read config file
configs=read_configfile(dataSource)

datasets = ['ICON_historical', 'ICON_future', 'IFS-NEMO_future']
legends = ['ICON_2010-2019', 'ICON_2030-2039', 'IFS-NEMO_2030-2039']
line_types = ['r-', 'r--', 'b--']


x       = np.arange(1,13)
stats   = ['MIZE', 'MEAN_LAT']
ylabels = ['MIZE ($10^6 km^2$)', 'mean_Latitude (' + u"\u00b0" +' N)']
texts   = ['(a)', '(b)']
 
mean_ext = np.zeros(12)
mean_lat = np.zeros(12)

#=====================================================================
fig, ax = plt.subplots(2,sharex=True,figsize=(10,5))

for k in range(len(datasets)):
    dataset = datasets[k]
    fname = configs['output']['output_folder'] + '/' + dataset + '_stats.txt'
    data = np.loadtxt(fname)
    date, ext, lat = data[:,0].astype(int), data[:,1], data[:,2]

    for j in range(1,13):
        i = date % 100
        mean_ext[j-1] = np.nanmean(ext[i == j]) * 1.0e-6
        mean_lat[j-1] = np.nanmean(lat[i == j])
        
    ax[0].plot(x,mean_ext,line_types[k],linewidth=2,label=legends[k])
    ax[0].set_xticks(x)
    ax[0].set_ylabel(ylabels[0]) 
    ax[0].grid(False)
    ax[0].legend(ncol=1,loc=2)
    #ax[0].set_xlim(1,12)
    ax[0].text(0.95, 0.85, texts[0], transform=ax[0].transAxes,fontsize=12)

    ax[1].plot(x,mean_lat,line_types[k],linewidth=2,label=legends[k])
    ax[1].set_xticks(x)
    ax[1].set_ylabel(ylabels[1]) 
    ax[1].grid(False)
    #ax[1].set_xlim(1,12)
    ax[1].text(0.95, 0.85, texts[1], transform=ax[1].transAxes,fontsize=12)
    ax[1].legend(ncol=1,loc=2)
    #ax[1].set_xticklabels(['Jan','Apr','Jul','Oct'])
    ax[1].set_xlabel('Month')

#plt.show()

fout = configs['output']['output_folder'] + '/MIZ_stats.png'
plt.savefig(fout,bbox_inches='tight',dpi=100)


