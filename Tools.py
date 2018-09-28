import pygame
import GameplayConstants
import math

black = (0, 0, 0)
lightgray = (150,150,150)

def draw_text(surface, text, size, x, y, font_name, color = GameplayConstants.black, bold = True):
    font = pygame.font.Font(pygame.font.match_font(font_name, bold = bold), size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midleft = (x, y)
    surface.blit(text_surface, text_rect)


def refresh_menubutton(rect, mousepos, text, stroke):
    if stroke == True:
        strokerect = (rect.left -3, rect.top -3, rect.width +6, rect.height +6)
        pygame.draw.rect(GameplayConstants.screen, black, strokerect)
    if rect.collidepoint(mousepos):
        color = (81, 103, 124)
    else:
        color = (150, 150, 150)
    pygame.draw.rect(GameplayConstants.screen, color, rect)

    draw_text(GameplayConstants.screen, text, 25, rect.left+5, rect.centery, "Xolonium")

def create_dragbar(rect, text, options, chosenoption):
    pygame.draw.rect(GameplayConstants.screen, lightgray,rect)
    draw_text(GameplayConstants.screen, text, 25, rect.left + 5, rect.top + 10, "Xolonium")
    dragrect = pygame.Rect(rect.left + 10, rect.top+20, rect.width -20,rect.height - 50)
    pygame.draw.rect(GameplayConstants.screen, black, dragrect)
    pygame.draw.circle(GameplayConstants.screen,lightgray,(int(rect.x+25+(rect.width-50)*chosenoption/options),int(rect.y + rect.height/2-5)),10,0)
    return dragrect


def displayshippart(list, shippartdisplayed, image, posx, posy):
    background = pygame.Rect(posx - 90, posy - 180, 180, 360)
    rect = image.get_rect()
    rect.center = (posx, posy)
    pygame.draw.rect(GameplayConstants.screen, black, background)
    GameplayConstants.screen.blit(image, rect)
    for height in range(len(GameplayConstants.shippartslist[list][shippartdisplayed][2])):
        if isinstance(GameplayConstants.shippartslist[list][shippartdisplayed][2][height], tuple):
            for width in range(len(GameplayConstants.shippartslist[list][shippartdisplayed][2][height])):
                if GameplayConstants.shippartslist[list][shippartdisplayed][2][height][width] == 1:
                    pygame.draw.rect(GameplayConstants.screen, lightgray, pygame.Rect(rect.left + 60 * width, rect.top + 60 * height, 57, 57), 2)
        elif GameplayConstants.shippartslist[list][shippartdisplayed][2][height] == 1:
            pygame.draw.rect(GameplayConstants.screen, lightgray, pygame.Rect(rect.left, rect.top + 60 * height, 57, 57), 2)

def getangle(rect1, rect2):
    distancex = rect1.centerx - rect2.centerx
    distancey = -(rect1.centery - rect2.centery)
    if distancex == 0:
        result = 90
    else:
        result = math.degrees(math.atan(distancey / distancex))
    if distancex < 0:
        result += 180
    result += 90
    return result

def getmovement(rect1, rect2, speed):
    distancex = -(rect1.centerx - rect2.centerx)
    distancey = rect1.centery - rect2.centery
    distance = (distancex ** 2 + distancey ** 2) ** .5
    move = []
    move.append(speed / distance * distancex)
    move.append(speed / distance * distancey)
    return move