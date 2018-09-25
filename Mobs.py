import pygame
import os
import math

import Projectiles
import Gamedata
import Tools
import GameplayConstants
import Sounds
import Explosions
import Backgroundprops

game_folder = os.path.dirname(__file__)
warscreenwidth = 1440
warscreenheight = 1080
class Unitstats:
    def __init__(self):
        self.deathsound = [0,0,0,2,2,2,5,5,5,3,6,4,9]
        self.hitpoints = [10,10,10,30,30,30,60,60,60,40,350,140,1000]
        self.gold = [0, 0, 0, 0, 0, 0, 0, 0, 0, 100, 800, 400,2500]
        self.pointvalue = [50,50,50,100,100,100,200,200,200,400,1500,800,5000]
        self.explosion = [4,4,4,1,1,1,9,9,9,10,11,9,11]

class Mobsloading:
    def __init__(self):
        self.imagenames = []
        self.hitimagenames = []
        for index in range(13):
            self.imagenames.append("normal_" + str(index) + ".png")
            self.hitimagenames.append("hit_" + str(index) + ".png")

    def load_level(self, mobtypes):
        self.imagelist = []
        self.imagehitlist = []
        for type in mobtypes:
            self.imagelist.append(pygame.image.load(os.path.join(game_folder, 'img', 'mob', self.imagenames[type])).convert_alpha())
            self.imagehitlist.append(pygame.image.load(os.path.join(game_folder, 'img', 'mob', self.hitimagenames[type])).convert_alpha())

unitstats = Unitstats()
images = Mobsloading()

