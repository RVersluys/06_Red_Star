import random

import Mobs
import Gamedata
import Backgroundprops
import Gametext
import Sounds

windowheight = 1080
warscreenwidth = 1440

class Level:
    def __init__(self):

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
        for missilelauncher in Gamedata.player.missiles:
            missilelauncher.replenish()
        for x in range(200):
            star = Backgroundprops.Star(True)
            Gamedata.stars.add(star)
        mobslist = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
        Mobs.images.load_level(mobslist)
        if Gamedata.player.levelnumber == 0:
            self.level_1()
        else:
            self.level_2()
        self.spawnlist.sort(key=lambda x: x[0])
        self.propslist.sort(key=lambda x: x[0])
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


    def level_1(self):
        Gamedata.bgimages = Backgroundprops.Images([0, 1, 2, 3])
        for enemy in range(300):
            spawntime = enemy * 50 + 100
            unittype = random.randint(0, 2)
            variant = random.randint(0, 2)
            speedx = random.randint(-3, 3)
            speedy = random.randint(6, 9)
            startx = random.randint(int(max(0, -(windowheight / speedy * speedx))), int(min(warscreenwidth, warscreenwidth - (warscreenwidth / speedy * speedx))))
            starty = 0
            programlist = [(0, 0)]
            weaponprogramlist = [(0, 0)]
            self.spawnlist.append([spawntime, unittype * 3 + variant, startx, starty, speedx, speedy, programlist, weaponprogramlist, 0])

        # liedje starten is simpel: ticks + naam. Zorg dat de file staat in de musicfolder.
        # False = start direct, onderbreek huidige muziek, True betekend: speel af na huidige nummer.
        self.musiclist.append([0, '04. Cry.flac', False])
        self.musiclist.append([0, '07. Final Frontier.flac', True])

        # 0 ticks: aankondiging level text
        self.textlist.append([100, "Level 1: Jupiter", 30, (0, 150, 0), (160, 40), (warscreenwidth / 2, 100), (800, 50)])
        self.textlist.append([150, "WARNING: ASTERIOD STORM DETECTED", 30, (200, 0, 0), (100, 40), (warscreenwidth / 2, 150), (warscreenwidth, 50)])
        self.textlist.append([200, "WARNING: ENEMY SHIPS DETECTED", 30, (200, 0, 0), (100, 40), (warscreenwidth / 2, 200), (warscreenwidth, 50)])

        self.propslist.append([5000, 0, 900, 1, (540, 767)])
        self.propslist.append([5500, 1, 600, 2, (675, 675)])
        self.propslist.append([9000, 2, 200, 2, (518, 520)])
        self.propslist.append([12000, 3, 800, 1, (240, 97)])

        # 500 ticks: eerste aanval: fighters (horizontaal naar links)
        self.spawnlist.append([500, 9, warscreenwidth, 200, -4, 0, [(0, 0)], [(100, 3, 0)], 0])
        self.spawnlist.append([560, 9, warscreenwidth, 200, -4, 0, [(0, 0)], [(100, 3, 0)], 200])
        self.spawnlist.append([620, 9, warscreenwidth, 200, -4, 0, [(0, 0)], [(100, 3, 0)], 0])

        # 1000 ticks: tweede aanval: fighters (verticaal)
        self.spawnlist.append([1000, 9, 400, 0, 0, 4, [(0, 0)], [(100, 3, 0)], 0])
        self.spawnlist.append([1060, 9, 800, 0, 0, 4, [(0, 0)], [(100, 3, 0)], 0])
        self.spawnlist.append([1120, 9, 1200, 0, 0, 4, [(0, 0)], [(100, 3, 0)], 200])

        # 1500 ticks: derde aanval: fighters (driveby shooting)
        self.spawnlist.append([1500, 9, 0, 0, 3, 3, [(0, 0)], [(100, 3, 0)], 0])
        self.spawnlist.append([1560, 9, 1440, 0, -3, 3, [(0, 0)], [(100, 3, 0)], 200])
        self.spawnlist.append([1520, 9, 200, 0, 3, 3, [(0, 0)], [(100, 3, 0)], 0])
        self.spawnlist.append([1580, 9, 1240, 0, -3, 3, [(0, 0)], [(100, 3, 0)], 200])

        # 2000 ticks: vierde aanval: fighters (horizontaal naar rechts)
        self.spawnlist.append([2000, 9, 0, 200, 4, 0, [(0, 0)], [(100, 3, 0)], 200])
        self.spawnlist.append([2060, 9, 0, 200, 4, 0, [(0, 0)], [(100, 3, 0)], 0])
        self.spawnlist.append([2120, 9, 0, 200, 4, 0, [(0, 0)], [(100, 3, 0)], 200])
        self.spawnlist.append([2180, 9, 0, 200, 4, 0, [(0, 0)], [(100, 3, 0)], 0])

        # 2500 ticks: zesde aanval: fighters (move, strafe)
        self.spawnlist.append([2500, 9, 420, 0, 0, 3, [(0, 0), (40, 2)], [(100, 3, 0)], 200])
        self.spawnlist.append([2600, 9, 720, 0, 0, 3, [(0, 0), (40, 2)], [(100, 3, 0)], 200])
        self.spawnlist.append([2700, 9, 1020, 0, 0, 3, [(0, 0), (40, 2)], [(100, 3, 0)], 200])
        self.spawnlist.append([2800, 9, 420, 0, 0, 3, [(0, 0), (40, 2)], [(100, 3, 0)], 200])
        self.spawnlist.append([2900, 9, 720, 0, 0, 3, [(0, 0), (40, 2)], [(100, 3, 0)], 200])
        self.spawnlist.append([3000, 9, 1020, 0, 0, 3, [(0, 0), (40, 2)], [(100, 3, 0)], 200])

        # 3300 ticks: zevende aanval: vultures (move, slower)
        self.spawnlist.append([3300, 15, 650, 0, 0, 2, [(0, 0), (40, 3, 0, 1), (0, 0), (0, 0, 0, 0)], [(100, 1, 0)], 250])
        self.spawnlist.append([3360, 15, 300, 0, 0, 2, [(0, 0), (40, 3, 0, 1), (0, 0), (0, 0, 0, 0)], [(100, 1, 0)], 250])
        self.spawnlist.append([3420, 15, 850, 0, 0, 2, [(0, 0), (40, 3, 0, 1), (0, 0), (0, 0, 0, 0)], [(100, 1, 0)], 250])

        # 3900 ticks: achtste aanval:  cruiser (zigzag strafing)
        self.spawnlist.append([3900, 10, 650, 0, 0, 1, [(0, 0), (250, 1)], [(40, 2, 0)], 500])

        # 4700 ticks: negende aanval: fighters (move, strafe)
        # en vultures (move, slower)
        self.spawnlist.append([4700, 9, 100, 0, 0, 4, [(0, 0), (40, 2)], [(100, 3, 0)], 0])
        self.spawnlist.append([4800, 9, 500, 0, 0, 4, [(0, 0), (40, 2)], [(100, 3, 0)], 0])
        self.spawnlist.append([4950, 15, 650, 0, 0, 2, [(0, 0), (40, 3, 0, 1), (0, 0), (0, 0, 0, 0)], [(100, 1, 0)], 250])
        self.spawnlist.append([4950, 9, 800, 0, 0, 4, [(0, 0), (40, 2)], [(100, 3, 0)], 0])
        self.spawnlist.append([5100, 15, 75, 0, 0, 2, [(0, 0), (40, 3, 0, 1), (0, 0), (0, 0, 0, 0)], [(100, 1, 0)], 250])
        self.spawnlist.append([5100, 9, 250, 0, 0, 4, [(0, 0), (40, 2)], [(100, 3, 0)], 0])
        self.spawnlist.append([5250, 15, 1350, 0, 0, 2, [(0, 0), (40, 3, 0, 1), (0, 0), (0, 0, 0, 0)], [(100, 1, 0)], 250])
        self.spawnlist.append([5250, 9, 1000, 0, 0, 4, [(0, 0), (40, 2)], [(100, 3, 0)], 0])

        # 5700 ticks: tiende aanval: fighters (horizontaal naar rechts)
        self.spawnlist.append([5700, 9, 0, 100, 4, 0, [(0, 0)], [(100, 3, 0)], 200])
        self.spawnlist.append([5800, 9, 0, 150, 4, 0, [(0, 0)], [(100, 3, 0)], 0])
        self.spawnlist.append([5900, 9, 0, 100, 4, 0, [(0, 0)], [(100, 3, 0)], 200])
        self.spawnlist.append([6000, 9, 0, 150, 4, 0, [(0, 0)], [(100, 3, 0)], 0])

        # 6300 ticks: elfde aanval: fighters (move, stop, change direction)
        self.spawnlist.append([6300, 9, 75, 0, 0, 2, [(0, 0), (60, 3, 0, 0), (150, 3, 3, 3)], [(100, 3, 0)], 0])
        self.spawnlist.append([6350, 9, 275, 0, 0, 2, [(0, 0), (60, 3, 0, 0), (130, 3, 3, 3)], [(100, 3, 0)], 0])
        self.spawnlist.append([6380, 9, 175, 0, 0, 2, [(0, 0), (60, 3, 0, 0), (120, 3, 3, 3)], [(100, 3, 0)], 200])
        self.spawnlist.append([6460, 9, 1200, 0, 0, 2, [(0, 0), (60, 3, 0, 0), (150, 3, -3, 4)], [(100, 3, 0)], 0])
        self.spawnlist.append([6500, 9, 1000, 0, 0, 2, [(0, 0), (60, 3, 0, 0), (130, 3, -3, 4)], [(100, 3, 0)], 0])
        self.spawnlist.append([6530, 9, 1100, 0, 0, 2, [(0, 0), (60, 3, 0, 0), (120, 3, -3, 4)], [(100, 3, 0)], 200])

        # 6800 ticks: twaalfde aanval: cruiser (zigzag strafing)
        self.spawnlist.append([6800, 10, 100, 0, 0, 1, [(0, 0), (250, 1)], [(40, 2, 0)], 500])

        # 7500 ticks: dertiende aanval: fighters (driveby)
        # en fighters (driveby)
        self.spawnlist.append([7500, 9, 0, 0, 2, 2, [(0, 0)], [(100, 3, 0)], 0])
        self.spawnlist.append([7530, 9, 1440, 0, -2, 2, [(0, 0)], [(100, 3, 0)], 200])
        self.spawnlist.append([7560, 9, 200, 0, 2, 2, [(0, 0)], [(100, 3, 0)], 0])
        self.spawnlist.append([7590, 9, 1200, 0, -2, 2, [(0, 0)], [(100, 3, 0)], 200])
        self.spawnlist.append([7620, 9, 250, 0, 2, 2, [(0, 0)], [(100, 3, 0)], 0])
        self.spawnlist.append([7650, 9, 1100, 0, -2, 2, [(0, 0)], [(100, 3, 0)], 200])

        # 8100 ticks: veertiende aanval: fighters (zigzag strafing)
        self.spawnlist.append([8100, 9, 1300, 0, 0, 3, [(0, 1), (0, 0)], [(100, 3, 0)], 0])
        self.spawnlist.append([8150, 9, 25, 0, 0, 3, [(0, 1), (0, 0)], [(100, 3, 0)], 0])
        self.spawnlist.append([8190, 9, 300, 0, 0, 3, [(0, 1), (0, 0)], [(100, 3, 0)], 200])
        self.spawnlist.append([8260, 9, 0, 0, 0, 3, [(0, 1), (0, 0)], [(100, 3, 0)], 200])
        self.spawnlist.append([8300, 9, 1150, 0, 0, 3, [(0, 1), (0, 0)], [(100, 3, 0)], 0])
        self.spawnlist.append([8400, 9, 750, 0, 0, 3, [(0, 1), (0, 0)], [(100, 3, 0)], 0])

        # 8800 ticks: vijftiende aanval: cruiser (move, slower)
        # en fighters (move, slower)
        self.spawnlist.append([8800, 9, 800, 0, 0, 2, [(0, 0), (180, 3, 0, 1), (0, 0), (0, 0, 0, 0)], [(100, 3, 0)], 0])
        self.spawnlist.append([8860, 10, 800, 0, 0, 1, [(0, 0), (250, 3, 0, 1), (0, 0), (0, 0, 0, 0)], [(100, 2, 0)], 500])
        self.spawnlist.append([8890, 9, 600, 0, 0, 2, [(0, 0), (80, 3, 0, 1), (0, 0), (0, 0, 0, 0)], [(100, 3, 0)], 0])
        self.spawnlist.append([8910, 9, 1000, 0, 0, 2, [(0, 0), (80, 3, 0, 1), (0, 0), (0, 0, 0, 0)], [(100, 3, 0)], 0])
        self.spawnlist.append([8940, 9, 600, 0, 0, 2, [(0, 0), (150, 3, 0, 1), (0, 0), (0, 0, 0, 0)], [(100, 3, 0)], 0])
        self.spawnlist.append([8950, 9, 1000, 0, 0, 2, [(0, 0), (150, 3, 0, 1), (0, 0), (0, 0, 0, 0)], [(100, 3, 0)], 0])

        # 9500 ticks: zestiende aanval: fighters (move, strafe)
        # en vultures (horizontaal naar links)
        self.spawnlist.append([9500, 9, 420, 0, 0, 2, [(0, 0), (40, 2)], [(100, 3, 0)], 0])
        self.spawnlist.append([9600, 9, 900, 0, 0, 2, [(0, 0), (40, 2)], [(100, 3, 0)], 0])
        self.spawnlist.append([9650, 15, warscreenwidth, 200, -2, 0, [(0, 0)], [(100, 1, 0)], 250])
        self.spawnlist.append([9700, 9, 600, 0, 0, 2, [(0, 0), (40, 2)], [(100, 3, 0)], 0])
        self.spawnlist.append([9750, 15, warscreenwidth, 200, -2, 0, [(0, 0)], [(100, 1, 0)], 250])
        self.spawnlist.append([9800, 9, 500, 0, 0, 2, [(0, 0), (40, 2)], [(100, 3, 0)], 0])
        self.spawnlist.append([9850, 15, warscreenwidth, 200, -2, 0, [(0, 0)], [(100, 1, 0)], 250])
        self.spawnlist.append([9900, 9, 200, 0, 0, 2, [(0, 0), (40, 2)], [(100, 3, 0)], 0])
        self.spawnlist.append([9900, 9, 1000, 0, 0, 2, [(0, 0), (40, 2)], [(100, 3, 0)], 0])

        # 10400 ticks: zeventiende aanval: fighters (move, stop, strafe)
        self.spawnlist.append([10400, 9, 175, 0, 0, 2, [(0, 0), (30, 2, 0, 0), (150, 2, 3, 3)], [(100, 3, 0)], 0])
        self.spawnlist.append([10420, 9, 250, 0, 0, 2, [(0, 0), (60, 2, 0, 0), (160, 2, 3, 3)], [(100, 3, 0)], 0])
        self.spawnlist.append([10440, 9, 50, 0, 0, 2, [(0, 0), (40, 2, 0, 0), (175, 2, 3, 3)], [(100, 3, 0)], 0])
        self.spawnlist.append([10455, 9, 350, 0, 0, 2, [(0, 0), (50, 2, 0, 0), (175, 2, 3, 3)], [(100, 3, 0)], 200])

        # 10700 ticks: achttiende aanval: cruisers (zigzag strafing)
        self.spawnlist.append([10700, 10, 1100, 0, 0, 1, [(0, 0), (200, 1)], [(40, 2, 0)], 500])
        self.spawnlist.append([11200, 10, 100, 0, 0, 1, [(0, 0), (300, 1)], [(40, 2, 0)], 500])

        # 11700 ticks: negentiende aanval: marauders (move, stop, charge, retreat)
        self.spawnlist.append([11700, 11, 500, 0, 0, 4, [(0, 0), (40, 3, 0, 0), (100, 4), (178, 3, 0, -7)], [(100, 2, 0), [3, 5, -1]], 300])
        self.spawnlist.append([12000, 11, 950, 0, 0, 4, [(0, 0), (40, 3, 0, 0), (100, 4), (178, 3, 0, -7)], [(100, 2, 0), [3, 5, -1]], 300])
        self.spawnlist.append([12250, 11, 140, 0, 0, 4, [(0, 0), (40, 3, 0, 0), (100, 4), (178, 3, 0, -7)], [(100, 2, 0), [3, 5, -1]], 300])

        # 12500 ticks: twintigste aanval: fighters (move, strafe)
        # en vultures (verticaal)
        self.spawnlist.append([12500, 9, 50, 0, 0, 3, [(0, 0), (40, 2)], [(100, 3, 0)], 0])
        self.spawnlist.append([12580, 9, 800, 0, 0, 3, [(0, 0), (40, 2)], [(100, 3, 0)], 0])
        self.spawnlist.append([12660, 9, 1020, 0, 0, 3, [(0, 0), (40, 2)], [(100, 3, 0)], 0])
        self.spawnlist.append([12740, 9, 200, 0, 0, 3, [(0, 0), (40, 2)], [(100, 3, 0)], 0])
        self.spawnlist.append([12820, 9, 720, 0, 0, 3, [(0, 0), (40, 2)], [(100, 3, 0)], 0])
        self.spawnlist.append([12900, 9, 1020, 0, 0, 3, [(0, 0), (40, 2)], [(100, 3, 0)], 0])
        self.spawnlist.append([13000, 15, 600, 0, 0, 2, [(0, 0)], [(100, 1, 0)], 250])
        self.spawnlist.append([13100, 15, 300, 0, 0, 2, [(0, 0)], [(100, 1, 0)], 250])
        self.spawnlist.append([13200, 15, 500, 0, 0, 2, [(0, 0)], [(100, 1, 0)], 250])
        self.spawnlist.append([13300, 15, 200, 0, 0, 2, [(0, 0)], [(100, 1, 0)], 250])

        # 13500 ticks: eenentwintigste aanval: destroyer (verticaal)
        self.spawnlist.append([13500, 14, warscreenwidth / 2, 0, 0, 2, [(0, 0)], [(100, 4, 0, 3, 15)], 350])

        # 13900 ticks: tweeentwintigste aanval: fighters (driveby)
        # en vultures (horizontaal naar rechts)
        # en marauders (move, stop, charge, retreat)
        # en cruiser (verticaal)
        # en destroyers (verticaal)
        self.spawnlist.append([13900, 9, 1400, 0, -2, 2, [(0, 0)], [(100, 3, 0)], 0])
        self.spawnlist.append([13930, 9, 50, 0, 2, 2, [(0, 0)], [(100, 3, 0)], 0])
        self.spawnlist.append([13960, 9, 400, 0, 2, 2, [(0, 0)], [(100, 3, 0)], 0])
        self.spawnlist.append([13990, 9, 1300, 0, -2, 2, [(0, 0)], [(100, 3, 0)], 0])
        self.spawnlist.append([14020, 9, 160, 0, 2, 2, [(0, 0)], [(100, 3, 0)], 0])
        self.spawnlist.append([14050, 9, 800, 0, -2, 2, [(0, 0)], [(100, 3, 0)], 0])
        self.spawnlist.append([14300, 15, 0, 200, 2, 0, [(0, 0)], [(100, 1, 0)], 0])
        self.spawnlist.append([14400, 15, 0, 175, 2, 0, [(0, 0)], [(100, 1, 0)], 0])
        self.spawnlist.append([14500, 15, 0, 150, 2, 0, [(0, 0)], [(100, 1, 0)], 0])
        self.spawnlist.append([14600, 15, 0, 125, 2, 0, [(0, 0)], [(100, 1, 0)], 250])
        self.spawnlist.append([14900, 11, 100, 0, 0, 4, [(0, 0), (40, 3, 0, 0), (100, 4), (178, 3, 0, -7)], [(100, 2, 0), [3, 5, -1]], 0])
        self.spawnlist.append([15200, 11, warscreenwidth / 2, 0, 0, 4, [(0, 0), (40, 3, 0, 0), (100, 4), (178, 3, 0, -7)], [(100, 2, 0), [3, 5, -1]], 300])
        self.spawnlist.append([15600, 10, 850, 0, 0, 1, [(0, 0), (0, 0)], [(40, 2, 0)], 500])
        self.spawnlist.append([16000, 14, 300, 0, 0, 2, [(0, 0)], [(100, 4, 0, 3, 15)], 0])
        self.spawnlist.append([16300, 14, 1000, 0, 0, 2, [(0, 0)], [(100, 4, 0, 3, 15)], 350])

        # 16700 ticks: drieentwintigste aanval: fighters (verticaal)
        self.spawnlist.append([16700, 9, 700, 0, 0, 2, [(0, 0)], [(100, 3, 0)], 0])
        self.spawnlist.append([16750, 9, 700, 0, 0, 2, [(0, 0)], [(100, 3, 0)], 0])
        self.spawnlist.append([16750, 9, 600, 0, 0, 2, [(0, 0)], [(100, 3, 0)], 0])
        self.spawnlist.append([16750, 9, 800, 0, 0, 2, [(0, 0)], [(100, 3, 0)], 0])
        self.spawnlist.append([16800, 9, 700, 0, 0, 2, [(0, 0)], [(100, 3, 0)], 200])
        self.spawnlist.append([16800, 9, 600, 0, 0, 2, [(0, 0)], [(100, 3, 0)], 0])
        self.spawnlist.append([16800, 9, 800, 0, 0, 2, [(0, 0)], [(100, 3, 0)], 0])
        self.spawnlist.append([16800, 9, 500, 0, 0, 2, [(0, 0)], [(100, 3, 0)], 0])
        self.spawnlist.append([16800, 9, 900, 0, 0, 2, [(0, 0)], [(100, 3, 0)], 0])

        # 17300 ticks: vierentwintigste aanval: vultures (move, strafe)
        # en destroyer (naar rechts)
        self.spawnlist.append([17300, 15, 750, 0, 0, 2, [(0, 0), (40, 2)], [(100, 1, 0)], 0])
        self.spawnlist.append([17400, 15, 500, 0, 0, 2, [(0, 0), (40, 2)], [(100, 1, 0)], 0])
        self.spawnlist.append([17500, 15, 1000, 0, 0, 2, [(0, 0), (40, 2)], [(100, 1, 0)], 0])
        self.spawnlist.append([17600, 15, 500, 0, 0, 2, [(0, 0), (40, 2)], [(100, 1, 0)], 250])
        self.spawnlist.append([17650, 14, 250, 0, 0, 2, [(0, 0)], [(100, 4, 0, 3, 15)], 350])

        self.textlist.append([18300, "WARNING: LARGE ENEMY SHIP DETECTED", 30, (200, 0, 0), (100, 40), (warscreenwidth / 2, 100), (warscreenwidth, 50)])
        self.textlist.append([18600, "SCANNING...", 30, (255, 255, 255), (100, 40), (warscreenwidth / 2, 50), (warscreenwidth, 100)])
        self.textlist.append([18800, "SCORCH COMMAND SHIP: HEXAPOD", 30, (255, 255, 255), (100, 40), (warscreenwidth / 2, 100), (warscreenwidth, 50)])

        # 18300 ticks: aankondiging + eindbaas: Hexapod (zigzag)
        self.spawnlist.append([19000, 12, 320, 0, 0, 6, [(0, 0), (60, 3, 0, 0), (150, 1), (600, 4), (756, 1), (1226, 4), (1382, 1), (1832, 4), (1988, 1)],
                               [((50, 50, 620), 4, 0, 6, 15), ((20, 776, 1226), 1, 1), ((50, 1382, 1832), 4, 0, 6, 15), ((50, 1988, 99999), 2, 0), ((100, 2100, 99999), 4, 0, 6, 20)], 1000])

        # level end
        self.spawnlist.append([19000, -1])

        ###################################################################################################

    def level_2(self):
        #Deze vliegtuigen vliegen horizontaal
        self.spawnlist.append([250, 9, warscreenwidth, 200, -4, 0, [(0,0)], [(60,1,0)],200])
        self.spawnlist.append([325, 9, 0, 350, 4, 0, [(0,0)], [(60,1,0)],200])
        self.spawnlist.append([400, 9, warscreenwidth, 500, -4, 0, [(0,0)], [(60,1,0)],200])
        self.spawnlist.append([475, 9, 0, 650, 4, 0, [(0,0)], [(60,1,0)],200])

        #deze vliegen verticaal naar beneden
        self.spawnlist.append([650, 9, 320, 0, 0, 7, [(0,0)], [(60,1,0)],0])
        self.spawnlist.append([700, 9, 620, 0, 0, 7, [(0,0)], [(60,1,0)],0])
        self.spawnlist.append([750, 9, 820, 0, 0, 7, [(0,0)], [(60,1,0)],0])
        self.spawnlist.append([800, 9, 1120, 0, 0, 7, [(0, 0)], [(60,1,0)],0])

        #deze vliegen 40 ticks verticaal, waarna ze na 40 ticks gaan strafen
        self.spawnlist.append([1050, 9, 420, 0, 0, 9, [(0,0),(40,2)], [(60,1,0)],0])
        self.spawnlist.append([1125, 9, 720, 0, 0, 9, [(0,0),(40,2)], [(60,1,0)],0])
        self.spawnlist.append([1200, 9, 1020, 0, 0, 9, [(0,0),(40,2)], [(60,1,0)],0])

        #deze cruiser begint recht, maar gaat na 250 ticks zigzaggen.
        self.spawnlist.append([1450, 10, 300, 0, 0, 1, [(0, 0), (250, 1)], [(40,2,0)],0])

        #vliegtuigen kunnen ook schuin.
        self.spawnlist.append([2050, 9, 0, 0, 5, 5, [(0,0)], [(60,1,0)],0])
        self.spawnlist.append([2100, 9, 1440, 0, -5, 5, [(0,0)], [(60,1,0)],0])
        self.spawnlist.append([2150, 9, 200, 0, 5, 5, [(0,0)], [(60,1,0)],0])
        self.spawnlist.append([2200, 9, 1240, 0, -5, 5, [(0,0)], [(60,1,0)],0])

        #deze cruiser komt snel binnen, remt af en gaat dan zigzaggen, na 8 seconden (480 ticks) strafed die het scherm uit.
        self.spawnlist.append([2450, 10, 300, 0, 0, 5, [(0, 0), (60, 3,0,0), (150,1), (480,2)], [(40,2,0)],800])

        #nog een paar verticaal vliegende tegenstanders
        self.spawnlist.append([2900, 9, 320, 0, 0, 7, [(0,0)], [(60,1,0)],200])
        self.spawnlist.append([2900, 9, 620, 0, 0, 7, [(0,0)], [(60,1,0)],200])
        self.spawnlist.append([3000, 9, 820, 0, 0, 7, [(0,0)], [(60,1,0)],200])
        self.spawnlist.append([3000, 9, 1120, 0, 0, 7, [(0,0)], [(60,1,0)],200])

        #bulltype unit die charged: komt scherm in, remt af, charged. Na charge gaat die naar achteren uit scherm.
        self.spawnlist.append([3200, 11, 320, 0, 0, 7, [(0,0), (40,3,0,0),(100,4),(178,3,0,-7)], [(100,3,1)],400])
        self.spawnlist.append([3300, 11, 320, 0, 0, 7, [(0, 0), (40, 3, 0, 0), (100, 4), (178, 3, 0, -7)], [(100, 3, 1)],400])

        #je kunt een schip ook meerdere wapensystemen geven, zoals aimed en forward
        self.spawnlist.append([3700, 10, 300, 0, 0, 5, [(0, 0), (60, 3, 0, 0), (150, 1), (480, 2)], [(10, 3, 0),[100,1,1]],800])

        #deze charged naar vooraf bepaalde locaties. Elke charge duurt 78 ticks. Het laatste programma is een strafe weg.
        self.spawnlist.append([4100, 11, 320, 0, 0, 7, [(0,0), (40,3,0,0),(100,4,1000,1000), (178,4,1300,300), (256,4,100,100), (334,2)], [(100,3,1)],400])

        #deze vliegen verticaal naar beneden met een voorwaarts zwaarder schot
        self.spawnlist.append([4600, 9, 320, 0, 0, 7, [(0,0)], [(50,3,1)],0])
        self.spawnlist.append([4620, 9, 620, 0, 0, 7, [(0,0)], [(50,3,1)],0])
        self.spawnlist.append([4640, 9, 820, 0, 0, 7, [(0,0)], [(50,3,1)],0])
        self.spawnlist.append([4660, 9, 1120, 0, 0, 7, [(0, 0)], [(50,3,1)],0])

        #deze eindbaas swingt een beetje heen en weer en schiet een cluster schot van 6 bullets met 10 graden ruimte tussen de bullets
        self.spawnlist.append([5200, 12, 320, 0, 0, 6, [(0, 0), (60, 3,0,0), (150,1)], [(100, 4, 0, 6, 15), (60,1,1)], 1000])

        self.spawnlist.append([5500, -1])

    def spawning(self):
        if len(self.spawnlist) > 0:
            if self.spawnlist[0][0] == self.ticks:
                if self.spawnlist[0][1] == -1:
                    print(len(Gamedata.mobs))
                    print(len(Gamedata.powerups))

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

