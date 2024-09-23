import os, sys
import math
import random
import core.func as func
from core.values import *
from utilities.anim_list import *
from networking.server_object import MP_Object


class Game_Object(MP_Object):
    def __init__(
        self,
        name="obj",
        pos=[0, 0],
        hostile=False,
        angle=0,
        damage=0,
        friendly_fire=False,
        lifetime=100,
        texture=None,
    ):
        super().__init__()
        self.name = name
        self._pos = pos.copy()
        self.hostile = hostile
        self.team = "hostile" if hostile else "friendy"
        self._angle = angle
        self._angle_radians = math.radians(self._angle) + math.pi / 2
        self._damage = damage
        self._friendly_fire = friendly_fire
        self.actors_hit = []
        self._lifetime = lifetime

        if name != "bullet":

            rotated_image = pygame.transform.rotate(texture, self._angle)
            new_rect = rotated_image.get_rect(
                center=texture.get_rect().center
            )
            self._pos = [pos[0] - new_rect[0], pos[1] - new_rect[1]]

    def create_explosion(self):
        #explosions.append(Explosion(self._pos, expl1))
        pass

    def update_life(self, kind_list):
        self._lifetime -= timedelta.mod(1)
        if self._lifetime < 0:
            kind_list.remove(self)
            return

    def get_string(self, kind):
        k = kind
        x = str(round(self._pos[0]))
        y = str(round(self._pos[1]))
        a = str(round(self._angle))
        d = str(round(self._damage))
        s = str(round(self.speed))
        string = f"{k}:{x}_{y}_{a}_{d}_{s}"
        return string

    def clean_up(self, l):
        try:
            l.remove(self)
        except:
            print("Not in list")
