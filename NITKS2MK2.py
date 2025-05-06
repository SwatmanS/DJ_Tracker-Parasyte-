class Button:
    def __init__(self,name = 'untitled button'):
        self.name = name
        self.pressed = False
        pass
    def setName(self,name):
        self.name = name
        return name
    def getName(self):
        return self.name
    def setPressed(self,state):
        self.pressed = state
        return self.pressed
    def getPressed(self):
        return self.pressed
    
class Knob:
    def __init__(self,name = 'untitled Knob',High = 4096,Low = 0, value = 0):
        self.name = name
        self.high = High
        self.low = Low
        self.value = value
    def setName(self,name):
        self.name = name
        return name
    def getName(self):
        return self.name
    def setState(self,value):
        self.value = value
        return self.value
    def getState(self):
        return self.value
    def setBounds(self,Low,High):
        self.high = High
        self.low = Low
        return [self.Low,self.High]
    def getBounds(self):
        return [self.Low,self.High]

class Encoder:
    def __init__(self,name = 'untitled Encoder',High = 4096,Low = 0, value = 0,pressed=False):
        self.name = name
        self.high = High
        self.low = Low
        self.value = value
        self.pressed = False
    def setName(self,name):
        self.name = name
        return name
    def getName(self):
        return self.name
    def setState(self,value):
        self.value = value
        return self.value
    def getState(self):
        return self.value
    def setBounds(self,Low,High):
        self.high = High
        self.low = Low
        return [self.Low,self.High]
    def getBounds(self):
        return [self.Low,self.High]
    def setPressed(self,state):
        self.pressed = state
        return self.pressed
    def getPressed(self):
        return self.pressed

class Jog:
    def __init__(self,name = 'untitled Encoder',High = 360,Low = 0, value = 0,pressed=False):
        self.name = name
        self.high = High
        self.low = Low
        self.value = value
        self.pressed = pressed
    def setName(self,name):
        self.name = name
        return name
    def getName(self):
        return self.name
    def setState(self,value):
        self.value = value
        return self.value
    def getState(self):
        return self.value
    def setBounds(self,Low,High):
        self.high = High
        self.low = Low
        return [self.Low,self.High]
    def getBounds(self):
        return [self.Low,self.High]
    def setPressed(self,state):
        self.pressed = state
        return self.pressed
    def getPressed(self):
        return self.pressed

class Slider:
    def __init__(self,name = 'untitled Slider',High = 4096 ,Low = 0, value = 0):
        self.name = name
        self.high = High
        self.low = Low
        self.value = value
    def setName(self,name):
        self.name = name
        return name
    def getName(self):
        return self.name
    def setState(self,value):
        self.value = value
        return self.value
    def getState(self):
        return self.value
    def setBounds(self,Low,High):
        self.high = High
        self.low = Low
        return [self.Low,self.High]
    def getBounds(self):
        return [self.Low,self.High]
    
class encoderBounds:
    def __init__(self,High = 4096,Low = 0,Value = 0):
        self.hi = High
        self.lo = Low
        self.val = Value

class Hotcue:
    def __init__(self,name):
        self.name = name
        self.Cue1 = Button("HotCue1")
        self.Cue2 = Button("HotCue2")
        self.Cue3 = Button("HotCue3")
        self.Cue4 = Button("HotCue4")

class Transport:
    def __init__(self,name):
        self.name = name
        self.Shift = Button("Shift")
        self.Sync = Button("Sync")
        self.Play = Button("Name")
        self.Cue = Button("Cue")
    

class Tempo:
    def __init__(self,name,s_high = 4096,s_low = 0,s_value = 0):
        self.name = name
        self.Flux = Button("Flux")
        self.Tempo_Slider = Slider("Tempo Slider",s_low,s_high,s_value)

class Jogs:
    def __init__(self,name,s_high = 360,s_low = 0,s_value = 0):
        self.name = name
        self.Jog = Jog("Jog Button",s_high,s_low,s_value)

class Loops:
    def __init__(self,name,l_high = 4096,l_low = 0,l_value = 0,r_high = 4096,r_low = 0,r_value = 0):
        self.name = name
        self.In = Button("In")
        self.Out = Button("Out")
        self.Left_Encoder = Encoder("Left Encoder",l_high,l_low,l_value)
        self.Right_Encoder = Encoder("Right Encoder",r_high,r_low,r_value)

class Deck:
    def __init__(self,name,l_high = 4096,l_low = 0,l_value = 0,r_high = 4096,r_low = 0,r_value = 0,s_high = 4096,s_low = 0,s_value = 0,j_high = 4096,j_low = 0,j_value = 0):
        self.name = name
        self.LoopSection = Loops("LoopSection",l_high,l_low,l_value,r_high,r_low,r_value)
        self.JogSection = Jogs("JogSection",j_high,j_low,j_value)
        self.TempoSection = Tempo("TempoSection",s_high,s_low,s_value)
        self.TransportSection = Transport("TransportSection")
        self.HotCueSection = Hotcue("HotCueSection")

