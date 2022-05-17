import os, sys
import pygame
import math
import random
import time
import mixer
from classtest import *
from _thread import *
import threading
import copy
import los
from network import Network
import ast
import network_parser
from app import App
from button import Button
from glitch import Glitch
from values import *
import classes
from classes import items
import func
#import path_finding

import armory
import objects
import enemies
import RUN

print("IMPORTS COMPLETE")



terminal = pygame.font.Font('texture/terminal.ttf', 20)
terminal2 = pygame.font.Font('texture/terminal.ttf', 30)
terminal3 = pygame.font.Font('texture/terminal.ttf', 10)



weapons = {


"M1911": armory.Weapon("M1911",
                        clip_s = 8,
                        fire_r = 2000,
                        spread = 7,
                        spread_r = 0.94,
                        reload_r = 45,
                        damage = 15,
                        semi_auto = True,
                        bullets_at_once = 1,
                        shotgun = False,
                        ammo_cap_lvlup = 1,
                        image = "m1911.png",
                        ammo = "INF",
                        view = 0.0,
                        handling = 0.7),

"AR-15": armory.Weapon("AR-15",
                        clip_s = 35,
                        fire_r = 500,
                        spread = 1,
                        spread_r = 0.93,
                        bullet_speed = 35,
                        reload_r = 60,
                        damage = 34,
                        bullets_at_once = 1,
                        shotgun = False,
                        sounds = assault_rifle_sounds,
                        ammo_cap_lvlup = 1,
                        image = "m16.png",
                        ammo = "7.62x39MM",
                        piercing = True,
                        view = 0.032,
                        handling = 0.25,
                        burst = True,
                        burst_bullets = 3,
                        burst_fire_rate = 2),



"AK": armory.Weapon("AK47",
                        clip_s = 30,
                        fire_r = 520,
                        spread = 3,
                        spread_r = 0.94,
                        bullet_speed = 25,
                        reload_r = 60,
                        damage = 34,
                        bullets_at_once = 1,
                        shotgun = False,
                        sounds = assault_rifle_sounds,
                        ammo_cap_lvlup = 1,
                        image = "ak.png",
                        ammo = "7.62x39MM",
                        piercing = True,
                        view = 0.03,
                        handling = 0.35),


"SCAR18": armory.Weapon("SCAR18",
                        clip_s = 20,
                        fire_r = 240,
                        spread = 1,
                        spread_r = 0.93,
                        bullet_speed = 30,
                        reload_r = 45,
                        damage = 45,
                        bullets_at_once = 1,
                        shotgun = False,
                        sounds = assault_rifle_sounds2,
                        ammo_cap_lvlup = 1,
                        image = "ak.png",
                        ammo = "INF",
                        piercing = True,
                        view = 0.035,
                        handling = 0.45),

"MINIGUN": armory.Weapon("MINIGUN",
                        clip_s = 999,
                        fire_r = 3000,
                        spread = 2,
                        spread_r = 0.93,
                        bullet_speed = 45,
                        reload_r = 60,
                        damage = 34,
                        bullets_at_once = 1,
                        shotgun = False,
                        sounds = assault_rifle_sounds,
                        ammo_cap_lvlup = 1,
                        image = "ak.png",
                        ammo = "7.62x39MM",
                        piercing = True,
                        view = 0.03,
                        handling = 0.1),

"SPAS": armory.Weapon("SPAS-12",
                        clip_s = 6,
                        fire_r = 120,
                        spread = 5,
                        spread_per_bullet = 2,
                        spread_r = 0.93,
                        reload_r = 60,
                        damage = 22,
                        bullet_speed = 15,
                        bullets_at_once = 8,
                        shotgun = True,
                        semi_auto = True,
                        sounds = shotgun_sounds,
                        ammo_cap_lvlup = 2,
                        image = "spas12.png",
                        ammo = "12 GAUGE",
                        view = 0.01,
                        handling = 0.2),

"P90": armory.Weapon("P90",
                        clip_s = 50,
                        fire_r = 950,
                        spread = 7,
                        spread_r = 0.94,
                        reload_r = 60,
                        damage = 21,
                        bullets_at_once = 1,
                        shotgun = False,
                        sounds = smg_sounds,

                        #sounds = shotgun_sounds,
                        ammo_cap_lvlup = 2,
                        image = "p90.png",
                        ammo = "9MM",
                        view = 0.02,
                        handling = 0.5),
"GLOCK": armory.Weapon("GLOCK",
                        clip_s = 20,
                        fire_r = 350,
                        spread = 3,
                        spread_r = 0.92,
                        reload_r = 30,
                        damage = 27,
                        semi_auto = False,
                        bullets_at_once = 1,
                        shotgun = False,
                        ammo_cap_lvlup = 1,
                        image = "glock.png",
                        ammo = "45 ACP",
                        view = 0.017,
                        handling = 0.9,
                        burst = True,
                        burst_bullets = 3,
                        burst_fire_rate = 3),

"AWP": armory.Weapon("AWP",
                        clip_s = 10,
                        fire_r = 50,
                        spread = 1,
                        spread_r = 0.965,
                        spread_per_bullet = 25,
                        reload_r = 120,
                        damage = 200,
                        bullets_at_once = 1,
                        sounds = sniper_rifle_sounds,
                        bullet_speed = 55,
                        shotgun = False,
                        ammo_cap_lvlup = 1,
                        image = "awp.png",
                        ammo = "50 CAL",
                        piercing = True,
                        view = 0.045,
                        handling = 0.15,
                        semi_auto = True),
}




