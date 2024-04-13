import pygame
from values import fp

terminal = pygame.font.Font(fp("texture/terminal.ttf"), 20)
terminal2 = pygame.font.Font(fp("texture/terminal.ttf"), 15)
terminal3 = pygame.font.Font(fp("texture/terminal.ttf"), 10)

def minus_list(list1, list2):
    list3 = list1.copy()
    for i in range(len(list1)):
        list3[i] = list1[i] - list2[i]

    return list3

def compareGuns(app, screen, gun1, gun2, playerPos, cameraPos, player_inventory, text = True):
    
    renderPos = minus_list(playerPos, cameraPos)

    xD, yD = gun2.comparisonImage.get_size()

    if gun1 != False:
        renderGunDetail(app, screen, gun1, gun2, minus_list(renderPos, (100 + xD/2, 20 + yD/2)), player_inventory, "CURRENT", text)

    renderGunDetail(app, screen, gun2, gun1, minus_list(renderPos, (-100 + xD/2, 20 + yD/2)), player_inventory, "F TO SWITCH" if gun1 != False else "F TO PICK UP", text)

def renderGunDetail(app, screen, gun, comparisonG, origin, player_inventory, writeBelow = "", text = True):
    screen.blit(gun.comparisonImage, origin)
    if text:
        t = terminal.render(writeBelow, False, [255,255,255])
        screen.blit(t, minus_list(origin, [0, 25]))

    t = terminal2.render(gun.name, False, [255,255,255])

    screen.blit(t, minus_list(origin, [0, -30]))

    DMG = gun.DPS

    if comparisonG == False:
        better = 3
    else:
        if DMG > comparisonG.DPS:
            better = 1
        elif DMG < comparisonG.DPS:
            better = 0
        else:
            better = 2

    factor = DMG/app.MAXDPS

    t = terminal3.render(f"DPS:", False, getColor(better))
    screen.blit(t, minus_list(origin, [0, -50]))

    pygame.draw.rect(screen, getColor(better), [origin[0]+25, origin[1] + 50, 60, 8], 1)
    pygame.draw.rect(screen, getColor(better), [origin[0]+27, origin[1] + 52, 56 * factor, 4])

    RPM = "SEMI" if gun.semi_auto else f"{gun._bullet_per_min}"

    if comparisonG == False:
        better = 3
    else:
        if gun.semi_auto or comparisonG.semi_auto:
            better = 2
        elif gun._bullet_per_min > comparisonG._bullet_per_min:
            better = 1
        else:
            better = 0

    t = terminal3.render(f"RPM: {RPM}", False, getColor(better))
    screen.blit(t, minus_list(origin, [0, -65]))

    AMMO = gun.ammo

    if AMMO != "INF":
        ammoAvailable = player_inventory.get_amount_of_type(AMMO)

    if comparisonG == False:
        better = 3
    else:
        if AMMO == comparisonG.ammo:
            better = 2
        else:
            if AMMO == "INF":
                better = 1
            elif comparisonG.ammo == "INF":
                better = 0
            else:
                ammoAvailable2 = player_inventory.get_amount_of_type(comparisonG.ammo)
                if ammoAvailable > ammoAvailable2:
                    better = 1
                elif ammoAvailable == ammoAvailable2:
                    better = 2
                else:
                    better = 0


    if AMMO != "INF":
        t = terminal3.render(f"AMMO: {AMMO} (+{ammoAvailable} RES.)", False, getColor(better))
    else:
        t = terminal3.render(f"AMMO: {AMMO}", False, getColor(better))
    screen.blit(t, minus_list(origin, [0, -80]))

def getColor(better):
    if better == 0:
        return [255,0,0]
    elif better == 1:
        return [0,255,0]
    elif better == 2:
        return [255,255,0]
    else:
        return [255,255,255]

