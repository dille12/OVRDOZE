import os, sys
import pygame
import math
import random
import time
import mixer
from screeninfo import get_monitors
import get_preferences
from bendedsound import *

a, a, a, a, a, a, a, a, size,a,a, a = get_preferences.pref()

def fp(file_name):

    file_name = file_name.split("assets/")[-1]

    file_name = f"assets/{file_name}"
    return os.path.join(os.getcwd(), file_name)

print("VALUE INIT")
pygame.init()
pygame.mixer.init()
los_tick = 10
multi_kill = 0
camera_pan = 0.03
respawn_ticks = 0


BLOODSINK_TILESIZE = 50

class GlobalVars():
    def __init__(self):
        self.blockClick = False

GV = GlobalVars()

class introState():
    def __init__(self):
        self.introPlayed = False
        self.menu_animations = []

IS = introState()

try:
    monitors = get_monitors()
    m = monitors[0]
    # get first in list or primary if set
    for n in monitors:
        if n.is_primary == True:
            m = n
            break

    fs_size = (m.width, m.height)
except:
    fs_size = (1920, 1080)

#size = 1366, 768
#size = 854, 480
#size = 1920, 1080
multi_kill_ticks = 0
multiplier = 1920 / size[0]
multiplier2 = size[0] / 854

zoom = 1 #CONTROLS THE ZOOM OF THE GAME
multiplier *= zoom
multiplier2 /= zoom

pygame.init()
screen = pygame.display.set_mode(size)
icon = pygame.image.load(fp("texture/icon.png"))
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

raindrops = []
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

class Player:
    def __init__(self, color, name, str_team):
        self.color = color
        self.name = name
        self.alloy = 0
        self.g = 0
        self.c = 0
        self.str_team = str_team

    def __str__(self):
        return f"{self.color} {self.name} {self.str_team}"

BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
BLUE = [51, 102, 255]
RED = [255, 0, 102]
GREEN = [153, 255, 51]
YELLOW = [255, 204, 102]
CYAN = [51, 204, 204]
blue_t = Player(BLUE, "", "blue_t")
red_t = Player(RED, "", "red_t")
green_t = Player(GREEN, "", "green_t")
yellow_t = Player(YELLOW, "", "yellow_t")
nature = Player(BLACK, "Nature", "nature")
placeholder = Player(WHITE, "", "placeholder")

last_hp = 0
free_tick = 0
last_text_i = 0
kills = 0
Inventory_open = False
tab_pressed = False



load_screen_splash = pygame.image.load(fp("texture/loadScreen.png"))





def get_sound_Variants(folder, name2, dont_bend = False):
    list = []
    i = 1
    while True:
        try:
            name = name2 + str(i)
            list.append(make_sound(name, folder, dont_bend))
            i += 1

        except Exception as e:
            return list

def make_sound(sound, file, dont_bend = False):
    path = fp(file + "/" + sound + ".wav")
    return get_Sound(path) if not dont_bend else pygame.mixer.Sound(fp(path))


def get_Sound(file):

    sound = pygame.mixer.Sound(fp(file))

    file_name = file.split("/")[-1]



    bended_file_name = "bended/" + file_name.removesuffix(".wav") + "_bended.wav"

    sound2 = pygame.mixer.Sound(fp(bended_file_name))

    return bendedSound(sound, sound2)


def rgb_image_load(image_dir):
    list = [pygame.image.load(fp(image_dir))]
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

    return image






def load(image, size = None, alpha = True, double = False):
    temp = pygame.image.load(fp(image))
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

    temp = pygame.image.load(fp(image))

    x,y = temp.get_size()

    im = pygame.transform.scale(
        temp,
        [round(x / multiplier), round(y / multiplier)],
    ).convert_alpha()
    return im

def splitText(text, maxLength = 50):
    textSplitten = text.split(" ")
    returnText = []
    currText = ""
    for word in textSplitten:
        if len(word) + len(currText) <= maxLength:
            currText += word + " "
        else:
            returnText.append(currText)
            currText = word + " "
    returnText.append(currText)
    return returnText


multikill_fonts = []
for i in range(5):
    font_s = 50 + i * 15
    multikill_fonts.append(pygame.font.Font(fp("texture/agencyb.ttf"), round(font_s)))

