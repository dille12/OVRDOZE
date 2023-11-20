import os, sys

import math
import random
import time
import mixer
from level import *
from _thread import *
import threading
import copy
import los
import render_los_image_jit
from network import Network
import ast
from app import App
from weapon_button import weapon_button
from button import Button
from glitch import Glitch
from values import *
import classes
from classes import items
import func
from dialog import *
from unit_status import UnitStatus
from npcs.zombie import Zombie
from npcs.patrol import Patrol
from anim_list import *
# import path_finding
from weapons.area import Explosion
from scroll_bar import ScrollBar
from game_objects.rain_drop import RainDrop
import highscores
import armory
import objects
from npcs.mp_dummy import Player_Multi
from utilities.storyTeller import storyTeller


import RUN

import enem_obs

print("IMPORTS COMPLETE")


terminal = pygame.font.Font("texture/terminal.ttf", 20)
terminal2 = pygame.font.Font("texture/terminal.ttf", 30)
terminal3 = pygame.font.Font("texture/terminal.ttf", 10)

terminal_map_desc = pygame.font.Font("texture/terminal.ttf", 50)
terminal_map_desc2 = pygame.font.Font("texture/terminal.ttf", 25)

terminal_waveSecs = []
for i in range(4):
    terminal_waveSecs.append(pygame.font.Font("texture/terminal.ttf", 50 + i*10))


def give_weapon(kind, name):
    return armory.__weapons_map[kind][name].copy()


# if multiplayer:
#     net = Network()
#     print("MULTIPLAYER")
# else:
#     print("SINGLEPLAYER")





def write_packet(object):
    string = write_packet.get_string() + "\n"
    return string


def quit(app):
    app.pygame.mixer.music.unload()
    app.write_prefs()
    print("Quitting game")

    RUN.main()


def cont_game(arg):
    return True

songDrops = {
    "Palpitations.wav" : [[29.0, 72.72], [120, 163.63]],
    "Take Me High.wav" : [[48.38, 79.35], [129.67, 160.64]],
    "FullAuto.wav" : [[36.09, 79.39], [126.31, 169.62]],
    "New colors.wav" : [[43.30, 72.18], [122.70, 151.57]],
    "Octane.wav" : [[46.45, 92.90]],
    "ovrdoz.wav" : [[43.82, 68.87], [102.26, 127.30]],
    "Veins.wav" : [[32, 71.11], [110.22, 159.33]],
    "Narcosis.wav" : [[28.02, 70.07], [108.61, 130.65]],
}



