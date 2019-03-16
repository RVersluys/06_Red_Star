import pygame
import Colors
import Tools
import Gamedata
import GameplayConstants

class Missioninfo:
    def __init__(self, rect):
        self.level = Gamedata.player.levelnumber
        rect.height = 45+20*len(missioninfo[self.level])
        self.rect = rect

    def update(self):
        Tools.draw_text(GameplayConstants.screen, "Mission details", 25, self.rect.x + 250, self.rect.y + 15, "Xolonium", Colors.white)

        if self.level == 2:
            if Gamedata.player.betrayAlfa:
                missioninfolist = missioninfo[self.level][0]
            else:
                missioninfolist = missioninfo[self.level][1]
        else:
            missioninfolist = missioninfo[self.level]

        for line in range(len(missioninfolist)):
            Tools.draw_text(GameplayConstants.screen, missioninfo[self.level][line], 20, self.rect.x + 5, self.rect.y + 60 + 25 * line, "Xolonium", Colors.white)

# Prompt after level 2
prompt2 = ["The Scorch flagship floats battered and bruised, and you prepare",
                "yourself for the final strike. Just when you are about to engage",
                "you are being hailed.",
                "A dark figure that is visibly wounded comes on screen. 'I commend",
                "you captain,' he says, 'we clearly underestimated your prowess in",
                "battle, but you are being played.'",
                "'The Alfa belief they should be the sole inhabitants of this galaxy,",
                "and with this Uridium 241, nothing will stand in their way to",
                "achieve their goals.'",
                "'Only if you use it for yourself and unlock it's power, you can",
                "ensure the safety of your home planet.",
                "",
                "Do you give the Uridium to the Alfa or keep it for yourself?"]
prompt2Options = ["Keep Uridium 241", "Give Uridium 241"]

# Prompt after level 4 A
prompt4A = ["While you are fighting in Sirius III distress messeges are starting",
                  "to come in. A giant fleet of the Scorch just passed Neptune.",
                  "The Scorch have betrayed us! You immediatly turn your spacecraft",
                  "to head home.",
                  "",
                  "The ship shakes as the engines roar at full capacity. You are",
                  "only halfway back when reports come in that Earth's planetary",
                  "defences are getting shattered.",
                  "",
                  "Then the messages stop...",
                  "",
                  "When you approach Earth your scanners reveal The Scorch already left.",
                  "Uppon further inspection your worst fears become truth. You see the",
                  "smoldering remains of what once was the inhabited surface of planet",
                  "Earth.",
                  "",
                  "But you are still here, and you swear The Scorch will pay the price...",
                  "You could loot a giant base of The Scorch for it's credits or steal",
                  "technology that can be used to unlock even more advanced applications",
                  "of Uridium 241."]
prompt4AOptions = ["Steel credits", "Steel technology"]



missioninfo = [[
                # Missioninfo level 1
                "The interplanetary dream of Earth is quickly squashed when a",
                "fleet of the Scorch entered our solar system, destroying our",
                "colonies on Mars and the Jupiter moon Europa. But then a",
                "mysterious allien race called Alfa came to intervene. If it wasn't",
                "for the timely intervention of the Alfa carriër Gantador, who",
                "knows what would remain of this little blue planet we call home...",
                "",
                "But we aren't save yet. After the departure of the Gantador, it",
                "appears that many Scorch ships remain in our solar system.",
                "The Alfa have left us with one specialised spaceship to defend",
                "ourselves, and you, as the greatest spaceship ace of Earth",
                "are assigned to fend of the remaining Scorch forces."],
                # Missioninfo level 2
               ["Nothing comes free and interstellar affairs appear to be no",
                "exception. The Alfa have come to collect our dept, demanding",
                "that we retrieve rare minerals in a base of The Scorch and",
                "return it to a secret Alfa base. Because The Scorch sensors",
                "are not adapted to human ships we would be able to approach it",
                "with relative ease. Although this mission is to satisfy",
                "the demands of the Alfa, it seems to be time wel spent",
                "to give the aliens that destroyed our colonies on Mars and",
                "Europa a visit."],
                 # Missioninfo level 3 A
                [["The scorch promised to ambush the secret Alfa base, and long",
                 "range scanners confirm they came through.",
                  "",
                  "It didn't stop the Alfa from sending a fleet to our solar system",
                  "though, and we were only just in time to intercept. The Alfa fleet",
                  "opened fire on sight.",
                  "",
                  "Keeping the Uridium was not in vain though: preliminary research",
                  "on Earth allready revealed that the Uridium-241 can be used as an",
                  "incredible source of energy."],
                 # Missioninfo level 3 B
                 ["After delivering the Uridium, the Alfa shared the technology of a",
                  "unique type of shield.",
                  "",
                  "The illusion that we have found a reliable galactic ally hoever,",
                  "is short lived, as long range scanners reveal an Alfa warfleet is",
                  "is approaching our solar system. When you intercept the fleet",
                  "opens fire on sight. Why the Alfa share their technology only",
                  "to attack us now, remains a mystery.",
                  "We have not the luxury to pursue our curiosity."]],
                # Missioninfo level 4 A
                [["The Alfa fleet is shattered, and the earth is save for now, but",
                  "nothing stops the hem from striking again.",
                 "",
                  "The Scorch offer a suggestion, if we were to attack a nearby Alfa,",
                  "base, theyw ould send their fleet to strike at the Alfa Core systems.",
                  "Striking the Alfa base is a good idea regardless as the base could",
                  "be used as a vantage point in future attacks against our solar",
                  "system."],
                # Missioninfo level 4 B
                 ["The Alfa fleet is shattered and the earth is save for now, but",
                  "nothing stops the Alfa from striking again.",
                  "",
                  "The Interplanetary Counsel  orders you to strike a nearby Alfa base",
                  "in Sirius III that could be used as a vantage point in future attacks",
                  "against our solar system."]],
                # Missioninfo level 5 A
                [[],
                 ]
               ]
