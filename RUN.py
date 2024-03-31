import os, sys

if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)
    FROZEN = True
else:
    FROZEN = False

import pygame
import math
import random
import time
from values import *
from _thread import *
from network import Network
import socket
import classes
import time
import game
import hud_elements
import get_preferences
import func
from glitch import Glitch
from button import Button
import mixer
from scroll_bar import ScrollBar
# import path_finding
from app import App
import map_creator
from menu import Menu
import map_creator
import scipy
import highscores
import traceback

from utilities.version import frozenVersion

VERSION = "0.9"
if FROZEN:
    subversion = str(frozenVersion)
else:
    with open("commit_message.txt", "r") as f:
        subversion = f.readline().strip("\n")
VERSION = VERSION + "." + subversion

terminal = pygame.font.Font("texture/terminal.ttf", 20)
terminal2 = pygame.font.Font("texture/terminal.ttf", 30)
prompt = pygame.font.Font("texture/terminal.ttf", 14)


dirty = False


def render_selected_map(screen, maps_dict, app, mouse_pos, mouse_single_tick, difficulty, mp = False, host = False):
    rect_map = maps_dict[app.selected_map]["image"].get_rect()

    map_pos = [size[0]/2 - rect_map.center[0], 80 * (size[0]/854)]

    text = terminal.render("MAP", False, [255, 255, 255])
    screen.blit(text, [size[0]/2 - text.get_rect().size[0] / 2, map_pos[1]-80])

    if rect_map.collidepoint(func.minus(mouse_pos, map_pos, "-")) and host:

        if mouse_single_tick:
            app.selected_map += 1
            menu_click2.play()
            app.map_tick = 5

            if app.selected_map == len(maps_dict):
                app.selected_map = 0
            if mp:
                app.send_data(f"self.game_ref.set_map({app.selected_map})")

        rect_map = maps_dict[app.selected_map]["image"].get_rect()

        rect_map.inflate_ip(4, 4)

        app.pygame.draw.rect(screen, [255, 255, 255], rect_map.move(map_pos), 5)

    if app.map_tick > 0:
        app.map_tick -= 1
        func.blit_glitch(screen, maps_dict[app.selected_map]["image"], map_pos, glitch = app.map_tick*4, black_bar_chance = 15-app.map_tick*2)

        func.render_text_glitch(screen,  maps_dict[app.selected_map]["map"].name, [size[0]/2, map_pos[1]-40], glitch = 5, centerx = True, font = terminal)

    else:
        screen.blit(maps_dict[app.selected_map]["image"], map_pos)

        text = terminal.render(
            maps_dict[app.selected_map]["map"].__dict__["name"], False, [255, 255, 255]
        )
        screen.blit(text, [size[0]/2 - text.get_rect().size[0] / 2, map_pos[1]-40])



    rect_map2 = maps_dict[app.selected_map]["image"].get_rect()
    y_1 = 0
    pos = [size[0]*3/4, map_pos[1] - 40]
    text = terminal.render(
        "ALL LOADED MAPS:", False, [255, 255, 255]
    )
    screen.blit(text, pos)

    for x in maps_dict:

        pos = [size[0]*3/4, map_pos[1] + y_1]
        text = terminal.render(maps_dict[x]["map"].name, False, [255,255,255])
        rect = text.get_rect()
        rect.x = pos[0]
        rect.y = pos[1]

        if rect.collidepoint(mouse_pos) and host:
            color = [255,0,0]
            if mouse_single_tick:
                app.selected_map = x
                menu_click2.play()
                app.map_tick = 5

                if mp:
                    app.send_data(f"self.game_ref.set_map({app.selected_map})")

                break

        elif  maps_dict[x]["map"].name == maps_dict[app.selected_map]["map"].name:
            color = [255,255,255]
        else:
            color = [100,100,100]

        text = terminal.render(maps_dict[x]["map"].name, False, color)
        screen.blit(text, pos)
        y_1 += 25






    app.pygame.draw.line(
        screen, [255, 255, 255], [map_pos[0] + rect_map2.w + 10, map_pos[1]], [map_pos[0] + rect_map2.w + 10, map_pos[1] + rect_map2.h]
    )
    app.pygame.draw.line(screen, [255, 255, 255], [map_pos[0] + rect_map2.w + 10, map_pos[1]], [map_pos[0] + rect_map2.w + 5, map_pos[1]])
    app.pygame.draw.line(
        screen,
        [255, 255, 255],
        [map_pos[0] + rect_map2.w + 10, map_pos[1] + rect_map2.h],
        [map_pos[0] + rect_map2.w + 5, map_pos[1] + rect_map2.h],
    )

    text = terminal.render(
        str(round(maps_dict[app.selected_map]["map"].size[1] /  (100*multiplier2)))
        + "m",
        False,
        [255, 255, 255],
    )
    screen.blit(text, [map_pos[0] + rect_map2.w + 12, map_pos[1] + rect_map2.h / 2 - text.get_rect().size[1] / 2])

    app.pygame.draw.line(
        screen,
        [255, 255, 255],
        [map_pos[0], map_pos[1] + 10 + rect_map2.h],
        [map_pos[0] + rect_map2.w, map_pos[1] + 10 + rect_map2.h],
    )
    app.pygame.draw.line(
        screen,
        [255, 255, 255],
        [map_pos[0], map_pos[1] + 10 + rect_map2.h],
        [map_pos[0], map_pos[1] + 5 + rect_map2.h],
    )

    # AIDS AIDS
    app.pygame.draw.line(
        screen,
        [255, 255, 255],
        [map_pos[0] + rect_map2.w, map_pos[1] + 10 + rect_map2.h],
        [map_pos[0] + rect_map2.w, map_pos[1] + 5 + rect_map2.h],
    )

    text = terminal.render(
        str(round(maps_dict[app.selected_map]["map"].__dict__["size"][0] / (100*multiplier2)))
        + "m",
        False,
        [255, 255, 255],

    )
    screen.blit(text, [map_pos[0] + rect_map2.w / 2  - text.get_rect().size[0] / 2, map_pos[1]+ 12 + rect_map2.h])
    if difficulty == 0 or difficulty == "NO ENEMIES":
        return

    if maps_dict[app.selected_map]["map"].name not in app.highscore:
        return

    wave = app.highscore[maps_dict[app.selected_map]["map"].name][difficulty][0]
    text = terminal.render(f"Highest wave: {wave}", False, [255, 255, 255])

    screen.blit(text, [map_pos[0], map_pos[1]+rect_map.height + 30])

    money = app.highscore[maps_dict[app.selected_map]["map"].name][difficulty][1]
    text = terminal.render(f"Most money earned: {money}$", False, [255, 255, 255])

    screen.blit(text, [map_pos[0], map_pos[1]+rect_map.height + 60])



