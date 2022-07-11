import os, sys
import pygame
import math
import random
import time
from values import *
import classes
import los
pygame.init()
pygame.font.init()

agency = pygame.font.Font('texture/agencyb.ttf', round(70))
terminal = pygame.font.Font('texture/terminal.ttf', 20)
terminal2 = pygame.font.Font('texture/terminal.ttf', 30)
terminal3 = pygame.font.Font('texture/terminal.ttf', 10)
terminal4 = pygame.font.Font('texture/terminal.ttf', 40)

evade_skip_tick = 0
acceleration = 200/1.875
velocity_cap = 9/1.875
breaking = 0.9
walking_speed = 7/1.875
running_speed = 13/1.875
evade_speed = 30/1.875
camera_breaking = 0.1/1.875
evading = False
tick_count = 60

camera_offset = [size[0]/2 , size[1]/2]

def debug_render(text_str):
    text = agency.render(str(text_str), False, [255,255,0])
    render_cool(text, [1000,60],15,16,render = True, offset = 10)   ### IN GAME

def print_s(screen,text_str,slot, color = hud_color):
    text = terminal.render(str(text_str), False, color)
    screen.blit(text, (size[0] - 10 - text.get_rect().size[0], slot*30)) #

def load_animation(directory, start_frame, frame_count):
    list = []
    for x in range(frame_count):
        x = x+start_frame
        im_dir = directory + "/" + (4-len(str(x)))*"0" + str(x) + ".png"
        print(im_dir)

        im = pygame.image.load(im_dir).convert_alpha()
        list.append(im)

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


def BezierInterpolation(positions, t):

    P0_x = pow((1-t), 2) * positions[0][0]
    P0_y = pow((1-t), 2) * positions[0][1]

    P1_x = 2 * (1-t) * t * positions[1][0]
    P1_y = 2 * (1-t) * t * positions[1][1]

    P2_x = t ** 2 * positions[2][0]
    P2_y = t ** 2 * positions[2][1]

    curve = (P0_x + P1_x + P2_x, P0_y + P1_y + P2_y)
    return list(curve)


def rgb_render(list, amount, pos, cam_delta, screen):

    #rect_pos = list[0].get_rect(center = list[0].get_rect(center = (pos[0], pos[1])).center)
    amount = amount * 0.6
    pos[1] = pos[1] + random.uniform(-amount,amount)



    screen.blit(pick_random_from_list(list[1:]),[pos[0] + 20 + random.uniform(-amount,amount) + cam_delta[0]*2, pos[1] + random.uniform(-amount,amount) + cam_delta[1]*2])

    screen.blit(list[0], [pos[0] + 20 + cam_delta[0], pos[1] + cam_delta[1]])







def get_dist_points(point_1,point_2):
    return math.sqrt((point_2[0] - point_1[0])**2 + (point_2[1] - point_1[1])**2)

def render_cool(image,pos,tick,beat_tick_h,render = False, offset = 0, scale = 1,screen = screen , style = "default", alpha = 255):

    a = 1 - math.sin(offset+10*tick/(2*math.pi*beat_tick_h))*0.1 * scale
    b = 1 - math.sin(math.pi/2 +offset+10*tick/(2*math.pi*beat_tick_h))*0.1 * scale
    rotation = math.sin(math.pi/2 +offset+10*tick/(2*math.pi*beat_tick_h))*2 * scale
    if style == "default":
        image_size = image.get_rect().size
        image_size_2 = [round(image_size[0]*a),round(image_size[1]*b)]

        image_2 = pygame.transform.scale(image,image_size_2)

        pos = [pos[0] - a/4 * image_size_2[0], pos[1] - b/4 * image_size_2[1]]

        if render == True:
            image_2, image_2_rot = rot_center(image_2,rotation,pos[0],pos[1])

        screen.blit(image_2,pos)

def check_for_render(player_pos,pos,range = 3000):
    if range < math.sqrt((player_pos[0] - pos[0])**2 + (player_pos[1] - pos[1])**2):
        return True
    return False

