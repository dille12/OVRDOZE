# Work in progress - very basic app class shell:
# goal: support passing obj instances between modules,
# move funcs out of RUN.property
# - Contrib: Velas2
from maps import get_maps
import get_preferences
from networking.server import Server
from networking.chat import Chat
from networking.datagatherer import DataGatherer
import os
import game
from values import *
import func
import ast


class App:
    def __init__(self, pygame):
        self.pygame = pygame
        self.server = Server(self)
        self.ip = None
        self.preferences()
        self.chat = Chat(self)
        self.data_collector = DataGatherer(self)
        print(self.res)
        pygame.init()
        pygame.font.init()
        self.path_cache = {}
        self.path_times = {"calc" : [0, 0], "cache" : [0, 0], "max" : 0}
        self.route = None
        self.player_team = placeholder
        self.net = None

        self.players = [self.name]
        self.nwobjects = {}
        self.selected_map = 0

        self.ping = [0]

        self.soldier_cache = {}

        self.zombiegroup = pygame.sprite.Group()
        self.unitstatuses = []
        self.screen_glitch = 1
        self.pos_sent = False
        self.levels = ["Requiem", "Manufactory", "Liberation", "Contamination"]
        self.day = -1

        self.start_game_with_mp = []


    def send_data(self, line):
        self.data_collector.data.append(line)

    def start_mp_list(self, list):
        self.start_game_with_mp = list

    def append_player(self, name):
        changed = False
        if name not in self.players:
            self.players.append(name)
            changed = True
        if changed:
            self.send_data(f"self.game_ref.append_player('{self.name}')")


    def collect_data(self):
        #self.chat.tick()
        if not self.net:
            return


        try:
            self.data_collector.tick()
        except Exception as e:
            print(e)

    def update_fps(self):
        if self.fps == "60":
            self.clocktick = 60
        elif self.fps == "144":
            self.clocktick = 144
        elif self.fps == "Unlimited":
            self.clocktick = 500

    def set_map(self, id):
        self.selected_map = id
        self.map_tick = 5
        menu_click2.play()

    def clear_compiled_navmeshes(self):
        for map in self.maps:
            if os.path.isfile(map.compiled_file):
                os.remove(map.compiled_file)



    def preferences(self):
        (
            self.name,
            self.draw_los,
            self.dev,
            self.fs,
            self.ultraviolence,
            self.last_ip,
            self.fps,
            self.vsync,
            self.res,
            self.volume,
            self.music,
        ) = get_preferences.pref()

        self.name = str(random.randint(1,9999))

    def write_prefs(self):
        get_preferences.write_prefs(
            self.name, self.draw_los, self.dev, self.fs, self.ultraviolence, self.ip, self.fps, self.vsync, self.res, self.volume, self.music,
        )


    def threaded_player_info_gathering(self):
        self.threading = True

        reply = self.net.send(self.name)

        if "STARTGAME" in reply.split("/"):
            print("Client reveived start order")
            self.start_multiplayer_client(None)
            return

        for x in reply.split("/"):
            y = x.split("-")
            if y[0] == "" or y[0] in self.get_names() or len(y) == 1:
                continue

            print("Player connected:", y[0])

            team = Player(ast.literal_eval(y[1]), y[0], y[2])

            self.game_ref.connected_players.append(team)
            if y[0] == self.name_box.text and self.game_ref.player_team == placeholder:
                print("Assigning to player team")
                self.game_ref.player_team = team

        self.threading = False





    def update_screen(self, return_screen = False):

        if return_screen:
            return pygame.display.get_surface(), 1

        if self.vsync:
            vs = 1
        else:
            vs = 0

        if self.fs:
            screen = pygame.display.set_mode(size, pygame.FULLSCREEN | pygame.SCALED , vsync=vs)
            mouse_conversion = 1
        else:
            print("Setting to windowed")
            screen = pygame.display.set_mode(size, vsync=vs)
            mouse_conversion = 1

        print("Screen update done")

        self.screen_copy = screen

        return screen, mouse_conversion




    def lobby_host(self, thread, ip):
        print("SERVER STARTING")
        self.server.server_run()

    def getMaps(self):
        maps_dict = {}

        self.maps = get_maps(self)
        i = 0
        for map_1 in self.maps:

            map_surf = map_1.__dict__["background"]
            x, y = map_surf.get_rect().size
            scale_factor = (200*(size[0]/854)) / x
            img = self.pygame.transform.scale(
                map_surf, (x * scale_factor, y * scale_factor)
            )

            if map_1.name == "Overworld":
                self.overworld = map_1
            else:
                maps_dict[i] = {"map": map_1, "image": img}
                i += 1

        self.maps_dict = maps_dict
        return maps_dict

    def start_sp(self, arg):
        print("SP")
        # get_preferences.write_prefs(name, draw_los, dev, ultraviolence, ip)
        app, name, arg, draw_los, dev, skip_intervals, map = arg
        func.load_screen(screen, "Loading")
        game.main(
            app,
            self_name=name,
            difficulty=arg,
            draw_los=draw_los,
            dev_tools=dev,
            skip_intervals=skip_intervals,
            map=map,
        )

    def launch_multiplier_server(self, arg):
        print("LAUNCHING!")
        reply = self.net.send(f"PACKET\nself.game_ref.start_mp_list([{self.players}, {self.selected_map}])\nEND#")
        self.start_multiplayer_client(self.players, self.selected_map)



    def start_multiplayer_client(self, players, selected_map):
        self.write_prefs()
        func.load_screen(screen, "Loading")
        game.main(
            self,
            multiplayer=True,
            net=self.net,
            players=players,
            self_name=self.name,
            map=self.maps_dict[selected_map]["map"],
        )
