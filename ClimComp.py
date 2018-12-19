#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 18 17:28:49 2018

@author: deborahkhider

Calculate the climatology
"""

import sys
import xarray as xr
import numpy as np
import os
import glob
import pandas as pd

def startup(dataset_source, path, flagP, min_lon, max_lon,\
               min_lat, max_lat,min_month,max_month,year):
    '''Calls the righ method for dataset_source
   
    Args:
        dataset_source (str): The source of the dataset. 
            Possible values include 'FLDAS' 
        path (str): The path to the directory containing the netCDF files
        flagP (str): Name of the variable of interest as declared in the file
        min_lon (float): Minimum longitude for the bounding box
        max_lon (float): Maximum longitude for the bounding box
        min_lat (float): Minimum latitude for the bounding box
        max_lat (float): Maximum latitude for the bounding box
        min_month (int): The first month of the season of interest
        max_month (int): The last month of the season of interest
        year (int): The year of interest for the comparison       
    '''
    
    # First make a few assertions to make sure that everything works
    assert min_lon<max_lon, "Maximum longitude smaller than minimum longitude"
    assert min_lat<max_lat, "Maximum latitude smaller than minimum latitude"
    assert min_month<max_month, "Maximum month smaller than minimum month"

    if dataset_source == 'FLDAS':
        clim_FLDAS(path, flagP, min_lon, max_lon,\
               min_lat, max_lat,min_month,max_month,year)
    else:
        sys.exit('Method to analyze dataset is not available')

def clim_FLDAS(path, flagP, min_lon, max_lon,\
               min_lat, max_lat,min_month,max_month,year):
    '''Calculate climatology for the FLDAS data
    
    This function takes the seasonal average over several years 
    to estimate the climatology and deviation for a specipic year.
    Works only for FLDAS monthly datasets.
    
    Args:
        path (str): The path to the directory containing the netCDF files
        flagP (str): Name of the variable of interest as declared in the file
        min_lon (float): Minimum longitude for the bounding box
        max_lon (float): Maximum longitude for the bounding box
        min_lat (float): Minimum latitude for the bounding box
        max_lat (float): Maximum latitude for the bounding box
        min_month (int): The first month of the season of interest
        max_month (int): The last month of the season of interest
        year (int): The year of interest for the comparison    
            
    Returns:
        'climatology.csv': The average for all years
        'summary.txt': The probability for a specific year 
    '''

    # Get the name of all the netCDF file in the directory
    # Assumes that the files are organized as per the FLDAS
    # datasets.
    subdirs = [os.path.join(path, o) for o in os.listdir(path) 
                        if os.path.isdir(os.path.join(path,o))]
    
    nc_files= []
    
    for d in subdirs:
        files = glob.glob(d+'/*.nc')
        for file in files:
            nc_files.append(file)
            
    if not nc_files:
        sys.exit('No available datasets')        
    
    # Go through the files and make calculations
    years = []
    months = []
    P = []
    season = np.arange(min_month,max_month+1,1)
    for file in nc_files:
        nc_fid = xr.open_dataset(file)
        time = nc_fid.coords['time'].values[0]
        month = time.astype('datetime64[M]').astype(int) % 12 + 1
        if month in season:
            lon = nc_fid.coords['X'].values
            lat = nc_fid.coords['Y'].values
            # Make sure that there is something to bound
            assert min_lat<np.max(lat), "Minimum latitude out of range"
            assert max_lat>np.min(lat), "Maximum latitude out of range"
            assert min_lon<np.max(lon), "Minimum longitude out of range"
            assert max_lon>np.min(lon), "Maximum longitude out of range"

            # Get the bounding box indices
            idx_x = np.arange(np.where(lon>min_lon)[0][0],\
                              np.where(lon<max_lon)[0][-1],1)
            
            idx_y = np.arange(np.where(lat>min_lat)[0][0],\
                              np.where(lat<max_lat)[0][-1],1)
            
            # Make sure the variable is in the file
            assert flagP in nc_fid, 'Variable not in dataset.'
            # Grab the appropriate data
            data_temp = nc_fid[flagP].values[:,idx_y,:]
            data = data_temp[:,:,idx_x]
            # Take the average
            P.append(np.mean(data))
            # Get the time
            years.append(time.astype('datetime64[Y]').astype(int) + 1970)
            months.append(time.astype('datetime64[M]').astype(int) % 12 + 1)
            nc_fid.close()
        else:
            nc_fid.close()
        
    # Place the data into a dataframe
    dt = pd.DataFrame({'Years':years,'Months':months,'Data':P})
    # Take the average for each year
    dt_mean = pd.DataFrame({'Years':dt['Years'].unique(),
            'Data': dt.groupby(['Years'])['Data'].transform('mean').unique()})
        
    # Write as csv file
    cwd = os.getcwd()
    dt_mean.to_csv(cwd+'/climatology.csv', sep =',')   
    
    # Calculate the probability of rain that year
    val = np.float(dt_mean[dt_mean['Years']==year]['Data'])
    # Order the Data column
    prob = dt_mean[dt_mean['Data']<val]['Data'].count()/dt_mean['Data'].count()
    # Write this out in a file
    f = open(cwd+"/summary.txt", "w")
    f.write('The probability of having a year with more '+\
            flagP +' than the '+str(year)+' year is '+str(prob*100)+\
            '%.')
    f.close()

#%% Main
path = sys.argv[1]
dataset_source = sys.argv[2]
flagP = sys.argv[3]
min_lon = float(sys.argv[4])
max_lon = float(sys.argv[5])
min_lat = float(sys.argv[6])
max_lat = float(sys.argv[7])
min_month = int(sys.argv[8])
max_month = int(sys.argv[9])
year = int(sys.argv[10])

startup(dataset_source, path, flagP, min_lon, max_lon,\
               min_lat, max_lat,min_month,max_month,year)