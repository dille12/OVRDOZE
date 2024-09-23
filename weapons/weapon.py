import sys
import os.path
import core.func as func
from core.values import *


class Weapon:
    def __init__(
        self,
        name="weapon",
        price=100,
        damage=10,
        image="",
        hostile=False,
        sounds={"fire": weapon_fire_Sounds, "reload": reload},
        view=0.03,
        kind="unknown",
        energy_weapon=False,
    ):
        self.name = name
        self.price = price
        self.energy_weapon = energy_weapon
        self._damage = damage
        self._double_damage_time = 0
        self._weapon_fire_Tick = 0
        self.enemy_weapon = hostile
        self.hostile = hostile
        self.team = "hostile" if hostile else "friendly"
        self.kind = kind

        self.kind = "guns"

        self.sounds = sounds["fire"] if sounds["fire"] else "-"
        self.reload_sound = sounds["reload"]

        self.soundBank = sounds

        self._reload_tick = 0
        self._weapon_fire_Tick = 0

        self.image_file_name = image
        self.view = view
        self.image_directory = fp(f"texture/{self.kind}/{image}")
        if image != "":
            self.image = func.colorize(
                pygame.image.load(self.image_directory),
                pygame.Color(hud_color[0], hud_color[1], hud_color[2]),
            )

            self.image.set_alpha(100)

            self.image_non_alpha = func.colorize(
                pygame.image.load(self.image_directory),
                pygame.Color(255, 155, 155),
            )

            self.image_red = func.colorize(
                pygame.image.load(self.image_directory),
                pygame.Color(255, 0, 0),
            )

            self.image.set_alpha(200)

            temp = pygame.transform.scale(
                pygame.image.load(self.image_directory), [30, 10]
            ).convert_alpha()
            self.icon = func.colorize(
                temp, pygame.Color(hud_color[0], hud_color[1], hud_color[2])
            )
            # self.icon.set_alpha(100)
            self.icon_active = func.colorize(temp, pygame.Color(0, 255, 0))
            # self.icon_active.set_alpha(100)
            self.icon_no_ammo = func.colorize(temp, pygame.Color(255, 0, 0))
            self.icon_no_ammo.set_alpha(100)

            self.comparisonImage = func.colorize(load(self.image_directory, size = [135, 45]), pygame.Color(200,200,200))

            self.change_to_image = pygame.transform.scale(
                pygame.image.load(self.image_directory), [135, 45]
            ).convert_alpha()

            self.change_to_image = func.colorize(
                self.change_to_image, pygame.Color(hud_color[0], hud_color[1], hud_color[2])
            ).convert_alpha()

            self.change_to_image_no_ammo = func.colorize(
                self.change_to_image, pygame.Color(200,0,0)
            ).convert_alpha()

            self.change_to_image_set = []
            self.change_to_image_set_no_ammo = []
            for i in range(6):
                self.change_to_image.set_alpha((i+1)*100/6)
                self.change_to_image_set.append(self.change_to_image.copy())

                self.change_to_image_no_ammo.set_alpha((i+1)*100/6)
                self.change_to_image_set_no_ammo.append(self.change_to_image_no_ammo.copy())

    def set_hostile(self):
        self.team = "hostile"

    def get_string(self, kind):
        x = str(round(self.pos[0]))
        y = str(round(self.pos[1]))
        tx = str(round(self.target_pos[0]))
        ty = str(round(self.target_pos[1]))
        string = f"{kind}: {x}_{y}_{tx}_{ty}"

        return string

    def get_image(self):
        return self.image

    def get_reload_tick(self):
        return self._reload_tick

    def set_reload_tick(self, val):
        self._reload_tick = val

    def upgrade_damage(self):
        self._damage += 0.5

    def get_double_damage_time(self):
        return self._double_damage_time

    def double_damage(self, state):
        self._doubledamage_time = state

    def get_reload_rate(self):
        return self._reload_rate

    def weapon_tick(self):
        if self._reload_tick > 0:
            self._reload_tick -= timedelta.mod(1)
            if self._reload_tick < 0:
                self._reload_tick = 0
        if self._weapon_fire_Tick > 0:
            self._weapon_fire_Tick -= 1

    def add_weapon_fire_tick(self, v):
        self._weapon_fire_Tick += timedelta.tick(v)

    def weapon_fire_Tick(self):
        return self._weapon_fire_Tick

    def use(self):
        if isinstance(self.sounds, list):
            func.list_play(self.sounds)
        else:
            self.sounds.stop()
            self.sounds.play()