terminal_kill_counter = pygame.font.Font(fp("texture/terminal.ttf"), 40)
kill_counter_texts = {}
for x in range(10, 101):
    image_list = []
    for color in [[255, 255, 255], [255, 0, 0], [0, 255, 0], [0, 0, 255]]:
        text = terminal_kill_counter.render("x" + str(x), False, color)
        image_list.append(text)
    kill_counter_texts[x] = image_list

kill_rgb = rgb_image_load("texture/kill.png")
menu_rgb = rgb_image_load("texture/menu_image.png")
ovrdoze_rgb = rgb_image_load("texture/ovrdoze.png")

jam1 = load("texture/jam1.png", size = [60, 88])
jam2 = load("texture/jam2.png", size = [60, 88])

packet_dict = {}
player = load("texture/player.png", size = [180,119])

player_pistol = load("texture/player_pistol.png", size = [180,119])


player_indicator = []
for x in range(45):
    t = load("texture/playerIndicator.png", size = [130 * x/30, 130 * x/30])
    t.set_alpha(x*155/45)
    player_indicator.append(t)

upgradeIcon = pygame.image.load("assets/texture/upgradeIcon.png").convert_alpha()
buyIcon = pygame.image.load("assets/texture/buyIcon.png").convert_alpha()
checkIcon = pygame.image.load("assets/texture/check.png").convert_alpha()
checkIcon.set_alpha(150)

soldierSprite = load("texture/soldier.png", size = [180,119])
soldierPistolSprite = load("texture/soldierPistol.png", size = [180,119])

PISTOLS = ["GLOCK", "M1911", "FN57-S", "DESERTEAGLE"]

zombie = load("texture/zombie.png", size = [119,119])
zombie2 = load("texture/zombie2.png", size = [119,119])
zombie3 = load("texture/zombie3.png", size = [119,119])
zombie4 = load("texture/zombie4.png", size = [119,119])
zombie5 = load("texture/zombie5.png", size = [119,119])

shirts = []
for i in range(1,6):
    shirts.append(load(f"texture/shirt{i}.png", size = [119,119]))

hairs = []
for i in range(1,4):
    hairs.append(load(f"texture/hair{i}.png", size = [119,119]))

hands = []
for i in range(1,5):
    hands.append(load(f"texture/hands{i}.png", size = [119,119]))
print("IMAGES:")
print(shirts, hairs, hands)

zombieImages = []
for s in shirts:
    for h in hairs:
        for d in hands:
            temp = s.copy()
            temp.blit(h, [0,0])
            temp.blit(d, [0,0])
            zombieImages.append(temp)


print("Zombie types:", len(zombieImages))


bomber = load("texture/bomber.png", size = [150,150])

zombie_big = load("texture/zombie.png", size = [200,200])

bullet_texture = load("texture/bullet.png", size = [15,4])

cursorIm = pygame.image.load(fp('texture/mouse.png'))

# Convert the image to a surface
cursor = pygame.Surface((32, 32), pygame.SRCALPHA)
cursor.blit(cursorIm, (0, 0))


y_size = bullet_texture.get_size()[1]

bullet_length = []
for x in range(200):
    x += 5
    bullet_length.append(
        pygame.transform.scale(
            pygame.image.load(fp("texture/bullet.png")), (round(x * multiplier2), round(4*multiplier2))
        ).convert_alpha()
    )

lazer_texture = load("texture/lazer.png", size = [15,8])
y_size = lazer_texture.get_size()[1]

rocket_texture = load("texture/rocket.png", size = [60,32])

energy_bullet_length = []
for x in range(200):
    x += 5
    energy_bullet_length.append(
        pygame.transform.scale(
            pygame.image.load(fp("texture/lazer.png")), (round(x * multiplier2), round(8*multiplier2))
        ).convert_alpha()
    )



grenade_throw = False
grenade = load("texture/items/grenade.png", size = [30,30])
molotov = load("texture/items/molotov.png", size = [40,40])

grenade_ico = colorize(load("texture/items/grenade.png", size = [50,50]), pygame.Color((200,200,200)))
molotov_ico =  colorize(load("texture/items/molotov.png", size = [50,50]), pygame.Color((200,200,200)))

molotov_explode_sound = get_Sound("sound/molotov.wav")
molotov_pickup = get_Sound("sound/molotov_pickup.wav")
drug_use = get_Sound("sound/drug_use.wav")

chargeSound = get_Sound("sound/sfx/chargeup.wav")
chargeCancelSound = get_Sound("sound/sfx/charge_cancel.wav")


