import random

import Mobs
import Gamedata
import Backgroundprops
import Gametext
import Sounds

windowheight = 1080
warscreenwidth = 1440

class Level:
    def __init__(self, levelnumber):
        if levelnumber == 0:
            Mobs.images.load_level([x for x in range(13)])
            self.end = False
            self.succes = False
            self.abort = False
            self.ticks = 0
            self.spawnlist = []
            self.propslist = []
            self.textlist = []
            self.musiclist = []
            self.startscore = Gamedata.player.score
            self.startgold = Gamedata.player.gold
            for enemy in range(300):
                spawntime = enemy * 50 + 100
                unittype = random.randint(0, 2)
                variant = random.randint(0,2)
                speedx = random.randint(-3, 3)
                speedy = random.randint(6, 9)
                startx = random.randint(int(max(0,-(windowheight/speedy*speedx))), int(min(warscreenwidth ,warscreenwidth -(warscreenwidth  / speedy * speedx))))
                starty = 0
                programlist = [(0,0)]
                weaponprogramlist = [(0,0)]
                self.spawnlist.append([spawntime, unittype*3 + variant, startx, starty, speedx, speedy, programlist, weaponprogramlist, 0])

            ###################################################################################################

            #1 = na hoeveel ticks komt // 60 ticks is 1 sec
            #2 = unittype
            #3 = startx
            #4 = starty
            #5 = startsnelheid horizontaal
            #6 = startsnelheid verticaal
            #7 = movementprogramma
                #1 = starttime
                #2 = movementtype
                    #0 = straightline
                    #1 = zigzag
                    #2 = strafe
                    #3 = change direction zet (0,0 op derde en vierde plaats voor remmen)
                    #4 = charge (charge duurt 78 ticks, retour 156) (wanneer op derde en vierde plaats coordinaten worden
                    #    geplaatst charged die daar naar toe, anders naar de hero.
            #8 = wapenprogramma
                #1 = cooldown (of een tuple: (cooldown, startticks, endticks)
                #2 = weaponprogram
                    #0 = no weapon
                    #1 = aimed shot
                    #2 = machinegun
                    #3 = forward shot
                    #4 = cluster shot
                    #5 = flame thrower bijv: [4(cooldown), 5(programma), -1(gericht schieten)]
                    #                        [4(cooldown), 5(programma), 0 (angle in graden (0-360), 0 graden is naar beneden)]
                #3 = wapentype
                #4 = bulletcount (only used in cluster shot)
                #5 = angle between bullets (only used in cluster shot)

            #BACKGROUNDPROPS:
            #1 na hoeveel ticks
            #2 plaatjenummer
            #3 x coordinaat van de linkerkant van het plaatje. Meest linker punt van het plaatje.
            #4 snelheid naar beneden
            #5 resize tot dit formaat in tuple: (nummer,nummer)

            #TEXT
            #1 ticks
            #2 text
            #3 fontsize
            #4 RGB color code
            #5 (ticks fully visable, ticks fadeout)
            #6 centeredposition (x,y)
            #7 grote van het plaatje (hoe meer en hoe groter de text, hoe groter het plaatje moet zijn. Anders wordt de text afgeknipt.

            #hier laad je de achtergrondplaatjes. Het nummer correspondeerd met het bestandsnummeer. Er kunnen dus ook nieuwe plaatjes worden toegevoegd.
            Gamedata.bgimages = Backgroundprops.Images([0,1,2,3,4])

            #liedje starten is simpel: ticks + naam. Zorg dat de file staat in de musicfolder.
            #False = start direct, onderbreek huidige muziek, True betekend: speel af na huidige nummer.
            self.musiclist.append([0, '04. Cry.flac', False])
            self.musiclist.append([0, '07. Final Frontier.flac', True])

            # 0 ticks: aankondiging level text
            self.textlist.append([100, "Level 1: Jupiter", 30, (0,150,0), (160,40), (warscreenwidth/2,100), (800,50)])
            self.textlist.append([150, "WARNING: ASTERIOD STORM DETECTED", 30, (200, 0, 0), (100, 40), (warscreenwidth / 2, 150), (warscreenwidth, 50)])
            self.textlist.append([200, "WARNING: ENEMY SHIPS DETECTED", 30, (200, 0, 0), (100, 40), (warscreenwidth / 2, 200),(warscreenwidth, 50)])

            self.propslist.append([0, 4, 0, 1, (1920, 20000)])
            self.propslist.append([5000, 0, 700, 1, (900, 1278)])
            self.propslist.append([5500, 1, 500, 2, (675, 675)])
            self.propslist.append([9000, 2, 200, 2, (518, 520)])
            self.propslist.append([12000, 3, 800, 1, (100, 100)])


            # Cruiser komt in scherm, opend vuur. stopt vuur, straved weg.
            self.spawnlist.append([50, 10, warscreenwidth/2, 0, 0, 5, [(0, 0), (60,3,0,0), (240,2)], [((20,70,240), 4, 0, 5, 20)], 0])

            # 300 ticks: eerste aanval: fighters (horizontaal naar links, straight shot)
            self.spawnlist.append([300, 9, warscreenwidth, 200, -6, 0, [(0, 0)], [(30, 3, 0)],0])
            self.spawnlist.append([360, 9, warscreenwidth, 200, -6, 0, [(0, 0)], [(30, 3, 0)], 200])
            self.spawnlist.append([420, 9, warscreenwidth, 200, -6, 0, [(0, 0)], [(30, 3, 0)], 0])

            # 700 ticks: tweede aanval: fighters (verticaal, aimed)
            self.spawnlist.append([700, 9, 400, 0, 0, 4, [(0,0)], [(60,1,1)],0])
            self.spawnlist.append([760, 9, 800, 0, 0, 4, [(0, 0)], [(60, 1, 1)], 0])
            self.spawnlist.append([820, 9, 1200, 0, 0, 4, [(0, 0)], [(60, 1, 1)], 200])

            # 1100 ticks: derde aanval: fighters (driveby shooting, aimed)
            self.spawnlist.append([1100, 9, 0, 0, 3, 3, [(0,0)], [(100,1,1)],0])
            self.spawnlist.append([1160, 9, 1440, 0, -3, 3, [(0,0)], [(100,1,1)],200])
            self.spawnlist.append([1220, 9, 200, 0, 3, 3, [(0,0)], [(100,1,1)],0])
            self.spawnlist.append([1280, 9, 1240, 0, -3, 3, [(0,0)], [(100,1,1)],200])

            # 1500 ticks: vierde aanval: fighters (horizontaal naar rechts, aimed)
            self.spawnlist.append([1500, 9, 0, 200, 5, 0, [(0,0)], [(100,1,1)],200])
            self.spawnlist.append([1560, 9, 0, 200, 5, 0, [(0, 0)], [(100, 1, 1)], 0])
            self.spawnlist.append([1620, 9, 0, 200, 5, 0, [(0, 0)], [(100, 1, 1)], 200])
            self.spawnlist.append([1680, 9, 0, 200, 5, 0, [(0, 0)], [(100, 1, 1)], 0])

            # 1900 ticks: zesde aanval: fighters (move, shoot aimed, strafe)
            self.spawnlist.append([1900, 9, 420, 0, 0, 6, [(0,0),(40,2)], [(100,1,1)],200])
            self.spawnlist.append([2000, 9, 720, 0, 0, 6, [(0,0),(40,2)], [(100,1,1)],200])
            self.spawnlist.append([2100, 9, 1020, 0, 0, 6, [(0,0),(40,2)], [(100,1,1)],200])
            self.spawnlist.append([2200, 9, 420, 0, 0, 6, [(0,0),(40,2)], [(100,1,1)],200])
            self.spawnlist.append([2300, 9, 720, 0, 0, 6, [(0,0),(40,2)], [(100,1,1)],200])
            self.spawnlist.append([2400, 9, 1020, 0, 0, 6, [(0,0),(40,2)], [(100,1,1)],200])

            # 2600 ticks: zevende aanval fighters (move, stop, aimed shooting)
            self.spawnlist.append([2600, 9, 650, 0, 0, 2, [(0, 0), (40, 3, 0, 0), (0, 0), (0, 0, 0, 0)], [(60, 1, 1)], 200])
            self.spawnlist.append([2660, 9, 75, 0, 0, 2, [(0, 0), (40, 3, 0, 0), (0, 0), (0, 0, 0, 0)], [(60, 1, 1)], 200])
            self.spawnlist.append([2720, 9, 1350, 0, 0, 2, [(0, 0), (40, 3, 0, 0), (0, 0), (0, 0, 0, 0)], [(60, 1, 1)], 200])

            # 2900 ticks: achtste aanval:  cruiser (zigzag strafing mg)
            self.spawnlist.append([2900, 10, 650, 0, 0, 1, [(0, 0), (250, 1)], [(40, 2, 0)], 500])

            # 3600 ticks: negende aanval: fighters (move, shoot aimed, strafe)
            # en fighters (move, stop, aimed shooting)
            self.spawnlist.append([3600, 9, 100, 0, 0, 6, [(0,0),(40,2)], [(60,1,1)],0])
            self.spawnlist.append([3700, 9, 500, 0, 0, 6, [(0,0),(40,2)], [(60,1,1)],0])
            self.spawnlist.append([3850, 9, 650, 0, 0, 2, [(0, 0), (40, 3, 0, 0), (0, 0), (0, 0, 0, 0)], [(60, 1, 1)], 200])
            self.spawnlist.append([3850, 9, 800, 0, 0, 6, [(0, 0), (40, 2)], [(60, 1, 1)], 0])
            self.spawnlist.append([4000, 9, 75, 0, 0, 2, [(0, 0), (40, 3, 0, 0), (0, 0), (0, 0, 0, 0)], [(60, 1, 1)], 200])
            self.spawnlist.append([4000, 9, 250, 0, 0, 6, [(0, 0), (40, 2)], [(60, 1, 1)], 0])
            self.spawnlist.append([4150, 9, 1350, 0, 0, 2, [(0, 0), (40, 3, 0, 0), (0, 0), (0, 0, 0, 0)], [(60, 1, 1)], 200])
            self.spawnlist.append([4150, 9, 1000, 0, 0, 6, [(0, 0), (40, 2)], [(60, 1, 1)], 0])

            # 4500 ticks: tiende aanval: fighters (horizontaal naar rechts, mg)
            self.spawnlist.append([4500, 9, 0, 100, 5, 0, [(0, 0)], [(100, 2, 0)], 200])
            self.spawnlist.append([4600, 9, 0, 150, 5, 0, [(0, 0)], [(100, 2, 0)], 0])
            self.spawnlist.append([4700, 9, 0, 100, 5, 0, [(0, 0)], [(100, 2, 0)], 200])
            self.spawnlist.append([4800, 9, 0, 150, 5, 0, [(0, 0)], [(100, 2, 0)], 0])

            # 5000 ticks: elfde aanval: fighters (move, stop, change direction, shoot aimed)
            self.spawnlist.append([5000, 9, 75, 0, 0, 2, [(0, 0), (60, 3,0,0),(150,3,3,3)], [(100, 1, 1)], 0])
            self.spawnlist.append([5050, 9, 275, 0, 0, 2, [(0, 0), (60, 3, 0, 0), (130, 3, 3, 3)], [(100, 1, 1)], 0])
            self.spawnlist.append([5080, 9, 175, 0, 0, 2, [(0, 0), (60, 3, 0, 0), (120, 3, 3, 3)], [(100, 1, 1)], 200])
            self.spawnlist.append([5160, 9, 1200, 0, 0, 2, [(0, 0), (60, 3,0,0),(150,3,-3,4)], [(100, 1, 1)], 0])
            self.spawnlist.append([5200, 9, 1000, 0, 0, 2, [(0, 0), (60, 3, 0, 0), (130, 3, -3, 4)], [(100, 1, 1)], 0])
            self.spawnlist.append([5230, 9, 1100, 0, 0, 2, [(0, 0), (60, 3, 0, 0), (120, 3, -3, 4)], [(100, 1, 1)], 200])

            # 5400 ticks: twaalfde aanval: cruiser (zigzag strafing mg)
            self.spawnlist.append([5400, 10, 100, 0, 0, 1, [(0, 0), (250, 1)], [(40, 2, 0)], 500])

            # 6000 ticks: dertiende aanval: fighters (driveby shooting, mg)
            # en fighters (driveby shooting, aimed)
            self.spawnlist.append([6000, 9, 0, 0, 2, 2, [(0,0)], [(100,2,0)],0])
            self.spawnlist.append([6030, 9, 1440, 0, -2, 2, [(0,0)], [(100,2,0)],200])
            self.spawnlist.append([6060, 9, 200, 0, 2, 2, [(0, 0)], [(100, 2, 0)], 0])
            self.spawnlist.append([6090, 9, 1200, 0, -2, 2, [(0, 0)], [(100, 2, 0)], 200])
            self.spawnlist.append([6120, 9, 250, 0, 2, 2, [(0, 0)], [(100, 1, 1)], 0])
            self.spawnlist.append([6150, 9, 1100, 0, -2, 2, [(0, 0)], [(100, 1, 1)], 200])

            # 6500 ticks: veertiende aanval: fighters (zigzag strafing mg)
            self.spawnlist.append([6500, 9, 1300, 0, 0, 3, [(0, 1), (0, 0)], [(100, 2, 0)], 0])
            self.spawnlist.append([6550, 9, 25, 0, 0, 3, [(0, 1), (0, 0)], [(100, 2, 0)], 0])
            self.spawnlist.append([6590, 9, 300, 0, 0, 3, [(0, 1), (0, 0)], [(100, 2, 0)], 200])
            self.spawnlist.append([6660, 9, 0, 0, 0, 3, [(0, 1), (0, 0)], [(100, 2, 0)], 200])
            self.spawnlist.append([6700, 9, 1150, 0, 0, 3, [(0, 1), (0, 0)], [(100, 2, 0)], 0])
            self.spawnlist.append([6800, 9, 750, 0, 0, 3, [(0, 1), (0, 0)], [(100, 2, 0)], 0])

            # 7100 ticks: vijftiende aanval: cruiser (move, stop, cluster shot)
            # en fighters (move, stop, aimed shooting)
            self.spawnlist.append([7100, 9, 800, 0, 0, 2, [(0, 0), (180, 3, 0, 0), (0, 0), (0, 0, 0, 0)], [(100, 1, 1)], 0])
            self.spawnlist.append([7160, 10, 800, 0, 0, 1, [(0, 0), (250, 3, 0, 0), (0, 0), (0, 0, 0, 0)], [(100, 4, 0,3,20)], 500])
            self.spawnlist.append([7190, 9, 600, 0, 0, 2, [(0, 0), (80, 3, 0, 0), (0, 0), (0, 0, 0, 0)], [(100, 1, 1)], 0])
            self.spawnlist.append([7210, 9, 1000, 0, 0, 2, [(0, 0), (80, 3, 0, 0), (0, 0), (0, 0, 0, 0)], [(100, 1, 1)], 0])
            self.spawnlist.append([7240, 9, 600, 0, 0, 2, [(0, 0), (150, 3, 0, 0), (0, 0), (0, 0, 0, 0)], [(100, 1, 1)], 0])
            self.spawnlist.append([7250, 9, 1000, 0, 0, 2, [(0, 0), (150, 3, 0, 0), (0, 0), (0, 0, 0, 0)], [(100, 1, 1)], 0])

            # 7700 ticks: zestiende aanval: fighters (move, mg, strafe)
            # en fighters (horizontaal naar links, straight shot)
            self.spawnlist.append([7700, 9, 420, 0, 0, 5, [(0, 0), (40, 2)], [(100, 2, 0)], 0])
            self.spawnlist.append([7800, 9, 900, 0, 0, 5, [(0, 0), (40, 2)], [(100, 2, 0)], 0])
            self.spawnlist.append([7850, 9, warscreenwidth, 200, -5, 0, [(0, 0)], [(30, 3, 0)], 0])
            self.spawnlist.append([7900, 9, 600, 0, 0, 5, [(0, 0), (40, 2)], [(100, 2, 0)], 0])
            self.spawnlist.append([7950, 9, warscreenwidth, 200, -5, 0, [(0, 0)], [(30, 3, 0)], 0])
            self.spawnlist.append([8000, 9, 500, 0, 0, 5, [(0, 0), (40, 2)], [(100, 2, 0)], 0])
            self.spawnlist.append([8050, 9, warscreenwidth, 200, -5, 0, [(0, 0)], [(30, 3, 0)], 0])
            self.spawnlist.append([8100, 9, 200, 0, 0, 5, [(0, 0), (40, 2)], [(100, 2, 0)], 200])
            self.spawnlist.append([8200, 9, 1000, 0, 0, 5, [(0, 0), (40, 2)], [(100, 2, 0)], 200])

            # 8500 ticks: zeventiende aanval: fighters (move, stop, strafe, shoot aimed)
            self.spawnlist.append([8500, 9, 175, 0, 0, 2, [(0, 0), (30, 3, 0, 0), (150, 2, 3, 3)], [(100, 1, 1)], 0])
            self.spawnlist.append([8520, 9, 250, 0, 0, 3, [(0, 0), (60, 3, 0, 0), (160, 2, 3, 3)], [(100, 1, 1)], 0])
            self.spawnlist.append([8540, 9, 50, 0, 0, 2, [(0, 0), (40, 3, 0, 0), (175, 2, 3, 3)], [(100, 1, 1)], 0])
            self.spawnlist.append([8555, 9, 350, 0, 0, 3, [(0, 0), (50, 3, 0, 0), (175, 2, 3, 3)], [(100, 1, 1)], 200])

            # 8700 ticks: achttiende aanval: cruisers (zigzag strafing mg)
            self.spawnlist.append([8700, 10, 1100, 0, 0, 1, [(0, 0), (200, 1)], [(40, 2, 0)], 500])
            self.spawnlist.append([9000, 10, 100, 0, 0, 1, [(0, 0), (300, 1)], [(40, 2, 0)], 500])





            # 3400 ticks: achtste aanval cruiser (zigzag)
            # en fighters (move, shoot, strafe)
           # self.spawnlist.append([3400, 10, 300, 0, 0, 1, [(0, 0), (250, 1)], [(40,2,0)],200])
           # self.spawnlist.append([3460, 9, 100, 0, 0, 9, [(0,0),(40,2)], [(60,1,0)],0])
           # self.spawnlist.append([3520, 9, 500, 0, 0, 9, [(0,0),(40,2)], [(60,1,0)],0])

            # 3900 ticks: negende aanval fighters (links naar rechts schuin)
           # self.spawnlist.append([3900, 9, -100, 0, 4, 3, [(0, 0)], [(60, 1, 0)], 200])
            #self.spawnlist.append([3930, 9, -75, 0, 4, 3, [(0, 0)], [(60, 1, 0)], 0])
            #self.spawnlist.append([3960, 9, -50, 0, 4, 3, [(0, 0)], [(60, 1, 0)], 200])
            #self.spawnlist.append([3990, 9, -25, 0, 4, 3, [(0, 0)], [(60, 1, 0)], 0])
            #self.spawnlist.append([4020, 9, 0, 0, 4, 3, [(0, 0)], [(60, 1, 0)], 200])
            #self.spawnlist.append([4050, 9, 25, 0, 4, 3, [(0, 0)], [(60, 1, 0)], 0])
            #self.spawnlist.append([4080, 9, 50, 0, 4, 3, [(0, 0)], [(60, 1, 0)], 200])
            #self.spawnlist.append([4110, 9, 75, 0, 4, 3, [(0, 0)], [(60, 1, 0)], 0])

            # 4300 ticks: tiende aanval fighters (verticaal)
           # self.spawnlist.append([4300, 9, 1350, 0, 0, 4, [(0,0)], [(60,3,0)],0])
            #self.spawnlist.append([4300, 9, 500, 0, 0, 4, [(0, 0)], [(60, 3, 0)], 0])
            #self.spawnlist.append([4330, 9, 0, 0, 0, 4, [(0, 0)], [(60, 3, 0)], 200])
            #self.spawnlist.append([4330, 9, 750, 0, 0, 4, [(0, 0)], [(60, 3, 0)], 0])
            #self.spawnlist.append([4360, 9, 1000, 0, 0, 4, [(0, 0)], [(60, 3, 0)], 0])
            #self.spawnlist.append([4360, 9, 250, 0, 0, 4, [(0, 0)], [(60, 3, 0)], 200])
            #self.spawnlist.append([4390, 9, 50, 0, 0, 4, [(0, 0)], [(60, 3, 0)], 0])
            #self.spawnlist.append([4390, 9, 1100, 0, 0, 4, [(0, 0)], [(60, 3, 0)], 0])
            #self.spawnlist.append([4420, 9, 1350, 0, 0, 4, [(0, 0)], [(60, 3, 0)], 0])
            #self.spawnlist.append([4420, 9, 500, 0, 0, 4, [(0, 0)], [(60, 3, 0)], 200])
            #self.spawnlist.append([4450, 9, 0, 0, 0, 4, [(0, 0)], [(60, 3, 0)], 0])
            #self.spawnlist.append([4450, 9, 750, 0, 0, 4, [(0, 0)], [(60, 3, 0)], 0])
            #self.spawnlist.append([4480, 9, 1000, 0, 0, 4, [(0, 0)], [(60, 3, 0)], 0])
            #self.spawnlist.append([4480, 9, 250, 0, 0, 4, [(0, 0)], [(60, 3, 0)], 200])
            #self.spawnlist.append([4510, 9, 50, 0, 0, 4, [(0, 0)], [(60, 3, 0)], 0])
            #self.spawnlist.append([4510, 9, 1100, 0, 0, 4, [(0, 0)], [(60, 3, 0)], 0])

            # 4700 ticks: elfde aanval fighters (move, shoot, strafe)
           # self.spawnlist.append([4700, 9, 300, 0, 0, 9, [(0, 0), (40, 2)], [(60, 1, 0)], 0])
           # self.spawnlist.append([4800, 9, 100, 0, 0, 9, [(0, 0), (40, 2)], [(60, 1, 0)], 200])
           # self.spawnlist.append([4900, 9, 700, 0, 0, 9, [(0, 0), (40, 2)], [(60, 1, 0)], 0])
           # self.spawnlist.append([5000, 9, 1000, 0, 0, 9, [(0, 0), (40, 2)], [(60, 1, 0)], 0])
           # self.spawnlist.append([5100, 9, 750, 0, 0, 9, [(0, 0), (40, 2)], [(60, 1, 0)], 200])
           # self.spawnlist.append([5200, 9, 50, 0, 0, 9, [(0, 0), (40, 2)], [(60, 1, 0)], 0])
           # self.spawnlist.append([5300, 9, 1200, 0, 0, 9, [(0, 0), (40, 2)], [(60, 1, 0)], 0])
           # self.spawnlist.append([5400, 9, 500, 0, 0, 9, [(0, 0), (40, 2)], [(60, 1, 0)], 0])



            # 9000 ticks: helft van level

            # 18000 ticks (5 min): eindbaas


            #Deze vliegtuigen vliegen horizontaal
           # self.spawnlist.append([250, 9, warscreenwidth, 200, -4, 0, [(0,0)], [(60,1,0)],200])
           # self.spawnlist.append([325, 9, 0, 350, 4, 0, [(0,0)], [(60,1,0)],200])
           # self.spawnlist.append([400, 9, warscreenwidth, 500, -4, 0, [(0,0)], [(60,1,0)],200])
           # self.spawnlist.append([475, 9, 0, 650, 4, 0, [(0,0)], [(60,1,0)],200])

            #deze vliegen verticaal naar beneden
           # self.spawnlist.append([650, 9, 320, 0, 0, 7, [(0,0)], [(60,1,0)],0])
           # self.spawnlist.append([700, 9, 620, 0, 0, 7, [(0,0)], [(60,1,0)],0])
           # self.spawnlist.append([750, 9, 820, 0, 0, 7, [(0,0)], [(60,1,0)],0])
           # self.spawnlist.append([800, 9, 1120, 0, 0, 7, [(0, 0)], [(60,1,0)],0])

            #deze vliegen 40 ticks verticaal, waarna ze na 40 ticks gaan strafen
           # self.spawnlist.append([1050, 9, 420, 0, 0, 9, [(0,0),(40,2)], [(60,1,0)],0])
           # self.spawnlist.append([1125, 9, 720, 0, 0, 9, [(0,0),(40,2)], [(60,1,0)],0])
           # self.spawnlist.append([1200, 9, 1020, 0, 0, 9, [(0,0),(40,2)], [(60,1,0)],0])

            #deze cruiser begint recht, maar gaat na 250 ticks zigzaggen.
           # self.spawnlist.append([1450, 10, 300, 0, 0, 1, [(0, 0), (250, 1)], [(40,2,0)],0])

            #vliegtuigen kunnen ook schuin.
           # self.spawnlist.append([2050, 9, 0, 0, 5, 5, [(0,0)], [(60,1,0)],0])
           # self.spawnlist.append([2100, 9, 1440, 0, -5, 5, [(0,0)], [(60,1,0)],0])
           # self.spawnlist.append([2150, 9, 200, 0, 5, 5, [(0,0)], [(60,1,0)],0])
           # self.spawnlist.append([2200, 9, 1240, 0, -5, 5, [(0,0)], [(60,1,0)],0])

            #deze cruiser komt snel binnen, remt af en gaat dan zigzaggen, na 8 seconden (480 ticks) strafed die het scherm uit.
           # self.spawnlist.append([2450, 10, 300, 0, 0, 5, [(0, 0), (60, 3,0,0), (150,1), (480,2)], [(40,2,0)],800])

            #nog een paar verticaal vliegende tegenstanders
           # self.spawnlist.append([2900, 9, 320, 0, 0, 7, [(0,0)], [(60,1,0)],200])
           # self.spawnlist.append([2900, 9, 620, 0, 0, 7, [(0,0)], [(60,1,0)],200])
           # self.spawnlist.append([3000, 9, 820, 0, 0, 7, [(0,0)], [(60,1,0)],200])
           # self.spawnlist.append([3000, 9, 1120, 0, 0, 7, [(0,0)], [(60,1,0)],200])

            #bulltype unit die charged: komt scherm in, remt af, charged. Na charge gaat die naar achteren uit scherm.
           # self.spawnlist.append([3200, 11, 320, 0, 0, 7, [(0,0), (40,3,0,0),(100,4),(178,3,0,-7)], [(100,3,1)],400])
           # self.spawnlist.append([3300, 11, 320, 0, 0, 7, [(0, 0), (40, 3, 0, 0), (100, 4), (178, 3, 0, -7)], [(100, 3, 1)],400])

            #je kunt een schip ook meerdere wapensystemen geven, zoals aimed en forward
           # self.spawnlist.append([3700, 10, 300, 0, 0, 5, [(0, 0), (60, 3, 0, 0), (150, 1), (480, 2)], [(10, 3, 0),[100,1,1]],800])

            #deze charged naar vooraf bepaalde locaties. Elke charge duurt 78 ticks. Het laatste programma is een strafe weg.
           # self.spawnlist.append([4100, 11, 320, 0, 0, 7, [(0,0), (40,3,0,0),(100,4,1000,1000), (178,4,1300,300), (256,4,100,100), (334,2)], [(100,3,1)],400])

            #deze vliegen verticaal naar beneden met een voorwaarts zwaarder schot
           # self.spawnlist.append([4600, 9, 320, 0, 0, 7, [(0,0)], [(50,3,1)],0])
           # self.spawnlist.append([4620, 9, 620, 0, 0, 7, [(0,0)], [(50,3,1)],0])
           # self.spawnlist.append([4640, 9, 820, 0, 0, 7, [(0,0)], [(50,3,1)],0])
           # self.spawnlist.append([4660, 9, 1120, 0, 0, 7, [(0, 0)], [(50,3,1)],0])

            # deze eindbaas swingt een beetje heen en weer en schiet een cluster schot van 6 bullets met 10 graden ruimte tussen de bullets
           # self.spawnlist.append([5200, 12, 320, 0, 0, 6, [(0, 0), (60, 3,0,0), (150,1)], [(100, 4, 0, 6, 15), (60,1,1)], 1000])

            #level end
            self.spawnlist.append([10000, -1])

            ###################################################################################################
            #lijst wordt gesorteerd om op volgorde uit te kunnen voeren.
            self.spawnlist.sort(key=lambda x: x[0])
            self.propslist.sort(key=lambda x: x[0])

        for x in range(200):
            star = Backgroundprops.Star(True)
            Gamedata.stars.add(star)

    def spawning(self):
        if len(self.spawnlist) > 0:
            if self.spawnlist[0][0] == self.ticks:
                if self.spawnlist[0][1] == -1:
                    self.end = True
                    self.succes = True
                    return
                m = Mobs.Mob(self.spawnlist[0][1],self.spawnlist[0][2],self.spawnlist[0][3],self.spawnlist[0][4], self.spawnlist[0][5],self.spawnlist[0][6], self.spawnlist[0][7], self.spawnlist[0][8])
                Gamedata.all_sprites.add(m)
                Gamedata.mobs.add(m)
                self.spawnlist.pop(0)
                self.spawning()
        if len(self.propslist) > 0:
            if self.propslist[0][0] == self.ticks:
                prop = Backgroundprops.Backgroundprop(self.propslist[0][1],self.propslist[0][2],self.propslist[0][3],self.propslist[0][4])
                Gamedata.background.add(prop)
                self.propslist.pop(0)

        if len(self.textlist) > 0:
            if self.textlist[0][0] == self.ticks:
                text = Gametext.Text(self.textlist[0][1],self.textlist[0][2],self.textlist[0][3],self.textlist[0][4],self.textlist[0][5],self.textlist[0][6])
                Gamedata.background.add(text)
                self.textlist.pop(0)
        if len(self.musiclist) > 0:
            if self.musiclist[0][0] == self.ticks:
                Sounds.playsong(self.musiclist[0][1], self.musiclist[0][2])
                self.musiclist.pop(0)

        if random.randint(0,10) == 0:
            star = Backgroundprops.Star(False)
            Gamedata.stars.add(star)
        self.ticks += 1
        return

