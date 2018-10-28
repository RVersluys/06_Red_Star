import pygame
import Colors
import Tools
import Gamedata
import GameplayConstants

class Missioninfo:
    def __init__(self, rect):
        self.level = Gamedata.player.levelnumber
        rect.height = 45+20*len(missioninfo[self.level])
        self.rect = rect
        self.outline = pygame.Rect(self.rect.x-5,self.rect.y-5,self.rect.width+10,self.rect.height+10)


    def update(self):
        pygame.draw.rect(GameplayConstants.screen, Colors.black, self.outline)
        pygame.draw.rect(GameplayConstants.screen, Colors.lightgray, self.rect)
        Tools.draw_text(GameplayConstants.screen, "Mission details", 25, self.rect.x + 190, self.rect.y + 15, "Xolonium")
        for line in range(len(missioninfo[self.level])):
            Tools.draw_text(GameplayConstants.screen, missioninfo[self.level][line], 17, self.rect.x + 5, self.rect.y + 45 + 20 * line, "Xolonium")




missioninfo = [["The interplanetary dream of Earth is quickly squashed when a",
               "fleet of the Scorch entered our solar system, destroying our",
                "colonies on Mars and the Jupiter moon Europa. But then a ",
               "mysterious allien race called Alfa came to intervene. If it wasn't",
               "for the timely intervention of the Alfa carriër Gantador, who",
               "knows what would remain of this little blue planet we call home...",
               "",
               "But we aren't save yet. After the departure of the Gantador, it",
               "appears that many Scorch ships remain in our solar system.",
               "The Alfa have left us with one specialised spaceship to defend",
               "ourselfes, and you, as the greatest spaceship ace of Earth",
               "are assigned to fend of the remaining Scorch forces."],
               ["Nothing comes free and interstellar affairs appear to be no",
                "exception. The Alfa have come to collect our dept, demanding",
                "that we retrieve rare minerals in a base of The Scorch and",
                "return it to a secret Alfa base. Because The Scorch sensors",
                "are not adapted to human ships we would be able to approach it",
                "with relative ease. Although this mission is to satisfy",
                "the demands of the Alfa, it seems to be time wel spent",
                "to give the aliens that destroyed our colonies on Mars and",
                "Europa a visit."]]