"""
Created on Fri Sep 20 20:18:56 2024

Script for reading and liveplotting two encoders from two ports. 
    - Reads port id's automatically
    - Opens live plot with two axes for easy viewing during run
    - Saves all readings and time stampes to csv file after terminating plot

Use plot_data.py for plot of full recorded data.
See helpers.py for associated functions.

@author: brutal_blondie
"""

#----------------------------------------------------------
# IMPORTS
#----------------------------------------------------------
import os
import time
import numpy as np
import pandas as pd
import csv
import serial
from rendering import PointsInSpace
import matplotlib
matplotlib.use('TkAgg') # NOTE! If this is run, python will try to open all matplotlib plots as a live plot!
import matplotlib.pyplot as plt
from multiprocessing import Process
import keyboard

import helpers as h

my_colors = ['#00C5CD','#FF0000', '#32CD32', '#8B8989','#00EE00'] 

#----------------------------------------------------------
# USER VARIABLES
# Imput important variables here
#----------------------------------------------------------
# set paths
OUT_ROOT = '/output/'

# set encoder names
enc_name1 = 'Magnetic' # NOTE: can change back to user input by unhashing block 0 in main
enc_name2 = 'Capacitive'

# set port information
TRAILING_POINTS = 100
MIN_MESSAGE_BYTES = 16

#----------------------------------------------------------
# MAIN
#----------------------------------------------------------
if __name__ == '__main__':
    
    # 0 - GET USER INPUT
    # NOTE! Unhash this if want user input encoder types
    #enc_name1, enc_name2, enc_type1, enc_type2 = get_encoder_names()
    
    # 1 - GET PORTS
    all_ports, best_ports = h.get_serial_ports()
    
    # 2 - OPEN PORTS
    ser1 = h.serialConnect(best_ports[0])
    ser2 = h.serialConnect(best_ports[1])
    
    # 3 - START RUN
    print('------------- BEGINNING RUN ------------- ')

    
    start_time = time.time()

    h.animPlot(enc_name1, ser1, enc_name2, ser2, TRAILING_POINTS, MIN_MESSAGE_BYTES)
    
    # NOTE! Current version will not get this far...
    # When quit run, will exit plot without executing past h.animPlot
    
    #--------------------------------------------
    # multithred loop: NOT WORKING!!!
    # see thread_test.py for example test...
    
    #print('Press q at any time to end measurement.')
    #process = Process(target=h.animPlot, args = (enc_name1, ser1, enc_name2, ser2, TRAILING_POINTS, MIN_MESSAGE_BYTES,))
    #process.start()
    #while process.is_alive():
    #    if keyboard.is_pressed('q'):
    #        process.terminate()
    #        break
    #--------------------------------------------
    end_time = time.time()
    print('------------- RUN COMPLETE :) ------------- ')
    
    # 4 - END RUN
    # close connections 
    ser1.close()
    print("Closed connection 1...")
    ser2.close()
    print("Closed connection 2...") 
    