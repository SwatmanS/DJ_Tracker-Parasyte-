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
                    width = not(pressed))
    tPos = [pos[0],pos[1]+size]
    renderText(screen,label,tPos,[255,255,255],textSize)
    
def drawJog(screen, pos = [0,0], deg = 0,size = 50,pressed = 0):
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
    size = width, height = 900,1600
    screen = pg.display.set_mode((0,0),pg.FULLSCREEN)
    screenRect = screen.get_rect()
    pg.display.set_caption("Controler Display")
    done = False
    clock = pg.time.Clock()
    white = [255,255,255]
    sp = 0
    while not done:
        screen.fill([0,0,0])
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
        drawJog(screen,[150,450],sp,70,(sp%60) > 30)

        drawBtn(screen=screen,
                pos=[450,450],
                label="Test",
                size=50,textSize=30,
                pressed = (sp%30)>15,
                colour=white)
        
        #renderText(screen,f"H = {screen.get_height()} , W = {screen.get_width()}",[700,100],[255,255,255],size=20)
        renderText(screen,f"mouse_pos = ({pg.mouse.get_pos()})",[pg.mouse.get_pos()[0]+80,pg.mouse.get_pos()[1]+30],[255,255,255],size=10)
        sp = (sp + 1) % 360
        pg.display.flip()
        clock.tick(60)
    pg.quit()
