import pygame

import Colors
import GameplayConstants
import Tools

class Button:
    def __init__(self, rect, text, function, active = True):
        self.rect = rect
        self.text = text
        self.function = function
        self.active = active
        self.selected = False
        if active:

            self.strokerect = (rect.left - 3, rect.top - 3, rect.width + 6, rect.height + 6)
            pygame.draw.rect(GameplayConstants.screen, Colors.black, self.strokerect)
            mousepos = pygame.mouse.get_pos()
            if rect.collidepoint(mousepos):
                color = Colors.bluegray
            else:
                color = Colors.lightgray
            pygame.draw.rect(GameplayConstants.screen, color, rect)
            Tools.draw_text(GameplayConstants.screen, text, 25, rect.left + 5, rect.centery, "Xolonium")

    def update(self):
        if self.active:
            pygame.draw.rect(GameplayConstants.screen, Colors.black, self.strokerect)
            mousepos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mousepos):
                color = Colors.bluegray
            else:
                color = Colors.lightgray
            pygame.draw.rect(GameplayConstants.screen, color, self.rect)
            Tools.draw_text(GameplayConstants.screen, self.text, 25, self.rect.left + 5, self.rect.centery, "Xolonium")


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
