import pygame
import random
import os

black = (0,0,0)
warscreenwidth = 1440
import Gamedata
import Gametext

"""Hier staan de objecten waarmee geen interactie mogelijk is, zoals sterren, en planeten"""

class Star(pygame.sprite.Sprite):
    def __init__(self, start):
        size = random.randint(1, 2)
        colortint = random.randint(size*60, 255)
        color = (colortint, random.randint(int(colortint/1.4),colortint), random.randint(int(colortint/2), colortint))
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((size*2,size*2))
        self.image.fill(black)
        self.rect = self.image.get_rect()
        pygame.draw.circle(self.image, color, self.rect.center, size)
        if start == True:
            y = random.randint(0, 1080)
            self.rect.bottom = y
        else:
            y = 0
            self.rect.bottom = y
        self.pos = y
        self.rect.centerx = random.randint(0,warscreenwidth)
        self.speed = size * 0.2 * random.uniform(1, 2)

    def update(self):
        self.pos += self.speed
        self.rect.y = self.pos
        if self.rect.top > 1080:
            self.kill()

imgfolder = os.path.join(os.path.dirname(__file__), 'img')
class Images:
    def __init__(self, propslist):
        self.powerup = []
        for picture in range(13):
            name = "0{}.png".format(picture)
            self.powerup.append(pygame.image.load(os.path.join(imgfolder, "Powerup", name)).convert_alpha())

        self.bgprops = []
        for picture in propslist:
            name = "bgprop_{}.png".format(picture)
            self.bgprops.append(pygame.image.load(os.path.join(imgfolder, "bgprops", name)).convert_alpha())

gemprofit = [0,50,100,200,300,400,500,650,800,1000,1200,1400,1600, 0]

class Powerup(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, type):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.gold = gemprofit[type]
        self.image = Gamedata.bgimages.powerup[type-1]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.type = type

    def update(self):
        self.rect.y = self.rect.y + self.speed
        if self.rect.y > 1080:
            self.kill()

    def collect(self):
        if self.type == 13:
            Gamedata.player.uridium241 += 1
            text = Gametext.Text("Uridium 241", 20, (100, 100, 255), (0, 50), self.rect.center)
        else:
            text = Gametext.Text(str(self.gold), int(10 + self.gold**.5), (255, 205, 0), (0,50),self.rect.center)
        Gamedata.all_sprites.add(text)

        return self.gold

class Backgroundprop(pygame.sprite.Sprite):
    def __init__(self, type, x, speed, size): #size in tuple
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(Gamedata.bgimages.bgprops[type],size)
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = 0

    def update(self):
        self.rect.y = self.rect.y + self.speed
        if self.rect.top > 1080:
            self.kill()