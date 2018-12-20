[![PyPI](https://img.shields.io/badge/python-3.6-yellow.svg)]()
[![license](https://img.shields.io/github/license/khider/ClimComp.svg)]()
[![Version](https://img.shields.io/github/release/khider/ClimComp.svg)]()

# ClimComp

**Python code for comparing the seasonal prediction with the average climatology**

This code is written for the MINT project.

**Table of contents**

* [What is it?](#what)
* [Version Information](#version)
* [Quickstart Guide](#quickstart)
* [Requirements](#req)
* [Files in this repository](#files)
* [Contact](#contact)
* [License](#license)

## <a name = "what">What is it?</a>

CompClim is a simple Python routine to calculate climatology from various datasets stored in netCDF format.

## <a name = "version"> Version information </a>
0.0.1: Initial release with function to deal with FLDAS datasets

## <a name ="quickstart"> Quickstart guide </a>
This routine is meant to be executed from the command line:

`python ClimComp.py path dataset_source flagP min_lon max_lon min_lat max_lat min_month max_month year`

where:
* dataset_source (str): The source of the dataset.Possible values include 'FLDAS'   
* path (str): The path to the directory containing the netCDF files  
* flagP (str): Name of the variable of interest as declared in the file  
* min_lon (float): Minimum longitude for the bounding box  
* max_lon (float): Maximum longitude for the bounding box  
* min_lat (float): Minimum latitude for the bounding box  
* max_lat (float): Maximum latitude for the bounding box  
* min_month (int): The first month of the season of interest  
* max_month (int): The last month of the season of interest  
* year (int): The year of interest for the comparison

*Example:*

`python ClimComp.py '/Users/deborahkhider/Documents/MINT/Climate/MonthlyDatasets' FLDAS Rainf_f_tavg 32 36 13 17 6 8 2017`

## <a name="req">Requirements</a>

### Software requirements
Current version tested under Python 3.6 with the following dependencies.

- xarray v0.11.0
- numpy v1.15.0
- pandas v0.23.4
- glob2 v 0.6

### Data Requirements

This routine assumes that the data is stored as per FLDAS netCDF format and file organization. This makes use of monthly data **ONLY**. 

## <a name = "files">Files in this repository</a>
 - README.md: this files. Instructions and other requirements
 - LICENSE: License Information
 - ClimComp.py: Main routine, executable from the command line (see [Quickstart](#quickstart))
 - climatology.csv: Sample output file that contains the average for each year
 - summary.txt: Sample output file that contains the climatology for the year of interest

## <a name = "contact"> Contact </a>

Please report issues to <khider@usc.edu>

## <a name ="license"> License </a>

The project is licensed under the GNU Public License. Please refer to the file call license.
