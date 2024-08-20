import os, sys
import pygame
import math
import random
import time
import copy
import socket
from _thread import *
import traceback
import numpy
import func
import los
from itertools import accumulate
import ast
import classes
import traceback
import render_los_image_jit
from tools.image_transform import *
from quadrant import Quadrant
from tools.wall_gen import *
from los import check_los_jit, intersect_jit
from jit_tools import line_intersection
from values import *

def render_center(image, pos):
    im = zoom_transform(image, zoom)
    r_pos = minus([-im.get_rect().center[0], -im.get_rect().center[1]], pos)
    screen.blit(im, r_pos)


pygame.init()
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


object_list = {}


class Object:
    def __init__(self, sub_object):
        global object_list
        self.__object = sub_object
        priority = sub_object.priority()
        if priority not in object_list:
            object_list[priority] = [self]
        else:
            object_list[priority].append(self)

    def tick(self):
        self.__object.tick()

    def kill(self):
        object_list[self.__object.priority()].remove(self)


def get_slope(point_1, point_2, y=False):
    try:
        slope = (point_2[1] - point_1[1]) / (point_2[0] - point_1[0])
    except:
        slope = (point_2[1] - point_1[1]) * float("inf")

    if y:
        try:
            slope = 1 / slope
        except:
            slope *= float("inf")

    return slope


def get_intersect(point, scalar, slope, y=False):
    if slope != 0:
        return (
            point[1] + (scalar - point[0]) / slope
            if y
            else point[0] + (scalar - point[1]) / slope
        )

    else:
        return point[1] if y else point[0]


def get_dist(point_1, point_2):
    return math.sqrt((point_2[0] - point_1[0]) ** 2 + (point_2[1] - point_1[1]) ** 2)


def PolyArea(x, y):
    return 0.5 * numpy.abs(
        numpy.dot(x, numpy.roll(y, 1)) - numpy.dot(y, numpy.roll(x, 1))
    )


def getcollisions(tiles, boxcollider):
    return (tile for tile in tiles if tile.colliderect(boxcollider))


def getcollisionspoint(tiles, point):
    return (tile for tile in tiles if tile.collidepoint(point))

def getcollisionspoint_condition(tiles, point, condition):
    cond = []
    for x in condition:
        cond.append(x[0])
    return (tile for tile in tiles if tile.collidepoint(point) and tile not in cond)


def load_level(map, mouse_conversion, player_inventory, app, screen, death = False):
    func.load_screen(app, screen, f"Loading {map.name}")
    app.pygame.mixer.music.fadeout(750)

    fade_tick.value = 15
    map_desc_tick.value = 0

    los_bg = pygame.Surface(map.get_size())
    los_bg.fill((0, 0, 0))

    los_bg2 = greyscale(map.background)
    los_bg2.set_alpha(85)
    los_bg.blit(los_bg2, (0, 0))

    burn_list.clear()
    turret_list.clear()
    enemy_list.clear()
    barricade_list.clear()
    app.zombiegroup.empty()

    app.kills = 0

    app.update_fps()

    block_movement_polygons = map.get_polygons()

    map_render = map.render(mouse_conversion).convert()





    # NAV_MESH = map2.compile_navmesh(mouse_conversion)
    # map_render2 = map2.render(mouse_conversion).convert()

    walls_filtered = []

    map_boundaries = [0, 0]

    map_conversion = 1920 / 854


    map.genQuadrants()

    print(map.quadrants)


    walls_filtered += map.generate_wall_structure2()

    map.generate_numpy_wall_points()

    for i in range(2):
        end_point = (
            map.__dict__["pos"][i] * map_conversion + map.__dict__["size"][i]
        ) / map_conversion
        if map_boundaries[i] < end_point:
            map_boundaries[i] = end_point
    print(map_boundaries)

    wall_points = []
    for x in walls_filtered:
        wall_points.append(x.get_points())

    player_pos = map.spawn_point.copy()
    camera_pos = [0, 0]

    map.compile_navmesh(multiplier)

    NAV_MESH = map.read_navmesh(walls_filtered)

    if map.name == "Downtown":
        map.enemy_type = "soldier"
    else:
        map.enemy_type = "zombie"



    print(mouse_conversion)
    if map.name == "Overworld":
        print("Loading overworld. Appending trashfires.")
        if not death and not app.dontIncreaseDay:
            app.day += 1
            
        app.dontIncreaseDay = False
        print([2362 * multiplier, 982 / multiplier])
        burn_list.append(
            classes.Burn(
                map,
                [2362 / multiplier, 982 / multiplier],
                2,
                500,
                infinite=True,
                magnitude2=0.7,
            )
        )
        burn_list.append(
            classes.Burn(
                map,
                [2315 / multiplier, 967 / multiplier],
                2,
                500,
                infinite=True,
                magnitude2=0.7,
            )
        )
        burn_list.append(
            classes.Burn(
                map,
                [2335 / multiplier, 1000 / multiplier],
                2,
                500,
                infinite=True,
                magnitude2=0.7,
            )
        )

        burn_list.append(
            
            classes.Burn(map, [352 / multiplier, 2257 / multiplier], 2, 500, infinite=True, magnitude2=0.7)
        )

    map.initBlood()

    interactables.clear()

    # [100,100],0, player_inventory, , "placeholder_npc.png", "placeholder_npc_potrait.png")

    # player_inventory.set_inventory({1 : {"item" : items["Molotov"], "amount" : 3 }, 2 : {"item" : items["5.56x45MM NATO"], "amount" : 999}})

    # player_inventory.set_inventory({8 : {"item" : items["Heroin"], "amount" : 1},9 : {"item" : items["Heroin"], "amount" : 1}, 1: {"item": items["45 ACP"], "amount": 999}, 2: {"item": items["50 CAL"], "amount": 999}, 3: {"item": items["7.62x39MM"], "amount": 999}, 4: {"item": items["12 GAUGE"], "amount": 999}, 5: {"item": items["9MM"], "amount": 999} ,6 : {"item": items["HE Grenade"], "amount": 999}, 7 : {"item": items["Sentry Turret"], "amount": 3}})
    # player_inventory.set_inventory({1: {"item": items["45 ACP"], "amount": 10}, 2 : {"item": items["Sentry Turret"], "amount": 1}, 3 : {"item": items["Barricade"], "amount": 3}})
    for x in map.objects:

        if x.endlessOnly and not app.endless:
            continue

        x.inv_save = player_inventory
        if map.name == "Overworld" and not death:
            x.re_init()
            if x.name == "Payphone":
                x.dialogue_bias = app.day
                print("set payphone dialogue to ", app.day)
        elif map.name != "Overworld":
            x.re_init()

        if map.name == "Downtown":
            print("LOADING DOWN TOWN OBJECT")
            print(app.endless)

        if map.name == "Downtown" and x.type == "door":
            if app.endless:
                x.active = False
            else:
                x.active = True
        


        interactables.append(x)

        if map.name == "Overworld" and x.name == "Basement" and not death:
            if not app.levels:
                return False
            x.door_dest = app.levels[0]
            app.levels.remove(app.levels[0])
            print("Set door destination to:", x.door_dest)

        
    

    for x in turret_bro:

        x.map = map
        x._pos = player_pos.copy()
        x.navmesh_ref = NAV_MESH.copy()
        x.wall_ref = walls_filtered

    app.MovTurretData = [map, NAV_MESH.copy(), walls_filtered]

    #pygame.display.set_gamma(map.GAMMA[0], map.GAMMA[1], map.GAMMA[2])


    init_jit()

    return (
        map,
        map_render,
        los_bg,
        map_boundaries,
        NAV_MESH,
        player_pos,
        camera_pos,
        wall_points,
        walls_filtered,
    )


