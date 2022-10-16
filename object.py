from game_objects.bullet import Bullet
from anim_list import *
from values import *
#from weapons.area import Explosion


class Obj:
    def __init__(self):
        self.bullet = Bullet
        self.Explosion = Explosion

    def create_explosion(self):
        explosions.append(Explosion(self._pos, expl1))

    def create_shrapnel(self):
        bullet_list.append(
            Bullet.Bullet(
                self.pos,
                random.uniform(0, 360),
                15,
                hostile=True,
                speed=15,
                piercing=False,
            )
        )
