from armory import *
from enemies import *
from objects import *
from values import *
import ast

# PACKET
# PLAYER:Runkkari_373_122_-340
# BULLET:421_103_-337_15_18
# #END


def parse_packet(packet):
    packet_data = packet.split("#END")

    players = []
    bullets = []
    grenades = []
    zombies = []
    z_events = []
    turrets = []
    barricades = []

    for packet_data_2 in packet_data:
        packet_lines = packet_data_2.split("\n")

        for line in packet_lines:
            try:
                type, data = line.split(":")
                if type == "BULLET":
                    if data.split("_") not in bullets:
                        bullets.append(data.split("_"))

                elif type == "PLAYER":
                    if data.split("_") not in players:
                        players.append(data.split("_"))

                elif type == "GRENADE":
                    print("Parsed a grenade")
                    if data.split("_") not in grenades:
                        grenades.append(data.split("_"))

                elif type == "ZOMBIE":
                    if data.split("_") not in zombies:
                        zombies.append(data.split("_"))
                elif type == "ZEVENT":
                    if data.split("_") not in z_events:
                        z_events.append(data.split("_"))

                elif type == "TURRET":
                    if data.split("_") not in turrets:
                        turrets.append(data.split("_"))

                elif type == "BARRICADE":
                    if data.split("_") not in barricades:
                        barricades.append(data.split("_"))

            except:
                pass
    return players, bullets, grenades, zombies, z_events, turrets, barricades


def gen_from_packet(packet, player_actor, multiplayer_actors, zomb_info):
    (
        players_info,
        bullets,
        grenades,
        zombies,
        z_events,
        turrets,
        barricades,
    ) = parse_packet(packet)

    interctables, camera_pos, map_render, NAV_MESH, walls, hp_diff, dam_diff = zomb_info
    zombie_events2 = []
    for name, x, y, angle, hp in players_info:

        if name not in multiplayer_actors:
            if name == "":
                continue
            else:
                multiplayer_actors[name] = Player_Multi(name)

        multiplayer_actors[name].set_values(x, y, angle, hp)

    for x, y, angle, damage, speed in bullets:
        print("GENERATING A BULLET")
        bullet_list.append(
            Bullet.Bullet(
                [int(x), int(y)], int(angle), int(damage), speed=int(speed), mp=True
            )
        )

    for type, x, y, t_x, t_y in grenades:
        print("GENERATING A GRENADE")
        grenade_list.append(
            Grenade([int(x), int(y)], [int(t_x), int(t_y)], type, mp=True)
        )

    for x, y, id, target_name, power, type in zombies:
        print(f"GENERATING A ZOMBIE {id}")
        if target_name == player_actor.name:
            targ = player_actor
        else:
            targ = multiplayer_actors[target_name]
        enemy_list.append(
            Zombie(
                [int(x), int(y)],
                interctables,
                targ,
                NAV_MESH,
                walls,
                hp_diff=float(hp_diff),
                dam_diff=float(dam_diff),
                type=type,
                wall_points=None,
                identificator=int(id),
                player_ref=player_actor,
                power=float(power),
            )
        )

    for id, z_event, outcome in z_events:

        gen = list(get_zombie_by_id(int(id)))
        if len(gen) == 0:
            print(f"NO ZOMBIE FOUND FOR ZEVENT!!! {id}")
            zombie_events2.append(f"ZEVENT:{id}_getinfo_1")
        for target in gen:
            # print(id, z_event, outcome)
            if z_event == "terminate":
                target.kill(camera_pos, enemy_list, map_render, zevent=True)
            elif z_event == "setpos":
                target.pos = ast.literal_eval(outcome)
            elif z_event == "setroute":
                target.route = ast.literal_eval(outcome)
            elif z_event == "getinfo" and target not in packet_dict:
                print(f"Sending zombie {id} back")
                packet_dict["zombies"].append(target)

            # else:
            #     if z_event == player_actor.name:
            #         target.target = player_actor
            #     else:
            #         target.target = multiplayer_actors[z_event]

    for x, y, ang_spe, fire_r, range, damage, lifetime in turrets:
        try:
            print(f"GENERATING A TURRET")
            turret_list.append(
                Turret(
                    [int(x), int(y)],
                    int(ang_spe),
                    int(fire_r),
                    int(range),
                    damage=0,
                    lifetime=round(float(lifetime)),
                    mp=True,
                )
            )
        except Exception as e:
            print(f"TURRET EXCEPTION: {e}")

    zombie_events.clear()
    for x in zombie_events2:

        zombie_events.append(x)


# PACKET
# PLAYER:Runkkari_373_122_-340
# BULLET:421_103_-337_15_18
# #END
