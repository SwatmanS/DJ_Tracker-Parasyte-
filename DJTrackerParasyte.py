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
do_Kon = True
do_Draw = True
Record = True


## Scripts to decode HID packets from the TKS2MK2
def boolFromBit(byte,index):
    # byte is the byte of data
    # index is the index of the bit to turn into a bool
    # returns the bool value of a particular bit from a byte
    return (byte>>index)&1

def DecodeButton(data,index,offset):
    # decodes button infromation from a HID packet
    return boolFromBit(data[index],offset)

def Decode16BitEncoder(data,index):
    # decodes a 16bit encoder value from a HID packet
    x = (data[index+1]*256)+data[index]
    return x 

def Decode8BitEncoder(data,index):
    # decodes a 8bit encoder value from a HID packet
    x = data[index]
    return x 

def Decode4BitEncoder(data,index,high=False):
    # decodes a 4bit encoder value from a HID packet
    # high differentiates from High nibble / Low nibble of a full byte
    if high:
        x = (data[index] - (data[index]%16))//16
    else:
        x = data[index]%16
    return x 

def prep16BitEncoderState(state):
    # converts the extracted data and prepares it for display
    # 101 to account for instability in potentiometers
    return (101*(boundValues(state,0,4096)))//4096

def prep16BitKnobState(state):
    # converts the extracted data and prepares it for display
    return 90+((270*(boundValues(state,0,4096)))//4096)

def prep4BitEncoderState(state):
    # converts the extracted data and prepares it for display
    return (100*(boundValues(state,0,16)))//16

## Load and manage the controller/timecontroller objects
def loadControllerBBuffer(bBuff,controller:Kon):
    # Loads all of the HID button buffer into the controller object
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

    controller.Mixer.FaderSection.CueB.setPressed(DecodeButton(bBuff,10,4))
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
    controller.Mixer.EQ_A_Section.FXEncoder.setPressed(DecodeButton(bBuff,13,6))
    controller.Mixer.EQ_B_Section.FXEncoder.setPressed(DecodeButton(bBuff,13,7))


    controller.Mixer.EQ_B_Section.FX1Select.setPressed(DecodeButton(bBuff,14,0))
    controller.Mixer.EQ_B_Section.FX2Select.setPressed(DecodeButton(bBuff,14,1))
    controller.Mixer.EQ_A_Section.FX2Select.setPressed(DecodeButton(bBuff,14,2))
    controller.Mixer.EQ_A_Section.FX1Select.setPressed(DecodeButton(bBuff,14,3))

    controller.FX.FX_Line_1.DryWetButton.setPressed(DecodeButton(bBuff,14,4))
    controller.FX.FX_Line_1.FX3Button.setPressed(DecodeButton(bBuff,14,5))
    controller.FX.FX_Line_1.FX2Button.setPressed(DecodeButton(bBuff,14,6))
    controller.FX.FX_Line_1.FX1Button.setPressed(DecodeButton(bBuff,14,7))

    controller.Deck_A.LoopSection.Left_Encoder.setPressed(DecodeButton(bBuff,15,1))
    controller.Deck_A.LoopSection.Right_Encoder.setPressed(DecodeButton(bBuff,15,0))
    controller.Mixer.MasterSection.BrowseEncoder.setPressed(DecodeButton(bBuff,15,2))
    controller.Deck_B.LoopSection.Left_Encoder.setPressed(DecodeButton(bBuff,15,3))
    controller.Deck_B.LoopSection.Right_Encoder.setPressed(DecodeButton(bBuff,15,4))

    controller.Deck_A.JogSection.Jog.setState(Decode8BitEncoder(bBuff,1))
    controller.Deck_B.JogSection.Jog.setState(Decode8BitEncoder(bBuff,5))
    return controller

def loadControllerPBuffer(pBuff,controller:Kon):
    # Loads all of the HID potentiometer (Encoder) buffer into the controller object
    controller.Deck_A.TempoSection.Tempo_Slider.setState(Decode16BitEncoder(pBuff,7))
    controller.Deck_A.LoopSection.Left_Encoder.setState(Decode4BitEncoder(pBuff,1,True))
    controller.Deck_A.LoopSection.Right_Encoder.setState( Decode4BitEncoder(pBuff,1))

    controller.Deck_B.TempoSection.Tempo_Slider.setState(Decode16BitEncoder(pBuff,9))
    controller.Deck_B.LoopSection.Left_Encoder.setState(Decode4BitEncoder(pBuff,2,True))
    controller.Deck_B.LoopSection.Right_Encoder.setState(Decode4BitEncoder(pBuff,3))

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
    # Loads and initialises the controller object
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

def loadTimeController():
    # Loads a time controller object
    return TKS2MK2_TimeControl()        

def updateTimeController(TC:TKS2MK2_TimeControl):
    # updates the time controller to control the colours onscreen
    global current_time
    global start_time
    global controller
    current_time = time.time() - start_time

    TC.DeckAJog.loadCurrentState(sT = start_time,
                                 cT = current_time,
                                 value = controller.Deck_A.JogSection.Jog.getState())
    TC.DeckBJog.loadCurrentState(sT = start_time,
                                 cT = current_time,
                                 value = controller.Deck_B.JogSection.Jog.getState())
    TC.DeckAJogPressed.loadCurrentState(sT = start_time,
                                 cT = current_time,
                                 value = controller.Deck_B.JogSection.Jog.getPressed())
    TC.DeckAJogPressed.loadCurrentState(sT = start_time,
                                 cT = current_time,
                                 value = controller.Deck_B.JogSection.Jog.getPressed())
    
    TC.DeckACue.loadCurrentState(sT = start_time,
                                 cT = current_time,
                                 value= controller.Deck_A.TransportSection.Cue.getPressed())
    TC.DeckAPlay.loadCurrentState(sT = start_time,
                                 cT = current_time,
                                 value= controller.Deck_A.TransportSection.Play.getPressed())
    TC.DeckASync.loadCurrentState(sT = start_time,
                                 cT = current_time,
                                 value= controller.Deck_A.TransportSection.Sync.getPressed())
    TC.DeckAShift.loadCurrentState(sT = start_time,
                                 cT = current_time,
                                 value= controller.Deck_A.TransportSection.Shift.getPressed())
    TC.DeckAHot1.loadCurrentState(sT = start_time,
                                  cT = current_time,
                                  value = controller.Deck_A.HotCueSection.Cue1.getPressed())
    TC.DeckAHot2.loadCurrentState(sT = start_time,
                                  cT = current_time,
                                  value = controller.Deck_A.HotCueSection.Cue2.getPressed())
    TC.DeckAHot3.loadCurrentState(sT = start_time,
                                  cT = current_time,
                                  value = controller.Deck_A.HotCueSection.Cue3.getPressed())
    TC.DeckAHot4.loadCurrentState(sT = start_time,
                                  cT = current_time,
                                  value = controller.Deck_A.HotCueSection.Cue4.getPressed())
    
    TC.DeckBCue.loadCurrentState(sT = start_time,
                                 cT = current_time,
                                 value= controller.Deck_B.TransportSection.Cue.getPressed())
    TC.DeckBPlay.loadCurrentState(sT = start_time,
                                 cT = current_time,
                                 value= controller.Deck_B.TransportSection.Play.getPressed())
    TC.DeckBSync.loadCurrentState(sT = start_time,
                                 cT = current_time,
                                 value= controller.Deck_B.TransportSection.Sync.getPressed())
    TC.DeckBShift.loadCurrentState(sT = start_time,
                                 cT = current_time,
                                 value= controller.Deck_B.TransportSection.Shift.getPressed())
    TC.DeckBHot1.loadCurrentState(sT = start_time,
                                  cT = current_time,
                                  value = controller.Deck_B.HotCueSection.Cue1.getPressed())
    TC.DeckBHot2.loadCurrentState(sT = start_time,
                                  cT = current_time,
                                  value = controller.Deck_B.HotCueSection.Cue2.getPressed())
    TC.DeckBHot3.loadCurrentState(sT = start_time,
                                  cT = current_time,
                                  value = controller.Deck_B.HotCueSection.Cue3.getPressed())
    TC.DeckBHot4.loadCurrentState(sT = start_time,
                                  cT = current_time,
                                  value = controller.Deck_B.HotCueSection.Cue4.getPressed())
    
    TC.DeckATempoSlider.loadCurrentState(sT = start_time,
                                         cT = current_time,
                                         value = controller.Deck_A.TempoSection.Tempo_Slider.getState())
    
    TC.DeckAFlux.loadCurrentState(sT = start_time,
                                         cT = current_time,
                                         value = controller.Deck_A.TempoSection.Flux.getPressed())
    
    TC.DeckBTempoSlider.loadCurrentState(sT = start_time,
                                         cT = current_time,
                                         value = controller.Deck_B.TempoSection.Tempo_Slider.getState())
    
    TC.DeckBFlux.loadCurrentState(sT = start_time,
                                         cT = current_time,
                                         value = controller.Deck_B.TempoSection.Flux.getPressed())
    
    TC.DeckALoopEncL.loadCurrentState(sT = start_time,
                                         cT = current_time,
                                         value = controller.Deck_A.LoopSection.Left_Encoder.getState())

    TC.DeckALoopEncLPress.loadCurrentState(sT = start_time,
                                         cT = current_time,
                                         value = controller.Deck_A.LoopSection.Left_Encoder.getPressed())

    TC.DeckALoopIn.loadCurrentState(sT = start_time,
                                         cT = current_time,
                                         value = controller.Deck_A.LoopSection.In.getPressed())
    
    TC.DeckALoopOut.loadCurrentState(sT = start_time,
                                         cT = current_time,
                                         value = controller.Deck_A.LoopSection.Out.getPressed())

    TC.DeckALoopEncR.loadCurrentState(sT = start_time,
                                         cT = current_time,
                                         value = controller.Deck_A.LoopSection.Right_Encoder.getState())

    TC.DeckALoopEncRPress.loadCurrentState(sT = start_time,
                                         cT = current_time,
                                         value = controller.Deck_A.LoopSection.Right_Encoder.getPressed())
    
    TC.DeckBLoopEncL.loadCurrentState(sT = start_time,
                                         cT = current_time,
                                         value = controller.Deck_A.LoopSection.Left_Encoder.getState())

    TC.DeckBLoopEncLPress.loadCurrentState(sT = start_time,
                                         cT = current_time,
                                         value = controller.Deck_A.LoopSection.Left_Encoder.getPressed())

    TC.DeckBLoopIn.loadCurrentState(sT = start_time,
                                         cT = current_time,
                                         value = controller.Deck_A.LoopSection.In.getPressed())
    
    TC.DeckBLoopOut.loadCurrentState(sT = start_time,
                                         cT = current_time,
                                         value = controller.Deck_A.LoopSection.Out.getPressed())

    TC.DeckBLoopEncR.loadCurrentState(sT = start_time,
                                         cT = current_time,
                                         value = controller.Deck_A.LoopSection.Right_Encoder.getState())

    TC.DeckBLoopEncRPress.loadCurrentState(sT = start_time,
                                         cT = current_time,
                                         value = controller.Deck_A.LoopSection.Right_Encoder.getPressed())
    
    TC.FxLine1DW.loadCurrentState(sT = start_time,
                                         cT = current_time,
                                         value = controller.FX.FX_Line_1.DryWetKnob.getState())

    TC.FxLine1DWButton.loadCurrentState(sT = start_time,
                                         cT = current_time,
                                         value = controller.FX.FX_Line_1.DryWetButton.getPressed())
    TC.FxLine1K1.loadCurrentState(sT = start_time,
                                         cT = current_time,
                                         value = controller.FX.FX_Line_1.FX1Knob.getState())

    TC.FxLine1K1Button.loadCurrentState(sT = start_time,
                                         cT = current_time,
                                         value = controller.FX.FX_Line_1.FX1Button.getPressed())
    TC.FxLine1K2.loadCurrentState(sT = start_time,
                                         cT = current_time,
                                         value = controller.FX.FX_Line_1.FX2Knob.getState())

    TC.FxLine1K2Button.loadCurrentState(sT = start_time,
                                         cT = current_time,
                                         value = controller.FX.FX_Line_1.FX2Button.getPressed())
    TC.FxLine1K3.loadCurrentState(sT = start_time,
                                         cT = current_time,
                                         value = controller.FX.FX_Line_1.FX3Knob.getState())

    TC.FxLine1K3Button.loadCurrentState(sT = start_time,
                                         cT = current_time,
                                         value = controller.FX.FX_Line_1.FX3Button.getPressed())
    
    TC.FxLine2DW.loadCurrentState(sT = start_time,
                                         cT = current_time,
                                         value = controller.FX.FX_Line_2.DryWetKnob.getState())

    TC.FxLine2DWButton.loadCurrentState(sT = start_time,
                                         cT = current_time,
                                         value = controller.FX.FX_Line_2.DryWetButton.getPressed())
    TC.FxLine2K1.loadCurrentState(sT = start_time,
                                         cT = current_time,
                                         value = controller.FX.FX_Line_2.FX1Knob.getState())

    TC.FxLine2K1Button.loadCurrentState(sT = start_time,
                                         cT = current_time,
                                         value = controller.FX.FX_Line_2.FX1Button.getPressed())
    TC.FxLine2K2.loadCurrentState(sT = start_time,
                                         cT = current_time,
                                         value = controller.FX.FX_Line_2.FX2Knob.getState())

    TC.FxLine2K2Button.loadCurrentState(sT = start_time,
                                         cT = current_time,
                                         value = controller.FX.FX_Line_2.FX2Button.getPressed())
    TC.FxLine2K3.loadCurrentState(sT = start_time,
                                         cT = current_time,
                                         value = controller.FX.FX_Line_2.FX3Knob.getState())

    TC.FxLine2K3Button.loadCurrentState(sT = start_time,
                                         cT = current_time,
                                         value = controller.FX.FX_Line_2.FX3Button.getPressed())
    
    TC.Crossfader.loadCurrentState(sT = start_time,
                                   cT = current_time,
                                   value = controller.Mixer.FaderSection.CrossFader.getState())
    
    TC.LevelA.loadCurrentState(sT = start_time,
                                   cT = current_time,
                                   value = controller.Mixer.FaderSection.LevelA.getState())
    TC.LevelB.loadCurrentState(sT = start_time,
                                   cT = current_time,
                                   value = controller.Mixer.FaderSection.LevelB.getState())
    
    TC.HeadPhoneCueA.loadCurrentState(sT = start_time,
                                      cT = current_time,
                                      value = controller.Mixer.FaderSection.CueA.getPressed())
    TC.HeadPhoneCueB.loadCurrentState(sT = start_time,
                                      cT = current_time,
                                      value = controller.Mixer.FaderSection.CueB.getPressed())
    
    TC.BrowserEnc.loadCurrentState(sT = start_time,
                                      cT = current_time,
                                      value = controller.Mixer.MasterSection.BrowseEncoder.getState())
    
    TC.BrowseEncPress.loadCurrentState(sT = start_time,
                                      cT = current_time,
                                      value = controller.Mixer.MasterSection.BrowseEncoder.getPressed())
    TC.DeckALoad.loadCurrentState(sT = start_time,
                                  cT = current_time,
                                  value = controller.Mixer.MasterSection.LoadA.getPressed())
    TC.DeckBLoad.loadCurrentState(sT = start_time,
                                  cT = current_time,
                                  value = controller.Mixer.MasterSection.LoadB.getPressed())
    TC.MasterLevel.loadCurrentState(sT = start_time,
                                      cT = current_time,
                                      value = controller.Mixer.MasterSection.MasterLevel.getState())
    
    TC.DeckAFxEnc.loadCurrentState(sT = start_time,
                                      cT = current_time,
                                      value = controller.Mixer.EQ_A_Section.FXEncoder.getState())
    TC.DeckAFxEncPress.loadCurrentState(sT = start_time,
                                      cT = current_time,
                                      value = controller.Mixer.EQ_A_Section.FXEncoder.getPressed())
    TC.DeckAFxLine1Select.loadCurrentState(sT = start_time,
                                      cT = current_time,
                                      value = controller.Mixer.EQ_A_Section.FX1Select.getPressed())
    TC.DeckAFxLine2Select.loadCurrentState(sT = start_time,
                                      cT = current_time,
                                      value = controller.Mixer.EQ_A_Section.FX2Select.getPressed())
    TC.EqA_HI.loadCurrentState(sT = start_time,
                                      cT = current_time,
                                      value = controller.Mixer.EQ_A_Section.EQ_HI.getState())
    TC.EqA_MI.loadCurrentState(sT = start_time,
                                      cT = current_time,
                                      value = controller.Mixer.EQ_A_Section.EQ_MID.getState())
    TC.EqA_LO.loadCurrentState(sT = start_time,
                                      cT = current_time,
                                      value = controller.Mixer.EQ_A_Section.EQ_LO.getState())
    
    TC.DeckBFxEnc.loadCurrentState(sT = start_time,
                                      cT = current_time,
                                      value = controller.Mixer.EQ_B_Section.FXEncoder.getState())
    TC.DeckBFxEncPress.loadCurrentState(sT = start_time,
                                      cT = current_time,
                                      value = controller.Mixer.EQ_B_Section.FXEncoder.getPressed())
    TC.DeckBFxLine1Select.loadCurrentState(sT = start_time,
                                      cT = current_time,
                                      value = controller.Mixer.EQ_B_Section.FX1Select.getPressed())
    TC.DeckBFxLine2Select.loadCurrentState(sT = start_time,
                                      cT = current_time,
                                      value = controller.Mixer.EQ_B_Section.FX2Select.getPressed())
    TC.EqB_HI.loadCurrentState(sT = start_time,
                                      cT = current_time,
                                      value = controller.Mixer.EQ_B_Section.EQ_HI.getState())
    TC.EqB_MI.loadCurrentState(sT = start_time,
                                      cT = current_time,
                                      value = controller.Mixer.EQ_B_Section.EQ_MID.getState())
    TC.EqB_LO.loadCurrentState(sT = start_time,
                                      cT = current_time,
                                      value = controller.Mixer.EQ_B_Section.EQ_LO.getState())
    
def loadGlobals():
    # Loads global variables to be used in the program
    global pButsBuffer
    global pPotsBuffer
    with open('DefaultValues.csv', "r") as f:
        reader = csv.reader(f)
        lines = [[int(j) for j in i] for i in reader]
    pButsBuffer = lines[0]
    pPotsBuffer = lines[1]

## HID Packet Scripts 
def sample_handler(data):
    # Defention for the HID packet handler  
    process_sample(data)

def process_sample(data):
    # Processes a HID packet either recorded or live
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
    #p1rint(f"{pButsBuffer[1]}\t{pButsBuffer[2]}\t{pButsBuffer[3]}\t{pButsBuffer[4]}\t{str(time.time())[8:15]}\t{data[4]-pButsBuffer[4]}")
    if rec == '1':
        sample_to_file(data=data,filename=inputRecordingPath+fn)
    if data[0] == 1: # Button Buffer  
        #controller = loadControllerBBuffer(bBuff=data,controller=controller)
        for i in range(len(data)): 
            if pButsBuffer[i] != data[i]:
                print(f">        Change in byte\t{i}\tfrom\t{pButsBuffer[i]}\tto\t{data[i]}\tof\t{data[i]-pButsBuffer[i]}")
                #print(f"{DecodeButton(data,10,0)}\t{data[10]}")
                pass
        pButsBuffer = data
    elif data[0] == 2: # Knob Buffer  
        #controller = loadControllerPBuffer(pBuff=data,controller=controller)
        for i in range(len(data)):
            if pPotsBuffer[i] != data[i]:
                print(f">       Change in byte\t{i}\tfrom\t{pPotsBuffer[i]}\tto\t{data[i]}\tof\t{data[i]-pPotsBuffer[i]}")
                pass
        pPotsBuffer = data

def samples_from_file(filename = inputRecordingPath+"DefaultParasyteSessionFile.csv"):
    # Returns the samples from a file
    with open(filename, "r") as f:
        reader = csv.reader(f)
        lines = [i for i in reader]
        time = [i[0] for i in lines]
        data = [[int(j) for j in i[1:]] for i in lines]
    return time , data

def sample_to_file(data,filename = inputRecordingPath + "DefaultParasyteSessionFile.csv"):
    # Writes a Sample to file
    global start_time
    with open(filename,"a",newline = '') as f:
        writer = csv.writer(f)
        writer.writerow([time.time()- start_time]+data)

def samples_to_file(data,filename = inputRecordingPath + "DefaultParasyteSessionFile.csv"):
    # Writes samples to file
    global start_time
    with open(filename,"a",newline = '') as f:
        writer = csv.writer(f)
        writer.writerows([time.time()- start_time]+data)
    
def hid_device_connection(fn = '',rec=False):
    # Connect to a HID Device
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

## GUI Scripts
def ControllerLoader():
    # Defenition of ControllerLoader Thread
    # Continously loads the controller object with data
    global controller # Write Only
    global pButsBuffer # Read Only
    global pPotsBuffer # Read Only
    global do_Kon
    L_clock = pg.time.Clock()
    while do_Kon:
        controller = loadControllerBBuffer(bBuff=pButsBuffer,controller=controller)
        controller = loadControllerPBuffer(pBuff=pPotsBuffer,controller=controller)
        L_clock.tick(120)
        
def draw_ControllerGUI():
    # Thread to Draw Controller GUI
    global controller
    global do_Kon
    #KonLoad_Thread = Thread(target=ControllerLoader,args=())
    #KonLoad_Thread.start()
    ui = ControllerInterface()
    screen = ui.screen
    sp = 0
    down = False
    done = False
    white = [255,255,255]
    clock = ui.clock
    TC:TKS2MK2_TimeControl = loadTimeController()
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
        ##pg.draw.line(screen,255,[875,0],[875,875])
        ##pg.draw.line(screen,255,[0,875],[875,875])
        ##pg.draw.line(screen,255,[0,0],[875,875])
        
        updateTimeController(TC=TC)
        ##  Draw Deck A
        ##  A_JogWheel
        A_JogPos = [400,400]
        drawJog(screen=screen,fontObj=ui.fontObj,
                pos=A_JogPos,
                deg=controller.Deck_A.JogSection.Jog.getState()*(255/360),
                size=100,
                pressed= controller.Deck_A.JogSection.Jog.getPressed(),
                label="Test Jog",
                colour= TC.DeckAJog.colour,
                textSize=10)
        ## A_LoopSection
        A_LoopPos = [250,600]
        drawEnc(screen=screen,fontObj=ui.fontObj,
                pos=[A_LoopPos[0]+300,A_LoopPos[1]],
                deg=22.5*controller.Deck_A.LoopSection.Left_Encoder.getState(),
                size=30,
                pressed=controller.Deck_A.LoopSection.Left_Encoder.getPressed(),
                colour=TC.DeckALoopEncL.colour,
                label="Deck A L Enc",
                textSize=10)
        
        drawEnc(screen=screen,fontObj=ui.fontObj,
                pos=[A_LoopPos[0],A_LoopPos[1]],
                deg=22.5*controller.Deck_A.LoopSection.Right_Encoder.getState(),
                size=30,
                pressed=controller.Deck_A.LoopSection.Right_Encoder.getPressed(),
                colour=TC.DeckALoopEncR.colour,
                label="Deck A R Enc",
                textSize=10)
        
        drawBtn(screen=screen,fontObj=ui.fontObj,
                pos=[A_LoopPos[0]+100,A_LoopPos[1]],
                label="IN",
                size=40,textSize=10,
                pressed = controller.Deck_A.LoopSection.In.getPressed(),
                colour=TC.DeckALoopIn.colour)
        
        drawBtn(screen=screen,fontObj=ui.fontObj,
                pos=[A_LoopPos[0]+200,A_LoopPos[1]],
                label="OUT",
                size=40,textSize=10,
                pressed = controller.Deck_A.LoopSection.Out.getPressed(),
                colour=TC.DeckALoopOut.colour)
        ##  A_HotCue
        A_HotCuePos = [250,700]
        drawBtn(screen=screen,fontObj=ui.fontObj,
                pos=[A_HotCuePos[0],A_HotCuePos[1]],
                label="HotCue1",
                size=40,textSize=10,
                pressed = controller.Deck_A.HotCueSection.Cue1.getPressed(),
                colour=TC.DeckAHot1.colour)
        drawBtn(screen=screen,fontObj=ui.fontObj,
                pos=[A_HotCuePos[0]+100,A_HotCuePos[1]],
                label="HotCue2",
                size=40,textSize=10,
                pressed = controller.Deck_A.HotCueSection.Cue2.getPressed(),
                colour=TC.DeckAHot2.colour)
        drawBtn(screen=screen,fontObj=ui.fontObj,
                pos=[A_HotCuePos[0]+200,A_HotCuePos[1]],
                label="HotCue3",
                size=40,textSize=10,
                pressed = controller.Deck_A.HotCueSection.Cue3.getPressed(),
                colour=TC.DeckAHot3.colour)
        drawBtn(screen=screen,fontObj=ui.fontObj,
                pos=[A_HotCuePos[0]+300,A_HotCuePos[1]],
                label="HotCue4",
                size=40,textSize=10,
                pressed = controller.Deck_A.HotCueSection.Cue4.getPressed(),
                colour=TC.DeckAHot4.colour)
        ##  A_Transport
        A_TransportPos = [250,800]
        drawBtn(screen=screen,fontObj=ui.fontObj,
                pos=[A_TransportPos[0],A_TransportPos[1]],
                label="Shift",
                size=40,textSize=10,
                pressed = controller.Deck_A.TransportSection.Shift.getPressed(),
                colour=TC.DeckAShift.colour)
        drawBtn(screen=screen,fontObj=ui.fontObj,
                pos=[A_TransportPos[0]+100,A_TransportPos[1]],
                label="Sync",
                size=40,textSize=10,
                pressed = controller.Deck_A.TransportSection.Sync.getPressed(),
                colour=TC.DeckASync.colour)
        drawBtn(screen=screen,fontObj=ui.fontObj,
                pos=[A_TransportPos[0]+200,A_TransportPos[1]],
                label="Cue",
                size=40,textSize=10,
                pressed = controller.Deck_A.TransportSection.Cue.getPressed(),
                colour=TC.DeckACue.colour)
        drawBtn(screen=screen,fontObj=ui.fontObj,
                pos=[A_TransportPos[0]+300,A_TransportPos[1]],
                label="Play",
                size=40,textSize=10,
                pressed = controller.Deck_A.TransportSection.Play.getPressed(),
                colour=TC.DeckAPlay.colour)
        ## A_Tempo
        A_TempoPos = [100,530]
        drawVFad(screen= screen,fontObj=ui.fontObj,
                pos=[A_TempoPos[0],A_TempoPos[1]],
                size=[80,300],
                percentage=100-prep16BitEncoderState(controller.Deck_A.TempoSection.Tempo_Slider.getState()),
                label="Deck A Tempo",
                textSize=10,
                colour=TC.DeckATempoSlider.colour
                )
        drawCBtn(screen=screen,fontObj=ui.fontObj,
                pos=[A_TempoPos[0]+40,A_TempoPos[1]-50],
                label="Flux",
                size=15,textSize=10,
                pressed = controller.Deck_A.TempoSection.Flux.getPressed(),
                colour=TC.DeckAFlux.colour)

        ##  Draw Deck B
        ##  B_JogWheel
        B_JogPos = [1350,400]
        drawJog(screen=screen,fontObj=ui.fontObj,
                pos=B_JogPos,
                deg=controller.Deck_B.JogSection.Jog.getState()*(255/360),
                size=100,
                pressed= controller.Deck_B.JogSection.Jog.getPressed(),
                label="Test Jog",
                colour=TC.DeckBJog.colour,
                textSize=10)
        ## B_LoopSection
        B_LoopPos = [1200,600]
        drawEnc(screen=screen,fontObj=ui.fontObj,
                pos=[B_LoopPos[0],B_LoopPos[1]],
                deg=22.5*controller.Deck_B.LoopSection.Left_Encoder.getState(),
                size=30,
                pressed=controller.Deck_B.LoopSection.Left_Encoder.getPressed(),
                label="Deck B L Enc",
                colour=TC.DeckBLoopEncL.colour,
                textSize=10)
        
        drawEnc(screen=screen,fontObj=ui.fontObj,
                pos=[B_LoopPos[0]+300,B_LoopPos[1]],
                deg=22.5*controller.Deck_B.LoopSection.Right_Encoder.getState(),
                size=30,
                pressed=controller.Deck_B.LoopSection.Right_Encoder.getPressed(),
                label="Deck B R Enc",
                colour=TC.DeckBLoopEncR.colour,
                textSize=10)
        
        drawBtn(screen=screen,fontObj=ui.fontObj,
                pos=[B_LoopPos[0]+100,B_LoopPos[1]],
                label="IN",
                size=40,textSize=10,
                pressed = controller.Deck_B.LoopSection.In.getPressed(),
                colour=TC.DeckBLoopIn.colour)
        
        drawBtn(screen=screen,fontObj=ui.fontObj,
                pos=[B_LoopPos[0]+200,B_LoopPos[1]],
                label="OUT",
                size=40,textSize=10,
                pressed = controller.Deck_B.LoopSection.Out.getPressed(),
                colour=TC.DeckBLoopOut.colour)
        ##  B_HotCue
        B_HotCuePos = [1200,700]
        drawBtn(screen=screen,fontObj=ui.fontObj,
                pos=[B_HotCuePos[0],B_HotCuePos[1]],
                label="HotCue1",
                size=40,textSize=10,
                pressed = controller.Deck_B.HotCueSection.Cue1.getPressed(),
                colour=TC.DeckBHot1.colour)
        drawBtn(screen=screen,fontObj=ui.fontObj,
                pos=[B_HotCuePos[0]+100,B_HotCuePos[1]],
                label="HotCue2",
                size=40,textSize=10,
                pressed = controller.Deck_B.HotCueSection.Cue2.getPressed(),
                colour=TC.DeckBHot2.colour)
        drawBtn(screen=screen,fontObj=ui.fontObj,
                pos=[B_HotCuePos[0]+200,B_HotCuePos[1]],
                label="HotCue3",
                size=40,textSize=10,
                pressed = controller.Deck_B.HotCueSection.Cue3.getPressed(),
                colour=TC.DeckBHot3.colour)
        drawBtn(screen=screen,fontObj=ui.fontObj,
                pos=[B_HotCuePos[0]+300,B_HotCuePos[1]],
                label="HotCue4",
                size=40,textSize=10,
                pressed = controller.Deck_B.HotCueSection.Cue4.getPressed(),
                colour=TC.DeckBHot4.colour)
        
        ##  B_Transport
        B_TransportPos = [1200,800]
        drawBtn(screen=screen,fontObj=ui.fontObj,
                pos=[B_TransportPos[0],B_TransportPos[1]],
                label="Shift",
                size=40,textSize=10,
                pressed = controller.Deck_B.TransportSection.Shift.getPressed(),
                colour=TC.DeckBShift.colour)
        drawBtn(screen=screen,fontObj=ui.fontObj,
                pos=[B_TransportPos[0]+100,B_TransportPos[1]],
                label="Sync",
                size=40,textSize=10,
                pressed = controller.Deck_B.TransportSection.Sync.getPressed(),
                colour=TC.DeckBSync.colour)
        drawBtn(screen=screen,fontObj=ui.fontObj,
                pos=[B_TransportPos[0]+200,B_TransportPos[1]],
                label="Cue",
                size=40,textSize=10,
                pressed = controller.Deck_B.TransportSection.Cue.getPressed(),
                colour=TC.DeckBCue.colour)
        drawBtn(screen=screen,fontObj=ui.fontObj,
                pos=[B_TransportPos[0]+300,B_TransportPos[1]],
                label="Play",
                size=40,textSize=10,
                pressed = controller.Deck_B.TransportSection.Play.getPressed(),
                colour=TC.DeckBPlay.colour)
        ## B_Tempo
        B_TempoPos = [1550,530] ## +350
        drawVFad(screen= screen,fontObj=ui.fontObj,
                pos=[B_TempoPos[0],B_TempoPos[1]],
                size=[80,300],
                percentage=100-prep16BitEncoderState(controller.Deck_B.TempoSection.Tempo_Slider.getState()),
                label="Deck B Tempo",
                textSize=10,
                colour=TC.DeckBTempoSlider.colour
                )
        drawCBtn(screen=screen,fontObj=ui.fontObj,
                pos=[B_TempoPos[0]+40,B_TempoPos[1]-50],
                label="Flux",
                size=15,textSize=10,
                pressed = controller.Deck_B.TempoSection.Flux.getPressed(),
                colour=TC.DeckBFlux.colour)

        ## FX Line 1
        FX1Pos = [100,100]
        ##buttons
        drawCBtn(screen=screen,fontObj=ui.fontObj,
                pos=[FX1Pos[0]+50,FX1Pos[1]+50],
                label="Dry/Wet",
                size=15,textSize=10,
                pressed = controller.FX.FX_Line_1.DryWetButton.getPressed(),
                colour=TC.FxLine1DWButton.colour)

        drawCBtn(screen=screen,fontObj=ui.fontObj,
                pos=[FX1Pos[0]+150,FX1Pos[1]+50],
                label="FX 1",
                size=15,textSize=10,
                pressed = controller.FX.FX_Line_1.FX1Button.getPressed(),
                colour=TC.FxLine1K1Button.colour)

        drawCBtn(screen=screen,fontObj=ui.fontObj,
                pos=[FX1Pos[0]+250,FX1Pos[1]+50],
                label="FX 2",
                size=15,textSize=10,
                pressed = controller.FX.FX_Line_1.FX2Button.getPressed(),
                colour=TC.FxLine1K2Button.colour)

        drawCBtn(screen=screen,fontObj=ui.fontObj,
                pos=[FX1Pos[0]+350,FX1Pos[1]+50],
                label="FX 2",
                size=15,textSize=10,
                pressed = controller.FX.FX_Line_1.FX3Button.getPressed(),
                colour=TC.FxLine1K3Button.colour)

        drawKnb(screen=screen,fontObj=ui.fontObj,
                pos=[FX1Pos[0],FX1Pos[1]],
                deg=prep16BitKnobState(controller.FX.FX_Line_1.DryWetKnob.getState()),
                size=20, textSize=10,
                label="Dry/Wet",
                colour=TC.FxLine1DW.colour)

        drawKnb(screen=screen,fontObj=ui.fontObj,
                pos=[FX1Pos[0]+100,FX1Pos[1]],
                deg=prep16BitKnobState(controller.FX.FX_Line_1.FX1Knob.getState()),
                size=20, textSize=10,
                label="FX 1",
                colour=TC.FxLine1K1.colour)
        
        drawKnb(screen=screen,fontObj=ui.fontObj,
                pos=[FX1Pos[0]+200,FX1Pos[1]],
                deg=prep16BitKnobState(controller.FX.FX_Line_1.FX2Knob.getState()),
                size=20, textSize=10,
                label="FX 2",
                colour=TC.FxLine1K2.colour)
        
        drawKnb(screen=screen,fontObj=ui.fontObj,
                pos=[FX1Pos[0]+300,FX1Pos[1]],
                deg=prep16BitKnobState(controller.FX.FX_Line_1.FX3Knob.getState()),
                size=20, textSize=10,
                label="FX 3",
                colour=TC.FxLine1K3.colour)
        
         ## FX Line 2
        FX2Pos = [1250,100]
        ##buttons
        drawCBtn(screen=screen,fontObj=ui.fontObj,
                pos=[FX2Pos[0]+50,FX2Pos[1]+50],
                label="Dry/Wet",
                size=15,textSize=10,
                pressed = controller.FX.FX_Line_2.DryWetButton.getPressed(),
                colour=TC.FxLine2DWButton.colour)

        drawCBtn(screen=screen,fontObj=ui.fontObj,
                pos=[FX2Pos[0]+150,FX2Pos[1]+50],
                label="FX 1",
                size=15,textSize=10,
                pressed = controller.FX.FX_Line_2.FX1Button.getPressed(),
                colour=TC.FxLine2K1Button.colour)

        drawCBtn(screen=screen,fontObj=ui.fontObj,
                pos=[FX2Pos[0]+250,FX2Pos[1]+50],
                label="FX 2",
                size=15,textSize=10,
                pressed = controller.FX.FX_Line_2.FX2Button.getPressed(),
                colour=TC.FxLine2K2Button.colour)

        drawCBtn(screen=screen,fontObj=ui.fontObj,
                pos=[FX2Pos[0]+350,FX2Pos[1]+50],
                label="FX 2",
                size=15,textSize=10,
                pressed = controller.FX.FX_Line_2.FX3Button.getPressed(),
                colour=TC.FxLine2K3Button.colour)

        drawKnb(screen=screen,fontObj=ui.fontObj,
                pos=[FX2Pos[0],FX2Pos[1]],
                deg=prep16BitKnobState(controller.FX.FX_Line_2.DryWetKnob.getState()),
                size=20, textSize=10,
                label="Dry/Wet",
                colour=TC.FxLine2DW.colour)

        drawKnb(screen=screen,fontObj=ui.fontObj,
                pos=[FX2Pos[0]+100,FX2Pos[1]],
                deg=prep16BitKnobState(controller.FX.FX_Line_2.FX1Knob.getState()),
                size=20, textSize=10,
                label="FX 1",
                colour=TC.FxLine2K1.colour)
        
        drawKnb(screen=screen,fontObj=ui.fontObj,
                pos=[FX2Pos[0]+200,FX2Pos[1]],
                deg=prep16BitKnobState(controller.FX.FX_Line_2.FX2Knob.getState()),
                size=20, textSize=10,
                label="FX 2",
                colour=TC.FxLine2K2.colour)
        
        drawKnb(screen=screen,fontObj=ui.fontObj,
                pos=[FX2Pos[0]+300,FX2Pos[1]],
                deg=prep16BitKnobState(controller.FX.FX_Line_2.FX3Knob.getState()),
                size=20, textSize=10,
                label="FX 3",
                colour=TC.FxLine2K3.colour)
    
        ## Mixer
        MixerPos = [875,875]
        ## Levels
        drawBtn(screen=screen,fontObj=ui.fontObj,
                pos=[MixerPos[0]-170,MixerPos[1]-450],
                label="Cue A",
                size=20,textSize=10,
                pressed = controller.Mixer.FaderSection.CueA.getPressed(),
                colour=TC.HeadPhoneCueA.colour)
        drawVFad(screen= screen,fontObj=ui.fontObj,
                pos=[MixerPos[0]-210,MixerPos[1]-400],
                size=[80,200],
                percentage=100-prep16BitEncoderState(controller.Mixer.FaderSection.LevelA.getState()),
                label="Deck A Level",
                colour=TC.LevelA.colour,
                textSize=10
                )
        
        drawBtn(screen=screen,fontObj=ui.fontObj,
                pos=[MixerPos[0]+185,MixerPos[1]-450],
                label="Cue B",
                size=20,textSize=10,
                pressed = controller.Mixer.FaderSection.CueB.getPressed(),
                colour=TC.HeadPhoneCueB.colour)
        
        drawVFad(screen= screen,fontObj=ui.fontObj,
                pos=[MixerPos[0]+150,MixerPos[1]-400],
                size=[80,200],
                percentage=100-prep16BitEncoderState(controller.Mixer.FaderSection.LevelB.getState()),
                label="Deck B Level",
                textSize=10,
                colour=TC.LevelB.colour
                )
        
        drawHFad(screen= screen,fontObj=ui.fontObj,
                pos=[MixerPos[0]-150,MixerPos[1]-100],
                size=[300,80],
                percentage=prep16BitEncoderState(controller.Mixer.FaderSection.CrossFader.getState()),
                label="Crossfader",
                colour=TC.Crossfader.colour,
                textSize=10
                )
        ## Master
        drawEnc(screen=screen,fontObj=ui.fontObj,
                pos=[MixerPos[0],MixerPos[1]-400],
                deg=22.5*(controller.Mixer.MasterSection.BrowseEncoder.getState()),
                pressed= controller.Mixer.MasterSection.BrowseEncoder.getPressed(),
                size=20, textSize=10,
                colour=TC.BrowserEnc.colour,
                label="Browse")#,
                #colour=white)
        drawCBtn(screen=screen,fontObj=ui.fontObj,
                pos=[MixerPos[0]-50,MixerPos[1]-350],
                label="Load A",
                size=10,textSize=10,
                colour=TC.DeckALoad.colour,
                pressed = controller.Mixer.MasterSection.LoadA.getPressed())
        drawCBtn(screen=screen,fontObj=ui.fontObj,
                pos=[MixerPos[0]+50,MixerPos[1]-350],
                label="Load B",
                colour=TC.DeckBLoad.colour,
                size=10,textSize=10,
                pressed = controller.Mixer.MasterSection.LoadB.getPressed())
        
        drawKnb(screen=screen,fontObj=ui.fontObj,
                pos=[MixerPos[0],MixerPos[1]-800],
                deg=prep16BitKnobState(controller.Mixer.MasterSection.MasterLevel.getState()),
                size=20, textSize=10,
                label="Master",
                colour=TC.MasterLevel.colour)

        ## Line A
        drawKnb(screen=screen,fontObj=ui.fontObj,
                pos=[MixerPos[0]-75,MixerPos[1]-500],
                deg=prep16BitKnobState(controller.Mixer.EQ_A_Section.EQ_LO.getState()),
                size=20, textSize=10,
                label="Low",
                colour=TC.EqA_LO.colour)
        drawKnb(screen=screen,fontObj=ui.fontObj,
                pos=[MixerPos[0]-75,MixerPos[1]-600],
                deg=prep16BitKnobState(controller.Mixer.EQ_A_Section.EQ_MID.getState()),
                size=20, textSize=10,
                label="Mid",
                colour=TC.EqA_MI.colour)
        
        drawKnb(screen=screen,fontObj=ui.fontObj,
                pos=[MixerPos[0]-75,MixerPos[1]-700],
                deg=prep16BitKnobState(controller.Mixer.EQ_A_Section.EQ_HI.getState()),
                size=20, textSize=10,
                label="High",
                colour=TC.EqA_HI.colour)
        
        drawEnc(screen=screen,fontObj=ui.fontObj,
                pos=[MixerPos[0]-250,MixerPos[1]-700],
                deg=22.5*(controller.Mixer.EQ_A_Section.FXEncoder.getState()),
                pressed= controller.Mixer.EQ_A_Section.FXEncoder.getPressed(),
                size=20, textSize=10,
                label="Gain/FX",
                colour=TC.DeckAFxEnc.colour)
        drawCBtn(screen=screen,fontObj=ui.fontObj,
                pos=[MixerPos[0]-300,MixerPos[1]-650],
                label="FX1",
                size=10,textSize=10,
                pressed = controller.Mixer.EQ_A_Section.FX1Select.getPressed(),
                colour=TC.DeckAFxLine1Select.colour)
        drawCBtn(screen=screen,fontObj=ui.fontObj,
                pos=[MixerPos[0]-200,MixerPos[1]-650],
                label="FX2",
                size=10,textSize=10,
                pressed = controller.Mixer.EQ_A_Section.FX2Select.getPressed(),
                colour=TC.DeckAFxLine2Select.colour)

        ## Line B
        drawKnb(screen=screen,fontObj=ui.fontObj,
                pos=[MixerPos[0]+75,MixerPos[1]-500],
                deg=prep16BitKnobState(controller.Mixer.EQ_B_Section.EQ_LO.getState()),
                size=20, textSize=10,
                label="Low",
                colour=TC.EqB_LO.colour)
        drawKnb(screen=screen,fontObj=ui.fontObj,
                pos=[MixerPos[0]+75,MixerPos[1]-600],
                deg=prep16BitKnobState(controller.Mixer.EQ_B_Section.EQ_MID.getState()),
                size=20, textSize=10,
                label="Mid",
                colour=TC.EqB_MI.colour)
        
        drawKnb(screen=screen,fontObj=ui.fontObj,
                pos=[MixerPos[0]+75,MixerPos[1]-700],
                deg=prep16BitKnobState(controller.Mixer.EQ_B_Section.EQ_HI.getState()),
                size=20, textSize=10,
                label="High",
                colour=TC.EqB_HI.colour)
        
        drawEnc(screen=screen,fontObj=ui.fontObj,
                pos=[MixerPos[0]+250,MixerPos[1]-700],
                deg=22.5*(controller.Mixer.EQ_B_Section.FXEncoder.getState()),
                pressed= controller.Mixer.EQ_B_Section.FXEncoder.getPressed(),
                size=20, textSize=10,
                label="Gain/FX",
                colour=TC.DeckBFxEnc.colour)
        drawCBtn(screen=screen,fontObj=ui.fontObj,
                pos=[MixerPos[0]+300,MixerPos[1]-650],
                label="FX1",
                size=10,textSize=10,
                pressed = controller.Mixer.EQ_B_Section.FX1Select.getPressed(),
                colour=TC.DeckBFxLine1Select.colour)
        drawCBtn(screen=screen,fontObj=ui.fontObj,
                pos=[MixerPos[0]+200,MixerPos[1]-650],
                label="FX2",
                size=10,textSize=10,
                pressed = controller.Mixer.EQ_B_Section.FX2Select.getPressed(),
                colour=TC.DeckBFxLine2Select.colour)
        renderText(screen,ui.fontObj,f"mouse_pos = ({pg.mouse.get_pos()})",[pg.mouse.get_pos()[0]+85,pg.mouse.get_pos()[1]+10],[255,255,255],size=10)  
        sp = (sp + 1) % 360
        pg.display.flip()

        clock.tick(60)
   
    pg.quit()
    do_Kon = False
    #Gui_Thread.join()


## MAIN
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
    global start_time
    global current_time
    start_time = time.time()
    current_time = time.time()
    
    controller = loadController()
    #pg.mixer.init() 
    loadGlobals()
    Gui_Thread = Thread(target=draw_ControllerGUI,args=())
    KonLoad_Thread = Thread(target=ControllerLoader,args=())
    
    mode = input("\nConnect to Hid or Replay from file?\n1 -\tHid Device Connection\n2 -\tReplay From File\n3 -\tReplay From File (With Audio)\n4 -\tDebug Screen\n5 -\tQuit\n> ")
    GUI = input("\nEnable GUI?\n1 - Yes\n0 - No\n> ")
    rec = 'NO'
    if mode == "1":
        rec = input("\nWould you like to record to a file?\n1 - Yes\nAny Key - No\n> ")
        fn = datetime.datetime.now().__str__().replace(":","_").replace(".","_").replace("-","_") + "_SessionFile.csv"
        if GUI != '1':
            hid_device_connection()
            
        else:
            KonLoad_Thread.start()
            Gui_Thread.start()
            hid_device_connection()
            #Gui_Thread.join()    
            KonLoad_Thread.join()       
    elif mode == "2":
        if GUI == '1':
            Gui_Thread.start()
            KonLoad_Thread.start()
        times,data = samples_from_file(inputRecordingPath + "AFXBUTTONSTHENKNOBS.csv")
       
        start_time = time.time()
        
        for i,sample in enumerate(data):
            while float(times[i]) > float(time.time()-start_time):
                ##  Spinlock
                pass
            print(time.time()-start_time)
            print(str(times[i])[:5],end="\t") 
            process_sample(sample)
        #Gui_Thread.join()
        KonLoad_Thread.join()
    elif mode == "3":
        if GUI == '1':
            Gui_Thread.start()
            KonLoad_Thread.start()
        times,data = samples_from_file(inputRecordingPath + "2025_03_08 18_04_33_499196_SessionFile.csv")
        audio = "audio.wav"
        audio_start = 80.066
        audio_play = False
       
        pg.mixer.music.load(audio)
        start_time = time.time()
        
        for i,sample in enumerate(data):
            while float(times[i]) > float(time.time()-start_time+60):
                ##  Spinlock
                pass
            print(time.time()-start_time )
            if audio_play == False and float(time.time()-start_time+60) >= audio_start:
                audio_play = True
                pg.mixer.music.play()
            print(str(times[i])[:5],end="\t") 
            process_sample(sample)
        #Gui_Thread.join()
        KonLoad_Thread.join()
    elif mode == "4":
        Gui_Thread.start()
    elif mode == "5":
        quit()
    elif mode == "P1S1":
        if GUI == '1':
            Gui_Thread.start()
            KonLoad_Thread.start()
        times,data = samples_from_file(inputRecordingPath + "2025_03_12 21_19_09_759864_SessionFile.csv")
        audio = "Participant1Set1.wav"
        audio_start = 11.82
        audio_play = False
       
        pg.mixer.music.load(audio)
        start_time = time.time()
        
        for i,sample in enumerate(data):
            while float(times[i]) > float(time.time()-start_time):
                ##  Spinlock
                pass
            print(time.time()-start_time )
            if audio_play == False and float(time.time()-start_time) >= audio_start:
                audio_play = True
                pg.mixer.music.play()
            print(str(times[i])[:5],end="\t") 
            process_sample(sample)
        #Gui_Thread.join()
        KonLoad_Thread.join()
    elif mode == "SWMN":
        if GUI == '1':
            Gui_Thread.start()
            KonLoad_Thread.start()
        times,data = samples_from_file(inputRecordingPath + "2025_04_02 19_45_20_866602_SessionFile.csv")
        audio = "SWMNTest1.wav"
        audio_start = 14
        audio_play = False
       
        pg.mixer.music.load(audio)
        start_time = time.time()
        
        for i,sample in enumerate(data):
            while float(times[i]) > float(time.time()-start_time):
                ##  Spinlock
                pass
            print(time.time()-start_time )
            if audio_play == False and float(time.time()-start_time) >= audio_start:
                audio_play = True
                pg.mixer.music.play()
            print(str(times[i])[:5],end="\t") 
            process_sample(sample)
        #Gui_Thread.join()
        KonLoad_Thread.join()



