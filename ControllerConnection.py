#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
"""
Handling raw data inputs example
"""
from time import sleep
from msvcrt import kbhit
import msvcrt
import sys
import pywinusb.hid as hid
import tkinter as tk
import time
import csv
import ControllerInterface as CuI
from ControllerInterface import *
import pygame as pg

start_time = time.time()

    
pdata = 0
pButsBuffer = []
pPotsBuffer = []

class NI_Controller:
    #   Native Instruments Kontrol s2mk2
    def __init__(self,Button,Knob):
        self.ButtonBuffer = [x]
        self.KnobBuffer = [y]

    def getKnobBuffer(self):
        return self.KnobBuffer
    def getButtonBuffer(self):
        return self.ButtonBuffer


def sample_handler(data):
    #print([time.time()-start_time]+[data])
    process_sample(data)

def process_sample(data):
    global pButsBuffer
    global pPotsBuffer
    global pdata
    
    if pdata == 0:
        #   Populating the Previous data variable
        print("Starting Listener...\n")
        print(f"Initial Data Input:\n {data}\n ")
        pButsBuffer = data
        pPotsBuffer = data
        pdata = 1
    else:
        ##print(f"New Button Chunk - Len: {len(data)}")
        ##print(data)
        if data[0] == 1: # Button Buffer
            ##SHIFT SYNC CUE PLAY                
            ##print(f"{(data[11]>>3)&1}{(data[11]>>2)&1}{(data[11]>>1)&1}{data[11]&1}")    
            for i in range(len(data)):
                if pButsBuffer[i] != data[i]:

##                    if i == 1 or i == 2 or i == 3 or i == 4: #JOG WHEEL A
##                        print(f"{data[1]}\t{data[2]}\t{data[3]}\t{data[4]}")
##                    elif i == 5 or i == 6 or i == 7 or i == 8: #JOG WHEEL B
##                        print(f"{data[5]}\t{data[6]}\t{data[7]}\t{data[8]}")                    

                    if i == 9:
                        diff = data[i]- pButsBuffer[i]
                        print(f"{diff & 1} {diff & 2} {diff & 4} {diff & 8} {data[i]}")
##                        if diff & 1 and data[i] == 1:
##                            print(f"{diff&1}\nDeck_B Play_ButtonDown")
##                        else:
##                            print(f"{diff&1 and data[i] == 1}\nDeck_B Play_ButtonUp")
##                            
                    elif i == 11:
                        if abs(data[i]-pButsBuffer[i]) == 8:
                            if (data[11]>>3)&1:
                                print("Shift Button Down")
                            else:
                                print("Shift Button Up")
                        if abs(data[i]-pButsBuffer[i]) == 4: 
                            if (data[11]>>2)&1:
                                print("Sync Button Down")
                            else:
                                print("Sync Button Up")
                        if abs(data[i]-pButsBuffer[i]) == 2:
                            if (data[11]>>1)&1:
                                print("Cue Button Down")
                            else:
                                print("Cue Button Up")
                        if abs(data[i]-pButsBuffer[i]) == 1:
                            if (data[11])&1:
                                print("Play Button Down")
                            else:
                                print("Play Button Up")
                    ##print(f"    Change in byte\t{i}\tfrom\t{pButsBuffer[i]}\tto\t{data[i]}\tof\t{data[i]-pButsBuffer[i]}")
            pButsBuffer = data




        elif data[0] == 2: # Pots Buffer
            ##print(f"New Potentiometer Chunk - Len: {len(data)}")     
            for i in range(len(data)):
                if pPotsBuffer[i] != data[i]:
                    if i == 7 or i == 8:
                        pass
                        print(f"Deck_A Tempo {(data[8]*256)+data[7]}")
                    if i == 19 or i == 20:
                        pass
                        print(f"Deck_A MixSlider {(data[20]*256)+data[19]}")
                    #print(f"    Change in byte\t{i}\tfrom\t{pPotsBuffer[i]}\tto\t{data[i]}\tof\t{data[i]-pPotsBuffer[i]}")
            pPotsBuffer = data


def samples_from_file(filename = "DefaultParasyteSessionFile.csv"):
    with open(filename, "r") as f:
        reader = csv.reader(f)
        lines = [i for i in reader]
        time = [i[0] for i in lines]
        data = [[int(j) for j in i[1:]] for i in lines]
    return time , data
     
   
def sample_to_file(data,filename = "DefaultParasyteSessionFile.csv"):
    global start_time
    with open(filename,"a",newline = '') as f:
        writer = csv.writer(f)
        writer.writerow([time.time()- start_time]+data)

def samples_to_file(data,filename = "DefaultParasyteSessionFile.csv"):
    global start_time
    with open(filename,"a",newline = '') as f:
        writer = csv.writer(f)
        writer.writerows([time.time()- start_time]+data)
    
    
    

def hid_device_connection():
    # simple test
    # browse devices...
    all_hids = hid.find_all_hid_devices()
    if all_hids:
        while True:
            
            print("Choose a device to monitor raw input reports:\n")
            print("0 => Exit")
            
            for index, device in enumerate(all_hids):
                device_name = unicode("{0.vendor_name} {0.product_name}" \
                        "(vID=0x{1:04x}, pID=0x{2:04x})"\
                        "".format(device, device.vendor_id, device.product_id))
                
                print("{0} => {1}".format(index+1, device_name))
                
            print("\n\tDevice ('0' to '%d', '0' to exit?) " \
                    "[press enter after number]:" % len(all_hids))
            
            index_option = raw_input()
            
            if index_option.isdigit() and int(index_option) <= len(all_hids):
                # invalid
                break;
            
        int_option = int(index_option)
        if int_option:
            device = all_hids[int_option-1]
            try:
                device.open()

                #set custom raw data handler

                device.set_raw_data_handler(sample_handler)

                print("\nWaiting for data...\nPress ESC key to stop...")
                key_stroke = 0
                while device.is_plugged():
                    #just keep the device opened to receive events
                    if msvcrt.kbhit():
                        key_stroke = msvcrt.getche()
                        #print(key_stroke)
                        if key_stroke==chr(27).encode():
                            print ("Esc key pressed")
                            break
                        
                    sleep(0.5)
                return
            finally:
                device.close()
    else:
        print("There's not any non system HID class device available")
        

if __name__ == '__main__':
    # first be kind with local encodings
    import sys
    if sys.version_info >= (3,):
        # as is, don't handle unicodes
        unicode = str
        raw_input = input
    else:
        # allow to show encoded strings
        import codecs
        sys.stdout = codecs.getwriter('mbcs')(sys.stdout)
    print("DJ_Parasyte Version: Pre-Alpha")
    print("Author: Sam Swatman")

    mode = input("\nConnect to Hid or Replay from file?\n1 -\tHid Device Connection\n2 -\tReplay From File\n3 -\tQuit\n> ")
    if mode == "1":
        hid_device_connection()
    elif mode == "2":
        times,data = samples_from_file("DeckATransport.csv")
        local_start_time = time.time()
        
        for i,sample in enumerate(data):
            while float(times[i]) > float(time.time()-local_start_time):
                ##print(time.time()-local_start_time)
                # print(str(time.time()-local_start_time)[:5],end="\n")
                pass
            
            print(str(times[i])[:5],end="\t")
            process_sample(sample)
            
            
            
            
            
    elif mode == "3":
        quit()



