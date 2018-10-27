import pygame
from copy import deepcopy
from copy import copy

import Gamedata
import Projectiles
import GameplayConstants
import Tools
import Sounds
import Colors
import Button

clock = pygame.time.Clock()

class Player:
    def __init__(self):
        self.speed = 18
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
        self.missiles = []
        self.shipfill = deepcopy(GameplayConstants.shipdesign)
        self.levelnumber = 0 # huidige level van het spel
        self.ship = 0

    def changeship(self, shipnr):
        Sounds.sounds.soundimplement.play()
        shipparts = copy(self.shippartsused)
        for item in shipparts:
            self.removepart(item)
        self.shipfill = deepcopy(GameplayConstants.shipdesign)
        self.gold += GameplayConstants.shippartslist[5][self.ship][1] * 900
        self.gold -= GameplayConstants.shippartslist[5][shipnr][1] * 900
        self.ship = shipnr
        self.maxarmor = GameplayConstants.shippartslist[5][shipnr][4]
        self.speed = GameplayConstants.shippartslist[5][shipnr][9]

    def removepart(self, part):
        self.shippartsused.remove(part)
        if part.type == 1:
            self.weapons.remove(part)
        x = part.xpos
        y = part.ypos
        height = len(part.shape)
        width = len(part.shape[0])
        for stepdown in range(height):
            if width > 1:
                for step in range(width):
                    if part.shape[stepdown][step] == 1:
                        self.shipfill[y + stepdown][x + step] = 1
            else:
                self.shipfill[y + stepdown][x] = 1
        part.remove()

class Shippart:
    def __init__(self, xpos, ypos, type, index, shape, rotations):
        self.xpos = xpos
        self.ypos = ypos
        self.shape = shape
        self.type = type
        self.index = index
        self.upgrades = 0
        self.rotations = rotations
        Gamedata.player.gold -= GameplayConstants.shippartprice(type, index, 0)

    def remove(self):
        returnprice = 0
        for x in range(self.upgrades + 1):
            returnprice += GameplayConstants.shippartprice(self.type, self.index, x)
        Gamedata.player.gold += returnprice
        self.changestats(self.upgrades+1, False)

    def upgrade(self):
        price = GameplayConstants.shippartprice(self.type,self.index, self.upgrades+1)
        if Gamedata.player.gold >= price:
            Gamedata.player.gold -= price
            self.upgrades += 1
            self.changestats(1)
            Sounds.sounds.soundimplement.play()
            if self.type == 1 and self.index == 2:
                for missilelauncher in Gamedata.player.missiles:
                    missilelauncher.replenish()
        else:
            Sounds.sounds.soundfail.play()

    def downgrade(self):
        price = GameplayConstants.shippartprice(self.type, self.index, self.upgrades)
        Gamedata.player.gold += price
        self.upgrades -= 1
        self.changestats(1, False)
        Sounds.sounds.soundremove.play()

    def changestats(self, rounds, add = True):
        if add:
            multiply = 1
        else:
            multiply = -1
        for x in range(rounds):
            if self.type == 1:
                Gamedata.player.speed -= GameplayConstants.shippartslist[1][self.index][9] * multiply
            elif self.type == 2:
                Gamedata.player.energyuse += GameplayConstants.shippartslist[2][self.index][3]* multiply
                Gamedata.player.speed += GameplayConstants.shippartslist[2][self.index][4]* multiply
            elif self.type == 3:
                Gamedata.player.energyuse += GameplayConstants.shippartslist[3][self.index][3]* multiply
                Gamedata.player.maxshield += GameplayConstants.shippartslist[3][self.index][4]* multiply
            elif self.type == 4:
                Gamedata.player.energyregen += GameplayConstants.shippartslist[4][self.index][3]* multiply
                Gamedata.player.maxenergy += GameplayConstants.shippartslist[4][self.index][4]* multiply

    def itemmenu(self): #submenu dat geopend wordt in het schipontwerpmenu
        startwidth = (GameplayConstants.windowwidth-850)/2
        startheight = (GameplayConstants.windowheight-400)/2
        windowrect = pygame.Rect(startwidth, startheight, 850, 400)
        textrect = pygame.Rect(startwidth + 210, startheight + 85, 300, 295)
        headerrect = pygame.Rect(startwidth + 210, startheight + 20, 430, 50)
        goldrect = pygame.Rect(1490, 30, 400, 50)

        buttons = [Button.Button(pygame.Rect(startwidth + 530, startheight + 90, 300, 50),"","Keybind"),
                   Button.Button(pygame.Rect(startwidth + 530, startheight + 150, 300, 50),"Upgrade", "Upgrade"),
                   Button.Button(pygame.Rect(startwidth + 530, startheight + 210, 300, 50), "Downgrade", "Downgrade"),
                   Button.Button(pygame.Rect(startwidth + 530, startheight + 270, 300, 50),"Remove", "Remove"),
                   Button.Button(pygame.Rect(startwidth + 530, startheight + 330, 300, 50),"Done","Done")]

        pygame.draw.rect(GameplayConstants.screen, Colors.darkgray, windowrect)
        pygame.draw.rect(GameplayConstants.screen, Colors.lightgray, headerrect)


        if self.type == 1:
            if self.keybind == 0:
                buttons[0].text = "Left keybind"
            else:
                buttons[0].text = "Right keybind"
        else:
            buttons[0].active = False
        if self.upgrades == 5:
            buttons[1].active = False
        elif self.upgrades == 0:
            buttons[2].active = False

        for button in buttons:
            button.update()

        Tools.draw_text(GameplayConstants.screen, GameplayConstants.shippartslist[self.type][self.index][0], 30, startwidth + 220, startheight + 45, "Xolonium")
        self.shipmenutext(self,startwidth,startheight, textrect)
        image = pygame.transform.rotate(GameplayConstants.shippartimages[self.type-1][self.index], -self.rotations * 90)
        Tools.displayshippart(image, startwidth+110, startheight+200, self.shape)
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                mousepos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEMOTION:
                    for button in buttons:
                        button.update()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pressed()
                    if mouse[0]:
                        for button in buttons:
                            if button.rect.collidepoint(mousepos):
                                if button.function == "Keybind":
                                    button.text = "Left keybind"
                                    self.keybind = 0
                                elif button.function == "Upgrade":
                                    self.upgrade()
                                    self.shipmenutext(self, startwidth, startheight, textrect)
                                    pygame.draw.rect(GameplayConstants.screen, Colors.lightgray, goldrect)
                                    Tools.draw_text(GameplayConstants.screen, "Gold: " + str(Gamedata.player.gold), 35, 1495, 55, "Xolonium")
                                    if self.upgrades > 0:
                                        buttons[2].active = True
                                        buttons[2].update()
                                    if self.upgrades == 5:
                                        pygame.draw.rect(GameplayConstants.screen, Colors.darkgray, (button.rect.left - 3, button.rect.top - 3, button.rect.width + 6, button.rect.height + 6))
                                        button.active = False
                                elif button.function == "Downgrade":
                                    self.downgrade()
                                    if self.upgrades == 4:
                                        buttons[1].active = True
                                        buttons[1].update()
                                    self.shipmenutext(self, startwidth, startheight, textrect)
                                    pygame.draw.rect(GameplayConstants.screen, Colors.lightgray, goldrect)
                                    Tools.draw_text(GameplayConstants.screen, "Gold: " + str(Gamedata.player.gold), 35, 1495, 55, "Xolonium")
                                    if self.upgrades == 0:
                                        pygame.draw.rect(GameplayConstants.screen, Colors.darkgray, (button.rect.left - 3, button.rect.top - 3, button.rect.width + 6, button.rect.height + 6))
                                        button.active = False
                                elif button.function == "Remove":
                                    Gamedata.player.removepart(self)
                                    Sounds.sounds.soundremove.play()
                                    return
                                elif button.function == "Done":
                                    Sounds.sounds.soundcancel.play()
                                    return
                    if mouse[2] and buttons[0].rect.collidepoint(mousepos):
                        self.keybind = 2
                        Sounds.sounds.soundclick.play()
                        buttons[0].text = "Right keybind"
                        buttons[0].update()
            clock.tick(GameplayConstants.fps)
            pygame.display.flip()

    def shipmenutext(self, part, startwidth,startheight, textrect):
        pygame.draw.rect(GameplayConstants.screen, Colors.lightgray, textrect)
        text = GameplayConstants.shippartinfo(part.type, part.index, part.upgrades + 1)
        for line in range(len(text)):
            Tools.draw_text(GameplayConstants.screen, text[line], 15, startwidth + 215, startheight +100 + 20 * line, "Xolonium")

