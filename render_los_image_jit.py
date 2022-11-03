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
import func
from values import *
from los import *
from numba import jit
import pygame
import jit_tools


def draw(
    los_screen,
    phase,
    camera_pos,
    player_pos,
    map,
    walls,
    size,
    los_angle=None,
    angle_tolerance=0,
    debug_angle=None,
    quick_render=False,
    los_background=None,
):

    """
    Renders the black and white image from a set of walls.
    This version uses numpy array of wall points to use jit powered intersection calculation.
    """

    cam_array = np.array(camera_pos, dtype = int)
    #start_pos = minus_list(player_pos, camera_pos)
    s_np = np.array(player_pos, dtype = int)



    walls2 = np.empty((0,4), int)


    walls = jit_tools.filter_walls_jit(walls, walls2, cam_array, size)

    if not quick_render:
        los_screen.fill(pygame.Color([0, 0, 0]))

    if los_background:
        los_screen.blit(los_background, [0, 0], area = [camera_pos[0], camera_pos[1], size[0], size[1]])




    y = np.zeros([0,0], dtype=float)
    angle_array = np.full_like(y, 0, shape = (walls.shape[0] + 4, 8))

    angle_array = jit_tools.get_wall_angles(s_np, walls, angle_array)

    jit_tools.filter_out_non_visible_walls(angle_array)

    del_list = []
    for i, line in enumerate(angle_array):
        if line[-1] == 0:
            del_list.append(i)

    for i in sorted(del_list, reverse = True):
        angle_array = np.delete(angle_array,i,axis = 0)


    individual_angle_array = np.full_like(y, 0, shape = (angle_array.shape[0] * 2 + 4, 4))

    individual_angle_array = jit_tools.re_arrange(individual_angle_array, angle_array)

    i = 1
    for p1 in [0,0], [size[0], 0], [size[0], size[1]], [0, size[1]]:
        angle1 =  math.atan2(p1[1] - s_np[1], p1[0] - s_np[0])
        if angle1 < 0:
            angle1 += math.pi * 2

        individual_angle_array[-i,0] = angle1
        individual_angle_array[-i, 1] = p1[0]
        individual_angle_array[-i, 2] = p1[1]
        individual_angle_array[-i, 3] = 1
        i += 1

    individual_angle_array = jit_tools.check_visible_points(s_np, individual_angle_array, angle_array)


    del_list = []
    angles = []
    for i, line in enumerate(individual_angle_array):
        if line[-1] == 0 or line[0] in angles:
            del_list.append(i)
        else:
            angles.append(line[0])

    for i in sorted(del_list, reverse = True):
        individual_angle_array = np.delete(individual_angle_array,i ,axis = 0)

    amount_of_points = individual_angle_array.shape[0]


    angles = individual_angle_array[individual_angle_array[:, 0].argsort()]

    #print("sorted angles:", angles)

    triangle_array = np.full_like(y, 0, shape = (amount_of_points, 8))


    for i, line in enumerate(angles):

        if i == 0:
            i2 = angles.shape[0] - 1
        else:
            i2 = i - 1

        triangle_array[i, 0] = line[0] + 0.0001
        triangle_array[i2, 4] = line[0] - 0.0001


    start = time.perf_counter()

    triangle_array = jit_tools.calc_triangles(np.array(player_pos), triangle_array, angles, angle_array)

    return draw_triangles(s_np, triangle_array, angles, angle_array, los_screen, phase), time.perf_counter() - start

def draw_triangles(s_np, triangle_array, angles, angle_array, screen, phase):

    for line in angles:
        if line[-1] == 0:
            continue
        pygame.draw.line(screen, [255,255,255], s_np, line[1:3],3)


    for triangle in triangle_array:
        try:


            x1, y1 = s_np
            x2, y2 = int(triangle[1]), int(triangle[2])
            x3, y3 = int(triangle[5]), int(triangle[6])

            pygame.gfxdraw.filled_trigon(
                screen, x1, y1, x2, y2, x3, y3, [255,255,255]
            )

            # pygame.draw.circle(screen, [255,255/i,255/i], [x2,y2], 10)
            # pygame.draw.circle(screen, [255,255,255], [x3,y3], 10)

        except Exception as e:
            print(e)

    if phase == 1:
        for line in angles:
            if line[-1] == 0:
                continue
            pygame.draw.line(screen, [255,0,0], s_np, line[1:3])
    elif phase == 2:
        for line in angle_array:
            if line[-1] == 0:
                continue
            pygame.draw.line(screen, [255,0,255], line[0:2], line[3:5])


    return screen





if __name__ == '__main__':
    player_pos = [-58.21221355950286, -314.7711827184913]
    #camera_pos = [623.8173302107729, 500]
    camera_pos = [100, 200]

    start_pos = minus_list(player_pos, camera_pos)

    clock = pygame.time.Clock()

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

    for i in range(1):

        size1 = 1336, 768

        size = np.array(size1)


        screen = pygame.display.set_mode(size1)
        w = []
        angles = []
        triangle_array = []

        l = pygame.Surface(size1)

        while 1:

            clock.tick(60)

            #start_pos = minus_list(player_pos, camera_pos)
            if pygame.mouse.get_pressed()[0]:
                player_pos = list(pygame.mouse.get_pos())
                t = time.perf_counter()
                l, t1 = draw(l, 1, camera_pos, player_pos, None, walls, size)
                print(f"{(time.perf_counter() - t)*1000:.2f}ms")
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    sys.exit()

            screen.fill((0,0,0))

            screen.blit(l, (0,0))

            # for line in w:
            #     pygame.draw.line(screen, [255,255,255] if line[-1] == 1 else [255,0,0], (line[0], line[1]), (line[3], line[4]))


            i = 1


            pygame.display.update()
