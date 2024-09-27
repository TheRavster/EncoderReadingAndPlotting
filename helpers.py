#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 15:37:05 2024

Script for all helper functions called by main.py

EDIT WITH CAUTION!!

@author: brutal_blondie
"""
#----------------------------------------------------------
# IMPORTS
#----------------------------------------------------------
import sys
import time
import glob
import serial
import matplotlib.pyplot as plt
import pandas as pd
import csv
from rendering import PointsInSpace
my_colors = ['#00C5CD','#FF0000', '#32CD32', '#8B8989','#00EE00'] 


#----------------------------------------------------------
# FUNCTIONS
#----------------------------------------------------------
def get_serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    # get ports most likely usable for connection
    best_ports = [s for s in result if "usbmodem" in s]
    return result, best_ports
#----------------------------------------------------------
def get_encoder_names():
    '''Asks user for encoder types and assigns names
    NOTE: enc_type is never used but leaving this in case you need it...'''
    print("Is First Encoder Type Magnetic or Capacitive?")
    res1 = input()
    enc_type1, enc_name1 = 1, "Capacitive"
    if (res1[0] == 'M'):
        enc_type1 = 0
        enc_name1 = "Magnetic"
    print("Is Second Encoder Type Magnetic or Capacitive?")
    res2 = input()
    enc_type2, enc_name2 = 1, "Capacitive"
    if (res2[0] == 'M'):
        enc_type2 = 0
        enc_name2 = "Magnetic"
    print(enc_name1, enc_name2)
    return enc_name1, enc_name2, enc_type1, enc_type2
#----------------------------------------------------------
def serialConnect(port):
    '''General function to connect to any given port
    Use modem number as input'''
    print("Connecting to serial port...")
    COM_PORT = port
    ser = serial.Serial(
        port=COM_PORT,
        baudrate=115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=0,)
    print(ser)
    print("Connected to: " + ser.portstr)
    return ser
#----------------------------------------------------------
def animPlot(enc_name1, ser1, enc_name2, ser2, TRAILING_POINTS, MIN_MESSAGE_BYTES):
    readings1 = []
    timings1 = []
    readings2 = []
    timings2 = []
    
    # sets plot maxes depending on sensor types
    if enc_name1 == 'Magnetic':
        max_val = 20e3
    else: max_val = 5e3
    
    if enc_name2 == 'Magnetic':
        max_val2 = 20e3
    else: max_val2 = 5e3
    
    #------------------------------------
    # INITIATE PLOT CLASS
    #------------------------------------
    live_plotter = PointsInSpace(
                    title = enc_name1,
                    title2 = enc_name2,
                    xlabel = 'Elapsed Time (s)',
                    xlabel2 = 'Elapsed Time (s)',
                    ylabel = 'Reading',
                    xlim=[0, 5],
                    ylim=[0, max_val],
                    ylim2=[0, max_val2],
                    enable_grid=True,
                    enable_legend=False,)
    # REGISTER PLOTS
    live_plotter.register_plot(enc_name1, alpha=0.5)
    live_plotter.register_plot2(enc_name2, alpha=0.5)
    
    index = -1
    with open(enc_name1 + enc_name2 + '_recordings.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(['t1, enc_1, t2, enc_2'])
    
        while True:
            try:
                # Read bytes goofery
                #------------------------------------
                # READ SER1
                #------------------------------------
                #print('ser1 reading')
                bytes_to_read1 = ser1.in_waiting
                if bytes_to_read1 < MIN_MESSAGE_BYTES:
                    continue
                line1 = ser1.read(bytes_to_read1).decode("utf-8")
                segments1 = line1.split()
                #print('passed ser1')
                #------------------------------------
                # READ SER2
                #------------------------------------
                #print('ser2read')
                bytes_to_read2 = ser2.in_waiting
                if bytes_to_read2 < MIN_MESSAGE_BYTES:
                    continue
                line2 = ser2.read(bytes_to_read2).decode("utf-8")
                segments2 = line2.split()
    
                # Parse the message by reading the value after each label
                try:
                    
                    # Do this in two steps so that values are not changed if not all values exist
                    def value_by_label(label, segments):
                        res = int(segments[segments.index(f"{label}:") + 1])
                        return res
                    #------------------------------------
                    # SAVE READINGS
                    #------------------------------------
                    # lists
                    reading1 = value_by_label("Reading", segments1)
                    time1 = time.time()
                    reading2 = value_by_label("Reading", segments2)
                    time2 = time.time()
                    
                    # DEBUG 
                    print(time1, reading1, time2, reading2)
                    
                    # append to lists for plotting
                    readings1.append(reading1)
                    readings2.append(reading2)
                    timings1.append(time1)
                    timings2.append(time2)
                    
                    # write to csv
                    csv_writer.writerow([str(time1), str(reading1), str(time2), str(reading2)])
                    
                except Exception as e:
                    print(e)
                    continue
    
                if len(readings1) > TRAILING_POINTS:
                    readings1.pop(0)
                    timings1.pop(0)
                #------------------------------------
                # PLOT READINGS
                #------------------------------------   
                # Display results
                live_plotter.start_drawing()
                live_plotter.draw_points(enc_name1, timings1, readings1)
                live_plotter.draw_points2(enc_name2, timings2, readings2)
                live_plotter.end_drawing()
                live_plotter.end_drawing2()
    
            except Exception as e:
                print(e)
                ser1.close()
                ser2.close()
                print("Closed connection inside")
                quit()
    
        ser1.close()
        ser2.close()
        print("Closed connection outside")
#----------------------------------------------------------
