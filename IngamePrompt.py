import pygame
import os


import Button
import GameplayConstants
import Tools
import Colors
import Gamedata


game_folder = os.path.dirname(__file__)
clock = pygame.time.Clock()

class IngamePrompt:
    def __init__(self, background, options, text):
        self.background = pygame.image.load(os.path.join(game_folder, "img", background)).convert()
        self.options = [Button.Button(pygame.Rect(1220, 1000, 300, 50), options[0], True),
                        Button.Button(pygame.Rect(1550, 1000, 300, 50), options[1], False)]
        self.text = text

        GameplayConstants.screen.blit(self.background, dest=(0, 0))
        for button in self.options:
            button.update()

        height = 22 * len(text) + 25
        s2 = pygame.Surface((630, height))
        s2.set_alpha(180)
        s2.fill(Colors.blackgray)
        GameplayConstants.screen.blit(s2, (1220, 970 - height))

        for line in range(len(text)):
            Tools.draw_text(GameplayConstants.screen, text[line], 16, 1238, 995 - height + 22 * line, "Xolonium", Colors.white)

        pygame.display.flip()


        running = True
        while running:
            mousepos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEMOTION:
                    for button in self.options:
                        button.update()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pressed()
                    if mouse[0]:
                        for button in self.options:  # op een van de onderdelen van het hoofdmenu
                            if button.rect.collidepoint(mousepos):
                                Gamedata.Hero = button.function
                                return

            pygame.display.flip()
            clock.tick(GameplayConstants.fps)