def get_angle(pos1,pos2):
    myradians = math.atan2(pos2[1]-pos1[1], pos2[0]-pos1[0])
    mydegrees = math.degrees(myradians)
    return mydegrees

def mult(list1, am):
    try:
        list_1 = list1.copy()
    except:
        list_1 = list1

    for x in range(len(list1)):
        list_1[x] *= am
    return list_1


def minus(list1,list2, op = "+"):
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
    return list[random.randint(0,len(list)-1)]

def pick_random_from_dict(dict, key = False):
    dict_keys = list(dict.keys())
    if key:
        return dict_keys[random.randint(0,len(dict_keys)-1)]
    else:
        return dict[dict_keys[random.randint(0,len(dict_keys)-1)]]

def minus_list(list1,list2):
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
    return pygame.transform.scale(im,size)

def draw_pos(pos,cam_pos, x_off = 0, y_off = 0):
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


def player_movement2(pressed, player_pos, x_vel, y_vel):
    global evading, evade_skip_tick

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



        if (x_vel, y_vel) != (0,0):
            evade_skip_tick = 30
            evading = True



    if evading == False:

        if pressed[pygame.K_LSHIFT]:
            sprinting = True
            velocity_cap = timedelta.mod(9/1.875)
        elif pressed[pygame.K_LCTRL]:
            crouching = True
            velocity_cap = timedelta.mod(2.75/1.875)
        else:
            sprinting = False
            velocity_cap = timedelta.mod(5/1.875)
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
        velocity_cap = timedelta.mod(5/1.875)
        x_acc, y_acc = 0,0

        if math.sqrt(x_vel**2 + y_vel**2) < velocity_cap:
            evading = False


    if abs(x_vel) < velocity_cap:
        x_vel += timedelta.mod(x_acc/tick_count)
    if abs(y_vel) < velocity_cap:
        y_vel += timedelta.mod(y_acc/tick_count)

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


    player_pos[0] += x_vel
    player_pos[1] += y_vel

    return player_pos, x_vel, y_vel

def player_movement(pressed, player_pos,x_vel, y_vel, angle):
    global evading, evade_skip_tick
    sprinting, crouching = False, False
    if pressed[pygame.K_LSHIFT]:
        sprinting = True
    elif pressed[pygame.K_LCTRL]:
        crouching = True




    if pressed[pygame.K_SPACE] and evading == False and evade_skip_tick == 0:
        evading = True
        hor_speed = 0
        vert_speed, hor_speed = 0,0
        if pressed[pygame.K_w]:
            vert_speed = evade_speed
        elif pressed[pygame.K_s]:
            vert_speed = -evade_speed
        if pressed[pygame.K_a]:
            hor_speed = -evade_speed
        elif pressed[pygame.K_d]:
            hor_speed = evade_speed

        try:
            scalar = (evade_speed/math.sqrt(vert_speed ** 2 + hor_speed **2))
        except:
            scalar = 1
        y_vel_target, x_vel_target = 0,0
        y_vel_target -= math.sin(math.radians(angle)) * vert_speed * scalar
        x_vel_target += math.cos(math.radians(angle)) * vert_speed * scalar

        y_vel_target += math.cos(math.radians(angle)) * hor_speed * scalar
        x_vel_target += math.sin(math.radians(angle)) * hor_speed * scalar



        x_vel += (x_vel_target)

        y_vel += (y_vel_target)

        print("EVADE SPEED:", x_vel, y_vel)







    speed, vert_speed, hor_speed = 0,0,0
    if evading == False:

        if pressed[pygame.K_w]:
            if sprinting:
                vert_speed = running_speed
            elif crouching:
                vert_speed = walking_speed*0.35
            else:
                vert_speed = walking_speed

        if pressed[pygame.K_a]:
            if sprinting:
                hor_speed = -running_speed
            elif crouching:
                hor_speed = -walking_speed*0.35
            else:
                hor_speed = -walking_speed

        if pressed[pygame.K_d]:
            if sprinting:
                hor_speed = running_speed
            elif crouching:
                hor_speed = walking_speed*0.35
            else:
                hor_speed = walking_speed


        if pressed[pygame.K_s]:
            if sprinting:
                vert_speed = -running_speed
            elif crouching:
                vert_speed = -walking_speed*0.35
            else:
                vert_speed = -walking_speed




    try:
        scalar = (running_speed/math.sqrt(vert_speed ** 2 + hor_speed **2) if sprinting else walking_speed/math.sqrt(vert_speed ** 2 + hor_speed **2))
    except:
        scalar = 1
    if scalar > 1:
        scalar = 1

    if evading == False:
        y_vel_target, x_vel_target = 0,0

        y_vel_target -= math.sin(math.radians(angle)) * vert_speed * scalar
        x_vel_target += math.cos(math.radians(angle)) * vert_speed * scalar

        y_vel_target += math.cos(math.radians(angle)) * hor_speed * scalar
        x_vel_target += math.sin(math.radians(angle)) * hor_speed * scalar

        x_vel += (x_vel_target-x_vel)*breaking

        y_vel += (y_vel_target-y_vel)*breaking

    if abs(x_vel) > 0.1:
        x_vel *= breaking
    else:
        x_vel = 0
    if abs(y_vel) > 0.1:
        y_vel *= breaking
    else:
        y_vel = 0

    if evading == True and math.sqrt(x_vel ** 2 + y_vel **2) < walking_speed:
        print("")
        pass
        evading = False
        evade_skip_tick = 30

    player_pos[0] += x_vel
    player_pos[1] += y_vel


    if evade_skip_tick != 0 and not pressed[pygame.K_SPACE]:
        evade_skip_tick -= 1



    return player_pos, x_vel, y_vel

