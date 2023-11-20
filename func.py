import os, sys
import pygame
import math
import random
import time
from values import *
import classes
import los
from pathfind import find_shortest_path
from _thread import start_new_thread


pygame.init()
pygame.font.init()

agency = pygame.font.Font("texture/agencyb.ttf", round(70))
terminal = pygame.font.Font("texture/terminal.ttf", 20)
terminal2 = pygame.font.Font("texture/terminal.ttf", 30)
terminal3 = pygame.font.Font("texture/terminal.ttf", 10)
terminal4 = pygame.font.Font("texture/terminal.ttf", 40)

terminal_hint = pygame.font.Font("texture/terminal.ttf", round(8*multiplier2))

evade_skip_tick = 0
acceleration = 200 / 1.875
velocity_cap = 9 / 1.875
breaking = 0.9
walking_speed = 7 / 1.875
running_speed = 13 / 1.875
evade_speed = 30 / 1.875
camera_breaking = 0.1 / 1.875
evading = False
tick_count = 60

camera_offset = [size[0] / 2, size[1] / 2]


def debug_render(text_str):
    text = agency.render(str(text_str), False, [255, 255, 0])
    render_cool(text, [1000, 60], 15, 16, render=True, offset=10)  ### IN GAME


def print_s(screen, text_str, slot, color=hud_color):
    text = terminal.render(str(text_str), False, color)
    screen.blit(text, (size[0] - 10 - text.get_rect().size[0], slot * 30))  #

def blit_glitch(screen, image, pos, glitch = 2, diagonal = False, black_bar_chance = 15, black_bar_color = (0,0,0)):
    upper_pos = 0
    lower_pos = random.randint(2, 5)
    image_size = image.get_size()
    while 1:
        if random.randint(1, black_bar_chance) != 1:
            screen.blit(
                image,
                [pos[0] + random.randint(-glitch, glitch), pos[1] + upper_pos + (0 if not diagonal else random.randint(-glitch, glitch))],
                area=[0, upper_pos, image_size[0], lower_pos-upper_pos],
            )
        if lower_pos == image_size[1]:
            break
        upper_pos = lower_pos
        lower_pos += random.randint(2, 5)
        if lower_pos >= image_size[1]:
            lower_pos = image_size[1]

def inverted(img):
   inv = pygame.Surface(img.get_rect().size, pygame.SRCALPHA)
   inv.fill((255,255,255,255))
   inv.blit(img, (0,0), None, pygame.BLEND_RGB_SUB)
   return inv

def render_text_glitch(
    screen, string, pos, color=[255, 255, 255], centerx=False, glitch=10, font = None
):
    # color = pick_random_from_list([[255,0,0], [0,255,0], [0,0,255]])
    if not font:
        font = terminal4
    text = font.render(str(string), False, color)

    upper_pos = 0
    lower_pos = random.randint(2, 5)
    text_size = text.get_size()
    if centerx:
        pos[0] -= text_size[0] / 2
    while 1:
        if random.randint(1, 5) == 1:
            screen.blit(
                text,
                [pos[0] + random.uniform(-glitch, glitch), pos[1] + upper_pos],
                area=[0, upper_pos, text_size[0], lower_pos],
            )
        if lower_pos == text_size[1]:
            break
        upper_pos = lower_pos
        lower_pos += random.randint(2, 5)
        if lower_pos >= text_size[1]:
            lower_pos = text_size[1]


def load_animation(directory, start_frame, frame_count, alpha=255, intro = False):
    list_anim = []


    for x in range(frame_count):
        x = x + start_frame
        im_dir = directory + "/" + (4 - len(str(x))) * "0" + str(x) + ".png"

        im = load(im_dir, double=True)

        if intro:
            if x - start_frame > frame_count-10:
                i = (x - start_frame) - (frame_count-10)
                i = (i/10) ** 3 + 1
                size = list(im.get_size())
                size[0] *= i
                size[1] *= i

                im = pygame.transform.scale(im, size)

        if alpha != 255:
            im2 = pygame.Surface(im.get_size())
            im2.fill((0, 0, 0))
            im.set_alpha(alpha)
            im2.blit(im, (0, 0))
            list_anim.append(im2)
        else:
            list_anim.append(im)

    return list_anim


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


def BezierInterpolation(positions, t):

    P0_x = pow((1 - t), 2) * positions[0][0]
    P0_y = pow((1 - t), 2) * positions[0][1]

    P1_x = 2 * (1 - t) * t * positions[1][0]
    P1_y = 2 * (1 - t) * t * positions[1][1]

    P2_x = t**2 * positions[2][0]
    P2_y = t**2 * positions[2][1]

    curve = (P0_x + P1_x + P2_x, P0_y + P1_y + P2_y)
    return list(curve)


def rgb_render(list, amount, pos, cam_delta, screen):

    # rect_pos = list[0].get_rect(center = list[0].get_rect(center = (pos[0], pos[1])).center)
    amount = amount * 0.6
    pos[1] = pos[1] + random.uniform(-amount, amount)

    screen.blit(
        pick_random_from_list(list[1:]),
        [
            pos[0] + 20 + random.uniform(-amount, amount) + cam_delta[0] * 2,
            pos[1] + random.uniform(-amount, amount) + cam_delta[1] * 2,
        ],
    )

    screen.blit(list[0], [pos[0] + 20 + cam_delta[0], pos[1] + cam_delta[1]])


def get_dist_points(point_1, point_2):
    return math.sqrt((point_2[0] - point_1[0]) ** 2 + (point_2[1] - point_1[1]) ** 2)


