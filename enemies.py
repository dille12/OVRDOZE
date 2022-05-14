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

a, draw_los, a, ultraviolence, a = get_preferences.pref()


terminal = pygame.font.Font('texture/terminal.ttf', 20)
terminal2 = pygame.font.Font('texture/terminal.ttf', 30)
prompt = pygame.font.Font('texture/terminal.ttf', 14)



class Zombie:
    def __init__(self,pos, interctables, player_pos, NAV_MESH, walls, hp_diff = 1, dam_diff = 1, type = "normal"):
        self.pos = pos
        self.target_pos = pos
        self.tick_every = 1
        self.moving_speed = random.uniform(1.5,2.75)
        self.detection_range = random.randint(400,600)
        self.detection_rate = 0.05 * self.tick_every
        self.target_angle = 0
        self.detected = False
        self.killed = False
        self.damage = random.randint(5,15) * dam_diff
        self.knockback_resistance = 1
        self.hp = 100 * hp_diff
        if type == "normal":
            self.size = 10
            self.image = zombie
        else:
            self.size = 20
            self.image = zombie_big
            self.moving_speed *= 0.35
            self.damage *= 2
            self.hp *= 5
            self.knockback_resistance = 0.1

        self.attack_tick = 0



        self.route = func.calc_route(pos, player_pos, NAV_MESH, walls)

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

    def kill(self, camera_pos, list, draw_blood_parts):
        list.remove(self)
        func.list_play(death_sounds)
        func.list_play(kill_sounds)

        self.inventory.drop_inventory(self.pos)

        self.killed = True

        for i in range(5):
            particle_list.append(classes.Particle(func.minus(self.pos,camera_pos), type = "blood_particle", magnitude = 1, screen = draw_blood_parts))
        print("KILLED")


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

    def knockback(self,amount,angle):

        self.knockback_tick = round(amount*self.knockback_resistance)
        self.knockback_angle = angle





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



    def tick(self, screen, map_boundaries, player_actor, camera_pos, map, walls, NAV_MESH,map_render, phase = 0):

        if phase == 6:
            t_1 = time.time()

        if self.process_tick == self.tick_every:
            self.process_tick = 0
        else:
            self.process_tick += 1



        if self.attack_tick != 0:
            self.attack_tick -= 1

        self.temp_pos = func.minus_list(self.pos,camera_pos)
        player_pos = player_actor.get_pos()
        pl_temp_pos = func.minus_list(player_pos,camera_pos)

        last_pos = self.pos.copy()

        if self.knockback_tick != 0:

            self.pos = [self.pos[0] + math.cos(self.knockback_angle) * self.knockback_tick**0.5, self.pos[1] - math.sin(self.knockback_angle) *self.knockback_tick**0.5]
            self.knockback_tick -= 1

        if phase == 6:
            t_2 = time.time()

        if draw_los and self.process_tick == 0:

            self.visible = los.check_los(player_pos, self.pos, walls)

        if phase == 6:
            t_3 = time.time()



        #pygame.draw.rect(screen, [255,255,255],[self.temp_pos[0], self.temp_pos[1], 20, 20])



        self.target_angle = 180 - math.degrees(math.atan2(self.pos[1] - self.target_pos[1], self.pos[0] - self.target_pos[0]))



        if self.visible or not draw_los:
            rot, rect= func.rot_center(self.image, self.angle, self.temp_pos[0], self.temp_pos[1])
            rect = rot.get_rect().center
            screen.blit(rot, [self.temp_pos[0] - rect[0], self.temp_pos[1] - rect[1]])

        if phase == 6:
            t_4 = time.time()


        if self.visible:  ## Render

            dist = los.get_dist_points(self.pos, player_pos)

            if dist < self.detection_range and player_actor.get_hp() > 0:

                if random.uniform(0,1) < (1 - dist/self.detection_range)*self.detection_rate:
                    self.detected = True
            else:
                self.detected = False

        else:
            self.detected = False

        if phase == 6:
            t_5 = time.time()

        if self.detected:
            self.target_angle = 180 - math.degrees(math.atan2(self.pos[1] - player_pos[1], self.pos[0] - player_pos[0]))
            if dist > 50:

                self.target_pos = player_pos

            else:
                self.target_pos = self.pos

                if self.attack_tick == 0:
                    self.attack_tick = 30
                    player_actor.set_hp(self.damage, reduce = True)
                    func.list_play(pl_hit)

                    for i in range(3):
                        particle_list.append(classes.Particle(func.minus(player_actor.get_pos(), camera_pos), type = "blood_particle", magnitude = 0.5, screen = map_render))

        if phase == 6:
            t_6 = time.time()


        if self.angle != self.target_angle:

            if abs(self.target_angle - self.angle) > 1:
                self.angle = self.angle + los.get_angle_diff(self.target_angle, self.angle)*0.1
            else:
                self.angle = self.target_angle

        if phase == 6:
            t_7 = time.time()

        if self.target_pos != self.pos:

            self.angle_rad = math.pi*2 - math.atan2(self.target_pos[1] - self.pos[1], self.target_pos[0] - self.pos[0])
            self.pos = [self.pos[0] + math.cos(self.angle_rad) *self.moving_speed, self.pos[1] - math.sin(self.angle_rad) *self.moving_speed]

            if self.attack_tick == 0:
                i = True
            else:
                i = False

            collision_types, coll_pos = map.checkcollision(self.pos,[math.cos(self.angle_rad) *self.moving_speed, self.pos[1] - math.sin(self.angle_rad) *self.moving_speed], self.size, map_boundaries, damage_barricades = i, damager = self)
            self.pos = coll_pos
            if los.get_dist_points(self.pos,self.target_pos) < 10:
                self.target_pos = self.pos

        else:
            if self.route != []:

                for route in self.route:

                    self.target_pos = route
                    self.route.remove(route)

                    if self.pos != self.target_pos:
                        break

            else:
                self.route = func.calc_route(self.pos, player_pos, NAV_MESH, walls)

        if phase == 6:
            t_8 = time.time()

        if last_pos == self.pos  and self.detected == False:

            self.stationary += 1
            if self.stationary > 30:
                self.route = func.calc_route(self.pos, player_pos, NAV_MESH, walls)
                try:
                    self.target_pos = self.route[0]
                except:
                    pass
        #
        else:
            self.stationary = 0

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



