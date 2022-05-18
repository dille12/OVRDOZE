import os, sys
import math
import random
import func
from values import *

class Game_Object:
    def __init__(self,name,pos,hostile,angle,damage,_friendly_fire=False,lifetime=100):
        self.name=name;
        self._pos = pos.copy()
        self.hostile=hostile;
        self.team="hostile" if hostile else "friendy"
        self._angle = angle
        self._angle_radians = math.radians(self._angle) + math.pi/2
        self._damage = damage
        self._friendly_fire=_friendly_fire
        self.actors_hit = []
        self.lifetime = lifetime

        rotated_image = pygame.transform.rotate(obj, self._angle)
        new_rect = rotated_image.get_rect(center = bullet.get_rect(center = self._pos).center)
        self._pos = [new_rect[0],new_rect[1]]
    def update_life(self,kind_list):
        self.lifetime -= 1
        if self.lifetime == 0:
            print("Bullet deleted")
            kind_list.remove(self)
            return

    def get_string(self,kind):
        k= kind;
        x= str(round(self._pos[0]))
        y= str(round(self._pos[1]))
        a=str(round(self._angle))
        d=str(round(self._damage))
        s=str(round(self.speed))
        string = f'{k}:{x}_{y}_{a}_{d}_{s}'
        return string


