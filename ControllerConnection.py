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
from ControllerInterface import ControllerInterface
import NITKS2MK2 as Kon
from ControllerInterface import *
import pygame as pg

start_time = time.time()

inputRecordingPath = "./Input_Recordings/"
pdata = 0
pButsBuffer = []
pPotsBuffer = []

def boolFromBit(byte,index):
    return (byte>>index)&1

def Decode16BitEncoder(data,index):
    x = (data[index+1]*256)+data[index]
    return x 


def Decode4BitEncoder(data,index,high=False):
    if high:
        x = (data[index] - (data[index]%16))//16
    else:
        x = data[index]%16
    return x 
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

        if data[0] == 1: # Button Buffer  
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




        elif data[0] == 2: # Knob Buffer  
            for i in range(len(data)):
                if pPotsBuffer[i] != data[i]:
                    if i == 7 or i == 8:
                        
                        print(f"Deck_A Tempo {Decode16BitEncoder(data,7)}")
                    if i == 9 or i == 10:
                        
                        print(f"Deck_B Tempo {Decode16BitEncoder(data,9)}")
                    if i == 19 or i == 20:
                        
                        print(f"Deck_A MixSlider {Decode16BitEncoder(data,19)}")
                    if i == 21 or i == 22:
                        
                        print(f"Deck_B MixSlider {Decode16BitEncoder(data,19)}")
                    if i == 1:
                        if abs(data[i]-pPotsBuffer[i])== 1 or abs(data[i]-pPotsBuffer[i])== 15:
                            print(f"L Loop Enc {Decode4BitEncoder(data,1)}")
                        else:
                            print(f"R Loop Enc {Decode4BitEncoder(data,1,True)}")
                    #print(f"    Change in byte\t{i}\tfrom\t{pPotsBuffer[i]}\tto\t{data[i]}\tof\t{data[i]-pPotsBuffer[i]}")
            pPotsBuffer = data


def samples_from_file(filename = inputRecordingPath+"DefaultParasyteSessionFile.csv"):
    with open(filename, "r") as f:
        reader = csv.reader(f)
        lines = [i for i in reader]
        time = [i[0] for i in lines]
        data = [[int(j) for j in i[1:]] for i in lines]
    return time , data
     
   
def sample_to_file(data,filename = inputRecordingPath + "DefaultParasyteSessionFile.csv"):
    global start_time
    with open(filename,"a",newline = '') as f:
        writer = csv.writer(f)
        writer.writerow([time.time()- start_time]+data)

def samples_to_file(data,filename = inputRecordingPath + "DefaultParasyteSessionFile.csv"):
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
                break
            
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

def gui_hid_device_connection():
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
                break
            
        int_option = int(index_option)
        if int_option:
            device = all_hids[int_option-1]
            try:
                device.open()

                #set custom raw data handler

                device.set_raw_data_handler(sample_handler)

                print("\nWaiting for data...\nPress ESC key to stop...")
                key_stroke = 0
                ui = ControllerInterface()
                screen = ui.screen
                while device.is_plugged():
                    #just keep the device opened to receive events
                    screen.fill([0,0,0])
                    for event in pg.event.get():
                        if event.type == pg.QUIT:
                            done = True
                        elif event.type == pg.KEYDOWN:
                            if event.key == pg.K_ESCAPE:
                                done = True
                            elif event.key == pg.K_SPACE:
                                down = True
                        elif event.type == pg.KEYUP:
                            if event.key == pg.K_SPACE:
                                down = False
                    ##  Lines For Testing
                    pg.draw.line(screen,255,[900,0],[900,900])
                    pg.draw.line(screen,255,[0,450],[900,450])
                    pg.draw.line(screen,255,[450,0],[450,900])
                    

                    ##  Draw Deck A
                    ##  A_JogWheel
                    drawJog(screen=screen,
                            pos=[150,450],
                            deg=sp,
                            size=70,
                            pressed= down,#(sp%60) > 30,
                            label="Test Jog",
                            textSize=30)

                    drawEnc(screen=screen,
                            pos=[150,150],
                            deg=sp,
                            size=70,
                            pressed=down,
                            label="Test Encoder",
                            textSize=30)

                    drawKnb(screen=screen,
                            pos=[450,150],
                            deg=sp,
                            size=70,
                            label="test Knob",
                            textSize=30)
                    
                    drawCBtn(screen=screen,
                            pos=[450,450],
                            label="Test Button",
                            size=50,textSize=30,
                            pressed = down,#(sp%30)>15,
                            colour=white)
                    
                    drawVFad(screen= screen,
                            pos=[750,150],
                            size=[100,400],
                            percentage=(boundValues(pg.mouse.get_pos()[1],150,550)-150)//4,
                            label="Test V Fader",
                            textSize=30
                            )
                    
                    drawHFad(screen= screen,
                            pos=[150,750],
                            size=[400,100],
                            percentage=(boundValues(pg.mouse.get_pos()[0],150,550)-150)//4,
                            label="Test H Fader",
                            textSize=30
                            )
                    
                    #renderText(screen,f"H = {screen.get_height()} , W = {screen.get_width()}",[700,100],[255,255,255],size=20)
                    renderText(screen,f"mouse_pos = ({pg.mouse.get_pos()})",[pg.mouse.get_pos()[0]+85,pg.mouse.get_pos()[1]+10],[255,255,255],size=10)
                    sp = (sp + 1) % 360
                    pg.display.flip()
                    clock.tick(60)  
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
        times,data = samples_from_file(inputRecordingPath + "DeckATransport.csv")
        local_start_time = time.time()
        
        for i,sample in enumerate(data):
            print(str(times[i])[:5],end="\t")
            process_sample(sample)
                 
    elif mode == "3":
        quit()



