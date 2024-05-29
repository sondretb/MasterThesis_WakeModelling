# Sondre Bungum Master thesis source code
This is the source code for the plots and case study featured in:
### "Integrating SCADA Data and Kinematic Wake Modeling for Enhanced Control Optimization in Offshore Wind Farms: A Study of Hybrid Modeling Solutions using Kinematic Wake Models and SCADA Data"

## Pre-requisites
**_requirements.txt_** contains a list of the libraries used. To download all modules, do "pip install -r requirements.txt" in the directory.\
**_.env.example_** contains a template for the .env file, which contains the environmental variables that were used to obtain the source data from Equinor. This data will not be publicly available.

## Python Notebooks
The notebooks provide the code used to generate the plots for the case study. 

**_pre_data_analysis.ipynb_** was used for the "preliminary data analysis" of the case study.\
_**power_predictior.ipynb**_ was used to visualise the "power curve modelling" part of the case study.\
**_wake_deficit_optimization.ipynb_** was used to execute the "wake deficit model optimization" part of the case study.
## Python Scripts

_**demo.py**_ is a script made to visualize the different kinematic models, layout, and flowfields in DOW. These plots were used in the "Theory" part of the thesis.\
**_download_files.py_** is a script made to fetch and download the source data provided by Equinor from Azure.\
_**generate_TI_set.py**_ is a script that generates the simulated effective TI dataset that was used in the case study.

## Python Modules

_**dudgeon.py**_ provides the layout of DOW and the names of the turbines.\
_**swt6.py**_  provides the WindTubine object specific to DOW, with the improvised ct and power curve.\
_**data_filter.py**_  provides the data filtering included in the data preprocessing for the case study.\
_**wake_estimator.py**_ provides the estimator object that was evaluated for the wake deficit model optimization part of the case study.\
_**util.py**_ includes help functions that were used throughout the project.
