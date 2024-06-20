import random
from values import *
import func
import math
import pygame

class powerWashParticle:
    def __init__(self, app, pos, angle, velocity):
        self.app = app
        self.pos = pos
        self.angle = math.radians(angle)
        self.height = 0.6
        self.bounce = 0.4
        self.size2 = random.randint(6,12)
        self.lifetime = 20
        velocity *= random.uniform(4.5,6)
        self.velocity = velocity
        self.velocityAtStart = velocity
        self.lastPoses = []
        self.colorMod = None


    def drawTrail(self, camera_pos):


        self.lastPoses.append(self.pos.copy())
        if len(self.lastPoses) > round(3 / timedelta.timedelta):
            self.lastPoses.remove(self.lastPoses[0])

        LP = None
        for i in range(len(self.lastPoses)):
            pos = self.lastPoses[i]

            DP = func.draw_pos(pos.copy(), camera_pos)

            if LP:
                pygame.draw.aaline(screen, [52, 210, 235], DP, LP)
            LP = DP.copy()

    def tick(self, screen, camera_pos, map):
           

        self.pos[0] += math.cos(self.angle) * self.velocity * timedelta.timedelta
        self.pos[1] -= math.sin(self.angle) * self.velocity * timedelta.timedelta

        self.size = 3*((self.velocity/self.velocityAtStart)**0.4)

        rect = pygame.Rect(self.pos[0] - self.size, self.pos[1] - self.size, self.size, self.size)

        self.height -= 0.6 * timedelta.timedelta
        if self.height < 0:
            self.height = self.bounce
            self.bounce *= 0.9
            self.velocity *= 0.9

            
            rect2 = rect.copy()
            rect2.inflate_ip(25, 25)

            xi = rect2.x
            yi = rect2.y

            colorMod = map.bloodPoints[round(self.pos[0]/BLOODSINK_TILESIZE), round(self.pos[1]/BLOODSINK_TILESIZE)] 
            colorMod *= 10
            colorMod = min(colorMod, 1)
            for i in range(3):
                SecondaryParticle(self.app, self.pos.copy(), self.angle, 8, hierarchy=2, colorMod=colorMod)


            for i in range(5):
                rX = random.randint(-5, 5)
                rY = random.randint(-5, 5)
                rect2.x = xi + rX
                rect2.y = yi + rY
                self.app.map_render.blit(map.map_rendered_alpha_PW, [rect2.x, rect2.y], rect2)
                map.bloodPoints[round((rect2.x+rect.w/2)/BLOODSINK_TILESIZE), round((rect2.y+rect.h/2)/BLOODSINK_TILESIZE)] *= 0.6


        drawPos = func.draw_pos(self.pos, camera_pos)

        rect.x = drawPos[0]
        rect.y = drawPos[1]

        self.drawTrail(camera_pos)

        pygame.draw.rect(screen, [52, 210, 235], rect)

        if self.velocity < 2*self.velocityAtStart/3:
            particle_list.remove(self)


class SecondaryParticle:
    def __init__(self, app, pos, angle, velocity, hierarchy = 0, colorMod = None):
        self.app = app
        self.pos = pos
        self.pos[0]+=random.randint(-5,5)
        self.pos[1]+=random.randint(-5,5)
        self.angle = angle + random.uniform(-2, 2)
        particle_list.append(self)
        self.height = 1
        self.velocity = velocity
        self.velocityAtStart = velocity
        self.size = 8
        self.bounceBack = 0.8
        self.s = pygame.Surface((self.size, self.size)).convert()
        self.hierarchy = hierarchy
        self.spawnedchildren = False
        self.colorMod = colorMod
        self.colorIntensity = random.uniform(0.5, 0.8)

    def tick(self, screen, camera_pos, map):
        
        

        
        self.height -= 0.2

        if self.height < 0:
            self.height = self.bounceBack
            self.bounceBack *= 0.8
            self.velocity *= 0.8
            self.colorIntensity *= 0.75
            if self.hierarchy > 0 and not self.spawnedchildren:
                for i in range(2):
                    SecondaryParticle(self.app, self.pos.copy(), self.angle, self.velocity*0.2, hierarchy=self.hierarchy-1, colorMod=self.colorMod)
                self.spawnedchildren = True

        self.pos[0] += math.cos(self.angle) * self.velocity * timedelta.timedelta
        self.pos[1] -= math.sin(self.angle) * self.velocity * timedelta.timedelta
        c = [10 + 37*self.colorMod, 42-42*self.colorMod, 47-47*self.colorMod]
        for i in range(3):
            c[i] *= self.colorIntensity
        self.s.fill(c)
        drawPos = func.draw_pos(self.pos, camera_pos)

        screen.blit(self.s, drawPos, None, pygame.BLEND_RGB_ADD)

        if self.velocity < 2*self.velocityAtStart/3:
            particle_list.remove(self)
        
        