def main(
    app,
    multiplayer=False,
    net=None,
    host=False,
    players=None,
    self_name=None,
    difficulty="NORMAL",
    draw_los=True,
    dev_tools=True,
    skip_intervals=False,
    map=None,
):
    print("GAME STARTED WITH", difficulty)

    diff_rates = {
        "NO ENEMIES": [0, 1, 1, 1, -1],
        "EASY": [0.9, 0.9, 0.75, 1, 3],
        "NORMAL": [1, 1, 1, 1, 20],
        "HARD": [1.25, 1.25, 1.1, 0.85, 30],
        "ONSLAUGHT": [1.5, 1.35, 1.2, 0.7, 40],
    }  #



    sanity_drain, zombie_hp, zombie_damage, turret_bullets, enemy_count = diff_rates[
        difficulty
    ]

    print("Enemy count:", enemy_count)

    self_name = app.name

    if multiplayer:
        enemy_count = -1

        packet_dict.clear()

    global barricade_in_hand

    def restart(arg):

        args = (app, self_name, difficulty, draw_los, dev_tools, skip_intervals, map)

        app.start_sp(args)

    clicked = False
    fps_counter = time.time()

    los_image = pygame.Surface(size).convert()
    los_image.set_colorkey((255, 255, 255))
    #
    # los_image.set_alpha(150)

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


    death_wave = -1
    deathMoney = -1


    last_ping = 0

    pause = False

    wave_text_tick = -20

    wave_anim_ticks = [0, 0]

    tick_rate = 3
    server_tick = 0

    respawn_ticks = 0
    app.pygame.init()
    app.pygame.font.init()
    app.pygame.mixer.init()



    level_order = ["Requiem", "Manufactory", "Liberation"]

    print(app)

    screen, mouse_conversion = app.update_screen(return_screen = True)

    weapon_keys = list(armory.__weapons_map["gun"].keys())
    print("KEYS", weapon_keys)

    route = None
    clock = app.pygame.time.Clock()
    app.multiplayer_actors = {}
    print("Initting actors")
    app.multiplayer = multiplayer
    if multiplayer:

        print("MP INIT")
        for y in players:
            print(y)
            if y == "" or y == self_name:
                continue
            app.multiplayer_actors[y] = Player_Multi(y, app, weapons = armory.__weapons_map["gun"])
    print("MP DUMMIES INITTED")
    enemy_up_time = time.time()

    app.weapon_ref = armory.__weapons_map["gun"]

    # multiplayer = True

    active_maps = [map]

    enemy_list.clear()
    turret_list.clear()
    burn_list.clear()

    fps = []

    ### load

    player_inventory = classes.Inventory(app, interactables, player=True)
    turret_bro.clear()

    

    app.day = -1

    print("Loading level...")

    try:

        (
            map,
            map_render,
            los_bg,
            map_boundaries,
            NAV_MESH,
            player_pos,
            camera_pos,
            wall_points,
            walls_filtered,
        ) = load_level(map, mouse_conversion, player_inventory, app, screen)

    except Exception as e:
        print(e)
        RUN.main(ms = "beta")

    print("Level loaded")

    wave = False
    wave_number = 0

    if not skip_intervals:
        wave_interval = 17
        wave_change_timer = time.time()
    else:
        wave_interval = 2
        wave_change_timer = time.time() - 15

    wave_length = 30

    player_actor = classes.Player(app, self_name, turret_bullets, inv = player_inventory)
    app.player_actor_ref = player_actor


    app.storyTeller = storyTeller(app, player_inventory)

    if dev_tools:
        player_inventory.append_to_inv(items["Barricade"], 3)

    player_melee = armory.Melee.Melee(
        strike_count=2, damage=35, hostile=False, owner_object=player_actor
    )
    equipped_gun = None
    # draw_los = True

    m_clicked = False
    grenadeJoyThrow = False

    phase = 0

    # [classes.Barricade([100,300], [200,400], map)]
    player_weapons.clear()
    

    if map.name != "Overworld":
        endless = True
        fn = armory.__weapons_map["gun"]["FN57-S"].copy()
        fn.ammo = "INF"
        player_weapons.append(fn)

    else:
        player_weapons.append(give_weapon("gun", "M1911"))
        endless = False
        dialogue.append(Dialogue("Intro", app))
        player_pos = [25 * multiplier2,950 * multiplier2]


    app.endless = endless




    gun_name_list = [
        "M1911",
        "FN57-S",
        "GLOCK",
        "AR-15",
        "DESERTEAGLE",
        "MP5",
        "AWP",
        "AK47",
        "SPAS-12",
        "P90",
        "SCAR18",
        "RPG-7",
        "M134-MINIGUN",
        "NRG-LMG.Mark1",
        "USAS-15",
        "NRG-SHLL",
    ]
    ruperts_shop_selections.clear()
    for i, x in enumerate(gun_name_list):
        ruperts_shop_selections.append(weapon_button(give_weapon("gun", x), i))

    a = sorted(ruperts_shop_selections, key=lambda x: x.weapon.price)

    ruperts_shop_selections.clear()

    for i, x in enumerate(a):
        x.slot = i
        ruperts_shop_selections.append(x)

    # ruperts_shop_selections.append(weapon_button(give_weapon("gun", "AR-15"),1))
    # ruperts_shop_selections.append(weapon_button(give_weapon("gun", "AK47"),2))
    # ruperts_shop_selections.append(weapon_button(give_weapon("gun", "SPAS-12"),3))
    for weapon_1 in player_weapons:
        not_used_weapons.append(weapon_1.name)

    c_weapon = player_weapons[0]
    weapon_scroll = 0
    newHigh = [False, False]
    if endless:
        player_inventory.columns = 4

    # pygame.mixer.music.set_volume(0.75)

    app.pygame.mouse.set_visible(False)
    path = os.path.abspath(os.getcwd()) + "/sound/songs/"
    songs = []
    for file in os.listdir(path):
        if (
            file.endswith(".wav")
            and "menu_loop" not in file
            and "downtown" not in file
            and "overworld_loop" not in file
        ):
            songs.append("sound/songs/" + file)

    pause_tick = False

    background_surf = app.pygame.Surface(size)
    background_surf.set_alpha(100)

    glitch = Glitch(screen)

    dropIndices = []

    resume_button = Button(
        [size[0] / 2, 100],
        "Resume",
        cont_game,
        None,
        gameInstance=app,
        glitchInstance=glitch,
    )
    quit_button = Button(
        [size[0] / 2, 200],
        "Quit",
        quit,
        app,
        gameInstance=app,
        glitchInstance=glitch,
    )


    retry_button = Button(
        [size[0] / 3, 2 * size[1]/3],
        "Retry",
        restart,
        None,
        gameInstance=app,
        glitchInstance=glitch,
        controller=0,
    )
    quit_button_alt = Button(
        [2 * size[0] / 3, 2 * size[1]/3],
        "Quit",
        quit,
        app,
        gameInstance=app,
        glitchInstance=glitch,
        controller=1,
    )



    scroll_bar_volume = ScrollBar("Game volume", [20,335], 200, mixer.set_sound_volume, max_value=100, init_value = app.volume, app = app)
    scroll_bar_music = ScrollBar("Music volume", [20,400], 200, mixer.set_music_volume, max_value=100, init_value = app.music, app = app)




    drying_time = time.time()

    last_tick = time.time() - 1

    start_time = time.time()

    up_next = ""

    fade_tick.value = 15

    beat_red = 0

    wave_text_color = True
    song_start_t = 0

    last_joy_pos = [0,0]

    decorationWaveNum = 1

    app.three_second_tick = 0

    app.camera_pos = camera_pos

    killProtection = True

    powerMult = 1

    app.loading = False

    while 1:
        app.phase = phase
        tick_time = time.time() - last_tick
        last_tick = time.time()

        tick_delta = tick_time / (1 / 60)


        timedelta.timedelta = min([tick_delta, 3])

        if multiplayer:
            if app.server_tick_rate.tick():
                app.collect_data()
                c_weapon.owner = player_actor
                c_weapon.app = app



        if player_actor.hp > 0:

            # hp_time_dilation = 0.1 + (player_actor.hp/100)**0.4 * 0.9

            if player_actor.hp < 30 and not multiplayer:

                timedelta.timedelta *= 0.5

            else:
                killProtection = True


            # pygame.display.set_gamma(1,random.randint(1,3),1.1)

        app.clock.tick(app.clocktick if not pause else 60)

        app.three_second_tick += timedelta.mod(1)
        if app.three_second_tick > 180:
            app.three_second_tick -= 180


        t = time.time()
        time_stamps = {}

        
        
        


        if app.joysticks and app.detectJoysticks:
            j = app.joysticks[0]
            x = j.get_axis(2)
            y = j.get_axis(3)

            current_hypotenuse = math.sqrt(x**2 + y**2)
            if current_hypotenuse > 1:
                x = x / current_hypotenuse
                y = y / current_hypotenuse

            current_hypotenuse = math.sqrt(x**2 + y**2)

            factor = 1 - 0.08 * current_hypotenuse**2

            angle = math.atan2(y, x)

            offx = math.cos(angle) * 200 * (0.5 + current_hypotenuse*0.5)
            offy = math.sin(angle) * 200 * (0.5 + current_hypotenuse*0.5)

            last_joy_pos[0] = last_joy_pos[0] * factor + (1-factor) * offx
            last_joy_pos[1] = last_joy_pos[1] * factor + (1-factor) * offy

            mouse_pos = [size[0]/2 + last_joy_pos[0], size[1]/2 + last_joy_pos[1]]


        else:

            mouse_pos = app.pygame.mouse.get_pos()

            mouse_pos = [mouse_pos[0] / mouse_conversion, mouse_pos[1] / mouse_conversion]




        click_single_tick = False
        if app.joysticks:
            firingButton = app.joysticks[0].get_axis(5) > -0.5 or pygame.mouse.get_pressed()[0]
        else:
            firingButton = pygame.mouse.get_pressed()[0]

        if firingButton and clicked == False:
            clicked = True
            click_single_tick = True
        elif firingButton == False:
            clicked = False

        if pause:

            if not app.joysticks:
                app.pygame.mouse.set_visible(True)

            screen.fill((0, 0, 0))
            screen.blit(background_surf, (0, 0))

            if pause_tick:
                resume_button.red_tick = 10
                quit_button.red_tick = 10

            wave_change_timer  += tick_time
            song_start_t  += tick_time

            s1 = resume_button.tick(screen, mouse_pos, click_single_tick, glitch)
            quit_button.tick(screen, mouse_pos, click_single_tick, glitch, arg=app)

            scroll_bar_volume.tick(screen, mouse_pos, clicked, click_single_tick, arg = globals())
            scroll_bar_music.tick(screen, mouse_pos, clicked, click_single_tick)

            app.volume = round(scroll_bar_volume.value)
            app.music = round(scroll_bar_music.value)

            pressed = app.pygame.key.get_pressed()
            if (pressed[app.pygame.K_ESCAPE] or s1) and not pause_tick:
                menu_click2.play()
                pause = False
                pause_tick = True
                glitch.glitch_tick = 5
                app.pygame.mouse.set_visible(False)
                click_single_tick = False
                app.pygame.mixer.music.unpause()

            elif not pressed[app.pygame.K_ESCAPE]:
                pause_tick = False

            for event in app.pygame.event.get():
                if event.type == app.pygame.QUIT:
                    sys.exit()

            glitch.tick()
            app.pygame.display.update()

            continue

        if c_weapon.jammed and click_single_tick:
            if random.uniform(0, 1) < 0.3:
                c_weapon.jammed = False
                gun_jam_clear.play()
                UnitStatus(screen, player_actor, "CLEARED!", [0,255,0])
            else:
                gun_jam.play()

        if map.name == "Overworld":
            overworld = True

        else:
            overworld = False

        if dialogue != []:
            app.pygame.mouse.set_visible(True)
            block_movement = True

        else:
            # app.pygame.mouse.set_visible(False)
            block_movement = False



        if app.pygame.mixer.music.get_busy() == False:

            if overworld:
                app.pygame.mixer.music.load("sound/songs/overworld_loop.wav")
                app.pygame.mixer.music.play(-1)
            # elif map.name == "Downtown":
            #     app.pygame.mixer.music.load("sound/songs/Palpitations.wav")
            #     app.pygame.mixer.music.play(-1)
            else:
                last_played = up_next
                while up_next == last_played:
                    up_next = func.pick_random_from_list(songs)
                print("Playing:", up_next)
                app.pygame.mixer.music.load(up_next)
                app.pygame.mixer.music.play()


                with open(
                    f"{up_next}_timestamps.txt"
                ) as file:  # Use file to refer to the file object
                    beat_map = ast.literal_eval(file.read())

                song_start_t = time.time()
                beat_index = 0

                dropIndices = []

                song = up_next.split("/")[-1]

                if song in songDrops:
                    drops = songDrops[song]

                    for s, e in drops:
                        dropIndices.append(beat_map.index(func.closest_value(s, beat_map)))

                print(dropIndices)




        beat_red = (beat_red - 1) * timedelta.exp(0.85) + 1
        try:
            if time.time() - song_start_t > beat_map[beat_index] > 0:
                beat_red = 3
                beat_index += 1

                beat_blink.value = 0

                if wave_text_color:
                    wave_text_color = False
                else:
                    wave_text_color = True

        except:
            pass



        if time.time() - drying_time > 0.1:

            s1 = 250/multiplier

            x = random.randint(0, round(map.map_rendered_alpha.get_size()[0]/s1) - 1)
            y = random.randint(0, round(map.map_rendered_alpha.get_size()[1]/s1) - 1)
            map_render.blit(map.__dict__["map_rendered_alpha"], (x*s1, y*s1), area = [x*s1, y*s1, s1, s1])
            drying_time = time.time()

        time_stamps["blood_drying"] = time.time() - t
        t = time.time()

        if phase != 4:
            camera_pan = c_weapon.__dict__["view"]
        else:
            camera_pan = 0.2

        m_click = app.pygame.mouse.get_pressed()[1]

        if m_click == True and m_clicked == False and dev_tools:
            m_clicked = True


            phase += 1

            if phase == 4:
                app.pygame.mouse.set_visible(True)
            else:
                app.pygame.mouse.set_visible(False)
            if phase == 8:
                phase = 0

        elif m_click == False:
            m_clicked = False

        r_click = app.pygame.mouse.get_pressed()[2]

        r_click_tick = False

        if r_click == True and r_clicked == False:
            r_clicked = True
            r_click_tick = True

        elif r_click == False:
            r_clicked = False



        scroll = [False, False]

        last_gun = c_weapon.name

        app.joystickEvents = []

        for event in app.pygame.event.get():
            if event.type == app.pygame.QUIT:
                sys.exit()

            # Handle hotplugging
            if event.type == pygame.JOYDEVICEADDED and app.detectJoysticks:
                # This event will be generated when the program starts for every
                # joystick, filling up the list without needing to create them manually.
                joy = pygame.joystick.Joystick(event.device_index)
                app.joysticks[joy.get_instance_id()] = joy
                print(f"Joystick {joy.get_instance_id()} connencted")

            if event.type == pygame.JOYDEVICEREMOVED and app.detectJoysticks:
                del app.joysticks[event.instance_id]
                print(f"Joystick {event.instance_id} disconnected")

            if event.type == pygame.JOYBUTTONDOWN:
                app.joystickEvents.append(event.button)


            if event.type == app.pygame.MOUSEBUTTONDOWN or event.type == pygame.JOYBUTTONDOWN:
                if event.button == 4:
                    if block_movement:
                        scroll[0] = True
                        continue
                    searching = True
                    while searching:
                        weapon_scroll -= 1
                        if weapon_scroll == -1:
                            weapon_scroll = len(player_weapons) - 1

                        c_weapon = player_weapons[weapon_scroll]

                        if (
                            c_weapon.get_Ammo() != 0
                            or player_inventory.get_amount_of_type(
                                c_weapon.__dict__["ammo"]
                            )
                            != 0
                            or c_weapon.__dict__["ammo"] == "INF"
                        ):
                            searching = False

                elif event.button == 5:
                    if block_movement:
                        scroll[1] = True
                        continue
                    searching = True
                    while searching:
                        weapon_scroll += 1
                        if weapon_scroll == len(player_weapons):
                            weapon_scroll = 0

                        c_weapon = player_weapons[weapon_scroll]

                        if (
                            c_weapon.get_Ammo() != 0
                            or player_inventory.get_amount_of_type(
                                c_weapon.__dict__["ammo"]
                            )
                            != 0
                            or c_weapon.__dict__["ammo"] == "INF"
                        ):
                            searching = False

        if last_gun != c_weapon.name:
            app.send_data(f"self.game_ref.multiplayer_actors['{self_name}'].set_gun({time.perf_counter()}, '{c_weapon.name}')")



        pressed = app.pygame.key.get_pressed()
        if pressed[app.pygame.K_ESCAPE] and not pause_tick:

            if endless and dialogue:
                dialogue.clear()
                pause_tick = True
            else:
                glitch.glitch_tick = 5
                pause = True
                pause_tick = True
                menu_click2.play()
                app.pygame.mixer.music.pause()

        elif not pressed[app.pygame.K_ESCAPE]:
            pause_tick = False

        rPressed = pressed[app.pygame.K_r] or 1 in app.joystickEvents

        key_r_click = False
        if rPressed and r_1 == False:
            r_1 = True
            key_r_click = True
        elif rPressed == False:
            r_1 = False

        screen.fill([0, 0, 0])
        try:
            fps_counter = time.time() - fps_counter
            fps.insert(0, fps_counter)
            if len(fps) > 60:
                fps.remove(fps[60])

        except Exception as e:
            print("EXCEPTION", e)
        fps_counter = time.time()
        func.keypress_manager(key_r_click, c_weapon, player_inventory, player_actor)

        last_camera_pos = camera_pos.copy()

        camera_pos = func.camera_aling(camera_pos, player_pos)

        app.camera_pos = camera_pos

        if overworld:

            camera_map_edge_tolerance = 0

            if camera_pos[0] < -camera_map_edge_tolerance:
                camera_pos[0] = -camera_map_edge_tolerance
            elif (
                camera_pos[0]
                > map.size_converted[0] - size[0] + camera_map_edge_tolerance
            ):
                camera_pos[0] = (
                    map.size_converted[0] - size[0] + camera_map_edge_tolerance
                )

            if camera_pos[1] < -camera_map_edge_tolerance:
                camera_pos[1] = -camera_map_edge_tolerance
            elif (
                camera_pos[1]
                > map.size_converted[1] - size[1] + camera_map_edge_tolerance
            ):
                camera_pos[1] = (
                    map.size_converted[1] - size[1] + camera_map_edge_tolerance
                )

        cam_delta = func.minus_list(last_camera_pos, camera_pos)

        if (
            (pressed[app.pygame.K_TAB] or 6 in app.joystickEvents)
            and tab_pressed == False
            and player_actor.get_hp() > 0
        ):

            tab_pressed = True

            player_inventory.toggle_inv(app, player_pos=player_pos)

        elif pressed[app.pygame.K_TAB] == False:
            tab_pressed = False

        f_press = False

        if pressed[app.pygame.K_f] and f_pressed == False and player_actor.get_hp() > 0:
            f_pressed = True
            f_press = True
        elif pressed[app.pygame.K_f] == False:
            f_pressed = False

        f11 = False

        if pressed[app.pygame.K_F11] and f11_pressed == False:
            f11_pressed = True
            f11 = True
        elif pressed[app.pygame.K_F11] == False:
            f11_pressed = False

        if f11:
            app.fs = not app.fs
            screen, mouse_conversion = app.update_screen()

        q_press = False
        if pressed[app.pygame.K_q] and q_pressed == False and player_actor.get_hp() > 0:
            q_pressed = True
            q_press = True
        elif pressed[app.pygame.K_q] == False:
            q_pressed = False

        if q_press:
            player_actor.change_nade(player_inventory)



        time_stamps["init"] = time.time() - t
        t = time.time()

        mouse_pos_var = [
            camera_pan * (mouse_pos[0] - size[0] / 2),
            camera_pan * (mouse_pos[1] - size[1] / 2),
        ]

        if not player_inventory.get_inv() and not dialogue:

            camera_pos = [
                camera_pos[0] + mouse_pos_var[0],
                camera_pos[1] + mouse_pos_var[1],
            ]

        for active_map in active_maps:
            # active_map.__dict__["map_rendered"]

            screen.blit(
                map_render,
                [
                    -camera_pos[0] + active_map.__dict__["pos"][0],
                    -camera_pos[1] + active_map.__dict__["pos"][1],
                ],
            )

        #los_walls = los.walls_generate(walls_filtered, camera_pos)

        time_stamps["walls"] = time.time() - t
        t = time.time()

        pvp = overworld
        SyncSongs = True

        if not pvp:

            if wave:
                if ((time.time() - wave_change_timer > wave_length) and not SyncSongs) or not func.songBetweenDrop(up_next, songDrops):

                    if wave_number >= 5:
                        if not endless:
                            for x in interactables:
                                if x.type == "door":
                                    x.active = True

                    wave = False
                    #pygame.display.set_gamma(1, 1.1, 1.1)
                    wave_change_timer = time.time()

                    decorationWaveNum += 1

                    wave_anim_ticks = [120, 0]
                wave_text_tick += timedelta.mod(beat_red*multiplier2)

            else:

                #

                if map.enemy_type == "zombie":  # Kill enemies if no wave.

                    if len(enemy_list) != 0:
                        rand_enemy = func.pick_random_from_list(enemy_list)
                        if not los.check_los(
                            player_actor.pos, rand_enemy.pos, walls_filtered
                        ):
                            rand_enemy.kill_actor(
                                camera_pos,
                                enemy_list,
                                map_render,
                                player_actor,
                                silent=True,
                            )

                if (((time.time() - wave_change_timer > wave_interval) and not SyncSongs) or func.songBetweenDrop(up_next, songDrops)) and map.enemy_type == "zombie":
                    wave_length += 3
                    # wave_interval += 1
                    wave = True
                    #pygame.display.set_gamma(1.2, 0.9, 0.9)
                    wave_number += 1
                    app.storyTeller.gunDropped = False

                    powerMult += 0.01

                    wave_text_tick = -20

                    wave_anim_ticks = [0, 120]

                    if wave_number >= 5:
                        if endless:
                            for x in interactables:
                                if x.type == "door":
                                    x.active = False

            if wave or map.enemy_type == "soldier":

                if map.enemy_type == "soldier":

                    if len(enemy_list) < 20 and not enemy_count == -1:
                        patrol = Patrol(
                            app,
                            map.get_random_point(p_pos=player_pos),
                            interactables,
                            player_actor,
                            NAV_MESH,
                            map.numpy_array_wall_los,
                            map,
                        )

                else:
                    if (
                        len(enemy_list)
                        < (enemy_count / (player_actor.sanity / 100 + 0.25))
                        and wave
                    ):
                        type = weighted_random_choice(enemyDropRate)

                        zombo = Zombie(
                            app,
                            map.get_random_point(p_pos=player_pos),
                            interactables,
                            player_actor,
                            NAV_MESH,
                            [walls_filtered, map.no_los_walls],
                            hp_diff=zombie_hp,
                            dam_diff=zombie_damage,
                            powerMult = powerMult,
                            type=type,
                            wall_points=wall_points,
                            player_ref=player_actor,
                            identificator=random.randint(0, 4096),
                            map=map
                        )
                    # print(f"Zombie spawned with id {zombo.identificator}")
                        enemy_list.append(zombo)


            # func.print_s(screen, str(round(enemy_count/((player_actor.__dict__["sanity"]/100)+0.25),3)),3)

            if time.time() - enemy_up_time > 20 and enemy_count != -1:
                enemy_up_time = time.time()
                enemy_count += 1
        for x in barricade_list:
            if x.tick(screen, camera_pos, map=map) == "KILL":
                barricade_list.remove(x)


        for x in turret_list:
            x.tick(screen, camera_pos, enemy_list, 0, map.numpy_array_wall_los, player_pos)

        for x in npcs:
            x.tick(screen, player_actor, camera_pos, map)

        time_stamps["turrets"] = time.time() - t
        t = time.time()
        delete_list = []
        for x in sorted(interactables, key=lambda x : x.rarity, reverse = True):
            x.__dict__["inv_save"] = player_inventory
            if x.__dict__["alive"] == False:
                delete_list.append(x)
            else:
                x.tick(screen, player_pos, camera_pos)
                if loading_cue != []:
                    door_dest = loading_cue[0]
                    loading_cue.clear()
                    for x in app.maps:
                        if x.name == door_dest:
                            try:
                                (
                                    map,
                                    map_render,
                                    los_bg,
                                    map_boundaries,
                                    NAV_MESH,
                                    player_pos,
                                    camera_pos,
                                    wall_points,
                                    walls_filtered,
                                ) = load_level(x, mouse_conversion, player_inventory, app, screen)
                            except:
                                RUN.main(ms = "beta")


                            wave = False
                            wave_number = 0
                            wave_anim_ticks = [0, 0]

                            if not skip_intervals:
                                wave_interval = 17
                                wave_change_timer = time.time()
                            else:
                                wave_interval = 2
                                wave_change_timer = time.time() - 15

                            #wave_length = 30

        time_stamps["interactables"] = time.time() - t
        t = time.time()

        for x in delete_list:
            interactables.remove(x)

        for x in turret_bro:
            x.tick(screen, camera_pos, enemy_list, 0, [walls_filtered, map.no_los_walls], player_pos)




        time_stamps["particles"] = time.time() - t
        t = time.time()

        bullet_list_copy = bullet_list.copy()
        grenade_list_copy = grenade_list.copy()

        grenade_throw_string = ""
        grenadeJoy = False
        if app.joysticks:
            if app.joysticks[0].get_axis(4) > 0.1 and grenadeJoyThrow == False and player_actor.get_hp() > 0:
                grenadeJoyThrow = True
                grenadeJoy = True
            elif not app.joysticks[0].get_axis(4) > -0.5:
                grenadeJoyThrow = False
        if (
            (pressed[app.pygame.K_g] or grenadeJoy)
            and grenade_throw == False
            and player_actor.get_hp() > 0
        ):

            grenade_throw = True



            if player_inventory.get_amount_of_type("HE Grenade") > 0 and player_actor.preferred_nade == "HE Grenade":
                grenade_list.append(
                    armory.Grenade(
                        player_pos, func.minus(mouse_pos, camera_pos), "HE"
                    )
                )
                player_inventory.remove_amount("HE Grenade", 1)
                print("throwing nade")

                app.send_data(f"grenade_list.append(Grenade({player_pos}, {func.minus(mouse_pos, camera_pos)}, 'HE'))")

            elif player_inventory.get_amount_of_type("Molotov") > 0 and player_actor.preferred_nade == "Molotov":
                grenade_list.append(
                    armory.Grenade(
                        player_pos, func.minus(mouse_pos, camera_pos), "Molotov"
                    )
                )
                player_inventory.remove_amount("Molotov", 1)
                print("throwing nade")

                app.send_data(f"grenade_list.append(Grenade({player_pos}, {func.minus(mouse_pos, camera_pos)}, 'Molotov'))")

            player_actor.update_nade(player_inventory)

        elif pressed[app.pygame.K_g] == False:
            grenade_throw = False

        last_bullet_list = tuple(bullet_list)

        if player_actor.get_hp() > 0:

            x_diff = (mouse_pos[0] + camera_pos[0]) - player_pos[0]
            y_diff = (mouse_pos[1] + camera_pos[1]) - player_pos[1]

            if not block_movement:

                try:
                    angle = math.atan(x_diff / y_diff) * 180 / math.pi + 90
                    if (x_diff < 0 and y_diff > 0) or (x_diff > 0 and y_diff > 0):
                        angle += 180
                except:
                    angle = 0

            else:
                angle = player_actor.angle

            player_actor.set_aim_at(angle)

            weapon_pan_rate = c_weapon.__dict__["handling"]

            player_angle = player_actor.get_angle()

            if abs(angle - player_angle) > 1:
                player_angle = player_angle + timedelta.mod(
                    los.get_angle_diff(angle, player_angle) * (weapon_pan_rate)
                )
            else:
                player_angle = angle

            player_actor.set_angle(player_angle)

            if c_weapon.__dict__["name"] in ["GLOCK", "M1911", "FN57-S", "DESERTEAGLE"]:
                pl = player_pistol
            else:
                pl = player

            func.render_player(
                screen, mouse_pos, pl, player_pos, camera_pos, player_actor
            )

            last_pos = player_pos.copy()

            if not block_movement:

                player_pos2 = player_pos.copy()
                player_pos, x_vel, y_vel = func.player_movement2(
                    pressed, player_pos, x_vel, y_vel, app
                )


            if collision_check_player:
                # angle_coll = map.check_collision(player_pos, map_boundaries, collision_box = 10, screen = screen, x_vel = x_vel, y_vel = y_vel, phase = phase)
                collision_types, angle_coll = map.checkcollision(
                    player_pos,
                    [x_vel, y_vel],
                    10*multiplier2,
                    map_boundaries,
                    ignore_barricades=True,
                )
                if angle_coll:
                    player_pos = angle_coll

            for x in (getcollisionspoint(map.rectangles, player_pos)):
                break_loop = False
                for y in map.barricade_rects:
                    if y[0] == x:
                        break_loop = True
                        break
                if break_loop:
                    continue
                player_pos = last_pos.copy()



            player_actor.set_pos(player_pos)

            if multiplayer and not app.pos_sent:
                app.send_data(f"self.game_ref.multiplayer_actors['{self_name}'].set_values({time.perf_counter()},{[player_pos[0]/multiplier2, player_pos[1]/multiplier2]}, {player_angle})")
                app.pos_sent = True


            if player_actor.knockback_tick != 0:

                player_actor.pos = [
                    player_actor.pos[0]
                    + math.cos(player_actor.knockback_angle)
                    * player_actor.knockback_tick**0.5,
                    player_actor.pos[1]
                    - math.sin(player_actor.knockback_angle)
                    * player_actor.knockback_tick**0.5,
                ]
                player_actor.knockback_tick -= 1

            player_pos = player_actor.pos

            for x in burn_list:
                if los.get_dist_points(x.pos, player_pos) < 40*multiplier2:
                    player_actor.set_hp(timedelta.mod(1), reduce=True)

            if player_actor.__dict__["barricade_in_hand"] != None:
                result = player_actor.__dict__["barricade_in_hand"].tick(
                    screen, camera_pos, mouse_pos, click_single_tick, map
                )
                if result == True:
                    barricade_list.append(player_actor.__dict__["barricade_in_hand"])
                    player_actor.__dict__["barricade_in_hand"] = None
                elif result == "revert":
                    player_inventory.append_to_inv(items["Barricade"], 1)
                    player_actor.__dict__["barricade_in_hand"] = None
            else:

                if player_inventory.get_inv() == False and not overworld and not dialogue:

                    firing_tick = func.weapon_fire(
                        app,
                        c_weapon,
                        player_inventory,
                        player_actor.get_angle(),
                        player_pos,
                        player_actor,
                        screen,
                    )
                    player_melee.tick(screen, r_click_tick)


                    if c_weapon._bullets_in_clip == 0 and click_single_tick:
                        gun_jam.play()
                        UnitStatus(screen, player_actor, "NO AMMO!", [255,0,0])

                else:
                    c_weapon.spread_recoverial()
                    c_weapon.weapon_tick()

            player_alive = True

        elif killProtection:
            killProtection = False
            player_actor.hp = 1
            print("Kill protection used")


        else:



            if player_alive:
                func.list_play(death_sounds)

                if multiplayer:
                    app.send_data("")

                dialogue.clear()

                player_alive = False
                respawn_ticks = 300 if not endless else 120
                death_wave = wave_number
                deathMoney = player_actor.money

                if endless and not multiplayer:
                    app.pygame.mouse.set_visible(True)
                    if map.name != "Downtown":
                        if app.highscore[map.name][difficulty][0] < death_wave:
                            app.highscore[map.name][difficulty][0] = death_wave
                            highscores.saveHighscore(app)
                            newHigh[0] = True

                        if app.highscore[map.name][difficulty][1] < deathMoney:
                            app.highscore[map.name][difficulty][1] = deathMoney
                            highscores.saveHighscore(app)
                            newHigh[1] = True

                for i in range(5):
                    particle_list.append(
                        classes.Particle(
                            func.minus(player_pos, camera_pos),
                            type="blood_particle",
                            magnitude=1.2,
                            screen=map_render,
                        )
                    )
            if not (endless and not multiplayer):
                if respawn_ticks > 0:
                    respawn_ticks -= timedelta.mod(1)
                else:
                    player_actor.set_hp(100)
                    if endless:
                        player_pos = map.get_random_point(enemies=enemy_list)
                    else:
                        player_actor.money = round(player_actor.money/2)
                        money_tick.value = 0
                        player_actor.sanity = 100
                        enemy_count = round(enemy_count*0.75)

                        for x in app.maps:
                            if x.name == "Overworld":
                                (
                                    map,
                                    map_render,
                                    los_bg,
                                    map_boundaries,
                                    NAV_MESH,
                                    player_pos,
                                    camera_pos,
                                    wall_points,
                                    walls_filtered,
                                ) = load_level(x, mouse_conversion, player_inventory, app, screen, death = True)

                                wave = False
                                wave_number = 0
                                wave_anim_ticks = [0, 0]

                                if not skip_intervals:
                                    wave_interval = 17
                                    wave_change_timer = time.time()
                                else:
                                    wave_interval = 2
                                    wave_change_timer = time.time() - 15

                                wave_length = 30


                    # c_weapon = give_weapon(player_we[weapon_scroll])

        c_weapon.add_to_spread(math.sqrt(x_vel**2 + y_vel**2) / 10)

        if last_hp == player_actor.get_hp() and player_alive == True:
            free_tick += timedelta.mod(1)
            if free_tick > 90 and player_actor.get_hp() < 100:
                player_actor.set_hp(timedelta.mod(-1), reduce=True)
                player_actor.set_sanity(timedelta.mod(0.2 * sanity_drain))
                if player_actor.get_hp() >= 100:
                    player_actor.hp = 100

        else:
            free_tick = 0
            # glitch.glitch_tick = 5

        time_stamps["player"] = time.time() - t
        t = time.time()

        closest = 1000
        closest_prompt = None
        closest_available_prompt = None
        for x in interactables:

            dist = x.prompt_dist(player_pos)
            if dist:
                if dist < closest:
                    closest_prompt = x
                    closest = dist

                    if closest_prompt.type == "item":

                        if (
                            player_inventory.append_to_inv(
                                closest_prompt.item,
                                closest_prompt.amount,
                                scan_only=True,
                            )
                            != closest_prompt.amount
                        ):
                            closest_available_prompt = closest_prompt

        if closest_available_prompt != None:
            closest_available_prompt.tick_prompt(
                screen, player_pos, camera_pos, f_press= f_press or 2 in app.joystickEvents
            )
        else:
            if closest_prompt != None:
                closest_prompt.tick_prompt(
                    screen, player_pos, camera_pos, f_press= f_press or 2 in app.joystickEvents
                )

        # for x in interactables:
        #     x.tick_prompt(
        #         screen, player_pos, camera_pos, f_press=f_press
        #     )

        last_hp = player_actor.get_hp()
        if multi_kill_ticks > 0:
            multi_kill_ticks -= timedelta.mod(1)
        else:
            multi_kill = 0

        time_stamps["prompts"] = time.time() - t
        t = time.time()

        for x in app.multiplayer_actors:
            app.multiplayer_actors[x].tick(
                screen, player_pos, camera_pos, walls_filtered, player_actor, map_render,
            )

        for enemy in enemy_list:
            if enemy.class_type == "SOLDIER":
                enemy.tick(phase)
            else:
                enemy.tick(
                    screen,
                    map_boundaries,
                    player_actor,
                    camera_pos,
                    map,
                    [walls_filtered, map.no_los_walls],
                    NAV_MESH,
                    map_render,
                    phase=phase,
                    wall_points=wall_points,
                )


        time_stamps["enemies"] = time.time() - t
        t = time.time()

        app.zombiegroup.draw(screen)

        for x in particle_list:
            x.tick(screen, camera_pos, map)


        time_stamps["zombie_Draw"] = time.time() - t
        t = time.time()



        i2 = []
        for x in bullet_list:
            if x not in last_bullet_list:
                i2.append(x)
            kills_bullet = x.move_and_draw_Bullet(
                screen,
                camera_pos,
                map_boundaries,
                map,
                enemy_list,
                player_actor,
                draw_blood_parts=map_render,
                dummies=app.multiplayer_actors,
            )
            if kills_bullet != 0 and kills_bullet != None:
                kills += kills_bullet
                multi_kill += kills_bullet

                if multi_kill > 99:
                    multi_kill = 1
                    player_actor.set_sanity(10, add = True)

                multi_kill_ticks = 45
                kill_counter = classes.kill_count_render(multi_kill, kill_rgb)

        for pos, type, blastSize in append_explosions:
            if type == "small":
                explosions.append(Explosion(pos, type, player_nade = True, player_damage_mult = 0.25, range = 100))
            else:
                explosions.append(Explosion(pos, type, player_nade = True, player_damage_mult = 0.25, range = blastSize))
        append_explosions.clear()

        last_bullet_list = tuple(bullet_list)

        bullets_new = tuple(i2)

        time_stamps["bullets"] = time.time() - t
        t = time.time()

        for x in grenade_list:
            x.tick(
                screen,
                map_boundaries,
                player_pos,
                camera_pos,
                grenade_list,
                explosions,
                expl1,
                map,
                walls_filtered,
            )
        mp = multi_kill
        for x in explosions:
            m_k, m_k_t = x.tick(
                screen,
                player_actor,
                enemy_list,
                map_render,
                camera_pos,
                explosions,
                multi_kill,
                multi_kill_ticks,
                walls_filtered,
            )

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

        if map.top_layer != None:
            screen.blit(map.top_layer, [-camera_pos[0], -camera_pos[1]])

        if draw_los:

            #print(camera_pos, player_pos, map.numpy_array_wall_los)

            draw_p_pos = func.minus(player_pos, camera_pos, op = "-")

            los_image, triangles, draw_time = render_los_image_jit.draw(
                los_image,
                phase,
                [round(camera_pos[0]), round(camera_pos[1])],
                [round(draw_p_pos[0]), round(draw_p_pos[1])],
                map,
                map.numpy_array_wall_los,
                np.array(size),
                los_background = los_bg

            )

            ###
            ### OPTIMZE point_inits, finishing
            ###

            time_stamps["los_compute"] = time.time() - t
            t = time.time()

            time_stamps["los_draw"] = draw_time
            t = time.time()

            # draw_time = 0
            start = time.time()

            screen.blit(los_image, (0, 0))

            draw_time2 = time.time() - start

            draw_time += time.time() - start

        # func.print_s(screen, f"TIME TILL WAVE: {round(wave_interval - (time.time() - wave_change_timer))}", 4)

        try:
            if multiplayer:

                ping = 0
                for i in app.ping:
                    ping += i

                ping /= len(app.ping)

                func.print_s(screen, "PING: " + str(round(ping * 1000)) + "ms", 4)


        except Exception as e:
            print(e)



        if map.name in ["Overworld", "Downtown"]:
            RainDrop(map, player_pos)

        for x in raindrops:
            x.tick(screen, camera_pos, map_render)

        if draw_los:

            if 60 * draw_time < 55:
                color = [255, 255, 255]
            else:
                color = [255, 0, 0]

            los_total_draw_time_frame = round(60 * draw_time, 3)

            if los_total_draw_time_frame < 0.8:
                color = [255, 255, 255]
            else:
                color = [255, 0, 0]
            try:
                perc1 = round(100 * draw_time / (draw_time + draw_time2))
                perc2 = round(100 * draw_time2 / (draw_time + draw_time2))
            except:
                pass

        if wave_number >= 5 and not endless:
            if not wave:
                text = terminal.render("EXIT DOOR IS OPEN!", False, [255, 255, 255])
                screen.blit(
                    text,
                    [
                        size[0] / 2 - text.get_rect().center[0],
                        size[1] - 30 - text.get_rect().center[1],
                    ],
                )



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
                i = 0
                for x in app.soldier_cache:
                    text = terminal3.render(x + ":" + str(app.soldier_cache[x]), False, [255, 255, 0])
                    screen.blit(text, [200, 50+i])
                    i += 20

            elif phase == 7:
                t = "ROUTE CACHE"

                text = terminal3.render("Cached routes: " + str(len(app.path_cache)), False, [255, 255, 0])
                screen.blit(text, [200, 50])

                try:
                    # text = terminal3.render("Cache route avrg time: " + str(app.path_times["cache"][1]/app.path_times["cache"][0]), False, [255, 255, 0])
                    # screen.blit(text, [200, 80])
                    text = terminal3.render("Calculated route avrg time: " + str(app.path_times["calc"][1]/app.path_times["calc"][0]), False, [255, 255, 0])
                    screen.blit(text, [200, 80])

                    text = terminal3.render("Calcs per sec: " + str(app.path_times["calc"][0]/round(time.time() - start_time)), False, [255, 255, 0])
                    screen.blit(text, [200, 110])

                    text = terminal3.render("Longest time: " + str(app.path_times["max"]), False, [255, 255, 0])
                    screen.blit(text, [200, 140])


                    time.time() - start_time

                except Exception as e:
                    pass


            text = terminal3.render("DEVSCREEN: " + t, False, [255, 255, 255])
            screen.blit(text, [200, 20])

        if player_actor.get_hp() > 0:

            if not block_movement:
                func.draw_HUD(
                    screen,
                    player_inventory,
                    cam_delta,
                    camera_pos,
                    c_weapon,
                    player_weapons,
                    player_actor,
                    mouse_pos,
                    clicked,
                    r_click_tick,
                    wave,
                    wave_anim_ticks,
                    round(wave_text_tick),
                    wave_number,
                    wave_text_color,
                    beat_red,
                    app,
                )

            if not overworld:
                player_actor.set_sanity(timedelta.mod(0.003 * sanity_drain))

            if phase == 3:
                map_points = map.__dict__["points_inside_polygons"]
                map_polygons = map.__dict__["polygons"]
                for point in map_points:
                    app.pygame.draw.circle(
                        screen,
                        [255, 0, 0],
                        [point[0] - camera_pos[0], point[1] - camera_pos[1]],
                        5,
                    )

                for a, b, c, d in map_polygons:
                    for e, f in [[a, b], [b, c], [c, d], [d, a]]:
                        app.pygame.draw.line(
                            screen,
                            [255, 255, 255],
                            [e[0] - camera_pos[0], e[1] - camera_pos[1]],
                            [f[0] - camera_pos[0], f[1] - camera_pos[1]],
                        )

            if phase == 4:
                mo_pos_real = [
                    mouse_pos[0] + camera_pos[0],
                    mouse_pos[1] + camera_pos[1],
                ]
                min_dist_point = None
                dist = 9999
                for point_dict in NAV_MESH:
                    point = point_dict["point"]
                    if func.get_dist_points(mo_pos_real, point) < dist:
                        dist = func.get_dist_points(mo_pos_real, point)
                        min_dist_point = point_dict


                if r_click_tick :
                    ref_point = {
                        "point": [int(mo_pos_real[0]), int(mo_pos_real[1])],
                        "connected": [],
                    }

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

                text = terminal3.render(
                    "APPARENT POS: "
                    + str(round(mo_pos_real[0]))
                    + " "
                    + str(round(mo_pos_real[1])),
                    False,
                    [255, 255, 255],
                )
                screen.blit(text, [mouse_pos[0] + 20, mouse_pos[1] + 20])
                app.pygame.draw.line(
                    screen,
                    [255, 255, 255],
                    mouse_pos,
                    [mouse_pos[0] + 20, mouse_pos[1] + 20],
                )
                pos = [
                    (mouse_pos[0] + camera_pos[0]) * multiplier,
                    (mouse_pos[1] + camera_pos[1]) * multiplier,
                ]
                text = terminal3.render(
                    "REAL POS: " + str(round(pos[0])) + " " + str(round(pos[1])),
                    False,
                    [255, 255, 255],
                )
                screen.blit(text, [mouse_pos[0] + 20, mouse_pos[1] + 40])

                if f_pressed:
                    text = terminal3.render(
                        "POINT POS: " + str(min_dist_point["point"]),
                        False,
                        [255, 255, 255],
                    )
                    screen.blit(text, [mouse_pos[0] + 20, mouse_pos[1] + 80])



                for point_dict in NAV_MESH:



                    point = point_dict["point"]
                    app.pygame.draw.circle(
                        screen,
                        [255, 0, 0],
                        [point[0] - camera_pos[0], point[1] - camera_pos[1]],
                        5,
                    )

                    if point_dict != min_dist_point and f_pressed:
                        continue

                    for point_2 in point_dict["connected"]:
                        app.pygame.draw.line(
                            screen,
                            [255, 255, 255],
                            [point[0] - camera_pos[0], point[1] - camera_pos[1]],
                            [point_2[0] - camera_pos[0], point_2[1] - camera_pos[1]],
                            1,
                        )



                if click_single_tick:
                    calc_time_1 = time.time()
                    route, c = func.calc_route(player_pos, mo_pos_real, NAV_MESH, [map.numpy_array_wall_los, map.numpy_array_wall_no_los], False, app)
                    calc_time_2 = time.time() - calc_time_1

                if route:

                    point_2 = player_pos
                    for point in route:
                        app.pygame.draw.line(
                            screen,
                            [255, 0, 0],
                            [point[0] - camera_pos[0], point[1] - camera_pos[1]],
                            [point_2[0] - camera_pos[0], point_2[1] - camera_pos[1]],
                            3,
                        )
                        point_2 = point
                    app.pygame.draw.line(
                        screen,
                        [255, 0, 0],
                        [mo_pos_real[0] - camera_pos[0], mo_pos_real[1] - camera_pos[1]],
                        [point_2[0] - camera_pos[0], point_2[1] - camera_pos[1]],
                        4,
                    )

                    text = terminal3.render(
                        "CALC TIME: " + str(round(calc_time_2 * 1000, 2)) + "ms",
                        False,
                        [255, 255, 255],
                    )
                    screen.blit(text, [mouse_pos[0] + 20, mouse_pos[1] + 60])



                else:
                    text = terminal3.render(
                        "COULD'T FIND ROUTE!",
                        False,
                        [255, 0, 0],
                    )
                    screen.blit(text, [mouse_pos[0] + 20, mouse_pos[1] + 60])


            elif phase == 7:
                try:
                    for x in app.path_cache:
                        route = app.path_cache[x]
                        if len(route) == 0:
                            continue
                        last_pos = route[0]
                        for tar in route:
                            pygame.draw.line(
                                screen,
                                [255,255,255],
                                func.minus(last_pos, camera_pos, op="-"),
                                func.minus(tar, camera_pos, op="-"),
                            )
                            last_pos = tar
                except Exception as e:
                    print(e)

            if dialogue != []:
                text_str = dialogue[0].main(
                    screen,
                    mouse_pos,
                    click_single_tick,
                    scroll,
                    glitch,
                    app,
                    player_inventory,
                    items,
                    player_actor,
                    map,
                )

                if text_str != "":

                    pygame.draw.rect(
                        screen,
                        [255, 255, 255],
                        [size[0] / 4, 3 * size[1] / 4 - 20, size[0] / 2, size[1] / 4],
                        4,
                    )

                    pygame.draw.line(
                        screen,
                        [255, 255, 255],
                        [size[0] / 4, 3 * size[1] / 4 + 10],
                        [3 * size[0] / 4 - 5, 3 * size[1] / 4 + 10],
                        4,
                    )

                    y_pos = -10 * len(text_str[1].split("\n"))

                    color = [255,255,255] if text_str[0] != "" else [144,144,144]

                    for text_line in text_str[1].split("\n"):

                        glitchy = text_str[0] == "Mysterious voice"

                        text = terminal.render(text_line, False, color if not glitchy else [255,100,100])
                        pos = [size[0] / 2, 7 * size[1] / 8]
                        screen.blit(
                            text,
                            [
                                pos[0] - text.get_rect().center[0],
                                pos[1] - text.get_rect().center[1] + 5 + y_pos,
                            ],
                        ) if not glitchy else func.blit_glitch(
                            screen, text, [pos[0] - text.get_rect().center[0], pos[1] - text.get_rect().center[1] + 5 + y_pos], 2, black_bar_chance = 3
                        )


                        y_pos += 20



                    if text_str[0] == "You":
                        text = terminal.render(text_str[0], False, color)
                        pos = [
                            3 * size[0] / 4 - 8 - text.get_rect().size[0],
                            3 * size[1] / 4 - 15,
                        ]
                    else:
                        text = terminal.render(text_str[0], False, color)
                        pos = [size[0] / 4 + 5, 3 * size[1] / 4 - 15]

                    screen.blit(text, [pos[0], pos[1]])

        elif not killProtection:
            if not endless:
                text = terminal.render(f"{round(player_actor.money/2)}$ lost. Going back to Overworld...", False, [255, 255, 255])
                pos = [size[0] / 2, size[1] / 2 - 40]
                screen.blit(
                    text,
                    [
                        pos[0] - text.get_rect().center[0],
                        pos[1] - text.get_rect().center[1],
                    ],
                )

                text = terminal_map_desc.render("YOU DIED!", False, [255, 255, 255])
                pos = [size[0] / 2, size[1] / 4 - 40]
                screen.blit(
                    text,
                    [
                        pos[0] - text.get_rect().center[0],
                        pos[1] - text.get_rect().center[1],
                    ],
                )


                if 40 <= respawn_ticks <= 50 and fade_tick.value >= fade_tick.max_value:
                    fade_tick.value = 0

            elif not multiplayer:
                if map.name == "Downtown":
                    text = terminal_map_desc.render(f"YOU DIED!", False, [255, 255, 255])
                else:
                    text = terminal_map_desc.render(f"YOU DIED ON WAVE {death_wave if death_wave != -1 else wave_number}!", False, [255, 255, 255])
                pos = [size[0] / 2, size[1] / 2 - 40]
                screen.blit(
                    text,
                    [
                        pos[0] - text.get_rect().center[0],
                        pos[1] - text.get_rect().center[1],
                    ],
                )

                if newHigh[0]:
                    text = terminal3.render(f"NEW RECORD!", False, [255, 255, 255])
                    pos = [size[0] / 2, size[1] / 2 - 10]
                    screen.blit(
                        text,
                        [
                            pos[0] - text.get_rect().center[0],
                            pos[1] - text.get_rect().center[1],
                        ],
                    )


                text = terminal.render(f"Money gathered: {deathMoney}$", False, [255, 255, 255])
                pos = [size[0] / 2, size[1] / 2 + 20]
                screen.blit(
                    text,
                    [
                        pos[0] - text.get_rect().center[0],
                        pos[1] - text.get_rect().center[1],
                    ],
                )

                if newHigh[1]:
                    text = terminal3.render(f"NEW RECORD!", False, [255, 255, 255])
                    pos = [size[0] / 2, size[1] / 2 + 40]
                    screen.blit(
                        text,
                        [
                            pos[0] - text.get_rect().center[0],
                            pos[1] - text.get_rect().center[1],
                        ],
                    )

                retry_button.tick(screen, mouse_pos, click_single_tick, glitch)
                quit_button_alt.tick(screen, mouse_pos, click_single_tick, glitch)

            else:
                text = terminal.render(f"Respawning", False, [255, 255, 255])
                pos = [size[0] / 2, size[1] / 2 - 40]
                screen.blit(
                    text,
                    [
                        pos[0] - text.get_rect().center[0],
                        pos[1] - text.get_rect().center[1],
                    ],
                )



        beat_blink.tick()

        try:
            kill_counter.tick(screen, cam_delta, kill_counter)
        except:
            pass

        if endless:
            text = terminal3.render("ENDLESS MODE", False, [255, 255, 255])
            x,y = text.get_rect().center
            screen.blit(text, [size[0]/2-x, 20/2-y])

        if multiplayer:
            text = terminal3.render("MULTIPLAYER", False, [255, 255, 255])
            screen.blit(text, [400, 20])
            text = terminal3.render(self_name, False, [255, 255, 255])
            screen.blit(text, [400, 40])
        else:
            zombie_events.clear()

        if phase != 5:
            try:
                func.print_s(screen, "FPS: " + str(round(1 / (sum(fps) / 60))), 1)
                pass
            except:
                pass

            func.print_s(screen, "KILLS: " + str(kills), 2)

            func.print_s(screen, f"PERF: {round(app.storyTeller.playerPerformace,4)}", 3)

            time_elapsed = round(time.time() - start_time)

            minutes = round((time_elapsed - 29.9) / 60)

            seconds = time_elapsed - minutes * 60

            if len(str(seconds)) == 1:
                seconds = "0" + str(seconds)

            #func.print_s(screen, f"{minutes}:{seconds}", 3)

        else:
            obje = enumerate(time_stamps, 1)
            total = 0
            try:
                for i, k in obje:
                    time_stamps[k] = (
                        time_stamps[k] * 1 / 20 + last_time_stamp[k] * 19 / 20
                    )

                    color = [
                        255,
                        round(255 / (1 + time_stamps[k] * 1000)),
                        round(255 / (1 + time_stamps[k] * 1000)),
                    ]

                    func.print_s(
                        screen,
                        k + ":" + str(round(time_stamps[k] * 1000, 1)) + "ms",
                        i,
                        color=color,
                    )

                    total += time_stamps[k]
                if total > 1 / 60:
                    color = [255, 0, 0]
                else:
                    color = [255, 255, 255]
                func.print_s(
                    screen,
                    "TOTAL"
                    + ":"
                    + str(round(total * 1000, 1))
                    + "ms ("
                    + str(round(1 / total))
                    + "FPS)",
                    i + 1,
                    color=color,
                )
            except Exception as e:
                print(e)

        last_time_stamp = time_stamps.copy()

        if wave_anim_ticks[0] > 0:
            wave_anim_ticks[0] -= timedelta.mod(1)
        if wave_anim_ticks[1] > 0:
            wave_anim_ticks[1] -= timedelta.mod(1)


        if not fade_tick.tick():
            tick = fade_tick.rounded()
            if 0 <= tick <= 9:
                screen.blit(fade_to_black_screen[tick], [0, 0])

            elif 51 <= tick <= 60:
                screen.blit(fade_to_black_screen[60 - tick], [0, 0])

            else:
                screen.fill([0, 0, 0])

        if not map_desc_tick.tick() and map_desc_tick.value > 20:
            tick = map_desc_tick.value - 20
            alpha = 255
            if tick < 40:
                alpha = 255 * tick / 40

            elif 160 > tick > 100:
                alpha = 255 * (160 - tick) / 60

            text = terminal_map_desc.render(map.name, False, [255, 255, 255])
            text.set_alpha(alpha)
            screen.blit(
                text,
                [
                    size[0] / 2 - text.get_rect().center[0],
                    size[1] / 3 - text.get_rect().center[1],
                ],
            )

        for x in unitstatuses:
            x.tick(camera_pos)

        if wave:
            if app.storyTeller.playerPerformanceTick.tick():
                if player_actor.hp < 80:
                    app.storyTeller.playerPerformanceLowHealth += 1
                else:
                    app.storyTeller.playerPerformanceHighHealth += 1
                
                app.storyTeller.playerPerformanceLowHealth *= 0.99
                app.storyTeller.playerPerformanceHighHealth *= 0.99
                app.storyTeller.playerPerformace = app.storyTeller.playerPerformanceHighHealth / (app.storyTeller.playerPerformanceHighHealth + app.storyTeller.playerPerformanceLowHealth)


        for dropBeat in dropIndices:
            if dropBeat - 4 <= beat_index-1 <= dropBeat:

                i = 5 - (dropBeat - beat_index+1)

                color = [
                            round(min([255, (beat_red-1)*255])), 
                            round((beat_red-1)*127.5), 
                            round((beat_red-1)*127.5)
                        ]
                
                #print(color)

                if dropBeat == beat_index-1:

                    text = terminal_waveSecs[-1].render(f"WAVE {decorationWaveNum}", False, color)
                else:

                    text = terminal_waveSecs[4 - (dropBeat - beat_index+1)].render(str(dropBeat - beat_index+1), False, color)
                                                                                      
                text.set_alpha(round((beat_red-1)*127.5))

                pos = [
                        size[0] / 2 - text.get_rect().center[0],
                        size[1] / 3 - text.get_rect().center[1],
                    ]

                func.blit_glitch(screen, text, pos, round((beat_red - 1) * (5 - (dropBeat - beat_index+1))))





        if pause:
            background_surf.blit(screen, (0, 0))
        glitch.tick()
        melee_list.clear()

        playerhealth.health = player_actor.hp

        if app.screen_glitch > 0:
            image_copy = screen.copy()
            screen.fill((0,0,0))
            func.blit_glitch(screen, image_copy, [0,0], round(2*app.screen_glitch), black_bar_chance = 15)
            app.screen_glitch -= timedelta.mod(1)

        app.pygame.display.update()


if __name__ == "__main__":
    main()