melee_sound = get_Sound("sound/sfx/melee.wav")
melee_hit_sound = get_Sound("sound/sfx/melee_hit.wav")
append_explosions = []
bullet_pickup = get_Sound("sound/bullet.wav")
grenade_pickup = get_Sound("sound/grenade_pickup.wav")
needle_pickup = get_Sound("sound/needle_pickup.wav")
pill_pickup = get_Sound("sound/pill_pickup.wav")
turret_pickup = get_Sound("sound/turret_pickup.wav")
sniff_sound = get_Sound("sound/sinff.wav")
info = pygame.image.load(fp("texture/info.png")).convert_alpha()

arrowRight = load("texture/arrow.png", size = [50,50])
arrowRightRed = colorize(arrowRight.copy(), pygame.Color((255,0,0)))
arrowLeft = pygame.transform.flip(arrowRight.copy(), True, False)
arrowLeftRed = colorize(arrowLeft.copy(), pygame.Color((255,0,0)))

crawlerBody = load("texture/crawlerBody.png", alpha=True)
crawlerArm = load("texture/arm.png")
crawlerHand = load("texture/hand.png")

crawlerFootSteps = [
    get_Sound("sound/sfx/crawlerFootstep1.wav"),
    get_Sound("sound/sfx/crawlerFootstep2.wav"),
    get_Sound("sound/sfx/crawlerFootstep3.wav"),
    get_Sound("sound/sfx/crawlerFootstep4.wav"),
]

crawlerAttack = [
    get_Sound("sound/sfx/crawlerAttack.wav"),
    get_Sound("sound/sfx/crawlerAttack2.wav"),

]

#crawlerBody = pygame.image.load("assets/texture/crawlerBody.png").convert_alpha()
#crawlerArm = pygame.image.load("assets/texture/arm.png").convert_alpha()
#crawlerHand = pygame.image.load("assets/texture/hand.png").convert_alpha()

hud_color = [255, 255, 255]


not_used_weapons = []

player_weapons = []

class ID_container:
    def __init__(self):
        self.nwobjects = {}

ID_container = ID_container()


class TimeDelta:
    def __init__(self):
        self.timedelta = 1
        self.nonMutableTimeDelta = 1

    def tick(self, am):
        return round(am / self.timedelta)

    def mod(self, am, nonMutable = False):
        if nonMutable:
            return am * self.nonMutableTimeDelta
        else:
            return am * self.timedelta

    def exp(self, am):
        return am**self.timedelta

    def exp_rev(self, am):
        return am ** (1 / self.timedelta)
    
    


timedelta = TimeDelta()


class GameTick:
    def __init__(self, max_value=30, oneshot=False, nonMutable = False):
        self.value = 0
        self.max_value = max_value
        self.oneshot = oneshot
        self.nonMutable = nonMutable

    def tick(self):
        if self.value < self.max_value:
            self.value += timedelta.mod(1, self.nonMutable)
        if self.value < self.max_value:
            return False
        else:
            if not self.oneshot:
                self.value = 0
            return True

    def rounded(self):
        return round(self.value)
    
    def isMaxed(self):
        return self.value > self.max_value


dialogue = []
dialogue_tick = GameTick(40)

money_tick = GameTick(35, oneshot=True)

beat_blink = GameTick(12, oneshot = True)

casing_list = []

last_hp = 0
damage_ticks = 0

inv_click = get_Sound("sound/inv_click.wav")
inv_open = get_Sound("sound/inv_open.wav")
inv_close = get_Sound("sound/inv_close.wav")

mov_turret_base = load("texture/movingturret_base.png", size = [70,70])
mov_turret_gun = load("texture/movingturret_gun.png", size = [70,70])

mov_fire = get_Sound("sound/mov_turret_fire.wav")

turret_leg = load("texture/turret_leg.png", size = [70,70])
turret = load("texture/turret.png", size = [70,70])
stains = [
    load("texture/stain1.png"),
    load("texture/stain2.png")
]
explosion_sound = get_sound_Variants("sound", "explosion")
sm_explosion_sound = get_sound_Variants("sound", "sm_explosion")

explosion_blood_sound = get_Sound("sound/explosion_blood.wav")
weapon_fire_Sounds = get_sound_Variants("sound", "weapon_fire")

radio_chatter = {
    "wander" : get_sound_Variants("sound/radio_chatter", "standby"),
    "attacking" : get_sound_Variants("sound/radio_chatter", "shout"),
    "takingcover" : get_sound_Variants("sound/radio_chatter", "take_cover"),
    "investigate" : get_sound_Variants("sound/radio_chatter", "attack"),
}

