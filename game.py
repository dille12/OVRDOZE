import os, sys
import pygame
import math
import random
import time
import mixer
from classtest import *
from _thread import *
import copy
import los
from network import Network

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
                        ammo = "7.62x39MM"),

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
                        spread_r = 0.98,
                        spread_per_bullet = 25,
                        reload_r = 120,
                        damage = 150,
                        bullets_at_once = 1,
                        sounds = sniper_rifle_sounds,
                        bullet_speed = 50,
                        shotgun = False,
                        ammo_cap_lvlup = 1,
                        image = "awp.png",
                        ammo = "50 CAL"),
}

def give_weapon(gun):
    return weapons[gun].copy()



# if multiplayer:
#     net = Network()
#     print("MULTIPLAYER")
# else:
#     print("SINGLEPLAYER")

full_screen_mode = True

def thread_data_collect(net, player_pos, player_Angle, bullets_new, grenade_throw_string, player_actor, bullet_list, grenade_list, multiplayer_actors):


    try:
        print("THREADING")
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
        print("string:", grenade_throw_string)
        player_info = net.send("pl_i:" + str(x_pos_1) + "_" + str(y_pos_1) + "_" + str(angle_1) + "_" + str(round(player_actor.get_hp())) + string)
        if not player_info == "%/":
            info = player_info.strip(" ").split("#")
            #print(info)
            client_info = info[0]
            if len(info) == 2 or len(info) == 3:
                print("Bullet info received")
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
                print("Grenade info received")
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
                    print("SETTING VALUES")
                except Exception as e:
                    print(e)




    except Exception as e:
        print("CLIENT ERROR:", traceback.print_exc())
        pass





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
        enemy_count = 3









    weapon_keys = list(weapons.keys())
    print("KEYS",weapon_keys)


    #multiplayer = True






    map = Map("Paska", mouse_conversion, [2000,1500],
    [ #x,y,width,height
    [2,470,125,186],
    [377,470,125,186],
    [502,376,125,561],
    #[128,844,124,187],
    [501,2,125,95],
    [253,1219,1122,93], #
    [502,1124,123,93],
    #[750,751,126,187],
    [1125,1030,124,189], #
    [1125,283,125,469],
    [1126,2,125,93],
    [1250,375,244,94],
    [1748,376,252,93],
    #[1374,657,245,95],
    #[1624,656,126,280],
    [1624,1218,376,93]



    # [(377,656),(377,470),(502,470),(502,656)],
    # [(502,376+561),(502,376), (502+125,376),(502+125,376+561)],
    #[(300,500),(500,3 00),(700,500),(500,700)]
    ],
    # [
    #
    # [(300,500),(500,300),(700,500),(500,700)]
    # ],
    #[[(200,200),"floor_tile_1",0],[(600,200),"floor_tile_1",0]]
    []
    )

    fps = []
    block_movement_polygons = map.get_polygons()

    NAV_MESH = map.compile_navmesh(mouse_conversion)
    map_render = map.render(mouse_conversion).convert()
    walls_filtered = map.generate_wall_structure()

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


    #turret_list.append(classes.Turret([random.randint(0,300),300],1,2,500,1,1000))

    player_weapons = [give_weapon("GLOCK"), give_weapon("AWP"), give_weapon("AK"), give_weapon("SPAS"), give_weapon("P90")]

    c_weapon = (player_weapons[0])
    weapon_scroll = 0

    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)

    pygame.mouse.set_visible(False)


    while 1:


        m_click = pygame.mouse.get_pressed()[1]

        if m_click == True and m_clicked == False:
            m_clicked = True

            print("CLICK")

            phase += 1
            if phase == 4:
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

        screen.blit(map_render,[-camera_pos[0],-camera_pos[1]])



        los_walls = los.walls_generate(walls_filtered,camera_pos)




        if not multiplayer:
            if len(enemy_list) < enemy_count:
                enemy_list.append(classes.Enemy(map.get_random_point(walls_filtered, p_pos = player_pos), weapons,interctables))


        for x in turret_list:
            x.tick(screen, camera_pos,enemy_list,0)
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

            print("Trying to thread")
            start_new_thread(thread_data_collect, (net, player_pos, player_Angle, bullets_new, grenade_throw_string, player_actor, bullet_list, grenade_list, multiplayer_actors))
            print("Success")

            for x in multiplayer_actors:
                multiplayer_actors[x].tick(screen, player_pos, camera_pos, walls_filtered)

        last_bullet_list = tuple(bullet_list)

        if player_actor.get_hp() > 0:

            player_Angle = func.render_player(screen, mouse_pos, player,player_pos, camera_pos)

            player_pos, x_vel, y_vel = func.player_movement2(pressed,player_pos,x_vel,y_vel)
            angle_coll = map.check_collision(player_pos, collision_box = 10, screen = screen, x_vel = x_vel, y_vel = y_vel)
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
            enemy.tick(screen, player_actor, camera_pos, map, walls_filtered)



        i2 = []
        for x in bullet_list:
            if x not in last_bullet_list:
                i2.append(x)
            kill = x.move_and_draw_Bullet(screen, camera_pos, map, enemy_list, player_actor, draw_blood_parts = map_render, dummies = multiplayer_actors)
            if kill == True:
                kills += 1
                multi_kill += 1
                multi_kill_ticks = 120
                kill_counter = classes.kill_count_render(multi_kill, kill_rgb)


        last_bullet_list = tuple(bullet_list)

        bullets_new = tuple(i2)

        for x in grenade_list:
            x.tick(screen, player_pos, camera_pos, grenade_list, explosions, expl1, map, walls_filtered)
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
            if phase != 3:
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
