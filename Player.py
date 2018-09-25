import pygame
from copy import deepcopy

import Gamedata
import Projectiles
import GameplayConstants
import Tools
import Sounds

clock = pygame.time.Clock()

class Player:
    def __init__(self):
        self.speed = 16
        self.weapons = []
        self.shipparts = []
        self.score = 0
        self.gold = 15000
        self.maxarmor = 50
        self.maxshield = 10
        self.maxenergy = 100
        self.energyuse = 0 # standaard energieverlies per seconde vanwege energiegebruik schipsonderdelen
        self.energyregen = 20 # basis energieproductie per seconde
        self.shippartsused = []  # list met alle geimplementeerde scheepsonderdelen
        self.shipfill = deepcopy(GameplayConstants.shipdesign)
        self.levelnumber = 0 # huidige level van het spel


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
        self.shape = GameplayConstants.shippartslist[type][index][2]
        self.type = type
        self.index = index
        self.upgrades = 0
        Gamedata.player.gold -= GameplayConstants.shippartprice(type, index, 0)

    def remove(self):
        returnprice = 0
        for x in range(self.upgrades + 1):
            returnprice += GameplayConstants.shippartprice(self.type, self.index, x)
        Gamedata.player.gold += returnprice

        if self.type == 1:
            Gamedata.player.weapons.remove(self)
            Gamedata.player.speed += GameplayConstants.shippartslist[self.type][self.index][9] * (self.upgrades + 1)
        elif self.type == 2:
            Gamedata.player.energyuse -= GameplayConstants.shippartslist[self.type][self.index][3] * (self.upgrades+1)
            Gamedata.player.speed -= GameplayConstants.shippartslist[self.type][self.index][4]* (self.upgrades+1)
        elif self.type == 3:
            Gamedata.player.energyuse -= GameplayConstants.shippartslist[self.type][self.index][3]* (self.upgrades+1)
            Gamedata.player.maxshield -= GameplayConstants.shippartslist[self.type][self.index][4]* (self.upgrades+1)
        elif self.type == 4:
            Gamedata.player.energyregen -= GameplayConstants.shippartslist[self.type][self.index][3]* (self.upgrades+1)
            Gamedata.player.maxenergy -= GameplayConstants.shippartslist[self.type][self.index][4]* (self.upgrades+1)

    def upgrade(self):
        price = GameplayConstants.shippartprice(self.type,self.index, self.upgrades+1)
        if Gamedata.player.gold >= price:
            Gamedata.player.gold -= price
            self.upgrades += 1
            self.increasestats()
            Sounds.sounds.soundimplement.play()
        else:
            Sounds.sounds.soundfail.play()

    def increasestats(self):
        if self.type == 1:
            Gamedata.player.speed -= GameplayConstants.shippartslist[1][self.index][9]
        elif self.type == 2:
            Gamedata.player.energyuse += GameplayConstants.shippartslist[2][self.index][3]
            Gamedata.player.speed += GameplayConstants.shippartslist[2][self.index][4]
        elif self.type == 3:
            Gamedata.player.energyuse += GameplayConstants.shippartslist[3][self.index][3]
            Gamedata.player.maxshield += GameplayConstants.shippartslist[3][self.index][4]
        elif self.type == 4:
            Gamedata.player.energyregen += GameplayConstants.shippartslist[4][self.index][3]
            Gamedata.player.maxenergy += GameplayConstants.shippartslist[4][self.index][4]

    def itemmenu(self): #submenu dat geopend wordt in het schipontwerpmenu
        running = True
        startwidth = (GameplayConstants.windowwidth-850)/2
        startheight = (GameplayConstants.windowheight-400)/2
        windowrect = pygame.Rect(startwidth, startheight, 850, 400)
        textrect = pygame.Rect(startwidth + 210, startheight + 85, 300, 295)
        headerrect = pygame.Rect(startwidth + 210, startheight + 20, 430, 50)
        goldrect = pygame.Rect(30, 30, 400, 50)
        refreshrects = [windowrect, goldrect]

        pygame.draw.rect(GameplayConstants.screen, GameplayConstants.darkgray, windowrect)
        pygame.draw.rect(GameplayConstants.screen, GameplayConstants.lightgray, headerrect)

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
        image = GameplayConstants.shippartimages[self.type-1][self.index]
        Tools.displayshippart(self.type, self.index, image, startwidth+110, startheight+200)
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
                                pygame.draw.rect(GameplayConstants.screen, GameplayConstants.lightgray, goldrect)
                                Tools.draw_text(GameplayConstants.screen, "Gold: " + str(Gamedata.player.gold), 35, 40, 55, "Xolonium")
                                if self.upgrades == 5:
                                    pygame.draw.rect(GameplayConstants.screen, GameplayConstants.darkgray, (upgraderect.left -3, upgraderect.top -3, upgraderect.width +6, upgraderect.height +6))
                                    indexnr = rects.index(upgraderect)
                                    rects.pop(indexnr)
                                    names.pop(indexnr)
                                break
                            elif names[x] == "Remove" and rects[x].collidepoint(mousepos):
                                Gamedata.player.removepart(self)
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
            clock.tick(GameplayConstants.fps)
            pygame.display.update(refreshrects)

    def shipmenutext(self, part, startwidth,startheight, textrect):
        pygame.draw.rect(GameplayConstants.screen, GameplayConstants.lightgray, textrect)
        text = GameplayConstants.shippartinfo(part.type, part.index, part.upgrades + 1)
        for line in range(len(text)):
            Tools.draw_text(GameplayConstants.screen, text[line], 15, startwidth + 215, startheight +100 + 20 * line, "Xolonium")

