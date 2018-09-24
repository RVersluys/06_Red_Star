import pygame
import os
from copy import deepcopy

import Sprites
import Projectiles
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
        self.speed = 16
        self.angle = 5
        self.alive = True
        self.weapons = []
        self.shipparts = []
        self.score = 0
        self.gold = 15000
        self.maxarmor = 50
        self.armor = self.maxarmor
        self.maxshield = 10
        self.shield = self.maxshield
        self.maxenergy = 100
        self.energy = self.maxenergy
        self.energyuse = 0
        self.energyregen = 20
        self.shippartsused = []  # list met alle geimplementeerde scheepsonderdelen
        self.shipfill = deepcopy(GameplayConstants.shipdesign)

    def refuel(self):
        self.energy = self.maxenergy
        self.shield = self.maxshield
        self.armor = self.maxarmor
        self.alive = True

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
        for weapon in self.weapons:
            weapon.update()
        #regenerate
        self.energy = max(0,min(self.maxenergy, self.energy + (self.energyregen-self.energyuse) / 60))
        if self.shield < self.maxshield:
            if self.energy > self.maxenergy * 0.5:
                regen = self.maxshield/(60*20)
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
            self.shield == 0
            self.armor -= amount - self.shield
            #Sounds.explosions[0].play()
            if self.armor <= 0:
                Sounds.sounds.explosions[8].play()
                self.armor = 0
                self.alive = False
                self.kill()
                explosion = Explosions.Explosion(self.rect.centerx, self.rect.centery,12)
                Sprites.all_sprites.add(explosion)
                return True
        else:
            angle = Tools.getangle(self.rect,source.rect)
            angle += 90
            angle %= 360
            m = Shieldhit(angle)
            Sprites.all_sprites.add(m)
            Sounds.sounds.shieldhitsound.play()
            self.shield -= amount
        return False

    def removepart(self, part):
        self.shippartsused.remove(part)
        x = part.xpos
        y = part.ypos
        height = len(part.shape)
        if isinstance(part.shape[0], tuple):
            width = len(part.shape[0])
        else:
            width = 1
        for stepdown in range(height):
            if width > 1:
                for step in range(width):
                    if part.shape[stepdown][step] == 1:
                        self.shipfill[y + stepdown][x + step] = 1
            else:
                self.shipfill[y + stepdown][x] = 1
        part.remove()

