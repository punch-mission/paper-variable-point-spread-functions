# "Coma Off It: Removing Variable Point Spread Functions from Astronomical Images" by Hughes et al.
[![DOI](https://zenodo.org/badge/573548130.svg)](https://zenodo.org/badge/latestdoi/573548130)

Code to accompany "Coma Off It: Removing Variable Point Spread Functions from Astronomical Images" by Hughes et al.

## Notebooks
The notebooks provided in the `notebooks` directory recreate all of the figures in the paper. 

### One-dimensional theory example
Figure 1 of the paper is generated in `notebooks/8-panel-theory.ipynb`. 

### Models

There are three demos from the paper in this repository
#### 1. Model data
This is fake data. Simply run all cells in `notebooks/model-data.ipynb`. 
The resulting figure is `figures/mode.png`

#### 2. PUNCH data
TODO: The data used for this still needs to be uploaded. 

#### 3. DASH data
First run `scripts/correct_dash.py`. Then to generate figures run `notebooks/dash.ipynb`. 
This will generate the figure `figures/dash.png`.