#!/bin/bash

# Script to merge the Inglefield plot into the Greenland plot

#    Author, copyright and license
#    -----------------------------
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



for filebase in iceparameters/climatology-siconc_March_2010-2019_ICON-historical iceparameters/climatology-siconc_March_2030-2039_ICON-future
#for filebase in fasticeclimatology_March_2010-2019_ICON-historical fasticeclimatology_March_2030-2039_ICON-future
#for filebase in  fasticeclimatology_March_2010-2019_icecharts
do
		# Merge Inglefield plot into Greenland plot
		#small font size: convert ${filebase}_Greenland.png ${filebase}_Inglefield.png -gravity Center -geometry 256x256+70+5 -composite tmp.png
		convert ${filebase}_Greenland.png ${filebase}_Inglefield.png -gravity Center -geometry 254x254+85+5 -composite tmp.png
		# Add a rectangle around Inglefield fjord in Greenland plot
		# small font size: convert tmp.png -fill none -stroke black -strokewidth 1.5 -draw 'rotate 30 rectangle 280,65 360,120' ${filebase}_GreenlandAndInglefield.png
		convert tmp.png -fill none -stroke black -strokewidth 1.5 -draw 'rotate 30 rectangle 295,45 371,96' ${filebase}_GreenlandAndInglefield.png # upper left corner (x,y) lower right corner (x,y)
		rm tmp.png
done



