import pygame
import os

import Gamedata
import GameplayConstants
import Tools
import Sounds
import Explosions

windowheight = GameplayConstants.windowheight
windowwidth = GameplayConstants.windowwidth
warscreenwidth = GameplayConstants.warscreenwidth
game_folder = os.path.dirname(__file__)
darkgray = (30,30,30)
lightgray = (150,150,150)
bluegray = (81,103,124)

clock = pygame.time.Clock()
fps = GameplayConstants.fps

class Hero(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagelist = []
        self.shieldimagelist = []
        for x in range(11):
            shipname = "ship" + str(x) + ".png"
            shieldname = "shield" + str(x) + ".png"
            self.imagelist.append(pygame.image.load(os.path.join(game_folder, 'img', 'hero', shipname)).convert_alpha())
            picture = pygame.image.load(os.path.join(game_folder, 'img', 'explosion', shieldname)).convert_alpha()
            self.shieldimagelist.append(pygame.transform.scale(picture, (150, 150)))
        self.image = self.imagelist[5]
        self.rect = self.image.get_rect()
        self.radius = 37
        self.rect.center = (warscreenwidth / 2, windowheight - 100)
        self.angle = 5
        self.alive = True
        self.armor = Gamedata.player.maxarmor
        self.shield = Gamedata.player.maxshield
        self.energy = Gamedata.player.maxenergy
        self.shieldrefresh = 200
        self.lastshieldhit = 0
        self.speed = max(0, Gamedata.player.speed)

    def movement(self, event):
        muisafstand = (event.rel[0]**2 + event.rel[1]**2)**0.5
        if muisafstand < self.speed:
            self.movex = event.rel[0]
            self.movey = event.rel[1]
        else:
            self.movex = self.speed * (event.rel[0]/muisafstand)
            self.movey = self.speed * (event.rel[1]/muisafstand)

        if self.movex > 0:
            self.angle = min(10,self.angle + 1, int(5 + self.movex/2))
        elif self.movex < 0:
            self.angle = max(0, self.angle -1, int(5 + self.movex/2))
        elif self.angle > 5:
            self.angle -= 1
        elif self.angle < 5:
            self.angle += 1
        self.image = self.imagelist[self.angle]

    def update(self):
        #cooldown weapons
        for weapon in Gamedata.player.weapons:
            weapon.update()
        #regenerate
        self.energy = max(0,min(Gamedata.player.maxenergy, self.energy + (Gamedata.player.energyregen-Gamedata.player.energyuse) / 60))
        if self.shield < Gamedata.player.maxshield:
            if self.energy > Gamedata.player.maxenergy * 0.5:
                regen = Gamedata.player.maxshield/(60*20)
                self.energy = max(self.energy - regen * 20,0)
                self.shield += regen
        #movement
        self.rect.x += self.movex
        self.rect.y += self.movey
        if self.rect.right > warscreenwidth:
            self.rect.right = warscreenwidth
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > windowheight:
            self.rect.bottom = windowheight
        if self.rect.left < 0:
            self.rect.left = 0
        self.movex = 0
        self.movey = 0

    def getdamage(self, amount, source):
        if amount > self.shield:
            self.shield = 0
            self.armor -= amount - self.shield
            #Sounds.explosions[0].play()
            if self.armor <= 0:
                Sounds.sounds.explosions[8].play()
                self.armor = 0
                self.alive = False
                self.kill()
                explosion = Explosions.Explosion(self.rect.centerx, self.rect.centery,12)
                Gamedata.all_sprites.add(explosion)
                return True
        else:
            self.shield -= amount
        if pygame.time.get_ticks() - self.lastshieldhit > self.shieldrefresh:
            self.lastshieldhit = pygame.time.get_ticks()
            angle = Tools.getangle(self.rect,source.rect)
            angle += 90
            angle %= 360
            m = Shieldhit(angle)
            Gamedata.all_sprites.add(m)
            Sounds.sounds.shieldhitsound.play()
        return False

class Shieldhit(pygame.sprite.Sprite):
    def __init__(self, angle):
        pygame.sprite.Sprite.__init__(self)
        self.count = 0
        self.lastchange = pygame.time.get_ticks()
        self.image = pygame.transform.rotate(Gamedata.hero.shieldimagelist[self.count],angle)
        self.rect = self.image.get_rect()
        self.rect.centerx = Gamedata.hero.rect.centerx
        self.rect.centery = Gamedata.hero.rect.centery
        self.angle = angle
        self.refreshrate = 100

    def update(self):
        now = pygame.time.get_ticks()
        self.rect.centerx = Gamedata.hero.rect.centerx
        self.rect.centery = Gamedata.hero.rect.centery
        if now - self.lastchange > self.refreshrate:
            self.count += 1
            if self.count > 10:
                self.kill()
            else:
                self.image = pygame.transform.rotate(Gamedata.hero.shieldimagelist[self.count], self.angle)

