import random

import Mobs
import Gamedata
import Backgroundprops
import Gametext
import Sounds

windowheight = 1080
warscreenwidth = 1440


fighter = 9
cruiser = 10
marauder = 11
tyrant = 12
destroyer = 14
vulture = 15
lancer = 16
scorchbase = 17
scorchbuilding1 = 19
scorchbuilding2 = 26
scorchbuilding3 = 27
scorchbuilding4 = 28
dominator = 13
chimera1 = 20
chimera2 = 21
chimera3 = 22
alfa_drone = 29
alfa_disruptor = 30
alfa_transmutator = 31
alfa_assimilator = 32
alfa_guardian = 33
alfa_forcefield = 34
alfa_mine = 35
alfa_commandship_administrator = 36
bird_of_pray = 28

straightLine = 0
zigzag = 1
strafe = 2
changeDirection = 3
charge = 4

nowWeapon = 0
aimedShot = 1
machineGun = 2
forwardShot = 3
clusterShot = 4
flameThrower = 5

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
        mobslist = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,17,18,19,20,21,22,23, 24,25,26,27, 28]
        Mobs.images.load_level(mobslist)
        if Gamedata.player.levelnumber == 0:
            self.level_1()
        elif Gamedata.player.levelnumber == 1:
            self.level_2()
        elif Gamedata.player.levelnumber == 2:
            self.level_3()
        else:
            self.level_4()
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

            #9 = powerup level

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

        # manier om meteorstorm in te voegen.
        # eerste staat voor de startticks, wanneer komt de eerste meteor
        # tweede getal staat voor increment: hoeveel ticks zitten er tussen elke meteor
        # derde getal is het aantal meteoren dat de storm duurt.
        # meerdere meteorstorms per level is mogelijk.
        self.meteorstorm(100, 50, 200)

        # liedje starten is simpel: ticks + naam. Zorg dat de file staat in de musicfolder.
        # False = start direct, onderbreek huidige muziek, True betekend: speel af na huidige nummer.
        self.musiclist.append([0, '04. Cry.flac', False])
        self.musiclist.append([0, '07. Final Frontier.flac', True])

        # 0 ticks: aankondiging level text
        self.textlist.append([100, "Level 1: Jupiter", 30, (0, 150, 0), (160, 40), (warscreenwidth / 2, 100), (800, 50)])
        self.textlist.append([150, "WARNING: ASTERIOD STORM DETECTED", 30, (200, 0, 0), (100, 40), (warscreenwidth / 2, 150), (warscreenwidth, 50)])
        self.textlist.append([200, "WARNING: ENEMY SHIPS DETECTED", 30, (200, 0, 0), (100, 40), (warscreenwidth / 2, 200), (warscreenwidth, 50)])

        self.propslist.append([2000, 0, 900, 1, (540, 767)])
        self.propslist.append([2500, 1, 600, 2, (675, 675)])
        self.propslist.append([6000, 2, 200, 2, (518, 520)])
        self.propslist.append([10000, 3, 800, 1, (240, 97)])

        # fighters (horizontaal naar links)
        self.spawnlist.append([500, fighter, warscreenwidth, 200, -3, 0, [(0, straightLine)], [(100, forwardShot, 0)], 1])
        self.spawnlist.append([560, fighter, warscreenwidth, 200, -3, 0, [(0, straightLine)], [(100, forwardShot, 0)], 1])
        self.spawnlist.append([620, fighter, warscreenwidth, 200, -3, 0, [(0, straightLine)], [(100, forwardShot, 0)], 1])

        # fighters (verticaal)
        self.spawnlist.append([1000, fighter, 400, 0, 0, 3, [(0, straightLine)], [(100, forwardShot, 0)], 0])
        self.spawnlist.append([1060, fighter, 800, 0, 0, 3, [(0, straightLine)], [(100, forwardShot, 0)], 0])
        self.spawnlist.append([1120, fighter, 1200, 0, 0, 3, [(0, straightLine)], [(100, forwardShot, 0)], 2])

        # fighters (driveby shooting)
        self.spawnlist.append([1500, fighter, 0, 0, 2, 2, [(0, straightLine)], [(100, forwardShot, 0)], 2])
        self.spawnlist.append([1560, fighter, 1440, 0, -2, 2, [(0, straightLine)], [(100, forwardShot, 0)], 1])
        self.spawnlist.append([1520, fighter, 200, 0, 2, 2, [(0, straightLine)], [(100, forwardShot, 0)], 0])
        self.spawnlist.append([1580, fighter, 1240, 0, -2, 2, [(0, straightLine)], [(100, forwardShot, 0)], 1])

        # fighters (horizontaal naar rechts)
        self.spawnlist.append([2000, fighter, 0, 200, 3, 0, [(0, straightLine)], [(100, forwardShot, 0)], 3])
        self.spawnlist.append([2060, fighter, 0, 200, 3, 0, [(0, straightLine)], [(100, forwardShot, 0)], 0])
        self.spawnlist.append([2120, fighter, 0, 200, 3, 0, [(0, straightLine)], [(100, forwardShot, 0)], 1])
        self.spawnlist.append([2180, fighter, 0, 200, 3, 0, [(0, straightLine)], [(100, forwardShot, 0)], 0])

        # fighters (move, strafe)
        self.spawnlist.append([2500, fighter, 420, 0, 0, 2, [(0, straightLine), (40, strafe)], [(100, forwardShot, 0)], 1])
        self.spawnlist.append([2600, fighter, 720, 0, 0, 2, [(0, straightLine), (40, strafe)], [(100, forwardShot, 0)], 1])
        self.spawnlist.append([2700, fighter, 1020, 0, 0, 2, [(0, straightLine), (40, strafe)], [(100, forwardShot, 0)], 1])
        self.spawnlist.append([2800, fighter, 420, 0, 0, 2, [(0, straightLine), (40, strafe)], [(100, forwardShot, 0)], 1])
        self.spawnlist.append([2900, fighter, 720, 0, 0, 2, [(0, straightLine), (40, strafe)], [(100, forwardShot, 0)], 1])
        self.spawnlist.append([3000, fighter, 1020, 0, 0, 2, [(0, straightLine), (40, strafe)], [(100, forwardShot, 0)], 1])

        # vultures (move, slower)
        self.spawnlist.append([3300, vulture, 650, 0, 0, 2, [(0, straightLine), (40, changeDirection, 0, 1)], [(100, aimedShot, 0)], 2])
        self.spawnlist.append([3360, vulture, 300, 0, 0, 2, [(0, straightLine), (40, changeDirection, 0, 1)], [(100, aimedShot, 0)], 3])
        self.spawnlist.append([3420, vulture, 850, 0, 0, 2, [(0, straightLine), (40, changeDirection, 0, 1)], [(100, aimedShot, 0)], 2])

        # destroyer komt in scherm en trek na een tijdje terug
        self.spawnlist.append([3900, destroyer, warscreenwidth/2, 0, 0, 2, [(0, straightLine), (300, 0, -1)], [(100, 4, 0, 4, 20)], 5])

        # fighters (move, strafe)
        # en vultures (move, slower)
        self.spawnlist.append([4700, fighter, 100, 0, 0, 3, [(0, 0), (40, 2)], [(100, 3, 0)], 0])
        self.spawnlist.append([4800, fighter, 500, 0, 0, 3, [(0, 0), (40, 2)], [(100, 3, 0)], 0])
        self.spawnlist.append([4950, vulture, 650, 0, 0, 1, [(0, 0), (40, 3, 0, 1), (0, 0), (0, 0, 0, 0)], [(100, 1, 0)], 2])
        self.spawnlist.append([4950, fighter, 800, 0, 0, 3, [(0, 0), (40, 2)], [(100, 3, 0)], 0])
        self.spawnlist.append([5100, vulture, 75, 0, 0, 1, [(0, 0), (40, 3, 0, 1), (0, 0), (0, 0, 0, 0)], [(100, 1, 0)], 2])
        self.spawnlist.append([5100, fighter, 250, 0, 0, 3, [(0, 0), (40, 2)], [(100, 3, 0)], 0])
        self.spawnlist.append([5250, vulture, 1350, 0, 0, 1, [(0, 0), (40, 3, 0, 1), (0, 0), (0, 0, 0, 0)], [(100, 1, 0)], 2])
        self.spawnlist.append([5250, fighter, 1000, 0, 0, 3, [(0, 0), (40, 2)], [(100, 3, 0)], 0])

        # fighters (horizontaal naar rechts)
        self.spawnlist.append([5700, fighter, 0, 100, 3, 0, [(0, 0)], [(100, 3, 0)], 1])
        self.spawnlist.append([5800, fighter, 0, 150, 3, 0, [(0, 0)], [(100, 3, 0)], 0])
        self.spawnlist.append([5900, fighter, 0, 100, 3, 0, [(0, 0)], [(100, 3, 0)], 1])
        self.spawnlist.append([6000, fighter, 0, 150, 3, 0, [(0, 0)], [(100, 3, 0)], 0])

        # fighters (move, stop, change direction)
        self.spawnlist.append([6300, fighter, 75, 0, 0, 2, [(0, 0), (60, 3, 0, 0), (150, 3, 3, 3)], [(100, 3, 0)], 1])
        self.spawnlist.append([6350, fighter, 275, 0, 0, 2, [(0, 0), (60, 3, 0, 0), (130, 3, 3, 3)], [(100, 3, 0)], 1])
        self.spawnlist.append([6380, fighter, 175, 0, 0, 2, [(0, 0), (60, 3, 0, 0), (120, 3, 3, 3)], [(100, 3, 0)], 1])
        self.spawnlist.append([6460, fighter, 1200, 0, 0, 2, [(0, 0), (60, 3, 0, 0), (150, 3, -3, 4)], [(100, 3, 0)], 1])
        self.spawnlist.append([6500, fighter, 1000, 0, 0, 2, [(0, 0), (60, 3, 0, 0), (130, 3, -3, 4)], [(100, 3, 0)], 1])
        self.spawnlist.append([6530, fighter, 1100, 0, 0, 2, [(0, 0), (60, 3, 0, 0), (120, 3, -3, 4)], [(100, 3, 0)], 1])

        # cruiser (zigzag strafing)
        self.spawnlist.append([6800, cruiser, 650, 0, 0, 1, [(0, straightLine), (250, zigzag)], [(150, machineGun, 0)], 7])

        # fighters (driveby)
        # en fighters (driveby)
        self.spawnlist.append([7500, fighter, 0, 0, 1, 1, [(0, 0)], [(100, 3, 0)], 0])
        self.spawnlist.append([7530, fighter, 1440, 0, -1, 1, [(0, 0)], [(100, 3, 0)], 1])
        self.spawnlist.append([7560, fighter, 200, 0, 1, 1, [(0, 0)], [(100, 3, 0)], 0])
        self.spawnlist.append([7590, fighter, 1200, 0, -1, 1, [(0, 0)], [(100, 3, 0)], 1])
        self.spawnlist.append([7620, fighter, 250, 0, 1, 1, [(0, 0)], [(100, 3, 0)], 0])
        self.spawnlist.append([7650, fighter, 1100, 0, -1, 1, [(0, 0)], [(100, 3, 0)], 1])

        # fighters (zigzag strafing)
        self.spawnlist.append([8100, fighter, 1300, 0, 0, 1, [(0, 1), (0, 0)], [(100, 3, 0)], 3])
        self.spawnlist.append([8150, fighter, 25, 0, 0, 1, [(0, 1), (0, 0)], [(100, 3, 0)], 3])
        self.spawnlist.append([8190, fighter, 300, 0, 0, 1, [(0, 1), (0, 0)], [(100, 3, 0)], 2])
        self.spawnlist.append([8260, fighter, 0, 0, 0, 1, [(0, 1), (0, 0)], [(100, 3, 0)], 2])
        self.spawnlist.append([8300, fighter, 1150, 0, 0, 1, [(0, 1), (0, 0)], [(100, 3, 0)], 1])
        self.spawnlist.append([8400, fighter, 750, 0, 0, 1, [(0, 1), (0, 0)], [(100, 3, 0)], 1])

        # destroyer (move, slower)
        # en fighters (move, slower)
        self.spawnlist.append([8800, fighter, 800, 0, 0, 2, [(0, 0), (100, 3, 0, 1)], [(150, 3, 0)], 1])
        self.spawnlist.append([8860, destroyer, 800, 0, 0, 1, [(0, 0), (250, 3, 0,1)], [(100, clusterShot, 0, 4, 20)], 7])
        self.spawnlist.append([8890, fighter, 600, 0, 0, 2, [(0, 0), (90, 3, 0, 1)], [(150, 3, 0)], 1])
        self.spawnlist.append([8910, fighter, 1000, 0, 0, 2, [(0, 0), (90, 3, 0, 1)], [(150, 3, 0)], 1])
        self.spawnlist.append([8940, fighter, 600, 0, 0, 2, [(0, 0), (30, 3, 0, 1)], [(150, 3, 0)], 2])
        self.spawnlist.append([8950, fighter, 1000, 0, 0, 2, [(0, 0), (30, 3, 0, 1)], [(150, 3, 0)], 2])

        # en vultures (horizontaal naar links)
        self.spawnlist.append([9500, vulture, warscreenwidth, 200, -1, 0, [(0, 0)], [(100, 1, 0)], 2])
        self.spawnlist.append([9700, vulture, warscreenwidth, 200, -1, 0, [(0, 0)], [(100, 1, 0)], 3])
        self.spawnlist.append([9900, vulture, warscreenwidth, 200, -1, 0, [(0, 0)], [(100, 1, 0)], 4])

        # fighters (move, stop, strafe)
        self.spawnlist.append([10400, fighter, 175, 0, 0, 2, [(0, straightLine), (30, 0, 0, 0), (150, strafe)], [(100, 3, 0)], 0])
        self.spawnlist.append([10420, fighter, 250, 0, 0, 2, [(0, straightLine), (60, 0, 0, 0), (160, strafe)], [(100, 3, 0)], 1])
        self.spawnlist.append([10440, fighter, 50, 0, 0, 2, [(0, straightLine), (40, 0, 0, 0), (175, strafe)], [(100, 3, 0)], 2])
        self.spawnlist.append([10455, fighter, 350, 0, 0, 2, [(0, straightLine), (50, 0, 0, 0), (175, strafe)], [(100, 3, 0)], 3])

        # cruisers (zigzag strafing)
        self.spawnlist.append([10700, cruiser, 1100, 0, 0, 1, [(0, 0), (200, 1)], [(150, machineGun, 0)], 7])
        self.spawnlist.append([11200, cruiser, 100, 0, 0, 1, [(0, 0), (300, 1)], [(150, machineGun, 0)], 7])

        # marauder (move, stop, charge, retreat)
        self.spawnlist.append([12000, marauder, 950, 0, 0, 4, [(0, 0), (40, 3, 0, 0), (100, 4), (178, 3, 0, -7)], [(100, 2, 0)], 6])

        self.textlist.append([12300, "WARNING: LARGE ENEMY SHIP DETECTED", 30, (200, 0, 0), (100, 40), (warscreenwidth / 2, 100),(warscreenwidth, 50)])
        self.textlist.append([12600, "SCANNING...", 30, (255, 255, 255), (100, 40), (warscreenwidth / 2, 50), (warscreenwidth, 100)])
        self.textlist.append([12800, "SCORCH COMMAND SHIP: TYRANT", 30, (255, 255, 255), (100, 40), (warscreenwidth / 2, 100),(warscreenwidth, 50)])

        # aankondiging + eindbaas: Tyrant (zigzag)
        self.spawnlist.append([13000, 12, 320, 0, 0, 6,
                               [(0, 0), (60, 3, 0, 0), (150, 1), (600, 4), (756, 1), (1226, 4), (1382, 1), (1832, 4),
                                (1988, 1)],
                               [((50, 50, 620), 4, 0, 6, 15), ((20, 776, 1226), 1, 1), ((50, 1382, 1832), 4, 0, 6, 15),
                                ((50, 1988, 99999), 2, 0), ((100, 2100, 99999), 4, 0, 6, 20)], 10])

        # level end
        self.spawnlist.append([13000, -1])

        ###################################################################################################

    def level_2(self):
        Gamedata.bgimages = Backgroundprops.Images([])

        # TEXT
        # 1 ticks
        # 2 text
        # 3 fontsize
        # 4 RGB color code
        # 5 (ticks fully visable, ticks fadeout)
        # 6 centeredposition (x,y)
        # 7 grote van het plaatje (hoe meer en hoe groter de text, hoe groter het plaatje moet zijn. Anders wordt de text afgeknipt.
        self.textlist.append([100, "Level 2: Scorch base", 30, (0, 150, 0), (160, 40), (warscreenwidth / 2, 100), (800, 50)])
        self.textlist.append([200, "Approaching Scorch base, heavy resistance ahead...", 30, (200, 0, 0), (150, 40), (warscreenwidth / 2, 150), (warscreenwidth, 50)])

        self.spawnlist.append([100, alfa_drone, 250, 0, 0, 1, [(0, 0), (0, 0)], [(0, 0, 0)], 1])
        self.spawnlist.append([0, alfa_disruptor, 400, 0, 0, 1, [(0, 0), (0, 0)], [(0, 0, 0)], 1])
        self.spawnlist.append([0, alfa_transmutator, 600, 0, 0, 1, [(0, 0), (0, 0)], [(0, 0, 0)], 1])
        self.spawnlist.append([0, alfa_assimilator, 800, 0, 0, 1, [(0, 0), (0, 0)], [(0, 0, 0)], 1])
        self.spawnlist.append([0, alfa_guardian, 1000, 0, 0, 1, [(0, 0), (0, 0)], [(0, 0, 0)], 1])
        self.spawnlist.append([0, alfa_forcefield, 250, 0, 0, 1, [(0, 0), (0, 0)], [(0, 0, 0)], 1])
        self.spawnlist.append([0, alfa_mine, 1200, 0, 0, 1, [(0, 0), (0, 0)], [(0, 0, 0)], 1])
        self.spawnlist.append([500, alfa_commandship_administrator, 700, 0, 0, 1, [(0, 0), (0, 0)], [(0, 0, 0)], 1])

        # Goede oude fighters kapot knallen.
        #      self.spawnlist.append([350, fighter, 420, 0, 0, 2, [(0, 0), (40, 2)], [(100, 3, 0)], 0])
        #      self.spawnlist.append([400, fighter, 720, 0, 0, 2, [(0, 0), (40, 2)], [(100, 3, 0)], 0])
        #      self.spawnlist.append([450, fighter, 1020, 0, 0, 2, [(0, 0), (40, 2)], [(100, 3, 0)], 0])
        #      self.spawnlist.append([500, fighter, 420, 0, 0, 2, [(0, 0), (40, 2)], [(100, 3, 0)], 0])
        #      self.spawnlist.append([550, fighter, 720, 0, 0, 2, [(0, 0), (40, 2)], [(100, 3, 0)], 0])
        #      self.spawnlist.append([600, fighter, 1020, 0, 0, 2, [(0, 0), (40, 2)], [(100, 3, 0)], 0])
        #      self.spawnlist.append([650, fighter, 420, 0, 0, 2, [(0, 0), (40, 2)], [(100, 3, 0)],0])
        #      self.spawnlist.append([700, fighter, 720, 0, 0, 2, [(0, 0), (40, 2)], [(100, 3, 0)], 0])
        #      self.spawnlist.append([750, fighter, 1020, 0, 0, 2, [(0, 0), (40, 2)], [(100, 3, 0)], 0])
        #      self.spawnlist.append([800, fighter, 420, 0, 0, 2, [(0, 0), (40, 2)], [(100, 3, 0)], 0])
        #      self.spawnlist.append([850, fighter, 720, 0, 0, 2, [(0, 0), (40, 2)], [(100, 3, 0)], 0])
        #      self.spawnlist.append([900, fighter, 1020, 0, 0, 2, [(0, 0), (40, 2)], [(100, 3, 0)], 0])

        #      self.spawnlist.append([925, scorchbuilding1, 800, 0, 0, 1, [(0, 0), (0, 0)], [(0, 0, 0)], 1])
        #      self.spawnlist.append([950, scorchbase, 300, 0, 0, 1, [(0, 0), (0, 0)], [(0, 0, 0)], 2])
        #      self.spawnlist.append([975, scorchbuilding1, 1200, 0, 0, 1, [(0, 0), (0, 0)], [(0, 0, 0)], 1])
        #      self.spawnlist.append([1000, scorchbuilding2, 400, 0, 0, 1, [(0, 0), (0, 0)], [(0, 0, 0)], 1])
        #      self.spawnlist.append([1200, scorchbuilding3, 75, 0, 0, 1, [(0, 0), (0, 0)], [(0, 0, 0)], 1])
        #      self.spawnlist.append([1400, scorchbuilding3, 1100, 0, 0, 1, [(0, 0), (0, 0)], [(0, 0, 0)], 1])
        #      self.spawnlist.append([1450, scorchbuilding1, 900, 0, 0, 1, [(0, 0), (0, 0)], [(0, 0, 0)], 1])
        #      self.spawnlist.append([1650, scorchbuilding4, 1300, 0, 0, 1, [(0, 0), (0, 0)], [(0, 0, 0)], 1])

        self.spawnlist.append([1000, fighter, -50, 200, 5, 0, [(0, straightLine), (30, changeDirection, 0, 1)], [(100, forwardShot, 0)], 0])
        #   self.spawnlist.append([1025, fighter, 1500, 170, -5, 0, [(0, straightLine), (30, changeDirection, 0, 1)], [(100, forwardShot, 0)],0])
        self.spawnlist.append([1050, fighter, -50, 200, 5, 0, [(0, straightLine), (60, changeDirection, 0, 1)], [(100, forwardShot, 0)], 0])
        self.spawnlist.append([1075, fighter, 1500, 170, -5, 0, [(0, straightLine), (60, changeDirection, 0, 1)], [(100, forwardShot, 0)], 0])
        self.spawnlist.append([1100, fighter, 1500, 200, 5, 0, [(0, straightLine), (60, changeDirection, 0, 1)], [(100, forwardShot, 0)], 0])
        self.spawnlist.append([1100, vulture, 1500, 50, -3, 0, [(0, straightLine), (120, changeDirection, 0, 1)], [(100, aimedShot, 0)], 2])
        #   self.spawnlist.append([1125, fighter, 1500, 170, -5, 0, [(0, straightLine), (90, changeDirection, 0, 1)], [(100, forwardShot, 0)],0])
        self.spawnlist.append([1125, vulture, 1500, 50, -4, 0, [(0, straightLine), (200, changeDirection, 0, 1)], [(100, aimedShot, 0)], 2])
        #    self.spawnlist.append([1125, fighter, -100, 1000, 8, -8, [(0, 0), (0, 0)], [(0, 0, 0)], 1])
        #    self.spawnlist.append([1125, fighter, -150, 1100, 8, -8, [(0, 0), (0, 0)], [(0, 0, 0)], 1])
        #    self.spawnlist.append([1140, fighter, -130, 1050, 8, -8, [(0, 0), (0, 0)], [(0, 0, 0)], 1])
        #    self.spawnlist.append([1200, fighter, -50, 200, 5, 0, [(0, straightLine), (90, changeDirection, 0, 1)], [(100, forwardShot, 0)], 0])
        self.spawnlist.append([1300, fighter, 1500, 150, -8, 0, [(0, straightLine), (90, changeDirection, 0, 1)], [(100, forwardShot, 0)], 0])
        #  self.spawnlist.append([1350, vulture, -130, 1050, 6, -6, [(0, 0), (0, 0)], [(100, aimedShot, 0)], 2])
        # self.spawnlist.append([1450, fighter, 1200, 1050, 0, -8, [(0, 0), (0, 0)], [(0, 0, 0)], 1])
        self.spawnlist.append([1500, vulture, 200, 0, 0, 2, [(100, strafe), (0, 0)], [(100, aimedShot, 0)], 2])
        self.spawnlist.append([1525, fighter, -50, 100, 5, 0, [(0, straightLine), (80, changeDirection, 0, 1)], [(100, forwardShot, 0)], 0])
        #  self.spawnlist.append([1550, fighter, -50, 200, 5, 0, [(0, straightLine), (100, changeDirection, 0, 1)], [(100, forwardShot, 0)], 0])
        self.spawnlist.append([1600, fighter, -50, 100, 5, 0, [(0, straightLine), (160, changeDirection, 0, 1)], [(100, forwardShot, 0)], 0])
        self.spawnlist.append([1650, vulture, 1000, 0, 0, 1, [(0, straightLine), (200, strafe)], [(100, aimedShot, 0)], 2])
        self.spawnlist.append([1850, cruiser, -150, 1100, 1, -1, [(0, 0), (0, 0)], [(50, machineGun, 0)], 6])
        #    self.spawnlist.append([1800, fighter, -50, 250, 6, 0, [(0, straightLine), (160, changeDirection, 0, 1)], [(100, forwardShot, 0)],0])
        self.spawnlist.append([1825, fighter, -50, 200, 6, 0, [(0, straightLine), (130, changeDirection, 0, 1)], [(100, forwardShot, 0)], 0])
        self.spawnlist.append([1850, fighter, -50, 180, 6, 0, [(0, straightLine), (90, changeDirection, 0, 1)], [(100, forwardShot, 0)], 0])

        self.spawnlist.append([1800, scorchbuilding4, 100, 0, 0, 1, [(0, 0), (0, 0)], [(0, 0, 0)], 1])
        self.spawnlist.append([1850, scorchbuilding2, 500, 0, 0, 1, [(0, 0), (0, 0)], [(0, 0, 0)], 1])
        self.spawnlist.append([1900, scorchbuilding1, 300, 0, 0, 1, [(0, 0), (0, 0)], [(0, 0, 0)], 1])
        self.spawnlist.append([2000, scorchbuilding1, 1300, 0, 0, 1, [(0, 0), (0, 0)], [(0, 0, 0)], 1])

        # Shit get's real met lancers en destroyers.
        self.spawnlist.append([2200, destroyer, 150, 0, 3, 1, [(0, 0), (300, 3, 0, 4)], [(100, 4, 0, 4, 20)], 5])
        self.spawnlist.append([2650, lancer, warscreenwidth, 500, -10, -1, [(0, 0), (90, 3, 0, -2), (160, 2)], [((25, 0, 100), 3, 1), ((60, 100, 99999), 4, 1, 4, 15)], 9])

        self.spawnlist.append([2400, scorchbuilding3, 600, 0, 0, 1, [(0, 0), (0, 0)], [(0, 0, 0)], 1])
        self.spawnlist.append([2500, scorchbase, warscreenwidth / 2, 0, 0, 1, [(0, 0), (0, 0)], [(0, 0, 0)], 3])
        self.spawnlist.append([2600, scorchbuilding1, 100, 0, 0, 1, [(0, 0), (0, 0)], [(0, 0, 0)], 1])
        self.spawnlist.append([2600, scorchbuilding1, 1000, 0, 0, 1, [(0, 0), (0, 0)], [(0, 0, 0)], 1])

        # Marauders
        self.spawnlist.append([3000, marauder, 100, 0, 0, 3, [(0, 0), (40, 3, 0, 0), (100, 4), (178, 3, 0, -7)], [(100, 2, 0)], 5])
        #    self.spawnlist.append([3200, marauder, 1340, 0, 0, 3, [(0, 0), (40, 3, 0, 0), (100, 4), (178, 3, 0, -7)], [(100, 2, 0)], 6])

        self.spawnlist.append([3050, scorchbuilding2, 600, 0, 0, 1, [(0, 0), (0, 0)], [(0, 0, 0)], 1])
        self.spawnlist.append([3100, scorchbase, 1000, 0, 0, 1, [(0, 0), (0, 0)], [(0, 0, 0)], 4])
        self.spawnlist.append([3150, scorchbuilding3, 400, 0, 0, 1, [(0, 0), (0, 0)], [(0, 0, 0)], 1])

        # Vultures en een cruiser die van de onderkant komt.
        #      self.spawnlist.append([3500, vulture, 1440, 300, -5, 0, [(0, 0), (300, 3, 0, 1)], [(100, 1, 0)], 0])
        self.spawnlist.append([3550, vulture, 0, 300, 5, 0, [(0, 0), (250, 3, 0, 1)], [(100, 1, 0)], 0])
        self.spawnlist.append([3600, vulture, 1440, 300, -5, 0, [(0, 0), (200, 3, 0, 1)], [(100, 1, 0)], 0])
        self.spawnlist.append([3600, cruiser, 400, 1355, 0, -6, [(0, 0), (130, 3, 0, 1), (250, 1)], [(150, 2, 0)], 7])
        self.spawnlist.append([3650, vulture, 0, 300, 5, 0, [(0, 0), (150, 3, 0, 1)], [(100, 1, 0)], 0])
        self.spawnlist.append([3700, vulture, 1440, 300, -5, 0, [(0, 0), (100, 3, 0, 1)], [(100, 1, 0)], 0])
        #       self.spawnlist.append([3750, vulture, 0, 300, 5, 0, [(0, 0), (50, 3, 0, 1),], [(100, 1, 0)], 0])

        self.spawnlist.append([3500, scorchbuilding1, 1200, 0, 0, 1, [(0, 0), (0, 0)], [(0, 0, 0)], 1])
        self.spawnlist.append([3600, scorchbuilding1, 400, 0, 0, 1, [(0, 0), (0, 0)], [(0, 0, 0)], 1])
        self.spawnlist.append([3700, scorchbuilding1, 1000, 0, 0, 1, [(0, 0), (0, 0)], [(0, 0, 0)], 1])
        self.spawnlist.append([3800, scorchbuilding2, 500, 0, 0, 1, [(0, 0), (0, 0)], [(0, 0, 0)], 1])

        # zware wave met vultures en lancers
        self.spawnlist.append([4200, lancer, 0, 150, 10, -1, [(0, 0), (10, 3, 0, 1)], [((25, 0, 100), 3, 1), ((60, 100, 99999), 4, 1, 4, 15)], 9])
        self.spawnlist.append([4300, vulture, 1240, 0, 0, 2, [(0, 0), (300, 3, 0, 1)], [(100, 1, 0)], 0])
        self.spawnlist.append([4300, vulture, 200, 0, 0, 2, [(0, 0), (250, 3, 0, 1)], [(100, 1, 0)], 0])

        # Fighters als kanonvoer
        self.spawnlist.append([4610, fighter, 720, 0, 0, 2, [(0, 0), (40, 2)], [(100, 3, 0)], 1])
        self.spawnlist.append([4640, fighter, 1020, 0, 0, 2, [(0, 0), (40, 2)], [(100, 3, 0)], 1])
        self.spawnlist.append([4670, fighter, 420, 0, 0, 2, [(0, 0), (40, 2)], [(100, 3, 0)], 1])
        self.spawnlist.append([4700, fighter, 720, 0, 0, 2, [(0, 0), (40, 2)], [(100, 3, 0)], 1])
        self.spawnlist.append([4730, fighter, 1020, 0, 0, 2, [(0, 0), (40, 2)], [(100, 3, 0)], 1])
        self.spawnlist.append([4760, fighter, 420, 0, 0, 2, [(0, 0), (40, 2)], [(100, 3, 0)], 1])
        self.spawnlist.append([4790, fighter, 720, 0, 0, 2, [(0, 0), (40, 2)], [(100, 3, 0)], 1])
        self.spawnlist.append([4820, fighter, 1020, 0, 0, 2, [(0, 0), (40, 2)], [(100, 3, 0)], 1])
        self.spawnlist.append([4850, fighter, 420, 0, 0, 2, [(0, 0), (40, 2)], [(100, 3, 0)], 1])
        self.spawnlist.append([4880, fighter, 720, 0, 0, 2, [(0, 0), (40, 2)], [(100, 3, 0)], 1])
        self.spawnlist.append([4910, fighter, 1020, 0, 0, 2, [(0, 0), (40, 2)], [(100, 3, 0)], 1])
        self.spawnlist.append([4940, fighter, 420, 0, 0, 2, [(0, 0), (40, 2)], [(100, 3, 0)], 1])
        self.spawnlist.append([4970, fighter, 720, 0, 0, 2, [(0, 0), (40, 2)], [(100, 3, 0)], 1])
        self.spawnlist.append([5000, fighter, 1020, 0, 0, 2, [(0, 0), (40, 2)], [(100, 3, 0)], 1])
        self.spawnlist.append([5030, fighter, 420, 0, 0, 2, [(0, 0), (40, 2)], [(100, 3, 0)], 1])
        self.spawnlist.append([5060, fighter, 720, 0, 0, 2, [(0, 0), (40, 2)], [(100, 3, 0)], 1])
        self.spawnlist.append([5090, fighter, 1020, 0, 0, 2, [(0, 0), (40, 2)], [(100, 3, 0)], 1])
        self.spawnlist.append([5120, fighter, 420, 0, 0, 2, [(0, 0), (40, 2)], [(100, 3, 0)], 1])
        self.spawnlist.append([5150, fighter, 720, 0, 0, 2, [(0, 0), (40, 2)], [(100, 3, 0)], 1])
        self.spawnlist.append([5180, fighter, 1020, 0, 0, 2, [(0, 0), (40, 2)], [(100, 3, 0)], 1])
        self.spawnlist.append([5210, fighter, 420, 0, 0, 2, [(0, 0), (40, 2)], [(100, 3, 0)], 1])
        self.spawnlist.append([5250, fighter, 720, 0, 0, 2, [(0, 0), (40, 2)], [(100, 3, 0)], 1])
        self.spawnlist.append([5280, fighter, 1020, 0, 0, 2, [(0, 0), (40, 2)], [(100, 3, 0)], 1])
        self.spawnlist.append([5310, fighter, 420, 0, 0, 2, [(0, 0), (40, 2)], [(100, 3, 0)], 1])

        self.spawnlist.append([4500, scorchbuilding3, 800, 0, 0, 1, [(0, 0), (0, 0)], [(0, 0, 0)], 1])
        self.spawnlist.append([4550, scorchbuilding3, 600, 0, 0, 1, [(0, 0), (0, 0)], [(0, 0, 0)], 1])
        self.spawnlist.append([4600, scorchbuilding1, 400, 0, 0, 1, [(0, 0), (0, 0)], [(0, 0, 0)], 1])
        self.spawnlist.append([4650, scorchbuilding2, 1000, 0, 0, 1, [(0, 0), (0, 0)], [(0, 0, 0)], 1])
        self.spawnlist.append([4700, scorchbuilding2, 300, 0, 0, 1, [(0, 0), (0, 0)], [(0, 0, 0)], 1])
        self.spawnlist.append([4750, scorchbuilding4, 800, 0, 0, 1, [(0, 0), (0, 0)], [(0, 0, 0)], 1])

        # cruisers zigzaggend
        self.spawnlist.append([5700, cruiser, 100, 0, 0, 1, [(0, 0), (200, 1)], [(150, 2, 0)], 6])
        self.spawnlist.append([5900, cruiser, 1100, 0, 0, 1, [(0, 0), (200, 1)], [(150, 2, 0)], 6])
        self.spawnlist.append([6100, cruiser, warscreenwidth / 2, 0, 0, 1, [(0, 0), (200, 1)], [(40, 2, 0)], 7])

        self.spawnlist.append([6400, scorchbuilding1, 750, 0, 0, 1, [(0, 0), (0, 0)], [(0, 0, 0)], 1])
        self.spawnlist.append([6450, scorchbuilding1, 450, 0, 0, 1, [(0, 0), (0, 0)], [(0, 0, 0)], 1])
        self.spawnlist.append([6500, scorchbase, 1200, 0, 0, 1, [(0, 0), (0, 0)], [(0, 0, 0)], 5])
        self.spawnlist.append([6550, scorchbuilding4, 800, 0, 0, 1, [(0, 0), (0, 0)], [(0, 0, 0)], 1])
        self.spawnlist.append([6600, scorchbuilding2, 800, 0, 0, 1, [(0, 0), (0, 0)], [(0, 0, 0)], 1])

        # destroyers (naar rechts)
        self.spawnlist.append([6800, destroyer, -50, 200, 2, 0, [(0, 0), ], [(100, 4, 0, 4, 20)], 4])
        self.spawnlist.append([6950, destroyer, -50, 200, 2, 0, [(0, 0), ], [(100, 4, 0, 4, 20)], 5])
        self.spawnlist.append([7100, destroyer, -50, 200, 2, 0, [(0, 0), ], [(100, 4, 0, 4, 20)], 6])

        self.spawnlist.append([7350, scorchbuilding3, 850, 0, 0, 1, [(0, 0), (0, 0)], [(0, 0, 0)], 1])
        self.spawnlist.append([7400, scorchbuilding2, 650, 0, 0, 1, [(0, 0), (0, 0)], [(0, 0, 0)], 1])
        self.spawnlist.append([7500, scorchbuilding1, 200, 0, 0, 1, [(0, 0), (0, 0)], [(0, 0, 0)], 1])
        self.spawnlist.append([7600, scorchbuilding1, 500, 0, 0, 1, [(0, 0), (0, 0)], [(0, 0, 0)], 1])

        # legertje fighters en vultures
        self.spawnlist.append([7700, fighter, 200, 0, 0, 2, [(0, 0), (40, strafe)], [(100, 3, 0)], 0])
        self.spawnlist.append([7750, fighter, 800, 0, 0, 2, [(0, 0), (40, strafe)], [(100, 3, 0)], 0])
        self.spawnlist.append([7800, fighter, 1000, 0, 0, 2, [(0, 0), (40, strafe)], [(100, 3, 0)], 0])
        self.spawnlist.append([7850, vulture, 500, 0, 0, 2, [(0, 0), (50, strafe), ], [(100, 1, 0)], 1])
        self.spawnlist.append([7900, fighter, 400, 0, 0, 2, [(0, 0), (40, strafe)], [(100, 3, 0)], 1])
        self.spawnlist.append([7950, fighter, 700, 0, 0, 2, [(0, 0), (40, strafe)], [(100, 3, 0)], 1])
        self.spawnlist.append([8000, fighter, 1000, 0, 0, 2, [(0, 0), (40, strafe)], [(100, 3, 0)], 2])
        self.spawnlist.append([8050, vulture, 200, 0, 0, 2, [(0, 0), (50, strafe), ], [(100, 1, 0)], 2])
        self.spawnlist.append([8100, fighter, 400, 0, 0, 2, [(0, 0), (40, strafe)], [(100, 3, 0)], 2])
        self.spawnlist.append([8150, fighter, 1000, 0, 0, 2, [(0, 0), (40, strafe)], [(100, 3, 0)], 3])
        self.spawnlist.append([8200, fighter, 700, 0, 0, 2, [(0, 0), (40, strafe)], [(100, 3, 0)], 3])
        self.spawnlist.append([8250, vulture, 1000, 0, 0, 2, [(0, 0), (50, strafe), ], [(100, 1, 0)], 3])
        self.spawnlist.append([8300, fighter, 200, 0, 0, 2, [(0, 0), (40, strafe)], [(100, 3, 0)], 4])
        self.spawnlist.append([8350, fighter, 500, 0, 0, 2, [(0, 0), (40, strafe)], [(100, 3, 0)], 4])
        self.spawnlist.append([8400, fighter, 700, 0, 0, 2, [(0, 0), (40, strafe)], [(100, 3, 0)], 4])

        # lancers die rechts en links in het scherm schieten en daarna weer weg gaan
        self.spawnlist.append([8800, lancer, warscreenwidth, 100, -15, 0, [(100, changeDirection, 0, 10), (50, changeDirection, 10, 0)], [((25, aimedShot, 100), 3, 1), ((60, 100, 99999), 4, 1, 4, 15)], 9])
        self.spawnlist.append([9100, lancer, 0, 150, 15, 0, [(100, changeDirection, 0, 10), (50, changeDirection, -10, 0)], [((25, aimedShot, 100), 3, 1), ((60, 100, 99999), 4, 1, 4, 15)], 9])

        # dominator
        # en fighters
        self.spawnlist.append([9500, dominator, 150, 0, 0, 2, [(0, 0), (100, zigzag)], [(100, machineGun, 0), (150, aimedShot, 1)], 5])
        self.spawnlist.append([9800, fighter, 1100, 0, 0, 2, [(0, 0), (0, 0)], [(100, forwardShot, 0)], 1])
        self.spawnlist.append([9850, fighter, 1150, 0, 0, 2, [(0, 0), (0, 0)], [(100, forwardShot, 0)], 1])
        self.spawnlist.append([9900, fighter, 1200, 0, 0, 2, [(0, 0), (0, 0)], [(100, forwardShot, 0)], 1])
        self.spawnlist.append([9950, fighter, 1250, 0, 0, 2, [(0, 0), (0, 0)], [(100, forwardShot, 0)], 1])
        self.spawnlist.append([10000, fighter, 1300, 0, 0, 2, [(0, 0), (0, 0)], [(100, forwardShot, 0)], 1])
        self.spawnlist.append([10050, fighter, 1250, 0, 0, 2, [(0, 0), (0, 0)], [(100, forwardShot, 0)], 1])
        self.spawnlist.append([10100, fighter, 1200, 0, 0, 2, [(0, 0), (0, 0)], [(100, forwardShot, 0)], 1])
        self.spawnlist.append([10150, fighter, 1150, 0, 0, 2, [(0, 0), (0, 0)], [(100, forwardShot, 0)], 1])
        self.spawnlist.append([10200, fighter, 1100, 0, 0, 2, [(0, 0), (0, 0)], [(100, forwardShot, 0)], 1])
        self.spawnlist.append([10250, fighter, 1150, 0, 0, 2, [(0, 0), (100, strafe)], [(100, forwardShot, 0)], 1])
        self.spawnlist.append([10300, fighter, 1200, 0, 0, 2, [(0, 0), (90, strafe)], [(100, forwardShot, 0)], 1])
        self.spawnlist.append([10350, fighter, 1250, 0, 0, 2, [(0, 0), (80, strafe)], [(100, forwardShot, 0)], 1])

        self.spawnlist.append([9800, scorchbuilding4, 50, 0, 0, 1, [(0, 0), (0, 0)], [(0, 0, 0)], 1])
        self.spawnlist.append([9900, scorchbase, 300, 0, 0, 1, [(0, 0), (0, 0)], [(0, 0, 0)], 6])
        self.spawnlist.append([10000, scorchbuilding2, 50, 0, 0, 1, [(0, 0), (0, 0)], [(0, 0, 0)], 1])
        self.spawnlist.append([10000, scorchbuilding3, 400, 0, 0, 1, [(0, 0), (0, 0)], [(0, 0, 0)], 1])
        self.spawnlist.append([10100, scorchbuilding1, 200, 0, 0, 1, [(0, 0), (0, 0)], [(0, 0, 0)], 1])

        # zware wave met dominators
        self.spawnlist.append([10600, dominator, 1100, 0, 0, 1, [(0, 0), (50, zigzag)], [(100, machineGun, 0), (150, aimedShot, 1)], 4])
        self.spawnlist.append([10700, dominator, 900, 0, 0, 2, [(0, 0), (50, zigzag)], [(100, machineGun, 0), (150, aimedShot, 1)], 5])
        self.spawnlist.append([10900, dominator, 200, 0, 0, 2, [(0, 0), (50, zigzag)], [(100, machineGun, 0), (150, aimedShot, 1)], 6])

        # lancer met fighters
        self.spawnlist.append([11400, lancer, 700, 0, 0, 1, [(0, 0), (0, 0)], [((25, aimedShot, 100), 3, 1), ((60, 100, 99999), 4, 1, 4, 15)], 9])
        self.spawnlist.append([11400, fighter, 600, 0, 0, 2, [(0, 0), (150, strafe)], [(150, forwardShot, 0)], 3])
        self.spawnlist.append([11400, fighter, 700, 0, 0, 2, [(0, 0), (150, strafe)], [(150, forwardShot, 0)], 3])
        self.spawnlist.append([11400, fighter, 800, 0, 0, 2, [(0, 0), (150, strafe)], [(150, forwardShot, 0)], 3])
        self.spawnlist.append([11450, fighter, 600, 0, 0, 2, [(0, 0), (150, strafe)], [(150, forwardShot, 0)], 2])
        self.spawnlist.append([11450, fighter, 800, 0, 0, 2, [(0, 0), (150, strafe)], [(150, forwardShot, 0)], 2])
        self.spawnlist.append([11500, fighter, 600, 0, 0, 2, [(0, 0), (150, strafe)], [(150, forwardShot, 0)], 1])
        self.spawnlist.append([11500, fighter, 700, 0, 0, 2, [(0, 0), (150, strafe)], [(150, forwardShot, 0)], 1])
        self.spawnlist.append([11500, fighter, 800, 0, 0, 2, [(0, 0), (150, strafe)], [(150, forwardShot, 0)], 1])
        #
        # destroyers die van onder komen en dan gaan zigzaggen
        #       self.spawnlist.append([11800, destroyer, 200, 1355, 0, -7, [(0, 0), (120, 3, 0, 2), (250, zigzag)], [(100, 4,0,4, 20)], 5])
        self.spawnlist.append([11800, destroyer, 1200, 1355, 0, -7, [(0, 0), (120, 3, 0, 2), (250, zigzag)], [(100, 4, 0, 4, 20)], 5])

        self.spawnlist.append([11600, scorchbuilding1, 750, 0, 0, 1, [(0, 0), (0, 0)], [(0, 0, 0)], 1])
        self.spawnlist.append([11650, scorchbuilding1, 1150, 0, 0, 1, [(0, 0), (0, 0)], [(0, 0, 0)], 1])
        self.spawnlist.append([11700, scorchbuilding1, 100, 0, 0, 1, [(0, 0), (0, 0)], [(0, 0, 0)], 1])
        self.spawnlist.append([11750, scorchbuilding2, 500, 0, 0, 1, [(0, 0), (0, 0)], [(0, 0, 0)], 1])
        self.spawnlist.append([11800, scorchbuilding2, 300, 0, 0, 1, [(0, 0), (0, 0)], [(0, 0, 0)], 1])
        self.spawnlist.append([11850, scorchbuilding2, 800, 0, 0, 1, [(0, 0), (0, 0)], [(0, 0, 0)], 1])
        self.spawnlist.append([12000, scorchbuilding1, 50, 0, 0, 1, [(0, 0), (0, 0)], [(0, 0, 0)], 1])
        self.spawnlist.append([12050, scorchbuilding3, 900, 0, 0, 1, [(0, 0), (0, 0)], [(0, 0, 0)], 1])
        self.spawnlist.append([12100, scorchbuilding3, 400, 0, 0, 1, [(0, 0), (0, 0)], [(0, 0, 0)], 1])
        self.spawnlist.append([12150, scorchbuilding3, 700, 0, 0, 1, [(0, 0), (0, 0)], [(0, 0, 0)], 1])
        self.spawnlist.append([12200, scorchbuilding4, 250, 0, 0, 1, [(0, 0), (0, 0)], [(0, 0, 0)], 1])

        self.textlist.append([12000, "Reaching destination...", 30, (0, 150, 0), (100, 40), (warscreenwidth / 2, 100), (warscreenwidth, 50)])
        self.textlist.append([12200, "SCANNING...", 30, (255, 255, 255), (100, 40), (warscreenwidth / 2, 50), (warscreenwidth, 100)])
        self.textlist.append([12400, "WARNING: LARGE ENEMY OBJECT DETECTED", 30, (200, 0, 0), (100, 40), (warscreenwidth / 2, 100), (warscreenwidth, 50)])
        self.textlist.append([12700, "SCORCH COMMAND BASE: CHIMERA", 30, (255, 255, 255), (100, 40), (warscreenwidth / 2, 100), (warscreenwidth, 50)])

        # Command Ship: Chimera
        # hoofdbaas die uit 3 delen bestaat

        self.spawnlist.append([13000, chimera2, warscreenwidth / 2 - 300, 0, 0, 6, [(0, straightLine), (60, changeDirection, 0, 0), (200, zigzag)], [(60, machineGun, 0)], 5])
        self.spawnlist.append([13000, chimera1, warscreenwidth / 2, 0, 0, 6, [(0, straightLine), (50, changeDirection, 0, 0)], [(100, clusterShot, 1, 6, 20), ((60, 1000, 99999), aimedShot, 0)], 10])
        self.spawnlist.append([13000, chimera3, warscreenwidth / 2 + 300, 0, 0, 6, [(0, straightLine), (60, changeDirection, 0, 0), (200, zigzag)], [(4, flameThrower, 0)], 5])

        #  self.spawnlist.append([13000, 12, 320, 0, 0, 6,[(0, 0), (60, 3, 0, 0), (150, 1), (600, 4), (756, 1), (1226, 4), (1382, 1), (1832, 4),(1988, 1)],
        # [((50, 50, 620), 4, 0, 6, 15), ((20, 776, 1226), 1, 1), ((50, 1382, 1832), 4, 0, 6, 15),((50, 1988, 99999), 2, 0), ((100, 2100, 99999), 4, 0, 6, 20)], 10])

        self.spawnlist.append([13000, -1])



    def level_3(self):
        Gamedata.bgimages = Backgroundprops.Images([])
        self.textlist.append([100, "Level 3: Alfa attack", 30, (0, 150, 0), (160, 40), (warscreenwidth / 2, 100), (800, 50)])
        self.textlist.append([200, "WARNING: ALFA FLEET DETECTED", 30, (200, 0, 0), (150, 40), (warscreenwidth / 2, 150), (warscreenwidth, 50)])

        #Goede oude fighters kapot knallen.
        self.spawnlist.append([400, bird_of_pray , 420, 0, 0, 2, [(0, 0), (40, 2)], [(60, 1, 2)], 0])

        self.spawnlist.append([400, bird_of_pray , 780, 0, 0, 2, [(0, 0), (40, 2)], [(60, 1, 2)], 0])

        self.spawnlist.append([550, bird_of_pray , 600, 0, 0, 2, [(0, 0), (40, 2)], [(60, 1, 2)], 0])

        self.spawnlist.append([1000, -1])

    def level_4(self):
        Gamedata.bgimages = Backgroundprops.Images([])
        self.textlist.append([100, "Level 4: Under development", 30, (0, 150, 0), (160, 40), (warscreenwidth / 2, 100), (800, 50)])

        #Goede oude fighters kapot knallen.
        self.spawnlist.append([1000, -1])


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

    def meteorstorm(self, startticks, incrementticks, number):
        for meteor in range(number):
            spawntime = meteor * incrementticks + startticks
            unittype = random.randint(0, 2)
            variant = random.randint(0, 2)
            speedx = random.randint(-3, 3)
            speedy = random.randint(6, 9)
            startx = random.randint(int(max(0, -(windowheight / speedy * speedx))), int(min(warscreenwidth, warscreenwidth - (warscreenwidth / speedy * speedx))))
            starty = 0
            programlist = [(0, 0)]
            weaponprogramlist = [(0, 0)]
            self.spawnlist.append([spawntime, unittype * 3 + variant, startx, starty, speedx, speedy, programlist, weaponprogramlist, 0])