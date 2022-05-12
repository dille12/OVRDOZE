from classes import *
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
                print("bullet detected")
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
        multiplayer_actors[name].set_values(x, y, angle, hp)

    for x, y, angle, damage, speed in bullets:
        print("GENERATING A BULLET")
        bullet_list.append(Bullet([int(x), int(y)], int(angle), int(damage), speed = int(speed)))

    for x, y ,t_x, t_y in grenades:
        grenade_list.append([int(x),int(y)], [int(t_x), int(t_y)])

    return bullet_list, grenade_list
