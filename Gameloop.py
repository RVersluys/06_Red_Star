import pygame
import os

windowwidth = 1920
windowheight = 1080
warscreenwidth = 1440
interfacewidth = 480
warrect = pygame.Rect(0, 0, 1440, 1080)
sidebarrect = pygame.Rect(1440, 0, 480, 1080)

clock = pygame.time.Clock()

import GameplayConstants
import Tools
import Gamedata
import Level
import Sounds
import Hero
import Gametext
import Colors
import Button
import Optionsmenu

screen = GameplayConstants.screen

"""Hier staat de loop waarin elk level wordt uitgevoerd. De mobs en overige zaken die tevoorschijn komen staan in een lijst in 'Level'."""

class Gameloop:
    def __init__(self):
        # levelinit
        self.level = Level.Level()
        Gamedata.hero = Hero.Hero()
        Gamedata.all_sprites.add(Gamedata.hero)
        pygame.mouse.set_visible(False)
        # maak sidebar
        self.scorerect = pygame.Rect(1610, 38, 280, 40)
        self.barrects = []
        for x in range(3):
            self.barrects.append(pygame.Rect(1474, 820 + x * 80, 413, 40))
        # pygame.display.update()
        running = True
        endlevelbool = False
        self.missilepic = pygame.transform.rotate(pygame.image.load(os.path.join(os.path.dirname(__file__), 'img', 'projectiles', 'rocket.png')).convert_alpha(),270)

        while running:
            # Eventcheck
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                # mousemovement and click
                elif event.type == pygame.MOUSEMOTION:
                    Gamedata.hero.movement(event)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.gamemenu()
                elif event.type == pygame.MOUSEBUTTONUP:
                    for button in range(3):
                        for weapon in Gamedata.player.weapons:
                            if weapon.keybind == button and weapon.index == 4:
                                weapon.plasmashot()

            # hero projectiles
            mouse = pygame.mouse.get_pressed()
            for button in range(3):
                if mouse[button]:
                    for weapon in Gamedata.player.weapons:
                        if weapon.keybind == button:
                            weapon.fireevent()
            # Spawn enemies
            self.level.spawning()
            # Update
            Gamedata.stars.update()
            Gamedata.background.update()
            Gamedata.all_sprites.update()
            # Collisioncheck
            hits = pygame.sprite.groupcollide(Gamedata.mobs, Gamedata.herobullets, False, False)
            for mob in hits:  # collision herobullets - mobs
                for bullet in hits[mob]:
                    Gamedata.player.score += bullet.hit(mob)
            if Gamedata.hero.alive == True:
                hits = pygame.sprite.spritecollide(Gamedata.hero, Gamedata.mobbullets, False, pygame.sprite.collide_circle)
                for bullet in hits:  # collision player - mobbullets
                    if Gamedata.hero.getdamage(bullet.damage, bullet):
                        self.level.succes = False
                        self.level.abort = True
                    bullet.hit()
                hits = pygame.sprite.spritecollide(Gamedata.hero, Gamedata.mobs, False, pygame.sprite.collide_circle)
                for mob in hits:  # collision player - mobs
                    if Gamedata.hero.getdamage(4, mob):
                        self.level.succes = False
                        self.level.abort = True

                    Gamedata.player.score += mob.getdamage(4)

                hits = pygame.sprite.spritecollide(Gamedata.hero, Gamedata.powerups, True, pygame.sprite.collide_circle)
                for powerup in hits:  # collision player powerups
                    Gamedata.player.gold += powerup.collect()
                    Sounds.sounds.pickupsound.play()
            # check end level
            if self.level.end and len(Gamedata.mobs) == 0 and len(Gamedata.powerups) == 0 or self.level.abort:
                if endlevelbool == False:
                    endlevelbool = True
                    endleveltime = pygame.time.get_ticks()  # starter tick

                    # If no 5 Iridium is collected, level 2 failed
                    if Gamedata.player.uridium241 < 5 and Gamedata.player.levelnumber == 1:
                        self.level.succes = False

                    if self.level.succes:
                        text = Gametext.Text("Mission Accomplished", 35, (100,255,100), (120,30), (warscreenwidth/2, windowheight/2), (800,100))
                    else:
                        text = Gametext.Text("Mission Failed", 35, (200, 0, 0), (120,30), (warscreenwidth/2, windowheight/2), (800, 100))
                    Gamedata.background.add(text)
                if pygame.time.get_ticks() > endleveltime + 2500:
                    self.endlevel(self.level.succes)
                    return
            # Draw / render
            pygame.draw.rect(screen, Colors.black, warrect)
            Gamedata.stars.draw(screen)
            Gamedata.background.draw(screen)
            Gamedata.all_sprites.draw(screen)
            self.sidebar()
            # keep loop running at the right speed
            clock.tick(GameplayConstants.fps)
            pygame.display.flip()


    def sidebar(self):
        pygame.draw.rect(screen, Colors.darkgray, sidebarrect)
        pygame.draw.rect(screen, Colors.black, pygame.Rect(1455, 30, 450, 60))
        pygame.draw.rect(screen, Colors.lightgray, pygame.Rect(1458, 33, 444, 54))
        pygame.draw.rect(screen, Colors.black, pygame.Rect(1455, 120, 450, 60))
        pygame.draw.rect(screen, Colors.lightgray, pygame.Rect(1458, 123, 444, 54))
        Tools.draw_text(screen, "Score:", 38, 1475, 60, "Xolonium")
        Tools.draw_text(screen, "Gold:", 38, 1475, 150, "Xolonium")

        if Gamedata.player.levelnumber == 1:
            pygame.draw.rect(screen, Colors.black, pygame.Rect(1455, 210, 450, 60))
            pygame.draw.rect(screen, Colors.lightgray, pygame.Rect(1458, 213, 444, 54))
            Tools.draw_text(screen, "Uridium 241:", 38, 1475, 240, "Xolonium")
            Tools.draw_text(screen, str(Gamedata.player.uridium241) + " of 5", 38, 1760, 240, "Xolonium")

        Tools.draw_text(screen, "Energy", 35, 1482, 803, "Xolonium")
        Tools.draw_text(screen, "Shield", 35, 1482, 883, "Xolonium")
        Tools.draw_text(screen, "Armor", 35, 1482, 963, "Xolonium")

        # statusbars
        fills = []
        fills.append(pygame.Rect(self.barrects[0].left + 3, self.barrects[0].top + 3,Gamedata.hero.energy / Gamedata.player.maxenergy * 413, 36))
        if Gamedata.player.maxshield:
            fills.append(pygame.Rect(self.barrects[1].left + 3, self.barrects[1].top + 3,Gamedata.hero.shield / Gamedata.player.maxshield * 413, 36))
        else:
            fills.append(pygame.Rect(0, 0, 0, 0))
        fills.append(pygame.Rect(self.barrects[2].left + 3, self.barrects[2].top + 3,Gamedata.hero.armor / Gamedata.player.maxarmor * 413, 36))
        if Gamedata.player.missiles:
            ammo = 0
            for weapon in Gamedata.player.missiles:
                ammo += weapon.ammo
            pygame.draw.rect(screen, Colors.black, pygame.Rect(1455, 210, 450, 60))
            pygame.draw.rect(screen, Colors.lightgray, pygame.Rect(1458, 213, 444, 54))
            Tools.draw_text(screen, ": " + str(ammo), 35, 1580, 240, "Xolonium")
            screen.blit(self.missilepic, dest=(1472, 233))

        for barnr in range(3):
            pygame.draw.rect(screen, Colors.black, self.barrects[barnr])
            pygame.draw.rect(screen, Colors.colorbars[barnr], fills[barnr])
        # score
        pygame.draw.rect(screen, Colors.lightgray, self.scorerect)
        Tools.draw_text(screen, str(Gamedata.player.score), 38, 1610, 60, "Xolonium")
        Tools.draw_text(screen, str(Gamedata.player.gold), 38, 1610, 150, "Xolonium")


    def endlevel(self, levelsucces):
        if not levelsucces:
            Gamedata.player.gold = self.level.startgold
            Gamedata.player.score = self.level.startscore
            Gamedata.mobs.empty()
            Gamedata.powerups.empty()
        Gamedata.background.empty()
        Gamedata.herobullets.empty()
        Gamedata.mobbullets.empty()
        Gamedata.all_sprites.empty()
        pygame.mouse.set_visible(True)
        Sounds.playsong('Hymne.mp3', True)

    def gamemenu(self):
        pygame.mouse.set_visible(True)
        screenalpha = pygame.Surface((1920, 1080))
        screenalpha.set_alpha(150)
        screenalpha.fill(Colors.black)
        screen.blit(screenalpha, dest=(0, 0))
        pygame.draw.rect(screen, Colors.darkgray, pygame.Rect(windowwidth / 2 - 300, windowheight / 2 - 180, 600, 360))
        mainmenu = [Button.Button(pygame.Rect(windowwidth / 2 - 275, windowheight / 2 - 115, 550, 50),"Quit game", "Quit"),
                    Button.Button(pygame.Rect(windowwidth / 2 - 275, windowheight / 2 - 55, 550, 50), "Abort mission", "Abort"),
                    Button.Button(pygame.Rect(windowwidth / 2 - 275, windowheight / 2 + 5, 550, 50), "Settings", "Settings"),
                    Button.Button(pygame.Rect(windowwidth / 2 - 275, windowheight / 2 + 65, 550, 50), "Resume", "Resume")]
        optionmenu = Optionsmenu.Optionmenu((windowwidth / 2 - 275, windowheight / 2 - 160))
        returnbutton = Button.Button(pygame.Rect(windowwidth / 2 - 275, windowheight / 2 + 110, 550, 50), "Return", "Return", False)
        pygame.display.flip()

        while True:
            mousepos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pressed()
                    if mouse[0]:
                        if optionmenu.click(mousepos): #return true betekend afsluiten optiemenu
                            for button in mainmenu:
                                button.active = True
                                button.update()

                        for button in mainmenu:
                            if button.rect.collidepoint(mousepos) and button.active:
                                if button.function == "Quit":
                                    pygame.quit()
                                elif button.function == "Abort":
                                    self.level.abort = True
                                    Sounds.sounds.soundclick.play()
                                    return
                                elif button.function == "Settings":
                                    pygame.draw.rect(GameplayConstants.screen, Colors.darkgray, pygame.Rect(windowwidth/2-300, windowheight/2-180, 600, 360))
                                    optionmenu.display()
                                    returnbutton.active = True
                                    returnbutton.update()
                                    for button in mainmenu:
                                        button.active = False
                                    Sounds.sounds.soundclick.play()
                                elif button.function == "Resume":
                                    pygame.mouse.set_visible(False)
                                    Sounds.sounds.soundclick.play()
                                    return
                        if returnbutton.rect.collidepoint(mousepos) and returnbutton.active:
                            optionmenu.hide()
                            returnbutton.active = False
                            pygame.draw.rect(GameplayConstants.screen, Colors.darkgray, pygame.Rect(windowwidth / 2 - 300, windowheight / 2 - 180, 600, 360))
                            for button in mainmenu:
                                button.active = True
                                button.update()
                elif event.type == pygame.MOUSEMOTION:
                    if optionmenu.drag:
                        optionmenu.draghandling(mousepos)

                    for button in mainmenu:
                        button.update()
                    optionmenu.update()
                    returnbutton.update()

                elif event.type == pygame.MOUSEBUTTONUP:
                    optionmenu.drag = False
            pygame.display.flip()
            clock.tick(GameplayConstants.fps)
