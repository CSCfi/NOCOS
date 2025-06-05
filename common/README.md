# Common Tools

This directory contains shared tools and modules for accessing Climate DT sea ice data.  
Reusable functions for data loading, processing, and visualization are developed here to aid various use cases within the NOCOS DT project.


For more information how to acess ClimateDT data via local or remote machine or using various platforms [visit NOCOS internal webpage](https://wiki.eduuni.fi/spaces/cscRDIcollaboration/pages/539865523/Accessing+Climate+DT+data+instructions+for+NOCOS+DT).

## ClimateDT  database
See [climate DT cataloguew](https://climate-catalogue.lumi.apps.dte.destination-earth.eu/?root=root)

## Access to the Destination Earth databases
To begin  request access to DESP  see [README_desp](README_desp.md).

## Metadata Requests

To explore and request available metadata (such as available variables, temporal coverage, and spatial domains) from the Climate DT datasets, use the provided metadata tools.

- Example script: [metadata_request.py](#) <!-- Replace # with actual path -->
- Usage instructions are included within the script.

## Downloading Data

Download sea ice data from the Climate DT data services using the dedicated download script.  
You can specify the desired region, variables, and time period.

- Example script: [download_data.py](#) <!-- Replace # with actual path -->
- See the script’s documentation or help message for command-line options.

## Visualizing the Data

After downloading, you can use the visualization tools to quickly plot and analyze sea ice fields, time series, or derived products.

- Example script: [visualize_data.py](#) <!-- Replace # with actual path -->
- Example notebooks: [visualization_demo.ipynb](#) <!-- Replace # with actual path -->

These scripts and notebooks provide example workflows for generating maps, time series, and other plots from Climate DT datasets.




---
Back to [NOCOS github front page](../README.md).

For more information about NOCOS project, see the [NOCOS webpage](https://wiki.eduuni.fi/spaces/CSCNOCOS/pages/480353786/Nordic+Cryosphere+Digital+Twin).
