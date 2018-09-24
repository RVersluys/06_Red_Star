import os
import pygame

import GameplayConstants

class Sounds:
    def __init__(self):
        #explosies
        soundfolder = os.path.join(os.path.dirname(__file__), 'sounds')
        self.explosions = []
        filenames = ["explosion_" + str(nr) + ".wav" for nr in range(10)]
        for filename in filenames:
            self.explosions.append(pygame.mixer.Sound(os.path.join(soundfolder, filename)))

        #menugeluiden
        self.soundclick = pygame.mixer.Sound(os.path.join(soundfolder, "menu", "click.wav"))
        self.soundfail = pygame.mixer.Sound(os.path.join(soundfolder, "menu", "fail.wav"))
        self.soundimplement = pygame.mixer.Sound(os.path.join(soundfolder, "menu", "implement.wav"))
        self.soundremove = pygame.mixer.Sound(os.path.join(soundfolder, "menu", "remove.wav"))
        self.soundcancel = pygame.mixer.Sound(os.path.join(soundfolder, "menu", "cancel.wav"))

        #geluiden van hero
        self.lasersound = pygame.mixer.Sound(os.path.join(soundfolder, 'laser.wav'))
        self.pickupsound = pygame.mixer.Sound(os.path.join(soundfolder, 'goldpickup.wav'))
        self.bangs = []
        self.bangs.append(pygame.mixer.Sound(os.path.join(soundfolder, "bang0.ogg")))
        self.bangs.append(pygame.mixer.Sound(os.path.join(soundfolder, "bang1.ogg")))
        self.bangs.append(pygame.mixer.Sound(os.path.join(soundfolder, "bang2.ogg")))
        self.shieldhitsound = pygame.mixer.Sound(os.path.join(soundfolder, "shieldhit.wav"))


    def soundchange(self):
        for sound in self.explosions:
            sound.set_volume(GameplayConstants.effectsvolume / 100)
        self.soundclick.set_volume(GameplayConstants.effectsvolume / 100)
        self.soundfail.set_volume(GameplayConstants.effectsvolume / 100)
        self.soundimplement.set_volume(GameplayConstants.effectsvolume / 100)
        self.soundremove.set_volume(GameplayConstants.effectsvolume / 100)
        self.soundcancel.set_volume(GameplayConstants.effectsvolume / 100)
        self.lasersound.set_volume(GameplayConstants.effectsvolume / 100)
        self.lasersound.set_volume(GameplayConstants.effectsvolume / 100)
        self.shieldhitsound.set_volume(GameplayConstants.effectsvolume / 100)
        self.pickupsound.set_volume(GameplayConstants.effectsvolume / 100)
        for sound in self.bangs:
            sound.set_volume(GameplayConstants.effectsvolume / 100)


sounds = Sounds()
sounds.soundchange()