def render_player(screen, mouse_pos, player, player_pos, camera_pos, player_actor,firing_tick = False):

    player_pos = [player_pos[0] - camera_pos[0],player_pos[1] - camera_pos[1]]



    angle = player_actor.get_angle()


    if firing_tick == False:
        player_rotated, player_rotated_rect = rot_center(player,angle,player_pos[0],player_pos[1])
    else:
        player_rotated, player_rotated_rect = rot_center(player_firing,angle,player_pos[0],player_pos[1])

    offset = [player_rotated_rect[0]-player_pos[0], player_rotated_rect[1]-player_pos[1]]
    player_pos_center = player_rotated.get_rect().center
    player_pos_center = [player_pos[0]-player_pos_center[0],player_pos[1]-player_pos_center[1]]

    screen.blit(player_rotated,[player_pos[0]+offset[0],player_pos[1]+offset[1]])


def rot_center(image, angle, x, y):

    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(center = (x, y)).center)

    return rotated_image, new_rect

def camera_aling(camera_pos,target_pos):
    camera_pos = [camera_pos[0] + camera_offset[0], camera_pos[1] + camera_offset[1]]
    camera_pos = [camera_pos[0] + (-camera_pos[0] + target_pos[0])*camera_breaking - camera_offset[0], camera_pos[1] + (-camera_pos[1] + target_pos[1])*camera_breaking - camera_offset[1]]
    return camera_pos

def keypress_manager(key_r_click,c_weapon, player_inventory):
    if key_r_click:
        if c_weapon.reload_tick() == 0 and c_weapon.get_Ammo() != c_weapon.get_clip_size()+1:
            c_weapon.reload(player_inventory)
        elif c_weapon.reload_tick() != 0:
            if abs(c_weapon.reload_tick() - c_weapon.__dict__["random_reload_tick"]) <= 7:
                print("Successful quick reload")
                q_r_success.play()
                c_weapon.__dict__["_reload_tick"] = 0

            elif c_weapon.__dict__["random_reload_tick"] != -1:
                print("Reload failed")
                q_r_fail.play()
                c_weapon.__dict__["random_reload_tick"] = -1
                c_weapon.__dict__["_reload_tick"] = c_weapon.__dict__["_reload_rate"]


