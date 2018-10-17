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
import Button

screen = GameplayConstants.screen

"""Hier staat de loop waarin elk level wordt uitgevoerd. De mobs en overige zaken die tevoorschijn komen staan in een lijst in 'Level'."""

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

    def gamemenu(self):
        pygame.mouse.set_visible(True)
        drag = False
        screenalpha = pygame.Surface((1920, 1080))
        screenalpha.set_alpha(150)
        screenalpha.fill(Colors.black)
        screen.blit(screenalpha, dest=(0, 0))
        pygame.draw.rect(screen, Colors.darkgray, pygame.Rect(windowwidth / 2 - 300, windowheight / 2 - 180, 600, 360))
        mainmenu = [Button.Button(pygame.Rect(windowwidth / 2 - 275, windowheight / 2 - 115, 550, 50),"Quit game", "Quit"),
                    Button.Button(pygame.Rect(windowwidth / 2 - 275, windowheight / 2 - 55, 550, 50), "Abort mission", "Abort"),
                    Button.Button(pygame.Rect(windowwidth / 2 - 275, windowheight / 2 + 5, 550, 50), "Settings", "Settings"),
                    Button.Button(pygame.Rect(windowwidth / 2 - 275, windowheight / 2 + 65, 550, 50), "Resume", "Resume")]
        speed = (GameplayConstants.fps - 30) / 5

        optionmenu = [Button.Dragbar(pygame.Rect(windowwidth / 2 - 275, windowheight / 2 - 160, 550, 80),"Game speed", 6, speed, False),
                      Button.Dragbar(pygame.Rect(windowwidth / 2 - 275, windowheight / 2 - 70, 550, 80), "Music volume", 100, GameplayConstants.musicvolume, False),
                      Button.Dragbar(pygame.Rect(windowwidth / 2 - 275, windowheight / 2 + 20, 550, 80), "Effects volume", 100, GameplayConstants.effectsvolume, False),
                      Button.Button(pygame.Rect(windowwidth / 2 - 275, windowheight / 2 + 110, 550, 50), "Return", "Return", False)]
        pygame.display.flip()

        while True:
            mousepos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pressed()
                    if mouse[0]:
                        for button in optionmenu:
                            if button.active and button.rect.collidepoint(mousepos):
                                if button.function == "Game speed":
                                    x = int((mousepos[0] - button.rect.left) / (button.rect.width / 7))
                                    GameplayConstants.fps = 30 + x * 5
                                    button.chosenoption = x
                                    Sounds.sounds.soundclick.play()
                                    drag = True
                                    choice = 0
                                    button.update()
                                elif button.function == "Music volume":
                                    x = int((mousepos[0] - button.rect.left) / (button.rect.width / 101))
                                    GameplayConstants.musicvolume = x
                                    button.chosenoption = x
                                    Sounds.sounds.soundclick.play()
                                    pygame.mixer.music.set_volume(GameplayConstants.musicvolume / 100)
                                    drag = True
                                    choice = 1
                                    button.update()
                                elif button.function == "Effects volume":
                                    x = int((mousepos[0] - button.rect.left) / (button.rect.width / 101))
                                    GameplayConstants.effectsvolume = x
                                    button.chosenoption = x
                                    Sounds.sounds.soundchange()
                                    Sounds.sounds.soundclick.play()
                                    drag = True
                                    choice = 2
                                    button.update()

                                elif button.function == "Return":
                                    pygame.draw.rect(screen, Colors.darkgray, pygame.Rect(windowwidth / 2 - 300, windowheight / 2 - 180, 600, 360))
                                    for button in optionmenu:
                                        button.active = False
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
                                    pygame.draw.rect(screen, Colors.darkgray, pygame.Rect(windowwidth / 2 - 300, windowheight / 2 - 180, 600, 360))
                                    for button in mainmenu:
                                        button.active = False
                                    for button in optionmenu:
                                        button.active = True
                                        button.update()
                                    Sounds.sounds.soundclick.play()
                                elif button.function == "Resume":
                                    pygame.mouse.set_visible(False)
                                    Sounds.sounds.soundclick.play()
                                    return

                elif event.type == pygame.MOUSEMOTION:
                    if drag:
                        if choice == 0:
                            x = max(0, min(6, int((mousepos[0] - optionmenu[0].rect.left) / (optionmenu[0].rect.width / 7))))
                            GameplayConstants.fps = 30 + x * 5
                            optionmenu[0].chosenoption = x
                        elif choice == 1:
                            x = max(0, min(100, int((mousepos[0] - optionmenu[1].rect.left) / (optionmenu[1].rect.width / 101))))
                            GameplayConstants.musicvolume = x
                            pygame.mixer.music.set_volume(GameplayConstants.musicvolume / 100)
                            optionmenu[1].chosenoption = x
                        elif choice == 2:
                            x = max(0, min(100, int((mousepos[0] - optionmenu[2].rect.left) / (optionmenu[2].rect.width / 101))))
                            GameplayConstants.effectsvolume = x
                            Sounds.sounds.soundchange()
                            optionmenu[2].chosenoption = x
                    for button in mainmenu:
                        button.update()
                    for button in optionmenu:
                        button.update()
                elif event.type == pygame.MOUSEBUTTONUP:
                    drag = False
            pygame.display.flip()
            clock.tick(GameplayConstants.fps)
