import pygame
import numpy as np
import random
import func
from values import *

terminal2 = pygame.font.Font("texture/terminal.ttf", 30)

class UnitStatus:
    def __init__(self, screen, parent, text, color):
        self.parent = parent
        self.surface_perm = terminal2.render(text, False, color)
        self.angle = 0
        self.screen = screen
        self.velocity = [random.uniform(-2,2), -2]
        self.pos = func.minus(parent.pos.copy(), self.surface_perm.get_rect().center, op = "-")
        self.rotational_velocity = self.velocity[0]*-0.4
        self.lifetime = 30
        unitstatuses.append(self)

    def tick(self, camera_pos):
        mult = 1 if self.lifetime <= 25 else (self.lifetime-25)
        self.angle += self.rotational_velocity * mult
        surf_temp = pygame.transform.rotate(self.surface_perm, self.angle)

        if self.lifetime < 10:
            surf_temp.set_alpha(255*self.lifetime/20)
        rx, ry = surf_temp.get_rect().center
        self.pos = [self.pos[0] + self.velocity[0] * mult, self.pos[1] + self.velocity[1] * mult]
        pos = [self.pos[0] - rx, self.pos[1] - ry]
        self.screen.blit(surf_temp, func.minus(self.pos, camera_pos, op = "-"))
        self.lifetime -= timedelta.mod(1)
        self.velocity[0] *= 0.99
        self.velocity[1] *= 0.99
        self.rotational_velocity *= 0.99
        if self.lifetime < 0:
            unitstatuses.remove(self)
