# Use case: Discrete element model based sea ice model development

## Description

Traditionally, sea ice dynamics have been modeled using continuum-based methods such as finite-element or finite-difference schemes. The NOCOS-DT project introduces a high-resolution Discrete Element Model (DEM) approach to better capture sea ice behavior at sub-kilometer scales, where continuum models become unreliable due to the multifractal nature of ice dynamics—evidenced by ship-radar observations. To address the computational intensity of DEM, we developed the HiDEM code, a GPU-optimized simulation tool written in CUDA and HIP, capable of modeling sea ice at 0.5-meter spatial and millisecond temporal resolution across large areas. Initially designed for studying brittle fragmentation and glacier calving, HiDEM now enables realistic simulations of sea ice interactions with infrastructure such as wind power pylons.


## Overview 

![Overview image](image/HiDEM_poster.png)

## Models and data

The Discrete Element Model HiDEM is modified for sea ice simulations. The code adapts boundary conditions, driving forces, and bathymetry according to user-provided input data.

---

Back to the [NOCOS DT GitHub front page](../../README.md).  

For more information about the NOCOS DT project, see the [NOCOS DT website](https://wiki.eduuni.fi/x/_p2hH).
