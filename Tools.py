import pygame
import GameplayConstants
import math
import os
import datetime

import Colors
import Button

def draw_text(surface, text, size, x, y, font_name, color = Colors.black, bold = True):
    font = pygame.font.Font(pygame.font.match_font(font_name, bold = bold), size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midleft = (x, y)
    surface.blit(text_surface, text_rect)

def get_savegames():
    count = 0
    filepath = os.path.join(os.path.dirname(__file__), 'savegames')
    allfiles = os.listdir(filepath)
    filelist = []
    for file in allfiles:
        filetuple = os.path.splitext(file)
        if filetuple[0] != 'auto_save' and filetuple[1] == '.pickle':
            filelist.append(filetuple)
            count += 1
        if count == 10:
            break
    return filelist

def loadgame():
    filelist = get_savegames()
    pygame.draw.rect(GameplayConstants.screen, Colors.darkgray, pygame.Rect(GameplayConstants.windowwidth / 2 - 300, GameplayConstants.windowheight / 2 - 30 * (len(filelist)+1) - 20, 600, 60 * (len(filelist)+1) + 40))
    submenu = []
    filenr = 0
    for file in filelist:
        rect = pygame.Rect(GameplayConstants.windowwidth / 2 - 275, GameplayConstants.windowheight / 2 - 30 * (len(filelist)+1) + 60 * filenr, 550, 50)
        path = os.path.join(GameplayConstants.game_folder, "savegames", str(file[0] + file[1]))
        date = datetime.datetime.fromtimestamp(os.path.getmtime(path)).strftime('%d-%m-%Y %H:%M:%S')
        text = file[0] + " - (" + str(date) + ")"
        submenu.append(Button.Selectable(rect, text, file))
        filenr += 1
    rect = pygame.Rect(GameplayConstants.windowwidth / 2 - 275, GameplayConstants.windowheight / 2 + 30 * len(filelist)-20, 550, 50)
    submenu.append(Button.Button(rect, "Load Game", "Load"))
    return submenu

def displayshippart(image, posx, posy, shippartshape = False):
    background = pygame.Rect(posx - 90, posy - 180, 180, 360)
    rect = image.get_rect()
    rect.center = (posx, posy)
    pygame.draw.rect(GameplayConstants.screen, Colors.black, background)
    GameplayConstants.screen.blit(image, rect)
    if shippartshape:
        for height in range(len(shippartshape)):
            if isinstance(shippartshape[height], list):
                for width in range(len(shippartshape[height])):
                    if shippartshape[height][width] == 1:
                        pygame.draw.rect(GameplayConstants.screen, Colors.lightgray, pygame.Rect(rect.left + 60 * width, rect.top + 60 * height, 57, 57), 2)
            elif shippartshape[height] == 1:
                pygame.draw.rect(GameplayConstants.screen, Colors.lightgray, pygame.Rect(rect.left, rect.top + 60 * height, 57, 57), 2)

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