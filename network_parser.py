from armory import *
from enemies import *
from objects import *
# PACKET
# PLAYER:Runkkari_373_122_-340
# BULLET:421_103_-337_15_18
# #END

def parse_packet(packet):
    packet_data = packet.split("#END")[0]
    packet_lines = packet_data.split("\n")

    players = []

    bullets = []
    grenades = []


    for line in packet_lines:
        try:
            type, data = line.split(":")
            if type == "BULLET":
                x, y, angle, damage, speed = data.split("_")
                bullets.append([x, y, angle, damage, speed])

            elif type == "PLAYER":
                name, x, y, angle, hp = data.split("_")

                players.append([name, x, y, angle, hp])

            elif type == "GRENADE":
                x, y ,t_x, t_y = data.split("_")
                grenades.append([x, y ,t_x, t_y])
        except:
            pass
    return players, bullets, grenades

def gen_from_packet(packet, multiplayer_actors, bullet_list, grenade_list):
    players_info, bullets, grenades = parse_packet(packet)

    for name, x, y, angle, hp in players_info:

        if name not in multiplayer_actors:
            if name == "":
                continue
            else:
                multiplayer_actors[name] = Player_Multi(name)

        multiplayer_actors[name].set_values(x, y, angle, hp)

    for x, y, angle, damage, speed in bullets:
        print("GENERATING A BULLET")
        bullet_list.append(Bullet([int(x), int(y)], int(angle), int(damage), speed = int(speed), mp = True))

    for x, y ,t_x, t_y in grenades:
        print("GENERATING A GRENADE")
        grenade_list.append(Grenade([int(x),int(y)], [int(t_x), int(t_y)], mp = True))

    return bullet_list, grenade_list