class Mob(pygame.sprite.Sprite):
    def __init__(self, unitindex, startx, starty, speedx, speedy, programlist, wprogramlist, powerup):
        pygame.sprite.Sprite.__init__(self)
        self.imageindex = unitindex
        self.image = images.imagelist[unitindex]
        self.rect = self.image.get_rect()
        #hitpox radius, alleen voor collision met hero, niet met projectiles
        self.radius = int(self.rect.width*0.9/2)
        #startpositie
        self.rect.centerx = startx
        self.rect.bottom = starty
        #verandering x en y per frame, movement programma's kunnen dit overschrijven
        self.speedx = speedx
        self.speedy = speedy

        #laden specificaties van schip
        self.hp = unitstats.hitpoints[unitindex]
        self.points = unitstats.pointvalue[unitindex]
        self.worth = unitstats.gold[unitindex]
        self.deathsound = unitstats.deathsound[unitindex]
        self.powerup = powerup
        #gedrag
        self.ticks = 0
        self.programlist = programlist
        self.wprogramlist = wprogramlist
        self.hit = False

    def getdamage(self, amount):
        if amount == 0:
            return 0
        self.hp -= amount
        if self.hp <= 0:
            self.kill()
            explosion = Explosions.Explosion(self.rect.centerx, self.rect.centery, unitstats.explosion[self.imageindex])
            Gamedata.all_sprites.add(explosion)
            if self.powerup >= 1:
                powerup = Backgroundprops.Powerup(self.rect.centerx, self.rect.centery, 1, self.powerup)
                Gamedata.powerups.add(powerup)
                Gamedata.all_sprites.add(powerup)
            Sounds.sounds.explosions[self.deathsound].play()
            Gamedata.player.gold += self.worth
            return self.points
        else:
            self.image = images.imagehitlist[self.imageindex]
            self.lasthit = pygame.time.get_ticks()
            self.hit = True
            return 0

    def update(self):
        if self.ticks == 0:
            self.programinit()
        elif len(self.programlist) > 1:
            if self.programlist[1][0] == self.ticks: #een nieuw programma wordt geïnnitieerd.
                self.programlist.pop(0)  # als het niet gaat om het eerste programma wordt het oude programma weggehaald.
                self.programinit()
        self.program()

        if not GameplayConstants.extendedscreen.colliderect(self.rect):
            self.kill()

        if self.wprogramlist[0][1] >= 1:
            self.wprogram()

        if self.hit == True:
            if pygame.time.get_ticks() - self.lasthit > 200:
                self.image = images.imagelist[self.imageindex]

    def programinit(self): #eenmalige trigger aan het begin van het programma.
        if self.programlist[0][1] == 1:
            self.startx = self.rect.x
            self.programticks = 1
        elif self.programlist[0][1] == 2:
            self.speedx = 0  # strave begint altijd recht naar beneden.
            if self.rect.centerx > warscreenwidth / 2:
                self.straveleft = True
            else:
                self.straveleft = False
            height = warscreenheight - self.rect.y
            straveduration = height * 2 / self.speedy
            self.speedchange = self.speedy / straveduration
        if self.programlist[0][1] == 4:
            self.startx = self.rect.centerx
            self.starty = self.rect.centery
            if len(self.programlist[0]) == 2:
                self.targetx = Gamedata.hero.rect.centerx
                self.targety = Gamedata.hero.rect.centery
            elif len(self.programlist[0]) == 4:
                self.targetx = self.programlist[0][2]
                self.targety = self.programlist[0][3]
            self.programticks = 1

    def program(self): #trigger voor elke tick van het programma.
        if self.programlist[0][1] == 0: #straightline
            self.rect.x += self.speedx
            self.rect.y += self.speedy
        elif self.programlist[0][1] == 1: #zigzag
            self.rect.y += self.speedy
            if self.startx > warscreenwidth / 2:
                dest = warscreenwidth * 0.2
                self.rect.x = self.startx - (self.startx - dest) * (1-(math.cos(self.programticks/100)**2))
            else:
                dest = warscreenwidth * 0.8
                self.rect.x = self.startx + (dest - self.startx) * (1-(math.cos(self.programticks/100)**2))
            self.programticks += 1
        elif self.programlist[0][1] == 2: #strafe
            self.speedy = max(0, self.speedy - self.speedchange)
            if self.straveleft:
                self.speedx -= max(0.05,self.speedchange*1.5)
            else:
                self.speedx += max(0.05,self.speedchange*1.5)
            self.rect.x += self.speedx
            self.rect.y += self.speedy
        elif self.programlist[0][1] == 3: #change direction
            if self.speedx > self.programlist[0][2]:
                self.speedx -= 0.1
            elif self.speedx < self.programlist[0][2]:
                self.speedx += 0.1
            if self.speedy > self.programlist[0][3]:
                self.speedy -= 0.1
            elif self.speedy < self.programlist[0][3]:
                self.speedy += 0.1
            self.rect.x += self.speedx
            self.rect.y += self.speedy
        elif self.programlist[0][1] == 4: #charge
            self.programticks += 1
            if self.programticks == 156:
                self.programinit()
            self.rect.centerx = self.startx + (self.targetx - self.startx) * (1 - (math.cos(self.programticks / 50) ** 2))
            self.rect.centery = self.starty + (self.targety - self.starty) * (1 - (math.cos(self.programticks / 50) ** 2))
        self.ticks += 1

    def wprogram(self):
        for program in self.wprogramlist:
            if program[1] == 1: #aimed weapon
                if self.ticks % program[0] == 0:
                    speed = Projectiles.images.projectiles[program[2]][0]
                    angle = Tools.getangle(self.rect, Gamedata.hero.rect)
                    move = Tools.getmovement(self.rect, Gamedata.hero.rect, speed)
                    bullet = Projectiles.Mobbullet(self.rect.centerx, self.rect.centery, move[0], move[1], angle, program[2])
                    Gamedata.mobbullets.add(bullet)
                    Gamedata.all_sprites.add(bullet)
            elif program[1] == 2: #machinegun
                if self.ticks % program[0] in [0,3,6,9,12,15]:
                    movex = 0
                    movey = -Projectiles.images.projectiles[program[2]][0]
                    angle = 180
                    change = ((self.ticks % program[0]) %6) * 30-45
                    bullet = Projectiles.Mobbullet(self.rect.centerx + change, self.rect.centery, movex, movey, angle, program[2])
                    Gamedata.mobbullets.add(bullet)
                    Gamedata.all_sprites.add(bullet)
            elif program[1] == 3: #forward shot
                if self.ticks % program[0] == 0:
                    movex = 0
                    movey = -Projectiles.images.projectiles[program[2]][0]
                    angle = 180
                    bullet = Projectiles.Mobbullet(self.rect.centerx, self.rect.centery, movex, movey, angle, program[2])
                    Gamedata.mobbullets.add(bullet)
                    Gamedata.all_sprites.add(bullet)
            elif program[1] == 4: #cluster shot
                if self.ticks % program[0] == 0:
                    speed = Projectiles.images.projectiles[program[2]][0]
                    for x in range(program[3]):
                        angle = -(program[3]-1)*program[4]*0.5 + x * program[4]
                        movey = -math.cos(math.radians(angle)) * speed
                        movex = math.sin(math.radians(angle)) * speed
                        bullet = Projectiles.Mobbullet(self.rect.centerx, self.rect.centery, movex, movey, (angle + 180) % 360, program[2])
                        Gamedata.mobbullets.add(bullet)
                        Gamedata.all_sprites.add(bullet)





