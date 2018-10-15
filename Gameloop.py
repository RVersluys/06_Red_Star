import pygame

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

screen = GameplayConstants.screen

class Gameloop:
    def __init__(self, levelnumber):
        # levelinit
        self.level = Level.Level(levelnumber)
        #Sprites.hero.refuel()
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

        while running:
            # Eventcheck
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                # mousemovement and click
                elif event.type == pygame.MOUSEMOTION:
                    Gamedata.hero.movement(event)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.gamemenu()
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
                    #Gamedata.player.score += mob.getdamage(bullet.damage)
                    Gamedata.player.score += bullet.hit(mob)
            if Gamedata.hero.alive == True:
                hits = pygame.sprite.spritecollide(Gamedata.hero, Gamedata.mobbullets, False, pygame.sprite.collide_circle)
                for bullet in hits:  # collision player - mobbullets
                    if Gamedata.hero.getdamage(bullet.damage, bullet):
                        self.level.abort = True
                    bullet.hit()
                hits = pygame.sprite.spritecollide(Gamedata.hero, Gamedata.mobs, False, pygame.sprite.collide_circle)
                for mob in hits:  # collision player - mobs
                    if Gamedata.hero.getdamage(4, mob):
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

        Tools.draw_text(screen, "Energy", 35, 1482, 803, "Xolonium")
        Tools.draw_text(screen, "Shield", 35, 1482, 883, "Xolonium")
        Tools.draw_text(screen, "Armor", 35, 1482, 963, "Xolonium")

        # statusbars
        barfill = [Gamedata.hero.energy, Gamedata.hero.shield, Gamedata.hero.armor]
        startx = 1474
        starty = 820
        barheight = 40
        barwidth = 413
        spacing = 80
        fills = []
        fills.append(pygame.Rect(self.barrects[0].left + 3, self.barrects[0].top + 3,Gamedata.hero.energy / Gamedata.player.maxenergy * 413, 36))
        if Gamedata.player.maxshield:
            fills.append(pygame.Rect(self.barrects[1].left + 3, self.barrects[1].top + 3,Gamedata.hero.shield / Gamedata.player.maxshield * 413, 36))
        else:
            fills.append(pygame.Rect(0, 0, 0, 0))
        fills.append(pygame.Rect(self.barrects[2].left + 3, self.barrects[2].top + 3,Gamedata.hero.armor / Gamedata.player.maxarmor * 413, 36))
        for barnr in range(3):
            fill = pygame.Rect(startx + 3, starty + 3 + barnr * spacing, (barwidth - 6) / 100 * barfill[barnr], barheight - 6)
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


    def generate_menu(self, buttonlist):
        buttoncount = len(buttonlist)
        buttonrects = []
        pygame.draw.rect(screen, Colors.darkgray, pygame.Rect(windowwidth / 2 - 300, windowheight / 2 - 30 * buttoncount - 20, 600, 60 * buttoncount + 30))
        mousepos = pygame.mouse.get_pos()
        for button in range(buttoncount):
            if isinstance(buttonlist[button], tuple):
                dragrect = pygame.Rect(windowwidth / 2 - 275, windowheight / 2 - 30 * buttoncount + 60 * button, 550, 80)
                if buttonlist[button][0] == "Game speed":
                    positions = 6
                    position = (GameplayConstants.fps - 30) / 5
                elif buttonlist[button][0] == "Music volume":
                    positions = 100
                    position = GameplayConstants.musicvolume
                elif buttonlist[button][0] == "Effects volume":
                    positions = 100
                    position = GameplayConstants.effectsvolume
                buttonrects.append(Tools.create_dragbar(dragrect, buttonlist[button][0], positions, position))
            else:
                buttonrects.append(pygame.Rect(windowwidth / 2 - 275, windowheight / 2 - 30 * buttoncount + 60 * button, 550, 50))
                pygame.draw.rect(screen, Colors.black, buttonrects[button])
                Tools.refresh_menubutton(buttonrects[button], mousepos, buttonlist[button], True)
        pygame.display.flip()
        return buttonrects


    def gamemenu(self):
        running = True
        pygame.mouse.set_visible(True)

        screenalpha = pygame.Surface((1920, 1080))
        screenalpha.set_alpha(150)
        screenalpha.fill(Colors.black)
        screen.blit(screenalpha, dest=(0, 0))
        buttonlist = ["Quit game", "Abort mission", "Settings", "Resume"]
        buttonrects = self.generate_menu(buttonlist)

        while running:
            mousepos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pressed()
                    if mouse[0]:
                        if buttonrects[0].collidepoint(mousepos):
                            pygame.quit()
                        elif buttonrects[1].collidepoint(mousepos):
                            self.level.abort = True
                            Sounds.sounds.soundclick.play()
                            return
                        elif buttonrects[2].collidepoint(mousepos):
                            self.optionmenu()
                            self.generate_menu(buttonlist)
                            Sounds.sounds.soundclick.play()
                        elif buttonrects[3].collidepoint(mousepos):
                            pygame.mouse.set_visible(False)
                            Sounds.sounds.soundclick.play()
                            return
                elif event.type == pygame.MOUSEMOTION:
                    self.generate_menu(buttonlist)
            clock.tick(GameplayConstants.fps)


    def optionmenu(self):
        running = True
        drag = False
        buttonrects = self.generate_menu([("Game speed", 7), ("Music volume", 7), ("Effects volume", 7), "Back"])
        while running:
            mousepos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pressed()
                    if mouse[0]:
                        if buttonrects[0].collidepoint(mousepos):
                            x = int((mousepos[0] - buttonrects[0].left) / (buttonrects[0].width / 7))
                            GameplayConstants.fps = 30 + x * 5
                            Sounds.sounds.soundclick.play()
                            drag = True
                            choice = 0
                        elif buttonrects[1].collidepoint(mousepos):
                            x = int((mousepos[0] - buttonrects[0].left) / (buttonrects[0].width / 101))
                            GameplayConstants.musicvolume = x
                            Sounds.sounds.soundclick.play()
                            pygame.mixer.music.set_volume(GameplayConstants.musicvolume / 100)
                            drag = True
                            choice = 1
                        elif buttonrects[2].collidepoint(mousepos):
                            x = int((mousepos[0] - buttonrects[0].left) / (buttonrects[0].width / 101))
                            GameplayConstants.effectsvolume = x
                            Sounds.sounds.soundchange()
                            Sounds.sounds.soundclick.play()
                            drag = True
                            choice = 2
                        elif buttonrects[3].collidepoint(mousepos):
                            Sounds.sounds.soundclick.play()
                            return
                        else:
                            choice = 3
                    self.generate_menu([("Game speed", 7), ("Music volume", 100), ("Effects volume", 100), "Back"])
                elif event.type == pygame.MOUSEMOTION:
                    self.generate_menu([("Game speed", 7), ("Music volume", 100), ("Effects volume", 100), "Back"])
                    if drag == True and choice < 3:
                        if choice == 0:
                            x = max(0, min(6, int((mousepos[0] - buttonrects[0].left) / (buttonrects[0].width / 7))))
                            GameplayConstants.fps = 30 + x * 5
                        elif choice == 1:
                            x = max(0, min(100, int((mousepos[0] - buttonrects[0].left) / (buttonrects[0].width / 101))))
                            GameplayConstants.musicvolume = x
                            pygame.mixer.music.set_volume(GameplayConstants.musicvolume / 100)
                        elif choice == 2:
                            x = max(0, min(100, int((mousepos[0] - buttonrects[0].left) / (buttonrects[0].width / 101))))
                            GameplayConstants.effectsvolume = x
                            Sounds.sounds.soundchange()
                elif event.type == pygame.MOUSEBUTTONUP:
                    drag = False

            clock.tick(GameplayConstants.fps)