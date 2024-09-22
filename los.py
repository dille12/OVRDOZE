import pygame
import random
import math
import numpy as np

clock = pygame.time.Clock()
pygame.font.init()
import traceback
import sys
import time
import pygame.gfxdraw
from values import *
from numba import jit
walls = []

draw_distance = 1200 * multiplier2

vecEdges = []

debug_text = pygame.font.Font(fp("texture/terminal.ttf"), 10)



def get_angle_diff(angle1, angle2):
    anglediff = (angle1 - angle2 + 180 + 360) % 360 - 180
    return anglediff

def get_angle_diff_rad(angle1, angle2):
    anglediff = (angle1 - angle2 + math.pi + 2*math.pi) % 2*math.pi - math.pi
    return anglediff


def get_points_from_np(line):
    return (line[0], line[1]), (line[2], line[3])


def get_rounded_pos(point):
    x1, y1 = point
    x1 = int(round(x1))
    y1 = int(round(y1))
    return x1, y1


def get_dist(p1, p2, p3):
    p1 = np.asarray(p1)
    p2 = np.asarray(p2)
    p3 = np.asarray(p3)
    d = [np.linalg.norm(np.cross(p2 - p1, p1 - p3)) / np.linalg.norm(p2 - p1)]
    for point in [p1, p2]:
        d.append(math.sqrt((p3[0] - point[0]) ** 2 + (p3[1] - point[1]) ** 2))

    return d


def get_dist_points(point_1, point_2):
    return math.sqrt((point_2[0] - point_1[0]) ** 2 + (point_2[1] - point_1[1]) ** 2)


def ccw(A, B, C):
    return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])


def intersect(A, B, C, D):
    return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)


agency = pygame.font.Font(fp("texture/agencyb.ttf"), round(70))


def debug_render(text_str):
    text = agency.render(str(text_str), False, [255, 255, 0])
    render_cool(text, [60, 60], 15, 16, render=True, offset=10)  ### IN GAME

def within_tolernace(point1, point2, angle, tolerance):
    angle2 = math.degrees(math.atan2(point2[0]-point1[0],point2[1]-point1[1]))

    if abs(get_angle_diff(angle, angle2)) < tolerance:
        return True
    else:
        return False



def rot_center(image, angle, x, y):

    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(center=(x, y)).center)

    return rotated_image, new_rect


def check_line_cross(line_start, line_end, segment_start, segment_end):

    slope = (line_end[1] - line_start[1]) / (line_end[0] - line_start[0])

    line_start = list(line_start)

    line_start[1] -= slope * 1000
    line_start[0] -= 1000
    line_end[1] += slope * 1000
    line_end[0] += 1000

    return intersect(line_start, line_end, segment_start, segment_end)


a = [40, 50]
b = [45, 50]
c = [50, 40]
d = [50, 60]


ang1 = 45

ang2 = 315

ang3 = 50
diff1 = get_angle_diff(ang2, ang1)
diff2 = get_angle_diff(ang3, ang1)

print(diff1)

print(diff2)

print(ang1 - diff1, ang1 - diff2, ang1)

print(ang1 - diff1 >= ang1 - diff2 >= ang1 or ang1 - diff1 <= ang1 - diff2 <= ang1)


class Wall:
    def __init__(self, start, end, pol=[]):
        global walls
        self.__start = start
        self.__end = end
        self.__center = [(start[0] + end[0]) / 2, (start[1] + end[1]) / 2]
        self.polygon = pol

        self.set_vert()

    def __str__(self):
        return "WALL: " + str(self.__start) + " " + str(self.__end)

    def set_vert(self):
        if abs(self.__start[0] - self.__end[0]) < 5:
            self.vertical = True
        else:
            self.vertical = False

    def get_center(self):
        return self.__center

    def get_points(self):
        return self.__start, self.__end

    def set_new_points(self, p1, p2):
        self.__start = p1
        self.__end = p2
        self.set_vert()

    def highlight(self, screen):

        if not random.randint(1, 5) == 1:
            return

        pygame.draw.line(
            screen, [255, 0, 255], self.__start, self.__end, random.randint(1, 5)
        )

        t = debug_text.render(str(self.vertical), False, [255, 0, 0])
        screen.blit(t, self.__center)

def walls_generate_np(walls_filtered, cam_array):
    for line in walls_filtered:
        line[0:2] -= cam_array
        line[2:4] -= cam_array
    return walls_filtered


