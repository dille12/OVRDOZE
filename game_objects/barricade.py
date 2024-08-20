# how to normalize this more to a game object?
from game_objects.game_object import Game_Object
import level
from values import *
import numpy as np
import jit_tools
import func
import los

tolerance = 10

defaultBarricadeHealth = 2500

class Barricade(Game_Object):
    def __init__(self, origin, pygame):
        super().__init__(
            name="barricade", pos=origin, lifetime=100, texture=barricade_texture
        )
        self.pos = origin
        self.ref = pygame
        self.hp = defaultBarricadeHealth
        self.blink_tick = 1

        self.maxLength = 100 * multiplier2

        self.stage = "building_1"

    def build(self, x, y, w, h, map):
        self.width = w
        self.height = h
        self.stage = "built"
        self.pos = [x + camera_pos[0], y + camera_pos[1]]
        self.rect = self.ref.Rect(
            self.pos[0], self.pos[1], self.width, self.height
        )

        self.surf = self.ref.Surface([w, h]).convert()

        for x in range(round(w / 100 + 0.49)):
            for y in range(round(h / 100 + 0.49)):
                self.surf.blit(
                    barricade_texture,
                    [x * 100, y * 100],
                    area=[0, 0, self.width, self.height],
                )
                print("BLITTED IN:", x, y)

        map.rectangles.append(self.rect)
        map.barricade_rects.append([self.rect, self])

        print(map.barricade_rects)

        turret_pickup.stop()
        turret_pickup.play()

        return True


    def tick(self, screen, camera_pos, mouse_pos=[0, 0], clicked=False, map=None):
        self.blink_tick += timedelta.mod(0.25)
        if self.blink_tick > 4:
            self.blink_tick = 1
        if self.hp <= 0:
            map.__dict__["rectangles"].remove(self.rect)
            map.__dict__["barricade_rects"].remove([self.rect, self])
            return "KILL"

        if self.stage == "building_1":
            x = mouse_pos[0] + camera_pos[0]
            y = mouse_pos[1] + camera_pos[1]
            
            detectPoints = []
            for x1 in [-1, 1]:
                detectPoints.append([x + x1*self.maxLength, y])

            for y1 in [-1, 1]:
                detectPoints.append([x, y + y1*self.maxLength])

            detectPoints = np.array(detectPoints)
            xy = np.array([x, y])
            closestWalls = [False, False, False, False]
            for i in range(detectPoints.shape[0]):
                xy2 = detectPoints[i]

                minDist = self.maxLength
                
                for i2, w in enumerate(map.numpy_array_wall_los):

                    if not los.intersect_jit(xy, xy2, w[0:2], w[2:4]):
                        continue

                    point = jit_tools.line_intersection(xy, xy2, w[0:2], w[2:4])
                    if point != (False, False):
                        
                        d = func.get_dist_points([x, y], point)

                        if d < minDist:

                            closestWalls[i] = point
                            minDist = d

            if closestWalls[0] and closestWalls[1]:
                self.ref.draw.line(
                    screen, [255, 204, 0], [closestWalls[0][0] - camera_pos[0], closestWalls[0][1] - camera_pos[1]-5], [closestWalls[1][0] - camera_pos[0], closestWalls[1][1] - camera_pos[1]-5], 3
                )
                self.ref.draw.line(
                    screen, [255, 204, 0], [closestWalls[0][0] - camera_pos[0], closestWalls[0][1] - camera_pos[1]+5], [closestWalls[1][0] - camera_pos[0], closestWalls[1][1] - camera_pos[1]+5], 3
                )

                canBuild = True

                pos = [closestWalls[0][0], closestWalls[0][1]-10, closestWalls[1][0] - closestWalls[0][0], 20]
                
            elif closestWalls[2] and closestWalls[3]:
                self.ref.draw.line(
                    screen, [255, 204, 0], [closestWalls[2][0] - camera_pos[0]-5, closestWalls[2][1] - camera_pos[1]], [closestWalls[3][0] - camera_pos[0]-5, closestWalls[3][1] - camera_pos[1]], 3
                )
                self.ref.draw.line(
                    screen, [255, 204, 0], [closestWalls[2][0] - camera_pos[0]+5, closestWalls[2][1] - camera_pos[1]], [closestWalls[3][0] - camera_pos[0]+5, closestWalls[3][1] - camera_pos[1]], 3
                )
                canBuild = True

                pos = [closestWalls[2][0]-10, closestWalls[2][1], 20, closestWalls[3][1] - closestWalls[2][1]]

            else:
                canBuild = False
                        




            self.ref.draw.circle(
                screen, [0, 204, 0], [x - camera_pos[0], y - camera_pos[1]], 2
            )

            if clicked and canBuild:
                self.pos = pos
                x,y,w,h = pos
                return self.build(x, y, w, h, map)
            else:
                return "revert" if clicked else False

        elif self.stage == "building_2":

            w = round((mouse_pos[0] + camera_pos[0])/tolerance)*tolerance - self.pos[0]
            h = round((mouse_pos[1] + camera_pos[1])/tolerance)*tolerance - self.pos[1]

            x = self.pos[0] - camera_pos[0]
            y = self.pos[1] - camera_pos[1]

            if w < 0:
                x += w
                w = abs(w)

            if h < 0:
                y += h
                h = abs(h)

            area = w * h

            if area > 5000 * (multiplier2 ** 2) or w < 20 * multiplier2 or h < 20 * multiplier2:
                clear = False
                color = [204, 0, 0]
            else:
                clear = True
                color = [0, 204, 0]

            rect_1 = self.ref.Rect(x, y, w, h)

            rect_2 = self.ref.Rect(x + camera_pos[0], y + camera_pos[1], w, h)

            collisions = list(
                level.getcollisions(map.__dict__["rectangles"], rect_2)
            )
            if collisions:
                clear = False
                color = [204, 0, 0]

            self.ref.draw.rect(screen, color, rect_1, 3)

            if clicked and clear:
                return self.build(x, y, w, h, map)

            else:
                return "revert" if clicked else False

        else:
            screen.blit(
                self.surf, [self.pos[0] - camera_pos[0], self.pos[1] - camera_pos[1]]
            )  #
            # pygame.draw.rect(screen, [61, 61, 41], pygame.Rect(self.pos[0]-camera_pos[0], self.pos[1]-camera_pos[1], self.width, self.height))
            pygame.draw.rect(
                screen,
                [
                    round(((defaultBarricadeHealth - self.hp) / defaultBarricadeHealth) * 255),
                    round((self.hp / defaultBarricadeHealth) * 255),
                    0,
                ],
                pygame.Rect(
                    self.pos[0] - camera_pos[0],
                    self.pos[1] - camera_pos[1],
                    self.width,
                    self.height,
                ),
                round(self.blink_tick),
            )
            pygame.draw.rect(
                screen,
                [0, 0, 0],
                pygame.Rect(
                    self.pos[0] - camera_pos[0],
                    self.pos[1] - camera_pos[1],
                    self.width,
                    self.height,
                ),
                1,
            )