footsteps = get_sound_Variants("sound/sfx", "footstep")

evade_sound = get_Sound("sound/sfx/woosh.wav")

loadSymbolRGB = rgb_image_load("texture/kill.png")
for i, x in enumerate(loadSymbolRGB):
    sx, sy = x.get_size()
    loadSymbolRGB[i] = pygame.transform.scale(x, [sx * 6, sy * 6])


loadSymbol = pygame.image.load(fp("texture/kill.png")).convert_alpha()
sx, sy = loadSymbol.get_size()
loadSymbol = pygame.transform.scale(loadSymbol, [sx * 6, sy * 6])
loadSymbol.set_alpha(10)

footstep_tick = GameTick(15)

reload = get_Sound("sound/reload.wav")

upgradeSound = get_Sound("sound/sfx/upgrade.wav")

no_ammo_sound = get_Sound("sound/no_ammo.wav")
inv_image = pygame.image.load(fp("texture/inv.png")).convert_alpha()
inv4_image = pygame.image.load(fp("texture/inv4.png")).convert_alpha()
inv5_image = pygame.image.load(fp("texture/inv5.png")).convert_alpha()


casingIm = pygame.image.load(fp("texture/casing.png")).convert_alpha()

huuto = pygame.transform.scale(
    pygame.image.load(fp("texture/huutomerkki.png")), [12, 33]
).convert_alpha()
huuto.set_alpha(100)
thuds = get_sound_Variants("sound", "thud")
kill_sound = get_Sound("sound/kill_sound.wav")
menu_click = get_Sound("sound/menu_click.wav")
menu_click2 = get_Sound("sound/menu_click2.wav")
q_r_success = get_Sound("sound/sfx/quick_reload_success.wav")
q_r_fail = get_Sound("sound/sfx/quick_reload_fail.wav")
energy_cell_sound = get_Sound("sound/item_sounds/energy_ammo.wav")

gun_jam = get_Sound("sound/sfx/gun_jam.wav")
gun_jam_clear = get_Sound("sound/sfx/gun_jam_clear.wav")

barricade_texture = pygame.image.load(fp("texture/barricade.png")).convert()
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

door_sound = get_Sound("sound/door_sound.wav")
phone_ring = get_Sound("sound/phone_ring.wav")

scroll_bar_clicks = get_sound_Variants("sound/scrollbarclicks", "file", dont_bend = True)

introSound = pygame.mixer.Sound(fp("sound/sfx/introLighter.wav"))

kill_sounds = get_sound_Variants("sound", "kill")
# kill_sound = get_Sound("sound/kill5.wav")
hit_sounds = get_sound_Variants("sound", "hit")
rico_sounds = get_sound_Variants("sound", "rico")
pl_hit = get_sound_Variants("sound", "pl_hit")
death_sounds = get_sound_Variants("sound", "death")
death_sounds_soldier = get_sound_Variants("sound", "death_soldier")
shotgun_sounds = {"fire": get_sound_Variants("sound", "shotgun"), "reload": reload}
assault_rifle_sounds = {
    "fire": get_sound_Variants("sound", "assault"),
    "reload": get_Sound("sound/reload_assault.wav"),
}
sniper_rifle_sounds = {
    "fire": get_sound_Variants("sound", "sniper"),
    "reload": get_Sound("sound/reload_assault.wav"),
}
smg_sounds = {
    "fire": get_sound_Variants("sound", "smg"),
    "reload": get_Sound("sound/reload_assault.wav"),
}
pistol_sounds_silenced = {
    "fire": get_sound_Variants("sound", "silenced"),
    "reload": get_Sound("sound/pistol_reload.wav"),
}
rocket_launcher_sounds = {
    "fire": get_sound_Variants("sound/sfx", "rocket_launch"),
    "reload": get_Sound("sound/sfx/rocket_reload.wav"),
}

typing = get_sound_Variants("sound", "type")

ruperts_shop_selections = []

assault_rifle_sounds2 = {
    "fire": get_sound_Variants("sound", "ar2_fire"),
    "reload": get_Sound("sound/reload_assault.wav"),
}

nrg_sounds = {
    "fire": get_sound_Variants("sound", "nrg_fire"),
    "reload": get_Sound("sound/nrg_reload.wav"),
    "chargeCancelSound" : chargeCancelSound,
    "chargeSound" : chargeSound,
}

