'''
DJ Tracker 'Parasyte'
Author - Sam Swatman
'''
from time import sleep
from msvcrt import kbhit
import msvcrt
import sys
import pywinusb.hid as hid
import tkinter as tk
import time
import csv
from ControllerInterface import ControllerInterface
from NITKS2MK2 import TKS2MK2 as Kon
from NITKS2MK2 import *
from ControllerInterface import *
import pygame as pg
import datetime
import threading
from threading import Thread





inputRecordingPath = "./Input_Recordings/"
pdata = 0
pButsBuffer = []
pPotsBuffer = []

Record = True

def boolFromBit(byte,index):
    return (byte>>index)&1

def DecodeButton(data,index,offset):
    return boolFromBit(data[index],offset)

def Decode16BitEncoder(data,index):
    x = (data[index+1]*256)+data[index]
    return x 

def Decode8BitEncoder(data,index):
    x = data[index]
    return x 

def Decode4BitEncoder(data,index,high=False):
    if high:
        x = (data[index] - (data[index]%16))//16
    else:
        x = data[index]%16
    return x 

def prep16BitEncoderState(state):
    # 101 to account for instability in potentiometers
    return (101*(boundValues(state,0,4096)))//4096

def prep16BitKnobState(state):
    
    return 90+((270*(boundValues(state,0,4096)))//4096)

def prep4BitEncoderState(state):
    return (100*(boundValues(state,0,16)))//16

def loadControllerBBuffer(bBuff,controller:Kon):
    controller.Deck_A.TransportSection.Play.setPressed(DecodeButton(bBuff,11,0))
    controller.Deck_A.TransportSection.Cue.setPressed(DecodeButton(bBuff,11,1))
    controller.Deck_A.TransportSection.Sync.setPressed(DecodeButton(bBuff,11,2))
    controller.Deck_A.TransportSection.Shift.setPressed(DecodeButton(bBuff,11,3))

    controller.Deck_A.HotCueSection.Cue4.setPressed(DecodeButton(bBuff,11,4))
    controller.Deck_A.HotCueSection.Cue3.setPressed(DecodeButton(bBuff,11,5))
    controller.Deck_A.HotCueSection.Cue2.setPressed(DecodeButton(bBuff,11,6))
    controller.Deck_A.HotCueSection.Cue1.setPressed(DecodeButton(bBuff,11,7))

    controller.Deck_A.JogSection.Jog.setPressed(DecodeButton(bBuff,10,0))
    controller.Deck_B.JogSection.Jog.setPressed(DecodeButton(bBuff,10,1))

    controller.Mixer.FaderSection.CueA.setPressed(DecodeButton(bBuff,10,4))
    controller.Deck_B.TempoSection.Flux.setPressed(DecodeButton(bBuff,10,5))
    controller.Deck_B.LoopSection.In.setPressed(DecodeButton(bBuff,10,6))
    controller.Deck_B.LoopSection.Out.setPressed(DecodeButton(bBuff,10,7))

    controller.Deck_B.TransportSection.Play.setPressed(DecodeButton(bBuff,9,0))
    controller.Deck_B.TransportSection.Cue.setPressed(DecodeButton(bBuff,9,1))
    controller.Deck_B.TransportSection.Sync.setPressed(DecodeButton(bBuff,9,2))
    controller.Deck_B.TransportSection.Shift.setPressed(DecodeButton(bBuff,9,3))

    controller.Deck_B.HotCueSection.Cue4.setPressed(DecodeButton(bBuff,9,4))
    controller.Deck_B.HotCueSection.Cue3.setPressed(DecodeButton(bBuff,9,5))
    controller.Deck_B.HotCueSection.Cue2.setPressed(DecodeButton(bBuff,9,6))
    controller.Deck_B.HotCueSection.Cue1.setPressed(DecodeButton(bBuff,9,7))

    controller.Mixer.MasterSection.RemixB.setPressed(DecodeButton(bBuff,12,0))
    controller.Mixer.MasterSection.RemixA.setPressed(DecodeButton(bBuff,12,1))
    controller.Mixer.MasterSection.LoadB.setPressed(DecodeButton(bBuff,12,2))
    controller.Mixer.MasterSection.LoadA.setPressed(DecodeButton(bBuff,12,3))

    controller.Mixer.FaderSection.CueA.setPressed(DecodeButton(bBuff,12,4))
    controller.Deck_A.TempoSection.Flux.setPressed(DecodeButton(bBuff,12,5))
    controller.Deck_A.LoopSection.In.setPressed(DecodeButton(bBuff,12,6))
    controller.Deck_A.LoopSection.Out.setPressed(DecodeButton(bBuff,12,7))

    controller.FX.FX_Line_2.DryWetButton.setPressed(DecodeButton(bBuff,13,2))
    controller.FX.FX_Line_2.FX3Button.setPressed(DecodeButton(bBuff,13,3))
    controller.FX.FX_Line_2.FX2Button.setPressed(DecodeButton(bBuff,13,4))
    controller.FX.FX_Line_2.FX1Button.setPressed(DecodeButton(bBuff,13,5))
    controller.Mixer.EQ_A_Section.FXEncoder.setPressed(DecodeButton(bBuff,12,6))
    controller.Mixer.EQ_B_Section.FXEncoder.setPressed(DecodeButton(bBuff,12,7))


    controller.Mixer.EQ_B_Section.FX2Select.setPressed(DecodeButton(bBuff,14,0))
    controller.Mixer.EQ_B_Section.FX1Select.setPressed(DecodeButton(bBuff,14,1))
    controller.Mixer.EQ_A_Section.FX2Select.setPressed(DecodeButton(bBuff,14,2))
    controller.Mixer.EQ_A_Section.FX1Select.setPressed(DecodeButton(bBuff,14,3))

    controller.FX.FX_Line_1.DryWetButton.setPressed(DecodeButton(bBuff,14,4))
    controller.FX.FX_Line_1.FX3Button.setPressed(DecodeButton(bBuff,14,5))
    controller.FX.FX_Line_1.FX2Button.setPressed(DecodeButton(bBuff,14,6))
    controller.FX.FX_Line_1.FX1Button.setPressed(DecodeButton(bBuff,14,7))

    controller.Deck_A.LoopSection.Left_Encoder.setPressed(DecodeButton(bBuff,15,0))
    controller.Deck_A.LoopSection.Right_Encoder.setPressed(DecodeButton(bBuff,15,1))
    controller.Mixer.MasterSection.BrowseEncoder.setPressed(DecodeButton(bBuff,15,2))
    controller.Deck_B.LoopSection.Left_Encoder.setPressed(DecodeButton(bBuff,15,4))
    controller.Deck_B.LoopSection.Right_Encoder.setPressed(DecodeButton(bBuff,15,5))

    controller.Deck_A.JogSection.Jog.setState(Decode8BitEncoder(bBuff,1))
    controller.Deck_B.JogSection.Jog.setState(Decode8BitEncoder(bBuff,5))
    return controller

def loadControllerPBuffer(pBuff,controller:Kon):
    controller.Deck_A.TempoSection.Tempo_Slider.setState(Decode16BitEncoder(pBuff,7))
    controller.Deck_A.LoopSection.Left_Encoder.setState(Decode4BitEncoder(pBuff,1))
    controller.Deck_A.LoopSection.Right_Encoder.setState( Decode4BitEncoder(pBuff,1,True))

    controller.Deck_B.TempoSection.Tempo_Slider.setState(Decode16BitEncoder(pBuff,2))
    controller.Deck_B.LoopSection.Left_Encoder.setState(Decode4BitEncoder(pBuff,3))
    controller.Deck_B.LoopSection.Right_Encoder.setState(Decode4BitEncoder(pBuff,3,True))

    controller.FX.FX_Line_1.DryWetKnob.setState(Decode16BitEncoder(pBuff,23))
    controller.FX.FX_Line_1.FX1Knob.setState(Decode16BitEncoder(pBuff,25))
    controller.FX.FX_Line_1.FX2Knob.setState(Decode16BitEncoder(pBuff,27))
    controller.FX.FX_Line_1.FX3Knob.setState(Decode16BitEncoder(pBuff,29))

    controller.FX.FX_Line_2.DryWetKnob.setState(Decode16BitEncoder(pBuff,31))
    controller.FX.FX_Line_2.FX1Knob.setState(Decode16BitEncoder(pBuff,33))
    controller.FX.FX_Line_2.FX2Knob.setState(Decode16BitEncoder(pBuff,35))
    controller.FX.FX_Line_2.FX3Knob.setState(Decode16BitEncoder(pBuff,37))

    controller.Mixer.FaderSection.LevelA.setState(Decode16BitEncoder(pBuff,19))
    controller.Mixer.FaderSection.LevelB.setState(Decode16BitEncoder(pBuff,21))
    controller.Mixer.FaderSection.CrossFader.setState(Decode16BitEncoder(pBuff,5))

    controller.Mixer.EQ_A_Section.EQ_HI.setState(Decode16BitEncoder(pBuff,39))
    controller.Mixer.EQ_A_Section.EQ_MID.setState(Decode16BitEncoder(pBuff,41))
    controller.Mixer.EQ_A_Section.EQ_LO.setState(Decode16BitEncoder(pBuff,43))

    controller.Mixer.EQ_B_Section.EQ_HI.setState(Decode16BitEncoder(pBuff,45))
    controller.Mixer.EQ_B_Section.EQ_MID.setState(Decode16BitEncoder(pBuff,47))
    controller.Mixer.EQ_B_Section.EQ_LO.setState(Decode16BitEncoder(pBuff,49))

    controller.Mixer.EQ_A_Section.FXEncoder.setState(Decode4BitEncoder(pBuff,3,True))
    controller.Mixer.EQ_B_Section.FXEncoder.setState(Decode4BitEncoder(pBuff,4))

    controller.Mixer.MasterSection.MasterLevel.setState(Decode16BitEncoder(pBuff,15))
    controller.Mixer.MasterSection.RemixLevel.setState(Decode16BitEncoder(pBuff,13))
    controller.Mixer.MasterSection.BrowseEncoder.setState(Decode4BitEncoder(pBuff,2)) 


    return controller

def loadController():
    with open('DefaultValues.csv', "r") as f:
        reader = csv.reader(f)
        lines = [[int(j) for j in i] for i in reader]
    bBuff = lines[0]
    pBuff = lines[1]
    print(lines)
    controller = Kon(name="NITKS2MK2")
    ##  Load p Buffer Values
    controller = loadControllerPBuffer(pBuff,controller)
    controller = loadControllerBBuffer(bBuff,controller)
    return controller

def loadGlobals():
    global pButsBuffer
    global pPotsBuffer
    with open('DefaultValues.csv', "r") as f:
        reader = csv.reader(f)
        lines = [[int(j) for j in i] for i in reader]
    pButsBuffer = lines[0]
    pPotsBuffer = lines[1]



def sample_handler(data):
    process_sample(data)

def process_sample(data):
    global pButsBuffer
    global pPotsBuffer
    global pdata
    global controller
    global rec 
    if pdata == 0:
        #   Populating the Previous data variable
        print("Starting Listener...\n")
        #print(f"Initial Data Input:\n {data}\n ")
        #pButsBuffer = data
        #pPotsBuffer = data
        pdata = 1
    
    #print(data)
    
    print(f"{pButsBuffer[1]}\t{pButsBuffer[2]}\t{pButsBuffer[3]}\t{pButsBuffer[4]}\t{str(time.time())[8:15]}\t{data[4]-pButsBuffer[4]}")
    sample_to_file(data=data,filename=inputRecordingPath+'DefaultValues.csv')
    if data[0] == 1: # Button Buffer  
        controller = loadControllerBBuffer(bBuff=data,controller=controller)
        for i in range(len(data)):
            
            if pButsBuffer[i] != data[i]:
                #print(f"    Change in byte\t{i}\tfrom\t{pButsBuffer[i]}\tto\t{data[i]}\tof\t{data[i]-pButsBuffer[i]}")
                #print(f"{DecodeButton(data,10,0)}\t{data[10]}")
                pass
        pButsBuffer = data
    elif data[0] == 2: # Knob Buffer  
        controller = loadControllerPBuffer(pBuff=data,controller=controller)
        for i in range(len(data)):
            if pPotsBuffer[i] != data[i]:
               
                #print(f"    Change in byte\t{i}\tfrom\t{pPotsBuffer[i]}\tto\t{data[i]}\tof\t{data[i]-pPotsBuffer[i]}")
                pass
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
    
    
    

def hid_device_connection(fn = '',rec=False):
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
                    "[press enter after number]:" % len(all_hids),end="\n> ")
            
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
                    #print(f"")
                    
                    if msvcrt.kbhit():
                        key_stroke = msvcrt.getche()
                        
                        if key_stroke==chr(27).encode():
                            print ("Esc key pressed")
                            break
                        
                    sleep(0.5)
                return
            finally:
                device.close()
    else:
        print("There's not any non system HID class device available")

        
