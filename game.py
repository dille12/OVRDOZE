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

from values import *
import classes
import func

print("IMPORTS COMPLETE")



terminal = pygame.font.Font('texture/terminal.ttf', 20)
terminal2 = pygame.font.Font('texture/terminal.ttf', 30)
terminal3 = pygame.font.Font('texture/terminal.ttf', 10)

weapons = {

"AK": classes.Weapon("AK47",
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
                        piercing = True),

"MINIGUN": classes.Weapon("MINIGUN",
                        clip_s = 999,
                        fire_r = 1000,
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
                        piercing = True),

"SPAS": classes.Weapon("SPAS-12",
                        clip_s = 6,
                        fire_r = 120,
                        spread = 15,
                        spread_per_bullet = 1,
                        spread_r = 0.94,
                        reload_r = 60,
                        damage = 22,
                        bullet_speed = 15,
                        bullets_at_once = 8,
                        shotgun = True,
                        semi_auto = True,
                        sounds = shotgun_sounds,
                        ammo_cap_lvlup = 2,
                        image = "spas12.png",
                        ammo = "12 GAUGE"),

"P90": classes.Weapon("P90",
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
                        ammo = "9MM"),
"GLOCK": classes.Weapon("GLOCK",
                        clip_s = 12,
                        fire_r = 2000,
                        spread = 5,
                        spread_r = 0.94,
                        reload_r = 30,
                        damage = 22,
                        semi_auto = True,
                        bullets_at_once = 1,
                        shotgun = False,
                        ammo_cap_lvlup = 1,
                        image = "glock.png",
                        ammo = "45 ACP"),

"AWP": classes.Weapon("AWP",
                        clip_s = 10,
                        fire_r = 50,
                        spread = 1,
                        spread_r = 0.965,
                        spread_per_bullet = 25,
                        reload_r = 120,
                        damage = 150,
                        bullets_at_once = 1,
                        sounds = sniper_rifle_sounds,
                        bullet_speed = 55,
                        shotgun = False,
                        ammo_cap_lvlup = 1,
                        image = "awp.png",
                        ammo = "50 CAL",
                        piercing = True),
}

def give_weapon(gun):
    return weapons[gun].copy()



# if multiplayer:
#     net = Network()
#     print("MULTIPLAYER")
# else:
#     print("SINGLEPLAYER")

full_screen_mode = True

def thread_data_collect(net, player_pos, player_Angle, bullets_new, grenade_throw_string, player_actor, bullet_list, grenade_list, multiplayer_actors, current_threading):
    try:
        x_pos_1 = round(player_pos[0])
        y_pos_1 = round(player_pos[1])
        angle_1 = round(player_Angle)
        string = ":"
        for bull in bullets_new:
            string += bull.get_string()
            string += ","
        if grenade_throw_string != "":
            string += ":"
            string += grenade_throw_string

        player_info = net.send("pl_i:" + str(x_pos_1) + "_" + str(y_pos_1) + "_" + str(angle_1) + "_" + str(round(player_actor.get_hp())) + string)
        player_info = player_info.split("REPLY")[1]
        if not player_info == "%/":
            info = player_info.strip(" ").split("#")
            client_info = info[0]
            if len(info) == 2 or len(info) == 3:
                bullets = info[1]
                for bullet in bullets.split("%"):
                    #print(bullet)
                    try:
                        x1,y1,a1,d1,s1 = bullet.split("_")
                        bullet_list.append(classes.Bullet(camera_pos, [int(x1), int(y1)],int(a1),int(d1), speed = int(s1)))
                        #print("Bullet created")
                    except Exception as e:
                        #print("BULLET CREATING ERROR:")
                        #print(traceback.print_exc())
                        pass
            if len(info) == 3:
                grenades = info[2]
                print(grenades)
                for grenade in grenades.split("%"):
                    try:
                        x1,y1,a1,d1 = grenade.split("_")
                        grenade_list.append(classes.Grenade([int(x1), int(y1)], [int(a1),int(d1)]))
                    except:
                        pass



            for client_info in player_info.split("%"):
                try:
                    info = client_info.split("_")
                    multiplayer_actors[info[0]].set_values(info[1], info[2], info[3], info[4])
                except Exception as e:
                    print(e)




    except Exception as e:
        print("CLIENT ERROR:", traceback.print_exc())
        pass
    current_threading = False




