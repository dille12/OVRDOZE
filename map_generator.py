import math
import pygame
import level
import classes
import func
from values import *

map_size = 30000, 20000
x_division = 10
screen = pygame.display.set_mode((900, 600))
clock = pygame.time.Clock()
terminal3 = pygame.font.Font(fp("texture/terminal.ttf"), 10)


scale = 900 / 30000

# random.seed(1000)


class building:
    def __init__(self, x, y, w, h):
        self.building_size_scale = 1000
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.w_2 = w * self.building_size_scale
        self.h_2 = h * self.building_size_scale
        self.rect = pygame.Rect(self.x, self.y, self.w_2, self.h_2)
        self.sectors = []

    def create_sectors(self):
        matrix_x = list(range(self.w))
        matrix_y = list(range(self.h))

        matrix = {}
        for aids in range(len(matrix_x)):
            print(aids)
            matrix[aids] = list(range(self.h))
        print(matrix)

        print("BUILDING SIZE:", self.w, self.h)

        adjacent_y = 0

        blocked_x = []
        while True:
            for y_1 in range(self.h):
                print("    ", end="")
                for aids in range(len(matrix)):
                    if y_1 in matrix[aids]:
                        print("X ", end="")
                    else:
                        print("O ", end="")
                print()

            keys = [key for key, value_ in matrix.items() if value_ != []]
            x = func.pick_random_from_list(keys)
            y = func.pick_random_from_list(matrix[x])

            print("ORIGIN", x, y)

            adjacent_x = 0
            for x_1 in range(x, self.w):

                if y in matrix[x_1]:
                    adjacent_x += 1
                else:
                    break

            print("adjacent_x:", adjacent_x)

            available = []
            limit_x = 50
            for y_1 in range(y, self.h):
                for x_2 in range(x, self.w):

                    if y_1 in matrix[x_2] and y_1 < limit_x:
                        print("APPENDING", [x_2, y_1], "LIMIT:", limit_x)
                        available.append([x_2, y_1])

                    else:
                        print("SKIPPING point", [x_2, y_1])
                        if limit_x > x_2:
                            print("Set new limit")
                            limit_x = x_2
                        break
            print("AVAILABLE SHAPES:", available)
            w, h = func.pick_random_from_list(available)
            print("SELECTED:", w, h)

            points = []
            print(x, y, w, h)
            for w_ in range(x, w + 1):
                for h_ in range(y, h + 1):
                    print(w_, h_)
                    points.append([w_, h_])

            print(points)

            for point in points:
                print("MATRIX:", matrix, "removing point", point)
                matrix[point[0]].remove(point[1])

                # if matrix[point[0]] == []:
                #     del matrix[point[0]]

            w = w - x + 1

            h = h - y + 1

            print("SECTOR:", [x, y, w, h], "\n\n")
            self.sectors.append(
                [
                    x * self.building_size_scale,
                    y * self.building_size_scale,
                    w * self.building_size_scale,
                    h * self.building_size_scale,
                ]
            )
            continual = all(value == [] for value in matrix.values())
            if continual:
                break

        print("Building sectorinit done.", len(self.sectors))

    def collision_check(self, x, y):
        print(x, y)
        if self.rect.collidepoint([x, y]):
            return True
        return False

    def return_rect(self):
        return self.rect


def check_closest_building(buildings, point):
    closest = 0
    for x in buildings:

        if not x.__dict__["x"] <= point <= x.__dict__["x"] + x.__dict__["w_2"]:
            continue

        height = x.__dict__["y"] + x.__dict__["h_2"]

        if height > closest:
            closest = height
            closest_b = x
    return closest


def generate():

    map_tiles = {}

    div_x = map_size[0] / x_division
    div_y = map_size[1] / x_division

    for x in range(x_division):
        map_tiles[x * div_x] = {}

        for y in range(x_division):
            if y * div_y > map_size[1]:
                continue
            map_tiles[x * div_x][y * div_y] = {
                "width": div_x,
                "height": div_y,
                "polygons": [],
                "objects": [],
            }

    print(map_tiles)

    buildings = []

    x = 10
    y = 10

    building_size_scale = 1000

    while True:
        building_size_x, building_size_y = random.randint(1, 4), random.randint(1, 4)

        if (
            building_size_x < 0
            or x + building_size_x * building_size_scale > map_size[0]
        ):
            print("next row")
            x = random.randint(1, 6) * 10

            y = check_closest_building(buildings, x) + 100
            print("CLOSEST:", y)

        else:
            x += building_size_x * building_size_scale + random.randint(5, 20) * 100
            y += random.randint(-2, 2) * 100
            y = max(y, 0)
            for b in buildings:
                if b.collision_check(x, y):
                    y_var = check_closest_building(buildings, x)
                    y += y_var + random.randint(1, 3) * 100
                    break

        if y + building_size_scale * building_size_y > map_size[1]:
            y = 10

        if x + building_size_scale * building_size_x > map_size[0]:
            x = 10

        bui = building(x, y, building_size_x, building_size_y)

        collided = any(
            bui.return_rect().colliderect(b.return_rect()) for b in buildings
        )

        if not collided:
            build = building(x, y, building_size_x, building_size_y)
            build.create_sectors()
            buildings.append(build)
            print(x, y)
        if len(buildings) > 40:
            break

    ### HIGHROADS

    return map_tiles, buildings


map_tiles, buildings = generate()

while True:
    screen.fill((0, 40, 0))
    for x in map_tiles:
        for y in map_tiles[x]:
            pygame.draw.rect(
                screen,
                [50, 50, 50],
                [
                    x * scale,
                    y * scale,
                    map_tiles[x][y]["width"] * scale,
                    map_tiles[x][y]["height"] * scale,
                ],
                1,
            )
    for x in buildings:

        pygame.draw.rect(
            screen,
            [255 / (len(x.__dict__["sectors"]) + 1), 255, 50],
            [
                x.__dict__["x"] * scale,
                x.__dict__["y"] * scale,
                x.__dict__["w_2"] * scale,
                x.__dict__["h_2"] * scale,
            ],
            1,
        )

        for xpos, ypos, w, h in x.__dict__["sectors"]:
            pygame.draw.rect(
                screen,
                [255, 0, 0],
                [
                    (x.__dict__["x"] + xpos) * scale,
                    (x.__dict__["y"] + ypos) * scale,
                    (w) * scale,
                    (h) * scale,
                ],
                1,
            )
        text = terminal3.render(str(len(x.__dict__["sectors"])), False, [255, 255, 255])
        screen.blit(text, (x.__dict__["x"] * scale, x.__dict__["y"] * scale))  #

        # for x_line in range(x.__dict__["w"]):
        #     if x_line == 0:
        #         continue
        #     x_line *= x.__dict__["building_size_scale"]
        #     pygame.draw.line(screen, [255,0,0], [(x.__dict__["x"] + x_line)*scale, x.__dict__["y"]*scale], [(x.__dict__["x"] + x_line)*scale, (x.__dict__["y"] + x.__dict__["h_2"])*scale], 3)
        #
        # for y_line in range(x.__dict__["h"]):
        #     if y_line == 0:
        #         continue
        #     y_line *= x.__dict__["building_size_scale"]
        #     pygame.draw.line(screen, [255,0,0], [(x.__dict__["x"])*scale, (x.__dict__["y"]+ y_line)*scale], [(x.__dict__["x"]+ x.__dict__["w_2"])*scale, (x.__dict__["y"]+ y_line)*scale], 3)

    pygame.display.update()
    clock.tick(60)