class Weapon(Shippart):
    def __init__(self, index, xposition, yposition):
        self.xpos = xposition
        self.ypos = yposition
        self.type = 1
        self.shape = GameplayConstants.shippartslist[self.type][index][2]
        self.index = index
        self.energyuse = GameplayConstants.shippartslist[self.type][index][3]
        self.cooldown = GameplayConstants.shippartslist[self.type][index][4]
        self.nowcooldown = 0
        self.upgrades = 0
        self.keybind = 0
        Gamedata.player.gold -= GameplayConstants.shippartprice(self.type, index, 0)

    def update(self):
        if self.nowcooldown != 0:
            self.nowcooldown -= 1

    def fireevent(self):
        if self.nowcooldown == 0:
            if Gamedata.hero.energy >= (self.upgrades + 1) * self.energyuse:
                self.nowcooldown = self.cooldown
                Gamedata.hero.energy -= (self.upgrades + 1) * self.energyuse
                if self.index == 0:
                    bullets = self.upgrades+1
                    for bullet in range(bullets):
                        x = Gamedata.hero.rect.centerx - bullets / 2 * 20 + bullet * 20 + 10 + (-120 + 30 * self.xpos)
                        y = Gamedata.hero.rect.centery - ((bullets - 1) * bullet - bullet ** 2) * 5
                        if bullet < bullets / 2 - 1:
                            movey = -1
                        elif bullet > bullets / 2:
                            movey = 1
                        else:
                            movey = 0
                        speed = 25
                        damage = GameplayConstants.shippartslist[self.type][self.index][8]
                        bullet = Projectiles.Kineticbullet(x, y, movey, speed, damage)
                        Gamedata.all_sprites.add(bullet)
                        Gamedata.herobullets.add(bullet)

                elif self.index == 1:
                    for x in range(self.upgrades+1):
                        adjustment = -90 + 30 * self.xpos
                        damage = GameplayConstants.shippartslist[self.type][self.index][8]
                        bullet = Projectiles.FlakCannon(adjustment, damage)
                        Gamedata.all_sprites.add(bullet)
                        Gamedata.herobullets.add(bullet)

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
                        Gamedata.all_sprites.add(bullet)