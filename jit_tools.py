from numba import jit
import numpy as np
import time
import random
import math

#@jit(nopython = True)
def filter_walls_jit(walls, walls2, cam_array, size):
    for i in walls:
        if check_wall_np(i, cam_array, size):
            walls2 = np.append(walls2, [i], axis = 0)

    return walls_generate_np(walls2, cam_array)

@jit(nopython = True)
def walls_generate_np(walls_filtered, cam_array):
    for line in walls_filtered:
        line[0:2] -= cam_array
        line[2:4] -= cam_array
    return walls_filtered

@jit(nopython = True)
def check_wall_np(wall, cam_array, size):
    check = check_point(wall[0:2] - cam_array, size) or check_point(wall[2:4] - cam_array, size)
    return check

@jit(nopython = True)
def check_point(point, size):
    check = 0 < point[0] < size[0] and 0 < point[1] < size[1]
    return check

@jit(nopython=True)
def get_dist_points_jit(point_1, point_2):
    return math.sqrt((point_2[0] - point_1[0]) ** 2 + (point_2[1] - point_1[1]) ** 2)

@jit(nopython=True)
def get_wall_angles(s_np, walls, angle_array):
    i = 0
    for line in walls:
        p1 = line[0:2]
        p2 = line[2:4]
        angle1 = math.atan2(p1[1] - s_np[1], p1[0] - s_np[0])
        angle2 = math.atan2(p2[1] - s_np[1], p2[0] - s_np[0])

        if angle1 < 0:
            angle1 += math.pi * 2

        if angle2 < 0:
            angle2 += math.pi * 2

        center = (p1+p2)/2

        dist = get_dist_points_jit(center, s_np)

        angle_array[i, 0] = p1[0]
        angle_array[i, 1] = p1[1]
        angle_array[i, 2] = angle1
        angle_array[i, 3] = p2[0]
        angle_array[i, 4] = p2[1]
        angle_array[i, 5] = angle2
        angle_array[i, 6] = dist
        angle_array[i, 7] = 1

        i += 1

    return angle_array

@jit(nopython = True)
def intersect_jit(A, B, C, D):
    return ccw_jit(A, C, D) != ccw_jit(B, C, D) and ccw_jit(A, B, C) != ccw_jit(A, B, D)

@jit(nopython = True)
def ccw_jit(A, B, C):
    return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])

@jit(nopython=True)
def check_visible_points(start, i_array, angle_array):
    for line in i_array:

        a, x, y, value = line

        x_n = x - math.cos(a)*5
        y_n = y - math.sin(a)*5



        pos = np.array([x_n,y_n])

        visible = True
        for wall in angle_array:
            x1, y1, a1, x2, y2, a2, dist, value = wall

            if (x1 == pos[0] and y1 == pos[1]) or (x2 == pos[0] and y2 == pos[1]):
                #print("SAME WALL")
                continue

            if intersect_jit(start, pos, np.array([x1,y1]), np.array([x2,y2])) == True:
                visible = False
                #print("Wall", x1, "-", x2, "x and", y1, "-", y2, "y intersected ray", a)
                break

        if visible == False:
            line[-1] = 0


    return i_array






@jit(nopython=True)
def re_arrange(new_array, angle_array):
    i = 0
    for line in angle_array:
        x1, y1, a1, x2, y2, a2, dist, value = line

        while a1 < 0:
            a1 += math.pi * 2

        new_array[i, 0] = a1
        new_array[i, 1] = x1
        new_array[i, 2] = y1
        new_array[i, 3] = 1

        while a2 < 0:
            a2 += math.pi * 2

        new_array[i+1, 0] = a2
        new_array[i+1, 1] = x2
        new_array[i+1, 2] = y2
        new_array[i+1, 3] = 1

        i+=2

    return new_array

@jit(nopython=True)
def det(a, b):
    return a[0] * b[1] - a[1] * b[0]



@jit(nopython=True)
def line_intersection(A, B, C, D):
    xdiff = (A[0] - B[0], C[0] - D[0])
    ydiff = (A[1] - B[1], C[1] - D[1])

    div = det(xdiff, ydiff)
    if div == 0:
        return False, False

    d = (det(A, B), det(C, D))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y

@jit(nopython=True)
def calc_triangles(s_np, triangle_array, individual_angle_array, angle_array):

    row = -1

    for line in triangle_array:
        line[7] = 2500
        line[3] = 2500

    for i, line in enumerate(triangle_array):
        for n in (0,4):

            angle = line[n]
            x = math.cos(angle) * 2500 + s_np[0]
            y = math.sin(angle) * 2500 + s_np[1]
            pos = np.array([x,y])

            line[n+1] = x
            line[n+2] = y

            for wall in angle_array:

                pos = line[n+1:n+2]

                if wall[-1] == 0:
                    continue

                x1, y1, a1, x2, y2, a2, dist, value = wall

                p1, p2 = np.array([x1,y1]), np.array([x2,y2])

                if intersect_jit(s_np, pos, p1, p2) == True:
                    point = line_intersection(s_np, pos, p1, p2)
                    if point == (False, False):
                        continue

                    line[n+1] = point[0]
                    line[n+2] = point[1]
                    line[n+3] = dist
    return triangle_array




@jit(nopython=True)
def filter_out_non_visible_walls(angle_array):


    for line in angle_array:
        x1, y1, a1, x2, y2, a2, dist, value = line

        if line[7] == 0:
            continue
        if get_angle_diff_jit(line[2], line[5]) < get_angle_diff_jit(line[5], line[2]):
            angle1 = line[2]
            angle2 = line[5]
        else:
            angle1 = line[5]
            angle2 = line[2]

        diff1 = get_angle_diff_jit(angle1, angle2)



        for line2 in angle_array:

            if line2[7] == 0:
                continue

            if line2[6] < line[6]:
                continue

            good_point = False
            for i in range(8):
                if line[i] != line2[i]:
                    good_point = True
                    break

            if good_point == False:
                continue





            if get_angle_diff_jit(line2[2], line2[5]) < get_angle_diff_jit(line2[5], line2[2]):
                angle3 = line2[2]
                angle4 = line2[5]
            else:
                angle3 = line2[5]
                angle4 = line2[2]

            diff2 = get_angle_diff_jit(angle1, angle3)
            diff3 = get_angle_diff_jit(angle1, angle4)

            if 0 <= diff2 <= diff1 and 0 <= diff3 <= diff1:
                line2[7] = 0


@jit(nopython=True)
def get_angle_diff_jit(angle1, angle2):
    angle1 = math.degrees(angle1)
    angle2 = math.degrees(angle2)
    anglediff = (angle1 - angle2 + 360) % 360
    return math.radians(anglediff)









if __name__ == '__main__':

    a = np.array([0,0])
    b = np.array([5,0])
    c = np.array([3,2])
    d = np.array([2,-2])

    print(line_intersection(a,b,c,d))

    size = np.array([854, 480])

    walls = np.empty((0,4), int)

    for i in range(400):
        walls = np.append(walls,
            [[random.randint(-100, 100), random.randint(-100, 100), random.randint(-100, 100), random.randint(-100, 100)]],
            axis = 0
        )

    walls2 = np.empty((0,4), int)
    cam_array = np.array([5,5])

    for i in range(100):
        t = time.perf_counter()
        w = filter_walls_jit(walls, walls2, cam_array, size)
        print(w, time.perf_counter() - t)
