import pygame, sys, pytmx
from pygame.locals import *
from math import floor
import numpy as np
import math

class IsoGame:
    def __init__(self, title='Calc Game'):
        pygame.init()
        
        self.fpsClk=pygame.time.Clock()

        self.WSurf=pygame.display.set_mode((800,600),HWSURFACE|DOUBLEBUF|RESIZABLE)
        self.scrW=800
        self.scrH=600
        
        pygame.display.set_caption(title)
        self.font=pygame.font.SysFont(u'arial',24)
 
        self.music=None
	self.x=0
	self.y=0
	self.vx=0
	self.vy=0
        self.speed=400

        self.myRect=pygame.Rect(15*32,15*32,32,32)
        pygame.mixer.init(44100,-16,300,1024)        

    def buffLvl(self,lvl='levels/lvl0.tmx'):
        self.tmx=pytmx.load_pygame(lvl, pixelalpha=True)
        
        self.lvlSurf=pygame.Surface((self.tmx.tilewidth*self.tmx.width,self.tmx.tileheight*self.tmx.height))
        self.bg=(self.tmx.background_color)
	self.lvlSurf.fill(self.bg)

	for l in self.tmx.visible_layers:
	    if isinstance(l, pytmx.TiledTileLayer):
		    for x,y,gid in l:
                        tile=self.tmx.get_tile_image_by_gid(gid)
			if tile:
			    self.lvlSurf.blit(tile,(self.tmx.tilewidth*x,self.tmx.tileheight*y-tile.get_height())) 

    def playSound(self,filename):
        chan=pygame.mixer.find_channel()
        if chan:
            snd=pygame.mixer.Sound(filename)
            chan.play(snd)
        else:
            print "err: not enough sound channels"

    def startMusic(self):
        pygame.mixer.music.load(self.music)
        pygame.mixer.music.play(-1)
        
    def checkCollission(self,nextx,nexty):

        dx=nextx-self.x
        dy=nexty-self.y

        txr=self.myRect.x+dx
        tyr=self.myRect.y+dy
        tr=pygame.Rect(txr,tyr,32,32)

        #pygame.draw.rect(self.WSurf,(255,255,255),self.myRect)
        undo=False
	for k in range(len(self.tmx.layers)):
	    if isinstance(self.tmx.layers[k], pytmx.TiledObjectGroup):
	        l=self.tmx.layers[k]	
	        for i in l:
                    recto=pygame.Rect(i.x,i.y,i.width,i.height)
		    #print i
                    if hasattr(l,'Collide') and tr.colliderect(recto):
                        undo=True
			self.vy=0
		    if hasattr(i,'Music') and recto.contains(tr):
			#print 'music'
		        if self.music!=i.Music:
			    print i.Music
			    self.music=i.Music
			    pygame.mixer.music.stop()
			    self.startMusic()
		    if hasattr(i,'Talk'):
			if i.Talk=='In':
			    if recto.contains(tr):
				pnum=0
				wnum=0
				while hasattr(i,'p'+str(pnum)):
				    msg=getattr(i,'p'+str(pnum))
				    msgSurf=self.font.render(msg,False,(255,255,255))
				    msgRect=msgSurf.get_rect()
				    msgRect.topleft=(10,20+50*pnum)
				    self.WSurf.blit(msgSurf,msgRect)
				    pnum+=1

#        for i in o[2]:
#            recto=pygame.Rect(i.x,i.y,i.width,i.height)
#            if tr.colliderect(recto):
#                try:
#                    msg=i.name+':'+i.header
#                except AttributeError:
#                    msg=i.name#
#
#                msgSurf=self.font.render(msg,False,(255,255,255))
#                msgRect=msgSurf.get_rect()
#                msgRect.topleft=(10,20)
#                self.WSurf.blit(msgSurf,msgRect)
                
        if not  undo:
            self.myRect=tr
 
        self.x=self.myRect.x
        self.y=self.myRect.y

	#print self.x,self.y

    def loop(self):
        while True:
            self.WSurf.fill(self.bg)  

            for event in pygame.event.get(): 
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_LCTRL:
                        self.speed=200
                    if event.key== K_LSHIFT:
                        self.speed=1400
                    if event.key == K_LEFT:
                        self.vx-=1
                    if event.key == K_RIGHT:
                        self.vx+=1
                    elif event.key == K_ESCAPE:
                        pygame.event.post(pygame.event.Event(QUIT))
                elif event.type ==KEYUP:
                    if event.key == K_LCTRL:
                        self.speed=400
                    if event.key== K_LSHIFT:
                        self.speed=400
                    if event.key == K_LEFT:
                        self.vx+=1
                    if event.key == K_RIGHT:
                        self.vx-=1
                elif event.type==VIDEORESIZE:
                    self.WSurf=pygame.display.set_mode(event.dict['size'],HWSURFACE|DOUBLEBUF|RESIZABLE)
                    self.scrW,self.scrH=event.dict['size']

	    self.vy+=0.3*(float(self.fpsClk.get_time())/1000)

            self.WSurf.blit(self.lvlSurf, (-self.x+self.scrW/2,-self.y+self.scrH/2))


            nextx=self.x+(self.fpsClk.get_time()/1000.)*(self.vx)*self.speed
            nexty=self.y+(float(self.fpsClk.get_time())/1000)*(self.vy)*self.speed
            r=pygame.Rect(self.scrW/2-32,self.scrH/2-32,32,32)
            pygame.draw.rect(self.WSurf,(0,0,255),r)

	    print nextx, nexty
            self.checkCollission(nextx,nexty)

            pygame.display.flip()
            self.fpsClk.tick(60)

if __name__ == '__main__':
    game=IsoGame()
    game.buffLvl()
    #game.music="media/snd/first levels/very beginning/abandoned spaceship interior.mp3"
    #game.startMusic()
    game.loop()