def render_cool(
    image,
    pos,
    tick,
    beat_tick_h,
    render=False,
    offset=0,
    scale=1,
    screen=screen,
    style="default",
    alpha=255,
):

    a = 1 - math.sin(offset + 10 * tick / (2 * math.pi * beat_tick_h)) * 0.1 * scale
    b = (
        1
        - math.sin(math.pi / 2 + offset + 10 * tick / (2 * math.pi * beat_tick_h))
        * 0.1
        * scale
    )
    rotation = (
        math.sin(math.pi / 2 + offset + 10 * tick / (2 * math.pi * beat_tick_h))
        * 2
        * scale
    )
    if style == "default":
        image_size = image.get_rect().size
        image_size_2 = [round(image_size[0] * a), round(image_size[1] * b)]

        image_2 = pygame.transform.scale(image, image_size_2)

        pos = [pos[0] - a / 4 * image_size_2[0], pos[1] - b / 4 * image_size_2[1]]

        if render == True:
            image_2, image_2_rot = rot_center(image_2, rotation, pos[0], pos[1])

        screen.blit(image_2, pos)


def check_for_render(player_pos, pos, range=3000):
    if range < math.sqrt((player_pos[0] - pos[0]) ** 2 + (player_pos[1] - pos[1]) ** 2):
        return True
    return False


def get_angle(pos1, pos2):
    myradians = math.atan2(pos2[1] - pos1[1], pos2[0] - pos1[0])
    mydegrees = math.degrees(myradians)
    return mydegrees


def return_price(x):
    return x.weapon.price


def mult(list1, am):
    try:
        list_1 = list1.copy()
    except:
        list_1 = list1

    for x in range(len(list1)):
        list_1[x] *= am
    return list_1


def minus(list1, list2, op="+"):
    try:
        list_1 = list1.copy()
        list_2 = list2.copy()
    except:
        list_1 = list1
        list_2 = list2
    for x in range(len(list1)):
        if op == "+":
            list_1[x] += list_2[x]
        else:
            list_1[x] -= list_2[x]
    return list_1


def pick_random_from_list(list):
    return list[random.randint(0, len(list) - 1)]


def pick_random_from_dict(dict, key=False):
    dict_keys = list(dict.keys())
    if key:
        return dict_keys[random.randint(0, len(dict_keys) - 1)]
    else:
        return dict[dict_keys[random.randint(0, len(dict_keys) - 1)]]


def minus_list(list1, list2):
    list3 = list1.copy()
    for i in range(len(list1)):
        list3[i] = list1[i] - list2[i]

    return list3


def list_play(list):
    for y in list:
        y.stop()
    pick_random_from_list(list).play()


def load_image(image):
    im = pygame.image.load(image)
    size = im.get_rect().size
    size = [round(size[0] * r_w), round(size[1] * r_h)]
    return pygame.transform.scale(im, size)


def draw_pos(pos, cam_pos, x_off=0, y_off=0):
    return [pos[0] - cam_pos[0] + x_off, pos[1] - cam_pos[1] + y_off]


def get_closest_value(value, list):
    list_1 = {}
    for x in list:
        list_1[abs(value - x)] = x
    key_min = min(list_1)
    return list_1[key_min]


def get_closest_point(pos, list):
    dists = {}
    for point in list:
        dists[point] = get_dist_points(pos, point)

    key_min = min(dists.keys(), key=(lambda k: dists[k]))
    return dists[key_min]

def joystick_movement(joystick, player_pos, x_vel, y_vel, evading, evade_skip_tick, app):
    space = False
    shift = False
    for event in pygame.event.get():
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == 0:
                space = True
            elif event.button == 8:
                shift = True

    x_amount = joystick.get_axis(0)
    y_amount = joystick.get_axis(1)
    current_hypotenuse = math.sqrt(x_amount**2 + y_amount**2)
    if current_hypotenuse > 1:
        x_amount = x_amount / current_hypotenuse
        y_amount = y_amount / current_hypotenuse


    if abs(x_amount) < 0.05:
        x_amount = 0

    if abs(y_amount) < 0.05:
        y_amount = 0

    if space and evading == False and evade_skip_tick <= 0:
        y_vel = timedelta.mod(evade_speed) * y_amount
        x_vel = timedelta.mod(evade_speed) * x_amount

        if (x_vel, y_vel) != (0, 0):
            evade_skip_tick = 30
            evading = True
            evade_sound.stop()
            evade_sound.play()

    if evading == False:
        total_vel = math.sqrt(x_amount**2 + y_amount**2)
        velocity_cap = timedelta.mod(9 / 1.875)
        if total_vel > 5/9:
            sprinting = True
            crouching = False
        elif total_vel < 2.75/9:
            crouching = True
            sprinting = False
        else:
            sprinting = False
            crouching = False

        x_acc = timedelta.mod(acceleration) * x_amount
        y_acc = timedelta.mod(acceleration) * y_amount

    else:
        velocity_cap = timedelta.mod(5 / 1.875)
        x_acc, y_acc = 0, 0

        if math.sqrt(x_vel**2 + y_vel**2) < velocity_cap:
            evading = False

    if sprinting:
        if footstep_tick.tick():
            for x in footsteps:
                x.stop()
            pick_random_from_list(footsteps).play()
    else:
        pass


    if abs(x_vel) < velocity_cap:
        x_vel += timedelta.mod(x_acc / tick_count)
    if abs(y_vel) < velocity_cap:
        y_vel += timedelta.mod(y_acc / tick_count)

    if abs(x_vel) > 0.1:
        x_vel *= timedelta.exp(breaking)
    else:
        x_vel = 0
    if abs(y_vel) > 0.1:
        y_vel *= timedelta.exp(breaking)
    else:
        y_vel = 0

    if evade_skip_tick > 0:
        evade_skip_tick -= timedelta.mod(1)
    else:
        evading = False

    player_pos[0] += x_vel * multiplier2
    player_pos[1] += y_vel * multiplier2

    return player_pos, x_vel, y_vel