class Shippart:
    def __init__(self, xpos, ypos, type, index):
        self.xpos = xpos
        self.ypos = ypos
        self.image = GameplayConstants.shippartimages[type-1][index]
        self.shape = GameplayConstants.shippartslist[type][index][2]
        self.type = type
        self.index = index
        self.upgrades = 0
        Sprites.hero.gold -= GameplayConstants.shippartprice(type, index, 0)

    def remove(self):
        returnprice = 0
        for x in range(self.upgrades + 1):
            returnprice += GameplayConstants.shippartprice(self.type, self.index, x)
        Sprites.hero.gold += returnprice

        if self.type == 1:
            Sprites.hero.weapons.remove(self)
            Sprites.hero.speed += GameplayConstants.shippartslist[self.type][self.index][9] * (self.upgrades + 1)
        elif self.type == 2:
            Sprites.hero.energyuse -= GameplayConstants.shippartslist[self.type][self.index][3] * (self.upgrades+1)
            Sprites.hero.speed -= GameplayConstants.shippartslist[self.type][self.index][4]* (self.upgrades+1)
        elif self.type == 3:
            Sprites.hero.energyuse -= GameplayConstants.shippartslist[self.type][self.index][3]* (self.upgrades+1)
            Sprites.hero.shield -= GameplayConstants.shippartslist[self.type][self.index][4]* (self.upgrades+1)
            Sprites.hero.maxshield -= GameplayConstants.shippartslist[self.type][self.index][4]* (self.upgrades+1)
        elif self.type == 4:
            Sprites.hero.energyregen -= GameplayConstants.shippartslist[self.type][self.index][3]* (self.upgrades+1)
            Sprites.hero.energy -= GameplayConstants.shippartslist[self.type][self.index][4]* (self.upgrades+1)
            Sprites.hero.maxenergy -= GameplayConstants.shippartslist[self.type][self.index][4]* (self.upgrades+1)

    def upgrade(self):
        price = GameplayConstants.shippartprice(self.type,self.index, self.upgrades+1)
        if Sprites.hero.gold >= price:
            Sprites.hero.gold -= price
            self.upgrades += 1
            self.increasestats()
            Sounds.sounds.soundimplement.play()
        else:
            Sounds.sounds.soundfail.play()

    def increasestats(self):
        if self.type == 1:
            Sprites.hero.speed -= GameplayConstants.shippartslist[1][self.index][9]
        elif self.type == 2:
            Sprites.hero.energyuse += GameplayConstants.shippartslist[2][self.index][3]
            Sprites.hero.speed += GameplayConstants.shippartslist[2][self.index][4]
        elif self.type == 3:
            Sprites.hero.energyuse += GameplayConstants.shippartslist[3][self.index][3]
            Sprites.hero.shield += GameplayConstants.shippartslist[3][self.index][4]
            Sprites.hero.maxshield += GameplayConstants.shippartslist[3][self.index][4]
        elif self.type == 4:
            Sprites.hero.energyregen += GameplayConstants.shippartslist[4][self.index][3]
            Sprites.hero.energy += GameplayConstants.shippartslist[4][self.index][4]
            Sprites.hero.maxenergy += GameplayConstants.shippartslist[4][self.index][4]

    def itemmenu(self): #submenu dat geopend wordt in het schipontwerpmenu
        running = True
        startwidth = (windowwidth-850)/2
        startheight = (windowheight-400)/2
        windowrect = pygame.Rect(startwidth, startheight, 850, 400)
        textrect = pygame.Rect(startwidth + 210, startheight + 85, 300, 295)
        headerrect = pygame.Rect(startwidth + 210, startheight + 20, 430, 50)
        goldrect = pygame.Rect(30, 30, 400, 50)
        refreshrects = [windowrect, goldrect]

        pygame.draw.rect(GameplayConstants.screen, darkgray, windowrect)
        pygame.draw.rect(GameplayConstants.screen, lightgray, headerrect)

        rects = []
        names = []
        if self.type == 1:
            keybind = pygame.Rect(startwidth + 530, startheight + 150, 300, 50)
            if self.keybind == 0:
                names.append("Left keybind")
            else:
                names.append("Right keybind")
            rects.append(keybind)
        if self.upgrades < 5:
            upgraderect = pygame.Rect(startwidth + 530, startheight + 210, 300, 50)
            rects.append(upgraderect)
            names.append("Upgrade")
        removerect = pygame.Rect(startwidth + 530, startheight + 270, 300, 50)
        rects.append(removerect)
        names.append("Remove")
        donerect = pygame.Rect(startwidth + 530, startheight + 330, 300, 50)
        rects.append(donerect)
        names.append("Done")

        for x in range(len(rects)):
            Tools.refresh_menubutton(rects[x], pygame.mouse.get_pos(), names[x], True)

        Tools.draw_text(GameplayConstants.screen, GameplayConstants.shippartslist[self.type][self.index][0], 30, startwidth + 220, startheight + 45, "Xolonium")
        self.shipmenutext(self,startwidth,startheight, textrect)
        Tools.displayshippart(self.type, self.index, self.image, startwidth+110, startheight+200)
        pygame.display.flip()
        while running:
            for event in pygame.event.get():
                mousepos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                elif event.type == pygame.MOUSEMOTION:
                    for x in range(len(rects)):
                        Tools.refresh_menubutton(rects[x], mousepos, names[x], False)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pressed()
                    if mouse[0]:
                        for x in range(len(rects)):
                            if names[x] == "Right keybind" and rects[x].collidepoint(mousepos):
                                self.keybind = 0
                                Sounds.sounds.soundclick.play()
                                names[x] = "Left keybind"
                                Tools.refresh_menubutton(rects[x], mousepos, names[x], False)
                                break
                            elif names[x] == "Upgrade" and rects[x].collidepoint(mousepos) and self.upgrades < 5:
                                self.upgrade()
                                self.shipmenutext(self, startwidth, startheight, textrect)
                                pygame.draw.rect(GameplayConstants.screen, lightgray, goldrect)
                                Tools.draw_text(GameplayConstants.screen, "Gold: " + str(Sprites.hero.gold), 35, 40, 55, "Xolonium")
                                if self.upgrades == 5:
                                    pygame.draw.rect(GameplayConstants.screen, darkgray, (upgraderect.left -3, upgraderect.top -3, upgraderect.width +6, upgraderect.height +6))
                                    indexnr = rects.index(upgraderect)
                                    rects.pop(indexnr)
                                    names.pop(indexnr)
                                break
                            elif names[x] == "Remove" and rects[x].collidepoint(mousepos):
                                Sprites.hero.removepart(self)
                                Sounds.sounds.soundremove.play()
                                return
                            elif names[x] == "Done" and rects[x].collidepoint(mousepos):
                                Sounds.sounds.soundcancel.play()
                                return
                    if mouse[2] and names[0] == "Left keybind" and rects[0].collidepoint(mousepos):
                        self.keybind = 2
                        Sounds.sounds.soundclick.play()
                        names[0] = "Right keybind"
                        Tools.refresh_menubutton(rects[0], mousepos, names[0], False)
            clock.tick(fps)
            pygame.display.update(refreshrects)

    def shipmenutext(self, part, startwidth,startheight, textrect):
        pygame.draw.rect(GameplayConstants.screen, lightgray, textrect)
        text = GameplayConstants.shippartinfo(part.type, part.index, part.upgrades + 1)
        for line in range(len(text)):
            Tools.draw_text(GameplayConstants.screen, text[line], 15, startwidth + 215, startheight +100 + 20 * line, "Xolonium")

