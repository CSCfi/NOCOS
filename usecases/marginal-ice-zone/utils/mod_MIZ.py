#===============================================================================
#
# author: Keguang Wang, Norwegian Meteorological Institute
# 20 Jan. 2025
#
#===============================================================================

import numpy as np
import cartopy.crs as ccrs
import matplotlib.colors as colors
from matplotlib import pyplot as plt
from matplotlib.colors import BoundaryNorm

levels = np.array([0, 0.1, 0.85, 1.0])
cl = ['#8bb5d9','#fcff42',[1.,0.,0.]]
cmap = colors.ListedColormap(cl,"", len(cl))
cmap = colors.LinearSegmentedColormap.from_list('',cl)
norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)

#===============================================================================
def plot_mizt(sic,src='NIC',area='Arctic'):
    # plot traditional marginal ice zones

    if area == 'Barents':
       plt.figure(figsize=[6,10])
       subplot_kws=dict(projection=ccrs.LambertConformal(central_longitude=-25.0,
                central_latitude=77.5),facecolor='grey')
    else:
       plt.figure(figsize=[12,8])
       subplot_kws=dict(projection=ccrs.NorthPolarStereo(central_longitude=0.0),
                 facecolor='grey')

    p = sic.plot(x='longitude', y='latitude',
#                  vmin=-2, vmax=12,
                  cmap=cmap,
                  norm=norm,
#                  levels=4,
                  subplot_kws=subplot_kws,
                  transform=ccrs.PlateCarree(),
                  add_labels=False,
                  add_colorbar=False)

    try:
       plt.title(src + ' traditional MIZ on ' + str(sic.time.values)[:10])
    except:
       plt.title(src + 'traditional MIZ on ' + str(sic.time.values[0])[:10])
    
    # add separate colorbar
    if area == 'Barents':
       cb = plt.colorbar(p, ticks=[0.05, 0.475, 0.925], shrink=0.5)
       p.axes.set_extent([-13, 50, 68, 82], ccrs.PlateCarree())
    else:
       cb = plt.colorbar(p, ticks=[0.05, 0.475, 0.925], shrink=0.99)
       p.axes.set_extent([-180, 180, 55, 90], ccrs.PlateCarree())

    cb.ax.set_yticklabels(['Open water','Traditional MIZ','Dense pack ice'],
                          rotation=90,va='center')
    cb.ax.tick_params(labelsize=12)

    p.axes.stock_img()
    p.axes.gridlines(color='black', alpha=0.5, linestyle='--')

    out_dir = '/home/jovyan/my_env/figs/'
    fout = out_dir + 'MIZt_' src + '_' + str(sic.time.values)[:10] + '.png'
    plt.savefig(fout,bbox_inches='tight',dpi=100)

#===============================================================================
def plot_mizd(sic,sit,src='NIC',area='Arctic'):
    # plot traditional marginal ice zones

    sit1 = sit/(sic + 1.0e-10)
    sic1 = sic.copy()
    
    sic = sic.where(~((sic1 >= 0.1) & (sic1 <= 0.85) & (sit1 <= 2.0)), 0.5)
    sic = sic.where(~((sic1 > 0.85) & (sit1 <= 10.5 - 10.*sic1)), 0.5)

    if area == 'Barents':
       plt.figure(figsize=[8,10])
       subplot_kws=dict(projection=ccrs.LambertConformal(central_longitude=-25.0,
                central_latitude=77.5),facecolor='grey')
    else:
       plt.figure(figsize=[12,8])
       subplot_kws=dict(projection=ccrs.NorthPolarStereo(central_longitude=-45.0),
                 facecolor='grey')

    p = sic.plot(x='longitude', y='latitude',
#                  vmin=-2, vmax=12,
                  cmap=cmap,
                  norm=norm,
#                  levels=4,
                  subplot_kws=subplot_kws,
                  transform=ccrs.PlateCarree(),
                  add_labels=False,
                  add_colorbar=False)
    try:
       plt.title(src + ' dynamical MIZ on ' + str(sic.time.values)[:10])
    except:
       plt.title(src + 'dynamical MIZ on ' + str(sic.time.values[0])[:10])
    
    # add separate colorbar
    if area == 'Barents':
       cb = plt.colorbar(p, ticks=[0.05, 0.475, 0.925], shrink=0.55)
       p.axes.set_extent([-13, 50, 68, 82], ccrs.PlateCarree())
    else:
       cb = plt.colorbar(p, ticks=[0.05, 0.475, 0.925], shrink=0.99)
       p.axes.set_extent([-180, 180, 55, 90], ccrs.PlateCarree())

    cb.ax.set_yticklabels(['Open water','Dynamical MIZ','Dense pack ice'],
                          rotation=90,va='center')
    cb.ax.tick_params(labelsize=12)

    p.axes.stock_img()
    p.axes.gridlines(color='black', alpha=0.5, linestyle='--')

    out_dir = '/home/jovyan/my_env/figs/'
    fout = out_dir + 'MIZd_' + src + str(sic.time.values)[:10] + '.png'
    plt.savefig(fout,bbox_inches='tight',dpi=100)

