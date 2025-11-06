# Use Case: Iceberg Drift

## Description

Here we showcase how the model output of Climate DT simulations can be used as forcing data for 
a model that simulates the drift of icebergs. Icebergs are for example important for
distributing freshwater in the ocean but they also pose risks for shipping. Therefore, it is
valuable to investigate whether the drift patters of icebergs might change in a future climate.

The Climate Adaptation Digital Twin simulations (Climate DT) feature high spatial resolution and
are therefore a useful dataset for assessing iceberg drift.

## The Iceberg Drift Model

This usecase provides scripts to download and prepare ClimateDT data as input/forcing
for the drift model OpenDrift/OpenBerg. This model is described here:
https://opendrift.github.io/
And can be downloaded here:
https://github.com/OpenDrift/opendrift

## Technical Description

This use case demonstrates how forcing data for OpenDrift can be
    a) downloaded through Polytope from ClimateDT
    b) pre-processed to yield input data for OpenDrift.

Following variables are processed:
  - 10--m wind velocities: 10u, 10v (6-hourly)
  - surface ocean currents: avg_uoe, avg_von (daily)
  - surface water temperature and salinity: avg_thetao, avg_so (daily)
  - sea ice drift: avg_siue, avg_sivn (daily)
  - sea ice concentration and thickness: avg_siconc, avg_sithick (daily)

> [!NOTE]
> Be aware that currently (as of October 2025) no depth information of subsurface ocean currents seems accessible from ClimateDT simulations. Hence, the script downloads only surface currents (level=1).

## Software Description

### Description of files

<!-- List and link the main scripts, notebooks, and tools used in this use case -->
1) [download_ClimateDT-for-icebergdrift.py](download_ClimateDT-for-icebergdrift.py) – Downloads relevant parameters from ClimateDT on healpix grid and saves the output as NetCDF files.
- [step2_remap-to-latlon.sh](step2_remap-to-latlon.sh) – Bash script for remapping NetCDF files from healpix grid to regular lat/lon grid.
- [griddescriptions/](griddescriptions/) – Grid description files used by cdo (in step2) to remap from healpix grid to a regular lat/lon grid.
- [step3_set_standardnames.sh](step3_set_standardnames.sh) – Bash script for assigning proper attributes to the variables. This is required by OpenDrift to automatically detect the variables.

### Requirements for additional software

The Python code provided in this usecase does not require any additional Python packages. It is sufficient to install the packages listed in Polytope's [environment.yml](https://github.com/destination-earth-digital-twins/polytope-examples/blob/868ddbde5139a448ac94e937cd12ec8fe258219b/environment.yml) file.

The bash scripts require `cdo` and `nco` (`ncatted`).

---

## Footer

Back to [NOCOS github front page](../../README.md).  
For more information about NOCOS project, see the [NOCOS webpage](https://wiki.eduuni.fi/spaces/CSCNOCOS/pages/480353786/Nordic+Cryosphere+Digital+Twin).
