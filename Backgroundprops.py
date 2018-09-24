import pygame
import random
import os

black = (0,0,0)
warscreenwidth = 1440

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

imgfolder = os.path.join(os.path.dirname(__file__), 'img', 'Powerup')
powerup = []
for picture in range(1,11):
    name = "gold{}.png".format(picture)
    powerup.append(pygame.image.load(os.path.join(imgfolder, name)).convert_alpha())


class Powerup(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, gold):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.gold = gold
        self.image = powerup[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.ticks = 0

    def update(self):
        self.ticks += 1
        self.image = powerup[self.ticks%10]
        self.rect.y = self.rect.y + self.speed
        if self.rect.y > 1080:
            self.kill()

    def collect(self):

        return self.gold