def main(ms = "start", TEST = False):
    quick_load = False

    app = App(pygame)



    maps_dict = app.getMaps()
    app.clock = app.pygame.time.Clock()

    highscores.write_default_highscore()
    highscores.checkHighscores(app)


    screen, mouse_conversion = app.update_screen()
    if not quick_load:
        app.introScreen(screen, app.clock)

    func.load_screen(app, screen, "Loading")





    menu_status = ms

    app.pygame.mouse.set_visible(True)

    terminal = app.pygame.font.Font("texture/terminal.ttf", 20)
    terminal2 = app.pygame.font.Font("texture/terminal.ttf", 10)

    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    ip = ""
    # app.name += str(random.randint(1,109))
    textbox_name = hud_elements.text_box((100, 200), app.name)
    textbox_ip = hud_elements.text_box((640, 415), ip)

    textbox_ip.text = app.last_ip
    players = []
    port = 5555
    menu_alpha = 30

    fade_tick.value = 45



    if not IS.menu_animations:
        print("Loading animations...")
        intro1 = func.load_animation("anim/intro1", 0, 30, alpha=menu_alpha, intro = True, loadCompressed=True, size = [854,480])

        if not quick_load:
            intro2 = func.load_animation("anim/intro2", 0, 30, alpha=menu_alpha, intro = True, loadCompressed=True, size = [854,480])
            intro3 = func.load_animation("anim/intro3", 60, 31, alpha=menu_alpha, intro = True, loadCompressed=True, size = [854,480])
            intro4 = func.load_animation("anim/intro4", 1, 30, alpha=menu_alpha, intro = True, loadCompressed=True, size = [856,480])
            intro5 = func.load_animation("anim/intro5", 1825, 32, alpha=menu_alpha, intro = True, loadCompressed=True, size = [854,480])
            intro6 = func.load_animation("anim/intro6", 1, 30, alpha=menu_alpha, intro = True, loadCompressed=True, size = [856,480])
            intro7 = func.load_animation("anim/intro7", 1, 30, alpha=menu_alpha, intro = True, loadCompressed=True, size = [854,480])
            intro8 = func.load_animation("anim/intro8", 30, 31, alpha=menu_alpha, intro = True, loadCompressed=True, size = [854,480])

            IS.menu_animations = [intro1, intro2, intro3, intro4, intro5, intro6, intro7, intro8] #
        else:
            IS.menu_animations = [intro1]
    menu_i = 0

    def start_map_creator(arg):
        map_creator.main(app)

    def host_game(arg):
        print("HOSTING GAME")
        textbox_ip.__dict__["text"] = ip_address
        ip = ip_address
        try:
            app.players.clear()
            app.players.append(app.name)
            start_new_thread(app.lobby_host, ("1", ip))
            return join_game(ip, True)
        except:
            return "start", None, None

    def upnp_menu(arg):
        if app.dev:
            print("test")
            return "upnp_menu"

    def upnp_test(arg):
        if app.dev:
            print("upnp_test")
            return "upnp_test"



    def join_game(arg, host=False):

        print("JOINING TO:", arg)

        app.players.clear()
        app.players.append(app.name)

        try:
            app.net = Network(arg)

            print("CLIENT: STARTING SEARCH")

            reply = app.net.send(app.name)

            app.send_data(f"self.game_ref.append_player('{app.name}')")

            if reply != [""]:

                print("CLIENT:", reply)
                print("CLIENT: CONNECTED")

                return "lobby", app.net, host
            else:
                print("CLIENT: No connection found")
                return "start", None, None
        except Exception as e:
            print("CLIENT: Connection failed")
            print(e)
            return "start", None, None

    def main_menu(arg):
        app.write_prefs()
        return "start"

    def restart(arg):
        app.write_prefs()
        os.execv(sys.executable, ['python'] + sys.argv)


    def main_menu_save(arg):
        res = app.res
        app.write_prefs()
        for x in check_box_res:
            if x.checked:
                resx, resy= x.caption.split("x")
                app.res = [int(resx), int(resy)]

        app.update_screen()
        if app.res != res:
            return "res_change"

        return "start"

    def launch_map_editor(args):
        pygame.mixer.music.fadeout(1000)
        map_creator.launch()



    def quit(args):

        app.write_prefs()

        sys.exit()

    def start_sp_career(arg):
        print("SPa")

        app.endless = False

        app.write_prefs()
        args = (
            app,
            app.name,
            "NORMAL",
            app.draw_los,
            app.dev,
            check_box_inter.__dict__["checked"],
            app.overworld,
        )

        app.start_sp(args)


    def start_sp(arg):
        print("SPa")

        app.write_prefs()
        args = (
            app,
            app.name,
            arg,
            app.draw_los,
            app.dev,
            check_box_inter.__dict__["checked"],
            maps_dict[app.selected_map]["map"],
        )

        app.start_sp(args)

    def start_mp(arg):
        if not app.MULT_ACKNOWLEDGEMENT:
            return "warningScreen"
        return "mp_start"

    def sp(arg):
        return "sp"

    def settings(arg):
        return "settings"

    def kill_server(arg):
        reply = app.net.send("kill")
        return "start"

    def sp_lob(arg):
        return "single_player_lobby"

    host = False
    background_tick = 1



    glitch = Glitch(screen)

    x_s = size[0] / 2

    difficulty = "NORMAL"

    button_sp= Button(
        [x_s, 200],
        "Singleplayer",
        sp,
        None,
        gameInstance=app,
        glitchInstance=glitch,
        controller = 0,
    )

    button_sp_menu = Button(
        [x_s, 220],
        "Endless Mode",
        sp_lob,
        None,
        gameInstance=app,
        glitchInstance=glitch,
        controller = 0,
    )

    button_sp_new_game = Button(
        [x_s, 100],
        "Start New Game",
        start_sp_career,
        None,
        gameInstance=app,
        glitchInstance=glitch,
    )

    button_sp_continue_game = Button(
        [x_s, 160],
        "Continue",
        sp_lob,
        None,
        gameInstance=app,
        glitchInstance=glitch,
        locked = True
    )

    button_back_sp = Button(
        [x_s, 280],
        "Back",
        main_menu,
        None,
        gameInstance=app,
        glitchInstance=glitch,
    )


    button_mp_menu = Button(
        [x_s, 260],
        "Multiplayer",
        start_mp,
        None,
        gameInstance=app,
        glitchInstance=glitch,
    )

    button_WarnContinue = Button(
        [x_s, 320],
        "Continue",
        start_mp,
        None,
        gameInstance=app,
        glitchInstance=glitch,
    )


    button_settings = Button(
        [x_s, 320],
        "Settings",
        settings,
        None,
        gameInstance=app,
        glitchInstance=glitch,
    )

    button_map_creator = Button(
        [x_s, 380],
        "Map Editor",
        launch_map_editor,
        None,
        gameInstance=app,
        glitchInstance=glitch,
    )

    button_quit_game = Button(
        [x_s, 380], "Exit", quit, None, gameInstance=app, glitchInstance=glitch
    )

    button_back_beta = Button(
        [x_s, 380], "Back", main_menu, None, gameInstance=app, glitchInstance=glitch
    )

    button_restart_game = Button(
        [x_s, 380], "Restart", restart, None, gameInstance=app, glitchInstance=glitch
    )

    button_host_game = Button(
        [x_s, 100],
        "Host",
        host_game,
        "3",
        gameInstance=app,
        glitchInstance=glitch,
    )
    button_join_game = Button(
        [x_s, 160],
        "Join",
        join_game,
        app.ip,
        gameInstance=app,
        glitchInstance=glitch,
    )
    button_back = Button(
        [x_s, 220],
        "Back",
        main_menu,
        None,
        gameInstance=app,
        glitchInstance=glitch,
    )
    button_savesettings = Button(
        [180, 50],
        "Save Settings",
        main_menu_save,
        None,
        gameInstance=app,
        glitchInstance=glitch,
    )
    buttonUpnp = Button(
        [x_s, 280],
        "dev-test-upnp",
        upnp_menu,
        "upnp_menu",
        gameInstance=app,
        glitchInstance=glitch,
    )

    button_start_multi_player_host = Button(
        [140, 70],
        "START GAME",
        app.launch_multiplier_server,
        None,
        gameInstance=app,
        glitchInstance=glitch,
    )
    button_start_single_player = Button(
        [140, 70],
        "START GAME",
        start_sp,
        difficulty,
        gameInstance=app,
        glitchInstance=glitch,
        controller = 0,
    )
    button_host_quit = Button(
        [68, 130],
        "Back",
        kill_server,
        None,
        gameInstance=app,
        glitchInstance=glitch,
    )
    button_client_quit = Button(
        [68, 130],
        "Back",
        main_menu,
        None,
        gameInstance=app,
        glitchInstance=glitch,
    )

    buttonUpnpTest = Button(
        [x_s, 280],
        "dev-test-upnp",
        upnp_test,
        "upnp_test",
        gameInstance=app,
        glitchInstance=glitch,
    )
    buttonUpnpBack = Button(
        [x_s, 220],
        "Back",
        start_mp,
        None,
        gameInstance=app,
        glitchInstance=glitch,
    )

    scroll_bar_volume = ScrollBar("Game volume", [50,130], 200, mixer.set_sound_volume, max_value=100, init_value = app.volume, app = app)
    scroll_bar_music = ScrollBar("Music volume", [300,130], 200, mixer.set_music_volume, max_value=100, init_value = app.music, app = app)

    scroll_bar_volume.on_change_function(globals(), scroll_bar_volume.value/100)
    scroll_bar_music.on_change_function(None, scroll_bar_music.value/100)

    i_song = random.randint(0, 2)
    i_song = 1
    song = ["sound/songs/menu_loop.wav", "sound/songs/menu_loop_new.wav", "sound/songs/menu_loop_new2.wav"][i_song]

    app.pygame.mixer.music.load(song)
    app.pygame.mixer.music.play(-1)

    bpm = [70, 120, 115][i_song]
    beat_time = 1 / (bpm / 60)

    t = time.perf_counter()

    check_box_difficulties = []

    for text, y_pos in [
        ["NO ENEMIES", 200],
        ["NORMAL", 240],
        ["HARD", 280],
        ["ONSLAUGHT", 320],
    ]:
        box = hud_elements.Checkbox(
            screen,
            20,
            y_pos,
            caption=text,
            font_color=[255, 255, 255],
            text_offset=[40, 5],
            cant_uncheck=True,
        )

        if text == "NORMAL":
            box.checked = True
        check_box_difficulties.append(box)

    background = app.pygame.Surface(
        (size[0] + 50, size[1]), app.pygame.SRCALPHA, 32
    ).convert_alpha()
    #
    background.set_alpha(240)

    background2 = app.pygame.Surface(size, app.pygame.SRCALPHA, 32).convert_alpha()
    check_box_dev_commands = hud_elements.Checkbox(
        screen,
        20,
        300,
        caption="Dev tools",
        font_color=[255, 255, 255],
        text_offset=[40, 5],
    )

    check_box_inter = hud_elements.Checkbox(
        screen,
        20,
        400,
        caption="Ceaseless Storm",
        font_color=[255, 0, 0],
        text_offset=[40, 5],
    )

    if app.dev:
        check_box_dev_commands.checked = True

    check_box_fov = hud_elements.Checkbox(
        screen,
        20,
        260,
        caption="Fog of War",
        font_color=[255, 255, 255],
        text_offset=[40, 5],
    )

    if app.draw_los:
        check_box_fov.__dict__["checked"] = True


    check_box_fs = hud_elements.Checkbox(
        screen,
        20,
        340,
        caption="Fullscreen",
        font_color=[255, 255, 255],
        text_offset=[40, 5],
    )

    check_box_fps1 = hud_elements.Checkbox(
        screen,
        400,
        260,
        caption="60",
        font_color=[255, 255, 255],
        text_offset=[40, 5],
        cant_uncheck=True,
    )

    check_box_fps2 = hud_elements.Checkbox(
        screen,
        400,
        300,
        caption="144",
        font_color=[255, 255, 255],
        text_offset=[40, 5],
        cant_uncheck=True,
    )

    check_box_fps3 = hud_elements.Checkbox(
        screen,
        400,
        340,
        caption="Unlimited",
        font_color=[255, 255, 255],
        text_offset=[40, 5],
        cant_uncheck=True,
    )

    check_box_res1 = hud_elements.Checkbox(
        screen,
        600,
        260,
        caption="854x480",
        font_color=[255, 255, 255],
        text_offset=[40, 5],
        cant_uncheck=True,
    )

    check_box_res2 = hud_elements.Checkbox(
        screen,
        600,
        300,
        caption="1366x768",
        font_color=[255, 255, 255],
        text_offset=[40, 5],
        cant_uncheck=True,
    )

    check_box_res3 = hud_elements.Checkbox(
        screen,
        600,
        340,
        caption="1920x1080",
        font_color=[255, 255, 255],
        text_offset=[40, 5],
        cant_uncheck=True,
    )

    check_box_vsync = hud_elements.Checkbox(
        screen,
        400,
        400,
        caption="VSYNC",
        font_color=[255, 255, 255],
        text_offset=[40, 5],
    )

    check_box_fps = [check_box_fps1, check_box_fps2, check_box_fps3]

    check_box_res = [check_box_res1, check_box_res2, check_box_res3]

    for x in check_box_fps:
        if x.caption == app.fps:
            x.checked = True
            break

    for x in check_box_res:
        if x.caption == f"{app.res[0]}x{app.res[1]}":
            x.checked = True
            break


    if app.fs:
        check_box_fs.__dict__["checked"] = True

    if app.vsync:
        check_box_vsync.checked = True

    diff_captions = {
        "NO ENEMIES": "For testing.",
        "NORMAL": "Sanity drain, zombie health and damage are normal.",
        "HARD": "Sanity drains 25% faster, zombies have 25% more health and 10% more damage. Turrets have 15% less bullets.",
        "ONSLAUGHT": "Sanity drains 50% faster, zombies have 35% more health and 20% more damage. Turrets have 30% less bullets.",
    }

    app.net = None
    background_vel = 0
    app.buttons = [
        button_sp_menu,
        button_mp_menu,
        button_settings,
        button_host_game,
        button_join_game,
        button_start_single_player,
        buttonUpnp,
        button_start_multi_player_host,
        button_start_single_player,
        button_host_quit,
        button_client_quit,
        buttonUpnpTest,
        buttonUpnpBack,
        button_back,
        button_quit_game,
        button_savesettings,
        button_sp,
        button_sp_continue_game,
        button_restart_game,
        button_sp_new_game,
        button_back_sp,
        button_map_creator,
        button_WarnContinue,
    ]
    checkboxes = [
        check_box_difficulties,
        check_box_dev_commands,
        check_box_inter,
        check_box_fov,
        check_box_fs,
        check_box_fps1,
        check_box_fps2,
        check_box_fps3
    ]
    game_state = {
        "app.selected_map": app.selected_map,
        "players": players,
        "hostname": hostname,
        "ip": ip_address,
        "port": port,
        "difficulty": difficulty,
        "background_tick": background_tick,
        "background_vel": background_vel,
        "checked_boxes": [],
        "get_mouse_pos": app.pygame.mouse.get_pos,  # ref to func to call from menue
        "mouse_pos": app.pygame.mouse.get_pos(),
    }

    game_menu = Menu(
        buttons=app.buttons,
        checkboxes=checkboxes,
        background=background,
        screen=screen,
        terminal1=terminal,
        terminal2=terminal2,
        particle_list=particle_list,
    )




    #app.pygame.display.set_gamma(1, 1, 1)

    playerhealth.health = 100

    rgb_i = 2
    change_i = 0
    app.map_tick = 0

    last_beat = time.perf_counter()
    app.loading = False
    while 1:



        # game_menu.update(game_state)
        # menu should cover a lot of the while loop -

        app.volume = round(scroll_bar_volume.value)
        app.music = round(scroll_bar_music.value)
        app.joystickEvents = []
        #button_mp_menu.locked = not app.dev

        app.update_fps()

        app.collect_data()


        if app.start_game_with_mp:
            p, m = app.start_game_with_mp
            app.start_multiplayer_client(p, m)

        if background_tick != 0:
            background_tick -= 1
            background_vel += 0.2
        else:
            background_tick = 52

        app.clock.tick(60)

        app.name = textbox_name.text
        app.ip = textbox_ip.text
        events = app.pygame.event.get()

        full_screen_mode = check_box_fs.checked

        app.dev = check_box_dev_commands.checked
        app.draw_los = check_box_fov.checked
        app.fs = check_box_fs.checked
        app.vsync = check_box_vsync.checked

        mouse_pos = app.pygame.mouse.get_pos()

        mouse_pos = [mouse_pos[0] / mouse_conversion, mouse_pos[1] / mouse_conversion]
        game_state["mouse_pos"] = mouse_pos
        for event in events:
            if menu_status == "settings":
                check_box_fov.update_checkbox(event, mouse_pos)
                check_box_dev_commands.update_checkbox(event, mouse_pos)
                check_box_fs.update_checkbox(event, mouse_pos)
                check_box_vsync.update_checkbox(event, mouse_pos)


                check_box_fps1.update_checkbox(event, mouse_pos, part_of_list=check_box_fps)
                check_box_fps2.update_checkbox(event, mouse_pos, part_of_list=check_box_fps)
                check_box_fps3.update_checkbox(event, mouse_pos, part_of_list=check_box_fps)

                check_box_res1.update_checkbox(event, mouse_pos, part_of_list=check_box_res)
                check_box_res2.update_checkbox(event, mouse_pos, part_of_list=check_box_res)
                check_box_res3.update_checkbox(event, mouse_pos, part_of_list=check_box_res)

            if menu_status == "single_player_lobby":

                check_box_inter.update_checkbox(event, mouse_pos)

                for x in check_box_difficulties:
                    x.update_checkbox(
                        event, mouse_pos, part_of_list=check_box_difficulties
                    )

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


            if event.type == app.pygame.QUIT:
                sys.exit()
        mouse_single_tick = False
        if app.pygame.mouse.get_pressed()[0] and clicked == False:
            clicked = True
            mouse_single_tick = True
        elif app.pygame.mouse.get_pressed()[0] == False:
            clicked = False

        # screen.fill((round(30 - 15 * math.sin(2*math.pi*background_tick/52)),0,0))
        screen.fill((0, 0, 0))


        if rgb_i > 2:
            rgb_i -= 1


        curr = time.perf_counter()
        if curr - t > beat_time:

            t = curr - (curr - t - beat_time)


            background_tick = 52
            background_vel = 0

            rgb_i = 10

            menu_i += 1

            for i in app.buttons:
                i.red_tick = 10


            last_beat = curr

            if menu_i == len(IS.menu_animations):
                menu_i = 0

        try:

            im = IS.menu_animations[menu_i][
                round(
                    (len(IS.menu_animations[menu_i]) - 1)
                    * (((curr - last_beat)) / beat_time) ** 1
                )
            ]

            x1, y1 = im.get_rect().center

            y2 = (1 - ((curr - last_beat) / beat_time) ** 0.2) * 100

            screen.blit(
                im,
                [size[0]/2-x1, size[1]/2-y1+y2],
            )


        except Exception as e:
            print(e)


            # for y in range(10):
            #     pos = [random.randint(0,size[0]), random.randint(0,size[1])]
            #     for i in range(5):
            #         particle_list.append(classes.Particle(pos, type = "blood_particle", magnitude = 1.3, screen = background))

        # background2 = background.copy()
        #
        # background.fill((0, 0, 0, 0))
        #
        # background.blit(background2, (0,background_vel))
        #
        # screen.blit(background, (0,0))

        text = terminal.render(f"Version {VERSION}", False, [255, 255, 255] if not dirty else [255,0,0])
        screen.blit(text, [10, size[1]-30])


        for x in particle_list:
            x.tick(screen, [0, 0])

        if menu_status == "beta":
            text = terminal.render("Thank you for playing the story beta! Stay tuned for more.", False, [255, 255, 255])
            x,y = text.get_rect().center
            screen.blit(text, [size[0]/2 - x, size[1]/4 - y])

            s1 = button_back_beta.tick(screen, mouse_pos, mouse_single_tick, glitch)

            if s1 != None:
                menu_status = s1



        if menu_status == "res_change":
            text = terminal.render("Rendering resolution change requires restarting the game.", False, [255, 255, 255])
            x,y = text.get_rect().center
            screen.blit(text, [size[0]/2 - x, size[1]/4 - y])

            app.clear_compiled_navmeshes()

            button_restart_game.tick(screen, mouse_pos, mouse_single_tick, glitch)


        if menu_status == "start":
            # screen.blit(info, [20,150])

            func.rgb_render(
                menu_rgb,
                rgb_i ** 1.5,
                [size[0] / 2 - menu_rgb[0].get_rect().center[0] - 20, 10],
                [0, 0],
                screen,
            )

            s1 = button_sp.tick(screen, mouse_pos, mouse_single_tick, glitch)
            s2 = button_mp_menu.tick(screen, mouse_pos, mouse_single_tick, glitch)
            s3 = button_settings.tick(screen, mouse_pos, mouse_single_tick, glitch)
            button_quit_game.tick(screen, mouse_pos, mouse_single_tick, glitch)
            #button_map_creator.tick(screen, mouse_pos, mouse_single_tick, glitch)

            if s1 != None:
                menu_status = s1
                mouse_single_tick = False
            if s2 != None:
                menu_status = s2
                mouse_single_tick = False

            if s3 != None:
                menu_status = s3
                mouse_single_tick = False

        if menu_status == "settings":

            s8_2 = button_savesettings.tick(screen, mouse_pos, mouse_single_tick, glitch)

            scroll_bar_volume.tick(screen, mouse_pos, clicked, mouse_single_tick, arg = globals())
            scroll_bar_music.tick(screen, mouse_pos, clicked, mouse_single_tick)

            text = terminal.render("Name:", False, [255, 255, 255])
            screen.blit(text, [20, 207])

            text = terminal.render("FPS Lock", False, [255, 255, 255])
            screen.blit(text, [400, 207])

            text = terminal.render("Render resolution", False, [255, 255, 255])
            screen.blit(text, [600, 207])

            textbox_name.tick(screen, mouse_single_tick, mouse_pos, events)

            check_box_fov.render_checkbox()

            check_box_dev_commands.render_checkbox()


            check_box_fs.render_checkbox()

            check_box_vsync.render_checkbox()

            for x in check_box_fps:
                x.render_checkbox()

                if x.checked:
                    app.fps = x.caption

            for x in check_box_res:
                x.render_checkbox()



            if s8_2 != None:
                menu_status = s8_2
                mouse_single_tick = False

        if menu_status == "mp_start":
            s4, net1, host = button_host_game.tick(
                screen, mouse_pos, mouse_single_tick, glitch
            )
            list = button_join_game.tick(
                screen, mouse_pos, mouse_single_tick, glitch, arg=app.ip
            )

            if list != None:
                s5, net2, a1 = list
            else:
                s5 = None
                net2 = None
                a1 = None

            s6 = button_back.tick(screen, mouse_pos, mouse_single_tick, glitch)
            if app.dev:
                sButtonUpnp = buttonUpnp.tick(
                    screen, mouse_pos, mouse_single_tick, glitch
                )
            else:
                sButtonUpnp = None

            if app.net == None and net1 != None:
                app.net = net1
                print("NETWORK SAVED")
            if app.net == None and net2 != None:
                app.net = net2
                print("NETWORK SAVED")
            if s4 != None:
                menu_status = s4
                print("Game hosted")
                mouse_single_tick = False
            if s5 != None:
                button_join_game.__dict__["args"] = app.ip
                menu_status = s5
                mouse_single_tick = False
            if s6 != None:
                menu_status = s6
                mouse_single_tick = False
            if sButtonUpnp != None:
                menu_status = sButtonUpnp
                print(f"--------------menu status:{menu_status}")
                mouse_single_tick = False

        if menu_status == "upnp_menu":
            text = terminal.render(
                "This is a STUB menu - more to come.", False, [255, 255, 255]
            )
            screen.blit(text, [430 - text.get_rect().size[0] / 2, 20])
            text = terminal.render(
                "{button to enter here only visible with dev tools enabled}",
                False,
                [255, 255, 255],
            )
            screen.blit(text, [430 - text.get_rect().size[0] / 2, 80])

            sButtonUpnpTest = buttonUpnpTest.tick(
                screen, mouse_pos, mouse_single_tick, glitch
            )
            if sButtonUpnpTest != None:
                print("stub ... exiting game here by design...")
                sys.exit()

            sButtonUpnpBack = buttonUpnpBack.tick(
                screen, mouse_pos, mouse_single_tick, glitch
            )
            if sButtonUpnpBack != None:
                menu_status = sButtonUpnpBack
                mouse_single_tick = False

        if menu_status == "sp":

            s1 = button_sp_continue_game.tick(screen, mouse_pos, mouse_single_tick, glitch)
            s2 = button_sp_new_game.tick(screen, mouse_pos, mouse_single_tick, glitch)
            s3 = button_sp_menu.tick(screen, mouse_pos, mouse_single_tick, glitch)
            s4 = button_back_sp.tick(screen, mouse_pos, mouse_single_tick, glitch)


            for x in [s1, s2, s3, s4]:
                if x != None:
                    menu_status = x
                    mouse_single_tick = False



        if menu_status == "single_player_lobby":

            # text = terminal.render("SINGLEPLAYER LOBBY", False, [255,255,255])
            # screen.blit(text, [400,20])



            check_box_inter.render_checkbox()

            intervals = check_box_inter.__dict__["checked"]

            for diff in check_box_difficulties:
                diff.render_checkbox()

                if diff.__dict__["checked"]:
                    difficulty = diff.__dict__["caption"]
                    button_start_single_player.__dict__["args"] = difficulty

            render_selected_map(screen, maps_dict, app, mouse_pos, mouse_single_tick, difficulty, mp = False, host = True)

            s7_2 = button_start_single_player.tick(screen, mouse_pos, mouse_single_tick, glitch)
            s8_2 = button_client_quit.tick(screen, mouse_pos, mouse_single_tick, glitch)

            text = terminal2.render(diff_captions[difficulty], False, [255, 255, 255])
            screen.blit(text, [20, 370])

            if s7_2 != None:
                menu_status = s7_2
                mouse_single_tick = False
            if s8_2 != None:
                menu_status = "sp"
                mouse_single_tick = False

        if menu_status == "lobby":

            render_selected_map(screen, maps_dict, app, mouse_pos, mouse_single_tick, 0, mp = True, host = host)

            text = terminal.render("Players:", False, [255, 255, 255])

            screen.blit(text, [20, 200])




            i = 210
            for y in app.players:
                if y == "" or y == "clients":
                    continue
                i += 20
                text = terminal.render(y, False, [255, 255, 255])
                screen.blit(text, [30, i])
            if host:
                button_start_multi_player_host.tick(screen, mouse_pos, mouse_single_tick, glitch)
            s8 = button_host_quit.tick(screen, mouse_pos, mouse_single_tick, glitch)
            if s8 != None:
                menu_status = s8

        if menu_status == "warningScreen":
            y_pos = 40
            for textStr in [
                "Multiplayer is barely functional,",
                "and only works in local networks.",
                "Do you wish to continue?",
            ]:

                text = terminal.render(textStr, False, [255, 255, 255])
                screen.blit(text, [size[0]/2 - text.get_size()[0]/2, y_pos])
                y_pos += 40

            s5 = button_WarnContinue.tick(screen, mouse_pos, mouse_single_tick, glitch)

            s6 = button_back.tick(screen, mouse_pos, mouse_single_tick, glitch)
            if s6 != None:
                menu_status = s6
                mouse_single_tick = False

            if s5 != None:

                menu_status = "mp_start"
                mouse_single_tick = False

                app.MULT_ACKNOWLEDGEMENT = True
                app.write_prefs()


        if menu_status == "mp_start":

            # text = terminal.render("Your IP: -", False, [255,255,255])
            # screen.blit(text, [30,420])

            type = "(LOCAL NETWORK)" if ip_address[:3] == "192" else ""

            text = terminal.render("Your IP: " + ip_address + " " + type, False, [255, 255, 255])
            screen.blit(text, [30, 420])

            text = terminal.render("Joining to:", False, [255, 255, 255])
            screen.blit(text, [500, 420])

            textbox_ip.tick(screen, mouse_single_tick, mouse_pos, events)

        # print(thread.active_count())
        glitch.tick()

        if not fade_tick.tick():
            tick = fade_tick.rounded()
            if 0 <= tick <= 9:
                screen.blit(fade_to_black_screen[tick], [0, 0])

            elif 51 <= tick <= 60:
                screen.blit(fade_to_black_screen[60 - tick], [0, 0])

            else:
                screen.fill([0, 0, 0])


        if glitch.glitch_tick > 0:
            image_copy = screen.copy()
            screen.fill((menu_alpha,menu_alpha,menu_alpha))
            func.blit_glitch(screen, image_copy, [0,0], round(10*glitch.glitch_tick))

        app.pygame.display.update()

        if TEST:
            return


if __name__ == "__main__":
    try:
        main()
        # If main() completes without any errors, write a blank txt file
        with open("error_log.txt", "w") as file:
            file.write("")
    except Exception as e:
        # If an exception occurs, write the full traceback into a txt file
        with open("error_log.txt", "w") as file:
            traceback.print_exc(file=file)

        print(traceback.format_exc())
