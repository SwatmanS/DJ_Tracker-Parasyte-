
class KontrolS2Mk2:
    pass

#class 

class Button:
    b_name = 'untitled button'
    b_state = False
    def setName(self,name):
        self.b_name = name
        return name
    def getName(self):
        return self.b_name
    def setState(self,state):
        self.__dir__b_state = state
        return state
    def getState(self):
        return self.b_state
    
class Knob:
    pass

class Encoder:
    pass

class Jog:
    pass

class Slider:
    s_top = 1
    s_bottom = 0
    s_value = 0.5