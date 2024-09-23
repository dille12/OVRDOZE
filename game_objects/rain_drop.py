import pygame
import core.los as los
import core.func as func
import random
from core.values import *

def gen_point_from_map_on_screen(map, camera_pos):
    return (point for point in map.nav_mesh_available_spots if func.get_dist_points(point, camera_pos) < 1000*multiplier2)

class RainDrop:
    def __init__(self, map, player_pos):
        self.map = map
        self.pos = random.choice(list(gen_point_from_map_on_screen(map, player_pos)))
        #self.pos = random.choice(map.nav_mesh_available_spots)
        #map.nav_mesh_available_spots
        self.pos = func.minus(self.pos, [random.randint(-100,100), random.randint(-100,100)])
        #self.pos = func.minus(self.pos, [-200 * multiplier2, 1000*multiplier2], op = "-")
        self.lifetime = 0
        self.lifetime_max = 40
        self.color = [0 + random.randint(0,5), 13 + random.randint(-10,10), 51 + random.randint(-10,10)]
        self.x_pos = random.randint(-250, -150)
        raindrops.append(self)

    def tick(self, screen, camera_pos, map_render):
        #print("Ticking")
        mult = (self.lifetime_max - self.lifetime)/self.lifetime_max
        mult2 = (self.lifetime_max - self.lifetime)/self.lifetime_max + 0.05

        pos1 = func.minus(self.pos.copy(), ( (-self.x_pos*multiplier2) * mult, (-1000*multiplier2) * mult) )
        pos2 = func.minus(self.pos.copy(), ( (-self.x_pos*multiplier2) * mult2, (-1000*multiplier2) * mult2) )


        pygame.draw.line(screen, self.color , func.minus(pos1, camera_pos, op = "-"), func.minus(pos2, camera_pos, op = "-"), round(1*multiplier2))

        self.lifetime += timedelta.mod(1)

        if self.lifetime >= self.lifetime_max:
            raindrops.remove(self)
            surf = pygame.Surface((5,5))
            whiteness = random.randint(1,5)
            surf.fill((whiteness,whiteness,5))
            for i in range(3):
                map_render.blit(surf, func.minus(self.pos.copy(), [random.randint(-5,5), random.randint(-5,5)]), None, pygame.BLEND_RGB_ADD)