class Weapon(Shippart):
    def __init__(self, index, xposition, yposition, image):
        self.xpos = xposition
        self.ypos = yposition
        self.image = image
        self.type = 1
        self.shape = GameplayConstants.shippartslist[self.type][index][2]
        self.index = index
        self.energyuse = GameplayConstants.shippartslist[self.type][index][3]
        self.cooldown = GameplayConstants.shippartslist[self.type][index][4]
        self.nowcooldown = 0
        self.upgrades = 0
        self.keybind = 0
        Sprites.hero.gold -= GameplayConstants.shippartprice(self.type, index, 0)

    def update(self):
        if self.nowcooldown != 0:
            self.nowcooldown -= 1

    def fireevent(self):
        if self.nowcooldown == 0:
            if Sprites.hero.energy >= (self.upgrades + 1) * self.energyuse:
                self.nowcooldown = self.cooldown
                Sprites.hero.energy -= (self.upgrades + 1) * self.energyuse
                if self.index == 0:
                    bullets = self.upgrades+1
                    for bullet in range(bullets):
                        x = Sprites.hero.rect.centerx - bullets / 2 * 20 + bullet * 20 + 10 + (-120 + 30 * self.xpos)
                        y = Sprites.hero.rect.centery - ((bullets - 1) * bullet - bullet ** 2) * 5
                        if bullet < bullets / 2 - 1:
                            movey = -1
                        elif bullet > bullets / 2:
                            movey = 1
                        else:
                            movey = 0
                        speed = 25
                        damage = GameplayConstants.shippartslist[self.type][self.index][8]
                        bullet = Projectiles.Kineticbullet(x, y, movey, speed, damage)
                        Sprites.all_sprites.add(bullet)
                        Sprites.herobullets.add(bullet)

                elif self.index == 1:
                    for x in range(self.upgrades+1):
                        adjustment = -90 + 30 * self.xpos
                        damage = GameplayConstants.shippartslist[self.type][self.index][8]
                        bullet = Projectiles.FlakCannon(adjustment, damage)
                        Sprites.all_sprites.add(bullet)
                        Sprites.herobullets.add(bullet)

                elif self.index == 2:
                    Sounds.sounds.lasersound.play()
                    totaldamage = (self.upgrades + 1) * GameplayConstants.shippartslist[self.type][self.index][8]
                    beams = 3 + self.upgrades * 2
                    beamhitstotal = (self.upgrades + 2) ** 2
                    beamhits = 0
                    for x in range(beams):
                        if x < (beams+1)/2:
                            beamhits += 1
                        else:
                            beamhits -= 1
                        adjustment = x*3 - beams *1.5
                        damage = totaldamage/beamhitstotal * beamhits
                        bullet = Projectiles.Laser(adjustment,damage)
                        Sprites.all_sprites.add(bullet)



class Shieldhit(pygame.sprite.Sprite):
    def __init__(self, angle):
        pygame.sprite.Sprite.__init__(self)
        self.count = 0
        self.lastchange = pygame.time.get_ticks()
        self.image = pygame.transform.rotate(Sprites.hero.shieldimagelist[self.count],angle)
        self.rect = self.image.get_rect()
        self.rect.centerx = Sprites.hero.rect.centerx
        self.rect.centery = Sprites.hero.rect.centery
        self.angle = angle
        self.refreshrate = 100

    def update(self):
        now = pygame.time.get_ticks()
        self.rect.centerx = Sprites.hero.rect.centerx
        self.rect.centery = Sprites.hero.rect.centery
        if now - self.lastchange > self.refreshrate:
            self.count += 1
            if self.count > 10:
                self.kill()
            else:
                self.image = pygame.transform.rotate(Sprites.hero.shieldimagelist[self.count], self.angle)