def draw_ControllerGUI():
    # simple test
    # browse devices...
    global controller
    ui = ControllerInterface()
    screen = ui.screen
    sp = 0
    down = False
    done = False
    white = [255,255,255]
    clock = ui.clock
    while not(done):
        #just keep the device opened to receive events
        screen.fill([0,0,0])
        global pButsBuffer
        global pPotsBuffer
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    done = True
        ##  Lines For Testing
        pg.draw.line(screen,255,[900,0],[900,900])
        pg.draw.line(screen,255,[0,450],[900,450])
        pg.draw.line(screen,255,[450,0],[450,900])
        

        ##  Draw Deck A
        ##  A_JogWheel
        drawJog(screen=screen,
                pos=[450,350],
                deg=controller.Deck_A.JogSection.Jog.getState()*(255/360),
                size=70,
                pressed= controller.Deck_A.JogSection.Jog.getPressed(),#(sp%60) > 30,
                label="Test Jog",
                textSize=10)
        ## A_Tempo
        ##TempoPos = [200,900]
        drawEnc(screen=screen,
                pos=[300,500],
                deg=22.5*controller.Deck_A.LoopSection.Left_Encoder.getState(),
                size=30,
                pressed=controller.Deck_A.LoopSection.Left_Encoder.getPressed(),
                label="Deck A L Enc",
                textSize=10)
        
        drawEnc(screen=screen,
                pos=[600,500],
                deg=22.5*controller.Deck_A.LoopSection.Right_Encoder.getState(),
                size=30,
                pressed=controller.Deck_A.LoopSection.Right_Encoder.getPressed(),
                label="Deck A R Enc",
                textSize=10)
        
        drawBtn(screen=screen,
                pos=[400,500],
                label="IN",
                size=40,textSize=10,
                pressed = controller.Deck_A.LoopSection.In.getPressed(),
                colour=white)
        
        drawBtn(screen=screen,
                pos=[500,500],
                label="OUT",
                size=40,textSize=10,
                pressed = controller.Deck_A.LoopSection.Out.getPressed(),
                colour=white)
        ##  A_HotCue
        drawBtn(screen=screen,
                pos=[300,600],
                label="HotCue1",
                size=40,textSize=10,
                pressed = controller.Deck_A.HotCueSection.Cue1.getPressed(),
                colour=white)
        drawBtn(screen=screen,
                pos=[400,600],
                label="HotCue2",
                size=40,textSize=10,
                pressed = controller.Deck_A.HotCueSection.Cue2.getPressed(),
                colour=white)
        drawBtn(screen=screen,
                pos=[500,600],
                label="HotCue3",
                size=40,textSize=10,
                pressed = controller.Deck_A.HotCueSection.Cue3.getPressed(),
                colour=white)
        drawBtn(screen=screen,
                pos=[600,600],
                label="HotCue4",
                size=40,textSize=10,
                pressed = controller.Deck_A.HotCueSection.Cue4.getPressed(),
                colour=white)
        ##  A_Transport
        drawBtn(screen=screen,
                pos=[300,700],
                label="Shift",
                size=40,textSize=10,
                pressed = controller.Deck_A.TransportSection.Shift.getPressed(),
                colour=white)
        drawBtn(screen=screen,
                pos=[400,700],
                label="Sync",
                size=40,textSize=10,
                pressed = controller.Deck_A.TransportSection.Sync.getPressed(),
                colour=white)
        drawBtn(screen=screen,
                pos=[500,700],
                label="Cue",
                size=40,textSize=10,
                pressed = controller.Deck_A.TransportSection.Cue.getPressed(),
                colour=white)
        drawBtn(screen=screen,
                pos=[600,700],
                label="Play",
                size=40,textSize=10,
                pressed = controller.Deck_A.TransportSection.Play.getPressed(),
                colour=white)
        ## A_Tempo
        drawVFad(screen= screen,
                pos=[100,500],
                size=[100,400],
                percentage=100-prep16BitEncoderState(controller.Deck_A.TempoSection.Tempo_Slider.getState()),
                label="Deck A Tempo",
                textSize=30
                )
        drawCBtn(screen=screen,
                pos=[150,400],
                label="Flux",
                size=10,textSize=10,
                pressed = controller.Deck_A.TempoSection.Flux.getPressed(),
                colour=white)
        '''
        drawKnb(screen=screen,
                pos=[450,150],
                deg=prep16BitKnobState(controller.Mixer.EQ_A_Section.EQ_LO.getState()),
                size=70,
                label=f"Knob {prep16BitKnobState(controller.Mixer.EQ_A_Section.EQ_LO.getState())}",
                textSize=30)
        
        drawCBtn(screen=screen,
                pos=[450,450],
                label="Deck A Flux",
                size=50,textSize=30,
                pressed = controller.Deck_A.TempoSection.Flux.getPressed(),
                colour=white)
        
        drawVFad(screen= screen,
                pos=[750,150],
                size=[100,400],
                percentage=100-prep16BitEncoderState(controller.Mixer.FaderSection.LevelA.getState()),
                label="Deck A Level",
                textSize=30
                )

        drawVFad(screen= screen,
                pos=[1150,150],
                size=[100,400],
                percentage=100-prep16BitEncoderState(controller.Mixer.FaderSection.LevelB.getState()),
                label="Deck B Level",
                textSize=30
                )
        
        drawHFad(screen= screen,
                pos=[1000,750],
                size=[400,100],
                percentage=prep16BitEncoderState(controller.Mixer.FaderSection.CrossFader.getState()),
                label="Crossfader",
                textSize=30
                )'''
        
        #renderText(screen,f"H = {screen.get_height()} , W = {screen.get_width()}",[700,100],[255,255,255],size=20)
        renderText(screen,f"mouse_pos = ({pg.mouse.get_pos()})",[pg.mouse.get_pos()[0]+85,pg.mouse.get_pos()[1]+10],[255,255,255],size=10)
        renderText(screen,f"{time.time()-start_time}",[900,900],[255,255,255],size=30)
        sp = (sp + 1) % 360
        pg.display.flip()
        clock.tick(60)  

