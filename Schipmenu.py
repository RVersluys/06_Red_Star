import pygame
import os
import pickle
import datetime


import GameplayConstants
import Tools
import Player
import Gamedata
import Sounds
import Gameloop
import Colors
import Button
import Missioninformation
import IngamePrompt

game_folder = os.path.dirname(__file__)
clock = pygame.time.Clock()

class Schipmenu:
    def __init__(self):
        # laden images
        self.hangarpic = pygame.image.load(os.path.join(game_folder, "img", "hangar.png")).convert()
        self.energymeter = pygame.image.load(os.path.join(game_folder, "img", "Parts", "energymeter.png")).convert()

        # deze variabelen houden bij waar de speler is in het menu.
        self.menunumber = 0
        self.shippartselected = False  # Een shippart is geselecteerd en vervangt de muis
        self.shippartdisplayed = -1  # schippartnr displayed, -1 = geen shippart

        self.shippartmenurect = pygame.Rect(55, 515, 1810, 507)  # groot blok onderaan

        # menuknoppen
        self.menu = [Button.Button(pygame.Rect(920, 935, 400, 50), "Back", "Back", False),
                     Button.Button(pygame.Rect(1535, 935, 300, 60), "Launch", "Launch", False, Button.buttonlaunch),
                     Button.Button(pygame.Rect(30, 30, 400, 50), "Quit", "Quit", False),
                     Button.Button(pygame.Rect(30, 90, 400, 50), "Save Game", "Save Game", False),
                     Button.Button(pygame.Rect(1335, 910, 180, 50), "Rotate", "Rotate", False)]

        self.submenu = [Button.Button(pygame.Rect(920, 553 + x * 60, 400, 50), "", x, False) for x in range(6)]
        self.shippartdrag = False

    def shipmenuloop(self):
        self.shipimage = GameplayConstants.shipimages[Gamedata.player.ship]
        for x in range(1,4):
            self.menu[x].active = True
        levelinforect = pygame.Rect(600, 50, 720, 400)
        self.levelinfo = Missioninformation.Missioninfo(levelinforect)
        self.resetscreen()



        while True:
            for event in pygame.event.get():
                mousepos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEMOTION:
                    # beweging van de muis bij een geselecteerd schiponderdeel
                    if self.shippartselected == True:
                        mouserect.center = (mousepos[0], mousepos[1])
                        self.resetscreen()
                        GameplayConstants.screen.blit(self.partimage, mouserect)
                    else:
                        # kleuren van de knoppen bij het er overheen hoveren.
                        for button in self.menu:
                            button.update()
                        for button in self.submenu:
                            button.update()

                elif event.type == pygame.MOUSEBUTTONUP and self.shippartdrag:
                    self.placeshippart(mousepos)
                    self.shippartdrag = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pressed()
                    if mouse[2]:  # rechtermuisknop
                        if self.shippartselected == True:  # deselecteer een schipdeel
                            Sounds.sounds.soundcancel.play()
                            pygame.mouse.set_visible(True)
                            self.shippartselected = False
                            self.resetscreen()
                        else:  # verwijder een schipdeel in het schip met de rechter muisknop
                            x = int((mousepos[0] - 69) / 60)
                            y = int((mousepos[1] - 559) / 60)
                            if x >= 0 and x <= 9 and y >= 0 and y <= 9:
                                if not isinstance(Gamedata.player.shipfill[y][x], int):
                                    Sounds.sounds.soundremove.play()
                                    Gamedata.player.removepart(Gamedata.player.shipfill[y][x])
                                    self.shipoverview()
                    if mouse[0]:  # linkermuisknop
                        if self.shippartselected == True:  # onderstaande is voor als de cursor is vervangen door een schiponderdeel
                            self.placeshippart(mousepos)
                        else:
                            x = int((mousepos[0] - 69) / 60)
                            y = int((mousepos[1] - 559) / 60)
                            if x >= 0 and x < 9 and y >= 0 and y < 9:
                                if not isinstance(Gamedata.player.shipfill[y][x], int):
                                    Sounds.sounds.soundclick.play()
                                    Gamedata.player.shipfill[y][x].itemmenu()
                                    self.resetscreen()
                            # er wordt geklikt op het onderdelenmenu
                            for button in self.submenu: # op een van de onderdelen van het hoofdmenu
                                if button.rect.collidepoint(mousepos) and button.active:
                                    if self.menunumber == 0:
                                        self.menunumber = button.function + 1
                                        for x in range(len(GameplayConstants.shippartslist[self.menunumber])):
                                            self.submenu[x].text = GameplayConstants.shippartslist[self.menunumber][x][0]
                                            self.submenu[x].active = True
                                        for x in range(len(GameplayConstants.shippartslist[self.menunumber]), 6):
                                            self.submenu[x].active = False
                                        self.menu[0].active = True #activeer back knop
                                        self.menu[0].update()
                                    else: # op een van de onderdelen van het submenu
                                        self.rotations = 0
                                        self.shippartdisplayed = button.function
                                        self.partimage = GameplayConstants.shippartimages[self.menunumber - 1][self.shippartdisplayed]
                                        if self.menunumber == 5:
                                            price = GameplayConstants.shippartslist[5][self.shippartdisplayed][1]*900
                                            price -= GameplayConstants.shippartslist[5][Gamedata.player.ship][1]*900
                                            for part in Gamedata.player.shippartsused:
                                                partworth = 0
                                                for x in range(part.upgrades + 1):
                                                    partworth += GameplayConstants.shippartprice(part.type, part.index, x)
                                                price -= partworth
                                            if Gamedata.player.gold - price >= 0 and self.shippartdisplayed != Gamedata.player.ship:
                                                self.menu[4].text = "Buy"
                                                self.menu[4].function = "Buy"
                                                self.menu[4].active = True  # activeer buyknop als er genoeg geld is
                                            else:
                                                self.menu[4].active = False
                                        else:
                                            self.shippartshape = GameplayConstants.shippartslist[self.menunumber][self.shippartdisplayed][2]

                                        if self.menunumber == 3 or self.menunumber == 4:
                                            self.menu[4].text = "Rotate"
                                            self.menu[4].function = "Rotate"
                                            self.menu[4].active = True #activeer rotateknop
                                        text = GameplayConstants.shippartinfo(self.menunumber, self.shippartdisplayed, 0)
                                        for line in range(len(text)):
                                            Tools.draw_text(GameplayConstants.screen, text[line], 15, 1525, 563 + 20 * line, "Xolonium")
                                    self.resetscreen()
                            for button in self.menu:
                                if button.rect.collidepoint(mousepos) and button.active:
                                    if button.function == "Quit":
                                        Sounds.sounds.soundcancel.play()
                                        return
                                    elif button.function == "Launch":
                                        Sounds.sounds.soundclick.play()

                                        succes = Gameloop.Gameloop()

                                        if succes:
                                            Gamedata.player.levelnumber += 1
                                            if Gamedata.player.levelnumber == 2:
                                                IngamePrompt.IngamePrompt("brokenship.jpg", Missioninformation.prompt2Options, Missioninformation.prompt2)

                                            filepath = os.path.join(game_folder, 'savegames', 'auto_save.pickle')
                                            pickle_out = open(filepath, "wb")
                                            pickle.dump(Gamedata.player, pickle_out)
                                            Gamedata.halloffame.addscore("Player", Gamedata.player.score)
                                            self.levelinfo = Missioninformation.Missioninfo(levelinforect)
                                        self.resetscreen()
                                    elif button.function == "Back":
                                        Sounds.sounds.soundcancel.play()
                                        self.menunumber = 0
                                        self.shippartdisplayed = -1
                                        self.shippartselected = False
                                        self.menu[0].active = False
                                        self.menu[4].active = False
                                        self.resetscreen()
                                    elif button.function == "Save Game":
                                        self.savegameloop()
                                        self.resetscreen()
                                    elif button.function == "Rotate":
                                        self.shippartshape = self.rotateshippart(self.shippartshape)
                                        self.partimage = pygame.transform.rotate(GameplayConstants.shippartimages[self.menunumber - 1][self.shippartdisplayed], -self.rotations * 90)
                                        self.resetscreen()
                                    elif button.function == "Buy":
                                        self.menu[4].active = False
                                        Gamedata.player.changeship(self.shippartdisplayed)
                                        self.shipimage = GameplayConstants.shipimages[Gamedata.player.ship]
                                        self.resetscreen()

                            # op het displayed onderdeel
                            if self.shippartrect.collidepoint(mousepos) and self.shippartdisplayed >= 0 and self.menunumber != 5:
                                if Gamedata.player.gold >= GameplayConstants.shippartprice(self.menunumber, self.shippartdisplayed, 0):
                                    Sounds.sounds.soundclick.play()
                                    self.partimage = pygame.transform.rotate(GameplayConstants.shippartimages[self.menunumber - 1][self.shippartdisplayed], -self.rotations * 90)
                                    mouserect = self.partimage.get_rect()
                                    mouserect.center = (mousepos[0], mousepos[1])
                                    pygame.mouse.set_visible(False)
                                    pygame.mouse.set_pos(970, 530)
                                    GameplayConstants.screen.blit(self.partimage, mouserect)
                                    self.shippartselected = True
                                    self.shippartdrag = True
                                else:
                                    Sounds.sounds.soundfail.play()
            pygame.display.flip()
            clock.tick(GameplayConstants.fps)


    def rotateshippart(self, shippart):
        newobject = []
        height = len(shippart)
        width = len(shippart[0])
        for x in range(width):
            list = []
            for y in range(height):
                list.append(shippart[height - (y + 1)][x])
            newobject.append(list)
        self.rotations = (self.rotations + 1) % 4
        return newobject


    def savegameloop(self):
        pygame.draw.rect(GameplayConstants.screen, Colors.darkgray, pygame.Rect(GameplayConstants.windowwidth / 2 - 300, GameplayConstants.windowheight / 2 - 350, 600, 700))
        filelist = Tools.get_savegames()
        savegamebuttons = []
        filenr = 1
        for file in filelist:
            rect = pygame.Rect(GameplayConstants.windowwidth / 2 - 275, GameplayConstants.windowheight / 2 - 330 + 60 * (filenr-1), 550, 50)
            path = os.path.join(game_folder, "savegames", str(file[0] + file[1]))
            date = datetime.datetime.fromtimestamp(os.path.getmtime(path)).strftime('%d-%m-%Y %H:%M:%S')
            text = file[0] + " - (" + str(date) + ")"
            savegamebuttons.append(Button.Selectable(rect, text, filenr))
            filenr += 1
        for emptyslot in range(len(filelist), 10):
            rect = pygame.Rect(GameplayConstants.windowwidth / 2 - 275, GameplayConstants.windowheight / 2 - 330 + 60 * (emptyslot), 550, 50)
            text = "EMPTY SLOT"
            savegamebuttons.append(Button.Selectable(rect, text, filenr))
            filenr += 1
        savegamebuttons.append(Button.Button(pygame.Rect(GameplayConstants.windowwidth / 2 - 275, GameplayConstants.windowheight / 2 + 280, 550, 50), "Save game", "Save"))
        pygame.display.flip()
        selectedfile = False
        while True:
            for event in pygame.event.get():
                mousepos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        Sounds.sounds.soundcancel.play()
                        return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pressed()
                    if mouse[0]:
                        for button in savegamebuttons:
                            if type(button) is Button.Selectable:
                                if button.selected:
                                    button.selected = False
                                    if button.rect.collidepoint(mousepos):
                                        selectedfile = False
                                elif button.rect.collidepoint(mousepos):
                                    button.selected = True
                                    selectedfile = button.file
                            elif button.function == "Save" and button.rect.collidepoint(mousepos):
                                if selectedfile:
                                    filepath = os.path.join(game_folder, 'savegames', str(selectedfile) + '.pickle')
                                    pickle_out = open(filepath, "wb")
                                    pickle.dump(Gamedata.player, pickle_out)
                                    Sounds.sounds.soundimplement.play()
                                else:
                                    Sounds.sounds.soundfail.play()
                                return
                            button.update()

                elif event.type == pygame.MOUSEMOTION:
                    for button in savegamebuttons:
                        button.update()
            clock.tick(GameplayConstants.fps)
            pygame.display.flip()


    def placeshippart(self, mousepos):
        x = int((mousepos[0] - 69) / 60)
        y = int((mousepos[1] - 559) / 60)
        height = len(self.shippartshape)
        width = len(self.shippartshape[0])
        if x >= 0 and x <= 9 - width and y >= 0 and y <= 9 - height:  # past het object in het schipdisplay
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
                        if self.greenlist[yadjusted + stepdown][xadjusted + step] != 1 and self.shippartshape[stepdown][step] == 1:
                            succes = False
                elif self.greenlist[yadjusted + stepdown][xadjusted] != 1:
                    succes = False

            if succes == True:  # het onderdeel wordt geplaatst op een mogelijke plek.
                if self.menunumber == 1:
                    item = Player.Weapon(self.shippartdisplayed, xadjusted, yadjusted, self.shippartshape)
                    Gamedata.player.weapons.append(item)
                else:
                    item = Player.Shippart(xadjusted, yadjusted, self.menunumber, self.shippartdisplayed, self.shippartshape, self.rotations)  # itemobject
                    Gamedata.player.shipparts.append(item)
                item.changestats(1)  # geef hero de statsboost van het geplaatste item
                for stepdown in range(height):
                    if width > 1:
                        for step in range(width):
                            if self.shippartshape[stepdown][step] == 1:
                                Gamedata.player.shipfill[yadjusted + stepdown][xadjusted + step] = item
                    else:
                        Gamedata.player.shipfill[yadjusted + stepdown][xadjusted] = item
                        #GameplayConstants.screen.blit(self.partimage, (70 + 60 * xadjusted, 560 + 60 * yadjusted))
                Gamedata.player.shippartsused.append(item)
                pygame.mouse.set_visible(True)
                self.shippartselected = False
                #self.shipoverview()
                Sounds.sounds.soundimplement.play()
                self.resetscreen()


    def resetscreen(self):
        GameplayConstants.screen.blit(self.hangarpic, dest=(0, 0))
        self.create_menu()
        self.shipoverview()
        if self.menunumber > 0 and self.shippartdisplayed >= 0:
            text = GameplayConstants.shippartinfo(self.menunumber, self.shippartdisplayed, 0)
            for line in range(len(text)):
                Tools.draw_text(GameplayConstants.screen, text[line], 13, 1555, 575 + 17 * line, "Xolonium", Colors.white)
        self.levelinfo.update()


    def shipinfo(self):
        weaponuse = 0
        for weapon in Gamedata.player.weapons:
            weaponuse += weapon.energyuse * (weapon.upgrades + 1) / weapon.cooldown * 60
        maxuse = round(Gamedata.player.energyuse + Gamedata.player.maxshield + weaponuse)

        text = GameplayConstants.heroshipinfo(maxuse)
        for line in range(len(text)):
            Tools.draw_text(GameplayConstants.screen, text[line], 15, 660, 560 + 20 * line, "Xolonium", Colors.white)

        if Gamedata.player.energyuse == maxuse and Gamedata.player.energyregen >= Gamedata.player.energyuse:
            energybalance = 1
        elif Gamedata.player.energyuse == maxuse and Gamedata.player.energyregen <= Gamedata.player.energyuse:
            energybalance = 0
        else:
            energybalance = max(0, min(1, (Gamedata.player.energyregen - Gamedata.player.energyuse) / (maxuse - Gamedata.player.energyuse)))
        pygame.draw.rect(GameplayConstants.screen, Colors.black, pygame.Rect(604, 572 + (432 * (1 - energybalance)), 40, 6))  # indicator op energymeter


    def shipoverview(self):
        goldrect = pygame.Rect(1490, 30, 400, 50)
        gold = Gamedata.player.gold
        pygame.draw.rect(GameplayConstants.screen, Colors.lightgray, goldrect)
        Tools.draw_text(GameplayConstants.screen, "Gold: " + str(gold), 35, 1495, 55, "Xolonium")
        GameplayConstants.screen.blit(self.shipimage, dest= GameplayConstants.shippartslist[5][Gamedata.player.ship][8])
        GameplayConstants.screen.blit(self.energymeter, dest=(607, 530))
        self.shipinfo()
        s2 = pygame.Surface((60, 60))
        s2.set_alpha(50)
        s2.fill(Colors.darkgreen)
        self.greenlist = [[0 for x in range(9)] for y in range(8)]
        freelist = [[False for x in range(9)] for y in range(8)]

        # display geplaatste scheepsonderdelen
        for shippart in Gamedata.player.shippartsused:
            image = pygame.transform.rotate(GameplayConstants.shippartimages[shippart.type - 1][shippart.index], -shippart.rotations * 90)
            rect = image.get_rect()
            rect.top = 560 + int(shippart.ypos) * 60
            rect.left = 70 + int(shippart.xpos) * 60
            GameplayConstants.screen.blit(image, rect)

        for x in range(9):
            for y in range(8):
                if isinstance(Gamedata.player.shipfill[y][x], int):
                    if Gamedata.player.shipfill[y][x] > 0 and Gamedata.player.shipfill[y][x] <= Gamedata.player.ship + 1:
                        if self.shippartselected == False:
                            pygame.draw.rect(GameplayConstants.screen, Colors.lightgray, pygame.Rect(70 + x * 60, 560 + y * 60, 57, 57), 2)
                        else:
                            freelist[y][x] = True
        if self.shippartselected:  # onderstaande is het inventariseren waar op het schip het geselecteerde object kan worden geplaatst.
            height = len(self.shippartshape)
            width = len(self.shippartshape[0])
            for x in range(9 - (width - 1)):
                for y in range(8 - (height - 1)):
                    succes = True
                    for step in range(height):
                        if width > 1:
                            for stepdown in range(width):
                                if not freelist[y + step][x + stepdown] and self.shippartshape[step][stepdown] == 1:
                                    succes = False
                        elif not freelist[y + step][x]:
                            succes = False
                    if succes == True:
                        for stepdown in range(height):
                            if width > 1:
                                for step in range(width):
                                    if self.shippartshape[stepdown][step] == 1 and self.greenlist[y + stepdown][x + step] == 0:
                                        self.greenlist[y + stepdown][x + step] = 1
                                        GameplayConstants.screen.blit(s2, (70 + (x + step) * 60, 560 + (y + stepdown) * 60))
                                        pygame.draw.rect(GameplayConstants.screen, Colors.darkgreen, pygame.Rect(70 + (x + step) * 60, 560 + (y + stepdown) * 60, 57, 57), 2)
                            elif self.greenlist[y + stepdown][x] == 0:
                                self.greenlist[y + stepdown][x] = 1
                                GameplayConstants.screen.blit(s2, (70 + x * 60, 560 + (y + stepdown) * 60))
                                pygame.draw.rect(GameplayConstants.screen, Colors.darkgreen, pygame.Rect(70 + x * 60, 560 + (y + stepdown) * 60, 57, 57), 2)
            for x in range(9):
                for y in range(8):
                    if self.greenlist[y][x] == 0 and Gamedata.player.shipfill[y][x] == 1:
                        pygame.draw.rect(GameplayConstants.screen, Colors.darkred, pygame.Rect(70 + x * 60, 560 + y * 60, 57, 57), 2)

    def create_menu(self):
        for x in range(len(GameplayConstants.shippartslist[self.menunumber])):
            self.submenu[x].active = True
            self.submenu[x].text = GameplayConstants.shippartslist[self.menunumber][x][0]
            self.submenu[x].update()
        for button in self.submenu:
            button.update()
        for button in self.menu:
            button.update()
        self.shippartrect = pygame.Rect(1335, 550, 180, 360)
        if self.shippartdisplayed != -1 and self.menunumber != 5:
            Tools.displayshippart(self.partimage, 1427, 730, self.shippartshape)
        elif self.shippartdisplayed != -1 and self.menunumber == 5:
            Tools.displayshippart(self.partimage, 1427, 730)