def player_movement2(pressed, player_pos, x_vel, y_vel, app):
    global evading, evade_skip_tick
    sprinting = False

    if pygame.joystick.get_count() and app.detectJoysticks:
        joystick = app.joysticks[0]
        return joystick_movement(joystick, player_pos, x_vel, y_vel, evading, evade_skip_tick, app)


    if pressed[pygame.K_SPACE] and evading == False and evade_skip_tick <= 0:
        if pressed[pygame.K_w]:
            y_vel = timedelta.mod(-evade_speed)
        elif pressed[pygame.K_s]:
            y_vel = timedelta.mod(evade_speed)
        else:
            y_vel = 0
        if pressed[pygame.K_d]:
            x_vel = timedelta.mod(evade_speed)
        elif pressed[pygame.K_a]:
            x_vel = timedelta.mod(-evade_speed)
        else:
            x_vel = 0

        if (x_vel, y_vel) != (0, 0):
            evade_skip_tick = 30
            evading = True
            evade_sound.stop()
            evade_sound.play()

    if evading == False:

        if pressed[pygame.K_LSHIFT]:
            sprinting = True
            velocity_cap = timedelta.mod(9 / 1.875)
        elif pressed[pygame.K_LCTRL]:
            crouching = True
            velocity_cap = timedelta.mod(2.75 / 1.875)
        else:
            sprinting = False
            velocity_cap = timedelta.mod(5 / 1.875)
        if pressed[pygame.K_w]:
            y_acc = timedelta.mod(-acceleration)
        elif pressed[pygame.K_s]:
            y_acc = timedelta.mod(acceleration)
        else:
            y_acc = 0
        if pressed[pygame.K_d]:
            x_acc = timedelta.mod(acceleration)
        elif pressed[pygame.K_a]:
            x_acc = timedelta.mod(-acceleration)
        else:
            x_acc = 0

    else:
        velocity_cap = timedelta.mod(5 / 1.875)
        x_acc, y_acc = 0, 0

        if math.sqrt(x_vel**2 + y_vel**2) < velocity_cap:
            evading = False

    if sprinting:
        if footstep_tick.tick():
            for x in footsteps:
                x.stop()
            pick_random_from_list(footsteps).play()
    else:
        pass


    if abs(x_vel) < velocity_cap:
        x_vel += timedelta.mod(x_acc / tick_count)
    if abs(y_vel) < velocity_cap:
        y_vel += timedelta.mod(y_acc / tick_count)

    if abs(x_vel) > 0.1:
        x_vel *= timedelta.exp(breaking)
    else:
        x_vel = 0
    if abs(y_vel) > 0.1:
        y_vel *= timedelta.exp(breaking)
    else:
        y_vel = 0

    if evade_skip_tick > 0:
        evade_skip_tick -= timedelta.mod(1)
    else:
        evading = False

    player_pos[0] += x_vel * multiplier2
    player_pos[1] += y_vel * multiplier2

    return player_pos, x_vel, y_vel


def player_movement(pressed, player_pos, x_vel, y_vel, angle):
    global evading, evade_skip_tick
    sprinting, crouching = False, False
    if pressed[pygame.K_LSHIFT]:
        sprinting = True
    elif pressed[pygame.K_LCTRL]:
        crouching = True

    if pressed[pygame.K_SPACE] and evading == False and evade_skip_tick == 0:
        evading = True
        hor_speed = 0
        vert_speed, hor_speed = 0, 0
        if pressed[pygame.K_w]:
            vert_speed = evade_speed
        elif pressed[pygame.K_s]:
            vert_speed = -evade_speed
        if pressed[pygame.K_a]:
            hor_speed = -evade_speed
        elif pressed[pygame.K_d]:
            hor_speed = evade_speed

        try:
            scalar = evade_speed / math.sqrt(vert_speed**2 + hor_speed**2)
        except:
            scalar = 1
        y_vel_target, x_vel_target = 0, 0
        y_vel_target -= math.sin(math.radians(angle)) * vert_speed * scalar
        x_vel_target += math.cos(math.radians(angle)) * vert_speed * scalar

        y_vel_target += math.cos(math.radians(angle)) * hor_speed * scalar
        x_vel_target += math.sin(math.radians(angle)) * hor_speed * scalar

        x_vel += x_vel_target

        y_vel += y_vel_target


    speed, vert_speed, hor_speed = 0, 0, 0
    if evading == False:

        if pressed[pygame.K_w]:
            if sprinting:
                vert_speed = running_speed
            elif crouching:
                vert_speed = walking_speed * 0.35
            else:
                vert_speed = walking_speed

        if pressed[pygame.K_a]:
            if sprinting:
                hor_speed = -running_speed
            elif crouching:
                hor_speed = -walking_speed * 0.35
            else:
                hor_speed = -walking_speed

        if pressed[pygame.K_d]:
            if sprinting:
                hor_speed = running_speed
            elif crouching:
                hor_speed = walking_speed * 0.35
            else:
                hor_speed = walking_speed

        if pressed[pygame.K_s]:
            if sprinting:
                vert_speed = -running_speed
            elif crouching:
                vert_speed = -walking_speed * 0.35
            else:
                vert_speed = -walking_speed

    try:
        scalar = (
            running_speed / math.sqrt(vert_speed**2 + hor_speed**2)
            if sprinting
            else walking_speed / math.sqrt(vert_speed**2 + hor_speed**2)
        )
    except:
        scalar = 1
    if scalar > 1:
        scalar = 1

    if evading == False:
        y_vel_target, x_vel_target = 0, 0

        y_vel_target -= math.sin(math.radians(angle)) * vert_speed * scalar
        x_vel_target += math.cos(math.radians(angle)) * vert_speed * scalar

        y_vel_target += math.cos(math.radians(angle)) * hor_speed * scalar
        x_vel_target += math.sin(math.radians(angle)) * hor_speed * scalar

        x_vel += (x_vel_target - x_vel) * breaking

        y_vel += (y_vel_target - y_vel) * breaking

    if abs(x_vel) > 0.1:
        x_vel *= breaking
    else:
        x_vel = 0
    if abs(y_vel) > 0.1:
        y_vel *= breaking
    else:
        y_vel = 0

    if evading == True and math.sqrt(x_vel**2 + y_vel**2) < walking_speed:
        evading = False
        evade_skip_tick = 30

    player_pos[0] += x_vel
    player_pos[1] += y_vel

    if evade_skip_tick != 0 and not pressed[pygame.K_SPACE]:
        evade_skip_tick -= 1

    return player_pos, x_vel, y_vel