def weapon_fire(c_weapon, player_inventory, angle, player_pos, screen = screen, ai = False):
    firing_tick = False
    if ai:
        if c_weapon.get_semi_auto():

            click = pick_random_from_list([True,False,False,False,False,False,False,False,False,False,False,False,False])

        else:
            click = True
    else:
        click = pygame.mouse.get_pressed()[0]

    if c_weapon.get_semi_auto():
        if c_weapon.check_for_Fire(click) == True and c_weapon.reload_tick() == 0:
            reload.stop()
            c_weapon.fire(player_pos,angle,screen)
            firing_tick = True
        elif c_weapon.get_Ammo() == 0 and (player_inventory.get_amount_of_type(c_weapon.__dict__["ammo"]) or c_weapon.__dict__["ammo"] == "INF"):

            reload_tick = c_weapon.reload(player_inventory)

            for x in weapon_fire_Sounds:
                x.stop()

    elif c_weapon.__dict__["burst"]:

        if c_weapon.__dict__["burst_tick"] != 0:
            c_weapon.__dict__["burst_tick"] -= 1


        if c_weapon.check_for_Fire(click) == True and c_weapon.reload_tick() == 0 and c_weapon.weapon_fire_Tick() <= 0:

            c_weapon.__dict__["current_burst_bullet"] = min(c_weapon.__dict__["burst_bullets"],c_weapon.get_Ammo())

            reload.stop()
            c_weapon.fire(player_pos,angle,screen)
            firing_tick = True

        else:

            if c_weapon.__dict__["burst_tick"] == 0 and c_weapon.__dict__["current_burst_bullet"] != 0:

                c_weapon.fire(player_pos,angle,screen)
                firing_tick = True

            elif c_weapon.get_Ammo() == 0 and (player_inventory.get_amount_of_type(c_weapon.__dict__["ammo"]) > 0 or c_weapon.__dict__["ammo"] == "INF"):
                reload_tick = c_weapon.reload(player_inventory)

                for x in weapon_fire_Sounds:
                    x.stop()






    else:
        if c_weapon.check_for_Fire(click) == True and  c_weapon.weapon_fire_Tick() <= 0 and c_weapon.reload_tick() == 0:##FIRE
            while c_weapon.weapon_fire_Tick() <= 0 and c_weapon.check_for_Fire(click) == True:
                reload.stop()
                c_weapon.fire(player_pos,angle,screen)
                firing_tick = True


        elif c_weapon.get_Ammo() == 0 and (player_inventory.get_amount_of_type(c_weapon.__dict__["ammo"]) > 0 or c_weapon.__dict__["ammo"] == "INF"):
            reload_tick = c_weapon.reload(player_inventory)

            for x in weapon_fire_Sounds:
                x.stop()



    c_weapon.spread_recoverial()
    c_weapon.weapon_tick()

    return firing_tick

def get_point_from_list(point,dict):
    for point_2 in dict:
        if point == point_2["point"]:
            return point_2




