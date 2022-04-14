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


from values import *


def render_center(image,pos):
    im = zoom_transform(image,zoom)
    r_pos = minus([-im.get_rect().center[0],-im.get_rect().center[1]],pos)
    screen.blit(im,r_pos)

pygame.init()
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


object_list = {}
class Object:
    def __init__(self,sub_object):
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
            slope = 1/slope
        except:
            slope *= float("inf")


    return slope

def get_intersect(point,scalar,slope, y=False):
    if slope != 0:
        if y:
            A_ypos = point[1] + (scalar - point[0])/slope
        else:
            A_ypos = point[0] + (scalar - point[1])/slope
    else:
        if y:
            A_ypos = point[1]
        else:
            A_ypos = point[0]
    return A_ypos

def get_dist(point_1,point_2):
    return math.sqrt((point_2[0] - point_1[0])**2 + (point_2[1] - point_1[1])**2)

class anus:
    def priority(self):
        return "1"

    def tick(self):
        print("anus")

class pissa:
    def priority(self):
        return "2"

    def tick(self):
        print("pissa")

def PolyArea(x,y):
    return 0.5*numpy.abs(numpy.dot(x,numpy.roll(y,1))-numpy.dot(y,numpy.roll(x,1)))


class Map:
    def __init__(self,name, conv,size,polygons,objects):
        self.name = name
        self.size = size
        self.polygons = []
        self.nav_mesh_available_spots = []
        self.conv = conv
        self.points_inside_polygons = []

        # polygons.append([-100,0,100,size[1]])
        # polygons.append([size[0],0,100,size[1]])
        # polygons.append([0,-100,size[0],100])
        # polygons.append([0,size[1],size[0],100])


        for polygon in polygons:
            x,y,width,height = polygon
            self.polygons.append([[(x)/ conv, (y+height) / conv],[(x) / conv,(y) / conv],[(x+width) / conv,(y) / conv],[(x+width) / conv,(y+height) / conv]])
        self.objects = objects

        self.background = pygame.transform.scale(pygame.image.load("texture/map.png"), [round(size[0] / conv), round(size[1] / conv)]).convert()

    def get_polygons(self):
        return self.polygons

    def append_polygon(self, polygon):
        x,y,width,height = polygon
        self.polygons.append([[(x)/ self.conv, (y+height) / self.conv],[(x) / self.conv,(y) / self.conv],[(x+width) / self.conv,(y) / self.conv],[(x+width) / self.conv,(y+height) / self.conv]])

    def generate_wall_structure(self):
        print("CHECKING POINTS INSIDE WALLS")
        polygons_temp = []
        polygons_temp.append([pygame.Rect(0,0, 2000, 10), []])
        polygons_temp.append([pygame.Rect(0,0, 10, 2000), []])
        polygons_temp.append([pygame.Rect(1990/ self.conv ,0, 15, 2000/ self.conv ), []])
        polygons_temp.append([pygame.Rect(0,1490/ self.conv , 2000/ self.conv , 14), []])
        for polygon in self.polygons:
            a,b,c,d = polygon
            x = [a[0],b[0],c[0],d[0]]
            y = [a[1],b[1],c[1],d[1]]
            poly = pygame.Rect(min(x)- 10,min(y) - 10, max(x)-min(x) + 10*2, max(y) - min(y) + 10*2)

            polygons_temp.append([poly,[a,b,c,d]])


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
            a,b,c,d = polygon
            # a = ratio(a,size_ratio)
            # b = ratio(b,size_ratio)
            # c = ratio(c,size_ratio)
            # d = ratio(d,size_ratio)
            walls.append(los.Wall(a,b))
            walls.append(los.Wall(b,c))
            walls.append(los.Wall(c,d))
            walls.append(los.Wall(d,a))

        intersecting_walls = []

        for wall_1 in walls:
            wall_points = wall_1.get_points()
            wp1, wp2 = wall_points

            if wp1[0] == wp2[0]:
                mode = "vert"
            else:
                mode = "hor"



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
                if los.intersect(wall_points[0], wall_points[1], func.minus(p1,[-1,-1]), func.minus(p2,[1,1])):
                    print("INTERSECTING LINE")
                    print(wall_points, [p1,p2])
                    intersecting_walls.append([wall_1, wall_2])

        # for wall_1, wall_2 in intersecting_walls:
                    a,b = wall_1.get_points()
                    c,d = wall_2.get_points()
                    print(a,b,c,d)

                    res_key = min([a,b], key=lambda x: sum(x))
                    res_key2 = min([c,d], key=lambda x: sum(x))
                    res_key_max = max([a,b], key=lambda x: sum(x))
                    res_key_max2 = max([c,d], key=lambda x: sum(x))
                    print("SMALLER VALUES:",res_key, res_key2)
                    wall_1.set_new_points(res_key,res_key2)
                    wall_2.set_new_points(res_key_max,res_key_max2)


        return walls





    def check_collision(self,player_pos, return_only_collision = False, collision_box = 0, screen = screen ,x_vel = 0, y_vel = 0, dir_coll = False):

        collision_box_size = collision_box

        collide = False
        collides = 0
        vert_coll, hor_coll = False, False
        closest_point = None

        x5,y5 = player_pos

        if collision_box > player_pos[0]:
            x5 = collision_box
            collide = True
            vert_coll = True

        if self.size[0]/self.conv - collision_box < player_pos[0]:
            x5 = self.size[0]/self.conv - collision_box
            vert_coll = True
            collide = True
        if collision_box > player_pos[1]:
            y5 = collision_box
            collide = True
            hor_coll = True
        if self.size[1]/self.conv - collision_box < player_pos[1]:
            y5 = self.size[1]/self.conv - collision_box
            collide = True
            hor_coll = True

        # if collide and not dir_coll:
        #
        #     return [x5,y5]




        player_pos_der = [x5,y5]

        #pygame.draw.rect(screen,[255,0,0], [player_pos[0]-collision_box_size,player_pos[1]-collision_box_size,collision_box_size,collision_box_size])



        for polygon in self.polygons:
            a,b,c,d = polygon
            x = [a[0],b[0],c[0],d[0]]
            y = [a[1],b[1],c[1],d[1]]

            if player_pos[0] < min(x)-50 or player_pos[0] > max(x)+50 or player_pos[1] < min(y)-50 or player_pos[1] > max(y)+50:
                continue

            poly = pygame.Rect(min(x)- collision_box_size,min(y) - collision_box_size, max(x)-min(x) + collision_box_size*2, max(y) - min(y) + collision_box_size*2)

            minx,maxx,miny,maxy = min(x) - collision_box_size, max(x) + collision_box_size, min(y) - collision_box_size, max(y) + collision_box_size

            #pygame.draw.rect(screen,[255,255,0], [min(x)- collision_box_size,min(y) - collision_box_size, max(x)-min(x) + collision_box_size*2, max(y) - min(y) + collision_box_size*2])

            if poly.collidepoint(player_pos_der):

                collides += 1

                collide = True

                closest = 1000
                for line in range(4):
                    x1,y1 = [a,b,c,d][line]

                    x2,y2 = [a,b,c,d,a][line+1]

                    if [x1,y1] in self.points_inside_polygons and [x2,y2] in self.points_inside_polygons:
                        continue

                    x3,y3 = player_pos_der

                    dx = x2 - x1
                    dy = y2 - y1

                    alpha = (dy * y3 - dy * y1 + dx * x3 - dx * x1) / (dy ** 2 + dx ** 2)
                    #beta = (dy * x3 - dy * x1 - dx * y3 + dx * y1) / (dy ** 2 + dx ** 2)



                    x4 = x1+alpha*dx
                    y4 = y1+alpha*dy

                    dist_to_player = get_dist(player_pos, [x4,y4])
                    if dist_to_player < closest:
                        closest = dist_to_player
                        closest_line = [[x1,y1],[x2,y2]]






                if minx < player_pos_der[0] < maxx and closest_line[0][0] == closest_line[1][0]:
                    player_pos_der[0] = func.get_closest_value(player_pos_der[0],[minx, maxx])
                    vert_coll = True

                if miny < player_pos_der[1] < maxy and closest_line[0][1] == closest_line[1][1]:
                    player_pos_der[1] = func.get_closest_value(player_pos_der[1],[miny, maxy])
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
        for x1 in range(21):
            for y1 in range(16):
                point = [x1*100/conv,y1*100/conv]
                point[0] += 15
                point[1] += 15


                collision = False

                for polygon in self.polygons:
                    a,b,c,d = polygon
                    x = [a[0],b[0],c[0],d[0]]
                    y = [a[1],b[1],c[1],d[1]]

                    poly = pygame.Rect(min(x),min(y), max(x)-min(x), max(y) - min(y))

                    if poly.collidepoint(point):
                        collision = True
                        break
                if not collision:
                    self.nav_mesh_available_spots.append(point)



    def get_random_point(self, walls, p_pos = None, enemies = None, visibility = True, max_tries = 100):
        tries = 0
        while True:
            tries += 1
            point = func.pick_random_from_list(self.nav_mesh_available_spots)
            conds = [True, True]
            if p_pos != None:
                if los.check_los(p_pos, point, walls):
                    conds[0] = False
            if enemies != None:
                for x in enemies:
                    if los.check_los(point, x.get_pos(), walls):
                        conds[1] = False
                        break

            if False not in conds or tries > max_tries:
                return point






    def render(self, conv):

        self.map_rendered = pygame.Surface([self.size[0]/conv, self.size[1]/conv, ])
        self.map_rendered.fill([255,255,255])

        self.textures = {
        "floor_tile_1" : pygame.image.load("texture/floor.png").convert_alpha()
        }


        self.map_rendered.blit(self.background,(0,0))




        for object in self.objects:   ### ((0,0),"floor_tile_1",180)
            object_texture = self.textures[object[1]]
            if object[2] != 0:
                rotated_image, new_rect = rot_center(object_texture,object[2],object[0][0],object[0][1])
                object_pos = [object[0][0] - new_rect[0], object[0][1] - new_rect[1]]
            else:
                object_pos = object[0]
                rotated_image = object_texture
            self.map_rendered.blit(rotated_image, object_pos)

        for polygon in self.polygons:
            print(polygon)
            #pygame.draw.polygon(self.map_rendered, [0,0,0], polygon)

        for point in self.nav_mesh_available_spots:
            pygame.draw.rect(self.map_rendered, [255,0,0], [point[0], point[1], 1,1])


        return self.map_rendered



def rot_center(image, angle, x, y):

    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(center = (x, y)).center)

    return rotated_image, new_rect

map = (
        # # Border
        # {"a":{"x":0,"y":0}, "b":{"x":size[0],"y":0}},
        # {"a":{"x":size[0],"y":0}, "b":{"x":size[0],"y":size[1]}},
        # {"a":{"x":size[0],"y":size[1]}, "b":{"x":0,"y":size[1]}},
        # {"a":{"x":0,"y":size[1]}, "b":{"x":0,"y":0}},

        # Polygon #1
        {"a":{"x":100,"y":100}, "b":{"x":300,"y":100}},
        {"a":{"x":300,"y":100}, "b":{"x":300,"y":300}},
        {"a":{"x":300,"y":300}, "b":{"x":100,"y":300}},
        {"a":{"x":100,"y":300}, "b":{"x":100,"y":100}},

        # Polygon #1
        {"a":{"x":700,"y":100}, "b":{"x":800,"y":100}},
        {"a":{"x":800,"y":100}, "b":{"x":800,"y":300}},
        {"a":{"x":800,"y":300}, "b":{"x":700,"y":300}},
        {"a":{"x":700,"y":300}, "b":{"x":700,"y":100}},


)
