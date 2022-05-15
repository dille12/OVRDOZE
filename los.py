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

walls = []

draw_distance = 700

vecEdges = []

debug_text = pygame.font.Font('texture/terminal.ttf', 10)

def get_angle_diff(angle1,angle2):
    anglediff = (angle1 - angle2 + 180 + 360) % 360 - 180
    return anglediff

def get_rounded_pos(point):
    x1, y1 = point
    x1 = int(round(x1))
    y1 = int(round(y1))
    return x1,y1

def get_dist(p1, p2, p3):
    p1 = np.asarray(p1)
    p2 = np.asarray(p2)
    p3 = np.asarray(p3)
    d = [np.linalg.norm(np.cross(p2-p1, p1-p3))/np.linalg.norm(p2-p1)]
    for point in [p1,p2]:
        d.append(math.sqrt((p3[0] - point[0])**2 + (p3[1] - point[1])**2))


    return d

def get_dist_points(point_1,point_2):
    return math.sqrt((point_2[0] - point_1[0])**2 + (point_2[1] - point_1[1])**2)

def ccw(A,B,C):
    return (C[1]-A[1])*(B[0]-A[0]) > (B[1]-A[1])*(C[0]-A[0])

def intersect(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)
agency = pygame.font.Font('texture/agencyb.ttf', round(70))

def debug_render(text_str):
    text = agency.render(str(text_str), False, [255,255,0])
    render_cool(text, [60,60],15,16,render = True, offset = 10)   ### IN GAME

def rot_center(image, angle, x, y):

    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(center = (x, y)).center)

    return rotated_image, new_rect




def check_line_cross(line_start, line_end, segment_start, segment_end):

    slope = (line_end[1] - line_start[1])/(line_end[0] - line_start[0])

    line_start = list(line_start)

    line_start[1] -= slope * 1000
    line_start[0] -= 1000
    line_end[1] += slope * 1000
    line_end[0] += 1000

    return intersect(line_start, line_end, segment_start, segment_end)



a = [40,50]
b = [45,50]
c = [50,40]
d = [50,60]


ang1 = 45

ang2 = 315

ang3 = 50
diff1 = get_angle_diff(ang2,ang1)
diff2 = get_angle_diff(ang3,ang1)

print(diff1)

print(diff2)

print(ang1 - diff1 , ang1 -diff2 , ang1)

print(ang1 - diff1 >= ang1 -diff2 >= ang1 or ang1 - diff1 <= ang1 -diff2 <= ang1)








class Wall:
    def __init__(self,start,end):
        global walls
        self.__start = start
        self.__end = end
        self.__center = [(start[0] + end[0])/2,(start[1] + end[1])/2]



    def get_center(self):
        return self.__center

    def get_points(self):
        return self.__start, self.__end

    def set_new_points(self,p1,p2):
        self.__start = p1
        self.__end = p2

    def highlight(self, screen):
        pygame.draw.line(screen,[255,0,255],self.__start, self.__end,5)



def walls_generate(walls_filtered, camera_pos):
    size_ratio = size2[0] / size[0]
    walls = []


    for wall in walls_filtered:
        a,b = wall.get_points()

        if if_within_screen(a) and if_within_screen(b):
            pass
        else:
            continue

        a = ratio(a,size_ratio)
        b = ratio(b,size_ratio)

        a = minus_list(a,camera_pos)
        b = minus_list(b,camera_pos)






        walls.append(Wall(a,b))

    return walls


#Wall([0,0],[800,0])
#Wall([0,0],[0,800])
#Wall([800,0],[800,800])
#Wall([0,800],[800,800])



alpha_col = (255,255,255)


start_pos = [400,400]

size =  854,480  #256, 144
size2 = 854,480
size_ratio = size2[0] / size[0]

print(size_ratio)

conv = 1920/854





pygame.init()
screen = pygame.display.set_mode(size)
los = pygame.Surface(size, pygame.SRCALPHA, 32).convert_alpha()
# screen = pygame.display.set_mode(size)
# background = pygame.Surface(size)
# background.fill(pygame.Color([0,70,0]))


def render_cool(image,pos,tick,beat_tick_h,render = False, offset = 0, scale = 1,screen = los , style = "default", alpha = 255):

    a = 1 - math.sin(offset+10*tick/(2*math.pi*beat_tick_h))*0.1 * scale
    b = 1 - math.sin(math.pi/2 +offset+10*tick/(2*math.pi*beat_tick_h))*0.1 * scale
    rotation = math.sin(math.pi/2 +offset+10*tick/(2*math.pi*beat_tick_h))*2 * scale
    if style == "default":
        image_size = image.get_rect().size
        image_size_2 = [round(image_size[0]*a),round(image_size[1]*b)]

        image_2 = pygame.transform.scale(image,image_size_2)

        pos = [pos[0] - a/4 * image_size_2[0], pos[1] - b/4 * image_size_2[1]]

        if render == True:
            image_2, image_2_rot = rot_center(image_2,rotation,pos[0],pos[1])

        screen.blit(image_2,pos)

