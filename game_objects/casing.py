from values import *
from func import minus
import random
import math
class Casing:
    def __init__(self, app, screen, pos, angle):
        self.app = app
        self.screen = screen
        self.pos = pos
        self.angle = angle + random.uniform(-10,10)
        self.angV = 0
        self.height = random.randint(9,14)
        self.speed = random.uniform(1.5,3.5)
        self.vertSpeed = 0 

    def tick(self, map_d, camera_pos):


        

        radA = math.radians(self.angle)

        self.pos[0] += math.sin(radA) * self.speed
        self.pos[1] += math.cos(radA) * self.speed
        self.vertSpeed -= 0.2
        self.height += self.vertSpeed
        if self.height < 0:
            self.height = 0
            self.vertSpeed = -self.vertSpeed*0.6
            self.speed *= 0.9
            self.angV += 0.01
            self.angle += self.angV


        im = pygame.transform.rotate(casingIm, self.angle)

        if self.speed <= 0.1:
            s = map_d
            self.app.casings.remove(self)
            dPos = self.pos
        else:
            s = self.screen
            dPos = minus(self.pos, camera_pos, op="-")

        s.blit(im, dPos)

        
