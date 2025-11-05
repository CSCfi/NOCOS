#!/bin/bash

# This script can be used to remap the output of download_ClimateDT-for-icebergdrift.py
# from healpix grid onto a regular lat/lon grid. 
#
# 1) Choose one of the pre-definied domains, BaffinLabra or CoburgLabra. Grid information
#    will be read from griddes_BaffinLabra.txt and griddes_CoburgLabra.txt, respectively.
# 2) Define the input directory (rawdatdir) where the output of
#    download_ClimateDT-for-icebergdrift.py is located.
# 3) The script will treat all files *${domain}*_healpix.nc in the input directory.
#    It will create the remapped files in the same place and move the original
#    files into a subdirectoy called "healpix".
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

# The domain
#domain=BaffinLabra
domain=CoburgLabra

# Directory with input data (on healpix grid)
rawdatdir=/tmp/

#####################


mkdir -p ${rawdatdir}/healpix/

for filename in ${rawdatdir}/*${domain}*_healpix.nc
do
	outname=${filename/_healpix.nc/_orivarnames.nc}
	echo Remapping $filename to $outname ...
	cdo remapdis,griddes_${domain}.txt  $filename $outname 
	echo Moving $filename to ${rawdatdir}/healpix/
	mv $filename ${rawdatdir}/healpix/
done

