"""
Created on Wed Sep 25 16:39:22 2024

Script for plotting full data saved after main.py runs sucessfully.
    - Includes two options in code blocks for single or multi axis plots
    - Saves to high def png

Can run this any time csv file of readings exists!
Test with test_data.csv

@author: brutal_blondie
"""
#----------------------------------------------------------
# IMPORTS
#----------------------------------------------------------
import time
import numpy as np
import pandas as pd
import csv
import matplotlib
import matplotlib.pyplot as plt
my_colors = ['#00C5CD','#FF0000', '#32CD32', '#8B8989','#00EE00'] 

#----------------------------------------------------------
# USER VARIABLES
# Input plot variables here
#----------------------------------------------------------
plot_name = 'run1' # name to keep track of plots

DATA_ROOT = 'MagneticCapacitive_recordings.csv' # path to data file to plot
OUT_ROOT = 'output/' # path to save figure to

# TODO! The following variables are manual for now - 
# Eventually need way to get true enc_name1, enc_name2 from user input into this script?
enc_name1 = 'Magnetic' 
enc_name2 = 'Capacitive'

#----------------------------------------------------------
# DATA CLEANING
# Deals with csv to dataframe 
#----------------------------------------------------------
# read csv and clean
df = pd.read_csv(DATA_ROOT, sep = ',')
df.columns = ['t1', 'enc_1', 't2', 'enc_2']
df['t1'] = pd.to_datetime(df['t1'], unit='s')
df['t2'] = pd.to_datetime(df['t2'], unit='s')

# get times
t1_start = df['t1'].iloc[0]
t1_end = df['t1'].iloc[-1]
t1_time = t1_end-t1_start

t2_start = df['t2'].iloc[0]
t2_end = df['t2'].iloc[-1]
t2_time = t2_end-t2_start
#%%
#----------------------------------------------------------
# PLOT 1 - SINGLE PLOT
#----------------------------------------------------------
'''Plots both signals onto same plot'''

fig, ax = plt.subplots(1,1,figsize=[6,4])

df.plot(x = 't1',
        y = ['enc_1', 'enc_2'],
        label = [enc_name1, enc_name2],
        style = '-',
        lw = 1,
        ax = ax, 
        color = my_colors)

# axis config
ax.set_title('Encoder Reading Plots: Elapsed Time = %s sec'%t1_time.total_seconds()) # NOTE! Just chosing one time reading since usually similar
ax.ticklabel_format(axis ='y', style = 'sci', scilimits=(0,0))
#ax.set_xlim(xmin,xmax)
ax.set_ylim(0,None)
ax.set_xlabel('Time [sec]')
ax.set_ylabel('Encoder Readings')
ax.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')   

# save fig in high def
plt.savefig(OUT_ROOT + plot_name + '.png', dpi=300, bbox_inches="tight")
    
    
#%%
#----------------------------------------------------------
# PLOT 2 - MULTI PLOT
#----------------------------------------------------------
'''Plots to two multiplots in same fig.'''
fig, (ax1,ax2) = plt.subplots(1,2,figsize=[10,4])

df.plot(x = 't1',
        y = 'enc_1',
        label = enc_name1,
        style = '-',
        lw = 1,
        ax = ax1, 
        color = my_colors[0])


df.plot(x = 't2',
        y = 'enc_2',
        label = enc_name2,
        style = '-',
        lw = 1,
        ax = ax2, 
        color = my_colors[1])


# axis 1 config
ax1.set_title('Elapsed Time = %s sec'%t1_time.total_seconds())
ax1.ticklabel_format(axis ='y', style = 'sci', scilimits=(0,0))
#ax1.set_xlim(xmin,xmax)
ax1.set_ylim(0,None)
ax1.set_xlabel('Time [sec]')
ax1.set_ylabel('Encoder Reading')
ax1.legend(loc='upper right') 
ax1.legend(bbox_to_anchor=(2.25, 1), loc='upper left') # use if want floating legend

# axis 2 config
ax2.set_title('Elapsed Time = %s sec'%t2_time.total_seconds())
ax2.ticklabel_format(axis ='y', style = 'sci', scilimits=(0,0))
#ax2.set_xlim(xmin,xmax)
ax2.set_ylim(0,None)
ax2.set_xlabel('Time [sec]')
ax2.set_ylabel('Encoder Reading')
ax2.legend(loc='upper right')   
ax2.legend(bbox_to_anchor=(1.05, 0.80), loc='upper left') # use if want floating legend


# save fig in high def
plt.savefig(OUT_ROOT + plot_name + '_multi.png', dpi=300, bbox_inches="tight")
