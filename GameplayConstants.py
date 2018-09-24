import pygame
import os
import Sprites

game_folder = os.path.dirname(__file__)


windowwidth = 1920
windowheight = 1080
warscreenwidth = 1440
fps = 60
musicvolume = 100
effectsvolume = 100
extendedscreen = pygame.Rect(-10,-10,windowwidth+20,windowheight+20)



# de vorm van elk shippart: tuples zijn verticale lijnen. 1 is dat er iets zit.
kinetic_weapon = [(1), (1), (1)]
flak_cannon = [(0, 1, 0), (0, 1, 0), (1, 1, 1)]
laser_cannon = [(1), (1), (1), (1)]
rocket_engine = [(1), (1)]
ion_thruster = [(1, 1), (1, 1)]
magnatic_shield = [(1, 1)]
flux_shield = [(1, 1, 1)]
solar_panel = [(1)]
fission_reactor = [(1, 1), (0, 1)]

# specificaties en namen van de onderdelen
# prijs is keer duizend voor aanschaf. Upgrades: upgrade 1: *2250, upgrade 2: *4000, upgrade 3: *6259, upgrade 4: *9000
shippartslist = [[["Weapons"], ["Engine"], ["Shield"], ["Power"]],
                 [["Kinetic Weapon", 1.5, kinetic_weapon, 6, 12, "A large cannon that shoots", "depleted uranium projectiles", "at high rate.", 5, 1], #wapens: 0=name, 1=price, 2=shape, 3=energyuse(shot), 4=cooldown(ticks), 5-7=description, 8=damage, 9=speedreduction
                  ["Flak Cannon", 6, flak_cannon, 10, 21, "Magnatic balista that propels", "projectiles that explode to carpet", "the area with small fragments.", 20, 2],
                  ["Laser Cannon", 10, laser_cannon, 50, 54, "High powered laser weapon that", "can blow a hole in even the ", "strongest armor.", 40, 1]],
                 [["Rocket Engine", 1, rocket_engine, 10, 2, "Conventional rocket propulsion ", "is not necessary efficiënt but it", "is flexible."], #engines: name, price, shape, energyuse(second), speedboost
                  ["Ion Thruster", 3, ion_thruster, 20, 5, "Higly efficient propulsion system", "that fires ions at the opposite", "direction."]],
                 [["Magnatic Deflector", 2.5, magnatic_shield, 7, 15, "The use of powerfull magnetic", "fields are able to dispurse many", "types of projectiles."], #shields: name,  price, energyuse(second), shape, maxschildboost
                  ["Flux Shield", 5, flux_shield, 12, 30, "This shield filters undesirable", "wavelengths while allowing other", "wavelengths to protect the ship."]],
                 [["Solar Panel", 1, solar_panel, 15, 30, "Conventional energy mechanism", "that converts solar energy in large", "batteries."], #power source: name, price, shape, energyregen(second), maxenergyboost
                  ["Fission Reactor", 4, fission_reactor, 65, 75, "Based on nuclear fission, this", "reactor gives the ship massive", "amounts of energy."]]]

# locaties waar schiponderdelen kunnen worden geplaatst
# dit is de layout van het schip. 1 = schip1, 1+2 = schip2 en 1+2+3 = schip 3
shipdesign = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 1, 0, 0, 0, 0],
              [0, 3, 0, 0, 1, 0, 0, 3, 0],
              [0, 3, 3, 1, 1, 1, 3, 3, 0],
              [0, 3, 1, 1, 1, 1, 1, 3, 0],
              [3, 2, 1, 1, 2, 1, 1, 2, 3],
              [3, 2, 2, 0, 0, 0, 2, 2, 3],
              [0, 0, 0, 0, 0, 0, 0, 0, 0]]

shippartimages = []
for catagory in range(1, 5):
    templist = []
    for item in range(len(shippartslist[catagory])):
        templist.append(pygame.image.load(os.path.join(game_folder, "img", "parts", shippartslist[catagory][item][0] + ".png")).convert_alpha())
    shippartimages.append(templist)

def shippartinfo(list, index, upgrade):
    price = shippartprice(list, index, upgrade)
    shippartinfo = []
    if upgrade == 0:
        shippartinfo.append("Price: " + str(price))
        shippartinfo.append(shippartslist[list][index][0])
    else:
        shippartinfo.append("Current level: " + str(upgrade))
        shippartinfo.append("Cost to upgrade: " + str(price))
        upgrade -= 1

    shippartinfo.append(shippartslist[list][index][5])
    shippartinfo.append(shippartslist[list][index][6])
    shippartinfo.append(shippartslist[list][index][7])
    shippartinfo.append("")
    if list == 1:
        shippartinfo.append("Damage: " + str(shippartslist[list][index][8]*(upgrade+1)))
        shippartinfo.append("Cooldown: " + str(shippartslist[list][index][4]) + " ms")
        shippartinfo.append("Energy per shot: " + str(shippartslist[list][index][3]*(upgrade+1)))
        shippartinfo.append("Speed: -" + str(shippartslist[list][index][9] * (upgrade + 1)))
    elif list == 2:
        shippartinfo.append("Increased speed: " + str(shippartslist[list][index][4]*(upgrade+1)))
        shippartinfo.append("Power use: " + str(shippartslist[list][index][3]*(upgrade+1)))
    elif list == 3:
        shippartinfo.append("Increased shield: " + str(shippartslist[list][index][4]*(upgrade+1)))
        shippartinfo.append("Power use (normal): " + str(shippartslist[list][index][3]*(upgrade+1)))
        shippartinfo.append("Power use (recharging): " + str((shippartslist[list][index][3] + shippartslist[list][index][4])*(upgrade+1)))
    elif list == 4:
        shippartinfo.append("Energy output: " + str(shippartslist[list][index][3]*(upgrade+1)))
        shippartinfo.append("Energy storage: " + str(shippartslist[list][index][4]*(upgrade+1)))
    return shippartinfo

def heroshipinfo(maxuse):
    text = []
    text.append("Max speed: " + str(Sprites.hero.speed) + " AUh")
    text.append("Armor: " + str(Sprites.hero.maxarmor))
    text.append("Shields: " + str(Sprites.hero.maxshield))
    text.append("")
    text.append("Energy:")
    text.append("Storage: " + str(Sprites.hero.maxenergy) + " MWh")
    text.append("Base gain: " + str(Sprites.hero.energyregen) + " MW")
    text.append("Base use: " + str(Sprites.hero.energyuse) + " MW")
    text.append("Max use: " + str(maxuse) + " MW")
    return text


def shippartprice(list, index, upgrade):
    baseprice = shippartslist[list][index][1]
    price = int(100*(upgrade+3)**2*baseprice)
    return price