# Work in progress - very basic app class shell:
# goal: support passing obj instances between modules,
# move funcs out of RUN.property
# - Contrib: Velas2
from maps import maps
import get_preferences
import server
import game


class App:
    def __init__(self, pygame, server):
        self.pygame = pygame
        self.server = server
        self.ip = None
        (
            self.name,
            self.draw_los,
            self.dev,
            self.fs,
            self.ultraviolence,
            self.last_ip,
        ) = get_preferences.pref()
        pygame.init()
        pygame.font.init()

    def lobby_host(self, thread, ip):
        print("SERVER STARTING")
        server.server_run()

    def getMaps(self):
        maps_dict = {}
        self.maps = maps
        for index, map_1 in enumerate(maps):
            map_surf = map_1.__dict__["background"]
            x, y = map_surf.get_rect().size
            scale_factor = 200 / x
            img = self.pygame.transform.scale(
                map_surf, (x * scale_factor, y * scale_factor)
            )
            maps_dict[index] = {"map": map_1, "image": img}
        return maps_dict

    def start_sp(self, arg):
        print("SP")
        # get_preferences.write_prefs(name, draw_los, dev, ultraviolence, ip)
        app, name, arg, draw_los, dev, skip_intervals, map, full_screen_mode = arg

        game.main(
            app,
            self_name=name,
            difficulty=arg,
            draw_los=draw_los,
            dev_tools=dev,
            skip_intervals=skip_intervals,
            map=map,
            full_screen_mode=full_screen_mode,
        )