def render_player(
    screen, mouse_pos, player, player_pos, camera_pos, player_actor, firing_tick=False
):

    player_pos = [player_pos[0] - camera_pos[0], player_pos[1] - camera_pos[1]]

    angle = player_actor.get_angle()

    if firing_tick == False:
        player_rotated, player_rotated_rect = rot_center(
            player, angle, player_pos[0], player_pos[1]
        )
    else:
        player_rotated, player_rotated_rect = rot_center(
            player_firing, angle, player_pos[0], player_pos[1]
        )

    offset = [
        player_rotated_rect[0] - player_pos[0],
        player_rotated_rect[1] - player_pos[1],
    ]
    player_pos_center = player_rotated.get_rect().center
    player_pos_center = [
        player_pos[0] - player_pos_center[0],
        player_pos[1] - player_pos_center[1],
    ]

    screen.blit(player_rotated, [player_pos[0] + offset[0], player_pos[1] + offset[1]])

    for x in player_actor.unitstatuses:
        x.tick(camera_pos)



def rot_center(image, angle, x, y):

    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(center=(x, y)).center)

    return rotated_image, new_rect

def load_loop(app, screen, text):
    while app.loading:

        app.clock.tick(30)

        screen.fill((0,0,0))

        rgb_render(loadSymbolRGB, 5, [size[0] / 2 - loadSymbol.get_size()[0]/2, size[1] / 2 - loadSymbol.get_size()[1]/2], [0,0], screen)

        textSurf = terminal3.render(text, False, [100, 100, 100])
        screen.blit(textSurf, [10, size[1]-40])

        if time.time() - hint.t > 3:
            hint.hint = pick_random_from_list(hints)
            hint.t = time.time()


        hintSurf = terminal_hint.render(hint.hint, False, [50, 50, 50])
        x,y = hintSurf.get_rect().center
        screen.blit(hintSurf, [10, size[1] - 20])

        pygame.display.update()


def load_screen(app, screen, text):

    app.loading = True
    start_new_thread(load_loop, (app, screen, text))

    

def closest_value(target, lst):
    return min(lst, key=lambda x: abs(x - target))

def songBetweenDrop(song, dropTable):

    song = song.split("/")[-1]
    if song in dropTable:
        drops = dropTable[song]
    else:
        return False
    between = False
    for s, e in drops:
        if s < pygame.mixer.music.get_pos() / 1000 < e:
            return True
    return False


def camera_aling(camera_pos, target_pos):
    camera_pos = [camera_pos[0] + camera_offset[0], camera_pos[1] + camera_offset[1]]
    camera_pos = [
        camera_pos[0]
        + (-camera_pos[0] + target_pos[0]) * camera_breaking
        - camera_offset[0],
        camera_pos[1]
        + (-camera_pos[1] + target_pos[1]) * camera_breaking
        - camera_offset[1],
    ]
    return camera_pos


def keypress_manager(key_r_click, c_weapon, player_inventory, player_actor):
    if key_r_click:
        if (
            c_weapon.reload_tick() == 0
            and c_weapon.get_Ammo() != c_weapon.get_clip_size() + (1 if c_weapon.extra_bullet else 0)
        ):
            c_weapon.reload(player_inventory, player_actor, screen)
        elif c_weapon.reload_tick() != 0:
            if (
                abs(c_weapon.reload_tick() - c_weapon.__dict__["random_reload_tick"])
                <= 7
            ):
                q_r_success.play()
                c_weapon.__dict__["_reload_tick"] = 0

            elif c_weapon.__dict__["random_reload_tick"] != -1:
                q_r_fail.play()
                c_weapon.__dict__["random_reload_tick"] = -1
                c_weapon.__dict__["_reload_tick"] = c_weapon.__dict__["_reload_rate"]


