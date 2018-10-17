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
import Schipmenu
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
                                        shipmenu.shipmenuloop()
                                        self.screenupdate()
                                    else:
                                        Sounds.sounds.soundfail.play()
                                elif button.function == "New Game":
                                    Sounds.sounds.soundclick.play()
                                    Gamedata.player = Player.Player()
                                    shipmenu.shipmenuloop()
                                    self.screenupdate()
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
                                        shipmenu.shipmenuloop()
                                        self.screenupdate()
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
        pygame.draw.rect(screen, Colors.darkgray, pygame.Rect(windowwidth / 2 - 300, windowheight / 2 - 30 * (len(filelist)+1) - 20, 600, 60 * (len(filelist)+1) + 40))
        self.submenu = []

        filenr = 0
        for file in filelist:
            rect = pygame.Rect(windowwidth / 2 - 275, windowheight / 2 - 30 * (len(filelist)+1) + 60 * filenr, 550, 50)
            path = os.path.join(game_folder, "savegames", str(file[0] + file[1]))
            date = datetime.datetime.fromtimestamp(os.path.getmtime(path)).strftime('%d-%m-%Y %H:%M:%S')
            text = file[0] + " - (" + str(date) + ")"
            self.submenu.append(Button.Selectable(rect, text, file))
            filenr += 1
        rect = pygame.Rect(windowwidth / 2 - 275, windowheight / 2 + 30 * len(filelist)-20, 550, 50)
        self.submenu.append(Button.Button(rect, "Load Game", "Load"))

    def screenupdate(self):
        screen.blit(self.background, dest=(0, 0))
        for button in self.menu:
            button.update()
        for button in self.submenu:
            button.update()

shipmenu = Schipmenu.Schipmenu()
game = Game()
game.menuloop()
pygame.quit()