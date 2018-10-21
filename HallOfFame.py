import pygame
import GameplayConstants
import Button
import Colors

class HallOfFame:
    def __init__(self):
        self.highscores = []
        self.scorelist = [("Scuti", 2500000),
                          ("Canis Majoris", 2000000),
                          ("Betelgeuse", 1550000),
                          ("Antaris", 1250000),
                          ("Pistol", 440000),
                          ("Rigel", 90000),
                          ("Aldebaran", 64000),
                          ("Arcturus", 36000),
                          ("Polux", 12800),
                          ("Sirius", 2500)]

    def addscore(self, name, score):
        if score > self.scorelist[9][1]:
            self.scorelist.append((name,score))
            self.scorelist.sort(key=lambda x: int(x[1]), reverse=True)
            self.scorelist.pop(10)

    def display(self):
        pygame.draw.rect(GameplayConstants.screen, Colors.darkgray, pygame.Rect(GameplayConstants.windowwidth / 2 - 300, GameplayConstants.windowheight / 2 - 320, 600, 640))
        submenu = []
        scorenr = 0
        for score in self.scorelist:
            rect = pygame.Rect(GameplayConstants.windowwidth / 2 - 275, GameplayConstants.windowheight / 2 - 295 + 60 * scorenr, 550, 50)
            name = score[0]
            score = score[1]
            text = str(scorenr+1) + ". " + str(name) + ": " + str(score)
            submenu.append(Button.Selectable(rect, text, False))
            scorenr += 1