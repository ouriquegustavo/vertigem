import numpy as np
import pygame

class Background():
    def __init__(self,game, pid, width, height, num):
        self.game=game
        self.pid=pid
        self.width=width
        self.height=height
        self.num=num
        self.r=1
        self.colour=(127,255,212,255)
        self.sprite=[]
        self.sprite_size=[]
        for i in [0,1,2,3,2,1,0]:
            r=self.r+i
            temp_sprite=pygame.Surface((2*r, 2*r), flags=pygame.SRCALPHA)
            temp_sprite.fill((255,255,255,0))
            temp_sprite_size=temp_sprite.get_size()
            pygame.draw.circle(temp_sprite,self.colour,(r,r),r)
            self.sprite.append(temp_sprite)
            self.sprite_size.append(temp_sprite_size)
        self.num_sprites=len(self.sprite)
        self.zorder=-9999
        self.x=(np.random.rand(self.num)-0.5)*self.width
        self.y=(np.random.rand(self.num)-0.5)*self.height
        self.sid=np.random.randint(0,3, self.num)
        
    def update(self):
        pass
        
    def draw(self):
        for star in range(self.num):
            if np.random.rand() < 0.1:
                self.sid[star]+=1
            if self.sid[star] >= self.num_sprites:
                self.sid[star]=0
            self.game.screen.blit(self.sprite[self.sid[star]], (
                self.x[star]-self.sprite_size[self.sid[star]][0]/2-self.game.camera.x+self.game.screen.width/2,
                self.y[star]-self.sprite_size[self.sid[star]][1]/2-self.game.camera.y+self.game.screen.height/2
                )
            )
        
    def set_pid(self,pid):
        self.pid=pid