if __name__ == '__main__':
    global controller
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
    
    controller = loadController()
    loadGlobals()
    start_time = time.time()
    Gui_Thread = Thread(target=draw_ControllerGUI,args=())
    mode = input("\nConnect to Hid or Replay from file?\n1 -\tHid Device Connection\n2 -\tReplay From File\n3 -\tQuit\n> ")
    GUI = input("\nEnable GUI?\n1 - Yes\n0 - No\n> ")
    if mode == "1":
        rec = input("\nWould you like to record to a file?\n1 - Yes\nAny Key - No\n> ")
        fn = inputRecordingPath + datetime.datetime.now().__str__() + "_SessionFile.csv"
        if GUI != '1':
            hid_device_connection()
        else:
            Gui_Thread.start()
            hid_device_connection()               
    elif mode == "2":
        if GUI == '1':
            Gui_Thread.start()
        times,data = samples_from_file(inputRecordingPath + "AFXBUTTONSTHENKNOBS.csv")
        start_time = time.time()
        
        for i,sample in enumerate(data):
            while float(times[i]) > float(time.time()-start_time):
                ##  Spinlock
                pass
            
            print(str(times[i])[:5],end="\t") 
            process_sample(sample)
        Gui_Thread.join()
                 
    elif mode == "3":
        quit()



