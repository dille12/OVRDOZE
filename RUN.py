import os, sys
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
import server
import game
import hud_elements
import get_preferences
import func
from glitch import Glitch
from button import Button
#import path_finding
from app import App
import map_creator
from menu import Menu
def main():

    app = App(pygame,server)

    terminal = pygame.font.Font('texture/terminal.ttf', 20)
    terminal2 = pygame.font.Font('texture/terminal.ttf', 30)
    prompt = pygame.font.Font('texture/terminal.ttf', 14)
    maps_dict = app.getMaps()
    selected_map = 0

    full_screen = pygame.display.set_mode(fs_size, pygame.FULLSCREEN)

    screen =  app.pygame.Surface(size).convert()
    mouse_conversion = fs_size[0] /  size[0] # = 2.25
    clock = app.pygame.time.Clock()
    print("run init")

    menu_status = "start"

    app.pygame.mouse.set_visible(True)

    terminal = app.pygame.font.Font('texture/terminal.ttf', 20)
    terminal2 = app.pygame.font.Font('texture/terminal.ttf', 10)

    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)


    ip = ""
    #app.name += str(random.randint(1,109))
    textbox_name = hud_elements.text_box((100,200), app.name)
    textbox_ip = hud_elements.text_box((640,415), ip)

    textbox_ip.__dict__["text"] = app.last_ip
    players = []
    port = 5555


    intro1 = func.load_animation("anim/intro1",0,30, alpha = 70)
    intro2 = func.load_animation("anim/intro2",30,30, alpha = 70)
    intro3 = func.load_animation("anim/intro3",60,31, alpha = 70)

    menu_animations = [intro1, intro2, intro3]
    menu_i = 0



    def start_mp_game(arg):
        reply = net.send("start_game")
        start_multiplayer_client()

    def start_map_creator(arg):
        map_creator.main(app)


    def host_game(arg) :
        print("HOSTING GAME")
        textbox_ip.__dict__["text"] = ip_address
        ip = ip_address
        try:
            start_new_thread(app.lobby_host, ("1", ip) )
            return join_game(ip, True)
        except:
            return "start", None, None

    def upnp_menu(arg):
        if app.dev:
            print('test')
            return('upnp_menu')
    def upnp_test(arg):
        if app.dev:
            print('upnp_test')
            return('upnp_test')

    def start_multiplayer_client():
        game.main(app, multiplayer = True, net = net, players = players, self_name = app.name, map = maps_dict[selected_map]["map"], full_screen_mode = full_screen_mode)


    def join_game(arg, host = False):

        print("JOINING TO:", arg)

        try:
            net = Network(arg)

            print("CLIENT: STARTING SEARCH")

            reply = net.send(app.name)
            if reply != [""]:

                print("CLIENT:", reply)
                print("CLIENT: CONNECTED")

                return "lobby", net, host
            else:
                print("CLIENT: No connection found")
                return "start", None, None
        except Exception as e:
            print("CLIENT: Connection failed")
            print(e)
            return "start", None, None

    def main_menu(arg):
        get_preferences.write_prefs(app.name, app.draw_los, app.dev, app.fs,
          app.ultraviolence, app.ip)
        return "start"


    def quit(args):

        get_preferences.write_prefs(app.name, app.draw_los, app.dev, app.fs,
          app.ultraviolence, app.ip)

        sys.exit()

    def start_sp(arg):
        print("SPa")

        get_preferences.write_prefs(app.name, app.draw_los, app.dev, app.fs,
          app.ultraviolence, app.ip)
        args = (app,app.name,arg,app.draw_los,app.dev,
          check_box_inter.__dict__["checked"],
          maps_dict[selected_map]["map"],full_screen_mode)

        app.start_sp(args)

    def start_mp(arg):
        return "mp_start"

    def settings(arg):
        return "settings"

    def kill_server(arg):
        reply = net.send("kill")
        return "start"

    def sp_lob(arg):
        return "single_player_lobby"


    host = False
    background_tick = 1

    app.pygame.mixer.music.load("sound/songs/menu_loop.wav")
    app.pygame.mixer.music.play(-1)
    t = time.time() - 0.85714285714
    glitch = Glitch(screen)

    x_s = size[0]/2

    difficulty = "NORMAL"

    button_sp_menu = Button([x_s,200], "Singleplayer", sp_lob, None,gameInstance=app.pygame,glitchInstance=glitch)
    button_mp_menu = Button([x_s,260], "Multiplayer", start_mp, None,gameInstance=app.pygame,glitchInstance=glitch)
    button_settings = Button([x_s,320], "Settings", settings, None,gameInstance=app.pygame,glitchInstance=glitch)

    button_quit_game = Button([x_s,380], "Exit", quit, None, gameInstance=app.pygame, glitchInstance=glitch)



    button_host_game = Button([x_s,100], "Host", host_game, "3",gameInstance=app.pygame,glitchInstance=glitch)
    button_join_game = Button([x_s,160], "Join", join_game, app.ip,gameInstance=app.pygame,glitchInstance=glitch)
    button_back = Button([x_s,220], "Back", main_menu, None,gameInstance=app.pygame,glitchInstance=glitch)
    buttonUpnp = Button([x_s,280], "dev-test-upnp", upnp_menu, "upnp_menu",gameInstance=app.pygame,glitchInstance=glitch)


    button_start_sp = Button([140,70], "START GAME", start_mp_game, None,gameInstance=app.pygame,glitchInstance=glitch)
    button_start_mp = Button([140,70], "START GAME", start_sp, difficulty,gameInstance=app.pygame,glitchInstance=glitch)
    button_host_quit = Button([68,130], "Back", kill_server, None,gameInstance=app.pygame,glitchInstance=glitch)
    button_client_quit = Button([68,130], "Back", main_menu, None,gameInstance=app.pygame,glitchInstance=glitch)

    buttonUpnpTest = Button([x_s,280], "dev-test-upnp", upnp_test, "upnp_test",gameInstance=app.pygame,glitchInstance=glitch)
    buttonUpnpBack = Button([x_s,220], "Back", start_mp, None,gameInstance=app.pygame,glitchInstance=glitch)

    check_box_difficulties = []

    for text, y_pos in [["NO ENEMIES", 200], ["NORMAL", 240], ["HARD",280], ["ONSLAUGHT", 320]]:
        box = hud_elements.Checkbox(screen, 20,y_pos, caption = text, font_color = [255,255,255], text_offset = [40,5], cant_uncheck = True)

        if text == "NORMAL":
            box.__dict__["checked"] = True
        check_box_difficulties.append(box)


    background = app.pygame.Surface((size[0]+50,size[1]), app.pygame.SRCALPHA, 32).convert_alpha()
    #
    background.set_alpha(240)

    background2 = app.pygame.Surface(size, app.pygame.SRCALPHA, 32).convert_alpha()
    check_box_dev_commands = hud_elements.Checkbox(screen, 20,300, caption = "Dev tools", font_color = [255,255,255], text_offset = [40,5])

    check_box_inter = hud_elements.Checkbox(screen, 20,400, caption = "Ceaseless Storm", font_color = [255,0,0], text_offset = [40,5])

    if app.dev:
        check_box_dev_commands.__dict__["checked"] = True

    check_box_fov = hud_elements.Checkbox(screen, 20, 260, caption = "Fog of War", font_color = [255,255,255], text_offset = [40,5])

    if app.draw_los:
        check_box_fov.__dict__["checked"] = True

    check_box_ultra = hud_elements.Checkbox(screen, 20,380, caption = "Ultraviolence", font_color = [255,0,0], text_offset = [40,5])

    check_box_fs = hud_elements.Checkbox(screen, 20, 340, caption = "Fullscreen", font_color = [255,255,255], text_offset = [40,5])
    if app.fs:
        check_box_fs.__dict__["checked"] = True
    if app.ultraviolence:
        check_box_ultra.__dict__["checked"] = True

    diff_captions = {"NO ENEMIES" : "For testing.",
    "NORMAL" : "Sanity drain, zombie health and damage are normal.",
    "HARD" : "Sanity drains 25% faster, zombies have 25% more health and 10% more damage. Turrets have 15% less bullets.",
    "ONSLAUGHT" : "Sanity drains 50% faster, zombies have 35% more health and 20% more damage. Turrets have 30% less bullets."
    }

    net = None
    background_vel = 0
    buttons =[
        button_sp_menu,
        button_mp_menu,
        button_settings,
        button_host_game,
        button_join_game,
        button_start_mp,
        buttonUpnp,
        button_start_sp,
        button_start_mp,
        button_host_quit,
        button_client_quit,
        buttonUpnpTest,
        buttonUpnpBack,
        button_back,
        button_quit_game,
    ]
    checkboxes=[
        check_box_difficulties,
        check_box_dev_commands,
        check_box_inter,
        check_box_fov,
        check_box_ultra,
        check_box_fs,


    ]
    game_state = {
        "selected_map":selected_map,
        "players":players,
        "hostname":hostname,
        "ip":ip_address,
        "port":port,
        "difficulty":difficulty,
        "background_tick":background_tick,
        "background_vel":background_vel,
        "checked_boxes":[],
        "get_mouse_pos":app.pygame.mouse.get_pos,#ref to func to call from menue
        "mouse_pos":app.pygame.mouse.get_pos()
        }



    game_menu = Menu(
        buttons=buttons,
        checkboxes=checkboxes,
        background=background,
        screen=screen,
        terminal1=terminal,
        terminal2=terminal2,
        particle_list=particle_list,

        )

    app.pygame.display.set_gamma(1,1,1)

    rgb_i = 2

    last_beat = time.time()

    while 1:
        #game_menu.update(game_state)
        #menu should cover a lot of the while loop -


        if background_tick != 0:
            background_tick -= 1
            background_vel += 0.2
        else:

            print("RESET")
            background_tick = 52

        clock.tick(60)

        app.name = textbox_name.__dict__["text"]
        app.ip = textbox_ip.__dict__["text"]
        events = app.pygame.event.get()

        full_screen_mode = check_box_fs.__dict__["checked"]

        app.dev = check_box_dev_commands.__dict__["checked"]
        app.ultraviolence = check_box_ultra.__dict__["checked"]
        app.draw_los = check_box_fov.__dict__["checked"]


        mouse_pos = app.pygame.mouse.get_pos()

        mouse_pos = [mouse_pos[0] / mouse_conversion, mouse_pos[1] / mouse_conversion]
        game_state["mouse_pos"]=mouse_pos
        for event in events:
            if menu_status == "settings":
                check_box_fov.update_checkbox(event, mouse_pos)
                check_box_dev_commands.update_checkbox(event, mouse_pos)
                check_box_ultra.update_checkbox(event, mouse_pos)
                check_box_fs.update_checkbox(event, mouse_pos)

            if menu_status == "single_player_lobby":

                check_box_inter.update_checkbox(event, mouse_pos)

                for x in check_box_difficulties:
                    x.update_checkbox(event, mouse_pos, part_of_list = check_box_difficulties)

            if event.type == app.pygame.QUIT: sys.exit()
        mouse_single_tick = False
        if app.pygame.mouse.get_pressed()[0] and clicked == False:
            clicked = True
            mouse_single_tick = True
        elif app.pygame.mouse.get_pressed()[0] == False:
            clicked = False

        #screen.fill((round(30 - 15 * math.sin(2*math.pi*background_tick/52)),0,0))
        screen.fill((0,0,0))
        try:
            screen.blit(menu_animations[menu_i][round((len(menu_animations[menu_i])-1) * ((time.time() - last_beat)/0.85714285714) ** 0.75)], [0,0])
        except Exception as e:
            print(e)


        if rgb_i > 2:
            rgb_i -= 1

        if time.time() - t > 0.85714285714:
            t = time.time() - (time.time() - t - 0.85714285714)

            background_tick = 52
            background_vel = 0

            rgb_i = 10

            menu_i += 1

            last_beat = time.time()



            if menu_i == len(menu_animations):
                menu_i = 0

            for y in range(10):
                pos = [random.randint(0,size[0]), random.randint(0,size[1])]
                for i in range(5):
                    particle_list.append(classes.Particle(pos, type = "blood_particle", magnitude = 1.3, screen = background))

        background2 = background.copy()

        background.fill((0, 0, 0, 0))

        background.blit(background2, (0,background_vel))

        screen.blit(background, (0,0))

        for x in particle_list:
            x.tick(screen, [0,0])

        if menu_status == "start":
            #screen.blit(info, [20,150])

            func.rgb_render(menu_rgb, rgb_i, [size[0]/2 - menu_rgb[0].get_rect().center[0] - 20, 10], [0,0], screen)

            s1 = button_sp_menu.tick(screen, mouse_pos, mouse_single_tick, glitch)
            s2= button_mp_menu.tick(screen, mouse_pos, mouse_single_tick, glitch)
            s3 = button_settings.tick(screen, mouse_pos, mouse_single_tick, glitch)
            button_quit_game.tick(screen, mouse_pos, mouse_single_tick, glitch)

            if s1 != None:
                menu_status = s1
                mouse_single_tick = False
            if s2 != None:
                menu_status  = s2
                mouse_single_tick = False

            if s3 != None:
                menu_status  = s3
                mouse_single_tick = False

        if menu_status == "settings":

            s8_2 = button_client_quit.tick(screen, mouse_pos, mouse_single_tick, glitch)

            text = terminal.render("Name:", False, [255,255,255])
            screen.blit(text, [20,207])

            textbox_name.tick(screen, mouse_single_tick, mouse_pos, events)

            check_box_fov.render_checkbox()

            check_box_dev_commands.render_checkbox()

            check_box_ultra.render_checkbox()

            check_box_fs.render_checkbox()

            if s8_2 != None:
                menu_status  = s8_2
                mouse_single_tick = False

        if menu_status == "mp_start":
            s4, net1, host = button_host_game.tick(screen, mouse_pos, mouse_single_tick, glitch)
            list  = button_join_game.tick(screen, mouse_pos, mouse_single_tick, glitch, arg = app.ip)

            if list != None:
                s5, net2, a1 = list
            else:
                s5 = None
                net2 = None
                a1 = None

            s6 = button_back.tick(screen, mouse_pos, mouse_single_tick, glitch)
            if app.dev:
                sButtonUpnp = buttonUpnp.tick(screen, mouse_pos, mouse_single_tick, glitch)
                print(f"sButtonUpnp:{sButtonUpnp}")
            else:
                sButtonUpnp = None

            if net == None and net1 != None:
                net = net1
                print("NETWORK SAVED")
            if net == None and net2 != None:
                net = net2
                print("NETWORK SAVED")
            if s4 != None:
                menu_status  = s4
                print("Game hosted")
                mouse_single_tick = False
            if s5 != None:
                button_join_game.__dict__["args"] = app.ip
                menu_status  = s5
                mouse_single_tick = False
            if s6 != None:
                menu_status  = s6
                mouse_single_tick = False
            if sButtonUpnp != None:
                menu_status  = sButtonUpnp
                print(f'--------------menu status:{menu_status}')
                mouse_single_tick = False

        if menu_status == "upnp_menu":
            print('tst2')
            text = terminal.render("This is a STUB menu - more to come.", False, [255,255,255])
            screen.blit(text, [430- text.get_rect().size[0]/2,20])
            text = terminal.render("{button to enter here only visible with dev tools enabled}", False, [255,255,255])
            screen.blit(text, [430- text.get_rect().size[0]/2,80])

            sButtonUpnpTest = buttonUpnpTest.tick(screen, mouse_pos, mouse_single_tick, glitch)
            if sButtonUpnpTest != None:
                print('stub ... exiting game here by design...')
                sys.exit()

            sButtonUpnpBack = buttonUpnpBack.tick(screen, mouse_pos, mouse_single_tick, glitch)
            if sButtonUpnpBack != None:
                menu_status  = sButtonUpnpBack
                mouse_single_tick = False

        if menu_status == "single_player_lobby":

            # text = terminal.render("SINGLEPLAYER LOBBY", False, [255,255,255])
            # screen.blit(text, [400,20])

            text = terminal.render("MAP", False, [255,255,255])
            screen.blit(text, [430- text.get_rect().size[0]/2,20])

            rect_map = maps_dict[selected_map]["image"].get_rect()

            if rect_map.collidepoint(func.minus(mouse_pos,[330,80],"-")):

                if mouse_single_tick:
                    selected_map += 1

                    menu_click2.play()

                    if selected_map == len(maps_dict):
                        selected_map = 0

                rect_map = maps_dict[selected_map]["image"].get_rect()

                rect_map.inflate_ip(4,4)

                app.pygame.draw.rect(screen, [255,255,255], rect_map.move([330,80]))


            screen.blit(maps_dict[selected_map]["image"], [330,80])

            rect_map2 = maps_dict[selected_map]["image"].get_rect()

            text = terminal.render(maps_dict[selected_map]["map"].__dict__["name"], False, [255,255,255])
            screen.blit(text, [430- text.get_rect().size[0]/2,50])

            app.pygame.draw.line(screen, [255,255,255], [550, 80], [550, 80 + rect_map2.h])
            app.pygame.draw.line(screen, [255,255,255], [550, 80], [545, 80])
            app.pygame.draw.line(screen, [255,255,255], [550, 80 + rect_map2.h], [545, 80 + rect_map2.h])

            text = terminal.render(str(round(maps_dict[selected_map]["map"].__dict__["size"][1]/100)) + "m", False, [255,255,255])
            screen.blit(text, [552,80 + rect_map2.h/2 - text.get_rect().size[1]/2])

            app.pygame.draw.line(screen, [255,255,255], [330, 100 + rect_map2.h], [530, 100 + rect_map2.h])
            app.pygame.draw.line(screen, [255,255,255], [330, 100 + rect_map2.h], [330, 95 + rect_map2.h])
            app.pygame.draw.line(screen, [255,255,255], [530, 100 + rect_map2.h], [530, 95 + rect_map2.h])

            text = terminal.render(str(round(maps_dict[selected_map]["map"].__dict__["size"][0]/100)) + "m", False, [255,255,255])
            screen.blit(text, [430- text.get_rect().size[0]/2,105 + rect_map2.h])


            check_box_inter.render_checkbox()

            intervals = check_box_inter.__dict__["checked"]


            for diff in check_box_difficulties:
                diff.render_checkbox()

                if diff.__dict__["checked"]:
                    difficulty = diff.__dict__["caption"]
                    button_start_mp.__dict__["args"] = difficulty

            s7_2 = button_start_mp.tick(screen, mouse_pos, mouse_single_tick, glitch)
            s8_2 = button_client_quit.tick(screen, mouse_pos, mouse_single_tick, glitch)

            text = terminal2.render(diff_captions[difficulty], False, [255,255,255])
            screen.blit(text, [20, 370])

            if s7_2 != None:
                menu_status  = s7_2
                mouse_single_tick = False
            if s8_2 != None:
                menu_status  = s8_2
                mouse_single_tick = False

        if menu_status == "lobby":

            text = terminal.render("MAP", False, [255,255,255])
            screen.blit(text, [430- text.get_rect().size[0]/2,20])

            rect_map = maps_dict[selected_map]["image"].get_rect()


            if host:
                text = terminal.render("LOBBY (HOSTING)", False, [255,255,255])
                screen.blit(text, [30,20])
                text = terminal.render("HOSTED AT:" + ip_address, False, [255,255,255])
                screen.blit(text, [500,420])

                if rect_map.collidepoint(func.minus(mouse_pos,[330,80],"-")):

                    if mouse_single_tick:
                        selected_map += 1

                        menu_click2.play()

                        if selected_map == len(maps_dict):
                            selected_map = 0

                    rect_map = maps_dict[selected_map]["image"].get_rect()

                    rect_map.inflate_ip(4,4)

                    app.pygame.draw.rect(screen, [255,255,255], rect_map.move([330,80]))
            else:
                text = terminal.render("LOBBY", False, [255,255,255])
                screen.blit(text, [30,20])
                text = terminal.render("HOSTED AT:" + app.ip, False, [255,255,255])
                screen.blit(text, [500,420])
            #screen.blit(text, [400,20])

            screen.blit(maps_dict[selected_map]["image"], [330,80])


            text = terminal.render(maps_dict[selected_map]["map"].__dict__["name"], False, [255,255,255])
            screen.blit(text, [430- text.get_rect().size[0]/2,50])

            rect_map2 = maps_dict[selected_map]["image"].get_rect()

            text = terminal.render(maps_dict[selected_map]["map"].__dict__["name"], False, [255,255,255])
            screen.blit(text, [430- text.get_rect().size[0]/2,50])

            app.pygame.draw.line(screen, [255,255,255], [550, 80], [550, 80 + rect_map2.h])
            app.pygame.draw.line(screen, [255,255,255], [550, 80], [545, 80])
            app.pygame.draw.line(screen, [255,255,255], [550, 80 + rect_map2.h], [545, 80 + rect_map2.h])

            text = terminal.render(str(round(maps_dict[selected_map]["map"].__dict__["size"][1]/100)) + "m", False, [255,255,255])
            screen.blit(text, [552,80 + rect_map2.h/2 - text.get_rect().size[1]/2])

            app.pygame.draw.line(screen, [255,255,255], [330, 100 + rect_map2.h], [530, 100 + rect_map2.h])
            app.pygame.draw.line(screen, [255,255,255], [330, 100 + rect_map2.h], [330, 95 + rect_map2.h])
            app.pygame.draw.line(screen, [255,255,255], [530, 100 + rect_map2.h], [530, 95 + rect_map2.h])

            text = terminal.render(str(round(maps_dict[selected_map]["map"].__dict__["size"][0]/100)) + "m", False, [255,255,255])
            screen.blit(text, [430- text.get_rect().size[0]/2,105 + rect_map2.h])

            text = terminal.render("Players:", False, [255,255,255])

            screen.blit(text, [20,200])

            if host:
                reply = net.send("index:" + str(selected_map))
            else:
                reply = net.send("un")


            if reply == "KILL":
                menu_status = "start"

            if reply == "start_game/":
                print("STARTING GAME")
                start_multiplayer_client()

            else:
                try:
                    reply2 = reply.split("#END")[0]
                    data = reply2.split("\n")
                    for line in data:
                        type, info1 = line.split(":")
                        if type == "players":
                            players = info1.split("/")
                        elif type == "index" and not host:
                            selected_map = int(info1)

                except Exception as e:
                    pass

            i = 210
            for y in players:
                if y == "" or y == "clients":
                    continue
                i += 20
                text = terminal.render(y, False, [255,255,255])
                screen.blit(text, [30,i])
            if host:
                button_start_sp.tick(screen, mouse_pos, mouse_single_tick, glitch)
            s8 = button_host_quit.tick(screen, mouse_pos, mouse_single_tick, glitch)
            if s8 != None:
                menu_status  = s8

        if menu_status == "mp_start":

            # text = terminal.render("Your IP: -", False, [255,255,255])
            # screen.blit(text, [30,420])

            text = terminal.render("Your IP: " + ip_address, False, [255,255,255])
            screen.blit(text, [30,420])

            text = terminal.render("Joining to:", False, [255,255,255])
            screen.blit(text, [500,420])

            textbox_ip.tick(screen, mouse_single_tick, mouse_pos, events)

        #print(thread.active_count())
        glitch.tick()
        app.pygame.transform.scale(screen, full_screen.get_rect().size, full_screen)

        app.pygame.display.update()


if __name__ == "__main__":
    main()
