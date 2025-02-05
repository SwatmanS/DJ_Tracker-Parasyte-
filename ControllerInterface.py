import pygame as pg
import random
import math

def spin(ang,p,q):
    a = ((p*(math.cos(math.radians(ang))))-(q*(math.sin(math.radians(ang)))))
    b = ((q*(math.cos(math.radians(ang))))+(p*(math.sin(math.radians(ang)))))
    return a,b

def three(rot,pot):
    x,y,z=pot[0],pot[1],pot[2]
    rol,pit,yaw = rot[0],rot[1],rot[2]
    x,y = spin(rol,x,y)
    y,z = spin(pit,y,z)
    x,z= spin(yaw,x,z)
    return x,y,z

def drawBtn(screen, pos = [0,0], pressed = False, label = ""):
    
    points = [[-10 + pos[0],10+ pos[1]],[10+ pos[0],10+ pos[1]],[10+ pos[0],-10 + pos[1]],[-10 + pos[0],-10 + pos[1]]]
    
    pg.draw.polygon(screen,
                    [255,255,255],
                    points,
                    width = not(pressed))
    
def drawJog(screen, pos = [0,0], deg = 0,size = 50,down = 0):
    ex = size
    ey = size
    
    pg.draw.polygon(screen,
                    [255,255,255],
                    [(spin(deg+(i*60),ex,ey)[0] + pos[0] ,spin(deg+(i*60),ex,ey)[1] + pos[1]) for i in range(6)],
                    width = (2 * int(not(down))))

def drawEnc(screen, pos = [0,0], deg = 0,size = 10,down = 0):
    ex = size
    ey = size

    pg.draw.polygon(screen,
                    [255,255,255],
                    [(spin(deg+(i*44),ex,ey)[0] + pos[0] ,spin(deg+(i*44),ex,ey)[1] + pos[1]) for i in range(8)],
                    width = (2*int(not(down))))

def drawKnb(screen, pos = [0,0], deg = 0,size = 10):
    ex = size
    ey = size

    pg.draw.polygon(screen,
                    [255,255,255],
                    [(spin(deg+(i*44),ex,ey)[0] + pos[0] ,spin(deg+(i*44),ex,ey)[1] + pos[1]) for i in range(8)],
                    width = 2)
    pg.draw.line(screen,[255,255,255],pos,[spin(deg,(ex),(ey))[0]+pos[0],spin(deg,(ex),(ey))[1] + pos[1]],width = 2)

def drawFad(screen, pos = [0,0], Val = 0, Max = 80):
    Val = ((Val/Max)*80)-40
    
    points = [[-10 + pos[0],40+ pos[1]],[10+ pos[0],40+ pos[1]],[10+ pos[0],-40 + pos[1]],[-10 + pos[0],-40 + pos[1]]]
    points2 = [[-10 + pos[0],5+ pos[1]+Val],
               [10+ pos[0],5+ pos[1]+Val],
               [10+ pos[0],-5 + pos[1]+Val],
               [-10 + pos[0],-5 + pos[1]+Val]]
    
    pg.draw.polygon(screen,
                    [255,255,255],
                    points,
                    width = 2)

    pg.draw.line(screen,[255,255,255],[pos[0],pos[1]+40],[pos[0],pos[1]-40],1)

    pg.draw.polygon(screen,
                    [255,255,255],
                    points2,
                    width = 0)


if __name__ == "__main__":
    
    pg.init()
    fps = 60
    size = width, height = 500,500
    screen = pg.display.set_mode(size)
    screenRect = screen.get_rect()
    pg.display.set_caption("Controler Display")
    done = False
    clock = pg.time.Clock()
    sp = 0

    while not done:
        screen.fill([0,0,0])
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
              
        ##  Draw Deck A
        ##  A_JogWheel
        drawJog(screen,[120,200],sp)
        ##  A_VolumeFader
        drawFad(screen,[200,330],(sp%80),80)
        
        ##  Deck A Transport
        ##  A_PlayButton
        drawBtn(screen,[150,350], sp > 30)
        ##  A_CueButton
        drawBtn(screen,[125,350], sp > 120)
        ##  A_SyncButton
        drawBtn(screen,[100,350],sp > 210)
        ##  A_ShiftButton
        drawBtn(screen,[75,350],sp > 300)
        
        ##  Deck A HotCues
        ##  A_HotCue1
        drawBtn(screen,[150,325], sp > 40)
        ##  A_HotCue2
        drawBtn(screen,[125,325], sp > 130)
        ##  A_HotCue3
        drawBtn(screen,[100,325],sp > 220)
        ##  A_HotCue4
        drawBtn(screen,[75,325],sp > 310)
        
        ##  Deck A Loop Section
        ##  A_LoopLENC
        drawEnc(screen,[75,300],sp)
        ##  A_LoopIN
        drawBtn(screen,[100,300],sp > 230)
        ##  A_LoopOUT
        drawBtn(screen,[125,300], sp > 140)
        ##  A_LoopRENC
        drawEnc(screen,[150,300],sp)

        ##  Deck A Tempo Section
        ##  A_TempoFader
        drawFad(screen,[40,330],(sp%80),80)
        ##  A_FluxButton
        drawBtn(screen,[40,275], sp > 140)

        ##  Deck A FX Section
        ##  A_DryWetKnob
        drawKnb(screen,[25,50],sp)
        drawBtn(screen,[50,75], sp > 140)
        ##  A_FX1Knob
        drawKnb(screen,[75,50],sp)
        drawBtn(screen,[100,75], sp > 140)
        ##  A_FX2Knob
        drawKnb(screen,[125,50],sp)
        drawBtn(screen,[150,75], sp > 140)
        ##  A_FX3Knob
        drawKnb(screen,[175,50],sp)
        drawBtn(screen,[200,75], sp > 140)
        
        ##  Draw Deck B
        ##  B_JogWheel
        drawJog(screen,[350,150],390 - sp)
        ##  B_VolumeFader
        drawFad(screen,[300,300],(sp%80),80)
        ##  Deck B Transport
        ##  B_PlayButton
        drawBtn(screen,[350,350], sp > 30)
        ##  B_CueButton
        drawBtn(screen,[375,350], sp > 120)
        ##  B_SyncButton
        drawBtn(screen,[400,350],sp > 210)
        ##  B_ShiftButton
        drawBtn(screen,[425,350],sp > 300)
        ##  Deck B HotCue
        ##  B_HotCue1
        drawBtn(screen,[350,325], sp > 40)
        ##  B_HotCue2
        drawBtn(screen,[375,325], sp > 130)
        ##  B_HotCue3
        drawBtn(screen,[400,325],sp > 220)
        ##  B_HotCue4
        drawBtn(screen,[425,325],sp > 310)

        ##  Deck B Loop Section
        ##  B_LoopLENC
        drawEnc(screen,[350,300],sp)
        ##  B_LoopIN
        drawBtn(screen,[375,300],sp > 140) 
        ##  B_LoopOUT
        drawBtn(screen,[400,300], sp > 230)   
        ##  B_LoopRENC
        drawEnc(screen,[425,300],sp)

        ##  B_TempoFader
        drawFad(screen,[460,330],(sp%80),80)
        

        
        #drawEnc(screen,[350,250],sp)
        
        #drawKnb(screen,[350,350],sp)
        
        sp = (sp + 1) % 360
        pg.display.flip()
        clock.tick(60)
    pg.quit()
