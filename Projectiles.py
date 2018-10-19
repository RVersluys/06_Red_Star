import os
import pygame
import random

import Gamedata
import GameplayConstants
import Explosions
import Sounds

yellow = (255, 201, 76)

class Imageloading:
    def __init__(self):
        imgfolder = os.path.join(os.path.dirname(__file__), 'img')
        self.projectiles = []
        #speed, damage, plaatje
        self.projectiles.append([15, 6, pygame.image.load(os.path.join(imgfolder, 'projectiles', 'beam.png')).convert_alpha()])
        self.projectiles.append([11, 18, pygame.image.load(os.path.join(imgfolder, 'projectiles', 'shockblast.png')).convert_alpha()])
        self.projectiles.append([15, 3])
        self.heroprojectiles = [pygame.image.load(os.path.join(imgfolder, 'projectiles', 'bullet.png')).convert_alpha(),
                                pygame.image.load(os.path.join(imgfolder, 'projectiles', 'rocket.png')).convert_alpha(),
                                pygame.image.load(os.path.join(imgfolder, 'projectiles', 'plasma.png')).convert_alpha()]

class Mobbullet(pygame.sprite.Sprite):
    def __init__(self, x, y, movex, movey, angle, type):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.rotate(images.projectiles[type][2], angle)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.movex = movex
        self.movey = movey
        self.damage = images.projectiles[type][1]
        self.type = type

    def update(self):
        self.rect.x += self.movex
        self.rect.y -= self.movey
        if not GameplayConstants.extendedscreen.contains(self.rect):
            self.kill()

    def hit(self):
        self.kill()

class Flamethrower(pygame.sprite.Sprite):
    def __init__(self, x, y, movex, movey, damage):
        pygame.sprite.Sprite.__init__(self)
        self.ticks = 0
        self.image = Explosions.explosions[13][0]
        self.rect = pygame.Rect(0, 0, 15, 15)
        self.rect.x = x - 28
        self.rect.y = y - 28
        self.movex = movex
        self.movey = movey
        self.damage = damage

    def update(self):
        self.ticks += 1
        if self.ticks % 3 == 0:
            self.image = Explosions.explosions[13][int(self.ticks/3)]
        self.rect.x += self.movex
        self.rect.y -= self.movey
        if not GameplayConstants.extendedscreen.contains(self.rect) or self.ticks >= 46:
            self.kill()

    def hit(self):
        self.damage = 0
        self.ticks += 1

class Kineticbullet(pygame.sprite.Sprite):
    def __init__(self, x, y, movex, movey, damage):
        pygame.sprite.Sprite.__init__(self)
        self.image = images.heroprojectiles[0]
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.movex = movex
        self.movey = movey
        self.damage = damage
        self.type = 0

    def update(self):
        self.rect.x += self.movex
        self.rect.y -= self.movey

        if not GameplayConstants.extendedscreen.colliderect(self.rect):
            self.kill()

    def hit(self, mob):
        self.kill()
        return mob.getdamage(self.damage)

class FlakCannon(pygame.sprite.Sprite):
    def __init__(self, adjustment, damage):
        pygame.sprite.Sprite.__init__(self)
        self.ticks = 0
        self.damage = damage
        self.image = Explosions.explosions[14][0]
        self.rect = self.image.get_rect()
        self.rect.centerx = Gamedata.hero.rect.centerx + adjustment
        self.rect.y = Gamedata.hero.rect.y - 50
        self.type = 1
        self.hitlist = []

    def update(self):
        self.ticks += 1
        if self.ticks < 24:
            self.image = Explosions.explosions[14][self.ticks]
            self.rect.y = self.rect.y-2
        elif self.ticks == 24:
            x = self.rect.x
            y = self.rect.y
            if self.damage != 0:
                self.image = Explosions.explosions[15][self.ticks - 24]
            else:
                self.image = Explosions.explosions[16][self.ticks - 24]
            self.rect = self.image.get_rect()
            self.rect.centerx = x + random.randint(-75, 75)
            self.rect.y = y - random.randint(375, 525)
        elif self.ticks < 40:
            if self.damage != 0:
                self.image = Explosions.explosions[15][self.ticks - 24]
            else:
                self.image = Explosions.explosions[16][self.ticks - 24]
        else:
            self.kill()

    def hit(self, mob):
        if mob not in self.hitlist:
            self.hitlist.append(mob)
            Sounds.sounds.bangs[0].play()
            if self.ticks < 24:
                self.ticks = 24
                x = self.rect.x
                y = self.rect.y
                self.image = Explosions.explosions[16][0]
                self.rect.x = x
                self.rect.y = y
            return mob.getdamage(self.damage)
        return 0