class Weapon(Shippart):
    def __init__(self, index, xposition, yposition, shape):
        self.xpos = xposition
        self.ypos = yposition
        self.type = 1
        self.shape = shape
        self.index = index
        self.energyuse = GameplayConstants.shippartslist[self.type][index][3]
        self.cooldown = GameplayConstants.shippartslist[self.type][index][4]
        self.nowcooldown = 0
        self.upgrades = 0
        self.keybind = 0
        self.rotations = 0
        Gamedata.player.gold -= GameplayConstants.shippartprice(self.type, index, 0)
        if self.index == 2:
            self.fireleft = True
            self.ammo = 10
            Gamedata.player.missiles.append(self)
        elif self.index == 4:
            self.chargeup = 0

    def replenish(self):
        self.ammo = (self.upgrades+1) * 10

    def update(self):
        if self.nowcooldown != 0:
            self.nowcooldown -= 1

    def remove(self):
        returnprice = 0
        for x in range(self.upgrades + 1):
            returnprice += GameplayConstants.shippartprice(self.type, self.index, x)
        Gamedata.player.gold += returnprice
        self.changestats(self.upgrades+1, False)


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
                    if self.ammo > 0:
                        adjustment = -90 + 30 * self.xpos
                        if self.fireleft:
                            adjustment += 5
                        else:
                            adjustment -= 5
                        self.fireleft = not self.fireleft
                        damage = GameplayConstants.shippartslist[self.type][self.index][8]
                        bullet = Projectiles.Rocket(adjustment, damage)
                        Gamedata.all_sprites.add(bullet)
                        Gamedata.herobullets.add(bullet)
                        self.ammo -= 1

                elif self.index == 3:
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

                elif self.index == 4:
                    if self.chargeup < GameplayConstants.shippartslist[self.type][self.index][8] * 15:
                        self.chargeup += GameplayConstants.shippartslist[self.type][self.index][8]


    def plasmashot(self):
        if self.chargeup:
            bullets = self.upgrades + 1
            for bullet in range(bullets):
                x = Gamedata.hero.rect.centerx - bullets / 2 * 20 + bullet * 20 + 10 + (-120 + 30 * self.xpos)
                y = Gamedata.hero.rect.centery - ((bullets - 1) * bullet - bullet ** 2) * 5
                if bullet < bullets / 2 - 1:
                    movey = -1
                elif bullet > bullets / 2:
                    movey = 1
                else:
                    movey = 0
                bullet = Projectiles.Plasmabeam(x, y, self.chargeup, movey)
                Gamedata.all_sprites.add(bullet)
                Gamedata.herobullets.add(bullet)
            self.chargeup = 0