def calc_route(start_pos, end_pos, NAV_MESH, walls, quick = True):
    """
    Calculates the shortest route to a point using the navmesh points
    """

    if los.check_los(start_pos, end_pos, walls):
        return [end_pos]
    dist_start = {}
    dist_end = {}
    for nav_point in NAV_MESH:
        point = nav_point["point"]
        if los.check_los(start_pos, point, walls):
            dist_start[los.get_dist_points(start_pos, point)] = nav_point
        if los.check_los(end_pos, point, walls):
            dist_end[los.get_dist_points(end_pos, point)] = nav_point
    try:
        start_nav_point = dist_start[min(dist_start.keys())]
        end_nav_point = dist_end[min(dist_end.keys())]
    except:
        return [end_pos]


    complete_routes = []
    routes = []
    for conne in start_nav_point["connected"]:
        routes.append([start_nav_point["point"], conne])

    while routes != []:
        if len(complete_routes) > 3:
            # print("ROUTES SHOOT OVER 2000!")
            # for route in routes:
            #
            #     print(route)   #sometimes continues infinetely, so the loop must be broken
            break
        route = pick_random_from_list(routes)
        routes.remove(route)
        point = route[-1]
        point_2 = get_point_from_list(point, NAV_MESH)
        if end_nav_point["point"] in point_2["connected"]:
            route.append(end_nav_point["point"])
            complete_routes.append(route)

        else:
            for point_3 in point_2["connected"]:
                if point_3 in route:
                    continue
                if route.copy() + [point_3] in routes:
                    continue
                routes.append(route.copy() + [point_3])
    shortest_route = {"dist" : 10000, "route" : []}


    for route in complete_routes:
        route_ref = {"dist" : 0, "route" : route}
        last_pos = start_pos
        for point in route:
            route_ref["dist"] += los.get_dist_points(last_pos, point)

        if route_ref["dist"] < shortest_route["dist"]:
            shortest_route = route_ref

    if not quick:
        obs_points = []
        last_point = None
        for route_point in shortest_route["route"]:
            if last_point == None:
                last_point = route_point
                continue
            if los.check_los(start_pos, route_point, walls):
                obs_points.append(last_point)
                last_point = route_point
            else:
                break

        last_point = None
        for route_point in reversed(shortest_route["route"]):
            if last_point == None:
                last_point = route_point
                continue
            if los.check_los(end_pos, route_point, walls):
                obs_points.append(last_point)
                last_point = route_point
            else:
                break

        for point in obs_points:
            try:
                shortest_route["route"].remove(obs_points)
            except:
                print("COULDNT DELETE POINT")




    return shortest_route["route"]