def give_weapon(gun):
    return weapons[gun].copy()



# if multiplayer:
#     net = Network()
#     print("MULTIPLAYER")
# else:
#     print("SINGLEPLAYER")


def thread_data_collect(net, packet, player_actor, multiplayer_actors, bullet_list, grenade_list, current_threading, zomb_info):
    try:
        reply = net.send(packet).translate({ord('/'): None})

        for i, line in enumerate(reply.split("\n")):
            func.print_s(screen, line, i+4)

        network_parser.gen_from_packet(reply, player_actor, multiplayer_actors, zomb_info)


    except Exception as e:
        print("CLIENT ERROR:", traceback.print_exc())
        pass
    current_threading = False


def write_packet(object):
    string = write_packet.get_string() + "\n"
    return string


def quit(arg):
    print("Quitting game")

    RUN.main()

def cont_game(arg):
    return True





def main(app, multiplayer = False, net = None, host = False, players = None, self_name = None, difficulty = "NORMAL", draw_los = True, dev_tools = True, skip_intervals = False, map = None, full_screen_mode = True):
    print("GAME STARTED WITH",difficulty)

    diff_rates = {"NO ENEMIES" : [0,1,1,1, -1], "EASY" : [0.9,0.9,0.75,1, 3], "NORMAL" : [1,1,1,1,6], "HARD" : [1.25, 1.25, 1.1, 0.85, 10], "ONSLAUGHT" : [1.5, 1.35, 1.2, 0.7, 14]} #

    sanity_drain, zombie_hp, zombie_damage, turret_bullets, enemy_count = diff_rates[difficulty]

    if not skip_intervals:
        wave_interval = 12
        wave_change_timer = time.time()
    else:
        wave_interval = 2
        wave_change_timer = time.time() - 15

    if multiplayer:
        enemy_count = 1

        packet_dict.clear()


    global barricade_in_hand

    clicked = False
    fps_counter = time.time()


    los_image = pygame.Surface(size, pygame.SRCALPHA, 32).convert_alpha()
    los_image.set_colorkey((255,255,255))
        #
    los_image.set_alpha(150)

    x_vel = 0
    y_vel = 0
    last_hp = 0
    multi_kill_ticks = 0
    multi_kill = 0
    global kills
    kills = 0
    player_Angle = 0
    bullets_new = []
    current_threading = False
    data_collector = None
    collision_check_player = True

    wave = False
    wave_number = 0

    last_ping = 0

    pause = False

    wave_text_tick = -20

    wave_length = 30

    wave_anim_ticks = [0,0]

    tick_rate = 3
    server_tick = 0

    respawn_ticks = 0
    pygame.init()
    pygame.font.init()
    app.pygame.mixer.init()

    app.pygame.mixer.music.fadeout(2000)

    if full_screen_mode:
        full_screen = pygame.display.set_mode(fs_size, pygame.FULLSCREEN, vsync=1) #
        screen =  pygame.Surface(size).convert()
        mouse_conversion = fs_size[0] / size[0]
    else:
        screen = pygame.display.set_mode(size, pygame.RESIZABLE, vsync=1)
        mouse_conversion = 1

    print(mouse_conversion)

    expl1 = func.load_animation("anim/expl1",0,31)

    clock = pygame.time.Clock()
    multiplayer_actors = {}
    if multiplayer:

        for y in players:
            if y == "" or y == self_name:
                continue
            multiplayer_actors[y] = enemies.Player_Multi(y)
    enemy_up_time = time.time()









    weapon_keys = list(weapons.keys())
    print("KEYS",weapon_keys)


    #multiplayer = True









    active_maps = [map]

    enemy_list.clear()
    turret_list.clear()
    burn_list.clear()



    fps = []
    block_movement_polygons = map.get_polygons()

    map.compile_navmesh(mouse_conversion)


    map_render = map.render(mouse_conversion).convert()



    # NAV_MESH = map2.compile_navmesh(mouse_conversion)
    # map_render2 = map2.render(mouse_conversion).convert()

    walls_filtered = []
    global map_boundaries
    map_boundaries = [0,0]

    map_conversion = 1920/854

    for map_1 in active_maps:
        walls_filtered += map.generate_wall_structure()
        for i in range(2):
            end_point = (map_1.__dict__["pos"][i]*map_conversion + map_1.__dict__["size"][i])/map_conversion
            if map_boundaries[i] < end_point:
                map_boundaries[i] = end_point
    print(map_boundaries)

    wall_points = []
    for x in walls_filtered:
        wall_points.append(x.get_points())

    player_pos = map.get_random_point(walls_filtered)
    camera_pos = [0,0]

    NAV_MESH = []
    try:
        file = open(map.__dict__["nav_mesh_name"], "r")
        lines = file.readlines()
        file.close()
        for line in lines:
            ref_point = {"point" : ast.literal_eval(line), "connected" : []}
            NAV_MESH.append(ref_point)
        for ref_point in NAV_MESH:
            for point_dict in NAV_MESH:
                point = point_dict["point"]
                if point == ref_point["point"]:
                    continue
                if los.check_los(point, ref_point["point"], walls_filtered):
                    ref_point["connected"].append(point)


    except Exception as e:
        print(e)


    interactables = []

    player_inventory = classes.Inventory(interactables, player = True)
    player_inventory.set_inventory({1 : {"item" : items["Molotov"], "amount" : 3 }})



    #player_inventory.set_inventory({8 : {"item" : items["Heroin"], "amount" : 1},9 : {"item" : items["Heroin"], "amount" : 1}, 1: {"item": items["45 ACP"], "amount": 999}, 2: {"item": items["50 CAL"], "amount": 999}, 3: {"item": items["7.62x39MM"], "amount": 999}, 4: {"item": items["12 GAUGE"], "amount": 999}, 5: {"item": items["9MM"], "amount": 999} ,6 : {"item": items["HE Grenade"], "amount": 999}, 7 : {"item": items["Sentry Turret"], "amount": 3}})
    #player_inventory.set_inventory({1: {"item": items["45 ACP"], "amount": 10}, 2 : {"item": items["Sentry Turret"], "amount": 1}, 3 : {"item": items["Barricade"], "amount": 3}})

    for x in map.__dict__["objects"]:
        x.__dict__["inv_save"] = player_inventory
        interactables.append(x)

    player_actor = classes.Player(self_name, turret_bullets)

    player_melee = armory.Melee(strike_count = 2, damage = 35, hostile = False, owner_object = player_actor)




    #draw_los = True

    m_clicked = False



    phase = 0


    #turret_list.append(classes.Turret([100,300],8,10,500,20,500))
    barricade_list = []#[classes.Barricade([100,300], [200,400], map)]
    player_weapons = [give_weapon("M1911"), give_weapon("AR-15"), give_weapon("GLOCK"), give_weapon("AWP"), give_weapon("AK"), give_weapon("SPAS"), give_weapon("P90")]


    c_weapon = (player_weapons[0])
    weapon_scroll = 0

    #pygame.mixer.music.set_volume(0.75)

    pygame.mouse.set_visible(False)
    path = os.path.abspath(os.getcwd()) + "/sound/songs/"
    songs = []
    for file in os.listdir(path):
        if file.endswith(".wav") and file != "menu_loop.wav":
            songs.append("sound/songs/" + file)

    pause_tick = False

    background_surf = pygame.Surface(size)
    background_surf.set_alpha(100)

    glitch = Glitch(screen)

    resume_button = button = Button([size[0]/2,100], "Resume", cont_game, None,gameInstance=pygame,glitchInstance=glitch)
    quit_button = button = Button([size[0]/2,200], "Quit", quit, None,gameInstance=pygame,glitchInstance=glitch)
    drying_time = time.time()


    while 1:



        clock.tick(tick_count)

        t = time.time()
        time_stamps = {}




        mouse_pos = pygame.mouse.get_pos()

        mouse_pos = [mouse_pos[0] / mouse_conversion, mouse_pos[1] / mouse_conversion]

        click_single_tick = False
        if pygame.mouse.get_pressed()[0] and clicked == False:

            clicked = True

            click_single_tick = True

        elif pygame.mouse.get_pressed()[0] == False:
            clicked = False



        if pause:
            pygame.mouse.set_visible(True)




            screen.fill((0,0,0))
            screen.blit(background_surf,(0,0))

            s1 = resume_button.tick(screen, mouse_pos, click_single_tick, glitch)
            quit_button.tick(screen, mouse_pos, click_single_tick, glitch)


            pressed = pygame.key.get_pressed()
            if (pressed[pygame.K_ESCAPE] or s1) and not pause_tick:
                menu_click2.play()
                pause = False
                pause_tick = True
                glitch.glitch_tick = 5
                pygame.mouse.set_visible(False)
                click_single_tick = False
                app.pygame.mixer.music.unpause()

            elif not pressed[pygame.K_ESCAPE]:
                pause_tick = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()

            glitch.tick()
            if full_screen_mode:
                pygame.transform.scale(screen, full_screen.get_rect().size, full_screen)


            pygame.display.update()

            continue


        if app.pygame.mixer.music.get_busy() == False:
            app.pygame.mixer.music.load(func.pick_random_from_list(songs))
            app.pygame.mixer.music.play()



        if time.time() - drying_time > 1:
            map_render.blit(map.__dict__["map_rendered_alpha"],(0,0))
            drying_time = time.time()


        time_stamps["blood_drying"] = time.time() - t
        t = time.time()




        if phase != 4:
            camera_pan = c_weapon.__dict__["view"]
        else:
            camera_pan = 0.2


        m_click = pygame.mouse.get_pressed()[1]

        if m_click == True and m_clicked == False and dev_tools:
            m_clicked = True

            print("CLICK")

            phase += 1


            if phase == 4:
                pygame.mouse.set_visible(True)
            else:
                pygame.mouse.set_visible(False)
            if phase == 7:
                phase = 0


        elif m_click == False:
            m_clicked = False

        r_click = pygame.mouse.get_pressed()[2]

        r_click_tick = False

        if r_click == True and r_clicked == False:
            r_clicked = True
            r_click_tick = True
            print("CLICK")


        elif r_click == False:
            r_clicked = False













        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()


            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    print("Scroll down")
                    searching = True
                    while searching:
                        weapon_scroll -= 1
                        if weapon_scroll == -1:
                            weapon_scroll = len(player_weapons) -1

                        c_weapon = (player_weapons[weapon_scroll])

                        if c_weapon.get_Ammo() != 0 or player_inventory.get_amount_of_type(c_weapon.__dict__["ammo"]) != 0 or c_weapon.__dict__["ammo"] == "INF":
                            searching = False

                elif event.button == 5:
                    print("Scroll up")
                    searching = True
                    while searching:
                        weapon_scroll += 1
                        if weapon_scroll == len(player_weapons):
                            weapon_scroll = 0

                        c_weapon = (player_weapons[weapon_scroll])

                        if c_weapon.get_Ammo() != 0 or player_inventory.get_amount_of_type(c_weapon.__dict__["ammo"]) != 0 or c_weapon.__dict__["ammo"] == "INF":
                            searching = False

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_ESCAPE] and not pause_tick:
            glitch.glitch_tick = 5
            pause = True
            pause_tick = True
            menu_click2.play()
            app.pygame.mixer.music.pause()

        elif not pressed[pygame.K_ESCAPE]:
            pause_tick = False






        screen.fill([0,0,0])
        try:
            fps_counter = time.time() - fps_counter
            fps.insert(0, fps_counter)
            if len(fps) > 60:
                fps.remove(fps[60])

        except Exception as e:
            print("EXCEPTION", e)
        fps_counter = time.time()
        func.keypress_manager(pressed,c_weapon, player_inventory)

        last_camera_pos = camera_pos.copy()


        camera_pos = func.camera_aling(camera_pos,player_pos)
        cam_delta = func.minus_list(last_camera_pos,camera_pos)








        if pressed[pygame.K_TAB] and tab_pressed == False and player_actor.get_hp() > 0:

            tab_pressed = True

            player_inventory.toggle_inv(player_pos = player_pos)

        elif pressed[pygame.K_TAB] == False:
            tab_pressed = False

        f_press = False

        if pressed[pygame.K_f] and f_pressed == False and player_actor.get_hp() > 0:

            f_pressed = True

            f_press = True


        elif pressed[pygame.K_f] == False:
            f_pressed = False


        time_stamps["init"] = time.time() - t
        t = time.time()





        mouse_pos_var = [camera_pan*(mouse_pos[0] - size[0]/2), camera_pan*(mouse_pos[1] - size[1]/2)]

        if player_inventory.get_inv() == False:

            camera_pos = [camera_pos[0] + mouse_pos_var[0], camera_pos[1] + mouse_pos_var[1]]

        for active_map in active_maps:
            #active_map.__dict__["map_rendered"]

            screen.blit(map_render,[-camera_pos[0] + active_map.__dict__["pos"][0],-camera_pos[1] + active_map.__dict__["pos"][1]])



        los_walls = los.walls_generate(walls_filtered,camera_pos)


        time_stamps["walls"] = time.time() - t
        t = time.time()


        pvp = False

        if not pvp:

            if wave:
                if time.time() - wave_change_timer > wave_length:
                    wave = False
                    wave_change_timer = time.time()

                    wave_anim_ticks = [120, 0]
                wave_text_tick += 1


            else:


                if False: #Kill enemies if no wave.

                    if len(enemy_list) != 0:
                        if random.uniform(0,1) < 0.1:
                            func.pick_random_from_list(enemy_list).kill(camera_pos, enemy_list, map_render, silent = True)


                if time.time() - wave_change_timer > wave_interval:
                    wave_length += 3
                    #wave_interval += 1
                    wave = True
                    wave_number += 1

                    wave_text_tick = -20

                    wave_anim_ticks = [0, 120]





            if len(enemy_list) < (enemy_count/(player_actor.__dict__["sanity"]/100+0.25)) and wave:
                type = "normal"
                type_drop = random.uniform(0,1)
                if type_drop < 0.02:
                    type = "big"
                elif type_drop < 0.05:
                    type = "bomber"


                zombo = enemies.Zombie(map.get_random_point(walls_filtered, p_pos = player_pos),interactables, player_actor, NAV_MESH, walls_filtered, hp_diff = zombie_hp, dam_diff = zombie_damage, type = type, wall_points = wall_points, player_ref = player_actor, identificator = random.randint(0,4096))
                print(f"Zombie spawned with id {zombo.identificator}")
                enemy_list.append(zombo)
                if multiplayer:
                    if "zombies" not in packet_dict:
                        packet_dict["zombies"] = []
                    packet_dict["zombies"].append(zombo)

            #func.print_s(screen, str(round(enemy_count/((player_actor.__dict__["sanity"]/100)+0.25),3)),3)

            if time.time() - enemy_up_time > 20 and enemy_count != -1:
                enemy_up_time = time.time()
                enemy_count += 1
        for x in barricade_list:
            if x.tick(screen, camera_pos, map = map) == "KILL":
                barricade_list.remove(x)

        time_stamps["barricade"] = time.time() - t
        t = time.time()

        for x in turret_list:
            x.tick(screen, camera_pos,enemy_list,0, walls_filtered, player_pos)
        time_stamps["turrets"] = time.time() - t
        t = time.time()
        delete_list = []
        for x in interactables:
            x.__dict__["inv_save"] = player_inventory
            if x.__dict__["alive"] == False:
                delete_list.append(x)
            else:
                x.tick(screen, player_pos, camera_pos)

        time_stamps["interactables"] = time.time() - t
        t = time.time()

        for x in delete_list:
            interactables.remove(x)

        for x in particle_list:
            x.tick(screen, camera_pos, map)

        time_stamps["particles"] = time.time() - t
        t = time.time()

        if multiplayer:

            if data_collector == None or data_collector.is_alive() == False and server_tick == tick_rate:

                try:
                    ping = time.time() - thread_start - 1/60
                except:
                    pass
                thread_start = time.time()


                x_pos_1 = str(round(player_pos[0]))
                y_pos_1 = str(round(player_pos[1]))
                angle_1 = str(round(player_actor.get_angle()))

                packet = "PACKET\nPLAYER:" + self_name + "_" + x_pos_1 + "_" + y_pos_1 + "_" + angle_1 + "_" + str(player_actor.get_hp()) + "\n"



                for type_1 in packet_dict:
                    for x in packet_dict[type_1]:
                        packet += x.get_string() + "\n"

                for issue in zombie_events:
                    packet += issue + "\n"
                packet += "#END"

                packet_dict.clear()

                zomb_info = [interactables, camera_pos, map_render, NAV_MESH, walls_filtered, zombie_hp, zombie_damage]
                data_collector = threading.Thread(target = thread_data_collect, args = (net, packet, player_actor, multiplayer_actors, bullet_list, grenade_list, current_threading, zomb_info))
                data_collector.start()

                server_tick = 0
            if server_tick < tick_rate:
                server_tick += 1

            for x in multiplayer_actors:
                multiplayer_actors[x].tick(screen, player_pos, camera_pos, walls_filtered)

        bullet_list_copy = bullet_list.copy()
        grenade_list_copy = grenade_list.copy()



        grenade_throw_string = ""

        if pressed[pygame.K_g] and grenade_throw == False and player_actor.get_hp() > 0:

            grenade_throw = True

            if player_inventory.get_amount_of_type("HE Grenade") > 0:
                grenade_list.append(armory.Grenade(player_pos, func.minus(mouse_pos, camera_pos), "HE Grenade"))
                player_inventory.remove_amount("HE Grenade",1)
                print("throwing nade")

            elif player_inventory.get_amount_of_type("Molotov") > 0:
                grenade_list.append(armory.Grenade(player_pos, func.minus(mouse_pos, camera_pos), "Molotov"))
                player_inventory.remove_amount("Molotov",1)
                print("throwing nade")

        elif pressed[pygame.K_g] == False:
            grenade_throw = False


        last_bullet_list = tuple(bullet_list)

        if player_actor.get_hp() > 0:

            x_diff = (mouse_pos[0]+camera_pos[0])-player_pos[0]
            y_diff = (mouse_pos[1]+ camera_pos[1])-player_pos[1]

            try:
                angle = math.atan(x_diff/y_diff) * 180/math.pi +90
                if (x_diff < 0 and y_diff > 0) or (x_diff > 0 and y_diff > 0):
                    angle += 180
            except:
                angle = 0

            player_actor.set_aim_at(angle)

            weapon_pan_rate = c_weapon.__dict__["handling"]

            player_angle = player_actor.get_angle()

            if abs(angle - player_angle) > 1:
                player_angle = player_angle + los.get_angle_diff(angle, player_angle)*weapon_pan_rate
            else:
                player_angle = angle

            player_actor.set_angle(player_angle)

            if c_weapon.__dict__["_Weapon__name"] in ["GLOCK", "M1911"]:
                pl = player_pistol
            else:
                pl = player

            func.render_player(screen, mouse_pos, pl,player_pos, camera_pos, player_actor)

            player_pos, x_vel, y_vel = func.player_movement2(pressed,player_pos,x_vel,y_vel)
            if collision_check_player:
                #angle_coll = map.check_collision(player_pos, map_boundaries, collision_box = 10, screen = screen, x_vel = x_vel, y_vel = y_vel, phase = phase)
                collision_types, angle_coll = map.checkcollision(player_pos,[x_vel, y_vel], 10, map_boundaries, ignore_barricades = True)
                if angle_coll:
                    #dddwwwfunc.debug_render(math.degrees(angle_coll))
                    player_pos = angle_coll

            player_actor.set_pos(player_pos)

            if player_actor.knockback_tick != 0:

                player_actor.pos = [player_actor.pos[0] + math.cos(player_actor.knockback_angle) * player_actor.knockback_tick**0.5, player_actor.pos[1] - math.sin(player_actor.knockback_angle) *player_actor.knockback_tick**0.5]
                player_actor.knockback_tick -= 1

            player_pos = player_actor.pos

            for x in burn_list:
                if los.get_dist_points(x.pos, player_pos) < 25:
                    player_actor.set_hp(1, reduce = True)

            if player_actor.__dict__["barricade_in_hand"] != None:
                func.print_s(screen, str(player_actor.__dict__["barricade_in_hand"].__dict__["stage"]), 3)
                result = player_actor.__dict__["barricade_in_hand"].tick(screen, camera_pos, mouse_pos, click_single_tick, map)
                if result == True:
                    barricade_list.append(player_actor.__dict__["barricade_in_hand"])
                    player_actor.__dict__["barricade_in_hand"] = None
                elif result == "revert":
                    player_inventory.append_to_inv(items["Barricade"], 1)
                    player_actor.__dict__["barricade_in_hand"] = None
            else:


                if player_inventory.get_inv() == False:
                    firing_tick = func.weapon_fire(c_weapon, player_inventory, player_actor.get_angle(), player_pos, screen)
                    player_melee.tick(screen, r_click_tick)

            player_alive = True

        else:

            if player_alive:
                func.list_play(death_sounds)
                player_alive = False
                respawn_ticks = 120
                for i in range(5):
                    particle_list.append(classes.Particle(func.minus(player_pos, camera_pos), type = "blood_particle", magnitude = 1.2,screen = map_render))

            if respawn_ticks != 0:
                respawn_ticks -= 1
            else:
                player_actor.set_hp(100)
                player_pos = map.get_random_point(walls_filtered, enemies = enemy_list)
                #c_weapon = give_weapon(player_we[weapon_scroll])

        c_weapon.add_to_spread(math.sqrt(x_vel**2 + y_vel**2)/10)


        if last_hp == player_actor.get_hp() and player_alive == True:
            free_tick += 1
            if free_tick > 60 and player_actor.get_hp() < 100:
                player_actor.set_hp(-1, reduce = True)




        else:
            free_tick = 0
            #glitch.glitch_tick = 5

        time_stamps["player"] = time.time() - t
        t = time.time()


        closest = 1000
        closest_prompt = None
        for x in interactables:

            dist = x.prompt_dist(player_pos)
            if dist:
                if dist < closest:
                    closest_prompt = x
                    closest = dist

        if closest_prompt != None:
            closest_prompt.tick_prompt(screen, player_pos, camera_pos, f_press = f_press)

        last_hp = player_actor.get_hp()
        if multi_kill_ticks != 0:
            multi_kill_ticks -= 1
        else:
            multi_kill = 0

        time_stamps["prompts"] = time.time() - t
        t = time.time()




        for enemy in enemy_list:
            enemy.tick(screen, map_boundaries, player_actor, camera_pos, map, walls_filtered, NAV_MESH, map_render, phase = phase, wall_points = wall_points)

        time_stamps["enemies"] = time.time() - t
        t = time.time()



        i2 = []
        for x in bullet_list:
            if x not in last_bullet_list:
                i2.append(x)
            kills_bullet = x.move_and_draw_Bullet(screen, camera_pos, map_boundaries, map, enemy_list, player_actor, draw_blood_parts = map_render, dummies = multiplayer_actors)
            if kills_bullet != 0 and kills_bullet != None:
                kills += kills_bullet
                multi_kill += kills_bullet

                if multi_kill > 99:
                    multi_kill = 1


                multi_kill_ticks = 45
                kill_counter = classes.kill_count_render(multi_kill, kill_rgb)


        last_bullet_list = tuple(bullet_list)

        bullets_new = tuple(i2)

        time_stamps["bullets"] = time.time() - t
        t = time.time()


        for x in grenade_list:
            x.tick(screen, map_boundaries, player_pos, camera_pos, grenade_list, explosions, expl1, map, walls_filtered)
        mp = multi_kill
        for x in explosions:
            m_k, m_k_t = x.tick(screen, player_actor, enemy_list ,map_render,camera_pos,explosions, multi_kill, multi_kill_ticks, walls_filtered)

            if m_k != None:
                multi_kill = m_k

            if m_k_t != None:
                multi_kill_ticks = m_k_t

        for x in burn_list:
            x.tick(screen, map_render)

        if mp != multi_kill:
            kill_counter = classes.kill_count_render(multi_kill, kill_rgb)








        time_stamps["misc"] = time.time() - t
        t = time.time()


        if draw_los:
            los_image, draw_time = los.render_los_image(los_image, phase, camera_pos, player_pos,map, los_walls, debug_angle = player_actor.get_angle())
            time_stamps["los_compute"] = time.time() - t
            t = time.time()
            #draw_time = 0
            start = time.time()

            screen.blit(los_image, (0, 0))

            draw_time2 = time.time() - start

            draw_time += time.time() - start

            # los_image2 = pygame.transform.scale(los_image, [1920,1080])
            #
            #
            # los_image2.set_colorkey((255,255,255))
            #
            # los_image2.set_alpha(100)
            #
            # screen.blit(los_image2, (0,0))
            #
            #
            #
            # func.debug_render(draw_time)





            #screen.blit(los_image2,(0,0))



        #pygame.transform.scale(screen, (1920,1080), fullscreen)

        try:
            if multiplayer:
                func.print_s(screen, "PING: " + str(round(last_ping*1000)) + "ms", 3)

                last_ping = last_ping * 59/60 + ping/60


        except Exception as e:
            print(e)

        time_stamps["los_draw"] = time.time() - t
        t = time.time()


        if draw_los:

            if 60*draw_time < 55:
                color = [255,255,255]
            else:
                color = [255,0,0]



            los_total_draw_time_frame = round(60*draw_time,3)

            if los_total_draw_time_frame < 0.8:
                color = [255,255,255]
            else:
                color = [255,0,0]

            #func.print_s(screen, ("LOS DRAW TIME:" + str(los_total_draw_time_frame) + " frames."), 2, color)

            perc1 = round(100*draw_time/(draw_time+draw_time2))
            perc2 = round(100*draw_time2/(draw_time+draw_time2))

        #func.print_s(screen, str(perc1) + "% drawing/" + str(perc2) + "% blitting.", 3, color)

        if phase != 0:
            if phase == 1:
                t = "LINE OF SIGHT, POINTS"
            elif phase == 2:
                t = "LINE OF SIGHT, INTERSECT"
            elif phase == 3:
                t = "COLLISION"
            elif phase == 4:
                t = "NAV MESH"
            elif phase == 5:
                t = "RENDER TIMES"
            elif phase == 6:
                t = "ENEMY DEBUG"

            text = terminal3.render("DEVSCREEN: " + t, False, [255,255,255])
            screen.blit(text, [200, 20])


        if player_actor.get_hp() > 0:
            func.draw_HUD(screen, player_inventory, cam_delta, camera_pos, c_weapon, player_actor, mouse_pos, clicked, r_click_tick,wave, wave_anim_ticks, wave_text_tick, wave_number)
            player_actor.set_sanity(0.005*sanity_drain)


            if phase == 3:
                map_points = map.__dict__["points_inside_polygons"]
                map_polygons = map.__dict__["polygons"]
                for point in map_points:
                    pygame.draw.circle(screen, [255,0,0], [point[0] - camera_pos[0], point[1] - camera_pos[1]], 5)

                for a,b,c,d in map_polygons:
                    for e,f in [[a,b], [b,c], [c,d], [d,a]]:
                        pygame.draw.line(screen, [255,255,255], [e[0] - camera_pos[0], e[1] - camera_pos[1]], [f[0] - camera_pos[0], f[1] - camera_pos[1]])


            if phase == 4:
                mo_pos_real = [mouse_pos[0] + camera_pos[0], mouse_pos[1] + camera_pos[1]]
                if r_click_tick:
                    ref_point = {"point" : [int(mo_pos_real[0]), int(mo_pos_real[1])], "connected" : []}


                    for point_dict in NAV_MESH:
                        point = point_dict["point"]
                        if point == ref_point["point"]:
                            continue
                        if los.check_los(point, ref_point["point"], walls_filtered):
                            ref_point["connected"].append(point)

                    NAV_MESH.append(ref_point)

                    file = open("nav_mesh.txt", "a")
                    file.write(str(ref_point["point"]) + "\n")
                    file.close()



                text = terminal3.render("APPARENT POS: " +str(round(mo_pos_real[0])) + " " +  str(round(mo_pos_real[1])), False, [255,255,255])
                screen.blit(text, [mouse_pos[0] + 20, mouse_pos[1] + 20])
                pygame.draw.line(screen, [255,255,255], mouse_pos, [mouse_pos[0] + 20, mouse_pos[1] + 20])
                pos = [(mouse_pos[0] + camera_pos[0]) * mouse_conversion, (mouse_pos[1] + camera_pos[1]) * mouse_conversion]
                text = terminal3.render("REAL POS: " + str(round(pos[0])) + " " +  str(round(pos[1])), False, [255,255,255])
                screen.blit(text, [mouse_pos[0] + 20, mouse_pos[1] + 40])



                for point_dict in NAV_MESH:
                    point = point_dict["point"]
                    pygame.draw.circle(screen, [255,0,0], [point[0] - camera_pos[0], point[1] - camera_pos[1]], 5)
                    for point_2 in point_dict["connected"]:
                        pygame.draw.line(screen, [255,255,255], [point[0] - camera_pos[0], point[1] - camera_pos[1]], [point_2[0] - camera_pos[0], point_2[1] - camera_pos[1]],1)

                calc_time_1 = time.time()
                route = func.calc_route(player_pos, mo_pos_real, NAV_MESH, walls_filtered)
                calc_time_2 = time.time() - calc_time_1
                point_2 = player_pos
                for point in route:
                    pygame.draw.line(screen, [255,0,0], [point[0] - camera_pos[0], point[1] - camera_pos[1]], [point_2[0] - camera_pos[0], point_2[1] - camera_pos[1]], 4)
                    point_2 = point
                pygame.draw.line(screen, [255,0,0], [mo_pos_real[0] - camera_pos[0], mo_pos_real[1] - camera_pos[1]], [point_2[0] - camera_pos[0], point_2[1] - camera_pos[1]], 4)

                text = terminal3.render("CALC TIME: " + str(round(calc_time_2*1000,2)) + "ms", False, [255,255,255])
                screen.blit(text, [mouse_pos[0] + 20, mouse_pos[1] + 60])

        else:
            text = terminal.render("RESPAWN IN", False, [255,255,255])
            pos = [size[0] / 2, size[1] / 2-40]
            screen.blit(text, [pos[0] - text.get_rect().center[0], pos[1] - text.get_rect().center[1]])

            if respawn_ticks <= 40:
                t = "1"
            elif respawn_ticks <= 80:
                t = "2"
            else:
                t = "3"

            text = terminal2.render(t, False, [255,255,255])
            pos = [size[0] / 2, size[1] / 2]
            screen.blit(text, [pos[0] - text.get_rect().center[0], pos[1] - text.get_rect().center[1]])



        try:
            kill_counter.tick(screen, cam_delta, kill_counter)
        except:
            pass




        if multiplayer:
            text = terminal3.render("MULTIPLAYER", False, [255,255,255])
            screen.blit(text, [400,20])
            text = terminal3.render(self_name, False, [255,255,255])
            screen.blit(text, [400,40])


        if phase != 5:
            try:
                func.print_s(screen, "FPS: " + str(round(1/(sum(fps)/60))), 1)
                pass
            except:
                pass

            func.print_s(screen, "KILLS: " + str(kills), 2)



            #func.print_s(screen, "WAVE: " + str(wave_number), 3)

            # if c_weapon.__dict__["burst"]:
            #
            #     func.print_s(screen, "burst_tick: " + str(c_weapon.__dict__["burst_tick"]), 3)
            #     func.print_s(screen, "current_burst_bullet: " + str(c_weapon.__dict__["current_burst_bullet"]), 4)
            #     func.print_s(screen, "weapon_fire_Tick: " + str(c_weapon.weapon_fire_Tick()), 5)


        else:
            obje = enumerate(time_stamps, 1)
            total = 0
            try:
                for i, k in obje:
                    time_stamps[k] = time_stamps[k]*1/20 + last_time_stamp[k]*19/20

                    color = [255,round(255/(1 + time_stamps[k]*1000)), round(255/(1 + time_stamps[k]*1000))]


                    func.print_s(screen, k + ":" + str(round(time_stamps[k]*1000,1)) + "ms", i, color = color)

                    total += time_stamps[k]
                if total > 1/60:
                    color = [255,0,0]
                else:
                    color = [255,255,255]
                func.print_s(screen, "TOTAL" + ":" + str(round(total*1000,1)) + "ms (" + str(round(1/total)) + "FPS)", i+1, color = color)
            except Exception as e:
                print(e)


        last_time_stamp = time_stamps.copy()
        #func.print_s(screen, str(wave_text_tick), 5)


        if wave_anim_ticks[0] != 0:
            wave_anim_ticks[0] -= 1
        if wave_anim_ticks[1] != 0:
            wave_anim_ticks[1] -= 1
        try:

            if multiplayer:
                for list_1, list_copy, slot in [[bullet_list, bullet_list_copy, "bullets"], [grenade_list, grenade_list_copy, "grenades"]]:

                    if slot not in packet_dict:
                        packet_dict[slot] = []

                    for object in reversed(list_1):
                        if object not in list_copy and object.__dict__["mp"] == False:
                            packet_dict[slot].append(object)
                        else:
                            break
                    list_copy = list_1.copy()


        except Exception as e:
            print(e)






        if pause:
            background_surf.blit(screen, (0,0))
        glitch.tick()
        if full_screen_mode:
            pygame.transform.scale(screen, full_screen.get_rect().size, full_screen)
        melee_list.clear()
        pygame.display.update()

if __name__ == "__main__":
    main()