def weapon_fire(app, c_weapon, player_inventory, angle, player_pos, player_actor, screen=screen, ai=False):
    firing_tick = False

    c_weapon.spread_recoverial()

    if c_weapon.jammed:
        return

    if ai:
        if c_weapon.get_semi_auto():

            if ai.semi_auto_fire_tick <= 0:
                click = True
                ai.semi_auto_fire_tick = c_weapon.ai_fire_rate_mod + random.randint(-2,2)
            else:
                click = False
                ai.semi_auto_fire_tick -= timedelta.mod(1)

        else:
            click = True
    else:
        if app.joysticks and app.detectJoysticks:
            click = app.joysticks[0].get_axis(5) > -0.5 or pygame.mouse.get_pressed()[0]
        else:
            click = pygame.mouse.get_pressed()[0]

    if c_weapon.charge_up:

        if click and c_weapon.reload_tick() == 0:
            if not c_weapon.charge_tick.tick():
                return
        else:
            c_weapon.charge_tick.value = 0

    if c_weapon.get_semi_auto():
        if c_weapon.check_for_Fire(click) == True and c_weapon.reload_tick() == 0:
            reload.stop()
            c_weapon.fire(player_pos, angle, screen, player_actor, ai = ai)
            firing_tick = True
        elif c_weapon.get_Ammo() == 0 and (
            player_inventory.get_amount_of_type(c_weapon.__dict__["ammo"])
            or c_weapon.__dict__["ammo"] == "INF"
        ):

            reload_tick = c_weapon.reload(player_inventory, player_actor, screen)

            for x in weapon_fire_Sounds:
                x.stop()

    elif c_weapon.__dict__["burst"]:

        if c_weapon.__dict__["burst_tick"] != 0:
            c_weapon.__dict__["burst_tick"] -= 1

        if (
            c_weapon.check_for_Fire(click) == True
            and c_weapon.reload_tick() == 0
            and c_weapon.weapon_fire_Tick() <= 0
        ):

            c_weapon.__dict__["current_burst_bullet"] = min(
                c_weapon.__dict__["burst_bullets"], c_weapon.get_Ammo()
            )

            reload.stop()
            c_weapon.fire(player_pos, angle, screen, player_actor, ai = ai)
            firing_tick = True

        else:

            if (
                c_weapon.__dict__["burst_tick"] == 0
                and c_weapon.__dict__["current_burst_bullet"] != 0
            ):

                c_weapon.fire(player_pos, angle, screen, player_actor, ai = ai)
                firing_tick = True

            elif c_weapon.get_Ammo() == 0 and (
                player_inventory.get_amount_of_type(c_weapon.__dict__["ammo"]) > 0
                or c_weapon.__dict__["ammo"] == "INF"
            ):
                reload_tick = c_weapon.reload(player_inventory, player_actor, screen)

                for x in weapon_fire_Sounds:
                    x.stop()

    else:
        if (
            c_weapon.check_for_Fire(click) == True
            and c_weapon.weapon_fire_Tick() <= 0
            and c_weapon.reload_tick() == 0
        ):  ##FIRE
            while (
                c_weapon.weapon_fire_Tick() <= 0
                and c_weapon.check_for_Fire(click) == True
                and not c_weapon.jammed
            ):
                reload.stop()
                c_weapon.fire(player_pos, angle, screen, player_actor, ai = ai)
                firing_tick = True

        elif c_weapon.get_Ammo() == 0 and (
            player_inventory.get_amount_of_type(c_weapon.__dict__["ammo"]) > 0
            or c_weapon.__dict__["ammo"] == "INF"
        ):
            reload_tick = c_weapon.reload(player_inventory, player_actor, screen)

            for x in weapon_fire_Sounds:
                x.stop()


    c_weapon.weapon_tick()

    return firing_tick


def get_point_from_list(point, dict):
    for point_2 in dict:
        if point == point_2["point"]:
            return point_2

def check_route(point,endpoint,route, walls):
    last = point
    rou = route.copy()
    rou.append(endpoint)
    for x in rou:
        if not los.check_los(last, x, walls):
            return [last, x]
        last = x
    return False


def calc_route(start_pos, end_pos, NAV_MESH, walls, quick=True, cache = False):
    """
    Calculates the shortest route to a point using the navmesh points
    """

    return find_shortest_path(start_pos, end_pos, NAV_MESH, walls, quick=quick, cache = cache)


