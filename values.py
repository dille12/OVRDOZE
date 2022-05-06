import os, sys
import pygame
import math
import random
import time
import mixer
print("VALUE INIT")
pygame.init()
pygame.mixer.init()
los_tick = 10
multi_kill = 0
camera_pan = 0.03
respawn_ticks = 0
fs_size = (1920,1080)
size = 854,480
multi_kill_ticks = 0
multiplier = 1920/size[0]
multiplier2 = size[0]/854
pygame.init()
screen = pygame.display.set_mode(size)
tick_count = 60
player_pos = [50,50]
camera_pos = [0,0]
player_hp = 100
x_vel = 0
y_vel = 0
last_bullet_list = ()

enemy_count = 0
multiplayer = False

def set_multiplayer(arg):
    global multiplayer
    multiplayer = arg
    print("MULTIPLAYER=",multiplayer)


turret_list = []
enemy_list = []
bullet_list = []
particle_list = []
grenade_list = []
kill_counter  =[]
explosions = []

last_hp = 0
free_tick = 0
last_text_i = 0
kills = 0
Inventory_open = False
tab_pressed = False


def get_Sound(sound,file):
    path = file + "/" + sound + ".wav"
    print(path)
    return pygame.mixer.Sound(path)

def rgb_image_load(image_dir):
    list = [pygame.image.load(image_dir)]
    for color in [pygame.Color(255, 0, 0), pygame.Color(0, 255, 0), pygame.Color(0, 0, 255)]:
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

def get_sound_Variants(folder,name2):
    list = []
    i = 1
    while True:
        try:
            name = name2 + str(i)
            list.append(get_Sound(name,folder))
            i+=1

        except:
            return list


multikill_fonts = []
for i in range(5):
    font_s = 50 + i*15
    multikill_fonts.append(pygame.font.Font('texture/agencyb.ttf', round(font_s)))

kill_rgb = rgb_image_load("texture/kill.png")

player = pygame.transform.scale(pygame.image.load("texture/player.png"),[round(180/multiplier),round(119/multiplier)]).convert_alpha()
player_firing = pygame.transform.scale(pygame.image.load("texture/player_firing.png"),[round(225/multiplier),round(100/multiplier)]).convert_alpha()
bullet = pygame.transform.scale(pygame.image.load("texture/bullet.png"), (15,4)).convert_alpha()
bullet_length = []
for x in range(100):
    x += 5
    bullet_length.append(pygame.transform.scale(pygame.image.load("texture/bullet.png"), (x,4)).convert_alpha())

long_bullet = pygame.transform.scale(pygame.image.load("texture/bullet.png"), (45,4)).convert_alpha()
grenade_throw = False
grenade = pygame.transform.scale(pygame.image.load("texture/items/grenade.png"), [14,14]).convert_alpha()
drug_use = pygame.mixer.Sound("sound/drug_use.wav")

bullet_pickup = pygame.mixer.Sound("sound/bullet.wav")
grenade_pickup = pygame.mixer.Sound("sound/grenade_pickup.wav")
needle_pickup = pygame.mixer.Sound("sound/needle_pickup.wav")
pill_pickup = pygame.mixer.Sound("sound/pill_pickup.wav")
turret_pickup = pygame.mixer.Sound("sound/turret_pickup.wav")
sniff_sound = pygame.mixer.Sound("sound/sinff.wav")
info = pygame.image.load("texture/info.png").convert_alpha()

hud_color = [255, 255, 255]




last_hp = 0
damage_ticks = 0

inv_click = pygame.mixer.Sound("sound/inv_click.wav")
inv_open = pygame.mixer.Sound("sound/inv_open.wav")
inv_close = pygame.mixer.Sound("sound/inv_close.wav")



turret_leg =   pygame.transform.scale(pygame.image.load("texture/turret_leg.png"), [35,35]).convert_alpha()
turret =  pygame.transform.scale(pygame.image.load("texture/turret.png"), [35,35]).convert_alpha()
stains =  [pygame.image.load("texture/stain1.png").convert_alpha(),pygame.image.load("texture/stain2.png").convert_alpha()]
explosion_sound = mixer.get_sound_Variants("sound","explosion")
weapon_fire_Sounds = mixer.get_sound_Variants("sound","weapon_fire")
reload = pygame.mixer.Sound("sound/reload.wav")
no_ammo_sound = pygame.mixer.Sound("sound/no_ammo.wav")
inv_image = pygame.image.load("texture/inv.png").convert_alpha()
huuto = pygame.transform.scale(pygame.image.load("texture/huutomerkki.png"), [12,33]).convert_alpha()
huuto.set_alpha(100)
thuds = mixer.get_sound_Variants("sound","thud")
kill_sound = pygame.mixer.Sound("sound/kill_sound.wav")

kill_sounds = get_sound_Variants("sound","kill")
# kill_sound = pygame.mixer.Sound("sound/kill5.wav")
hit_sounds = get_sound_Variants("sound","hit")
rico_sounds = get_sound_Variants("sound","rico")
pl_hit = get_sound_Variants("sound","pl_hit")
death_sounds = get_sound_Variants("sound","death")
shotgun_sounds = {"fire": get_sound_Variants("sound","shotgun"),"reload":reload}
assault_rifle_sounds = {"fire": get_sound_Variants("sound","assault"),"reload":pygame.mixer.Sound("sound/reload_assault.wav")}
sniper_rifle_sounds = {"fire": get_sound_Variants("sound","sniper"),"reload":pygame.mixer.Sound("sound/reload_assault.wav")}
smg_sounds = {"fire": get_sound_Variants("sound","smg"),"reload":pygame.mixer.Sound("sound/reload_assault.wav")}
pygame.mixer.music.load("sound/paska_biisi.wav")
turret_fire1 = pygame.mixer.Sound("sound/turret_fire1.wav")
turret_fire2 = pygame.mixer.Sound("sound/turret_fire1.wav")
turret_fire3 = pygame.mixer.Sound("sound/turret_fire1.wav")
turret_fire = [turret_fire1,turret_fire2,turret_fire3]
