import pygame
import os
import pickle

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
import Optionsmenu
import HallOfFame

game_folder = os.path.dirname(__file__)
fps = GameplayConstants.fps


class Game:
    def __init__(self):
        # initialize music
        pygame.mixer.music.load(os.path.join(game_folder, 'sounds', 'music', 'Hymne.mp3'))
        pygame.mixer.music.set_volume(GameplayConstants.musicvolume/100)
        pygame.mixer.music.play(loops=-1)
        Gamedata.halloffame = HallOfFame.HallOfFame()

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
        self.optionmenu = Optionsmenu.Optionmenu((windowwidth / 2 - 275, windowheight / 2 - 130))
        self.choice = -1
        self.filepath = ""
        self.halloffameselected = False
        self.loadgameselected = False
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
                            if button.function == "Settings":
                                if button.rect.collidepoint(mousepos):
                                    if self.loadgameselected:
                                        self.submenu = []
                                        self.loadgameselected = False
                                    if self.optionmenu.displayed:
                                        self.screenupdate()
                                        Sounds.sounds.soundcancel.play()
                                    else:
                                        self.screenupdate()
                                        pygame.draw.rect(screen, Colors.darkgray, pygame.Rect(windowwidth / 2 - 300, windowheight / 2 - 155, 600, 310))
                                        self.optionmenu.display()
                                        Sounds.sounds.soundclick.play()
                            elif button.function == "Continue" and button.rect.collidepoint(mousepos):
                                filepath = os.path.join(game_folder, 'savegames', 'auto_save.pickle')
                                if os.path.isfile(filepath):
                                    Sounds.sounds.soundclick.play()
                                    pickle_in = open(filepath, "rb")
                                    Gamedata.player = pickle.load(pickle_in)
                                    shipmenu.shipmenuloop()
                                    self.screenupdate()
                                else:
                                    Sounds.sounds.soundfail.play()
                            elif button.function == "Hall of Fame":
                                if button.rect.collidepoint(mousepos):
                                    if self.optionmenu.displayed:
                                        self.optionmenu.hide()
                                    elif self.loadgameselected:
                                        self.submenu = []
                                        self.loadgameselected = False
                                    if self.halloffameselected:
                                        self.screenupdate()
                                        self.halloffameselected = False
                                        Sounds.sounds.soundcancel.play()
                                    else:
                                        self.screenupdate()
                                        self.halloffameselected = True
                                        filepath = os.path.join(game_folder, 'savegames', 'HOF.pickle')
                                        Sounds.sounds.soundclick.play()
                                        if os.path.isfile(filepath):
                                            pickle_in = open(filepath, "rb")
                                            Gamedata.halloffame = pickle.load(pickle_in)
                                        else:
                                            Gamedata.halloffame.display()
                                elif self.halloffameselected:
                                    self.halloffameselected = False
                            elif button.function == "New Game" and button.rect.collidepoint(mousepos):
                                Sounds.sounds.soundclick.play()
                                filepath = os.path.join(game_folder, 'gamefiles', 'new_game.pickle')
                                if os.path.isfile(filepath):
                                    pickle_in = open(filepath, "rb")
                                    Gamedata.player = pickle.load(pickle_in)
                                else:
                                    Gamedata.player = Player.Player()
                                shipmenu.shipmenuloop()
                                self.screenupdate()
                            elif button.function == "Load Game":
                                if button.rect.collidepoint(mousepos):
                                    if self.optionmenu.displayed:
                                        self.optionmenu.hide()
                                    if self.loadgameselected:
                                        self.screenupdate()
                                        Sounds.sounds.soundcancel.play()
                                        self.loadgameselected = False
                                    else:
                                        self.screenupdate()
                                        Sounds.sounds.soundclick.play()
                                        self.loadgameselected = True
                                        self.submenu = Tools.loadgame()
                            elif button.function == "Quit" and button.rect.collidepoint(mousepos):
                                pygame.quit()
                        if self.optionmenu.displayed:
                            self.optionmenu.click(mousepos)
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
                                button.update()
                            else:
                                if button.function == "Load" and button.rect.collidepoint(mousepos):
                                    if self.filepath != "":
                                        pickle_in = open(self.filepath, "rb")
                                        Gamedata.player = pickle.load(pickle_in)
                                        shipmenu.shipmenuloop()
                                        self.screenupdate()

                elif event.type == pygame.MOUSEMOTION:
                    for button in self.menu:
                        button.update()
                    for button in self.submenu:
                        button.update()
                    if self.optionmenu.drag:
                        self.optionmenu.draghandling(mousepos)
                        self.optionmenu.update()
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.optionmenu.drag = False
            pygame.display.flip()

    def screenupdate(self):
        self.optionmenu.hide()
        self.submenu = []
        screen.blit(self.background, dest=(0, 0))
        for button in self.menu:
            button.update()
        for button in self.submenu:
            button.update()

shipmenu = Schipmenu.Schipmenu()
game = Game()
game.menuloop()
pygame.quit()