def draw_HUD(
    screen,
    player_inventory,
    cam_delta,
    camera_pos,
    weapon,
    player_weapons,
    player_actor,
    mouse_pos,
    clicked,
    r_click_tick,
    wave,
    wave_anim_ticks,
    wave_text_tick,
    wave_number,
    wave_text_color,
    beat_red,
    app,
):
    global last_hp, damage_ticks

    hp = min([round(player_actor.__dict__["hp"]), 100])

    heartbeat_tick.tick()
    heartbeat_value = (1 - heartbeat_tick.value / 30 * (100 - hp) / 100) ** 2
    if wave:
        pygame.draw.rect(
            screen,
            [255, 0, 0],
            [-1, -1, size[0] + 2, size[1] + 2],
            round((beat_red - 0.8) * 5*multiplier2),
        )

    hud_color = [
        20 + round(200 * heartbeat_value) + round(35 * player_actor.hp / 100),
        round(255 * player_actor.hp / 100),
        round(255 * player_actor.hp / 100),
    ]
    x_d, y_d = cam_delta
    x_d = -x_d
    y_d = -y_d

    try:
        if hp < last_hp:
            damage_ticks = round((last_hp - hp) ** 0.6)

        if damage_ticks != 0:
            mpl = 4
            x_d += random.uniform(-damage_ticks * mpl, damage_ticks * mpl)
            y_d += random.uniform(-damage_ticks * mpl, damage_ticks * mpl)
            damage_ticks -= 1
    except Exception as e:
        print(e)

    hp_d = 10 - player_actor.hp / 10

    x_d += random.uniform(-hp_d, hp_d)
    y_d += random.uniform(-hp_d, hp_d)
    clip_size = weapon.get_clip_size()
    clip = round(weapon.get_Ammo())
    pl_pos = minus_list(player_actor.get_pos(), camera_pos)
    pl_angl = player_actor.__dict__["aim_angle"]
    pl_angl2 = player_actor.get_angle()

    positive = player_actor.money - player_actor.money_last_tick >= 0

    if not money_tick.tick() and not player_inventory.inventory_open:

        if money_tick.value <= money_tick.max_value / 6:
            x = 15 - 1 / ((money_tick.value + 1) ** 1.5) * 40
        elif (
            money_tick.max_value / 6 < money_tick.value <= 4 * money_tick.max_value / 6
        ):
            x = 15
        else:
            x = 15 - 1 / ((money_tick.max_value + 3 - money_tick.value) ** 1.2) * 40
        pre_tense = "+" if positive else ""
        text = terminal.render(
            f"{pre_tense}{player_actor.money - player_actor.money_last_tick}$",
            False,
            [0, random.randint(155, 255), 0] if positive else [random.randint(155, 255), 0, 0],
        )
        screen.blit(text, (x + x_d, 380 + y_d))  #

    else:
        player_actor.money_last_tick = player_actor.money

    pl_dist = los.get_dist_points(pl_pos, mouse_pos)
    # if pl_dist < 100:
    #     pl_dist = 100

    pl_dist_mult = (pl_dist / 25)  * multiplier2

    spread = weapon.__dict__["_c_bullet_spread"] + weapon.__dict__["_spread"]

    if not pygame.mouse.get_visible():

        if weapon.__dict__["_reload_tick"] == 0:

            pos7 = [
                pl_pos[0] + math.cos(math.radians(pl_angl2)) * (pl_dist - pl_dist_mult),
                pl_pos[1] - math.sin(math.radians(pl_angl2)) * (pl_dist - pl_dist_mult),
            ]
            pos8 = [
                pl_pos[0] + math.cos(math.radians(pl_angl2)) * (pl_dist + pl_dist_mult),
                pl_pos[1] - math.sin(math.radians(pl_angl2)) * (pl_dist + pl_dist_mult),
            ]

            pos2 = line = [
                pl_pos[0]
                + math.cos(math.radians(pl_angl - spread)) * (pl_dist + pl_dist_mult),
                pl_pos[1]
                - math.sin(math.radians(pl_angl - spread)) * (pl_dist + pl_dist_mult),
            ]
            pos3 = line = [
                pl_pos[0]
                + math.cos(math.radians(pl_angl + spread)) * (pl_dist + pl_dist_mult),
                pl_pos[1]
                - math.sin(math.radians(pl_angl + spread)) * (pl_dist + pl_dist_mult),
            ]

            pos1 = line = [
                pl_pos[0]
                + math.cos(math.radians(pl_angl - spread)) * (pl_dist - pl_dist_mult),
                pl_pos[1]
                - math.sin(math.radians(pl_angl - spread)) * (pl_dist - pl_dist_mult),
            ]
            pos4 = line = [
                pl_pos[0]
                + math.cos(math.radians(pl_angl + spread)) * (pl_dist - pl_dist_mult),
                pl_pos[1]
                - math.sin(math.radians(pl_angl + spread)) * (pl_dist - pl_dist_mult),
            ]

            pos5 = line = [
                pl_pos[0]
                + math.cos(math.radians(pl_angl)) * (pl_dist - pl_dist_mult * 2),
                pl_pos[1]
                - math.sin(math.radians(pl_angl)) * (pl_dist - pl_dist_mult * 2),
            ]
            pos6 = line = [
                pl_pos[0] + math.cos(math.radians(pl_angl)) * (pl_dist + pl_dist_mult),
                pl_pos[1] - math.sin(math.radians(pl_angl)) * (pl_dist + pl_dist_mult),
            ]

            pygame.draw.line(screen, [255, 0, 0], pos7, pos8, round(2 * multiplier2))
            pygame.draw.line(screen, hud_color, pos1, pos2, round(2 * multiplier2))
            pygame.draw.line(screen, hud_color, pos4, pos3, round(2 * multiplier2))
            pygame.draw.line(screen, hud_color, pos5, pos6, round(3 * multiplier2))

        else:

            circular = False

            if circular:  # VERY UGLE

                rect = pygame.Rect(mouse_pos[0] - 10, mouse_pos[1] - 10, 20, 20)
                rect2 = pygame.Rect(mouse_pos[0] - 16, mouse_pos[1] - 16, 32, 32)
                rect3 = pygame.Rect(mouse_pos[0] - 12, mouse_pos[1] - 12, 24, 24)

                angle = 5 * math.pi / 2 - math.pi * 2 * (
                    weapon.__dict__["_reload_tick"] / weapon.__dict__["_reload_rate"]
                )

                pygame.draw.arc(
                    screen, hud_color, rect, math.pi / 2, 5 * math.pi / 2, 2
                )
                pygame.draw.arc(
                    screen, hud_color, rect2, math.pi / 2, 5 * math.pi / 2, 2
                )
                pygame.draw.arc(screen, hud_color, rect3, math.pi / 2, angle, 2)

                if weapon.__dict__["random_reload_tick"] != -1:
                    angle1 = 5 * math.pi / 2 - math.pi * 2 * (
                        (weapon.__dict__["random_reload_tick"] - 2)
                        / weapon.__dict__["_reload_rate"]
                    )
                    angle2 = 5 * math.pi / 2 - math.pi * 2 * (
                        (weapon.__dict__["random_reload_tick"] + 2)
                        / weapon.__dict__["_reload_rate"]
                    )
                    pygame.draw.arc(
                        screen, [0, 0, 255], rect2, angle1, angle2 - angle1, 6
                    )

            else:
                rect = pygame.Rect(mouse_pos[0] + x_d, mouse_pos[1] + y_d, 0, 0)
                rect.inflate_ip(10, 30)

                height = (
                    22
                    * weapon.__dict__["_reload_tick"]
                    / weapon.__dict__["_reload_rate"]
                )

                rect2 = pygame.Rect(
                    mouse_pos[0] - 2 + x_d, mouse_pos[1] - height + 12 + y_d, 4, height
                )

                if weapon.__dict__["random_reload_tick"] != -1:

                    if (
                        abs(
                            weapon.reload_tick() - weapon.__dict__["random_reload_tick"]
                        )
                        <= 7
                    ):
                        color = [0, 255, 0]

                        rect5 = pygame.Rect(
                            mouse_pos[0] + x_d, mouse_pos[1] + y_d, 0, 0
                        )
                        rect5.inflate_ip(
                            10
                            + (
                                8
                                - abs(
                                    weapon.reload_tick()
                                    - weapon.__dict__["random_reload_tick"]
                                )
                            ),
                            30
                            + (
                                8
                                - abs(
                                    weapon.reload_tick()
                                    - weapon.__dict__["random_reload_tick"]
                                )
                            ),
                        )
                        pygame.draw.rect(screen, color, rect5, 2)
                    else:
                        color = hud_color

                    q_r_pos1 = (
                        22
                        * (weapon.__dict__["random_reload_tick"] - 7)
                        / weapon.__dict__["_reload_rate"]
                    )
                    q_r_pos2 = (
                        22
                        * (weapon.__dict__["random_reload_tick"] + 7)
                        / weapon.__dict__["_reload_rate"]
                    )

                    rect3 = pygame.Rect(
                        mouse_pos[0] - 2 + x_d,
                        mouse_pos[1] - q_r_pos2 + 12 + y_d,
                        4,
                        q_r_pos2 - q_r_pos1,
                    )

                else:
                    color = RED_COLOR

                pygame.draw.rect(screen, color, rect, 2)
                pygame.draw.rect(screen, color, rect2)
                if weapon.__dict__["random_reload_tick"] != -1:
                    pygame.draw.rect(screen, [0, 255, 0], rect3)

    wave_surf = pygame.Surface((size[0], 30), pygame.SRCALPHA, 32).convert_alpha()
    wave_surf.set_colorkey([255, 255, 255])
    if wave or wave_anim_ticks[0] > 0:
        wave_end_tick, wave_start_tick = wave_anim_ticks


        inverted = wave_text_color
        # if beat_blink.value%(beat_blink.max_value/2) < (beat_blink.max_value/4) and beat_blink.value < beat_blink.max_value:
        #     inverted = not inverted

        if inverted:
            color1 = [255, 255, 255]
            color2 = [255, 0, 0]
        else:
            color2 = [255, 255, 255]
            color1 = [255, 0, 0]

        if wave_start_tick > 0:

            pygame.draw.rect(
                wave_surf,
                color2,
                [0, 0, (1 - wave_start_tick / 120) ** 3 * size[0], 30],
            )

        elif wave_end_tick > 0:

            pygame.draw.rect(
                wave_surf,
                color2,
                [(1 - wave_end_tick / 120) ** 3 * size[0], 0, size[0], 30],
            )

        else:
            pygame.draw.rect(wave_surf, color2, [0, 0, size[0], 30])

        for x in range(0, round(wave_text_tick * 4 / 200)):
            mod = 0
            if wave_end_tick != 0:
                mod = (1 - wave_end_tick / 120) ** 3 * size[0]

            if wave_text_tick * 2 - 200 - x * 200 + mod > size[0]:
                continue

            text = terminal4.render("WAVE " + str(wave_number), False, color1)
            wave_surf.blit(text, [wave_text_tick * 4 - 300 - x * 200 + mod, -3])  #

    screen.blit(wave_surf, (0, 10 + y_d))

    try:
        im = weapon.image
        if weapon.jammed:
            blit_glitch(screen, im, [5 + x_d, 5 + y_d], glitch = 20, black_bar_chance = 7)
        else:
            screen.blit(im, [5 + x_d, 5 + y_d])

        if weapon.charge_up and weapon.charge_tick.value != 0:
            size1 = weapon.image_red.get_rect().size
            screen.blit(
                weapon.image_red,
                [5 + x_d, 5 + y_d],
                area=[
                    0,
                    0,
                    size1[0] * weapon.charge_tick.value / weapon.charge_tick.max_value,
                    size1[1],
                ],
            )

    except Exception as e:
        print(e)

    if not weapon.jammed:

        if weapon.__dict__["_reload_tick"] == 0:
            if clip == clip_size + 1:
                text = terminal.render(
                    str(clip - 1) + "+1/" + str(clip_size), False, hud_color
                )
                screen.blit(text, (15 + x_d, 45 + y_d))  #
            else:
                if clip == 0:
                    color = [255, 0, 0]
                else:
                    color = hud_color

                text = terminal.render(str(clip) + "/" + str(clip_size), False, color)
                screen.blit(text, (15 + x_d, 45 + y_d))  #

            if (
                player_inventory.get_amount_of_type(weapon.__dict__["ammo"]) < clip_size
                and weapon.__dict__["ammo"] != "INF"
            ):
                color = [255, 0, 0]
            else:
                color = hud_color

            if weapon.__dict__["ammo"] == "INF":
                text = terminal.render("+INF", False, color)
                screen.blit(text, (110 + x_d, 45 + y_d))  #
            else:

                text = terminal.render(
                    "+"
                    + str(player_inventory.get_amount_of_type(weapon.__dict__["ammo"]))
                    + " res.",
                    False,
                    color,
                )
                screen.blit(text, (110 + x_d, 45 + y_d))  #

        else:
            text = terminal.render("reloading...", False, hud_color)
            screen.blit(text, (15 + x_d, 45 + y_d))  #

        if weapon.get_semi_auto():
            text = terminal3.render("Semi-Automatic", False, hud_color)
            screen.blit(text, (15 + x_d, 65 + y_d))  #

            text = terminal3.render(str(weapon.__dict__["ammo"]), False, hud_color)
            screen.blit(text, (110 + x_d, 65 + y_d))  #

        elif weapon.__dict__["burst"]:

            text = terminal3.render("Burst-fire", False, hud_color)
            screen.blit(text, (15 + x_d, 65 + y_d))  #

            text = terminal3.render(str(weapon.__dict__["ammo"]), False, hud_color)
            screen.blit(text, (80 + x_d, 65 + y_d))  #

            text = terminal3.render(
                str(weapon.__dict__["_bullet_per_min"]) + "RPM", False, hud_color
            )
            screen.blit(text, (150 + x_d, 65 + y_d))  #

        else:
            text = terminal3.render(
                "Automatic" if not weapon.charge_up else "Charge-Up", False, hud_color
            )
            screen.blit(text, (15 + x_d, 65 + y_d))  #

            text = terminal3.render(str(weapon.__dict__["ammo"]), False, hud_color)
            screen.blit(text, (80 + x_d, 65 + y_d))  #

            ammo_text_len = 80 + text.get_rect().size[0] + 20
            # print(ammo_text_len)

            text = terminal3.render(
                str(weapon.__dict__["_bullet_per_min"]) + "RPM", False, hud_color
            )
            screen.blit(text, (max([150 + x_d, ammo_text_len + x_d]), 65 + y_d))  #

    else:
        if app.three_second_tick%10 < 5:
            text = terminal4.render("JAMMED!", False, [255, 0, 0])
            screen.blit(text, [5 + x_d, 40 + y_d])  #

    player_actor.update_nade(player_inventory)

    if player_actor.preferred_nade == "HE Grenade":
        screen.blit(grenade_ico, [240 + x_d, 5 + y_d])
        nades = player_inventory.get_amount_of_type("HE Grenade")

        x,y = grenade_ico.get_size()

        text = terminal.render(str(nades), False, [255, 255, 255] if nades else [255,0,0])

        x1, y1 = text.get_size()

        screen.blit(text, [240 + x_d + x - x1, 5 + y_d + y - y1])  #

    elif player_actor.preferred_nade == "Molotov":
        screen.blit(molotov_ico, [240 + x_d, 5 + y_d])
        nades = player_inventory.get_amount_of_type("Molotov")

        x,y = molotov_ico.get_size()

        text = terminal.render(str(nades), False, [255, 255, 255])

        x1, y1 = text.get_size()

        screen.blit(text, [240 + x_d + x - x1, 5 + y_d + y - y1])  #


    y_pos = 80

    for w_1 in player_weapons:
        if w_1 == weapon:
            screen.blit(w_1.icon_active, [20 + x_d, y_pos + y_d])
            pygame.draw.rect(screen, [0, 255, 0], [20 + x_d, y_pos + y_d, 30, 10], 1)
        elif (
            player_inventory.get_amount_of_type(w_1.ammo) != 0
            or w_1.ammo == "INF"
            or w_1.get_Ammo() != 0
        ):
            screen.blit(w_1.icon, [20 + x_d, y_pos + y_d])

        else:
            screen.blit(w_1.icon_no_ammo, [20 + x_d, y_pos + y_d])
        y_pos += 15

    bars = round((hp - 5) / 10)

    sanity = player_actor.__dict__["sanity"]
    bars_s = round((sanity) / 10)

    if sanity < 40 and app.three_second_tick%20 > 10:

        text = terminal3.render("CONSUME NARCOTICS TO REGAIN CONTROL", False, hud_color)
        screen.blit(text, (size[0] - 217 + x_d, size[1] - 100 + y_d))

    amount, tick = player_actor.get_sanity_change()
    if amount != False:

        if tick >= 60:

            bars_s = round((sanity - (amount * (tick - 60) / 30)) / 10)

        text = terminal3.render(str(amount) + "% SANITY REGAINED", False, hud_color)
        if 1 < tick <= 10:
            screen.blit(
                text, (size[0] - 12 + x_d + (400 / tick) - text.get_rect().size[0], size[1] - 80 + y_d)
            )  #
        elif 10 < tick <= 60:
            screen.blit(text, (size[0] - 12 + x_d - text.get_rect().size[0], size[1] - 80 + y_d))  #
        else:
            screen.blit(
                text,
                (
                    size[0] - 12 + 150 - 300 / (tick - 59) + x_d - text.get_rect().size[0],
                    size[1] - 80 + y_d,
                ),
            )

    text = terminal2.render("SANITY", False, hud_color)
    screen.blit(text, (size[0] - 10 + x_d - text.get_rect().size[0], size[1] - 68 + y_d))  #

    pygame.draw.rect(screen, hud_color, [size[0] - 223 + x_d, size[1] - 40 + y_d, 210, 30], 3)
    for i in range(bars_s):
        pygame.draw.rect(screen, hud_color, [size[0] - 36 - i * 20 + x_d, size[1] - 34 + y_d, 16, 18])

    text = terminal2.render("HP", False, hud_color)
    screen.blit(text, (12 + x_d, size[1] - 68 + y_d))  #

    pygame.draw.rect(screen, hud_color, [15 + x_d, size[1] - 40 + y_d, 210, 30], 3)
    for i in range(bars):
        pygame.draw.rect(screen, hud_color, [22 + i * 20 + x_d, size[1] - 34 + y_d, 16, 18])

    text = terminal2.render(str(weapon.__dict__["name"]), False, hud_color)
    screen.blit(text, (15 + x_d, 15 + y_d))  #

    player_inventory.draw_inventory(
        screen,
        x_d,
        y_d,
        mouse_pos,
        clicked,
        player_actor.get_pos(),
        r_click_tick,
        player_actor,
        app
    )

    last_hp = hp
