import pygame
import os
import pickle
import datetime

windowwidth = 1920
windowheight = 1080

# initieren van pygame
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((windowwidth, windowheight), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.FULLSCREEN)
clock = pygame.time.Clock()
pygame.display.set_caption("Red Star")

import GameplayConstants
GameplayConstants.screen = screen
import Tools
import Player
import Gamedata
import Sounds
import Gameloop
import Colors
import Button

game_folder = os.path.dirname(__file__)
fps = GameplayConstants.fps


class Game:
    def __init__(self):
        # initialize music
        pygame.mixer.music.load(os.path.join(game_folder, 'sounds', 'music', 'Hymne.mp3'))
        pygame.mixer.music.set_volume(GameplayConstants.musicvolume/100)
        pygame.mixer.music.play(loops=-1)

    def menuloop(self):
        running = True
        self.background = pygame.image.load(os.path.join(game_folder, "img", "menu.png")).convert()
        screen.blit(self.background, dest=(0, 0))
        self.menu = [Button.Button(pygame.Rect(54, 141, 234, 54),"Continue","Continue"),
                     Button.Button(pygame.Rect(54, 211, 234, 54),"New Game", "New Game"),
                     Button.Button(pygame.Rect(54, 281, 234, 54), "Settings", "Settings"),
                     Button.Button(pygame.Rect(54, 351, 234, 54), "Load Game", "Load Game"),
                     Button.Button(pygame.Rect(54, 421, 234, 54), "Hall of Fame", "Hall of Fame"),
                     Button.Button(pygame.Rect(54, 491, 234, 54), "Quit", "Quit")]
        self.submenu = []
        self.choice = -1
        self.filepath = ""
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
                        for button in self.menu:
                            if button.rect.collidepoint(mousepos):
                                if button.function == "Continue":
                                    filepath = os.path.join(game_folder, 'savegames', 'auto_save.pickle')
                                    if os.path.isfile(filepath):
                                        Sounds.sounds.soundclick.play()
                                        pickle_in = open(filepath, "rb")
                                        Gamedata.player = pickle.load(pickle_in)
                                        self.shipmenuloop()
                                    else:
                                        Sounds.sounds.soundfail.play()
                                elif button.function == "New Game":
                                    Sounds.sounds.soundclick.play()
                                    Gamedata.player = Player.Player()
                                    self.shipmenuloop()
                                elif button.function == "Settings":
                                    pass
                                elif button.function == "Load Game":
                                    self.generate_submenu(button)
                                elif button.function == "Quit":
                                    pygame.quit()
                        for button in self.submenu:
                            if type(button) is Button.Selectable:
                                if button.rect.collidepoint(mousepos):
                                    if button.selected == False:
                                        button.selected = True
                                        self.filepath = os.path.join(game_folder, 'savegames', str(button.file[0] + button.file[1]))
                                    else:
                                        button.selected = False
                                        self.filepath = False
                                else:
                                    button.selected = False
                            else:
                                if button.function == "Load" and button.rect.collidepoint(mousepos):
                                    if self.filepath != "":
                                        pickle_in = open(self.filepath, "rb")
                                        Gamedata.player = pickle.load(pickle_in)
                                        self.shipmenuloop()
                                        screen.blit(self.background, dest=(0, 0))
                            button.update()
                elif event.type == pygame.MOUSEMOTION:
                    for button in self.menu:
                        button.update()
                    for button in self.submenu:
                        button.update()
            pygame.display.flip()



    def generate_submenu(self, selectedbutton):
        screen.blit(self.background, dest=(0, 0))
        for button in self.menu:
            if button != selectedbutton:
                button.selected = False
            button.update()
        if selectedbutton.selected == True:
            selectedbutton.selected = False
            self.submenu = []
            selectedbutton.update()
            Sounds.sounds.soundcancel.play()
        else:
            Sounds.sounds.soundclick.play()
            selectedbutton.selected = True
            selectedbutton.update()
            if selectedbutton.function == "Load Game":
                filelist = Tools.get_savegames()
                self.loadgame(filelist)


    def loadgame(self, filelist):
        Sounds.sounds.soundclick.play()
        pygame.draw.rect(screen, Colors.darkgray, pygame.Rect(windowwidth / 2 - 300, windowheight / 2 - 30 * (len(filelist)+1) - 20, 600, 60 * (len(filelist)+1) + 30))
        self.submenu = []

        filenr = 0
        for file in filelist:
            rect = pygame.Rect(windowwidth / 2 - 275, windowheight / 2 - 30 * (len(filelist)+1) + 60 * filenr, 550, 50)
            path = os.path.join(game_folder, "savegames", str(file[0] + file[1]))
            date = datetime.datetime.fromtimestamp(os.path.getmtime(path)).strftime('%d-%m-%Y %H:%M:%S')
            text = file[0] + " - (" + str(date) + ")"
            self.submenu.append(Button.Selectable(rect, text, file))
            filenr += 1
        rect = pygame.Rect(windowwidth / 2 - 275, windowheight / 2 + 30 * len(filelist)-30, 550, 50)
        self.submenu.append(Button.Button(rect, "Load Game", "Load"))

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
        abortrect = pygame.Rect(30, 30, 400, 50)
        saverect = pygame.Rect(30, 90, 400, 50)
        rotaterect = pygame.Rect(1335, 910,180,50)

        self.activenames = [GameplayConstants.shippartslist[self.menunumber][x][0] for x in range(len(GameplayConstants.shippartslist[self.menunumber]))]
        self.activerects = [pygame.Rect(920, 553 + x * 60, 400, 50) for x in range(7)]
        self.buttons2names = ["Launch", "Quit", "Save game", "Rotate", "Back"]
        self.buttons2 = [launchrect, abortrect, saverect, rotaterect, backrect]
        self.buttons2active = [1,1,1,0,0]


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
                        #image = GameplayConstants.shippartimages[self.menunumber - 1][self.shippartdisplayed]
                        mouserect.center = (mousepos[0], mousepos[1])
                        self.resetscreen()
                        Tools.displayshippart(mouseimage, 1427, 730, self.shippartshape)
                        screen.blit(mouseimage, mouserect)
                    else:
                        # kleuren van de knoppen bij het er overheen hoveren.
                        for x in range(len(self.activenames)):
                            Tools.refresh_menubutton(self.activerects[x], mousepos,GameplayConstants.shippartslist[self.menunumber][x][0], False)
                        for x in range(len(self.buttons2)):
                            if self.buttons2active[x] == 1:
                                Tools.refresh_menubutton(self.buttons2[x], mousepos, self.buttons2names[x], False)
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
                            Tools.displayshippart(mouseimage, 1427, 730, self.shippartshape)
                        else:  # verwijder een schipdeel in het schip met de rechter muisknop
                            x = int((mousepos[0] - 69) / 60)
                            y = int((mousepos[1] - 529) / 60)
                            if x >= 0 and x <= 9 and y >= 0 and y <= 8:
                                if not isinstance(Gamedata.player.shipfill[y][x], int):
                                    Sounds.sounds.soundremove.play()
                                    Gamedata.player.removepart(Gamedata.player.shipfill[y][x])
                                    self.shipoverview()
                    if mouse[0]:  # linkermuisknop
                        if self.shippartselected == True:  # onderstaande is voor als de cursor is vervangen door een schiponderdeel
                            self.placeshippart(mousepos, mouseimage)
                        else:
                            x = int((mousepos[0] - 69) / 60)
                            y = int((mousepos[1] - 529) / 60)
                            if x >= 0 and x < 9 and y >= 0 and y < 8:
                                if not isinstance(Gamedata.player.shipfill[y][x], int):
                                    Sounds.sounds.soundclick.play()
                                    Gamedata.player.shipfill[y][x].itemmenu()
                                    #self.shippartselected = False
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
                                        self.buttons2active[4] = 1
                                    else:  # op een van de onderdelen van het submenu
                                        self.rotations = 0
                                        self.shippartdisplayed = button
                                        self.shippartshape = GameplayConstants.shippartslist[self.menunumber][self.shippartdisplayed][2]
                                        mouseimage = GameplayConstants.shippartimages[self.menunumber - 1][self.shippartdisplayed]
                                        Tools.displayshippart(mouseimage, 1427, 730, self.shippartshape)
                                        if self.menunumber >= 3:
                                            Tools.refresh_menubutton(rotaterect, mousepos, "Rotate", True)  # Rotate knop
                                            self.buttons2active[3] = 1
                                        pygame.draw.rect(screen, Colors.lightgray, pygame.Rect(1515, 550, 320, 260))
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
                                succes = Gameloop.Gameloop(Gamedata.player.levelnumber)
                                if succes:
                                    filepath = os.path.join(game_folder, 'savegames', 'auto_save.pickle')
                                    pickle_out = open(filepath, "wb")
                                    pickle.dump(Gamedata.player, pickle_out)
                                self.resetscreen()
                            # op de backknop (alleen in submenu)
                            elif backrect.collidepoint(mousepos) and self.menunumber != 0:
                                Sounds.sounds.soundcancel.play()
                                self.menunumber = 0
                                self.shippartselected = -1
                                self.activenames = [GameplayConstants.shippartslist[self.menunumber][x][0] for x in range(len(GameplayConstants.shippartslist[self.menunumber]))]
                                self.buttons2active[3] = 0
                                self.buttons2active[4] = 0
                                self.create_menu()
                            # op savegame
                            elif saverect.collidepoint(mousepos):
                                self.savegameloop()
                                self.resetscreen()
                            # op de rotateknop (alleen bij bepaalde items)
                            elif rotaterect.collidepoint(mousepos) and self.menunumber >= 3:
                                self.shippartshape = self.rotateshippart(self.shippartshape)
                                mouseimage = pygame.transform.rotate(GameplayConstants.shippartimages[self.menunumber - 1][self.shippartdisplayed], -self.rotations * 90)
                                #self.resetscreen()
                                Tools.displayshippart(mouseimage, 1427, 730, self.shippartshape)
                            # op het displayed onderdeel
                            elif self.shippartrect.collidepoint(mousepos) and self.shippartdisplayed >= 0:
                                if Gamedata.player.gold >= GameplayConstants.shippartprice(self.menunumber, self.shippartdisplayed, 0):
                                    Sounds.sounds.soundclick.play()
                                    mouseimage = pygame.transform.rotate(GameplayConstants.shippartimages[self.menunumber - 1][self.shippartdisplayed], -self.rotations*90)
                                    mouserect = mouseimage.get_rect()
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

    def rotateshippart(self, shippart):
        newobject = []
        height = len(shippart)
        width = len(shippart[0])
        for x in range(width):
            list = []
            for y in range(height):
                list.append(shippart[height - (y+1)][x])
            newobject.append(list)
        self.rotations = (self.rotations+1)%4
        return newobject

    def savegameloop(self):
        saves = Tools.get_savegames()
        for x in range(len(saves), 10):
            saves.append(("EMPTY SLOT", 0))
        saves.append("Save game")
        self.generate_submenu(11, 3, saves)
        running = True
        while running:
            for event in pygame.event.get():
                mousepos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif   event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        Sounds.sounds.soundcancel.play()
                        return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pressed()
                    if mouse[0]:
                        succes = False
                        count = 0
                        for rectnr in range(len(self.submenubuttonrects)-1):
                            if self.submenubuttonrects[rectnr].collidepoint(mousepos):
                                self.selection = saves[rectnr]
                                self.generate_submenu(11, 3, saves, rectnr)
                                self.selectnr = rectnr
                                succes = True
                            count += 1
                        if self.submenubuttonrects[10].collidepoint(mousepos):
                            filepath = os.path.join(game_folder, 'savegames', str(self.selectnr) + '.pickle')
                            pickle_out = open(filepath, "wb")
                            pickle.dump(Gamedata.player, pickle_out)
                            Sounds.sounds.soundimplement.play()
                            return
                        if not succes:
                            Sounds.sounds.soundcancel.play()
                            return
                elif event.type == pygame.MOUSEMOTION:
                    Tools.refresh_menubutton(self.submenubuttonrects[10], mousepos, "Save game", True)
            clock.tick(GameplayConstants.fps)
            pygame.display.flip()


    def placeshippart(self, mousepos, mouseimage):
        x = int((mousepos[0] - 69) / 60)
        y = int((mousepos[1] - 529) / 60)
        partlayout = self.shippartshape
        #partlayout = GameplayConstants.shippartslist[self.menunumber][self.shippartdisplayed][2]
        height = len(partlayout)
        width = len(partlayout[0])
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
                elif self.greenlist[yadjusted + stepdown][xadjusted] != 1:
                    succes = False

            if succes == True:  # het onderdeel wordt geplaatst op een mogelijke plek.
                if self.menunumber == 1:
                    item = Player.Weapon(self.shippartdisplayed, xadjusted, yadjusted, self.shippartshape)
                    Gamedata.player.weapons.append(item)
                else:
                    item = Player.Shippart(xadjusted, yadjusted, self.menunumber,self.shippartdisplayed, self.shippartshape, self.rotations) # itemobject
                    Gamedata.player.shipparts.append(item)
                item.increasestats()  # geef hero de statsboost van het geplaatste item
                for stepdown in range(height):
                    if width > 1:
                        for step in range(width):
                            if partlayout[stepdown][step] == 1:
                                Gamedata.player.shipfill[yadjusted + stepdown][xadjusted + step] = item
                    else:
                        Gamedata.player.shipfill[yadjusted + stepdown][xadjusted] = item

                screen.blit(mouseimage, (70 + 60 * xadjusted, 530 + 60 * yadjusted))
                Gamedata.player.shippartsused.append(item)
                pygame.mouse.set_visible(True)
                self.shippartselected = False
                self.shipoverview()
                Sounds.sounds.soundimplement.play()

    def resetscreen(self):
        screen.blit(self.hangarpic, dest=(0, 0))
        pygame.draw.rect(screen, Colors.black, self.shippartmenurect)
        self.create_menu()
        self.shipoverview()
        if self.menunumber > 0 and self.shippartdisplayed >= 0:
            pygame.draw.rect(screen, Colors.lightgray, pygame.Rect(1515, 550, 320, 260))
            text = GameplayConstants.shippartinfo(self.menunumber, self.shippartdisplayed, 0)
            for line in range(len(text)):
                Tools.draw_text(screen, text[line], 15, 1525, 563 + 20 * line, "Xolonium")

    def shipinfo(self):
        weaponuse = 0
        for weapon in Gamedata.player.weapons:
            weaponuse += weapon.energyuse * (weapon.upgrades + 1) / weapon.cooldown * 60
        maxuse = round(Gamedata.player.energyuse + Gamedata.player.maxshield + weaponuse)

        text = GameplayConstants.heroshipinfo(maxuse)
        for line in range(len(text)):
            Tools.draw_text(screen, text[line], 15, 650, 545 + 20 * line, "Xolonium")

        if Gamedata.player.energyuse == maxuse and Gamedata.player.energyregen >= Gamedata.player.energyuse:
            energybalance = 1
        elif Gamedata.player.energyuse == maxuse and Gamedata.player.energyregen <= Gamedata.player.energyuse:
            energybalance = 0
        else:
            energybalance = max(0, min(1, (Gamedata.player.energyregen - Gamedata.player.energyuse) / (maxuse - Gamedata.player.energyuse)))
        pygame.draw.rect(screen, Colors.black,pygame.Rect(604, 572 + (432 * (1 - energybalance)), 40, 6))  # indicator op energymeter

    def shipoverview(self):
        goldrect = pygame.Rect(1490, 30, 400, 50)
        gold = Gamedata.player.gold
        pygame.draw.rect(screen, Colors.lightgray, goldrect)
        Tools.draw_text(screen, "Gold: " + str(gold), 35, 1495, 55, "Xolonium")

        background = pygame.Rect(70, 530, 537, 477)
        pygame.draw.rect(screen, Colors.blackgray, background)
        screen.blit(self.shipimage, dest=(195, 590))
        screen.blit(self.energymeter, dest=(607, 530))

        textrect = pygame.Rect(640, 530, 240, 477)
        pygame.draw.rect(screen, Colors.lightgray, textrect)
        self.shipinfo()

        s2 = pygame.Surface((60, 60))
        s2.set_alpha(50)
        s2.fill(Colors.darkgreen)
        self.greenlist = [[0 for x in range(9)] for y in range(8)]

        # display geplaatste scheepsonderdelen
        for shippart in Gamedata.player.shippartsused:
            image = pygame.transform.rotate(GameplayConstants.shippartimages[shippart.type-1][shippart.index], -shippart.rotations * 90)
            rect = image.get_rect()
            rect.top = 530 + int(shippart.ypos) * 60
            rect.left = 70 + int(shippart.xpos) * 60
            screen.blit(image, rect)

        if self.shippartselected == False:
            for x in range(9):
                for y in range(8):
                    if isinstance(Gamedata.player.shipfill[y][x], int):
                        if Gamedata.player.shipfill[y][x] > 0 and Gamedata.player.shipfill[y][x] <= 1:
                            pygame.draw.rect(screen, Colors.lightgray, pygame.Rect(70 + x * 60, 530 + y * 60, 57, 57), 2)
        else:  # onderstaande is het inventariseren waar op het schip het geselecteerde object kan worden geplaatst.
            partlayout = self.shippartshape
            height = len(partlayout)
            width = len(partlayout[0])
            for x in range(9 - (width - 1)):
                for y in range(8 - (height - 1)):
                    succes = True
                    for step in range(height):
                        if width > 1:
                            for stepdown in range(width):
                                if Gamedata.player.shipfill[y + step][x + stepdown] != 1 and partlayout[step][stepdown] == 1:
                                    succes = False
                        elif Gamedata.player.shipfill[y + step][x] != 1:
                            succes = False
                    if succes == True:
                        for stepdown in range(height):
                            if width > 1:
                                for step in range(width):
                                    if partlayout[stepdown][step] == 1 and self.greenlist[y + stepdown][x + step] == 0:
                                        self.greenlist[y + stepdown][x + step] = 1
                                        screen.blit(s2, (70 + (x + step) * 60, 530 + (y + stepdown) * 60))
                                        pygame.draw.rect(screen, Colors.darkgreen,pygame.Rect(70 + (x + step) * 60, 530 + (y + stepdown) * 60,57, 57), 2)
                            elif self.greenlist[y + stepdown][x] == 0:
                                self.greenlist[y + stepdown][x] = 1
                                screen.blit(s2, (70 + x * 60, 530 + (y + stepdown) * 60))
                                pygame.draw.rect(screen, Colors.darkgreen, pygame.Rect(70 + x * 60, 530 + (y + stepdown) * 60, 57, 57), 2)
            for x in range(9):
                for y in range(8):
                    if self.greenlist[y][x] == 0 and Gamedata.player.shipfill[y][x] == 1:
                        pygame.draw.rect(screen, Colors.darkred, pygame.Rect(70 + x * 60, 530 + y * 60, 57, 57), 2)

    def create_menu(self):
        basex = 900
        pygame.draw.rect(screen, Colors.blackgray, pygame.Rect(basex, 530, 950, 477))
        mousepos = pygame.mouse.get_pos()
        for x in range(len(self.activenames)):
            pygame.draw.rect(screen, Colors.black, pygame.Rect(basex + 17, 550 + x * 60, 406, 56))
            Tools.refresh_menubutton(self.activerects[x], mousepos, self.activenames[x], True)
        for button in range(len(self.buttons2)):
            if self.buttons2active[button] == 1:
                Tools.refresh_menubutton(self.buttons2[button], mousepos, self.buttons2names[button], True)
        self.shippartrect = pygame.Rect(basex + 435, 550, 180, 360)
        pygame.draw.rect(screen, Colors.black, self.shippartrect)

game = Game()
game.menuloop()
pygame.quit()
