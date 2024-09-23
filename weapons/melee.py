import math
from core.values import *


class Melee:
    def __init__(
        self,
        mp=False,
        strike_count=2,
        damage=10,
        hostile=True,
        owner_object=None,
        strike_range=150,
    ):
        self.owner = owner_object
        self.mp = mp
        self.arc = 1 * math.pi
        self.strike_range = strike_range  # what's a good melee range number? - lets see if we can't make this more adjustable  ## The attack distance for zombies is 100, so at least 150
        self.strikes_used = 0
        self.strikes = strike_count
        self.damage = damage
        self.owner.stamina = 0

    def get_string(self):
        return super().get_string("MEELE")

    def check_for_strike(self, r_click):
        if r_click == True and self.owner.stamina < self.strikes:  ##FIRE
            return True
        else:
            return False

    def tick(self, screen, r_click):

        pos = tuple(self.owner.get_pos())
        angle = self.owner.get_angle()

        if self.check_for_strike(r_click):
            melee_sound.stop()
            melee_sound.play()
            melee_list.append(
                {
                    "pos": pos,
                    "angle": angle,
                    "damage": self.damage,
                    "strike_range": self.strike_range,
                    "arc": self.arc,
                }
            )  # BULLET
            self.owner.stamina += 1
        


