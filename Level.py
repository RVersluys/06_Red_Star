import random

import Mobs
import Sprites
import Backgroundprops

windowheight = 1080
warscreenwidth = 1440

class Level:
    def __init__(self):
        Mobs.images.load_level([x for x in range(13)])
        self.end = False
        self.succes = False
        self.abort = False
        self.ticks = 0
        self.spawnlist = []
        self.startscore = Sprites.hero.score
        self.startgold = Sprites.hero.gold
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

        #1 = na hoeveel ticks komt
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
            #1 = cooldown
            #2 = weaponprogram
                #0 = no weapon
                #1 = aimed shot
                #2 = machinegun
                #3 = forward shot
                #4 = cluster shot
            #3 = wapentype
            #4 = bulletcount (only used in cluster shot)
            #5 = angle between bullets (only used in cluster shot)

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

        # deze eindbaas swingt een beetje heen en weer en schiet een cluster schot van 6 bullets met 10 graden ruimte tussen de bullets
        self.spawnlist.append([5200, 12, 320, 0, 0, 6, [(0, 0), (60, 3,0,0), (150,1)], [(100, 4, 0, 6, 15), (60,1,1)], 1000])

        #level end
        self.spawnlist.append([5300, -1])

        ###################################################################################################
        #lijst wordt gesorteerd om op volgorde uit te kunnen voeren.
        self.spawnlist.sort(key=lambda x: x[0])

        for x in range(250):
            star = Backgroundprops.Star(True)
            Sprites.background.add(star)

    def spawning(self):
        if len(self.spawnlist) > 0:
            if self.spawnlist[0][0] == self.ticks:
                if self.spawnlist[0][1] == -1:
                    self.end = True
                    self.succes = True
                    return
                m = Mobs.Mob(self.spawnlist[0][1],self.spawnlist[0][2],self.spawnlist[0][3],self.spawnlist[0][4], self.spawnlist[0][5],self.spawnlist[0][6], self.spawnlist[0][7], self.spawnlist[0][8])
                Sprites.all_sprites.add(m)
                Sprites.mobs.add(m)
                self.spawnlist.pop(0)
                self.spawning()
        if random.randint(0,10) == 0:
            star = Backgroundprops.Star(False)
            Sprites.background.add(star)
        self.ticks += 1
        return