class Faders:
    def __init__(self,name,a_Bounds:encoderBounds,b_Bounds:encoderBounds,c_Bounds:encoderBounds):
        self.name = name
        self.CueA = Button("CueA")
        self.CueB = Button("CueB")
        self.LevelA = Slider("LevelA",a_Bounds.hi,a_Bounds.lo,a_Bounds.val)
        self.LevelB = Slider("LevelA",b_Bounds.hi,b_Bounds.lo,b_Bounds.lo)
        self.CrossFader = Slider("LevelA",c_Bounds.hi,c_Bounds.lo,c_Bounds.lo)

class FaderBoundStruct:
    def __init__(self,a_Bound,b_Bound,c_Bound):
        self.a = a_Bound
        self.b = b_Bound
        self.c = c_Bound

class EQ:
    def __init__(self,name,hi_Bounds,mid_Bounds,lo_Bounds,enc_Bounds):
        self.name = name
        self.FX1Select = Button("FX1Select")
        self.FX2Select = Button("FX2Select")
        self.FXEncoder = Encoder("FxEncoder",enc_Bounds.hi,enc_Bounds.lo,enc_Bounds.val)
        self.EQ_HI = Knob("EQ_High",hi_Bounds.hi,hi_Bounds.lo,hi_Bounds.val)
        self.EQ_MID = Knob("EQ_Mids",mid_Bounds.hi,mid_Bounds.lo,mid_Bounds.val)
        self.EQ_LO = Knob("EQ_Lows",lo_Bounds.hi,lo_Bounds.lo,lo_Bounds.val)

class EQBoundStruct:
    def __init__(self,hi_Bounds:encoderBounds,mid_Bounds:encoderBounds,lo_Bounds:encoderBounds,enc_Bounds:encoderBounds):
        self.hi_Bounds = hi_Bounds
        self.mid_Bounds = mid_Bounds
        self.lo_Bounds = lo_Bounds
        self.enc_Bounds = enc_Bounds

class MasterBoundStruct:
    def __init__(self,m_Bounds,b_Bounds,r_Bounds):
        self.m_Bounds = m_Bounds
        self.r_Bounds = r_Bounds
        self.b_Bounds = b_Bounds

class Master:
    def __init__(self,name,m_Bounds,b_Bounds,r_Bounds):
        self.name = name
        self.MasterLevel = Knob("MasterLevel",m_Bounds.hi,m_Bounds.lo,m_Bounds.val)
        self.BrowseEncoder = Encoder("BrowserEncoder",b_Bounds.hi,b_Bounds.lo,b_Bounds.val)
        self.LoadA = Button("LoadA")
        self.LoadB = Button("LoadB")
        self.RemixA = Button("RemixA")
        self.RemixB = Button("RemixB")
        self.RemixLevel = Knob("RemixLevel",r_Bounds.hi,r_Bounds.lo,r_Bounds.val)

class Mixer:
    def __init__(self,name,f:FaderBoundStruct,e1:EQBoundStruct,e2:EQBoundStruct,m:MasterBoundStruct):
        self.name = name
        self.MasterSection = Master("MasterSection",m.m_Bounds,m.b_Bounds,m.r_Bounds)
        self.EQ_A_Section = EQ("EQ_A_Section",e1.hi_Bounds,e1.mid_Bounds,e1.lo_Bounds,e1.enc_Bounds)
        self.EQ_B_Section = EQ("EQ_B_Section",e2.hi_Bounds,e2.mid_Bounds,e2.lo_Bounds,e2.enc_Bounds)
        self.FaderSection = Faders("FadersSection",f.a,f.b,f.c)

class FXBoundsStruct:
    def __init__(self,dw_Bound=encoderBounds(),FX1_Bound=encoderBounds(),FX2_Bound=encoderBounds(),FX3_Bound=encoderBounds()):
        self.dw = dw_Bound
        self.fx1 = FX1_Bound
        self.fx2 = FX2_Bound
        self.fx3 = FX3_Bound

class FX_Line:
    def __init__(self,name,f:FXBoundsStruct):
          self.name = name
          self.DryWetButton = Button("DryWetButton")
          self.FX1Button = Button("FX1Button")
          self.FX2Button = Button("FX2Button")
          self.FX3Button = Button("FX3Button")
          
          self.DryWetKnob = Knob("DryWetKnob",f.dw.hi,f.dw.lo,f.dw.val)
          self.FX1Knob = Knob("FX1Knob",f.fx1.hi,f.fx1.lo,f.fx1.val)
          self.FX2Knob = Knob("FX2Knob",f.fx2.hi,f.fx2.lo,f.fx2.val)
          self.FX3Knob = Knob("FX1Knob",f.fx3.hi,f.fx3.lo,f.fx3.val)
          


class FX:
    def __init__(self,name,FX1_Bounds,FX2_Bounds):
        self.name = name
        self.FX_Line_1 = FX_Line("FX_Line_1",FX1_Bounds)
        self.FX_Line_2 = FX_Line("FX_Line_2",FX2_Bounds)

class DeckBuffer:
    def __init__(self,):
        pass

