#!/bin/bash

# This script can be used to set the attribute "standard_name" of the
# variables from ClimateDT (as retrieved by download_ClimateDT-for-icebergdrift.py)
# to the standard names, that are required by OpenDrift.
#
# 1) Define the input directory (indatdir) where the output of
#    step2_remap-to-latlon.sh is located.
# 2) The script will treat all files *${domain}*_orivarnames.nc in the input directory.
#    It will create files with corrected attributes in the same place and move
#    the original files into a subdirectoy called "orivarnames".
# 3) The output will be saved into the directory speficied as 'outdir'.
#
# 
#    Author, copyright and license
#    #############################
#
#    Author: Andrea Gierisch, DMI
#    
#    Copyright 2025 CSC – IT Center for Science (CSC),
#                   Danish Meteorological Institute (DMI),
#                   Finnish Meteorological Institute (FMI),
#                   Norwegian Meteorological Institute (MetNo),
#                   Swedish Meteorological and Hydrological Institute (SMHI),
#                   Tallinn University of Technology (TalTech).
#    
#       Licensed under the Apache License, Version 2.0 (the "License");
#       you may not use this file except in compliance with the License.
#       You may obtain a copy of the License at
#    
#           http://www.apache.org/licenses/LICENSE-2.0
#    
#       Unless required by applicable law or agreed to in writing, software
#       distributed under the License is distributed on an "AS IS" BASIS,
#       WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#       See the License for the specific language governing permissions and
#       limitations under the License.
#    
#    License: Apache-2.0
#    

## User settings
#####################

indatdir=/tmp/
outdir=./readydata/

#####################

mkdir -p ${indatdir}/orivarnames/
mkdir -p $outdir

for levtype in sfc o2d o3d
do
	for filename in ${indatdir}/*${levtype}_orivarnames.nc
	do
		outname=${filename/_orivarnames.nc/.nc}
		echo Setting variables names from $filename to $outname ...

		if [[ "$levtype" == "o3d" ]]
		then
			echo o3d
			ncatted -a standard_name,avg_uoe,o,c,eastward_sea_water_velocity  -a standard_name,avg_von,o,c,northward_sea_water_velocity -a standard_name,avg_thetao,o,c,sea_water_potential_temperature -a standard_name,avg_so,o,c,sea_water_salinity  $filename  $outname 
		elif [[ "$levtype" == "sfc" ]]
		then
			echo sfc
			ncatted -a standard_name,\10u,o,c,x_wind -a standard_name,\10v,o,c,y_wind  $filename  $outname 
		
		elif [[ "$levtype" == "o2d" ]]
		then
			echo o2d
			ncatted -a standard_name,avg_siconc,o,c,sea_ice_area_fraction -a standard_name,avg_sithick,o,c,sea_ice_thickness -a standard_name,avg_siue,o,c,sea_ice_x_velocity -a standard_name,avg_sivn,o,c,sea_ice_y_velocity $filename  $outname 

		else
			echo "ERROR: Only implemented for levtype o3d, sfc and o2d. Not for: $levtype"
			exit 1
		fi

		echo Moving $filename to ${indatdir}/orivarnames/
		mv $filename ${indatdir}/orivarnames/
		echo Moving result to $outdir
		mv $outname $outdir
	done # file
done # levtype


