#!/bin/bash

for filebase in fasticeclimatology_March_2010-2019_ICON-historical fasticeclimatology_March_2030-2039_ICON-future
do
		# Merge Inglefield plot into Greenland plot
		convert ${filebase}_Greenland.png ${filebase}_Inglefield.png -gravity Center -geometry 256x256+70+5 -composite tmp.png
		# Add a rectangle around Inglefield fjord in Greenland plot
		convert tmp.png -fill none -stroke black -strokewidth 1.5 -draw 'rotate 30 rectangle 280,65 360,120' ${filebase}_GreenlandAndInglefield.png
		rm tmp.png
done



