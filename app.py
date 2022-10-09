# Work in progress - very basic app class shell:
# goal: support passing obj instances between modules,
# move funcs out of RUN.property
# - Contrib: Velas2
from maps import maps
import get_preferences
from networking.server import Server
from networking.chat import Chat
from networking.datagatherer import DataGatherer

import game
from values import *
import func


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
        self.path_times = {"calc" : [0, 0], "cache" : [0, 0]}

        self.player_team = placeholder


        self.zombiegroup = pygame.sprite.Group()
        self.unitstatuses = []
        self.screen_glitch = 1

        self.levels = ["Requiem", "Manufactory", "Liberation"]
        self.day = 0

    def collect_data(self):
        #self.chat.tick()
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
        ) = get_preferences.pref()

    def write_prefs(self):
        get_preferences.write_prefs(
            self.name, self.draw_los, self.dev, self.fs, self.ultraviolence, self.ip, self.fps, self.vsync, self.res
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





    def update_screen(self):

        if self.vsync:
            vs = 1
        else:
            vs = 0

        if self.fs:
            screen = self.pygame.display.set_mode(size, pygame.FULLSCREEN | pygame.SCALED , vsync=vs)
            mouse_conversion = 1
        else:
            print("Setting to windowed")
            screen = self.pygame.display.set_mode(size, pygame.RESIZABLE, vsync=vs)
            mouse_conversion = 1

        return screen, mouse_conversion




    def lobby_host(self, thread, ip):
        print("SERVER STARTING")
        self.server.server_run()

    def getMaps(self):
        maps_dict = {}
        self.maps_dict = maps_dict
        self.maps = maps
        for index, map_1 in enumerate(maps):
            map_surf = map_1.__dict__["background"]
            x, y = map_surf.get_rect().size
            scale_factor = (200*(size[0]/854)) / x
            img = self.pygame.transform.scale(
                map_surf, (x * scale_factor, y * scale_factor)
            )
            maps_dict[index] = {"map": map_1, "image": img}
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



    def start_multiplayer_client(self, arg):
        reply = self.net.send("/STARTGAME/")
        self.write_prefs()
        func.load_screen(screen, "Loading")
        game.main(
            self,
            multiplayer=True,
            net=self.net,
            players=players,
            self_name=self.name,
            map=maps_dict[selected_map]["map"],
        )
