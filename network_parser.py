from armory import *
from enemies import *
from objects import *
from values import *
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
    zombies = []
    z_events = []


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
                print("Parsed a grenade")
                type, x, y ,t_x, t_y = data.split("_")
                grenades.append([type, x, y ,t_x, t_y])

            elif type == "ZOMBIE":
                print("Parsed a zombie")
                x, y, id, target_name, power, type = data.split("_")
                zombies.append([x, y, id, target_name, power, type])
            elif type == "ZEVENT":
                print("z event")
                id, z_event = data.split("_")
                z_events.append([id, z_event])



        except:
            pass
    return players, bullets, grenades, zombies, z_events

def gen_from_packet(packet, player_actor, multiplayer_actors, zomb_info):
    players_info, bullets, grenades, zombies, z_events = parse_packet(packet)

    interctables, camera_pos, map_render, NAV_MESH, walls, hp_diff, dam_diff = zomb_info

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

    for type, x, y ,t_x, t_y in grenades:
        print("GENERATING A GRENADE")
        grenade_list.append(Grenade([int(x),int(y)], [int(t_x), int(t_y)], type, mp = True))

    for x, y, id, target_name, power, type in zombies:
        print(f"GENERATING A ZOMBIE {id}")
        if target_name == player_actor.name:
            targ = player_actor
        else:
            targ = multiplayer_actors[target_name]

        enemy_list.append(Zombie([int(x),int(y)], interctables, targ, NAV_MESH, walls, hp_diff = hp_diff, dam_diff = dam_diff, type = type, wall_points = None, identificator = int(id), power = float(power)))

    for id, z_event in z_events:
        print("Generating data from zevent")

        gen = list(get_zombie_by_id(int(id)))
        if len(gen) == 0:
            print(f"NO ZOMBIE FOUND FOR ZEVENT!!! {id}")
        for target in gen:
            print(id, z_event)
            if z_event == "terminate":
                print(f"Killing zombie {id}")
                target.kill(camera_pos, enemy_list, map_render, zevent = True)
            # else:
            #     if z_event == player_actor.name:
            #         target.target = player_actor
            #     else:
            #         target.target = multiplayer_actors[z_event]




    zombie_events.clear()


# PACKET
# PLAYER:Runkkari_373_122_-340
# BULLET:421_103_-337_15_18
# #END
