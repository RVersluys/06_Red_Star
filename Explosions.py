import os
import pygame
import random
import Gamedata
import Sounds


"""Hier worden alle plaatjes geladen voor de explosies, dat gebeurd bij het opstarten van het programma.
De explosie sprites worden hier ook gemannaged."""

imgfolder = os.path.join(os.path.dirname(__file__), 'img')
explosions = []
explosionsize = [(128,128),(128,128),(128,128),(128,128),(64,64),(128, 128), (64, 64), (128, 128), (256, 256), (256, 256),(192,192),(384,384),(256,256),(64,64),(16,16),(128,128),(128,128)]
explosionticks = [24,24,24,24,24,32,32,32,32,32,24,64,64,16,24,16,16]
sound = [4,1,2,3,0,4,1,4,5,7,6,9,8,2,-1,2,2]
for explosion in range(1, 12):
    list = []
    for picture in range(explosionticks[explosion-1]):
        name = "expl_{}_{}.png".format(explosion,picture)
        picture = pygame.image.load(os.path.join(imgfolder, 'explosion', name )).convert_alpha()
        pictureresize = pygame.transform.scale(picture,explosionsize[explosion-1])
        list.append(pictureresize)
    explosions.append(list)

for explosion in range(12,18):
    list = []
    for picture in range(1,explosionticks[explosion-1]+1):
        name = "expl_{}_{}.png".format(explosion, picture)
        picture = pygame.image.load(os.path.join(imgfolder, 'explosion', name )).convert_alpha()
        pictureresize = pygame.transform.scale(picture,explosionsize[explosion-1])
        list.append(pictureresize)
    explosions.append(list)

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, type, list = [0,], rect = False):
        pygame.sprite.Sprite.__init__(self)
        self.image = explosions[type][0]
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.ticks = 0
        self.type = type
        self.list = list
        self.rectship = rect
        if sound[self.type] >= 0:
            Sounds.sounds.explosions[sound[self.type]].play()


    def update(self):
        self.ticks += 1
        if self.ticks == 5 and len(self.list) > 1:
            self.list.pop(0)
            x = self.rectship.x + random.randint(0, self.rectship.width)
            y = self.rectship.y + random.randint(0, self.rectship.height)
            explosion = Explosion(x, y, self.list[0], self.list, self.rectship)
            Gamedata.all_sprites.add(explosion)

        integer = int(self.ticks/2)
        if integer == explosionticks[self.type]:
            self.kill()
        else:
            self.image = explosions[self.type][integer]