class TKS2MK2:
    def __init__(self,name):
        self.name = name
        self.Deck_A = Deck("Deck_A")
        self.Deck_B = Deck("Deck_B")
        self.Mixer = Mixer("Mixer",
                           FaderBoundStruct(encoderBounds(),encoderBounds(),encoderBounds()),
                           EQBoundStruct(encoderBounds(),encoderBounds(),encoderBounds(),encoderBounds()),
                           EQBoundStruct(encoderBounds(),encoderBounds(),encoderBounds(),encoderBounds()),
                           MasterBoundStruct(encoderBounds(),encoderBounds(),encoderBounds()))
        self.FX = FX("FX",FXBoundsStruct(),FXBoundsStruct())
        self.Time = 0

class TimeControl:
    lastOp = 0
    #time (current - start)
    currentVal = 0
    upcomingOp = False
    nextOp = 0
    #Time of next OP
    colour = [255,255,255]
    altColour = [255,0,0]
    def loadCurrentState(self,sT,cT,value):
        if self.currentVal == value:
            r = self.colour[0]*0.9
            b = self.colour[1]*0.9
            g = self.colour[2]*0.9
            if sum([r,b,g]) < sum([64,64,64]):
                self.colour = [64,64,64]
            else:
                self.colour = [(int(r)),(int(b)),(int(g))]
        else:
            self.currentVal = value
            self.lastOp = cT
            self.colour = [255,255,255]
    def anticipate(self,cT,fT):
        until = fT - cT
        lookahead = 1 #second
        if cT >= fT-lookahead:
            r = (self.colour[0]*(until/1)) + (self.altColour[0]*((1-until)/1))
            b = (self.colour[1]*(until/1)) + (self.altColour[1]*((1-until)/1))
            g = (self.colour[2]*(until/1)) + (self.altColour[2]*((1-until)/1))  
        self.colour = [(int(r)),(int(b)),(int(g))] 


class TKS2MK2_TimeControl:
    DeckATempoSlider = TimeControl()
    DeckALoopEncL = TimeControl()
    DeckALoopEncR = TimeControl()

    DeckBTempoSlider = TimeControl()
    DeckBLoopEncL = TimeControl()
    DeckBLoopEncR = TimeControl()
    
    FxLine1DW = TimeControl()
    FxLine1K1 = TimeControl()
    FxLine1K2 = TimeControl()
    FxLine1K3 = TimeControl()

    FxLine2DW = TimeControl()
    FxLine2K1 = TimeControl()
    FxLine2K2 = TimeControl()
    FxLine2K3 = TimeControl()

    LevelA = TimeControl()
    LevelB = TimeControl()
    Crossfader = TimeControl()

    EqA_HI = TimeControl()
    EqA_MI = TimeControl()
    EqA_LO = TimeControl()

    EqB_HI = TimeControl()
    EqB_MI = TimeControl()
    EqB_LO = TimeControl()

    DeckAFxEnc = TimeControl()
    DeckBFxEnc = TimeControl()

    MasterLevel = TimeControl()
    BrowserEnc = TimeControl()

    DeckAPlay = TimeControl()
    DeckACue = TimeControl()
    DeckASync = TimeControl()
    DeckAShift = TimeControl()
    DeckAHot1 = TimeControl()
    DeckAHot2 = TimeControl()
    DeckAHot3 = TimeControl()
    DeckAHot4 = TimeControl()

    DeckBPlay = TimeControl()
    DeckBCue = TimeControl()
    DeckBSync = TimeControl()
    DeckBShift = TimeControl()
    DeckBHot1 = TimeControl()
    DeckBHot2 = TimeControl()
    DeckBHot3 = TimeControl()
    DeckBHot4 = TimeControl()

    DeckAJogPressed = TimeControl()
    HeadPhoneCueA = TimeControl()
    DeckAFlux = TimeControl()
    DeckALoopIn = TimeControl()
    DeckALoopOut = TimeControl()
    DeckALoad = TimeControl()

    DeckBJogPressed = TimeControl()
    HeadPhoneCueB = TimeControl()
    DeckBFlux = TimeControl()
    DeckBLoopIn = TimeControl()
    DeckBLoopOut = TimeControl()
    DeckBLoad = TimeControl()

    FxLine1DWButton = TimeControl()
    FxLine1K1Button = TimeControl()
    FxLine1K2Button = TimeControl()
    FxLine1K3Button = TimeControl()

    FxLine2DWButton = TimeControl()
    FxLine2K1Button = TimeControl()
    FxLine2K2Button = TimeControl()
    FxLine2K3Button = TimeControl()

    DeckAFxLine1Select = TimeControl()
    DeckAFxLine2Select = TimeControl()
    DeckBFxLine1Select = TimeControl()
    DeckBFxLine2Select = TimeControl()
    
    DeckAFxEncPress = TimeControl()
    DeckBFxEncPress = TimeControl()

    DeckALoopEncLPress = TimeControl()
    DeckALoopEncRPress = TimeControl()
    DeckBLoopEncLPress = TimeControl()
    DeckBLoopEncRPress = TimeControl()

    BrowseEncPress = TimeControl()
    
    DeckAJog = TimeControl()
    DeckBJog = TimeControl()

    