class Laser(pygame.sprite.Sprite):
    def __init__(self, adjustment, damage):
        pygame.sprite.Sprite.__init__(self)
        self.damage = damage
        self.adjustment = adjustment
        self.ticks = 0
        self.image = pygame.Surface((3,20))
        self.rect = self.image.get_rect()
        self.rect.bottom = Gamedata.hero.rect.top
        self.rect.left = Gamedata.hero.rect.centerx + adjustment
        self.type = 3

    def update(self):
        self.rect.top = 0
        if self.ticks == 13:
            self.kill()
        else:
            self.ticks += 1
        self.rect = pygame.Rect(Gamedata.hero.rect.centerx + self.adjustment, 20, 2, Gamedata.hero.rect.top)
        hits = pygame.sprite.spritecollide(self, Gamedata.mobs, False)
        y = 0
        enemy = False
        for mob in hits:  # collision player-mobs
            if mob.rect.bottom > y:
                enemy = mob
                y = mob.rect.centery
        if enemy:
            height = Gamedata.hero.rect.top - y
            if self.ticks % 3 == 1:
                Gamedata.player.score += enemy.getdamage(self.damage / 4)
        else:
            height = Gamedata.hero.rect.top
        self.image = pygame.Surface((3, max(1,height)))
        self.rect.top = y
        rgcoloring = min(max(0,self.damage * 14 - 5*self.ticks-255),255)
        bcoloring = min(max(0,self.damage * 14 - 5*self.ticks),255)

        self.image.fill((rgcoloring,rgcoloring,bcoloring))

    def hit(self, mob):
        pass

class Rocket(pygame.sprite.Sprite):
    def __init__(self, adjustment, damage):
        pygame.sprite.Sprite.__init__(self)
        self.image = images.heroprojectiles[1]
        self.rect = self.image.get_rect()
        self.rect.top = Gamedata.hero.rect.top
        self.rect.left = Gamedata.hero.rect.centerx + adjustment
        self.type = 2
        self.movey = 16
        for part in Gamedata.player.shipparts:
            if part.type == 4:
                damage = max(damage, 20 + 10 * part.index)
        self.damage = damage

    def update(self):
        self.rect.y -= self.movey
        if not GameplayConstants.extendedscreen.colliderect(self.rect):
            self.kill()

    def hit(self, mob):
        self.kill()
        return mob.getdamage(self.damage)

class Plasmabeam(pygame.sprite.Sprite):
    def __init__(self, adjustment, damage):
        pygame.sprite.Sprite.__init__(self)
        width = int(damage ** 0.5 * 9)
        height = int(damage ** 0.5 * 14)
        size = (width, height)
        self.image = pygame.transform.scale(images.heroprojectiles[2], size)
        self.rect = self.image.get_rect()
        self.rect.top = Gamedata.hero.rect.top
        self.rect.centerx = Gamedata.hero.rect.centerx + adjustment
        self.type = 4
        self.movey = 16
        self.damage = damage

    def update(self):
        self.rect.y -= self.movey
        self.damage -= 1
        width = int(self.damage ** 0.5 * 9)
        height = int(self.damage ** 0.5 * 14)
        size = (width, height)
        self.image = pygame.transform.scale(images.heroprojectiles[2], size)
        x = self.rect.x
        y = self.rect.y
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if not GameplayConstants.extendedscreen.colliderect(self.rect) or self.damage == 0:
            self.kill()

    def hit(self, mob):
        self.kill()
        return mob.getdamage(self.damage)


images = Imageloading()