class Map:
    def __init__(
        self,
        app,
        name,
        dir,
        nav_mesh_name,
        pos,
        conv,
        map_size,
        POLYGONS=[],
        OBJECTS=[],
        SPAWNPOINT=[100, 100],
        GAMMA=[1, 1, 1],
        DESC="",
        TOP_LAYER=None,
        NO_LOS_POLYGONS=[],
        mult2 = multiplier2,
        mult = multiplier,
        CUSTOM = False,
    ):
        self.app = app
        self.CUSTOM = CUSTOM
        self.name = name
        self.size = [map_size[0] * mult2, map_size[1] * mult2]
        self.polygons = []
        self.DESC = DESC

        self.GAMMA = GAMMA
        self.total = 0
        self.total_error = 0
        self.spawn_point = [SPAWNPOINT[0] * mult2, SPAWNPOINT[1] * mult2]

        self.nav_mesh_available_spots = []

        self.conv = mult

        

        self.size_converted = func.mult(self.size, 1 / self.conv)

        # self.conv = conv
        self.points_inside_polygons = []
        self.pos = [pos[0] / self.conv, pos[1] / self.conv]

        self.nav_mesh_name = nav_mesh_name


        if self.CUSTOM:
            self.compiled_file = get_preferences.get_path(f"ovrdoze_data/{self.name}_compiled.cnv")

        else:

            if self.nav_mesh_name:
                name2 = self.nav_mesh_name.removesuffix(".txt")
                self.compiled_file = get_preferences.get_path(f"ovrdoze_data/{name2}_compiled.cnv")

        self.barricade_rects = []

        # polygons.append([-100,0,100,size[1]])
        # polygons.append([size[0],0,100,size[1]])
        # polygons.append([0,-100,size[0],100])
        # polygons.append([0,size[1],size[0],100])
        for polygon in POLYGONS:
            x, y, width, height = polygon

            x += pos[0]
            y += pos[1]

            self.polygons.append(
                [
                    [(x) / self.conv, (y + height) / self.conv],
                    [(x) / self.conv, (y) / self.conv],
                    [(x + width) / self.conv, (y) / self.conv],
                    [(x + width) / self.conv, (y + height) / self.conv],
                ]
            )
        self.objects = OBJECTS
        self.polygons_no_los_block = []
        for polygon in NO_LOS_POLYGONS:
            x, y, width, height = polygon
            x += pos[0]
            y += pos[1]
            self.polygons_no_los_block.append(
                [
                    [(x) / self.conv, (y + height) / self.conv],
                    [(x) / self.conv, (y) / self.conv],
                    [(x + width) / self.conv, (y) / self.conv],
                    [(x + width) / self.conv, (y + height) / self.conv],
                ]
            )
        if dir:

            if CUSTOM:
                self.background = pygame.transform.scale(
                    dir,
                    [round(map_size[0] / self.conv), round(map_size[1] / self.conv)],
                ).convert()
            else:


                self.background = pygame.transform.scale(
                    pygame.image.load(fp("texture/maps/" + dir)),
                    [round(map_size[0] / self.conv), round(map_size[1] / self.conv)],
                ).convert()

        if TOP_LAYER == None:
            self.top_layer = None
        else:
            self.top_layer = pygame.transform.scale(
                pygame.image.load(fp("texture/maps/" + TOP_LAYER)),
                [round(map_size[0] / self.conv), round(map_size[1] / self.conv)],
            ).convert_alpha()

    def get_polygons(self):
        return self.polygons
    
    def initBlood(self):
        self.bloodPoints = np.zeros([round(self.size[0] / BLOODSINK_TILESIZE), round(self.size[1] / BLOODSINK_TILESIZE)], dtype=np.float16)
        print("BLOOD")
        print(self.bloodPoints)

    def get_size(self):
        return self.size

    def append_polygon(self, polygon):
        x, y, width, height = polygon
        self.polygons.append(
            [
                [(x) / self.conv, (y + height) / self.conv],
                [(x) / self.conv, (y) / self.conv],
                [(x + width) / self.conv, (y) / self.conv],
                [(x + width) / self.conv, (y + height) / self.conv],
            ]
        )

    def genQuadrants(self):
        self.quadrants = []
        for x in range(self.app.divisions):
            self.quadrants.append([])
            for y in range(self.app.divisions):
                self.quadrants[x].append(Quadrant(self.app, self, x, y))

    def setToQuadrant(self, obj, pos):

        qX, qY =  [
                    math.floor(self.app.divisions * (pos[0] / self.size_converted[0])),
                    math.floor(self.app.divisions * (pos[1] / self.size_converted[1])),
                ]
        
        qX = max([0,qX])
        qX = min([self.app.divisions - 1, qX])

        qY = max([0,qY])
        qY = min([self.app.divisions - 1, qY])
        
        quadrant = self.quadrants[qX][qY]

        if obj.quadrantType == 0:
            quadrant.bullets.append(obj)

        elif obj.quadrantType == 1:
            quadrant.enemies.append(obj)

        elif obj.quadrantType == 2:
            quadrant.fires.append(obj)

        obj.quadrant = quadrant

    def getQuadrantObjects(self, quadrant, type):
        x = quadrant.x - 1
        y = quadrant.y - 1

        objects = []

        for xI in range(3):

            if x + xI >= self.app.divisions:
                break

            for yI in range(3):
                if y + yI >= self.app.divisions:
                    break

                if type == 0:
                    objects += self.quadrants[x + xI][y + yI].bullets

                if type == 1:
                    objects += self.quadrants[x + xI][y + yI].enemies

                if type == 2:
                    objects += self.quadrants[x + xI][y + yI].fires

        return objects

    def generate_navmesh(self, NAV_MESH, level, loading_screen = True):
        i = 0
        for ref_point in NAV_MESH:

            i += 1

            for point_dict in NAV_MESH:
                point = point_dict["point"]
                if point == ref_point["point"]:
                    continue
                if point in ref_point["connected"]:
                    continue

                good_point = True
                tolerance = 10
                if tolerance:
                    for x, y in ([tolerance,tolerance], [-tolerance,tolerance], [-tolerance,-tolerance], [tolerance, -tolerance]):
                        for x2, y2 in ([tolerance,tolerance], [-tolerance,tolerance], [-tolerance,-tolerance], [tolerance, -tolerance]):
                            if not los.check_los_jit(np.array([point[0]+x, point[1]+y]), np.array([ref_point["point"][0]+x2, ref_point["point"][1]+y2]), self.numpy_array_wall_los, self.numpy_array_wall_no_los):
                                good_point = False
                                break
                    if not good_point:
                        continue



                if los.check_los_jit(np.array(point), np.array(ref_point["point"]), level.numpy_array_wall_los, level.numpy_array_wall_no_los):

                    good_point = True
                    for point2 in ref_point["connected"]:

                        angle_to_point = func.get_angle(ref_point["point"], point2)
                        angle_to_point2 = func.get_angle(ref_point["point"], point)

                        if abs(los.get_angle_diff(angle_to_point2, angle_to_point)) < 30:
                            good_point = False

                            ref_point["connected"].remove(point2)

                            if func.get_dist_points(ref_point["point"], point2) < func.get_dist_points(ref_point["point"], point):
                                ref_point["connected"].append(point2)
                            else:
                                ref_point["connected"].append(point)

                    if good_point:
                        ref_point["connected"].append(point)
                        #point_dict["connected"].append(ref_point["point"])

        return NAV_MESH

    def read_navmesh(self, walls_filtered):
        NAV_MESH = []

        if self.CUSTOM:
            try:
                NAV_MESH = self.nav_mesh_name

                NAV_MESH = self.generate_navmesh(NAV_MESH, self)
                return NAV_MESH
            except Exception as e:
                print(e)
                traceback.print_exc()
                return []

        if os.path.isfile(self.compiled_file):
            with open(self.compiled_file) as file:
                raw = file.read()

            NAV_MESH = ast.literal_eval(raw)
            return NAV_MESH


        try:
            file = open(fp(f"texture/maps/{self.nav_mesh_name}"), "r")
            lines = file.readlines()
            file.close()
            for line in lines:
                ref_point = {"point": ast.literal_eval(line), "connected": []}
                ref_point["point"][0] *= multiplier2
                ref_point["point"][1] *= multiplier2
                NAV_MESH.append(ref_point)

            NAV_MESH = self.generate_navmesh(NAV_MESH, self)

        except Exception as e:
            print(e)
            traceback.print_exc()

        with open(self.compiled_file, "w") as file:
            file.write(str(NAV_MESH))


        return NAV_MESH

    def checkcollision(
        self,
        pos,
        movement,
        collider_size,
        map_size,
        damage_barricades=False,
        damager=None,
        ignore_barricades=False,
        collider_rect=False,
        check_only_collision=False,
        bullet = False
    ):
        if collider_rect:
            collider = pos
        else:
            collider = pygame.Rect(
                round(pos[0] - collider_size),
                round(pos[1] - collider_size),
                round(collider_size * 2),
                round(collider_size * 2),
            )
        map_rect = pygame.Rect(0, 0, map_size[0], map_size[1])

        collisiontypes = {"left": False, "right": False, "top": False, "bottom": False}

        if collider.centerx < collider_size:
            collider.left = 0

            collisiontypes["left"] = True

        if collider.centerx > map_size[0] - collider_size:
            collider.right = map_size[0]

            collisiontypes["right"] = True

        if collider.centery < collider_size:
            collider.top = 0

            collisiontypes["top"] = True

        if collider.centery > map_size[1] - collider_size:
            collider.bottom = map_size[1]

            collisiontypes["bottom"] = True

        # if not map_rect.collidepoint(collider.midleft) and map_rect.collidepoint(collider.midright):
        #
        #     collider.left = map_rect.left
        #
        #     collisiontypes["right"] = True
        #
        # if not map_rect.collidepoint(collider.midright) and map_rect.collidepoint(collider.midleft):
        #
        #     collider.right = map_rect.right
        #
        #     collisiontypes["left"] = True
        #
        #
        # if not map_rect.collidepoint(collider.midbottom):
        #
        #     collider.bottom = map_rect.bottom
        #
        #     collisiontypes["bottom"] = True
        #
        # if not map_rect.collidepoint(collider.midtop):
        #
        #     collider.top = map_rect.top
        #
        #     collisiontypes["top"] = True

        if abs(movement[0]) >= abs(movement[1]):
            check_order = ["x", "y"]
        else:
            check_order = ["y", "x"]

        for check in check_order:

            collisions = list(getcollisions(self.rectangles if not bullet else self.block_vis_rects, collider))

            if check == check_order[0] and damage_barricades:
                for barr in self.barricade_rects:
                    if barr[0] in getcollisions(self.rectangles, collider):
                        barr[1].__dict__["hp"] -= damager.__dict__["damage"]
                        damager.__dict__["attack_tick"] = 30

            for tile in collisions:
                if check == "x":
                    if ignore_barricades:
                        ignore = any(barr[0] == tile for barr in self.barricade_rects)
                        if ignore:
                            continue

                    if tile.collidepoint(collider.midright) and not tile.collidepoint(
                        collider.midleft
                    ):

                        collider.right = tile.left

                        collisiontypes["right"] = True

                    if tile.collidepoint(collider.midleft) and not tile.collidepoint(
                        collider.midright
                    ):

                        collider.left = tile.right

                        collisiontypes["left"] = True

                elif check == "y":
                    if ignore_barricades:
                        ignore = any(barr[0] == tile for barr in self.barricade_rects)
                        if ignore:
                            continue

                    if tile.collidepoint(collider.midbottom) and not tile.collidepoint(
                        collider.midtop
                    ):

                        collider.bottom = tile.top

                        collisiontypes["bottom"] = True

                    if tile.collidepoint(collider.midtop) and not tile.collidepoint(
                        collider.midbottom
                    ):

                        collider.top = tile.bottom

                        collisiontypes["top"] = True

        if collisiontypes != {
            "left": False,
            "right": False,
            "top": False,
            "bottom": False,
        }:

            pos = list(collider.center)

        if check_only_collision:

            if collisiontypes != {
                "left": False,
                "right": False,
                "top": False,
                "bottom": False,
            }:
                return True
            else:
                return False

        return collisiontypes, pos

    def generate_numpy_wall_points(self):
        y = np.zeros([0,0], dtype=int)
        self.numpy_array_wall_los = np.full_like(y, 0, shape = (len(self.walls_los_block), 4))
        for i, wall in enumerate(self.walls_los_block):
            x,y = wall.get_points()
            self.numpy_array_wall_los[i][0] = x[0]
            self.numpy_array_wall_los[i][1] = x[1]
            self.numpy_array_wall_los[i][2] = y[0]
            self.numpy_array_wall_los[i][3] = y[1]

        print(self.numpy_array_wall_los)


        y = np.zeros([0,0], dtype=int)
        self.numpy_array_wall_no_los = np.full_like(y, 0, shape = (len(self.no_los_walls), 4))
        for i, wall in enumerate(self.no_los_walls):
            x,y = wall.get_points()
            self.numpy_array_wall_no_los[i][0] = x[0]
            self.numpy_array_wall_no_los[i][1] = x[1]
            self.numpy_array_wall_no_los[i][2] = y[0]
            self.numpy_array_wall_no_los[i][3] = y[1]

        print(self.numpy_array_wall_no_los)

    def generate_wall_structure2(self):
        print("CHECKING POINTS INSIDE WALLS")
        polygons_temp = []
        polygons_temp.append([pygame.Rect(0, 0, self.size[0], 10), []])
        polygons_temp.append([pygame.Rect(0, 0, 10, self.size[1]), []])
        polygons_temp.append(
            [
                pygame.Rect(
                    (self.size[0] - 10) / self.conv, 0, 15, self.size[1] / self.conv
                ),
                [],
            ]
        )
        polygons_temp.append(
            [
                pygame.Rect(
                    0, (self.size[1] - 10) / self.conv, self.size[0] / self.conv, 14
                ),
                [],
            ]
        )
        self.rectangles = []
        self.block_vis_rects = []
        for polygon in self.polygons:
            a, b, c, d = polygon
            x = [a[0], b[0], c[0], d[0]]
            y = [a[1], b[1], c[1], d[1]]
            poly = pygame.Rect(min(x), min(y), max(x) - min(x), max(y) - min(y))

            self.rectangles.append(poly)
            self.block_vis_rects.append(poly)

            polygons_temp.append([poly, [a, b, c, d]])

        for polygon in self.polygons_no_los_block:
            a, b, c, d = polygon
            x = [a[0], b[0], c[0], d[0]]
            y = [a[1], b[1], c[1], d[1]]
            poly = pygame.Rect(min(x), min(y), max(x) - min(x), max(y) - min(y))

            self.rectangles.append(poly)

            # polygons_temp.append([poly,[a,b,c,d]])

        self.connected_polygons = {}
        for polygon in self.polygons:
            for point in polygon:
                for poly, points in polygons_temp:

                    if point in points:
                        continue

                    if poly.collidepoint(point):
                        self.points_inside_polygons.append(point)

                        break

        print("POINTS INSIDE:", len(self.points_inside_polygons))
        print("POINTS TOTAL:", points)
        self.no_los_walls = []
        for polygon in self.polygons_no_los_block:
            a, b, c, d = polygon
            # a = ratio(a,size_ratio)
            # b = ratio(b,size_ratio)
            # c = ratio(c,size_ratio)
            # d = ratio(d,size_ratio)
            self.no_los_walls.append(los.Wall(a, b, pol=polygon))
            self.no_los_walls.append(los.Wall(b, c, pol=polygon))
            self.no_los_walls.append(los.Wall(c, d, pol=polygon))
            self.no_los_walls.append(los.Wall(d, a, pol=polygon))


        print("GENERATING WALL STRUCTURE")
        walls = []
        for polygon in self.polygons:
            a, b, c, d = polygon
            # a = ratio(a,size_ratio)
            # b = ratio(b,size_ratio)
            # c = ratio(c,size_ratio)
            # d = ratio(d,size_ratio)
            walls.append(los.Wall(a, b, pol=polygon))
            walls.append(los.Wall(b, c, pol=polygon))
            walls.append(los.Wall(c, d, pol=polygon))
            walls.append(los.Wall(d, a, pol=polygon))

        del_walls = []

        for wall1 in walls:
            p1, p2 = wall1.get_points()
            for wall2 in walls:
                p3, p4 = wall2.get_points()
                if func.get_dist_points(p1, p3) < 3:
                    wall2.set_new_points(p1, p4)
                if func.get_dist_points(p2, p3) < 3:
                    wall2.set_new_points(p2, p4)

        wp = []
        for w in walls:
            p1, p2 = w.get_points()
            wp.append(p1)
            wp.append(p2)

        intersecting_walls = []

        for wall_1 in walls:
            wall_points = wall_1.get_points()
            wp1, wp2 = wall_points

            mode = "vert" if wp1[0] == wp2[0] else "hor"
            for wall_2 in walls:
                wall_points = wall_1.get_points()
                p1, p2 = wall_2.get_points()

                if mode == "vert":
                    if p1[0] != p2[0]:
                        continue
                else:
                    if p1[1] != p2[1]:
                        continue
                if p1 in wall_points or p2 in wall_points:
                    continue
                if los.intersect(
                    wall_points[0],
                    wall_points[1],
                    func.minus(p1, [-3, -3]),
                    func.minus(p2, [3, 3]),
                ):
                    intersecting_walls.append([wall_1, wall_2])
                    # for wall_1, wall_2 in intersecting_walls:
                    a, b = wall_1.get_points()
                    c, d = wall_2.get_points()

                    res_key = min([a, b], key=lambda x: sum(x))
                    res_key2 = min([c, d], key=lambda x: sum(x))
                    res_key_max = max([a, b], key=lambda x: sum(x))
                    res_key_max2 = max([c, d], key=lambda x: sum(x))
                    wall_1.set_new_points(res_key, res_key2)
                    wall_2.set_new_points(res_key_max, res_key_max2)

        for wall1 in walls:
            p1, p2 = wall1.get_points()
            for wall2 in walls:
                p3, p4 = wall2.get_points()
                if func.get_dist_points(p1, p3) < 3:
                    wall2.set_new_points(p1, p4)
                if func.get_dist_points(p2, p3) < 3:
                    wall2.set_new_points(p2, p4)

        for i in range(3):

            for wall1 in walls:
                p1, p2 = wall1.get_points()

                if func.get_dist_points(p1, p2) < 3:
                    del_walls.append(wall1)
                    continue

                for wall2 in walls:
                    p3, p4 = wall2.get_points()

                    if (
                        los.intersect(
                            func.minus(p1, [2, 2]),
                            func.minus(p2, [-2, -2]),
                            func.minus(p3, [2, 2]),
                            func.minus(p4, [-2, -2]),
                        )
                        and wall1.vertical == wall2.vertical
                    ):

                        i1, i2, i3, i4 = self.min_max([p1, p2, p3, p4])

                        wall1.set_new_points(i1, i2)

                        wall2.set_new_points(i3, i4)


        for x in del_walls:
            try:
                walls.remove(x)
            except:
                pass

        remove_list = []

        for wall_1 in walls:
            for wall_2 in walls:
                if wall_2 in remove_list:
                    continue
                wall_1_points = wall_1.get_points()
                interlink1 = None
                interlink2 = None

                for point in wall_1_points:
                    for point2 in wall_2.get_points():
                        if los.get_dist_points(point, point2) < 5:
                            interlink1 = point
                            interlink2 = point2

                if interlink1 != None and interlink2 != None:
                    wall_points = list(wall_1.get_points())
                    wall_points_2 = list(wall_2.get_points())

                    wall_points.remove(interlink1)
                    wall_points_2.remove(interlink2)

                    if los.intersect(
                        wall_points[0],
                        wall_points_2[0],
                        func.minus(interlink1, [-3, -3]),
                        func.minus(interlink1, [3, 3]),
                    ):
                        remove_list.append(wall_2)
                        wall_1.set_new_points(wall_points[0], wall_points_2[0])

        for wall_1 in remove_list:
            walls.remove(wall_1)

        print("WALLS:", len(walls))

        self.walls_los_block = walls

        return walls

    def min_max(self, list):
        sorted_list = sorted(list, key=sum)
        return sorted_list

    def generate_wall_structure(self):
        print("CHECKING POINTS INSIDE WALLS")
        polygons_temp = []
        polygons_temp.append([pygame.Rect(0, 0, self.size[0], 10), []])
        polygons_temp.append([pygame.Rect(0, 0, 10, self.size[1]), []])
        polygons_temp.append(
            [
                pygame.Rect(
                    (self.size[0] - 10) / self.conv, 0, 15, self.size[1] / self.conv
                ),
                [],
            ]
        )
        polygons_temp.append(
            [
                pygame.Rect(
                    0, (self.size[1] - 10) / self.conv, self.size[0] / self.conv, 14
                ),
                [],
            ]
        )
        self.rectangles = []
        for polygon in self.polygons:
            a, b, c, d = polygon
            x = [a[0], b[0], c[0], d[0]]
            y = [a[1], b[1], c[1], d[1]]
            poly = pygame.Rect(min(x), min(y), max(x) - min(x), max(y) - min(y))

            self.rectangles.append(poly)

            polygons_temp.append([poly, [a, b, c, d]])

        for polygon in self.polygons_no_los_block:
            a, b, c, d = polygon
            x = [a[0], b[0], c[0], d[0]]
            y = [a[1], b[1], c[1], d[1]]
            poly = pygame.Rect(min(x), min(y), max(x) - min(x), max(y) - min(y))

            self.rectangles.append(poly)

            # polygons_temp.append([poly,[a,b,c,d]])

        self.connected_polygons = {}
        for polygon in self.polygons:
            for point in polygon:
                for poly, points in polygons_temp:

                    if point in points:
                        continue

                    if poly.collidepoint(point):
                        self.points_inside_polygons.append(point)

                        break

        print("POINTS INSIDE:", len(self.points_inside_polygons))
        print("POINTS TOTAL:", points)

        print("GENERATING WALL STRUCTURE")
        walls = []
        for polygon in self.polygons:
            a, b, c, d = polygon
            # a = ratio(a,size_ratio)
            # b = ratio(b,size_ratio)
            # c = ratio(c,size_ratio)
            # d = ratio(d,size_ratio)
            walls.append(los.Wall(a, b))
            walls.append(los.Wall(b, c))
            walls.append(los.Wall(c, d))
            walls.append(los.Wall(d, a))

        intersecting_walls = []

        for wall_1 in walls:
            wall_points = wall_1.get_points()
            wp1, wp2 = wall_points

            mode = "vert" if wp1[0] == wp2[0] else "hor"
            for wall_2 in walls:
                wall_points = wall_1.get_points()
                p1, p2 = wall_2.get_points()

                if mode == "vert":
                    if p1[0] != p2[0]:
                        continue
                else:
                    if p1[1] != p2[1]:
                        continue
                if p1 in wall_points or p2 in wall_points:
                    continue
                if los.intersect(
                    wall_points[0],
                    wall_points[1],
                    func.minus(p1, [-3, -3]),
                    func.minus(p2, [3, 3]),
                ):
                    intersecting_walls.append([wall_1, wall_2])
                    # for wall_1, wall_2 in intersecting_walls:
                    a, b = wall_1.get_points()
                    c, d = wall_2.get_points()

                    res_key = min([a, b], key=lambda x: sum(x))
                    res_key2 = min([c, d], key=lambda x: sum(x))
                    res_key_max = max([a, b], key=lambda x: sum(x))
                    res_key_max2 = max([c, d], key=lambda x: sum(x))
                    wall_1.set_new_points(res_key, res_key2)
                    wall_2.set_new_points(res_key_max, res_key_max2)
        remove_list = []
        # for wall_1 in walls:
        #     a,b = wall_1.get_points()
        #     if los.get_dist_points(a, b) < 2:
        #         remove_list.append(wall_1)

        for wall_1 in walls:
            for wall_2 in walls:
                if wall_2 in remove_list:
                    continue
                wall_1_points = wall_1.get_points()
                interlink1 = None
                interlink2 = None

                for point in wall_1_points:
                    for point2 in wall_2.get_points():
                        if los.get_dist_points(point, point2) < 5:
                            interlink1 = point
                            interlink2 = point2

                if interlink1 != None and interlink2 != None:
                    wall_points = list(wall_1.get_points())
                    wall_points_2 = list(wall_2.get_points())

                    wall_points.remove(interlink1)
                    wall_points_2.remove(interlink2)

                    if los.intersect(
                        wall_points[0],
                        wall_points_2[0],
                        func.minus(interlink1, [-3, -3]),
                        func.minus(interlink1, [3, 3]),
                    ):
                        remove_list.append(wall_2)
                        wall_1.set_new_points(wall_points[0], wall_points_2[0])

        for wall_1 in remove_list:
            walls.remove(wall_1)

        return walls

    def check_collision2(
        self,
        player_pos,
        map_boundaries,
        return_only_collision=False,
        collision_box=0,
        screen=screen,
        x_vel=0,
        y_vel=0,
        dir_coll=False,
        phase=0,
    ):
        collision_box_size = collision_box

        collide = False
        collides = 0
        vert_coll, hor_coll = False, False
        closest_point = None
        x5, y5 = player_pos

        map_poly = pygame.Rect(
            collision_box_size,
            collision_box_size,
            map_boundaries[0] - collision_box_size,
            map_boundaries[1] - collision_box_size,
        )
        if not map_poly.collidepoint([x5, y5]):
            if collision_box > player_pos[0]:
                x5 = collision_box
                collide = True
                vert_coll = True

            if map_boundaries[0] - collision_box < player_pos[0]:
                x5 = map_boundaries[0] - collision_box
                vert_coll = True
                collide = True
            if collision_box > player_pos[1]:
                y5 = collision_box
                collide = True
                hor_coll = True
            if map_boundaries[1] - collision_box < player_pos[1]:
                y5 = map_boundaries[1] - collision_box
                collide = True
                hor_coll = True

        player_pos_der = [x5, y5]

        for polygon in self.polygons:
            a, b, c, d = polygon
            x = [a[0], b[0], c[0], d[0]]
            y = [a[1], b[1], c[1], d[1]]

            if (
                player_pos[0] < min(x) - 2 * collision_box_size
                or player_pos[0] > max(x) + 2 * collision_box_size
                or player_pos[1] < min(y) - 2 * collision_box_size
                or player_pos[1] > max(y) + 2 * collision_box_size
            ):
                continue

            poly = pygame.Rect(
                min(x) - collision_box_size,
                min(y) - collision_box_size,
                max(x) - min(x) + collision_box_size * 2,
                max(y) - min(y) + collision_box_size * 2,
            )

            if poly.collidepoint(player_pos_der):
                pass

    def check_collision(
        self,
        player_pos,
        map_boundaries,
        return_only_collision=False,
        collision_box=0,
        screen=screen,
        x_vel=0,
        y_vel=0,
        dir_coll=False,
        phase=0,
    ):

        collision_box_size = collision_box

        collide = False
        collides = 0
        vert_coll, hor_coll = False, False
        closest_point = None

        x5, y5 = player_pos

        if collision_box > player_pos[0]:
            x5 = collision_box
            collide = True
            vert_coll = True

        if map_boundaries[0] - collision_box < player_pos[0]:
            x5 = map_boundaries[0] - collision_box
            vert_coll = True
            collide = True
        if collision_box > player_pos[1]:
            y5 = collision_box
            collide = True
            hor_coll = True
        if map_boundaries[1] - collision_box < player_pos[1]:
            y5 = map_boundaries[1] - collision_box
            collide = True
            hor_coll = True

        # if collide and not dir_coll:
        #
        #     return [x5,y5]

        player_pos_der = [x5, y5]

        # pygame.draw.rect(screen,[255,0,0], [player_pos[0]-collision_box_size,player_pos[1]-collision_box_size,collision_box_size,collision_box_size])

        for polygon in self.polygons:
            a, b, c, d = polygon
            x = [a[0], b[0], c[0], d[0]]
            y = [a[1], b[1], c[1], d[1]]

            if (
                player_pos[0] < min(x) - 50
                or player_pos[0] > max(x) + 50
                or player_pos[1] < min(y) - 50
                or player_pos[1] > max(y) + 50
            ):
                continue
            poly = pygame.Rect(
                min(x) - collision_box_size,
                min(y) - collision_box_size,
                max(x) - min(x) + collision_box_size * 2,
                max(y) - min(y) + collision_box_size * 2,
            )

            minx, maxx, miny, maxy = (
                min(x) - collision_box_size,
                max(x) + collision_box_size,
                min(y) - collision_box_size,
                max(y) + collision_box_size,
            )

            # pygame.draw.rect(screen,[255,255,0], [min(x)- collision_box_size,min(y) - collision_box_size, max(x)-min(x) + collision_box_size*2, max(y) - min(y) + collision_box_size*2])

            if poly.collidepoint(player_pos_der):

                collides += 1

                collide = True

                closest = 1000
                for line in range(4):
                    x1, y1 = [a, b, c, d][line]

                    x2, y2 = [a, b, c, d, a][line + 1]

                    if [x1, y1] in self.points_inside_polygons and [
                        x2,
                        y2,
                    ] in self.points_inside_polygons:
                        continue

                    x3, y3 = player_pos_der

                    dx = x2 - x1
                    dy = y2 - y1

                    alpha = (dy * y3 - dy * y1 + dx * x3 - dx * x1) / (
                        dy**2 + dx**2
                    )
                    # beta = (dy * x3 - dy * x1 - dx * y3 + dx * y1) / (dy ** 2 + dx ** 2)

                    x4 = x1 + alpha * dx
                    y4 = y1 + alpha * dy

                    dist_to_player = get_dist(player_pos, [x4, y4])
                    if dist_to_player < closest:
                        closest = dist_to_player
                        closest_line = [[x1, y1], [x2, y2]]

                if (
                    minx < player_pos_der[0] < maxx
                    and closest_line[0][0] == closest_line[1][0]
                ):
                    player_pos_der[0] = func.get_closest_value(
                        player_pos_der[0], [minx, maxx]
                    )
                    vert_coll = True

                if (
                    miny < player_pos_der[1] < maxy
                    and closest_line[0][1] == closest_line[1][1]
                ):
                    player_pos_der[1] = func.get_closest_value(
                        player_pos_der[1], [miny, maxy]
                    )
                    hor_coll = True

        if dir_coll:

            if player_pos_der != player_pos:

                return player_pos_der, vert_coll, hor_coll
            else:
                return False, vert_coll, hor_coll

        if not return_only_collision:
            return player_pos_der
        else:
            if collide:

                return player_pos_der
            return False

            #
            #
            #
            # x4,y4 = closest_point
            #
            # angle = math.atan2(y4 - player_pos_der[1], x4 - player_pos_der[0]) + math.pi
            # x4 += math.cos(angle) * (collision_box_size+1)
            # y4 += math.sin(angle) * (collision_box_size+1)
            #
            # if x5 == 0 and y5 == 0:
            #     x5,y5 = x4,y4
            # else:
            #     x5 = (x4+x5)/2
            #     y5 = (y4+y5)/2
            #
            # print("MOVING X BY: ", x5-player_pos_der[0],"MOVING Y BY: ", y5-player_pos_der[1])
            #
            # player_pos_der = [x5,y5]

        return player_pos_der

    def compile_navmesh(self, conv):
        print("Navmesh conv:", conv)

        x_scale = (self.size[0]/conv)/20
        y_scale =(self.size[1]/conv)/20

        rect = pygame.Rect(0,0,self.size[0]/conv,self.size[1]/conv)


        for x1 in range(20):

            for y1 in range(20):

                point = [x1 * x_scale, y1 * y_scale]
                point[0] += 15
                point[1] += 15

                if not rect.collidepoint(point):
                    continue

                collision = False

                for polygon in self.polygons:
                    a, b, c, d = polygon
                    x = [a[0], b[0], c[0], d[0]]
                    y = [a[1], b[1], c[1], d[1]]

                    poly = pygame.Rect(min(x), min(y), max(x) - min(x), max(y) - min(y))

                    if poly.collidepoint(point):
                        collision = True
                        break
                if not collision:
                    self.nav_mesh_available_spots.append(point)

    def getPointBasedOnBlood(self, p_pos, max_tries = 13):
        averageBlood = np.average(self.bloodPoints)
        threshold = averageBlood - 0.025
        tries = 0
        nonVisiblePoints = []
        nonVisibleBloodPoints = []
        allPoints = []
        while tries < max_tries:
            point = func.pick_random_from_list(self.nav_mesh_available_spots)
            visible = los.check_los_jit(np.array(p_pos), np.array(point), self.numpy_array_wall_los)
            blood = self.bloodPoints[round(point[0] / BLOODSINK_TILESIZE), round(point[1] / BLOODSINK_TILESIZE)] > threshold

            if not visible:
                nonVisiblePoints.append(point)

                if blood:
                    nonVisibleBloodPoints.append(point)

            allPoints.append(point)

            tries += 1

        if nonVisibleBloodPoints:
            point = self.getFurthest(p_pos, nonVisibleBloodPoints)
        elif nonVisiblePoints:
            point = self.getFurthest(p_pos, nonVisiblePoints)
        else:
            point = self.getFurthest(p_pos, allPoints)
        return point

    def getFurthest(self, pos, l):
        furthest = 0
        furthest_p = None
        for x in l:
            d = los.get_dist_points(pos, x)
            if d > furthest:
                furthest_p = x
                furthest = d

        return furthest_p



    def get_random_point(
        self, p_pos=None, enemies=None, visible_from_origin_point=None, visibility=True, max_tries=100, furthest_point_from_point = False, max_dist = 0, max_dist_point = None,
    ):
        tries = 0
        walls = self.numpy_array_wall_los
        furthest_p = func.pick_random_from_list(self.nav_mesh_available_spots)
        furthest = 0
        while tries < max_tries:
            tries += 1
            point = func.pick_random_from_list(self.nav_mesh_available_spots)
            conds = [True, True, True, True]
            if p_pos != None:
                if los.check_los_jit(np.array(p_pos), np.array(point), walls):
                    conds[0] = False
            if enemies != None:
                for x in enemies:
                    if los.check_los_jit(np.array(point), np.array(x.get_pos()), walls):
                        conds[1] = False
                        break
            if visible_from_origin_point:
                if not los.check_los_jit(np.array(point), np.array(visible_from_origin_point), walls):
                    conds[2] = False

            if max_dist:
                if los.get_dist_points(point, max_dist_point) > max_dist:
                    conds[3] = False

            if furthest_point_from_point:
                if False not in conds:
                    dist = los.get_dist_points(point, furthest_point_from_point)
                    if dist > furthest:
                        furthest = dist
                        furthest_p = point
                if tries > max_tries:
                    return furthest_p


            elif False not in conds or tries > max_tries:
                return point
        return point

    def render(self, conv):

        self.map_rendered = pygame.Surface(
            self.background.get_size()
        )
        print("RENDER MAP SIZE", self.map_rendered.get_size())
        self.map_rendered.fill([255, 255, 255])

        self.textures = {
            "floor_tile_1": pygame.image.load(fp("texture/floor.png")).convert_alpha()
        }

        self.map_rendered.blit(self.background, (0, 0))

        # for object in self.objects:   ### ((0,0),"floor_tile_1",180)
        #     object_texture = self.textures[object[1]]
        #     if object[2] != 0:
        #         rotated_image, new_rect = rot_center(object_texture,object[2],object[0][0],object[0][1])
        #         object_pos = [object[0][0] - new_rect[0], object[0][1] - new_rect[1]]
        #     else:
        #         object_pos = object[0]
        #         rotated_image = object_texture
        #     self.map_rendered.blit(rotated_image, object_pos)

        for polygon in self.polygons:
            print(polygon)
            # pygame.draw.polygon(self.map_rendered, [0,0,0], polygon)

        # for point in self.nav_mesh_available_spots:
        #     pygame.draw.rect(self.map_rendered, [255,0,0], [point[0], point[1], 1,1])

        self.map_rendered_alpha = self.map_rendered.copy()
        self.map_rendered_alpha.set_alpha(3)

        self.map_rendered_alpha_PW = self.map_rendered.copy()
        self.map_rendered_alpha_PW.set_alpha(30)

        return self.map_rendered


