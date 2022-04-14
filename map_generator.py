import math
import pygame
import classtest
import classes
import func
from values import *
map_size = 30000, 20000
x_division = 10
screen = pygame.display.set_mode((900,600))
clock = pygame.time.Clock()

scale = 900/30000

random.seed(10)


class building:
    def __init__(self,x,y,w,h):
        building_size_scale = 1000
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.w_2 = w*building_size_scale
        self.h_2 = h*building_size_scale
        self.rect = pygame.Rect(self.x, self.y, self.w_2, self.h_2)

    def collision_check(self,x,y):
        print(x,y)
        if self.rect.collidepoint([x,y]):
            return True
        return False

    def return_rect(self):
        return self.rect

def check_closest_building(buildings, point):
    closest = 0
    for x in buildings:

        if x.__dict__["x"] <= point <= x.__dict__["x"] + x.__dict__["w_2"]:

            pass
        else:
            continue


        height = x.__dict__["y"] + x.__dict__["h_2"]

        if height > closest:
            closest = height
            closest_b = x
    return closest



def generate():

    map_tiles = {}

    div_x = map_size[0]/x_division
    div_y = map_size[1]/x_division


    for x in range(x_division):
        map_tiles[x*div_x] = {}

        for y in range(x_division):
            if y*div_y > map_size[1]:
                continue
            map_tiles[x*div_x][y*div_y] = {"width": div_x, "height": div_y, "polygons" : [], "objects": []}


    print(map_tiles)

    buildings = []

    x = 10
    y = 10

    building_size_scale = 1000

    while True:
        building_size_x, building_size_y = random.randint(1,4), random.randint(1,4)

        if building_size_x < 0 or x + building_size_x*building_size_scale > map_size[0]:
            print("next row")
            x = random.randint(1,6)*10

            y = check_closest_building(buildings, x)+ 100
            print("CLOSEST:",y)

        else:
            x += building_size_x*building_size_scale +random.randint(0,2)*100
            y += random.randint(-2,2)*100
            if y < 0:
                y = 0



            for b in buildings:
                if b.collision_check(x,y):
                    y_var = check_closest_building(buildings, x)
                    y += y_var + random.randint(1,3)*100
                    break


        if y+building_size_scale*building_size_y > map_size[1]:
            y = 10

        if x+building_size_scale*building_size_x > map_size[0]:
            x = 10

        collided = False
        bui = building(x,y, building_size_x,building_size_y)

        for b in buildings:
            if bui.return_rect().colliderect(b.return_rect()):
                collided = True
                break
        if not collided:
            buildings.append(building(x,y, building_size_x,building_size_y))
            print(x,y)
        if len(buildings) > 40:
            break





    ### HIGHROADS







    return map_tiles, buildings

map_tiles, buildings = generate()

while True:
    screen.fill((0,40,0))
    for x in map_tiles:
        for y in map_tiles[x]:
            pygame.draw.rect(screen,[50,50,50],[x*scale,y*scale, map_tiles[x][y]["width"]*scale, map_tiles[x][y]["height"]*scale], 1)

    for x in buildings:

        pygame.draw.rect(screen,[255,255,50],[x.__dict__["x"]*scale,x.__dict__["y"]*scale, x.__dict__["w_2"]*scale, x.__dict__["h_2"]*scale], 1)

    pygame.display.update()
    clock.tick(60)
