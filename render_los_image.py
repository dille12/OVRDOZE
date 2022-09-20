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


def draw(
    los,
    phase,
    camera_pos,
    player_pos,
    map,
    walls,
    los_angle=None,
    angle_tolerance=0,
    debug_angle=None,
    quick_render=False,
    los_background=None,
):

    """
    Renders the black and white image from a set of walls.
    """

    walls2 = []
    walls3 = []

    for i in walls:
        p1, p2 = i.get_points()
        if check_point(func.minus(p1, camera_pos, op = "-")) or check_point(func.minus(p2, camera_pos, op = "-")):
            walls2.append(i)

    walls = walls_generate(walls2, camera_pos)

    time_stamps = {}

    t = time.time()

    start = time.time()

    camera_pos = ratio(camera_pos, size_ratio)
    player_pos = ratio(player_pos, size_ratio)

    start_pos = minus_list(player_pos, camera_pos)

    # los.set_colorkey((255,255,255))
    if not quick_render:
        los.fill(pygame.Color([0, 0, 0]))

    if los_background:
        los.blit(los_background, [-camera_pos[0], -camera_pos[1]])

    point_dict = {}
    point_dict_dist = {}
    wall_points = []

    for point in [(0, 0), (size[0], 0), (size[0], size[1]), (0, size[1])]:
        angle = 180 + math.degrees(
            math.atan2(point[1] - start_pos[1], point[0] - start_pos[0])
        )
        point_dict[angle] = point

    time_stamps["angle calcs"] = time.time() - t
    t = time.time()

    if los_angle != None:

        los_angle1 = 360 - los_angle - 10
        line = [
            start_pos[0] + math.cos(math.radians(los_angle1)) * draw_distance,
            start_pos[1] + math.sin(math.radians(los_angle1)) * draw_distance,
        ]
        point_dict[los_angle1] = line

        los_angle2 = 360 - los_angle + 10
        line = [
            start_pos[0] + math.cos(math.radians(los_angle2)) * draw_distance,
            start_pos[1] + math.sin(math.radians(los_angle2)) * draw_distance,
        ]
        point_dict[los_angle2] = line

    time_stamps["los_angle"] = time.time() - t
    t = time.time()

    angle_possible_intersections = {}

    wall_angles = []

    time_stamps["point inits"] = time.time() - t
    t = time.time()

    for wall_1 in walls:
        wall_spes_points = []

        point1, point2 = wall_1.get_points()

        if (
            0 < point1[0] < size[0]
            and 0 < point1[1] < size[1]
            or 0 < point2[0] < size[0]
            and 0 < point2[1] < size[1]
        ):
            pass
        else:
            continue

        for point in wall_1.get_points():

            angle = 180 + math.degrees(
                math.atan2(point[1] - start_pos[1], point[0] - start_pos[0])
            )

            if angle not in angle_possible_intersections:
                angle_possible_intersections[angle] = [wall_1]
            else:
                angle_possible_intersections[angle].append(wall_1)

            wall_spes_points.append(angle)
            if angle not in point_dict:
                point_dict[angle] = point
            else:
                point2 = point_dict[angle]
                dist1, dist2 = get_dist_points(start_pos, point), get_dist_points(
                    start_pos, point2
                )
                if dist1 < dist2:
                    point_dict[angle] = point

        angles = sorted(wall_spes_points)

        wall_angles.append([angles, wall_1])

        #
        # angle1 = angles[0]
        # angle2 = angles[1]
        #
        # for angle3 in point_dict:
        #     if angle1 < angle3 < angle2:
        #         angle_possible_intersections[angle3].append(wall_1)
        #
        wall_points.append(wall_1.get_points())

    time_stamps["wall inits"] = time.time() - t
    t = time.time()

    intersects_visible = {}

    potential_point = []

    for angles, wall_2 in wall_angles:

        angle1, angle2 = sorted(angles)

        diff1 = get_angle_diff(angle1, angle2)

        for angle3 in point_dict:
            diff2 = get_angle_diff(angle1, angle3)

            if (
                angle1 - diff1 >= angle1 - diff2 >= angle1
                or angle1 - diff1 <= angle1 - diff2 <= angle1
            ):

                # if angle1-1 < angle3 < angle2+1:
                if angle3 not in angle_possible_intersections:
                    angle_possible_intersections[angle3] = [wall_2]
                else:
                    angle_possible_intersections[angle3].append(wall_2)

    if los_angle != None:
        delete_angles = []
        for angle in point_dict:
            if (
                not los_angle1 < angle < los_angle2
                and angle != los_angle1
                and angle != los_angle2
            ):
                delete_angles.append(angle)

        for x in delete_angles:

            for list in [point_dict, point_dict_dist, angle_possible_intersections]:
                try:
                    del list[x]
                except:
                    pass

    time_stamps["angle intersects"] = time.time() - t
    t = time.time()

    calcs = 0

    point_intersections = {}
    wall_points_set = {}

    for angle in point_dict:

        angle_spes_inter = [0, 0, 0]
        angle_point = point_dict[angle]

        point_intersections[angle] = []

        angle_inter = []

        for i in [-0.001, 0, 0.001]:

            if i == -0.001:
                j = 0
            elif i == 0:
                j = 1
            else:
                j = 2

            line = [
                start_pos[0] + math.cos(math.radians(angle + 180 + i)) * draw_distance,
                start_pos[1] + math.sin(math.radians(angle + 180 + i)) * draw_distance,
            ]
            intersec_list = {}
            intersecting = False
            if angle not in angle_possible_intersections:
                point_dict_dist[angle] = line
                continue

            for wall_1 in angle_possible_intersections[angle]:
                calcs += 1
                point_1, point_2 = wall_1.get_points()

                if intersect(start_pos, line, point_1, point_2):

                    intersecting = True
                    if angle_point in [point_1, point_2]:
                        angle_spes_inter[j] = 1

                    else:
                        point_intersections[angle].append(wall_1)

                    continue

            if intersecting == False:
                point_dict_dist[angle] = line

        if 0 in angle_spes_inter:
            line = [
                angle_point[0] + math.cos(math.radians(angle + 180)) * draw_distance,
                angle_point[1] + math.sin(math.radians(angle + 180)) * draw_distance,
            ]

            potential_point.append(angle_point)
            closest = 10000
            closest_point = None
            closest_wall = None
            for wall_1 in point_intersections[angle]:
                point_1, point_2 = wall_1.get_points()
                if angle_point in [point_1, point_2]:
                    continue
                if intersect(angle_point, line, point_1, point_2):
                    inter_point = line_intersection(
                        (angle_point, line), (point_1, point_2)
                    )
                    dist = get_dist_points(start_pos, inter_point)
                    if dist < closest:
                        closest_point = inter_point
                        closest = dist
                        closest_wall = wall_1

            if closest_point != None:
                if get_dist_points(angle_point, closest_point) > 5:
                    intersects_visible[angle] = [closest_point, point_1, point_2]

                    p1, p2 = closest_wall.get_points()

                    if math.atan2(
                        p1[1] - player_pos[1], p1[0] - player_pos[0]
                    ) > math.atan2(p2[1] - player_pos[1], p2[0] - player_pos[0]):
                        p_1 = p1
                        p_2 = p2
                    else:
                        p_2 = p1
                        p_1 = p2

                    if angle_spes_inter[2] == 0:  #

                        wall_points_set[angle] = [closest_wall, p_1, closest_point]
                    else:
                        wall_points_set[angle] = [closest_wall, p_2, closest_point]

                    #     closest_wall.set_new_points(p_1, closest_point)
                    # else:
                    #     closest_wall.set_new_points(p_2, closest_point)

    time_stamps["angle closeby check"] = time.time() - t
    t = time.time()

    wall_inter = []
    nearest = None
    nearest_dist = None
    nearest_wall = None
    last_nearest_wall = [None]

    skip_point = []
    drawable_point = {}
    visible_points = []

    for angle in point_dict:
        point = point_dict[angle]
        intersecting_ray = False
        for wall_1 in walls:

            point_1, point_2 = wall_1.get_points()
            if point in [point_1, point_2]:
                continue
            if intersect(start_pos, point, point_1, point_2):
                intersecting_ray = True

        if not intersecting_ray:
            drawable_point[angle] = point
            visible_points.append(point)

        else:
            if angle in intersects_visible:
                del intersects_visible[angle]
                del wall_points_set[angle]

    for angle in wall_points_set:
        wall_1, p1, p2 = wall_points_set[angle]
        wall_1.set_new_points(p1, p2)

    sorted_angles = sorted(drawable_point)

    # sorted_angles.insert(0, sorted_angles[-1])
    try:
        last_angle = sorted_angles[-1]
        point2 = drawable_point[sorted_angles[-1]]

        if last_angle in intersects_visible:
            sorted_angles.insert(0, sorted_angles[-1])
            del sorted_angles[-1]

            last_angle = sorted_angles[-1]
            point2 = drawable_point[sorted_angles[-1]]

    except:
        return los, 0

    first_angle = last_angle

    time_stamps["finishing"] = time.time() - t
    t = time.time()

    draw_point_list = drawable_point.values()
    wall_points = []
    for wall_1 in walls:
        wall_points.append(wall_1.get_points())

    ##############################################################################################################################################################################################
    last_point_intersected = False
    last_intersect_wp = None
    angle_completed_wall = []
    for i in sorted_angles:
        next_point = None
        if i in intersects_visible:

            p1 = drawable_point[i]
            i1 = intersects_visible[i][0]

            if (p1, point2) in wall_points or (point2, p1) in wall_points:
                point = p1
                next_point = i1
                angle_completed_wall.append(i)
            else:
                # if last_intersect_wp != None:
                #     if last_intersect_wp[0][0] <= i1[0] <= last_intersect_wp[1][0] and last_intersect_wp[0][1] <= i1[1] <= last_intersect_wp[1][1]:
                #         point = i1
                #         next_point = p1
                #
                #     else:
                #
                #         point = p1
                #         next_point = i1
                #
                # else:
                point = i1
                next_point = p1

        else:
            point = drawable_point[i]

        try:

            cond1 = (point, point2) not in wall_points
            cond2 = (point2, point) not in wall_points

            if (
                i in point_dict_dist
                and last_angle in point_dict_dist
                and cond1
                and cond2
            ):

                x1, y1 = get_rounded_pos(start_pos)
                x2, y2 = get_rounded_pos(point_dict_dist[i])
                x3, y3 = get_rounded_pos(point_dict_dist[last_angle])

                pygame.gfxdraw.filled_trigon(
                    los, x1, y1, x2, y2, x3, y3, (255, 255, 255)
                )

                # pygame.draw.polygon(los,[255,255,255],[start_pos,point_dict_dist[i],point_dict_dist[last_angle]])

            else:
                x1, y1 = get_rounded_pos(start_pos)
                x2, y2 = get_rounded_pos(point)
                x3, y3 = get_rounded_pos(point2)
                pygame.gfxdraw.filled_trigon(
                    los, x1, y1, x2, y2, x3, y3, (255, 255, 255)
                )
                # pygame.draw.polygon(los,[255,255,255],[start_pos,point,point2])

        except Exception as e:
            print(point, e)
        if next_point != None:
            point2 = next_point
            last_point_intersected = True
            last_intersect_wp = intersects_visible[i][1:]
        else:
            last_point_intersected = False
            last_intersect_wp = None
            point2 = point

        last_angle = i

    ##############################################################################################################################################################################################

    # min_angle = max(angle_possible_intersections)

    debug_angle = 180 - debug_angle
    if debug_angle < 0:
        debug_angle += 360
    elif debug_angle > 360:
        debug_angle -= 360

    res_key = min(drawable_point.keys(), key=lambda x: abs(debug_angle - x))

    if phase == 2:
        for point1, point2 in wall_points:
            pygame.draw.circle(los, [255, 0, 0], point1, 5)
            pygame.draw.circle(los, [255, 0, 0], point2, 5)
        pygame.draw.line(los, [255, 0, 0], start_pos, point_dict[res_key])
        try:
            for wall_1 in walls:
                #if point_dict[res_key] in wall_1.get_points():
                wall_1.highlight(los)

            text = debug_text.render(
                "WALLS LOADED: " + str(len(walls)),
                False,
                [255,255,0],
            )

            los.blit(text, (200,50))




        except Exception as e:
            print("exception")
            print(e)

    if phase == 1:

        for aids in drawable_point:
            point = drawable_point[aids]
            if aids == first_angle:
                color = [200, 200, 200]
            elif aids in intersects_visible:
                if aids in angle_completed_wall:
                    color = [255, 0, 255]
                else:
                    color = [255, 0, 0]
            elif aids in point_dict_dist:
                color = [0, 255, 0]
            else:
                color = [0, 255, 255]
            if aids != res_key:
                pygame.draw.line(los, color, start_pos, point)
                pygame.draw.rect(los, color, [point[0], point[1], 10, 10])

            else:

                pygame.draw.line(los, color, start_pos, point, 4)
                pygame.draw.rect(los, color, [point[0], point[1], 10, 10])
                text = debug_text.render(
                    str(int(conv * (point[0] + camera_pos[0])))
                    + ":"
                    + str(int(conv * (point[1] + camera_pos[1])))
                    + ":"
                    + str(round(aids, 3)),
                    False,
                    color,
                )
                los.blit(text, (point[0] + 10, point[1] + 10))

        for aids in intersects_visible:
            point = intersects_visible[aids][0]

            pygame.draw.line(los, [255, 0, 0], start_pos, point)
            pygame.draw.rect(los, [255, 0, 0], [point[0], point[1], 10, 10])

    time_stamps["draw"] = time.time() - t
    total = sum(time_stamps.values())

    walls = []
    draw_time = time.time() - start

    return los, draw_time