def rot_center(image, angle, x, y):

    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(center=(x, y)).center)

    return rotated_image, new_rect



def init_jit():
        player_pos = [209, 209]
        camera_pos = [100, 700]
        size = np.array([854, 480])
        walls =  np.array([
             [ 356,   67,  356,    0],
             [ 356,    0,  445 ,   0],
             [ 445,   67,  356  , 67],
             [ 445,    0,  445   ,67],
             [ 799,   66,  799,    0],
             [ 799,    0,  889 ,   0],
             [ 889,    0,  889  , 66],
             [ 889,   66,  799   ,66],
             [ 800,  200,  800,  532],
             [ 800,  200,  889 , 200],
             [ 889,  200,  889  ,266],
             [ 889,  266, 1066,  266],
             [1066,  266, 1066 , 334],
             [1245,  328, 1245  ,266],
             [1245,  266, 1422,  266],
             [1422,  266, 1422,  328],
             [1422,  328, 1245,  328],
             [ 355,  333,  355,  267],
             [ 355,  267,  443,  267],
             [ 443,  267,  443,  666],
             [ 266,  333,  355,  333],
             [ 266,  466,  266,  333],
             [ 266,  466,  355,  466],
             [   0,  466,    0,  334],
             [   0,  334,   88,  334],
             [  88,  334,   88,  466],
             [  88,  466,    0,  466],
             [ 889,  334, 1066,  334],
             [ 889,  334,  889,  532],
             [ 889,  532,  800,  532],
             [ 355,  666,  355,  466],
             [ 443,  666,  355,  666],
             [ 800,  868,  800,  734],
             [ 800,  734,  888,  734],
             [ 888,  734,  888,  868],
             [ 976,  868,  888,  868],
             [ 357,  868,  357,  801],
             [ 357,  801,  444,  801],
             [ 444,  801,  444,  868],
             [ 800,  868,  444,  868],
             [ 179,  934,  179,  868],
             [ 179,  868,  357,  868],
             [ 976,  868,  976,  934],
             [ 976,  934,  179,  934],
             [1156,  934, 1156,  868],
             [1156,  868, 1422,  868],
             [1422,  868, 1422,  934],
             [1422,  934, 1156,  934]])
        l = pygame.Surface((854, 480))

        l, t, t = render_los_image_jit.draw(l, 1, camera_pos, player_pos, None, walls, size)

        check_los_jit(np.array([10,10]), np.array([100,10]), walls)
        line_intersection(np.array([10,10]), np.array([20,10]), np.array([10,20]), np.array([20,20]))
        intersect_jit(np.array([10,10]), np.array([20,10]), np.array([10,20]), np.array([20,20]))


map = (
    # # Border
    # {"a":{"x":0,"y":0}, "b":{"x":size[0],"y":0}},
    # {"a":{"x":size[0],"y":0}, "b":{"x":size[0],"y":size[1]}},
    # {"a":{"x":size[0],"y":size[1]}, "b":{"x":0,"y":size[1]}},
    # {"a":{"x":0,"y":size[1]}, "b":{"x":0,"y":0}},
    # Polygon #1
    {"a": {"x": 100, "y": 100}, "b": {"x": 300, "y": 100}},
    {"a": {"x": 300, "y": 100}, "b": {"x": 300, "y": 300}},
    {"a": {"x": 300, "y": 300}, "b": {"x": 100, "y": 300}},
    {"a": {"x": 100, "y": 300}, "b": {"x": 100, "y": 100}},
    # Polygon #1
    {"a": {"x": 700, "y": 100}, "b": {"x": 800, "y": 100}},
    {"a": {"x": 800, "y": 100}, "b": {"x": 800, "y": 300}},
    {"a": {"x": 800, "y": 300}, "b": {"x": 700, "y": 300}},
    {"a": {"x": 700, "y": 300}, "b": {"x": 700, "y": 100}},
)