def walls_generate(walls_filtered, camera_pos):
    size_ratio = 1
    walls = []

    for wall in walls_filtered:
        a, b = wall.get_points()

        if if_within_screen(a, camera_pos) and if_within_screen(b, camera_pos):
            pass
        else:
            continue

        a = ratio(a, size_ratio)
        b = ratio(b, size_ratio)

        a = minus_list(a, camera_pos)
        b = minus_list(b, camera_pos)

        walls.append(Wall(a, b))

    return walls


# Wall([0,0],[800,0])
# Wall([0,0],[0,800])
# Wall([800,0],[800,800])
# Wall([0,800],[800,800])


alpha_col = (255, 255, 255)


start_pos = [400, 400]

size_ratio = 1

conv = 1920 / 854


pygame.init()
screen = pygame.display.set_mode(size)
los = pygame.Surface(size, pygame.SRCALPHA, 32).convert_alpha()
# screen = pygame.display.set_mode(size)
# background = pygame.Surface(size)
# background.fill(pygame.Color([0,70,0]))


def render_cool(
    image,
    pos,
    tick,
    beat_tick_h,
    render=False,
    offset=0,
    scale=1,
    screen=los,
    style="default",
    alpha=255,
):

    a = 1 - math.sin(offset + 10 * tick / (2 * math.pi * beat_tick_h)) * 0.1 * scale
    b = (
        1
        - math.sin(math.pi / 2 + offset + 10 * tick / (2 * math.pi * beat_tick_h))
        * 0.1
        * scale
    )
    rotation = (
        math.sin(math.pi / 2 + offset + 10 * tick / (2 * math.pi * beat_tick_h))
        * 2
        * scale
    )
    if style == "default":
        image_size = image.get_rect().size
        image_size_2 = [round(image_size[0] * a), round(image_size[1] * b)]

        image_2 = pygame.transform.scale(image, image_size_2)

        pos = [pos[0] - a / 4 * image_size_2[0], pos[1] - b / 4 * image_size_2[1]]

        if render == True:
            image_2, image_2_rot = rot_center(image_2, rotation, pos[0], pos[1])

        screen.blit(image_2, pos)

def det(a, b):
    return a[0] * b[1] - a[1] * b[0]

def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    div = det(xdiff, ydiff)
    if div == 0:
        raise Exception("lines do not intersect")

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y


def minus_list(list1, list2):
    list3 = list1.copy()
    for i in range(len(list1)):
        list3[i] = list1[i] - list2[i]

    return list3


def add_list(list1, list2):
    list3 = list1.copy()
    for i in range(len(list1)):
        list3[i] = list1[i] + list2[i]

    return list3


def ratio(pos, ratio):
    return [pos[0] / ratio, pos[1] / ratio]


def if_within_screen(point, camera_pos):
    check = (
        0 < point[0] - camera_pos[0] < fs_size[0]
        or 0 < point[1] - camera_pos[1] < fs_size[1]
    )
    return check


def check_point(point):
    check = 0 < point[0] < size[0] and 0 < point[1] < size[1]
    return check

def check_point_cam(point, cam):
    check = 0 < point[0] - cam[0] < size[0] and 0 < point[1] - cam[1] < size[1]
    return check

def check_wall_np(wall, cam_array):
    check = check_point(wall[0:2] - cam_array) or check_point(wall[2:4] - cam_array)
    return check


def check_los(p1, p2, los_walls, vis_walls = []):
    for walls in [los_walls, vis_walls]:
        for wall_1 in walls:
            point_1, point_2 = wall_1.get_points()
            if intersect(p1, p2, point_1, point_2):
                return False
    return True


def check_los_points(p1, p2, los_walls):
    for wall_1 in los_walls:
        point_1, point_2 = wall_1
        if intersect(p1, p2, point_1, point_2):
            return False
    return True


print("INITTING JIT")

@jit(nopython = True)
def ccw_jit(A, B, C):
    return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])

@jit(nopython = True)
def intersect_jit(A, B, C, D):
    return ccw_jit(A, C, D) != ccw_jit(B, C, D) and ccw_jit(A, B, C) != ccw_jit(A, B, D)

@jit(nopython = True)
def check_los_jit(p1, p2, walls, walls2 = None):

    for line in walls:
        if intersect_jit(p1, p2, line[0:2], line[2:4]):
            return False

    if walls2 == None:
        return True

    for line in walls2:
        if intersect_jit(p1, p2, line[0:2], line[2:4]):
            return False

    return True


print("Success")
