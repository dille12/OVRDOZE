import sys
import os.path
import func
from values import *
class Weapon:
    def __init__(
            self,
            name="weapon", 
            damage=10,
            image = "", 
            hostile = False,
            sounds = {"fire": weapon_fire_Sounds, "reload":reload }, 
            view = 0.03,
            kind = "unknown"
        ):
        self.name = name
        self._damage = damage
        self._double_damage_time = 0
        self._weapon_fire_Tick = 0
        self.enemy_weapon = hostile
        self.team = "hostile" if hostile else "friendly"
        self.kind = kind;

        self.sounds = sounds["fire"] if sounds["fire"] else "-"
        self.reload_sound = sounds["reload"]

        self._reload_tick = 0
        self._weapon_fire_Tick = 0

        self.image_file_name = image
        self.view = view
        self.image=None;
        if image != "":

            self.image = func.colorize(
                pygame.image.load(f"texture/{self.kind}/{image}"), 
                pygame.Color(hud_color[0], hud_color[1], hud_color[2]))
            print("Image loaded")

    def set_hostile(self):
        self.team = "hostile"

    def get_image(self):
        return self.image

    def get_reload_tick(self):
        return self._reload_tick
    def set_reload_tick(self,val):
        self._reload_tick=val
    def upgrade_damage(self):
        self._damage += 0.5


    def get_double_damage_time(self):
        return self._double_damage_time;
    def double_damage(self, state):
        self._doubledamage_time = state
    def get_reload_rate(self):
        return self._reload_rate
    def weapon_tick(self):
        if self._reload_tick != 0:
            self._reload_tick -= 1
        if self._weapon_fire_Tick > 0:
            self._weapon_fire_Tick -= 1
    def add_weapon_fire_tick(self,v):
        self._weapon_fire_Tick+=v

    def weapon_fire_Tick(self):
        return self._weapon_fire_Tick
    def use(self):
        func.list_play(self.sounds)

