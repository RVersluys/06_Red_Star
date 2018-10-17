import pygame
import os

import Colors
import GameplayConstants
import Tools



buttonactive = pygame.image.load(os.path.join(os.path.dirname(__file__), 'img', 'button_active.png')).convert()
buttonpassive = pygame.image.load(os.path.join(os.path.dirname(__file__), 'img', 'button_passive.png')).convert()


class Button:
    def __init__(self, rect, text, function, active = True):
        self.rect = rect
        self.text = text
        self.function = function
        self.active = active
        self.selected = False
        self.strokerect = (rect.left - 3, rect.top - 3, rect.width + 6, rect.height + 6)
        if active:
            pygame.draw.rect(GameplayConstants.screen, Colors.black, self.strokerect)
            mousepos = pygame.mouse.get_pos()
            if rect.collidepoint(mousepos):
                buttonpic = pygame.transform.scale(buttonactive, (rect.width, rect.height))
            else:
                buttonpic = pygame.transform.scale(buttonpassive, (rect.width, rect.height))
            GameplayConstants.screen.blit(buttonpic, dest=(rect.left, rect.top))
            Tools.draw_text(GameplayConstants.screen, text, 25, rect.left + 10, rect.centery, "Xolonium")

    def update(self):
        if self.active:
            pygame.draw.rect(GameplayConstants.screen, Colors.black, self.strokerect)
            mousepos = pygame.mouse.get_pos()

            if self.rect.collidepoint(mousepos):
                buttonpic = pygame.transform.scale(buttonactive, (self.rect.width, self.rect.height))
            else:
                buttonpic = pygame.transform.scale(buttonpassive, (self.rect.width, self.rect.height))
            GameplayConstants.screen.blit(buttonpic, dest=(self.rect.left, self.rect.top))
            Tools.draw_text(GameplayConstants.screen, self.text, 25, self.rect.left + 10, self.rect.centery, "Xolonium")


class Selectable(Button):
    def __init__(self, rect, text, file):
        self.rect = rect
        self.text = text
        self.file = file
        self.active = True
        self.selected = False
        self.strokerect = (rect.left - 3, rect.top - 3, rect.width + 6, rect.height + 6)
        pygame.draw.rect(GameplayConstants.screen, Colors.black, self.strokerect)
        pygame.draw.rect(GameplayConstants.screen, Colors.white, self.rect)
        Tools.draw_text(GameplayConstants.screen, text, 18, rect.left + 5, rect.centery, "Xolonium")

    def update(self):
        if self.selected:
            bgcolor = Colors.blackgray
            textcolor = Colors.white
        else:
            bgcolor = Colors.white
            textcolor = Colors.black
        pygame.draw.rect(GameplayConstants.screen, Colors.black, self.strokerect)
        pygame.draw.rect(GameplayConstants.screen, bgcolor, self.rect)
        Tools.draw_text(GameplayConstants.screen, self.text, 18, self.rect.left + 5, self.rect.centery, "Xolonium", textcolor)
