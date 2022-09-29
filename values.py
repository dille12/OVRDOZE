import os, sys
import pygame
import math
import random
import time
import mixer
from screeninfo import get_monitors
import get_preferences

a, a, a, a, a, a, a, a, size = get_preferences.pref()


print("VALUE INIT")
pygame.init()
pygame.mixer.init()
los_tick = 10
multi_kill = 0
camera_pan = 0.03
respawn_ticks = 0

try:
    monitors = get_monitors()
    m = monitors[0]
    # get first in list or primary if set
    for n in monitors:
        if n.is_primary == True:
            m = n
            break

    print(m)

    fs_size = (m.width, m.height)
except:
    fs_size = (1920, 1080)

#size = 1366, 768
#size = 854, 480
#size = 1920, 1080
multi_kill_ticks = 0
multiplier = 1920 / size[0]
multiplier2 = size[0] / 854
pygame.init()
screen = pygame.display.set_mode(size)
icon = pygame.image.load("texture/icon.png")
pygame.display.set_caption("OVRDOZE")
pygame.display.set_icon(icon)
pygame.display.update()
tick_count = 60
player_pos = [50, 50]
camera_pos = [0, 0]
player_hp = 100
x_vel = 0
y_vel = 0
last_bullet_list = ()

enemy_count = 0
multiplayer = False


def set_multiplayer(arg):
    global multiplayer
    multiplayer = arg
    print("MULTIPLAYER=", multiplayer)


WHITE_COLOR = [255, 255, 255]
CYAN_COLOR = (0, 255, 255)
PURPLE_COLOR = (255, 0, 255)
RED_COLOR = [255, 0, 0]
BLACK = [0, 0, 0]
turret_list = []
enemy_list = []
bullet_list = []
meele_list = []
particle_list = []
grenade_list = []
kill_counter = []
explosions = []
burn_list = []
melee_list = []
zombie_events = []
npcs = []
interactables = []
loading_cue = []
turret_bro = []

last_hp = 0
free_tick = 0
last_text_i = 0
kills = 0
Inventory_open = False
tab_pressed = False


def get_Sound(sound, file):
    path = file + "/" + sound + ".wav"
    print(path)
    return pygame.mixer.Sound(path)


def rgb_image_load(image_dir):
    list = [pygame.image.load(image_dir)]
    for color in [
        pygame.Color(255, 0, 0),
        pygame.Color(0, 255, 0),
        pygame.Color(0, 0, 255),
    ]:
        image = colorize(list[0], color)
        list.append(image)

    return list


def rgb_convert(image):
    list = [image]
    for color in [
        pygame.Color(255, 0, 0),
        pygame.Color(0, 255, 0),
        pygame.Color(0, 0, 255),
    ]:
        image = colorize(list[0], color)
        list.append(image)

    return list


def colorize(image, newColor):
    """
    Create a "colorized" copy of a surface (replaces RGB values with the given color, preserving the per-pixel alphas of
    original).
    :param image: Surface to create a colorized copy of
    :param newColor: RGB color to use (original alpha values are preserved)
    :return: New colorized Surface instance
    """
    image = image.copy()

    # zero out RGB values
    image.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
    # add in new RGB values
    image.fill(newColor[0:3] + (0,), None, pygame.BLEND_RGBA_ADD)
    print("colorized")

    return image


def get_sound_Variants(folder, name2):
    list = []
    i = 1
    while True:
        try:
            name = name2 + str(i)
            list.append(get_Sound(name, folder))
            i += 1

        except:
            return list



def load(image, size = None, alpha = True, double = False):
    temp = pygame.image.load(image)
    if size:
        x,y = size
    else:
        x,y = temp.get_size()


    im = pygame.transform.scale(
        temp,
        [round(x * multiplier2), round(y * multiplier2)] if not size else [round(x / multiplier), round(y / multiplier)],
    )

    im = im.convert_alpha() if alpha else im.convert()

    return im

def load_alpha(image):

    temp = pygame.image.load(image)

    x,y = temp.get_size()

    im = pygame.transform.scale(
        temp,
        [round(x / multiplier), round(y / multiplier)],
    ).convert_alpha()
    return im


multikill_fonts = []
for i in range(5):
    font_s = 50 + i * 15
    multikill_fonts.append(pygame.font.Font("texture/agencyb.ttf", round(font_s)))

