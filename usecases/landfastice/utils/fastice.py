def avg_fasticecoverage(dataICE,speedthreshold=5e-4,fasticeduration=4):
    """Calculate average landfast ice coverage.

    This function determines for each grid cell (vector/healpix) the fraction of time (days) 
    that this grid cell is covered by landfast ice during the provided time period. 
    Procedure: 
    1) For each day, determine whether the ice is 'stationary':
       * ice drift speed < speedthreshold (default 5e-4 m/s) 
       * AND SIC > 90% 
       [Number of time steps = number of days in input dataset]
    2) A grid cell is considered fastice (true/false) if the ice
       has been 'stationary' for at least n days in a row (default 4 days).
       [Number of time steps = number of days in input dataset - fasticeduration - 1]
    3) Calculate time average of over the given time period
       [Number of time steps = 1]
    Result:
    Average fastice coverage of the given time period (e.g. 1 month)
       
    Assumptions about input data dataICE:
    - grb object retrieved from Polytope
    - 3 fields per day, provided in this order: 
       * daily average sea ice concentration (avg_siconc)
       * daily average ice drift speed u-component (avg_siue)
       * daily average ice drift speed v-component (avg_sivn)
    - number of daily fields available in dateICE must be greater or equal fasticeduration.
      (fasticeduration is the number of days for which the ice needs to be 'stationary' in order to be considered fast ice.)
    - continuous daily time series without gaps

    Parameters
    ----------
    dataICE : grb-object
        Dataset from Polytope, including the parameters:
        avg_siconc, avg_siue, and avg_sivn for several days
    speedthreshold : float , optional
        Daily mean ice drift speed must be below this limit for the ice to be considered 'stationary'.
        Default: 5e-4 m/s
    fasticeduration : int, optional
        For how many days in a row the ice needs to be 'stationary' in order to be considered fastice.
        Default: 4 days

    Returns
    -------
    grb-object
        avg_fasticecover_grb: Field with values between 0 and 1 indicating the percentage of time 
        that the respective grid cell is covered by fastice during the given time period. 


    Author, copyright and license
    -----------------------------
    
    Author: Andrea Gierisch, DMI
    
    Copyright 2025 CSC – IT Center for Science (CSC),
                   Danish Meteorological Institute (DMI),
                   Finnish Meteorological Institute (FMI),
                   Norwegian Meteorological Institute (MetNo),
                   Swedish Meteorological and Hydrological Institute (SMHI),
                   Tallinn University of Technology (TalTech).
    
       Licensed under the Apache License, Version 2.0 (the "License");
       you may not use this file except in compliance with the License.
       You may obtain a copy of the License at
    
           http://www.apache.org/licenses/LICENSE-2.0
    
       Unless required by applicable law or agreed to in writing, software
       distributed under the License is distributed on an "AS IS" BASIS,
       WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
       See the License for the specific language governing permissions and
       limitations under the License.
    
    License: Apache-2.0


    """

    ##### Extract data from grib object

    siconc=dataICE[0::3].values
    siu=dataICE[1::3].values
    siv=dataICE[2::3].values

    ##### Calculate drift speed

    import numpy as np
    speed=np.sqrt(siu**2+siv**2)

    ##### Calculate areas covered by fast ice"

    canvaswithland=speed.copy()
    fasticemask=np.logical_and(np.less(speed,speedthreshold),np.greater(siconc,0.90)) # True where speed<5e-4 and SIC>90%
    landmask=np.isnan(canvaswithland)
    watermask=np.logical_and(np.logical_not(landmask),np.logical_not(fasticemask))
    canvaswithland[watermask]=0.
    canvaswithland[fasticemask]=1. # e.g.: Number of time stamps = number of days in month + fasticeduration

    #### Recursive function to determine where there is fastice for daysN in a row
    def fastice_for_x_days(fasticeN,daysN):
        # shape of fasticeN: [days,healpixcells]
        if daysN==1:
            return fasticeN
        else:
            # fasticeNm1=np.logical_and(fasticeN[0:-1,:],fasticeN[1:,:]) # Has there been fastice today and yesterday?
            fasticeNm1=(np.logical_and(fasticeN[0:-1],fasticeN[1:])).astype('float') # Has there been fastice today and yesterday? # float is needed for keeping NaN on land.
            nanmask=np.logical_and(np.isnan(fasticeN[0:-1]),np.isnan(fasticeN[1:]))
            fasticeNm1[nanmask]=np.nan
            daysNm1=daysN - 1
            return fastice_for_x_days(fasticeNm1,daysNm1) # Call again for one day less

    fasticedata=fastice_for_x_days(canvaswithland,fasticeduration) # e.g.: Number of time stamps = number of days in month"

    ### Averaging over all days
    avg_fasticecover_numpy=np.mean(fasticedata[:,:],axis=0)      # average over time -> percentage of fast ice coverage over time
    centertimestep=fasticeduration-1+int(fasticedata.shape[0]/2) # Number of day in dataICE representing mid of the month
    centertimestepidx=centertimestep*3                           # Index in dataICE representing mid of the month
    avg_fasticecover_grb=dataICE[centertimestepidx].clone(values=avg_fasticecover_numpy, name="Avg. fast ice coverage", shortName="fastice", units="") # Check metadata with e.g.: avg_fasticecover_grb.metadata("name")

    return avg_fasticecover_grb

