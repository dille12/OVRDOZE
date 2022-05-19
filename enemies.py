import os, sys
import pygame
import math
import random
import time
pygame.init()
import func
from values import *
import classtest
import los
import pyperclip
width, height = size
import classes
from classes import items, drop_index, drop_table
import get_preferences
import armory
a, draw_los, a, a, ultraviolence, a = get_preferences.pref()


terminal = pygame.font.Font('texture/terminal.ttf', 20)
terminal2 = pygame.font.Font('texture/terminal.ttf', 30)
prompt = pygame.font.Font('texture/terminal.ttf', 14)

expl_blood = func.load_animation("anim/expl_blood",0,25)

def get_zombie_by_id(id):
    return (zomb for zomb in enemy_list if zomb.identificator == id)





class Zombie:
    def __init__(self,pos, interctables, target_actor, NAV_MESH, walls, hp_diff = 1, dam_diff = 1, type = "normal", wall_points = None, player_ref = None, identificator = random.randint(0, 4096), power = random.uniform(1.5,2.75)):

        self.identificator = identificator
        self.power = power
        self.pos = pos
        self.target_pos = pos
        self.tick_every = 1
        self.moving_speed = power
        self.detection_range = 300*power
        self.detection_rate = 0.05 * self.tick_every
        self.target_angle = 0
        self.detected = False
        self.killed = False
        self.damage = round(5 * power * dam_diff)
        self.knockback_resistance = 1
        self.hp = 100 * hp_diff
        self.attack_speed = 30
        self.target = target_actor
        self.navmesh_ref = NAV_MESH.copy()
        self.wall_ref = walls
        self.player_ref = player_ref

        if type == "normal":
            self.size = 10
            self.image = zombie
            self.type = "normal"
            self.anglular_acceleration = 0.1
        elif type == "bomber":
            self.size = 13
            self.image = bomber
            self.moving_speed *= 0.75
            self.hp *= 0.75
            self.explosion = expl_blood
            self.type = "bomber"
            self.attack_speed = 60
            self.anglular_acceleration = 0.025
        else:
            self.size = 20
            self.image = zombie_big
            self.moving_speed *= 0.35
            self.damage *= 2
            self.hp *= 5
            self.knockback_resistance = 0.1
            self.anglular_acceleration = 0.05

            self.type = "big"

        self.attack_tick = 0
        self.route_tick = 0
        self.get_route_to_target()

        self.route = []
        self.stationary  = 0


        self.tick_time = 0

        self.knockback_tick = 0
        self.knockback_angle = 0




        self.process_tick = 0

        self.times = {"total" : 0}


        self.visible = False


        self.inventory = classes.Inventory(interctables)

        for i in range(random.randint(1,9)):
            if random.uniform(0,1) < 0.02:
                # item_to_pick = func.pick_random_from_dict(items, key = True)
                #

                drop = random.uniform(0, drop_index)
                print("DROP:", drop)
                keys = drop_table.keys()
                key_prox = {}
                for key in keys:
                    if drop - key >= 0:
                        key_prox[drop - key] = [drop_table[key], key]
                print(key_prox)
                item, key = key_prox[min(key_prox.keys())]
                print("KEY",key, "DROP",drop)
                self.inventory.append_to_inv(items[item], random.randint(1,items[item].__dict__["drop_stack"]))







        self.angle = 0

    def issue_event(self, event):
        zombie_events.append(f"ZEVENT:{self.identificator}_{event}")

    def kill(self, camera_pos, list, draw_blood_parts, silent = False, zevent = False):
        list.remove(self)
        if not zevent:
            self.issue_event("terminate_1")

        func.list_play(death_sounds)
        if not silent:
            func.list_play(kill_sounds)

        if self.type == "bomber":
            explosions.append(armory.Explosion(func.minus(self.pos,[25,25]), expl_blood, player_nade = True, range = 150, particles = "blood", color_override = "yellow"))

        self.inventory.drop_inventory(self.pos)

        self.killed = True

        for i in range(5):
            particle_list.append(classes.Particle(func.minus(self.pos,camera_pos), type = "blood_particle", magnitude = 1, screen = draw_blood_parts))


    def get_string(self):
        return f"ZOMBIE:{str(round(self.pos[0]))}_{str(round(self.pos[1]))}_{str(self.identificator)}_{self.target.name}_{str(round(self.power,5))}_{self.type}"


    def set_hp(self, hp, reduce = False):
        if reduce:
            self.hp -= hp
        else:
            self.hp = hp

    def get_hp(self):
        return self.hp

    def get_hitbox(self):
        return [25,25]

    def get_pos(self):
        return self.pos

    def knockback(self,amount,angle, daemon_bullet = False):

        self.knockback_tick = round(amount*self.knockback_resistance)
        self.knockback_angle = angle
        if not daemon_bullet:
            self.issue_event(f"setpos_{str(self.pos)}")



    def get_route_to_target(self):

        if self.route_tick == 0 and self.target == self.player_ref:
            self.route = func.calc_route(self.pos, self.target.pos, self.navmesh_ref, self.wall_ref)
            self.issue_event(f"setroute_{str(self.route)}")
            self.issue_event(f"setpos_{str(self.pos)}")
            self.route_tick = 60


    def hit_detection(self,camera_pos, pos, lastpos, damage, enemy_list, map_render):
        points_1 = [[self.pos[0], self.pos[1] - self.size*2.5], [self.pos[0], self.pos[1] + self.size*2.5]]
        points_2 = [[self.pos[0]-self.size*2.5, self.pos[1]], [self.pos[0]+self.size*2.5, self.pos[1]]]

        if los.intersect(pos, lastpos, points_1[0], points_1[1]) or los.intersect(pos, lastpos, points_2[0], points_2[1]):

            self.hp -= damage
            if self.hp < 0:
                self.kill(camera_pos, enemy_list, map_render)


            else:
                func.list_play(hit_sounds)

            return True
        return False

    def check_if_alive(self):
        if self.killed:
            return False
        else:
            return True



    def tick(self, screen, map_boundaries, player_actor, camera_pos, map, walls, NAV_MESH,map_render, phase = 0, wall_points = None):

        if self.route_tick != 0:
            self.route_tick -= 1

        if phase == 6:
            t_1 = time.time()

        if self.process_tick == self.tick_every:
            self.process_tick = 0
        else:
            self.process_tick += 1


        for melee_hit in melee_list:
            angle_to_melee = 360 - math.degrees(math.atan2(self.pos[1] - melee_hit["pos"][1], self.pos[0] - melee_hit["pos"][0]))
            if los.get_dist_points(melee_hit["pos"], self.pos) < melee_hit["strike_range"] and los.get_angle_diff(abs(angle_to_melee), melee_hit["angle"]) < melee_hit["arc"]/2:
                melee_hit_sound.stop()
                melee_hit_sound.play()
                self.knockback(melee_hit["damage"], math.radians(angle_to_melee))
                self.hp -= melee_hit["damage"]



        if self.attack_tick != 0:
            self.attack_tick -= 1

        self.temp_pos = func.minus_list(self.pos,camera_pos)
        player_pos = self.target.pos
        pl_temp_pos = func.minus_list(player_pos,camera_pos)

        last_pos = self.pos.copy()

        if self.knockback_tick != 0:

            self.pos = [self.pos[0] + math.cos(self.knockback_angle) * self.knockback_tick**0.5, self.pos[1] - math.sin(self.knockback_angle) *self.knockback_tick**0.5]
            self.knockback_tick -= 1

        if phase == 6:
            t_2 = time.time()

        if draw_los and self.process_tick == 0:

            self.visible = los.check_los(player_actor.get_pos(), self.pos, walls)

        if phase == 6:
            t_3 = time.time()



        #pygame.draw.rect(screen, [255,255,255],[self.temp_pos[0], self.temp_pos[1], 20, 20])

        for x in burn_list:
            if los.get_dist_points(x.pos, self.pos) < 25:
                self.hp -= 1

        self.target_angle = 180 - math.degrees(math.atan2(self.pos[1] - self.target_pos[1], self.pos[0] - self.target_pos[0]))



        if self.visible or not draw_los:  ## Render
            rot, rect= func.rot_center(self.image, self.angle, self.temp_pos[0], self.temp_pos[1])
            rect = rot.get_rect().center
            screen.blit(rot, [self.temp_pos[0] - rect[0], self.temp_pos[1] - rect[1]])

        # text = terminal.render(str(self.identificator), False, WHITE_COLOR)
        # screen.blit(text, self.temp_pos)

        if phase == 6:
            t_4 = time.time()


        if los.check_los(self.target.pos, self.pos, walls):

            dist = los.get_dist_points(self.pos, player_pos)

            if dist < self.detection_range and self.target.hp > 0:

                if random.uniform(0,1) < (1 - dist/self.detection_range)*self.detection_rate:
                    self.detected = True
            else:
                self.detected = False

        else:
            self.detected = False

        if phase == 6:
            t_5 = time.time()

        if self.detected:
            #self.target_angle = 180 - math.degrees(math.atan2(self.pos[1] - player_pos[1], self.pos[0] - player_pos[0]))
            if dist > 50:

                self.target_pos = player_pos

            else:
                self.target_pos = self.pos

                if self.attack_tick == 0:
                    self.attack_tick = self.attack_speed
                    if self.type != "bomber":
                        self.target.hp -= self.damage
                        func.list_play(pl_hit)
                        try:
                            self.target.knockback(self.damage,math.radians(90 + self.target_angle))
                        except:
                            pass
                    for i in range(3):
                        particle_list.append(classes.Particle(func.minus(self.target.pos, camera_pos), type = "blood_particle", magnitude = 0.5, screen = map_render))
                elif self.attack_tick == 1 and self.type == "bomber":
                    self.kill(camera_pos, enemy_list, map_render)

        if phase == 6:
            t_6 = time.time()


        if self.angle != self.target_angle:

            if abs(self.target_angle - self.angle) > 1:
                self.angle = self.angle + los.get_angle_diff(self.target_angle, self.angle)*self.anglular_acceleration
            else:
                self.angle = self.target_angle

        if phase == 6:
            t_7 = time.time()

        if self.target_pos != self.pos:

            #self.angle_rad = math.pi*2 - math.atan2(self.target_pos[1] - self.pos[1], self.target_pos[0] - self.pos[0])
            self.angle_rad = math.radians(self.angle)
            self.pos = [self.pos[0] + math.cos(self.angle_rad) *self.moving_speed, self.pos[1] - math.sin(self.angle_rad) *self.moving_speed]

            if self.attack_tick == 0:
                i = True
            else:
                i = False

            collision_types, coll_pos = map.checkcollision(self.pos,[math.cos(self.angle_rad) *self.moving_speed, self.pos[1] - math.sin(self.angle_rad) *self.moving_speed], self.size, map_boundaries, damage_barricades = i, damager = self)
            self.pos = coll_pos
            if los.get_dist_points(self.pos,self.target_pos) < 50:
                self.target_pos = self.pos

        else:
            if self.route != []:

                for route in self.route:

                    self.target_pos = route
                    self.route.remove(route)

                    if self.pos != self.target_pos:
                        break

            else:
                self.get_route_to_target()

        if phase == 6:
            t_8 = time.time()

        if last_pos == self.pos  and self.detected == False:

            self.stationary += 1
            if self.stationary > 30:
                self.get_route_to_target()
                try:
                    self.target_pos = self.route[0]
                except:
                    pass
        #
        else:
            self.stationary = 0

        if self.check_if_alive() and self.hp <= 0:
            self.kill(camera_pos, enemy_list, map_render)


        if phase == 6:
            t_9 = time.time()

        if phase == 6:

            if self.stationary != 0:
                text = terminal.render("stationary:" + str(self.stationary), False, [255,255,255])
                screen.blit(text, func.minus(self.pos,camera_pos, op="-"))

            tick_time = (t_2 - t_1)*1000

            self.tick_time = round(self.tick_time * 9/10 + 1/10 * tick_time,2)
            last = t_1
            x_p = 30
            delta = 0
            for i, x in enumerate([t_2,t_3,t_4,t_5,t_6,t_7,t_8,t_9]):

                t = round((x - last)*1000,2)

                if i in self.times:
                    self.times[i] = round(self.times[i] * 29/30 + 1/30 * t,2)
                else:
                    self.times[i] = t


                text = terminal.render(str(self.times[i]) + "ms", False, [255,255,255])
                screen.blit(text, func.minus(func.minus(self.pos,[0,x_p]),camera_pos, op="-"))
                x_p += 30
                last = x

                delta += self.times[i]
            self.times["total"] = round(self.times["total"] * 29/30 + 1/30 * delta,2)
            text = terminal.render(str(delta) + "ms", False, [255,255,255])
            screen.blit(text, func.minus(func.minus(self.pos,[0,0]),camera_pos, op="-"))

            if self.pos != self.target_pos:
                last_pos = self.pos
                for tar in self.route:
                    pygame.draw.line(screen, [255,255,255], func.minus(last_pos,camera_pos, op="-"), func.minus(tar,camera_pos, op="-"))
                    last_pos = tar






