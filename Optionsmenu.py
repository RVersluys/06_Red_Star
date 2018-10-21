import pygame

import Button
import GameplayConstants
import Sounds

windowwidth = GameplayConstants.windowwidth
windowheight = GameplayConstants.windowheight

class Optionmenu:
    def __init__(self, pos):
        speed = (GameplayConstants.fps - 30) / 5
        self.buttons = [Button.Dragbar(pygame.Rect(pos[0], pos[1], 550, 80), "Game speed", 6, speed, False),
                      Button.Dragbar(pygame.Rect(pos[0], pos[1]+90, 550, 80), "Music volume", 100, GameplayConstants.musicvolume, False),
                      Button.Dragbar(pygame.Rect(pos[0], pos[1]+180, 550, 80), "Effects volume", 100, GameplayConstants.effectsvolume, False)]
        self.drag = False
        self.pos = pos
        self.displayed = False

    def display(self):
        for button in self.buttons:
            button.active = True
            button.update()
        self.displayed = True

    def hide(self):
        for button in self.buttons:
            button.active = False
        self.displayed = False

    def update(self):
        for button in self.buttons:
            button.update()

    def click(self, mousepos):
        for button in self.buttons:
            if button.active and button.rect.collidepoint(mousepos):
                if button.function == "Game speed":
                    x = int((mousepos[0] - button.rect.left) / (button.rect.width / 7))
                    GameplayConstants.fps = 30 + x * 5
                    button.chosenoption = x
                    Sounds.sounds.soundclick.play()
                    self.choice = 0
                    button.update()
                    self.drag = True
                elif button.function == "Music volume":
                    x = int((mousepos[0] - button.rect.left) / (button.rect.width / 101))
                    GameplayConstants.musicvolume = x
                    button.chosenoption = x
                    Sounds.sounds.soundclick.play()
                    pygame.mixer.music.set_volume(GameplayConstants.musicvolume / 100)
                    self.choice = 1
                    button.update()
                    self.drag = True
                elif button.function == "Effects volume":
                    x = int((mousepos[0] - button.rect.left) / (button.rect.width / 101))
                    GameplayConstants.effectsvolume = x
                    button.chosenoption = x
                    Sounds.sounds.soundchange()
                    Sounds.sounds.soundclick.play()
                    self.choice = 2
                    button.update()
                    self.drag = True
        return False

    def draghandling(self, mousepos):
        if self.choice == 0:
            x = max(0, min(6, int((mousepos[0] - self.buttons[0].rect.left) / (self.buttons[0].rect.width / 7))))
            GameplayConstants.fps = 30 + x * 5
            self.buttons[0].chosenoption = x
        elif self.choice == 1:
            x = max(0, min(100, int((mousepos[0] - self.buttons[1].rect.left) / (self.buttons[1].rect.width / 101))))
            GameplayConstants.musicvolume = x
            pygame.mixer.music.set_volume(GameplayConstants.musicvolume / 100)
            self.buttons[1].chosenoption = x
        elif self.choice == 2:
            x = max(0, min(100, int((mousepos[0] - self.buttons[2].rect.left) / (self.buttons[2].rect.width / 101))))
            GameplayConstants.effectsvolume = x
            Sounds.sounds.soundchange()
            self.buttons[2].chosenoption = x