class Enemy:
    def __init__(self,pos, weapons, interctables):
        self.pos = pos
        self.target_pos = pos
        self.moving_speed = random.uniform(1.5,2.75)
        self.detection_range = random.randint(400,600)
        self.detection_rate = 0.05
        self.target_angle = 0
        self.detected = False



        self.knockback_tick = 0
        self.knockback_angle = 0

        self.hp = 100

        self.weapon = func.pick_random_from_dict(weapons).copy()

        self.inventory = Inventory(interctables)
        for i in range(random.randint(2,3)):
            self.inventory.append_to_inv(items[self.weapon.__dict__["ammo"]], items[self.weapon.__dict__["ammo"]].__dict__["max_stack"])
        self.weapon.set_hostile()

        self.angle = 0

    def kill(self, camera_pos, list, draw_blood_parts):
        list.remove(self)
        func.list_play(death_sounds)
        func.list_play(kill_sounds)

        #self.inventory.drop_inventory(self.pos)

        for i in range(5):
            particle_list.append(classes.Particle(func.minus(self.pos,camera_pos), type = "blood_particle", magnitude = 1, screen = draw_blood_parts))
        print("KILLED")


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

    def knockback(self,amount,angle):

        self.knockback_tick = amount
        self.knockback_angle = angle





    def hit_detection(self,camera_pos, pos, lastpos, damage, enemy_list, map_render):
        points_1 = [[self.pos[0], self.pos[1] -25], [self.pos[0], self.pos[1] + 25]]
        points_2 = [[self.pos[0]-25, self.pos[1]], [self.pos[0]+25, self.pos[1]]]

        if los.intersect(pos, lastpos, points_1[0], points_1[1]) or los.intersect(pos, lastpos, points_2[0], points_2[1]):

            self.hp -= damage
            if self.hp < 0:
                self.kill(camera_pos, enemy_list, map_render)


            else:
                func.list_play(hit_sounds)

            return True
        return False

    def check_if_alive(self):
        if self.hp > 0:
            return True
        else:
            return False



    def tick(self, screen, map_boundaries, player_actor, camera_pos, map, walls):
        self.temp_pos = func.minus_list(self.pos,camera_pos)
        player_pos = player_actor.get_pos()
        pl_temp_pos = func.minus_list(player_pos,camera_pos)

        if self.knockback_tick != 0:

            self.pos = [self.pos[0] + math.cos(self.knockback_angle) * self.knockback_tick, self.pos[1] - math.sin(self.knockback_angle) *self.knockback_tick]
            self.knockback_tick -= 1



        #pygame.draw.rect(screen, [255,255,255],[self.temp_pos[0], self.temp_pos[1], 20, 20])




        if los.check_los(player_pos, self.pos, walls):  ## Render

            rot, rect= func.rot_center(player, self.angle, self.temp_pos[0], self.temp_pos[1])
            rect = rot.get_rect().center
            screen.blit(rot, [self.temp_pos[0] - rect[0], self.temp_pos[1] - rect[1]])

            dist = los.get_dist_points(self.pos, player_pos)

            if dist < self.detection_range and player_actor.get_hp() > 0:

                if random.uniform(0,1) < (1 - dist/self.detection_range)*self.detection_rate:
                    self.detected = True

                if self.detected:
                    self.target_angle = 180 - math.degrees(math.atan2(self.pos[1] - player_pos[1], self.pos[0] - player_pos[0]))
                    if player_actor.get_hp() > 0:
                        func.weapon_fire(self.weapon, self.inventory, self.angle, self.pos, screen, ai = True)

                    if dist > 50:

                        self.target_pos = player_pos

                    else:
                        self.target_pos = self.pos

            else:
                self.detected = False

        # if player_actor.get_hp() < 0:
        #     self.target_pos = self.pos

        if self.angle != self.target_angle:

            if abs(self.target_angle - self.angle) > 1:
                self.angle = self.angle + los.get_angle_diff(self.target_angle, self.angle)*0.1
            else:
                self.angle = self.target_angle

        if self.target_pos != self.pos:

            self.angle_rad = math.pi*2 - math.atan2(self.target_pos[1] - self.pos[1], self.target_pos[0] - self.pos[0])
            self.pos = [self.pos[0] + math.cos(self.angle_rad) *self.moving_speed, self.pos[1] - math.sin(self.angle_rad) *self.moving_speed]
            coll_pos = map.check_collision(self.pos, map_boundaries, collision_box = 10)
            if coll_pos:
                self.pos = coll_pos
            if los.get_dist_points(self.pos,self.target_pos) < 10:
                self.target_pos = self.pos

        else:
            point = map.get_random_point(None, max_tries = 1)
            if los.check_los(point, self.pos, walls):
                print("Wandering")
                self.target_angle = 180 - math.degrees(math.atan2(self.pos[1] - point[1], self.pos[0] - point[0]))

                self.target_pos = point
                print("to", self.target_pos)



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

        if self.hp <= 0:
            self.killed = False

        if self.killed:
            return

        if self.interpolations != []:


            self.render_pos = self.interpolations[0]
            self.interpolations.remove(self.interpolations[0])

        else:
            self.render_pos = self.pos

        # pygame.draw.circle(screen, [255,255,255], func.minus(self.pos,camera_pos, "-"),8)

        if los.get_dist_points(player_pos, self.pos) > 1000 or self.hp <= 0 or los.check_los(player_pos, self.render_pos, walls) == False:
            return

        player_rotated, player_rotated_rect = func.rot_center(self.player_blit,self.angle,self.render_pos[0],self.render_pos[1])

        player_pos_center = player_rotated.get_rect().center
        player_pos_center = [self.pos[0]-player_pos_center[0],self.pos[1]-player_pos_center[1]]
        offset = [player_rotated_rect[0]-self.pos[0]-camera_pos[0], player_rotated_rect[1]-self.pos[1]-camera_pos[1]]
        screen.blit(player_rotated,[self.render_pos[0]+offset[0],self.render_pos[1]+offset[1]])






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

        self.pos = [int(x), int(y)]
        self.angle = int(a)
        self.hp = int(hp)
