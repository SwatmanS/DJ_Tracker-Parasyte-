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

def boundValues(Value,Low = 0,High = 100):
    if Value <= Low:
        return Low
    elif Value >= High:
        return High
    else:
        return Value


def renderText(screen,text='text',position = [0,0],colour = [0,0,0],size = 10):
    fontObj = pg.font.Font("MonospaceTypewriter.ttf",size)
    textSufaceObj = fontObj.render(text, True, colour)
    textRectObj = textSufaceObj.get_rect()
    textRectObj.midtop = (position)
    screen.blit(textSufaceObj, textRectObj,)

def drawBtn(screen, pos = [0,0], pressed = False, label = "",size = 10,textSize = 10,colour = [255,255,255]):
    points = [[-size + pos[0],size+ pos[1]],[size+ pos[0],size+ pos[1]],[size+ pos[0],-size + pos[1]],[-size + pos[0],-size + pos[1]]]
    pg.draw.polygon(screen,
                    [255,255,255],
                    points,
                    width = (2 * int(not(pressed))))
    tPos = [pos[0],pos[1]+(size)]
    renderText(screen,label,tPos,[255,255,255],textSize)

def drawCBtn(screen, pos = [0,0], pressed = False, label = "",size = 10,textSize = 10,colour = [255,255,255]):
    ex = size
    ey = size 
    offset = 22
    pg.draw.polygon(screen,
                    [255,255,255],
                    [(spin(offset+(i*45),ex,ey)[0] + pos[0] ,spin(offset+(i*45),ex,ey)[1] + pos[1]) for i in range(8)],
                    width =  (2 * int(not(pressed))))
    tPos = [pos[0],pos[1]+(1.2*size)]
    renderText(screen,label,tPos,[255,255,255],textSize)
    
def drawJog(screen, pos = [0,0], deg = 0,size = 50,pressed = False,label='',textSize=50):
    ex = size
    ey = size 
    pg.draw.polygon(screen,
                    [255,255,255],
                    [(spin(deg+(i*60),ex,ey)[0] + pos[0] ,spin(deg+(i*60),ex,ey)[1] + pos[1]) for i in range(6)],
                    width = (2 * int(not(pressed))))
    tPos = [pos[0],pos[1]+(1.2*size)]
    renderText(screen,label,tPos,[255,255,255],textSize)

def drawEnc(screen, pos = [0,0], deg = 0,size = 50,pressed = False,label='',textSize=50):
    ex = size
    ey = size

    pg.draw.polygon(screen,
                    [255,255,255],
                    [(spin(deg+(i*45),ex,ey)[0] + pos[0] ,spin(deg+(i*45),ex,ey)[1] + pos[1]) for i in range(8)],
                    width = (2*int(not(pressed))))
    
    tPos = [pos[0],pos[1]+(1.2*size)]
    pg.draw.line(screen,[255,255,255],
                 [spin(deg,(-ex),(-ey))[0]+pos[0],spin(deg,(-ex),(-ey))[1] + pos[1]],
                 [spin(deg,(ex),(ey))[0]+pos[0],spin(deg,(ex),(ey))[1] + pos[1]],
                 width = 2)
    renderText(screen,label,tPos,[255,255,255],textSize)

def drawKnb(screen, pos = [0,0], deg = 0,size = 50,label='',textSize=50):
    ex = size
    ey = size
    
    pg.draw.polygon(screen,
                    [255,255,255],
                    [(spin(deg+(i*45),ex,ey)[0] + pos[0] ,spin(deg+(i*45),ex,ey)[1] + pos[1]) for i in range(8)],
                    width = 2)
    pg.draw.line(screen,[255,255,255],pos,[spin(deg,(ex),(ey))[0]+pos[0],spin(deg,(ex),(ey))[1] + pos[1]],width = 2)
    tPos = [pos[0],pos[1]+(1.2*size)]
    renderText(screen,label,tPos,[255,255,255],textSize)

def drawVFad(screen, pos = [0,0], percentage = 0,size = [10,40],label='',textSize=50):
    Val = percentage
    height = size[1]
    width = size[0]

    points = [[pos[0],pos[1]],
              [pos[0],height+ pos[1]+ int(height/25)],
              [width + pos[0],height + pos[1]+ int(height/25)],
              [width + pos[0],pos[1]]]
    points2 = [[pos[0],             pos[1] + int(percentage/100*height)],
               [width+ pos[0],      pos[1] + int(percentage/100*height)],
               [width+ pos[0],      pos[1] + int(percentage/100*height) + int(height/25)],
               [pos[0],             pos[1] + int(percentage/100*height) + int(height/25)]] 
    pg.draw.polygon(screen,
                    [255,255,255],
                    points,
                    width = 2)
    pg.draw.line(screen,[255,255,255],[pos[0]+int(width/2),pos[1]],[pos[0]+int(width/2),pos[1] + int(height/25)+ height],1)
    pg.draw.polygon(screen,
                    [255,255,255],
                    points2,
                    width = 0) 
    tPos = [pos[0]+(width//2),pos[1]+(height + int(height/25))]
    renderText(screen,label,tPos,[255,255,255],textSize)

def drawHFad(screen, pos = [0,0], percentage = 0,size = [10,40],label='',textSize=50):

    height = size[1]     
    width = size[0]

    points = [[pos[0],pos[1]],
              [pos[0],height+ pos[1]],
              [width + pos[0]+ int(width/25),height + pos[1]],
              [width + pos[0]+ int(width/25),pos[1]]]
    
    points2 = [[pos[0]+ int(percentage/100*width),pos[1]],
               [pos[0]+ int(width/25)+ int(percentage/100*width), pos[1] ],
               [pos[0]+ int(width/25)+ int(percentage/100*width), pos[1]+(height)],
               [pos[0]+ int(percentage/100*width),pos[1]+(height)]] 
    
    pg.draw.polygon(screen,
                    [255,255,255],
                    points,
                    width = 2)
    
    pg.draw.line(screen,[255,255,255],[pos[0],pos[1]+int(height/2)],[pos[0]+int(width/25)+width,pos[1] + int(height/2)],1)
    pg.draw.polygon(screen,
                    [255,255,255],
                    points2,
                    width = 0) 
    tPos = [pos[0]+(width//2),pos[1]+(height + int(height/25))]
    renderText(screen,label,tPos,[255,255,255],textSize)

def testGraphics(screen,clock):
    done = False
    sp = 0
    down = False
    pg.display.set_caption("Input Graphics Test")    
    white = [255,255,255]
    while not done:
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
    pg.quit()

def interfaceSetup():
    pg.init()
    fps = 60
    size = width, height = 900,1600
    screen = pg.display.set_mode((0,0),pg.FULLSCREEN)
    screenRect = screen.get_rect()
    pg.display.set_caption("Controler Display")
    clock = pg.time.Clock()

class ControllerInterface:
    def __init__(self):
        pg.init()
        self.fps = 60
        self.size = self.width, self.height = 900,1600
        self.screen = pg.display.set_mode((0,0),pg.FULLSCREEN)
        self.screenRect = self.screen.get_rect()
        pg.display.set_caption("Controler Display")
        self.clock = pg.time.Clock()
    
if __name__ == "__main__":
    
    pg.init()
    fps = 60
    size = width, height = 900,1600
    screen = pg.display.set_mode((0,0),pg.FULLSCREEN)
    screenRect = screen.get_rect()
    pg.display.set_caption("Controler Display")
    clock = pg.time.Clock()
    white = [255,255,255]
    testGraphics(screen,clock)