washer_sounds = {
    "fire": get_Sound("sound/sfx/powerwasherfire.wav"),
    "reload": get_Sound("sound/nrg_reload.wav"),
    "chargeCancelSound" : chargeCancelSound,
    "chargeSound" : get_Sound("sound/sfx/powerwashercharge.wav"),
}

turret_fire1 = get_Sound("sound/turret_fire1.wav")
turret_fire2 = get_Sound("sound/turret_fire1.wav")
turret_fire3 = get_Sound("sound/turret_fire1.wav")
turret_fire = [turret_fire1, turret_fire2, turret_fire3]

tutorialTexts = [
    "Welcome to OVRDOZE, a tight-space wave survival game. Click to advance.",
    "You can move using WASD. Run by holding SHIFT, and dodge by pressing SPACE.",
    "Mouse placement aims your equipped weapon. The current bullet spread is indicated by the distance between the aim lines.",
    "LEFT MOUSE CLICK fires your currently equipped weapon. Guns have a chance of jamming, which can be cleared by rapidly clicking the firing button.",
    "RIGHT MOUSE CLICK performs a melee attack around you, dealing significant damage and knockback. Melee has a short cooldown, so use it liberally.",
    "Zombies deal damage, but your HP heals back quickly. However, healing drains your SANITY.",
    "SANITY affects the number of zombies present during a wave and the chance of your gun jamming. Consume narcotics to maintain your sanity.",
    "Zombies spawn during WAVES, which are synced with the currently playing music. Between waves, you should clean up the map and upgrade your weapons.",
    "Zombies occasionally drop weapons. First, you need to unlock weapons in LOADOUT to make them spawn in-game. You can carry up to five guns. The pistol you start with can be switched in LOADOUT, and it has infinite ammo.",
    "Each weapon has three upgrades, ranging from useful to overpowered. These must first be unlocked in LOADOUT by reaching a set number of kills. After unlocking, they can be exchanged for UPGRADE TOKENS in-game at the UPGRADE STATION.",
    "You sink into the blood of killed enemies. Avoid walking over blood or clean it up by switching to the POWERWASHER using T.",
    "Press G to throw GRENADES, which can be cycled by pressing Q. GRENADES are dangerous to everyone and can easily kill you too, so remember to take cover.",
    "TURRETS and BARRICADES assist in point defense and should be used in tight situations."
]

tutorialTitles = ["", "MOVEMENT", "AIMING", "FIRING", "MELEE", "HP", "SANITY", "WAVES", "GUNS", "UPGRADES", "BLOOD SINKING", "GRENADES", "UTILITIES"]


upgradeIcons = {}
uPath = "assets/texture/upgradeIcons"
for x in os.listdir(uPath):
    p = os.path.join(uPath, x)

    im = pygame.image.load(p).convert_alpha()

    imRed = colorize(im.copy(), pygame.Color(255, 0, 0))

    imAlpha = im.copy()
    imAlpha.set_alpha(100)
    
    upgradeIcons[x.lower().removesuffix(".png")] = [im, imRed, imAlpha]



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
"Clear a gun jam by spamming the firing button.",
"You sink in to the blood of your enemies. Remember to clean it up.",
"Time slows down while your health is below 30%.",
"Take them all with no hesitation.",
"You can dodge by pressing the spacebar.",
"You can extract recources from crates by pressing shift faster.",
"Move more slowly by pressing control.",
"Zombies drop weapons from time to time.",
"All upgrades are not created equal. Use your upgrade tokens wisely",
"Reaching 100 multikills awards you 10% sanity",
"Energy weapons do not jam.",
"You can tank one hit that would kill you.",
"Crawlers run right through your barricades. Reposition quickly if one enters the basement.",
"If you are told to run, run.",
]


enemyDropRate = {"big" : 0.02, "bomber" : 0.03, "runner" : 0.05, "normal" : 0.9, "psycho" : 0.02, "firestarter" : 0.02, "crawler" : 0.002}


def weighted_random_choice(weighted_dict):
    total_weight = sum(weighted_dict.values())
    rand_num = random.uniform(0, total_weight)

    cumulative_weight = 0
    for item, weight in weighted_dict.items():
        cumulative_weight += weight
        if rand_num < cumulative_weight:
            return item


if __name__ == '__main__':
    d = {}
    for x in range(100000):
        v = weighted_random_choice(enemyDropRate)
        if v in d:
            d[v] += 1
        else:
            d[v] = 1

    print(d)
