import pygame
import os

windowwidth = 1920
windowheight = 1080
warscreenwidth = 1440
interfacewidth = 480
warrect = pygame.Rect(0, 0, 1440, 1080)
sidebarrect = pygame.Rect(1440, 0, 480, 1080)

# kleuren
white = (255, 255, 255)

black = (0, 0, 0)
blackgray = (10, 10, 10)
darkgray = (30, 30, 30)
lightgray = (150, 150, 150)
bluegray = (81, 103, 124)
darkgreen = (0, 155, 0)
darkred = (155, 0, 0)
colorenergy = (255, 245, 104)
colorshield = (0, 191, 243)
colorarmor = (242, 101, 34)
colorbars = [colorenergy, colorshield, colorarmor]

# initieren van pygame
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((windowwidth, windowheight), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.FULLSCREEN)

clock = pygame.time.Clock()
pygame.display.set_caption("Cydonia")

import GameplayConstants

GameplayConstants.screen = screen
import Tools
import Hero
import Sprites
import Level
import Sounds

game_folder = os.path.dirname(__file__)
fps = GameplayConstants.fps


class Game:
    def __init__(self):
        # initialize music
        pygame.mixer.music.load(os.path.join(game_folder, 'sounds', 'Hymne.mp3'))
        pygame.mixer.music.set_volume(GameplayConstants.musicvolume/100)
        pygame.mixer.music.play(loops=-1)

    def submenu(self, buttons, choice):
        screen.blit(self.background, dest=(0, 0))
        Tools.draw_text(screen, self.menutext[choice], 38, 105, 152 + choice * 70, "Xolonium")
        if self.choice >= 0:
            self.dirtyrects.append(self.submenurect)
        if choice != self.choice:
            Sounds.sounds.soundclick.play()
            self.submenurect = pygame.draw.rect(screen, lightgray,pygame.Rect(windowwidth / 2 - 300, windowheight / 2 - 30 * buttons - 20, 600, 60 * buttons + 30))
            self.submenubuttonrects = []
            for button in range(buttons):
                self.submenubuttonrects.append(
                    pygame.Rect(windowwidth / 2 - 275, windowheight / 2 - 30 * buttons + 60 * button, 550, 50))
                pygame.draw.rect(screen, black, self.submenubuttonrects[button])
            self.dirtyrects.append(self.submenurect)
            self.choice = choice
        else:
            self.choice = -1
            Sounds.sounds.soundcancel.play()
        pygame.display.update(self.dirtyrects)

    def menuloop(self):
        running = True
        self.menutext = ["Continue", "New Game", "Settings", "Load game", "Hall of fame", "Quit"]
        self.submenus = {2: []}
        self.menurects = [pygame.Rect(100, 150 + x * 70, 400, 50) for x in range(6)]
        self.submenurect = pygame.Rect(0, 0, 0, 0)
        self.dirtyrects = [pygame.Rect(100, 150 + x * 70, 400, 50) for x in range(6)]
        self.choice = -1

        # create mainmenu
        self.background = pygame.image.load(os.path.join(game_folder, "img", "menu.png")).convert()
        screen.blit(self.background, dest=(0, 0))
        pygame.display.flip()
        mousepos = pygame.mouse.get_pos()
        for x in range(6):
            Tools.refresh_menubutton(self.menurects[x], mousepos, self.menutext[x], True)
        pygame.display.flip()
        while running:
            # keep loop running at the right speed
            clock.tick(GameplayConstants.fps)
            mousepos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pressed()
                    if mouse[0]:
                        if self.menurects[1].collidepoint(mousepos):
                            Sounds.sounds.soundclick.play()
                            Sprites.hero = Hero.Hero()  # create hero
                            self.shipmenuloop()
                        elif self.menurects[2].collidepoint(mousepos):
                            self.optionmenu()
                        elif self.menurects[3].collidepoint(mousepos):
                            self.submenu(5, 3)
                        elif self.menurects[4].collidepoint(mousepos):
                            self.submenu(8, 4)
                        elif self.menurects[5].collidepoint(mousepos):
                            pygame.quit()
                elif event.type == pygame.MOUSEMOTION:
                    for x in range(6):
                        Tools.refresh_menubutton(self.menurects[x], mousepos, self.menutext[x], False)
                        self.dirtyrects.append(self.menurects[x])
            if self.dirtyrects:
                pygame.display.update(self.dirtyrects)
                self.dirtyrects = []

    def shipmenuloop(self):
        running = True

        # laden images
        self.hangarpic = pygame.image.load(os.path.join(game_folder, "img", "hangar.jpg")).convert()
        self.shipimage = pygame.image.load(os.path.join(game_folder, "img", "hero", "menuship.png")).convert_alpha()
        self.energymeter = pygame.image.load(os.path.join(game_folder, "img", "Parts", "energymeter.png")).convert()

        # deze variabelen houden bij waar de speler is in het menu.
        self.menunumber = 0
        self.shippartselected = False  # Een shippart is geselecteerd en vervangt de muis
        self.shippartdisplayed = -1  # schippartnr displayed, -1 = geen shippart

        self.shippartmenurect = pygame.Rect(55, 515, 1810, 507)  # groot blok onderaan

        # menuknoppen
        backrect = pygame.Rect(920, 935, 400, 50)  # alleen zichtbaar in submenu
        launchrect = pygame.Rect(1535, 935, 300, 60)
        abortrect = pygame.Rect(1535, 855, 300, 60)

        self.activenames = [GameplayConstants.shippartslist[self.menunumber][x][0] for x in range(len(GameplayConstants.shippartslist[self.menunumber]))]
        self.activerects = [pygame.Rect(920, 553 + x * 60, 400, 50) for x in range(7)]
        self.activebuttons2names = ["Launch", "Abort", "Back"]
        self.activebuttons2 = [launchrect, abortrect]

        self.resetscreen()
        shippartdrag = False
        while running:
            for event in pygame.event.get():
                mousepos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEMOTION:
                    # beweging van de muis bij een geselecteerd schiponderdeel
                    if self.shippartselected == True:
                        image = GameplayConstants.shippartimages[self.menunumber - 1][self.shippartdisplayed]
                        mouserect.center = (mousepos[0], mousepos[1])
                        self.resetscreen()
                        Tools.displayshippart(self.menunumber, self.shippartdisplayed, image, 1427, 730)
                        screen.blit(mouseimage, mouserect)
                    else:
                        # kleuren van de knoppen bij het er overheen hoveren.
                        for x in range(len(self.activenames)):
                            Tools.refresh_menubutton(self.activerects[x], mousepos,GameplayConstants.shippartslist[self.menunumber][x][0], False)
                        for x in range(len(self.activebuttons2)):
                            Tools.refresh_menubutton(self.activebuttons2[x], mousepos, self.activebuttons2names[x], False)
                elif event.type == pygame.MOUSEBUTTONUP and shippartdrag:
                    self.placeshippart(mousepos, mouseimage)
                    shippartdrag = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pressed()
                    if mouse[2]:  # rechtermuisknop
                        if self.shippartselected == True:  # deselecteer een schipdeel
                            Sounds.sounds.soundcancel.play()
                            pygame.mouse.set_visible(True)
                            self.shippartselected = False
                            self.resetscreen()
                            Tools.displayshippart(self.menunumber, self.shippartdisplayed, image, 1427, 730)
                        else:  # verwijder een schipdeel in het schip met de rechter muisknop
                            x = int((mousepos[0] - 69) / 60)
                            y = int((mousepos[1] - 529) / 60)
                            if x >= 0 and x <= 9 and y >= 0 and y <= 8:
                                if not isinstance(Sprites.hero.shipfill[y][x], int):
                                    Sounds.sounds.soundremove.play()
                                    Sprites.hero.removepart(Sprites.hero.shipfill[y][x])
                                    self.shipoverview()
                    if mouse[0]:  # linkermuisknop
                        if self.shippartselected == True:  # onderstaande is voor als de cursor is vervangen door een schiponderdeel
                            self.placeshippart(mousepos, mouseimage)
                        else:
                            x = int((mousepos[0] - 69) / 60)
                            y = int((mousepos[1] - 529) / 60)
                            if x >= 0 and x < 9 and y >= 0 and y < 8:
                                if not isinstance(Sprites.hero.shipfill[y][x], int):
                                    Sounds.sounds.soundclick.play()
                                    Sprites.hero.shipfill[y][x].itemmenu()
                                    self.resetscreen()

                            # er wordt geklikt op het onderdelenmenu
                            for button in range(len(self.activenames)):
                                if self.activerects[button].collidepoint(mousepos):  # op een van de onderdelen van het hoofdmenu
                                    Sounds.sounds.soundclick.play()
                                    if self.menunumber == 0:
                                        self.menunumber = button + 1
                                        self.activenames = [GameplayConstants.shippartslist[self.menunumber][x][0] for x in range(len(GameplayConstants.shippartslist[self.menunumber]))]
                                        self.create_menu()
                                        Tools.refresh_menubutton(backrect, mousepos, "Back", True)  # back knop
                                        self.activebuttons2.append(backrect)  # backknop is 'actief' (kleur bij hover veranderd)

                                    else:  # op een van de onderdelen van het submenu
                                        self.shippartdisplayed = button
                                        image = GameplayConstants.shippartimages[self.menunumber - 1][self.shippartdisplayed]
                                        Tools.displayshippart(self.menunumber, self.shippartdisplayed, image, 1427, 730)

                                        pygame.draw.rect(screen, lightgray, pygame.Rect(1515, 550, 320, 260))
                                        text = GameplayConstants.shippartinfo(self.menunumber, self.shippartdisplayed,0)
                                        for line in range(len(text)):
                                            Tools.draw_text(screen, text[line], 15, 1525, 563 + 20 * line, "Xolonium")

                            # op de abortknop
                            if abortrect.collidepoint(mousepos):
                                Sounds.sounds.soundcancel.play()
                                self.menuloop()
                                return
                            # op de launchknop
                            elif launchrect.collidepoint(mousepos):
                                Sounds.sounds.soundclick.play()
                                self.gameloop()
                            elif backrect.collidepoint(mousepos) and self.menunumber != 0:
                                Sounds.sounds.soundcancel.play()
                                self.menunumber = 0
                                self.shippartselected = -1
                                self.activenames = [GameplayConstants.shippartslist[self.menunumber][x][0] for x in range(len(GameplayConstants.shippartslist[self.menunumber]))]
                                self.activebuttons2.pop(2)
                                self.create_menu()
                            # op het displayed onderdeel
                            elif self.shippartrect.collidepoint(mousepos) and self.shippartdisplayed >= 0:
                                if Sprites.hero.gold >= GameplayConstants.shippartprice(self.menunumber, self.shippartdisplayed, 0):
                                    Sounds.sounds.soundclick.play()
                                    mouseimage = GameplayConstants.shippartimages[self.menunumber - 1][self.shippartdisplayed]
                                    mouserect = image.get_rect()
                                    mouserect.center = (mousepos[0], mousepos[1])
                                    pygame.mouse.set_visible(False)
                                    pygame.mouse.set_pos(970, 530)
                                    screen.blit(mouseimage, mouserect)
                                    self.shippartselected = True
                                    shippartdrag = True
                                else:
                                    Sounds.sounds.soundfail.play()
            pygame.display.flip()
            clock.tick(GameplayConstants.fps)

    def placeshippart(self, mousepos, mouseimage):
        x = int((mousepos[0] - 69) / 60)
        y = int((mousepos[1] - 529) / 60)
        partlayout = GameplayConstants.shippartslist[self.menunumber][self.shippartdisplayed][2]
        height = len(partlayout)
        if isinstance(partlayout[0], tuple):
            width = len(partlayout[0])
        else:
            width = 1
        if x >= 0 and x <= 9 - width and y >= 0 and y <= 8 - height:  # past het object in het schipdisplay
            # in dit gedeelte wordt gekeken waar de hoek van het object zit.
            if width % 2 == 1:
                xadjusted = int(x - (width - 1) / 2)
            elif 100 + x * 60 > mousepos[0]:
                xadjusted = int(x - width / 2)
            else:
                xadjusted = x - int(((width - 2) / 2))
            if height % 2 == 1:
                yadjusted = int(y - (height - 1) / 2)
            elif 590 + x * 60 > mousepos[0]:
                yadjusted = int(y - height / 2)
            else:
                yadjusted = int(y - ((height - 2) / 2))
            # vanuit de hoek wordt gekeken of het object komt op een plek waar ruimte is.
            succes = True

            for stepdown in range(height):
                if width > 1:
                    for step in range(width):
                        if self.greenlist[yadjusted + stepdown][xadjusted + step] != 1 and partlayout[stepdown][step] == 1:
                            succes = False
                elif self.greenlist[yadjusted + stepdown][xadjusted] != 1 and partlayout[stepdown] == 1:
                    succes = False

            if succes == True:  # het onderdeel wordt geplaatst op een mogelijke plek.
                if self.menunumber == 1:
                    item = Hero.Weapon(self.shippartdisplayed, xadjusted, yadjusted,GameplayConstants.shippartimages[0][self.shippartdisplayed])
                    Sprites.hero.weapons.append(item)
                else:
                    item = Hero.Shippart(xadjusted, yadjusted, self.menunumber,self.shippartdisplayed)  # itemobject
                    Sprites.hero.shipparts.append(item)
                item.increasestats()  # geef hero de statsboost van het geplaatste item
                for stepdown in range(height):
                    if width > 1:
                        for step in range(width):
                            if partlayout[stepdown][step] == 1:
                                Sprites.hero.shipfill[yadjusted + stepdown][xadjusted + step] = item
                    elif partlayout[stepdown] == 1:
                        Sprites.hero.shipfill[yadjusted + stepdown][xadjusted] = item

                screen.blit(mouseimage, (70 + 60 * xadjusted, 530 + 60 * yadjusted))
                Sprites.hero.shippartsused.append(item)
                pygame.mouse.set_visible(True)
                self.shippartselected = False
                self.shipoverview()
                Sounds.sounds.soundimplement.play()

    def resetscreen(self):
        screen.blit(self.hangarpic, dest=(0, 0))
        pygame.draw.rect(screen, black, self.shippartmenurect)
        self.create_menu()
        self.shipoverview()
        if self.menunumber > 0 and self.shippartdisplayed >= 0:
            pygame.draw.rect(screen, lightgray, pygame.Rect(1515, 550, 320, 260))
            text = GameplayConstants.shippartinfo(self.menunumber, self.shippartdisplayed, 0)
            for line in range(len(text)):
                Tools.draw_text(screen, text[line], 15, 1525, 563 + 20 * line, "Xolonium")

    def shipinfo(self):
        weaponuse = 0
        for weapon in Sprites.hero.weapons:
            weaponuse += weapon.energyuse * (weapon.upgrades + 1) / weapon.cooldown * 60
        maxuse = round(Sprites.hero.energyuse + Sprites.hero.maxshield + weaponuse)

        text = GameplayConstants.heroshipinfo(maxuse)
        for line in range(len(text)):
            Tools.draw_text(screen, text[line], 15, 650, 545 + 20 * line, "Xolonium")

        if Sprites.hero.energyuse == maxuse and Sprites.hero.energyregen >= Sprites.hero.energyuse:
            energybalance = 1
        elif Sprites.hero.energyuse == maxuse and Sprites.hero.energyregen <= Sprites.hero.energyuse:
            energybalance = 0
        else:
            energybalance = max(0, min(1, (Sprites.hero.energyregen - Sprites.hero.energyuse) / (maxuse - Sprites.hero.energyuse)))
        pygame.draw.rect(screen, black,pygame.Rect(604, 572 + (432 * (1 - energybalance)), 40, 6))  # indicator op energymeter

    def shipoverview(self):
        goldrect = pygame.Rect(30, 30, 400, 50)
        gold = Sprites.hero.gold
        pygame.draw.rect(screen, lightgray, goldrect)
        Tools.draw_text(screen, "Gold: " + str(gold), 35, 40, 55, "Xolonium")

        background = pygame.Rect(70, 530, 537, 477)
        pygame.draw.rect(screen, blackgray, background)
        screen.blit(self.shipimage, dest=(195, 590))
        screen.blit(self.energymeter, dest=(607, 530))

        textrect = pygame.Rect(640, 530, 240, 477)
        pygame.draw.rect(screen, lightgray, textrect)
        self.shipinfo()

        s2 = pygame.Surface((60, 60))
        s2.set_alpha(50)
        s2.fill(darkgreen)
        self.greenlist = [[0 for x in range(9)] for y in range(8)]

        # display geplaatste scheepsonderdelen
        for shippart in Sprites.hero.shippartsused:
            image = shippart.image
            rect = image.get_rect()
            rect.top = 530 + int(shippart.ypos) * 60
            rect.left = 70 + int(shippart.xpos) * 60
            screen.blit(image, rect)

        if self.shippartselected == False:
            for x in range(9):
                for y in range(8):
                    if isinstance(Sprites.hero.shipfill[y][x], int):
                        if Sprites.hero.shipfill[y][x] > 0 and Sprites.hero.shipfill[y][x] <= 1:
                            pygame.draw.rect(screen, lightgray, pygame.Rect(70 + x * 60, 530 + y * 60, 57, 57), 2)
        else:  # onderstaande is het inventariseren waar op het schip het geselecteerde object kan worden geplaatst.
            partlayout = GameplayConstants.shippartslist[self.menunumber][self.shippartdisplayed][2]
            height = len(partlayout)
            if isinstance(partlayout[0], tuple):
                width = len(partlayout[0])
            else:
                width = 1
            for x in range(9 - (width - 1)):
                for y in range(8 - (height - 1)):
                    succes = True
                    for step in range(height):
                        if width > 1:
                            for stepdown in range(width):
                                if Sprites.hero.shipfill[y + step][x + stepdown] != 1 and partlayout[step][
                                    stepdown] == 1:
                                    succes = False
                        elif Sprites.hero.shipfill[y + step][x] != 1:
                            succes = False
                    if succes == True:
                        for stepdown in range(height):
                            if width > 1:
                                for step in range(width):
                                    if partlayout[stepdown][step] == 1 and self.greenlist[y + stepdown][x + step] == 0:
                                        self.greenlist[y + stepdown][x + step] = 1
                                        screen.blit(s2, (70 + (x + step) * 60, 530 + (y + stepdown) * 60))
                                        pygame.draw.rect(screen, darkgreen,pygame.Rect(70 + (x + step) * 60, 530 + (y + stepdown) * 60,57, 57), 2)
                            elif self.greenlist[y + stepdown][x] == 0:
                                self.greenlist[y + stepdown][x] = 1
                                screen.blit(s2, (70 + x * 60, 530 + (y + stepdown) * 60))
                                pygame.draw.rect(screen, darkgreen,pygame.Rect(70 + x * 60, 530 + (y + stepdown) * 60, 57, 57), 2)
            for x in range(9):
                for y in range(8):
                    if self.greenlist[y][x] == 0 and Sprites.hero.shipfill[y][x] == 1:
                        pygame.draw.rect(screen, darkred, pygame.Rect(70 + x * 60, 530 + y * 60, 57, 57), 2)

    def create_menu(self):
        basex = 900
        pygame.draw.rect(screen, blackgray, pygame.Rect(basex, 530, 950, 477))
        mousepos = pygame.mouse.get_pos()
        for x in range(len(self.activenames)):
            pygame.draw.rect(screen, black, pygame.Rect(basex + 17, 550 + x * 60, 406, 56))
            Tools.refresh_menubutton(self.activerects[x], mousepos, self.activenames[x], True)
        for button in range(len(self.activebuttons2)):
            Tools.refresh_menubutton(self.activebuttons2[button], mousepos, self.activebuttons2names[button], True)
        self.shippartrect = pygame.Rect(basex + 435, 550, 180, 360)
        pygame.draw.rect(screen, black, self.shippartrect)

    def gameloop(self):
        # levelinit
        self.level = Level.Level()
        Sprites.hero.refuel()
        Sprites.all_sprites.add(Sprites.hero)
        pygame.mouse.set_visible(False)
        # maak sidebar
        self.scorerect = pygame.Rect(1610, 38, 280, 40)
        self.barrects = []
        for x in range(3):
            self.barrects.append(pygame.Rect(1474, 820 + x * 80, 413, 40))
        # pygame.display.update()
        running = True
        while running:
            # Eventcheck
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                # mousemovement and click
                elif event.type == pygame.MOUSEMOTION:
                    Sprites.hero.movement(event)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.gamemenu()
            # hero projectiles
            mouse = pygame.mouse.get_pressed()
            for button in range(3):
                if mouse[button]:
                    for weapon in Sprites.hero.weapons:
                        if weapon.keybind == button:
                            weapon.fireevent()
            # Spawn enemies
            self.level.spawning()
            # Update
            Sprites.background.update()
            Sprites.all_sprites.update()
            # Collisioncheck
            hits = pygame.sprite.groupcollide(Sprites.mobs, Sprites.herobullets, False, False)
            for mob in hits:  # collision herobullets-mobs
                for bullet in hits[mob]:
                    Sprites.hero.score += mob.getdamage(bullet.damage)
                    bullet.hit()
            if Sprites.hero.alive == True:
                hits = pygame.sprite.spritecollide(Sprites.hero, Sprites.mobbullets, True, pygame.sprite.collide_circle)
                for bullet in hits:  # collision player - mobbullets
                    if Sprites.hero.getdamage(bullet.damage, bullet):
                        self.level.abort = True
                hits = pygame.sprite.spritecollide(Sprites.hero, Sprites.mobs, False, pygame.sprite.collide_circle)
                for mob in hits:  # collision player-mobs
                    if Sprites.hero.getdamage(4, mob):
                        self.level.abort = True
                    Sprites.hero.score += mob.getdamage(4)

                hits = pygame.sprite.spritecollide(Sprites.hero, Sprites.powerups, True, pygame.sprite.collide_circle)
                for powerup in hits:  # collision player powerups
                    Sprites.hero.gold += powerup.collect()
                    Sounds.sounds.pickupsound.play()
            # check end level
            if self.level.end and len(Sprites.mobs) == 0 and len(Sprites.powerups) == 0 or self.level.abort:
                self.endlevel(self.level.succes)
                return
            # Draw / render
            pygame.draw.rect(screen, black, warrect)
            Sprites.background.draw(screen)
            Sprites.all_sprites.draw(screen)
            self.sidebar()
            # keep loop running at the right speed
            clock.tick(GameplayConstants.fps)
            pygame.display.flip()

    def sidebar(self):
        pygame.draw.rect(screen, darkgray, sidebarrect)
        pygame.draw.rect(screen, black, pygame.Rect(1455, 30, 450, 60))
        pygame.draw.rect(screen, lightgray, pygame.Rect(1458, 33, 444, 54))
        pygame.draw.rect(screen, black, pygame.Rect(1455, 120, 450, 60))
        pygame.draw.rect(screen, lightgray, pygame.Rect(1458, 123, 444, 54))
        Tools.draw_text(screen, "Score:", 38, 1475, 60, "Xolonium")
        Tools.draw_text(screen, "Gold:", 38, 1475, 150, "Xolonium")

        Tools.draw_text(screen, "Energy", 35, 1482, 803, "Xolonium")
        Tools.draw_text(screen, "Shield", 35, 1482, 883, "Xolonium")
        Tools.draw_text(screen, "Armor", 35, 1482, 963, "Xolonium")

        # statusbars
        barfill = [Sprites.hero.energy, Sprites.hero.shield, Sprites.hero.armor]
        startx = 1474
        starty = 820
        barheight = 40
        barwidth = 413
        spacing = 80
        fills = []
        fills.append(pygame.Rect(self.barrects[0].left + 3, self.barrects[0].top + 3,
                                 Sprites.hero.energy / Sprites.hero.maxenergy * 413, 36))
        if Sprites.hero.maxshield:
            fills.append(pygame.Rect(self.barrects[1].left + 3, self.barrects[1].top + 3,
                                     Sprites.hero.shield / Sprites.hero.maxshield * 413, 36))
        else:
            fills.append(pygame.Rect(0, 0, 0, 0))
        fills.append(pygame.Rect(self.barrects[2].left + 3, self.barrects[2].top + 3,
                                 Sprites.hero.armor / Sprites.hero.maxarmor * 413, 36))
        for barnr in range(3):
            fill = pygame.Rect(startx + 3, starty + 3 + barnr * spacing, (barwidth - 6) / 100 * barfill[barnr],barheight - 6)
            pygame.draw.rect(screen, black, self.barrects[barnr])
            pygame.draw.rect(screen, colorbars[barnr], fills[barnr])
        # score
        pygame.draw.rect(screen, lightgray, self.scorerect)
        Tools.draw_text(screen, str(Sprites.hero.score), 38, 1610, 60, "Xolonium")
        Tools.draw_text(screen, str(Sprites.hero.gold), 38, 1610, 150, "Xolonium")

    def endlevel(self, levelsucces):
        if not levelsucces:
            Sprites.hero.gold = self.level.startgold
            Sprites.hero.score = self.level.startscore
            Sprites.mobs.empty()
            Sprites.powerups.empty()
        Sprites.background.empty()
        Sprites.herobullets.empty()
        Sprites.mobbullets.empty()
        Sprites.all_sprites.empty()
        self.resetscreen()
        pygame.mouse.set_visible(True)

    def generate_menu(self, buttonlist):
        buttoncount = len(buttonlist)
        buttonrects = []
        pygame.draw.rect(screen, darkgray,pygame.Rect(windowwidth / 2 - 300, windowheight / 2 - 30 * buttoncount - 20, 600,60 * buttoncount + 30))
        mousepos = pygame.mouse.get_pos()
        for button in range(buttoncount):
            if isinstance(buttonlist[button], tuple):
                dragrect = pygame.Rect(windowwidth / 2 - 275, windowheight / 2 - 30 * buttoncount + 60 * button, 550, 80)
                if buttonlist[button][0] == "Game speed":
                    positions = 6
                    position = (GameplayConstants.fps - 30) / 5
                elif buttonlist[button][0] == "Music volume":
                    positions = 100
                    position = GameplayConstants.musicvolume
                elif buttonlist[button][0] == "Effects volume":
                    positions = 100
                    position = GameplayConstants.effectsvolume
                buttonrects.append(Tools.create_dragbar(dragrect, buttonlist[button][0], positions, position))
            else:
                buttonrects.append(pygame.Rect(windowwidth / 2 - 275, windowheight / 2 - 30 * buttoncount + 60 * button, 550, 50))
                pygame.draw.rect(screen, black, buttonrects[button])
                Tools.refresh_menubutton(buttonrects[button], mousepos, buttonlist[button], True)
        pygame.display.flip()
        return buttonrects

    def gamemenu(self):
        running = True
        pygame.mouse.set_visible(True)

        screenalpha = pygame.Surface((1920, 1080))
        screenalpha.set_alpha(150)
        screenalpha.fill(black)
        screen.blit(screenalpha, dest=(0, 0))
        buttonlist = ["Quit game", "Abort mission", "Settings", "Resume"]
        buttonrects = self.generate_menu(buttonlist)

        while running:
            mousepos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pressed()
                    if mouse[0]:
                        if buttonrects[0].collidepoint(mousepos):
                            pygame.quit()
                        elif buttonrects[1].collidepoint(mousepos):
                            self.level.abort = True
                            Sounds.sounds.soundclick.play()
                            return
                        elif buttonrects[2].collidepoint(mousepos):
                            self.optionmenu()
                            self.generate_menu(buttonlist)
                            Sounds.sounds.soundclick.play()
                        elif buttonrects[3].collidepoint(mousepos):
                            pygame.mouse.set_visible(False)
                            Sounds.sounds.soundclick.play()
                            return
                elif event.type == pygame.MOUSEMOTION:
                    self.generate_menu(buttonlist)
            clock.tick(GameplayConstants.fps)

    def optionmenu(self):
        running = True
        drag = False
        buttonrects = self.generate_menu([("Game speed", 7), ("Music volume", 7), ("Effects volume", 7), "Back"])
        while running:
            mousepos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pressed()
                    if mouse[0]:
                        if buttonrects[0].collidepoint(mousepos):
                            x = int((mousepos[0] - buttonrects[0].left)/(buttonrects[0].width/7))
                            GameplayConstants.fps = 30+x*5
                            Sounds.sounds.soundclick.play()
                            drag = True
                            choice = 0
                        elif buttonrects[1].collidepoint(mousepos):
                            x = int((mousepos[0] - buttonrects[0].left) / (buttonrects[0].width / 101))
                            GameplayConstants.musicvolume = x
                            Sounds.sounds.soundclick.play()
                            pygame.mixer.music.set_volume(GameplayConstants.musicvolume / 100)
                            drag = True
                            choice = 1
                        elif buttonrects[2].collidepoint(mousepos):
                            x = int((mousepos[0] - buttonrects[0].left) / (buttonrects[0].width / 101))
                            GameplayConstants.effectsvolume = x
                            Sounds.sounds.soundchange()
                            Sounds.sounds.soundclick.play()
                            drag = True
                            choice = 2
                        elif buttonrects[3].collidepoint(mousepos):
                            Sounds.sounds.soundclick.play()
                            return
                        else:
                            choice = 3
                    self.generate_menu([("Game speed", 7), ("Music volume", 100), ("Effects volume", 100), "Back"])
                elif event.type == pygame.MOUSEMOTION:
                    self.generate_menu([("Game speed", 7), ("Music volume", 100), ("Effects volume", 100), "Back"])
                    if drag == True and choice < 3:
                        if choice == 0:
                            x = max(0,min(6,int((mousepos[0] - buttonrects[0].left)/(buttonrects[0].width/7))))
                            GameplayConstants.fps = 30+x*5
                        elif choice == 1:
                            x = max(0,min(100,int((mousepos[0] - buttonrects[0].left) / (buttonrects[0].width / 101))))
                            GameplayConstants.musicvolume = x
                            pygame.mixer.music.set_volume(GameplayConstants.musicvolume/100)
                        elif choice == 2:
                            x = max(0,min(100,int((mousepos[0] - buttonrects[0].left) / (buttonrects[0].width / 101))))
                            GameplayConstants.effectsvolume = x
                            Sounds.sounds.soundchange()
                elif event.type == pygame.MOUSEBUTTONUP:
                    drag = False

            clock.tick(GameplayConstants.fps)


game = Game()
game.menuloop()
pygame.quit()