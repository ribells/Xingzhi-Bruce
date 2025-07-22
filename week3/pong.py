import pygame,sys,random
SCREEN_W,SCREEN_H=1200,800
BORDER_W=10
ACCURACY=2
G=0.01
SPEEDY_MAX=0.2
def set_new_ball(ball):
    global gameStat
    gameStat=0
    ball.x,ball.y=SCREEN_W//2, 10
    ball.spdX=random.random()*3+1
    ball.spdX=random.random()*2+1

def show_txt(scr,txt,font,x,y,c):
    img=font.render(txt,True,c)
    scr.blit(img,(x,y))

class CLS_ball( object ):
    def __init__(self,x,y,spdX,spdY,scale):
        self.x, self.y=x,y
        self.spdX,self.spdY=spdX,spdY
        self.scale=scale
        self.w,self.h=0,0
        self.frmItv=8
        self.counter=0
        self.picList=[]
    def add_pic( self, pixel ):
        self.picList.append(pixel)
        self.w=len(pixel[0])*self.scale
        self.h=len(pixel)*self.scale
    def move(self):
        self.x+=self.spdX
        self.spdY+=G
        if self.spdY>SPEEDY_MAX:
            self.spdY>SPEEDY_MAX
        self.y+=self.spdY
        if self.y<BORDER_W or self.y>SCREEN_H-self.h-BORDER_W:
            self.spdY*=-1
        self.collide(paddleL)
        self.collide(paddleR)
        
    def draw(self,scr):
        pygame.draw.circle(scr, (255, 255, 0), (self.x, self.y), 5 * self.scale)
        self.counter+=((self.spdX>0)-(self.spdX>0))
    def collide(self,pad):
        global gameStat
        if gameStat==1:
            return
        if self.spdX<0:
            if abs(self.x-(pad.x+pad.w))<=ACCURACY:
                if pad.y<=self.y+self.h//2<=pad.y+pad.h:
                    self.spdX*=-1
                    self.spdY+=pad.spdY * pad.friction
                elif pad.type==0:
                    paddleR.score+=1
                    gameStat=1
        else:
            if abs(self.x+self.w-pad.x)<=ACCURACY:
                if pad.y<=self.y+self.h//2<=pad.y+pad.h:
                    self.spdX*=-1
                    self.spdY+=pad.spdY*pad.friction
                elif pad.type==0:  
                    paddleL.score+=1
                    gameStat=1 
class CLS_paddle(object):
    def __init__(self,x,y,w,h,c=(200,200,0)):
        self.x,self.y=x,y
        self.w,self.h=w,h
        self.spdY=0
        self.accY=0
        self.friction=0.5
        self.c=c
        self.score=0
        self.type=0
    def move(self):
        self.y+=self.accY
        if self.spdY<-SPEEDY_MAX*2:
            self.spdY=-SPEEDY_MAX*2
        if self.spdY>SPEEDY_MAX*2:
            self.spdY=SPEEDY_MAX*2
        self.y+=self.spdY
        if self.y<BORDER_W:
            self.y=BORDER_W
        if self.y>SCREEN_H-self.h-BORDER_W:
            self.y=SCREEN_H-self.h-BORDER_W
    def draw(self,scr):
        pygame.draw.rect(scr,self.c,[self.x,self.y,self.w,self.h],0)
def draw_field(scr):
    c=pygame.color.THECOLORS['brown']
    pygame.draw.rect(scr,c,(0,0,SCREEN_W,BORDER_W),0)
    pygame.draw.rect(scr,c,(0,SCREEN_H-BORDER_W,SCREEN_W,BORDER_W),0)
#---pygame init---
pygame.init()
pygame.display.set_caption("Pingpong Ball")
screen=pygame.display.set_mode( (SCREEN_W,SCREEN_H) )
clock=pygame.time.Clock()
font64=pygame.font.Font('simkai.ttf',64)
#---data init---
ball=CLS_ball(10,10,2,2,3)

paddleL=CLS_paddle(0,200,10,150,(255,0,0))
paddleR=CLS_paddle(SCREEN_W-10,200,10,150,(0,0,255))

paddle=CLS_paddle(SCREEN_W-BORDER_W,200,10,150)


gameStat=0
while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_UP:
                paddleR.accY=-2
            elif event.key==pygame.K_DOWN:
                paddleR.accY=2
            elif event.key==pygame.K_w:
                paddleL.accY=-2
            elif event.key==pygame.K_s:
                paddleL.accY=2
            elif event.key==pygame.K_SPACE:
                set_new_ball(ball)
        if event.type==pygame.KEYUP:
            if event.key in (pygame.K_UP,pygame.K_DOWN):
                paddleR.accY, paddleR.spdY=0,0
            if event.key in (pygame.K_s,pygame.K_w):
                paddleL.accY, paddleL.spdY=0,0
    screen.fill((0,64,0))
    draw_field(screen)
    ball.move()
    ball.draw(screen)
    paddleL.move()
    paddleL.draw(screen)
    paddleR.move()
    paddleR.draw(screen)
    pygame.display.update()
    clock.tick(200)