def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y



def minus_list(list1,list2):
    list3 = list1.copy()
    for i in range(len(list1)):
        list3[i] = list1[i] - list2[i]

    return list3

def add_list(list1,list2):
    list3 = list1.copy()
    for i in range(len(list1)):
        list3[i] = list1[i] + list2[i]

    return list3

def ratio(pos, ratio):
    return [pos[0]/ratio, pos[1]/ratio]

def if_within_screen(point):
    check = 0 < point[0] < 1920 and 0 < point[1] < 1080
    return check

def check_los(p1,p2,los_walls):
    for wall_1 in los_walls:
        point_1, point_2 = wall_1.get_points()
        if intersect(p1, p2, point_1, point_2):
            return False
    return True

def check_los_points(p1,p2,los_walls):
    for wall_1 in los_walls:
        point_1, point_2 = wall_1
        if intersect(p1, p2, point_1, point_2):
            return False
    return True


def render_los_image(los, phase, camera_pos, player_pos,map, walls, los_angle = None, angle_tolerance = 0, debug_angle = None):

    time_stamps = {}

    t = time.time()

    start = time.time()






    camera_pos = ratio(camera_pos,size_ratio)
    player_pos = ratio(player_pos,size_ratio)

    start_pos = minus_list(player_pos,camera_pos)


    #los.set_colorkey((255,255,255))
    los.fill(pygame.Color([0,0,0]))

    point_dict = {}
    point_dict_dist = {}
    wall_points = []

    for point in [(0,0), (size[0],0),(size[0],size[1]),(0,size[1])]:
        angle = 180 + math.degrees(math.atan2(point[1] - start_pos[1],point[0] - start_pos[0]))
        point_dict[angle] = point

    if los_angle != None:

        los_angle1 = 360 - los_angle - 10
        line = [start_pos[0] + math.cos(math.radians(los_angle1)) * draw_distance, start_pos[1] + math.sin(math.radians(los_angle1)) * draw_distance]
        point_dict[los_angle1] = line

        los_angle2 = 360 - los_angle + 10
        line = [start_pos[0] + math.cos(math.radians(los_angle2)) * draw_distance, start_pos[1] + math.sin(math.radians(los_angle2)) * draw_distance]
        point_dict[los_angle2] = line




    angle_possible_intersections = {}

    wall_angles = []

    time_stamps["point inits"] = time.time() - t
    t = time.time()




    for wall_1 in walls:
        wall_spes_points = []

        point1,point2 = wall_1.get_points()

        if 0 < point1[0] < size[0] and 0 < point1[1] < size[1] or 0 < point2[0] < size[0] and 0 < point2[1] < size[1]:
            pass
        else:
            continue

        for point in wall_1.get_points():




            angle = 180 + math.degrees(math.atan2(point[1] - start_pos[1],point[0] - start_pos[0]))

            if angle not in angle_possible_intersections:
                angle_possible_intersections[angle] = [wall_1]
            else:
                angle_possible_intersections[angle].append(wall_1)

            wall_spes_points.append(angle)
            if angle not in point_dict:
                point_dict[angle] = point
            else:
                point2 = point_dict[angle]
                dist1, dist2 = get_dist_points(start_pos,point),get_dist_points(start_pos,point2)
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

        diff1 = get_angle_diff(angle1,angle2)

        for angle3 in point_dict:
            diff2 = get_angle_diff(angle1,angle3)

            if angle1 - diff1 >= angle1 -diff2 >= angle1 or angle1 - diff1 <= angle1 -diff2 <= angle1:


            #if angle1-1 < angle3 < angle2+1:
                if angle3 not in angle_possible_intersections:
                    angle_possible_intersections[angle3] = [wall_2]
                else:
                    angle_possible_intersections[angle3].append(wall_2)


    if los_angle != None:
        delete_angles = []
        for angle in point_dict:
            if not los_angle1 < angle < los_angle2 and angle != los_angle1 and angle != los_angle2:
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



        angle_spes_inter = [0,0,0]
        angle_point = point_dict[angle]

        point_intersections[angle]  = []

        angle_inter = []

        for i in [-0.001,0,0.001]:

            if i == -0.001:
                j = 0
            elif i == 0:
                j = 1
            else:
                j = 2


            line = [start_pos[0] + math.cos(math.radians(angle+180+i)) * draw_distance, start_pos[1] + math.sin(math.radians(angle+180+i)) * draw_distance]
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
            line = [angle_point[0] + math.cos(math.radians(angle+180)) * draw_distance, angle_point[1] + math.sin(math.radians(angle+180)) * draw_distance]

            potential_point.append(angle_point)
            closest = 10000
            closest_point = None
            closest_wall = None
            for wall_1 in point_intersections[angle]:
                point_1,point_2 = wall_1.get_points()
                if angle_point in [point_1, point_2]:
                    continue
                if intersect(angle_point, line, point_1, point_2):
                    inter_point = line_intersection((angle_point, line), (point_1, point_2))
                    dist = get_dist_points(start_pos,inter_point)
                    if dist < closest:
                        closest_point = inter_point
                        closest = dist
                        closest_wall = wall_1


            if closest_point != None:
                if get_dist_points(angle_point, closest_point) > 10:
                    intersects_visible[angle] = [closest_point, point_1, point_2]
                    p1, p2 = closest_wall.get_points()

                    if math.atan2(p1[1] - player_pos[1],p1[0] - player_pos[0]) > math.atan2(p2[1] - player_pos[1],p2[0] - player_pos[0]):
                        p_1 = p1
                        p_2 = p2
                    else:
                        p_2 = p1
                        p_1 = p2

                    if angle_spes_inter[2] == 0: #

                        wall_points_set[angle] = [closest_wall,p_1, closest_point]
                    else:
                        wall_points_set[angle] = [closest_wall,p_2, closest_point]


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

    #sorted_angles.insert(0, sorted_angles[-1])
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

            if (p1,point2) in wall_points or (point2, p1) in wall_points:
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

            cond1 = (point,point2) not in wall_points
            cond2 = (point2,point) not in wall_points

            if i in point_dict_dist and last_angle in point_dict_dist and cond1 and cond2:


                x1,y1 = get_rounded_pos(start_pos)
                x2,y2 = get_rounded_pos(point_dict_dist[i])
                x3,y3 = get_rounded_pos(point_dict_dist[last_angle])


                pygame.gfxdraw.filled_trigon(los, x1, y1, x2, y2, x3, y3, (255,255,255))




                #pygame.draw.polygon(los,[255,255,255],[start_pos,point_dict_dist[i],point_dict_dist[last_angle]])

            else:
                x1,y1 = get_rounded_pos(start_pos)
                x2,y2 = get_rounded_pos(point)
                x3,y3 = get_rounded_pos(point2)
                pygame.gfxdraw.filled_trigon(los, x1, y1, x2, y2, x3, y3, (255,255,255))
                #pygame.draw.polygon(los,[255,255,255],[start_pos,point,point2])



        except Exception as e:
            print(point,e)
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

    #min_angle = max(angle_possible_intersections)

    debug_angle = 180 - debug_angle
    if debug_angle < 0:
        debug_angle += 360

    res_key = min(drawable_point.keys(), key=lambda x: abs(debug_angle - x))

    if phase == 2:
        for point1, point2 in wall_points:
            pygame.draw.circle(los, [255,0,0], point1, 5)
            pygame.draw.circle(los, [255,0,0], point2, 5)
        pygame.draw.line(los,[255,0,0],start_pos,point_dict[res_key])
        try:
            for wall_1 in angle_possible_intersections[res_key]:
                wall_1.highlight(los)

        except Exception as e:
            print("exception")
            print(e)


    if phase == 1:


        for aids in drawable_point:
            point = drawable_point[aids]
            if aids == first_angle:
                color = [200,200,200]
            elif aids in intersects_visible:
                if aids in angle_completed_wall:
                    color = [255,0,255]
                else:
                    color = [255,0,0]
            elif aids in point_dict_dist:
                color = [0,255,0]
            else:
                color = [0,255,255]
            if aids != res_key:
                pygame.draw.line(los,color,start_pos,point)
                pygame.draw.rect(los,color,[point[0],point[1],10,10])


            else:

                pygame.draw.line(los,color,start_pos,point, 4)
                pygame.draw.rect(los,color,[point[0],point[1],10,10])
                text = debug_text.render(str(int(conv*(point[0]+camera_pos[0]))) +":" +   str(int(conv*(point[1]+camera_pos[1]))) + ":" + str(round(aids,3)), False, color)
                los.blit(text, (point[0] +10, point[1] +10))


        for aids in intersects_visible:
            point = intersects_visible[aids][0]

            pygame.draw.line(los,[255,0,0],start_pos,point)
            pygame.draw.rect(los,[255,0,0],[point[0],point[1],10,10])





    time_stamps["draw"] = time.time() - t
    #print(time_stamps)
    total = sum(time_stamps.values())
    #print("TOTAL:", total)

    walls = []
    draw_time = time.time() - start

    return los, draw_time