def draw_HUD(screen, player_inventory, cam_delta, camera_pos, weapon, player_weapons, player_actor, mouse_pos, clicked, r_click_tick, wave, wave_anim_ticks, wave_text_tick, wave_number):
    global last_hp, damage_ticks

    hp = min([round(player_actor.__dict__["hp"]),100])

    heartbeat_tick.tick()
    heartbeat_value = (1 - heartbeat_tick.value/30 * (100 - hp)/100) ** 2




    hud_color = [20 + round(200*heartbeat_value) + round(35 * player_actor.hp/100), round(255 * player_actor.hp/100), round(255* player_actor.hp/100)]
    x_d, y_d =cam_delta
    x_d = -x_d
    y_d = -y_d


    try:
        if hp < last_hp:
            damage_ticks = round((last_hp-hp)**0.6)


        if damage_ticks != 0:
            mpl = 4
            x_d += random.uniform(-damage_ticks*mpl, damage_ticks*mpl)
            y_d += random.uniform(-damage_ticks*mpl, damage_ticks*mpl)
            damage_ticks -= 1
    except Exception as e:
        print(e)

    hp_d = 10 - player_actor.hp/10

    x_d += random.uniform(- hp_d, hp_d)
    y_d += random.uniform(- hp_d, hp_d)
    clip_size = weapon.get_clip_size()
    clip = weapon.get_Ammo()
    pl_pos = minus_list(player_actor.get_pos(),camera_pos)
    pl_angl = player_actor.__dict__["aim_angle"]
    pl_angl2 = player_actor.get_angle()





    pl_dist = los.get_dist_points(pl_pos, mouse_pos)
    # if pl_dist < 100:
    #     pl_dist = 100

    pl_dist_mult = pl_dist/25

    spread = weapon.__dict__["_c_bullet_spread"] + weapon.__dict__["_spread"]


    if not pygame.mouse.get_visible():

        if weapon.__dict__["_reload_tick"] == 0:

            pos7 = [pl_pos[0] + math.cos(math.radians(pl_angl2)) * (pl_dist-pl_dist_mult), pl_pos[1] - math.sin(math.radians(pl_angl2)) * (pl_dist-pl_dist_mult)]
            pos8 = [pl_pos[0] + math.cos(math.radians(pl_angl2)) * (pl_dist+pl_dist_mult), pl_pos[1] - math.sin(math.radians(pl_angl2)) * (pl_dist+pl_dist_mult)]


            pos2 = line = [pl_pos[0] + math.cos(math.radians(pl_angl-spread)) * (pl_dist+pl_dist_mult), pl_pos[1] - math.sin(math.radians(pl_angl-spread)) * (pl_dist+pl_dist_mult)]
            pos3 = line = [pl_pos[0] + math.cos(math.radians(pl_angl+spread)) * (pl_dist+pl_dist_mult), pl_pos[1] - math.sin(math.radians(pl_angl+spread)) * (pl_dist+pl_dist_mult)]

            pos1 = line = [pl_pos[0] + math.cos(math.radians(pl_angl-spread)) * (pl_dist-pl_dist_mult), pl_pos[1] - math.sin(math.radians(pl_angl-spread)) * (pl_dist-pl_dist_mult)]
            pos4 = line = [pl_pos[0] + math.cos(math.radians(pl_angl+spread)) * (pl_dist-pl_dist_mult), pl_pos[1] - math.sin(math.radians(pl_angl+spread)) * (pl_dist-pl_dist_mult)]

            pos5 = line = [pl_pos[0] + math.cos(math.radians(pl_angl)) * (pl_dist-pl_dist_mult*2), pl_pos[1] - math.sin(math.radians(pl_angl)) * (pl_dist-pl_dist_mult*2)]
            pos6 = line = [pl_pos[0] + math.cos(math.radians(pl_angl)) * (pl_dist+pl_dist_mult), pl_pos[1] - math.sin(math.radians(pl_angl)) * (pl_dist+pl_dist_mult)]


            pygame.draw.line(screen, [255,0,0], pos7, pos8,2)
            pygame.draw.line(screen, hud_color, pos1, pos2,2)
            pygame.draw.line(screen, hud_color, pos4, pos3,2)
            pygame.draw.line(screen, hud_color, pos5, pos6,3)

        else:

            circular = False

            if circular: # VERY UGLE

                rect = pygame.Rect(mouse_pos[0]-10,mouse_pos[1]-10, 20, 20)
                rect2 = pygame.Rect(mouse_pos[0]-16,mouse_pos[1]-16, 32, 32)
                rect3 = pygame.Rect(mouse_pos[0]-12,mouse_pos[1]-12, 24, 24)

                angle = 5*math.pi/2  - math.pi*2 * ( weapon.__dict__["_reload_tick"] / weapon.__dict__["_reload_rate"])



                pygame.draw.arc(screen, hud_color, rect, math.pi/2, 5*math.pi/2, 2)
                pygame.draw.arc(screen, hud_color, rect2, math.pi/2, 5*math.pi/2, 2)
                pygame.draw.arc(screen, hud_color, rect3, math.pi/2, angle, 2)

                if weapon.__dict__["random_reload_tick"] != -1:
                    angle1 = 5*math.pi/2  - math.pi*2 * ((weapon.__dict__["random_reload_tick"] - 2) / weapon.__dict__["_reload_rate"])
                    angle2 = 5*math.pi/2  - math.pi*2 * ((weapon.__dict__["random_reload_tick"] + 2) / weapon.__dict__["_reload_rate"])
                    pygame.draw.arc(screen, [0,0,255], rect2, angle1, angle2-angle1, 6)

            else:
                rect = pygame.Rect(mouse_pos[0] + x_d,mouse_pos[1] + y_d, 0, 0)
                rect.inflate_ip(10,30)



                height =  22 * weapon.__dict__["_reload_tick"] / weapon.__dict__["_reload_rate"]

                rect2 = pygame.Rect(mouse_pos[0]-2 + x_d,mouse_pos[1] - height + 12  + y_d, 4, height)



                if weapon.__dict__["random_reload_tick"] != -1:

                    if abs(weapon.reload_tick() - weapon.__dict__["random_reload_tick"]) <= 7:
                        color = [0,255,0]

                        rect5 = pygame.Rect(mouse_pos[0] + x_d,mouse_pos[1] + y_d, 0, 0)
                        rect5.inflate_ip(10 + (8-abs(weapon.reload_tick() - weapon.__dict__["random_reload_tick"])),30  + (8-abs(weapon.reload_tick() - weapon.__dict__["random_reload_tick"])))
                        pygame.draw.rect(screen, color, rect5,2)
                    else:
                        color = hud_color



                    q_r_pos1 = 22 *(weapon.__dict__["random_reload_tick"] - 7) / weapon.__dict__["_reload_rate"]
                    q_r_pos2 = 22 *(weapon.__dict__["random_reload_tick"] + 7) / weapon.__dict__["_reload_rate"]

                    rect3 = pygame.Rect(mouse_pos[0]-2 + x_d,mouse_pos[1] - q_r_pos2 + 12  + y_d, 4, q_r_pos2 - q_r_pos1)


                else:
                    color = RED_COLOR

                pygame.draw.rect(screen, color, rect,2)
                pygame.draw.rect(screen, color, rect2)
                if weapon.__dict__["random_reload_tick"] != -1:
                    pygame.draw.rect(screen, [0,255,0], rect3)







    wave_surf = pygame.Surface((size[0], 30), pygame.SRCALPHA, 32).convert_alpha()
    wave_surf.set_colorkey([255,255,255])
    if wave or wave_anim_ticks[0] >= 0:
        wave_end_tick, wave_start_tick = wave_anim_ticks

        if round(abs(wave_text_tick)/30)%2 == 0:

            color1 = [255,255,255]
            color2 = [255,0,0]
        else:
            color2 = [255,255,255]
            color1 = [255,0,0]

        if wave_start_tick != 0:

            pygame.draw.rect(wave_surf, color2, [0,0,(1-wave_start_tick/120)**3 * size[0],30])

        elif wave_end_tick != 0:

            pygame.draw.rect(wave_surf, color2, [(1-wave_end_tick/120)**3 * size[0],0,size[0],30])

        else:
            pygame.draw.rect(wave_surf, color2, [0,0,size[0],30])

        for x in range(0, round(wave_text_tick*4/200)):
            mod = 0
            if wave_end_tick != 0:
                mod = (1-wave_end_tick/120)**3 * size[0]

            if wave_text_tick*2-200 - x*200 + mod > size[0]:
                continue


            text = terminal4.render("WAVE " + str(wave_number),False,color1)
            wave_surf.blit(text, [wave_text_tick*4-300 - x*200 + mod, -3]) #


    screen.blit(wave_surf,(0,10+y_d))

    try:
        im = weapon.__dict__["image"]
        screen.blit(im,[5+x_d, 5+y_d])
    except Exception as e:
        pass
    if weapon.__dict__["_reload_tick"] == 0:
        if clip == clip_size + 1:
            text = terminal.render(str(clip-1) + "+1/" + str(clip_size), False, hud_color)
            screen.blit(text, (15+x_d, 45+y_d)) #
        else:
            if clip == 0:
                color = [255,0,0]
            else:
                color = hud_color


            text = terminal.render(str(clip) + "/" + str(clip_size), False, color)
            screen.blit(text, (15+x_d, 45+y_d)) #

        if player_inventory.get_amount_of_type(weapon.__dict__["ammo"]) < clip_size and weapon.__dict__["ammo"] != "INF":
            color = [255,0,0]
        else:
            color = hud_color

        if weapon.__dict__["ammo"] == "INF":
            text = terminal.render("+INF", False, color)
            screen.blit(text, (110+x_d, 45+y_d)) #
        else:

            text = terminal.render("+" + str(player_inventory.get_amount_of_type(weapon.__dict__["ammo"])) + " res.", False, color)
            screen.blit(text, (110+x_d, 45+y_d)) #

    else:
        text = terminal.render("reloading...", False, hud_color)
        screen.blit(text, (15+x_d, 45+y_d)) #

    if weapon.get_semi_auto():
        text = terminal3.render("Semi-Automatic", False, hud_color)
        screen.blit(text, (15+x_d, 65+y_d)) #

        text = terminal3.render(str(weapon.__dict__["ammo"]), False, hud_color)
        screen.blit(text, (110+x_d, 65+y_d)) #

    elif weapon.__dict__["burst"]:

        text = terminal3.render("Burst-fire", False, hud_color)
        screen.blit(text, (15+x_d, 65+y_d)) #

        text = terminal3.render(str(weapon.__dict__["ammo"]), False, hud_color)
        screen.blit(text, (80+x_d, 65+y_d)) #

        text = terminal3.render(str(weapon.__dict__["_bullet_per_min"]) + "RPM", False, hud_color)
        screen.blit(text, (150+x_d, 65+y_d)) #

    else:
        text = terminal3.render("Automatic", False, hud_color)
        screen.blit(text, (15+x_d, 65+y_d)) #

        text = terminal3.render(str(weapon.__dict__["ammo"]), False, hud_color)
        screen.blit(text, (80+x_d, 65+y_d)) #

        ammo_text_len = 80 + text.get_rect().size[0] + 20
        #print(ammo_text_len)

        text = terminal3.render(str(weapon.__dict__["_bullet_per_min"]) + "RPM", False, hud_color)
        screen.blit(text, (max([150+x_d, ammo_text_len+x_d]), 65+y_d)) #

    y_pos = 80

    for w_1 in player_weapons:
        if w_1 == weapon:
            screen.blit(w_1.icon_active, [20 + x_d,y_pos + y_d])
            pygame.draw.rect(screen, [0,255,0], [20 + x_d, y_pos + y_d, 30, 10], 1)
        elif player_inventory.get_amount_of_type(w_1.ammo) != 0 or w_1.ammo == "INF" or w_1.get_Ammo() != 0:
            screen.blit(w_1.icon, [20 + x_d,y_pos + y_d])

        else:
            screen.blit(w_1.icon_no_ammo, [20 + x_d,y_pos + y_d])
        y_pos += 15





    bars = round((hp-5)/10)


    sanity = player_actor.__dict__["sanity"]
    bars_s = round((sanity)/10)

    if sanity < 40:

        text = terminal3.render("CONSUME NARCOTICS TO REGAIN CONTROL", False, hud_color)
        screen.blit(text, (size[0] - 217+x_d, 380+y_d))


    amount, tick = player_actor.get_sanity_change()
    if amount != False:

        if tick >= 60:

            bars_s = round((sanity - (amount*(tick-60)/30))/10)
            print(bars_s)

        text = terminal3.render(str(amount) + "% SANITY REGAINED", False, hud_color)
        if 1 < tick <= 10:
            screen.blit(text, (844+x_d + (400/tick) - text.get_rect().size[0], 400 +y_d)) #
        elif 10 < tick <= 60:
            screen.blit(text, (844+x_d - text.get_rect().size[0], 400+y_d)) #
        else:
            screen.blit(text, (844 + 150 - 300/(tick-59)+x_d - text.get_rect().size[0], 400+y_d))



    text = terminal2.render("SANITY", False, hud_color)
    screen.blit(text, (844+x_d - text.get_rect().size[0], 412+y_d)) #

    pygame.draw.rect(screen, hud_color, [631+x_d,440+y_d,210,30],3)
    for i in range(bars_s):
        pygame.draw.rect(screen, hud_color, [818 - i*20+x_d,446+y_d,16,18])


    text = terminal2.render("HP", False, hud_color)
    screen.blit(text, (12+x_d, 412+y_d)) #

    pygame.draw.rect(screen, hud_color, [15+x_d,440+y_d,210,30],3)
    for i in range(bars):
        pygame.draw.rect(screen, hud_color, [22 + i*20+x_d,446+y_d,16,18])



    text = terminal2.render(str(weapon.__dict__["name"]), False, hud_color)
    screen.blit(text, (15+x_d, 15+y_d)) #

    player_inventory.draw_inventory(screen, x_d, y_d, mouse_pos, clicked, player_actor.get_pos(), r_click_tick, player_actor)











    last_hp = hp