def main(multiplayer = False, net = None, host = False, players = None, self_name = None):
    player_pos = [50,50]
    camera_pos = [0,0]
    x_vel = 0
    y_vel = 0
    last_hp = 0
    multi_kill_ticks = 0
    multi_kill = 0
    kills = 0
    player_Angle = 0
    bullets_new = []
    current_threading = False
    data_collector = None
    collision_check_player = True

    tick_rate = 1
    server_tick = 0

    respawn_ticks = 0
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()
    if full_screen_mode:
        full_screen = pygame.display.set_mode(fs_size, pygame.FULLSCREEN)
        screen =  pygame.Surface(size).convert()
        mouse_conversion = fs_size[0] / size[0]
    else:
        screen = pygame.display.set_mode(size)
        mouse_conversion = 1

    print(mouse_conversion)

    expl1 = func.load_animation("anim/expl1",0,31)

    clock = pygame.time.Clock()
    multiplayer_actors = {}
    if multiplayer:

        for y in players.split("/"):
            if y == "" or y == self_name:
                continue
            multiplayer_actors[y] = classes.Player_Multi(y)
    else:
        enemy_count = 0
        enemy_up_time = time.time()









    weapon_keys = list(weapons.keys())
    print("KEYS",weapon_keys)


    #multiplayer = True






    map1 = Map("Paska", "map.png", [0,0], mouse_conversion, [2000,1500],
    [ #x,y,width,height
    [2,470,125,186],
    [377,470,125,186],
    [502,376,125,561],
    [501,2,125,95],
    [253,1219,1122,93], #
    [502,1124,123,93],
    [1125,1030,124,189], #
    [1125,283,125,469],
    [1126,2,125,93],
    [1250,375,244,94],
    [1748,376,252,93],
    [1624,1218,376,93]

    ],

    []
    )

    map2 = Map("Paska2", "map2.png", [0,0], mouse_conversion, [2500,2500],
    [ #x,y,width,height
    [467,2,156,74],
    [2,312,621,155],
    [476,233,147,78],
    [311,781,156,783],
    [311,1565, 939, 156],
    [2, 2034, 465, 156],
    [781, 2034, 312, 156],
    [937,2191,156, 290],
    [1094, 311, 625, 156],
    [1094, 466, 155, 313],
    [1564, 467, 157, 1096],
    [1094, 1095, 470, 155],
    [1720, 1407, 470, 156],
    [2034, 1562, 156, 627],
    [1407, 2034, 628, 155],
    [2034, 2, 146, 309],
    [2034, 626, 157, 311],
    [2190, 781, 311, 156]
    ],

    []
    )

    map = map2

    active_maps = [map]



    fps = []
    block_movement_polygons = map.get_polygons()

    map.compile_navmesh(mouse_conversion)


    map_render = map.render(mouse_conversion).convert()

    # NAV_MESH = map2.compile_navmesh(mouse_conversion)
    # map_render2 = map2.render(mouse_conversion).convert()

    walls_filtered = []
    global map_boundaries
    map_boundaries = [0,0]

    for map_1 in active_maps:
        walls_filtered += map.generate_wall_structure()
        for i in range(2):
            end_point = (map_1.__dict__["pos"][i]*mouse_conversion + map_1.__dict__["size"][i])/mouse_conversion
            if map_boundaries[i] < end_point:
                map_boundaries[i] = end_point
    print(map_boundaries)

    NAV_MESH = []
    try:
        file = open("nav_mesh.txt", "r")
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


    interctables = []

    player_inventory = classes.Inventory(interctables, player = True)

    interctables.append(classes.Intercatable([300,200], player_inventory, name = "Box"))
    # interctables.append(classes.Intercatable([400,200], player_inventory, name = "Box"))
    # interctables.append(classes.Intercatable([160,145], player_inventory, name = "Box"))
    # interctables.append(classes.Intercatable([810,600], player_inventory, name = "Box"))
    #, classes.Intercatable([600,400], player_inventory, name = "Crate")]




    player_actor = classes.Player()




    draw_los = True

    m_clicked = False



    phase = 0


    turret_list.append(classes.Turret([100,300],8,10,500,20,500))

    player_weapons = [give_weapon("GLOCK"), give_weapon("AWP"), give_weapon("MINIGUN"), give_weapon("AK"), give_weapon("SPAS"), give_weapon("P90")]

    c_weapon = (player_weapons[0])
    weapon_scroll = 0

    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.75)

    pygame.mouse.set_visible(False)


    while 1:


        m_click = pygame.mouse.get_pressed()[1]

        if m_click == True and m_clicked == False:
            m_clicked = True

            print("CLICK")

            phase += 1


            if phase == 4:
                pygame.mouse.set_visible(True)
            else:
                pygame.mouse.set_visible(False)
            if phase == 5:
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










        clock.tick(tick_count)


        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()


            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    print("Scroll down")
                    weapon_scroll -= 1
                    if weapon_scroll == -1:
                        weapon_scroll = len(player_weapons) -1

                    c_weapon = (player_weapons[weapon_scroll])
                elif event.button == 5:
                    print("Scroll up")
                    weapon_scroll += 1
                    if weapon_scroll == len(player_weapons):
                        weapon_scroll = 0

                    c_weapon = (player_weapons[weapon_scroll])

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_ESCAPE]:

            sys.exit()




        screen.fill([0,0,0])
        try:
            fps_counter = time.time() - fps_counter
            fps.insert(0, fps_counter)
            if len(fps) > 60:
                fps.remove(fps[60])

        except Exception as e:
            print(e)
        fps_counter = time.time()
        func.keypress_manager(pressed,c_weapon, player_inventory)

        last_camera_pos = camera_pos.copy()


        camera_pos = func.camera_aling(camera_pos,player_pos)
        cam_delta = func.minus_list(last_camera_pos,camera_pos)
        mouse_pos = pygame.mouse.get_pos()

        mouse_pos = [mouse_pos[0] / mouse_conversion, mouse_pos[1] / mouse_conversion]

        if pygame.mouse.get_pressed()[0] and clicked == False:

            clicked = True

        elif pygame.mouse.get_pressed()[0] == False:
            clicked = False


        grenade_throw_string = ""

        if pressed[pygame.K_g] and grenade_throw == False and player_actor.get_hp() > 0:

            grenade_throw = True

            if player_inventory.get_amount_of_type("HE Grenade") > 0:

                grenade_list.append(classes.Grenade(player_pos, func.minus(mouse_pos, camera_pos)))
                grenade_throw_string = str(round(player_pos[0])) + "_" + str(round(player_pos[1])) + "_"+ str(round(func.minus(mouse_pos, camera_pos)[0])) + "_"+ str(round(func.minus(mouse_pos, camera_pos)[1]))
                player_inventory.remove_amount("HE Grenade",1)
                print("throwing nade")

        elif pressed[pygame.K_g] == False:
            grenade_throw = False



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





        mouse_pos_var = [camera_pan*(mouse_pos[0] - size[0]/2), camera_pan*(mouse_pos[1] - size[1]/2)]

        if player_inventory.get_inv() == False:

            camera_pos = [camera_pos[0] + mouse_pos_var[0], camera_pos[1] + mouse_pos_var[1]]

        for active_map in active_maps:
            #active_map.__dict__["map_rendered"]

            screen.blit(map_render,[-camera_pos[0] + active_map.__dict__["pos"][0],-camera_pos[1] + active_map.__dict__["pos"][1]])



        los_walls = los.walls_generate(walls_filtered,camera_pos)




        if not multiplayer:
            if len(enemy_list) < enemy_count:
                enemy_list.append(classes.Zombie(map.get_random_point(walls_filtered, p_pos = player_pos),interctables, player_pos, NAV_MESH, walls_filtered))

            if time.time() - enemy_up_time > 20 and enemy_count != 0:
                enemy_up_time = time.time()
                enemy_count += 1



        for x in turret_list:
            x.tick(screen, camera_pos,enemy_list,0, walls_filtered)
        delete_list = []
        for x in interctables:
            x.__dict__["inv_save"] = player_inventory
            if x.__dict__["alive"] == False:
                delete_list.append(x)
            else:
                x.tick(screen, player_pos, camera_pos)
        for x in delete_list:
            interctables.remove(x)

        for x in particle_list:
            x.tick(screen, camera_pos)

        if multiplayer:

            if server_tick == tick_rate:

                if data_collector == None or data_collector.is_alive() == False:
                    print("Trying to thread")
                    data_collector = threading.Thread(target = thread_data_collect, args = (net, player_pos, player_Angle, bullets_new, grenade_throw_string, player_actor, bullet_list, grenade_list, multiplayer_actors, current_threading))
                    data_collector.start()
                    last_thread = time.time()
                    server_tick = 1

                else:
                    print("CURRENTLY THREADING CANT GET NEW INFO")
            else:
                server_tick += 1


            for x in multiplayer_actors:
                multiplayer_actors[x].tick(screen, player_pos, camera_pos, walls_filtered)

        last_bullet_list = tuple(bullet_list)

        if player_actor.get_hp() > 0:

            player_Angle = func.render_player(screen, mouse_pos, player,player_pos, camera_pos)

            player_pos, x_vel, y_vel = func.player_movement2(pressed,player_pos,x_vel,y_vel)
            if collision_check_player:
                angle_coll = map.check_collision(player_pos, map_boundaries, collision_box = 10, screen = screen, x_vel = x_vel, y_vel = y_vel, phase = phase)
                if angle_coll:
                    #dddwwwfunc.debug_render(math.degrees(angle_coll))
                    player_pos = angle_coll

            player_actor.set_pos(player_pos)
            player_actor.set_angle(player_Angle)

            if player_inventory.get_inv() == False:

                firing_tick = func.weapon_fire(c_weapon, player_inventory, player_Angle, player_pos, screen)

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
        closest = 1000
        closest_prompt = None
        for x in interctables:

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


        for enemy in enemy_list:
            enemy.tick(screen, map_boundaries, player_actor, camera_pos, map, walls_filtered, NAV_MESH)



        i2 = []
        for x in bullet_list:
            if x not in last_bullet_list:
                i2.append(x)
            kill = x.move_and_draw_Bullet(screen, camera_pos, map_boundaries, map, enemy_list, player_actor, draw_blood_parts = map_render, dummies = multiplayer_actors)
            if kill == True:
                kills += 1
                multi_kill += 1
                if multi_kill > 10:
                    multi_kill = 1

                multi_kill_ticks = 120
                kill_counter = classes.kill_count_render(multi_kill, kill_rgb)


        last_bullet_list = tuple(bullet_list)

        bullets_new = tuple(i2)


        for x in grenade_list:
            x.tick(screen, map_boundaries, player_pos, camera_pos, grenade_list, explosions, expl1, map, walls_filtered)
        mp = multi_kill
        for x in explosions:
            multi_kill, multi_kill_ticks = x.tick(screen, player_actor, enemy_list ,map_render,camera_pos,explosions, multi_kill, multi_kill_ticks, walls_filtered)

        if mp != multi_kill:
            kill_counter = classes.kill_count_render(multi_kill, kill_rgb)











        if draw_los:
            los_image, draw_time = los.render_los_image(phase, camera_pos, player_pos,map, los_walls, debug_angle = player_Angle)
            #draw_time = 0
            start = time.time()
            los_image.convert()
            if phase != 7:
                los_image.set_colorkey((255,255,255))
                #
                los_image.set_alpha(200)
            else:
                los_image.set_colorkey((255,200,255))
                los_image.set_alpha(255)
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
            func.print_s(screen, "FPS: " + str(round(1/(sum(fps)/60))), 1)
        except:
            pass

        func.print_s(screen, "KILLS: " + str(kills), 2)
        try:
            if multiplayer:
                func.print_s(screen, "PING: " + str(round((time.time()-last_thread)*1000)) + "ms (" + str(round(1/(time.time()-last_thread))) + "frames)", 3)
        except Exception as e:
            print(e)


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
        if player_actor.get_hp() > 0:
            func.draw_HUD(screen, player_inventory, cam_delta, camera_pos, c_weapon, player_actor, mouse_pos, clicked, r_click_tick)
            player_actor.set_sanity(0.005)


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


        if full_screen_mode:
            pygame.transform.scale(screen, fs_size, full_screen)

        pygame.display.update()

if __name__ == "__main__":
    main()