class Player_Multi:
    def __init__(self, username):
        self.name = username
        self.pos = [0,0]
        self.hp = 100
        self.angle = 0
        self.player_blit = player
        self.killed = False
        self.name_text  = prompt.render(self.name,False, [255,255,255])
        self.last_tick = time.time()
        self.vel = [0,0]
        self.acc = [0,0]
        self.last_tick_pos = [0,0]
        self.interpolations2 = []
        self.interpolations = []
        self.idle_ticks = 0

    def check_if_alive(self):
        if self.killed:
            return False
        else:
            return True


    def kill(self, camera_pos, dict, draw_blood_parts):

        if self.killed:
            return


        func.list_play(death_sounds)
        func.list_play(kill_sounds)
        for i in range(5):
            particle_list.append(classes.Particle(func.minus(self.pos,camera_pos), type = "blood_particle", magnitude = 1, screen = draw_blood_parts))
        print("KILLED")
        self.killed = True

    def hit_detection(self,camera_pos, pos, lastpos, damage, actor_list, map_render):

        if self.killed == True and self.hp == 100:
            self.killed = False

        if self.hp <= 0:
            return False

        points_1 = [[self.pos[0], self.pos[1] -25], [self.pos[0], self.pos[1] + 25]]
        points_2 = [[self.pos[0]-25, self.pos[1]], [self.pos[0]+25, self.pos[1]]]

        if los.intersect(pos, lastpos, points_1[0], points_1[1]) or los.intersect(pos, lastpos, points_2[0], points_2[1]):

            if self.hp - damage < 0:
                self.kill(camera_pos, actor_list, map_render)


            else:
                func.list_play(hit_sounds)

            return True
        return False

    def tick(self, screen, player_pos,camera_pos, walls):

        if self.hp > 0:
            self.killed = False

        if self.killed:
            return

        if self.interpolations != []:
            self.pos = self.interpolations[0]
            self.interpolations.remove(self.interpolations[0])
            self.idle_ticks = 0
        else:
            self.idle_ticks += 1

        # pygame.draw.circle(screen, [255,255,255], func.minus(self.pos,camera_pos, "-"),8)

        if los.get_dist_points(player_pos, self.pos) > 1000 or self.hp <= 0 or los.check_los(player_pos, self.pos, walls) == False:
            return

        player_rotated, player_rotated_rect = func.rot_center(self.player_blit,self.angle,self.pos[0],self.pos[1])

        player_pos_center = player_rotated.get_rect().center
        player_pos_center = [self.pos[0]-player_pos_center[0],self.pos[1]-player_pos_center[1]]
        offset = [player_rotated_rect[0]-self.pos[0]-camera_pos[0], player_rotated_rect[1]-self.pos[1]-camera_pos[1]]
        screen.blit(player_rotated,[self.pos[0]+offset[0],self.pos[1]+offset[1]])






        #screen.blit(self.player_blit, func.minus_list(self.pos,camera_pos))
        text_rect = self.name_text.get_rect().size

        screen.blit(self.name_text, func.minus_list(func.minus_list(self.pos,camera_pos), [text_rect[0]/2, 25]))

        # for interpo in self.interpolations2:
        #     pygame.draw.circle(screen, [255,0,0], func.minus(interpo,camera_pos, "-"),5)

    def set_values(self, x, y, a, hp):
        if int(x) != self.pos[0] or int(y) != self.pos[1]:

            interpolation = (time.time() - self.last_tick)
            self.last_tick = time.time()
            #print("INTERP:", interpolation)

            inter_ticks = round(interpolation/(1/60))

            self.interpolations = []
            for i in range(1,inter_ticks):
                i /= inter_ticks
                curve = func.BezierInterpolation([self.pos, [self.vel[0] + self.pos[0], self.vel[1]  + self.pos[1]], [int(x), int(y)]], i)
                self.interpolations.append(curve)
                self.interpolations2.append(curve)

            self.vel = [(int(x) - self.pos[0]), (int(y) - self.pos[1])]


            #print("VELO:", self.vel)

        else:
            self.vel = [0,0]

        #self.pos = [int(x), int(y)]
        self.angle = int(a)
        self.hp = int(hp)
