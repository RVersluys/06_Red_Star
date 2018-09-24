import os
import pygame

imgfolder = os.path.join(os.path.dirname(__file__), 'img')
explosions = []
explosionsize = [(128,128),(128,128),(128,128),(128,128),(64,64),(128, 128), (64, 64), (128, 128), (256, 256), (320, 320),(192,192),(384,384),(256,256),(64,64),(32,32),(192,192),(192,192)]
explosionticks = [24,24,24,24,24,32,32,32,32,32,24,64,64,16,24,16,16]
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
    def __init__(self, x, y, type):
        pygame.sprite.Sprite.__init__(self)
        self.image = explosions[type][0]
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.ticks = 0
        self.type = type

    def update(self):
        self.ticks += 1
        if self.ticks == explosionticks[self.type]:
            self.kill()
        else:
            self.image = explosions[self.type][self.ticks]