terminal_kill_counter = pygame.font.Font("texture/terminal.ttf", 40)
kill_counter_texts = {}
for x in range(10, 101):
    image_list = []
    for color in [[255, 255, 255], [255, 0, 0], [0, 255, 0], [0, 0, 255]]:
        text = terminal_kill_counter.render("x" + str(x), False, color)
        image_list.append(text)
    kill_counter_texts[x] = image_list

kill_rgb = rgb_image_load("texture/kill.png")
menu_rgb = rgb_image_load("texture/menu_image.png")

packet_dict = {}
player = load("texture/player.png", size = [180,119])

player_pistol = load("texture/player_pistol.png", size = [180,119])

zombie = load("texture/zombie.png", size = [119,119])

bomber = load("texture/bomber.png", size = [150,150])

zombie_big = load("texture/zombie.png", size = [200,200])

bullet_texture = load("texture/bullet.png", size = [15,4])

y_size = bullet_texture.get_size()[1]

bullet_length = []
for x in range(100):
    x += 5
    bullet_length.append(
        pygame.transform.scale(
            pygame.image.load("texture/bullet.png"), (round(x * multiplier2), round(4*multiplier2))
        ).convert_alpha()
    )

lazer_texture = load("texture/lazer.png", size = [15,8])
y_size = lazer_texture.get_size()[1]


energy_bullet_length = []
for x in range(100):
    x += 5
    energy_bullet_length.append(
        pygame.transform.scale(
            pygame.image.load("texture/lazer.png"), (round(x * multiplier2), round(8*multiplier2))
        ).convert_alpha()
    )



grenade_throw = False
grenade = load("texture/items/grenade.png", size = [30,30])
molotov = load("texture/items/molotov.png", size = [40,40])

molotov_explode_sound = pygame.mixer.Sound("sound/molotov.wav")
molotov_pickup = pygame.mixer.Sound("sound/molotov_pickup.wav")
drug_use = pygame.mixer.Sound("sound/drug_use.wav")

melee_sound = pygame.mixer.Sound("sound/sfx/melee.wav")
melee_hit_sound = pygame.mixer.Sound("sound/sfx/melee_hit.wav")

bullet_pickup = pygame.mixer.Sound("sound/bullet.wav")
grenade_pickup = pygame.mixer.Sound("sound/grenade_pickup.wav")
needle_pickup = pygame.mixer.Sound("sound/needle_pickup.wav")
pill_pickup = pygame.mixer.Sound("sound/pill_pickup.wav")
turret_pickup = pygame.mixer.Sound("sound/turret_pickup.wav")
sniff_sound = pygame.mixer.Sound("sound/sinff.wav")
info = pygame.image.load("texture/info.png").convert_alpha()

hud_color = [255, 255, 255]


not_used_weapons = []

player_weapons = []


class TimeDelta:
    def __init__(self):
        self.timedelta = 1

    def tick(self, am):
        return round(am / self.timedelta)

    def mod(self, am):
        return am * self.timedelta

    def exp(self, am):
        return am**self.timedelta

    def exp_rev(self, am):
        return am ** (1 / self.timedelta)


timedelta = TimeDelta()


class GameTick:
    def __init__(self, max_value=30, oneshot=False):
        self.value = 0
        self.max_value = max_value
        self.oneshot = oneshot

    def tick(self):
        if self.value < self.max_value:
            self.value += timedelta.mod(1)
        if self.value < self.max_value:
            return False
        else:
            if not self.oneshot:
                self.value = 0
            return True

    def rounded(self):
        return round(self.value)


dialogue = []
dialogue_tick = GameTick(40)

money_tick = GameTick(35, oneshot=True)


last_hp = 0
damage_ticks = 0

inv_click = pygame.mixer.Sound("sound/inv_click.wav")
inv_open = pygame.mixer.Sound("sound/inv_open.wav")
inv_close = pygame.mixer.Sound("sound/inv_close.wav")

mov_turret_base = load("texture/movingturret_base.png", size = [70,70])
mov_turret_gun = load("texture/movingturret_gun.png", size = [70,70])

mov_fire = pygame.mixer.Sound("sound/mov_turret_fire.wav")

