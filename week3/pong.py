#PPBALL V2.1
import pygame,sys,random
SCREEN_W,SCREEN_H=1200,800
BORDER_W=10
ACCURACY=2#add in V1.0
G=0.01#重力加速度add in V1.1
SPEEDY_MAX=0.2#add in V1.1
def set_new_ball(ball):#add in V1.0
    global gameStat
    gameStat=0
    ball.x,ball.y=SCREEN_W//2, 10
    ball.spdX=random.random()*3+1
    ball.spdX=random.random()*2+1

def show_txt(scr,txt,font,x,y,c):
    img=font.render(txt,True,c)
    scr.blit(img,(x,y))
def draw(screen,pixel,x0,y0,scale):
    color=(pygame.color.THECOLORS['black'],
           pygame.color.THECOLORS['gray32'],
           pygame.color.THECOLORS['gray64'],
           pygame.color.THECOLORS['white'],
           pygame.color.THECOLORS['red'],
           pygame.color.THECOLORS['green'],
           pygame.color.THECOLORS['blue'],
           pygame.color.THECOLORS['orange'],
           pygame.color.THECOLORS['brown'],
           pygame.color.THECOLORS['purple'],
           pygame.color.THECOLORS['yellow'],
           pygame.color.THECOLORS['cyan'],
           pygame.color.THECOLORS['sienna'],
           pygame.color.THECOLORS['chocolate'],
           pygame.color.THECOLORS['coral'],
           pygame.color.THECOLORS['darkgreen'])
    for y in range(len(pixel)):
        line=pixel[y]
        for x in range(len(line)):
            if 'A'<=line[x]<='F':
                c=color[ord(line[x])-55]
            elif '0'<=line[x]<='9':
                c=color[eval(line[x])]
            else:
                continue
            pygame.draw.rect(screen,c,(x*scale+x0,y*scale+y0,scale,scale),0)
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
        draw(scr,\
                self.picList[self.counter//self.frmItv%len(self.picList)],\
                self.x,self.y,self.scale)
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
    show_txt(scr,'Pingpong',font64,350,200,(0,255,255))
    show_txt(scr,'SCORE:'+str(paddleL.score),font64,100,10,(255,0,0))
    show_txt(scr,'SCORE:'+str(paddleR.score),font64,SCREEN_W-300,10,(0,0,255))
#---pygame init---
pygame.init()
pygame.display.set_caption("Pingpong Ball")
screen=pygame.display.set_mode( (SCREEN_W,SCREEN_H) )
clock=pygame.time.Clock()
font64=pygame.font.Font('simkai.ttf',64)
#---data init---
ball=CLS_ball(10,10,2,2,3)
# 第1帧像素数据
pixel = []
pixel.append('....AA....')
pixel.append('..DDAADD..')
pixel.append('.DDDAADDD.')
pixel.append('.DDDAADDD.')
pixel.append('DDDDAADDDD')
pixel.append('DDDDAADDDD')
pixel.append('.DDDAADDD.')
pixel.append('.DDDAADDD.')
pixel.append('..DDAADD..')
pixel.append('....AA....')
ball.add_pic(pixel)
# 第2帧像素数据
pixel = []
pixel.append('....DD....')
pixel.append('..DDDDDD..')
pixel.append('.DDDDDDAD.')
pixel.append('.DDDDDAAD.')
pixel.append('DDDDDAADDD')
pixel.append('DDDDAADDDD')
pixel.append('.DAADDDD.')
pixel.append('.DDDDDDD.')
pixel.append('..DDDDDD..')
pixel.append('....DD....')
ball.add_pic(pixel)

# 第3帧像素数据
pixel = []
pixel.append('....DD....')
pixel.append('..DDDDDD..')
pixel.append('.DDDDDDDD.')
pixel.append('.DDDDDDDD.')
pixel.append('AAAAAAAAAA')
pixel.append('AAAAAAAAAA')
pixel.append('.DDDDDDDD.')
pixel.append('.DDDDDDDD.')
pixel.append('..DDDDDD..')
pixel.append('...DDDD...')
ball.add_pic(pixel)

# 第4帧像素数据
pixel = []
pixel.append('....DD....')
pixel.append('..DADDDD..')
pixel.append('.DDAADDDD.')
pixel.append('.DDDAADDD.')
pixel.append('DDDDDAADDD')
pixel.append('DDDDDDAADD')
pixel.append('.DDDDDDAA.')
pixel.append('.DDDDDDDD.')
pixel.append('..DDDDDD..')
pixel.append('...DDDD...')
ball.add_pic(pixel)

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
