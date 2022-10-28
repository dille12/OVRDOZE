# how to normalize this more to a game object?
from game_objects.game_object import Game_Object
import level
from values import *

tolerance = 10

class Barricade(Game_Object):
    def __init__(self, origin, pygame):
        super().__init__(
            name="barricade", pos=origin, lifetime=100, texture=barricade_texture
        )
        self.pos = origin
        self.ref = pygame
        self.hp = 1000
        self.blink_tick = 1

        self.stage = "building_1"

    def tick(self, screen, camera_pos, mouse_pos=[0, 0], clicked=False, map=None):
        self.blink_tick += timedelta.mod(0.25)
        if self.blink_tick > 4:
            self.blink_tick = 1
        if self.hp <= 0:
            map.__dict__["rectangles"].remove(self.rect)
            map.__dict__["barricade_rects"].remove([self.rect, self])
            return "KILL"

        if self.stage == "building_1":
            x = round((mouse_pos[0] + camera_pos[0])/tolerance)*tolerance
            y = round((mouse_pos[1] + camera_pos[1])/tolerance)*tolerance
            self.ref.draw.circle(
                screen, [0, 204, 0], [x - camera_pos[0], y - camera_pos[1]], 5
            )

            if clicked:
                self.pos = [x, y]
                self.stage = "building_2"

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

                map.__dict__["rectangles"].append(self.rect)
                map.__dict__["barricade_rects"].append([self.rect, self])

                print(map.__dict__["barricade_rects"])

                return True
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
                    round(((1000 - self.hp) / 1000) * 255),
                    round((self.hp / 1000) * 255),
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