turret_leg = load("texture/turret_leg.png", size = [70,70])
turret = load("texture/turret.png", size = [70,70])
stains = [
    load("texture/stain1.png"),
    load("texture/stain2.png")
]
explosion_sound = mixer.get_sound_Variants("sound", "explosion")
explosion_blood_sound = pygame.mixer.Sound("sound/explosion_blood.wav")
weapon_fire_Sounds = mixer.get_sound_Variants("sound", "weapon_fire")

reload = pygame.mixer.Sound("sound/reload.wav")
no_ammo_sound = pygame.mixer.Sound("sound/no_ammo.wav")
inv_image = pygame.image.load("texture/inv.png").convert_alpha()
huuto = pygame.transform.scale(
    pygame.image.load("texture/huutomerkki.png"), [12, 33]
).convert_alpha()
huuto.set_alpha(100)
thuds = mixer.get_sound_Variants("sound", "thud")
kill_sound = pygame.mixer.Sound("sound/kill_sound.wav")
menu_click = pygame.mixer.Sound("sound/menu_click.wav")
menu_click2 = pygame.mixer.Sound("sound/menu_click2.wav")
q_r_success = pygame.mixer.Sound("sound/sfx/quick_reload_success.wav")
q_r_fail = pygame.mixer.Sound("sound/sfx/quick_reload_fail.wav")
energy_cell_sound = pygame.mixer.Sound("sound/item_sounds/energy_ammo.wav")

gun_jam = pygame.mixer.Sound("sound/sfx/gun_jam.wav")
gun_jam_clear = pygame.mixer.Sound("sound/sfx/gun_jam_clear.wav")

barricade_texture = pygame.image.load("texture/barricade.png").convert()
barricade_list = []

heartbeat_tick = GameTick(max_value=10)
map_desc_tick = GameTick(180, oneshot=True)
unitstatuses = []

fade_to_black_screen = []

for i in range(10):
    rect = pygame.Surface(size)
    rect.fill([0, 0, 0])
    rect.set_alpha(255 * (i + 1) / 10)
    fade_to_black_screen.append(rect)


fade_tick = GameTick(60, oneshot=True)
fade_tick.value = 30

door_sound = pygame.mixer.Sound("sound/door_sound.wav")

kill_sounds = get_sound_Variants("sound", "kill")
# kill_sound = pygame.mixer.Sound("sound/kill5.wav")
hit_sounds = get_sound_Variants("sound", "hit")
rico_sounds = get_sound_Variants("sound", "rico")
pl_hit = get_sound_Variants("sound", "pl_hit")
death_sounds = get_sound_Variants("sound", "death")
shotgun_sounds = {"fire": get_sound_Variants("sound", "shotgun"), "reload": reload}
assault_rifle_sounds = {
    "fire": get_sound_Variants("sound", "assault"),
    "reload": pygame.mixer.Sound("sound/reload_assault.wav"),
}
sniper_rifle_sounds = {
    "fire": get_sound_Variants("sound", "sniper"),
    "reload": pygame.mixer.Sound("sound/reload_assault.wav"),
}
smg_sounds = {
    "fire": get_sound_Variants("sound", "smg"),
    "reload": pygame.mixer.Sound("sound/reload_assault.wav"),
}
pistol_sounds_silenced = {
    "fire": get_sound_Variants("sound", "silenced"),
    "reload": pygame.mixer.Sound("sound/pistol_reload.wav"),
}

typing = get_sound_Variants("sound", "type")

ruperts_shop_selections = []

assault_rifle_sounds2 = {
    "fire": get_sound_Variants("sound", "ar2_fire"),
    "reload": pygame.mixer.Sound("sound/reload_assault.wav"),
}

nrg_sounds = {
    "fire": get_sound_Variants("sound", "nrg_fire"),
    "reload": pygame.mixer.Sound("sound/nrg_reload.wav"),
}

turret_fire1 = pygame.mixer.Sound("sound/turret_fire1.wav")
turret_fire2 = pygame.mixer.Sound("sound/turret_fire1.wav")
turret_fire3 = pygame.mixer.Sound("sound/turret_fire1.wav")
turret_fire = [turret_fire1, turret_fire2, turret_fire3]

class Hint:
    def __init__(self):
        self.t = 0
        self.hint = ""

hint = Hint()

hints = [
"Lower sanity means exponentially more zombies.",
"Your gun jams more often as your sanity goes down.",
"Right click to melee.",
"By moving you disorient your enemies.",
"Armor-Piercing rounds and energy rounds pierce zombies.",
"Clear a gun jam by spamming the firing button."
]
