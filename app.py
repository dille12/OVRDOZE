# Work in progress - very basic app class shell:
# goal: support passing obj instances between modules, move funcs out of RUN.property
# - Contrib: Velas2
from maps import maps
class App:
    def __init__(self,pygame,server):
        self.pygame = pygame
        self.server = server

    def lobby_host(self,thread, ip):
        print("SERVER STARTING")
        server.server_run()
    def getMaps(self):
            maps_dict = {}

            index = 0

            for map_1 in maps:

                map_surf = map_1.__dict__["background"]

                x,y = map_surf.get_rect().size

                scale_factor = 200/x

                maps_dict[index] = {"map" : map_1, "image" : self.pygame.transform.scale(map_surf, (x*scale_factor, y*scale_factor))}

                index += 1
            return maps_dict
