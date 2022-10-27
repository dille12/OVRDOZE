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
import classes
from classes import items, drop_index, drop_table
import get_preferences
from armory import guns
from _thread import *

terminal = pygame.font.Font("texture/terminal.ttf", 20)

class Soldier:
    def __init__(
        self,
        app,
        pos,
        interactables,
        target_actor,
        NAV_MESH,
        walls,
        map,
    ):
        self.app = app
        self.pos = pos
        self.target_pos = pos.copy()
        self.route = []
        self.interactables = interactables
        self.target_actor = target_actor
        self.NAV_MESH = NAV_MESH
        self.walls = walls
        self.im = player
        self.targeting_angle = 90
        self.angle = 0
        self.target_angle = 0
        self.aim_at = [0,0]
        self.aim_angle_target = 0
        self.aim_angle = 0
        self.move_at = pos.copy()
        self.route_tick = 0
        self.map = map
        self.moving_speed = 2
        self.velocity = 0
        self.calculating = False
        self.random_aim_tick = 0
        self.anglular_acceleration = 0.1
        self.size = 10*multiplier2
        self.stationary = 0
        self.hp = 250
        self.state = None
        self.knockback_resistance = 1
        self.knockback_tick = 0
        self.knockback_angle = 0
        self.state_tick = 0
        self.investigating = False
        self.investigate_route = False
        self.sees_target = False
        self.class_type = "SOLDIER"
        self.killed = False

        self.collisions_with_walls = 0

        self.range = 500*multiplier2

        self.inventory = classes.Inventory(self.app, self.interactables)

        for i in range(random.randint(1, 9)):
            if random.uniform(0, 1) < 0.05:
                # item_to_pick = func.pick_random_from_dict(items, key = True)
                #

                drop = random.uniform(0, drop_index)
                keys = drop_table.keys()
                key_prox = {}
                for key in keys:
                    if drop - key >= 0:
                        key_prox[drop - key] = [drop_table[key], key]
                item, key = key_prox[min(key_prox.keys())]
                self.inventory.append_to_inv(
                    items[item], random.randint(1, items[item].__dict__["drop_stack"])
                )

        self.weapon = func.pick_random_from_list([guns["AK"], guns["P90"]]).copy()
        self.weapon._damage *= 0.5
        self.weapon.hostile = True
        self.weapon.ammo = "INF"


    def fire(self):
        if self.target.hp > 0:
            func.weapon_fire(self.weapon, self.inventory, self.angle, self.pos, self, self.app.screen_copy, ai = True)

    def get_pos(self):
        return self.pos

    def set_hp(self, hp, reduce=False):
        if reduce:
            self.hp -= hp
        else:
            self.hp = hp

    def get_hp(self):
        return self.hp


    def search_route(self):
        self.calculating = True
        self.route, self.cached_route = func.calc_route(
            self.pos, self.target_pos, self.NAV_MESH, [self.walls, self.map.no_los_walls], cache = self.app
        )

        if self.route == False:
            self.route_tick = 60
            self.route = []
            self.wander_to_random_point()

        self.calculating = False

    def get_route_to_target(self):

        if (
            self.route_tick <= 0
            and not self.calculating
        ):
            if self.route:
                if self.route[-1] == self.target_pos:
                    return
            self.route_tick = 60
            start_new_thread(self.search_route, ())



    def shoot(self):

        if self.target_actor.hp <= 0:
            return

        firing_tick = func.weapon_fire(
            self.weapon,
            self.inventory,
            (360-self.aim_angle),
            self.pos,
            self,
            self.app.screen_copy,
            ai = True
        )

        # self.weapon.spread_recoverial()
        # self.weapon.weapon_tick()

    def at_target_pos(self):
        return los.get_dist_points(self.target_pos, self.pos) < 50

    def get_state(self):
        last_state = self.state
        if self.weapon._reload_tick > 0 or self.hp < 150:
            self.state = "takingcover"
            self.movement_speed = 7
        elif self.sees_target:
            self.state = "attacking"
            self.movement_speed = 3
        elif self.investigating or self.investigate_route:
            self.movement_speed = 4
            self.state = "investigate"
        else:
            self.state = "wander"

            self.movement_speed = 1.5

            if self is not self.patrol.patrol_leader:
                if func.get_dist_points(self.pos, self.patrol.patrol_leader.pos) > 700:
                    self.movement_speed = 3


        if last_state != self.state or random.randint(1,300) == 1:
            can_play = True
            for x in radio_chatter[self.state]:
                if x.get_num_channels():
                    can_play = False
            if can_play:
                func.pick_random_from_list(radio_chatter[self.state]).play()

            if self.state == "attacking":
                for x in self.patrol.troops:
                    if x.state == "wander":
                        x.investigating = True

    def wander_to_random_point(self):
        if self is self.patrol.patrol_leader:
            self.target_pos = self.map.get_random_point(self.walls, max_dist = 1300, max_dist_point = self.pos.copy(), max_tries = 10)
        else:

            self.target_pos = self.map.get_random_point(self.walls, max_dist = 500, max_dist_point = self.patrol.patrol_leader.pos.copy(), max_tries = 10)



    def state_react(self):
        tar_pos = self.target_pos.copy()
        if self.state == "takingcover":
            if self.at_target_pos() and los.check_los(self.pos, self.target_actor.pos, self.walls, self.map.no_los_walls):
                self.target_pos = self.map.get_random_point(self.walls, max_dist = 400, max_dist_point = self.pos, p_pos = self.target_actor.pos, max_tries = 10)
                self.aim_at = self.target_actor.pos.copy()
                self.state_tick = 60
        elif self.state == "attacking":
            if self.at_target_pos() or not los.check_los(self.pos, self.target_actor.pos, self.walls):
                self.target_pos = self.map.get_random_point(self.walls, visible_from_origin_point = self.target_actor.pos, max_tries = 10)
                self.state_tick = 60

        elif self.state == "investigate":
            if not self.investigate_route:
                self.target_pos = self.target_actor.pos.copy()
            self.investigating = False
            self.investigate_route = True

            if self.at_target_pos():
                self.investigate_route = False

        else: #WANDER

            if self is not self.patrol.patrol_leader:
                patrol_follow_condion = func.get_dist_points(self.target_pos, self.patrol.patrol_leader.pos) > 400

            else:
                patrol_follow_condion = False

            if self.at_target_pos() or patrol_follow_condion:
                self.wander_to_random_point()


        if tar_pos != self.target_pos:
            self.get_route_to_target()


    def move(self):

        last_pos = self.pos.copy()

        if self.knockback_tick > 0:

            self.pos = [
                self.pos[0]
                + timedelta.mod(math.cos(self.knockback_angle) * self.knockback_tick**0.2 * multiplier2),
                self.pos[1]
                - timedelta.mod(math.sin(self.knockback_angle) * self.knockback_tick**0.2 * multiplier2),
            ]
            self.knockback_tick -= timedelta.mod(1)

        if not self.route and not self.at_target_pos():
            self.get_route_to_target()

        if not los.check_los(self.pos, self.target_pos, self.walls, self.map.no_los_walls):
            if self.route:
                if not los.check_los(self.pos, self.route[0], self.walls, self.map.no_los_walls):
                    self.get_route_to_target()
            else:
                self.get_route_to_target()


        if self.route:
            if los.get_dist_points(self.route[0], self.pos) > 40:

                if len(self.route) > 1:
                    if los.check_los(self.pos, self.route[1], self.walls, self.map.no_los_walls):
                        self.route.remove(self.route[0])

                self.target_angle = func.get_angle(self.pos, self.route[0])



                if self.velocity < self.movement_speed:
                    self.velocity += timedelta.mod(self.moving_speed * 0.1)
                else:
                    self.velocity -= timedelta.mod(self.moving_speed * 0.1)


            else:
                self.route.remove(self.route[0])

        elif self.route == False:
            self.wander_to_random_point()



        if self.collisions_with_walls > 30:
            self.route = []
            self.collisions_with_walls = 0
            self.wander_to_random_point()


        if self.collisions_with_walls > 0:
            self.collisions_with_walls -= 0.5

        rad = math.radians(self.angle)

        self.pos[0] += self.velocity * math.cos(rad)
        self.pos[1] += self.velocity * math.sin(rad)



        self.velocity *= 0.95


        collision_types, coll_pos = self.map.checkcollision(
            self.pos,
            [0,0],
            self.size,
            self.map.size,
            damage_barricades=True,
            damager=self,
        )

        if self.pos != coll_pos:
            self.collisions_with_walls += 1

        self.pos = coll_pos

    def aim(self):
        angle_to_player = func.get_angle(self.pos, self.target_actor.pos)
        ignore_player = False
        if random.randint(1,10) == 1 and not ignore_player:
            if abs(los.get_angle_diff(angle_to_player, self.aim_angle)) < self.targeting_angle and los.check_los(self.pos, self.target_actor.pos, self.walls) and self.target_actor.hp > 0 and func.get_dist_points(self.pos, self.target_actor.pos) < self.range:
                self.sees_target = True
            else:
                self.sees_target = False


        if self.state == "wander":
            if self.random_aim_tick > 0:
                self.random_aim_tick -= timedelta.mod(1)
            if self.random_aim_tick <= 0:
                self.random_aim_tick = random.randint(60, 120)
                self.aim_at = self.map.get_random_point(self.walls, max_tries = 10)
        elif not self.sees_target and self.investigate_route:
            self.aim_at = self.target_pos.copy()
        elif self.sees_target:
            self.aim_at = self.target_actor.pos.copy()

    def check_if_alive(self):
        if self.killed or self not in enemy_list:
            return False
        else:
            return True

    def kill_actor(
        self,
        camera_pos,
        list,
        draw_blood_parts,
        player_actor,
        silent=False,
        zevent=False,
    ):

        list.remove(self)
        self.patrol.troops.remove(self)
        self.patrol.check_leader()

        if not silent:

            player_actor.money += random.randint(5, 10)
            money_tick.value = 0

            func.list_play(death_sounds)
            func.list_play(kill_sounds)

            self.inventory.drop_inventory(self.pos)

            for i in range(5):
                particle_list.append(
                    classes.Particle(
                        func.minus(self.pos, camera_pos),
                        type="blood_particle",
                        magnitude=1,
                        screen=draw_blood_parts,
                    )
                )

                # particle_list.append(
                #     classes.Particle(
                #         func.minus(self.pos, camera_pos),
                #         type="flying_blood",
                #         magnitude=1,
                #         screen=screen,
                #     )
                # )

        self.killed = True

    def knockback(self, amount, angle, daemon_bullet=False):

        self.knockback_tick = round(amount * self.knockback_resistance)
        self.knockback_angle = angle


    def hit_detection(
        self, camera_pos, pos, lastpos, damage, enemy_list, map_render, player_actor
    ):
        points_1 = [
            [self.pos[0], self.pos[1] - self.size * 2.5],
            [self.pos[0], self.pos[1] + self.size * 2.5],
        ]
        points_2 = [
            [self.pos[0] - self.size * 2.5, self.pos[1]],
            [self.pos[0] + self.size * 2.5, self.pos[1]],
        ]

        if los.intersect(pos, lastpos, points_1[0], points_1[1]) or los.intersect(
            pos, lastpos, points_2[0], points_2[1]
        ):

            self.hp -= damage
            if self.hp < 0:
                self.kill_actor(camera_pos, enemy_list, map_render, player_actor)

            else:
                func.list_play(hit_sounds)

            return True
        return False


    def tick(self, phase = 0):

        times = {}
        t = time.perf_counter()

        if self.route_tick > 0:
            self.route_tick -= 1


        if self.hp < 250:
            self.hp += 0.1

        self.aim()
        state_tick = False

        times["aim"] = time.perf_counter() - t
        t = time.perf_counter()

        if self.state in ("attacking", "takingcover") and self.sees_target:
            self.shoot()
            self.investigating = True
        else:
            self.weapon.weapon_tick()

        times["shoot"] = time.perf_counter() - t
        t = time.perf_counter()

        if self.state_tick > 0:
            self.state_tick -= timedelta.mod(1)
        else:
            self.state_tick = 60
            self.get_state()
            self.state_react()
            state_tick = True

        times["state"] = time.perf_counter() - t
        t = time.perf_counter()

        # if not self.calculating:
        #
        #     if self.at_target_pos():
        #         self.investigate_route = False
        #         self.route = []
        #         self.target_pos = self.pos.copy()
        #
        #
        #     if not self.route:
        #         self.get_route_to_target()


        #
        self.move()

        times["move"] = time.perf_counter() - t
        t = time.perf_counter()

        self.aim_angle_target = func.get_angle(self.pos, self.aim_at)

        if self.angle != self.target_angle:

            if abs(self.target_angle - self.angle) > 1:
                self.angle = self.angle + timedelta.mod(
                    los.get_angle_diff(self.target_angle, self.angle)
                    * (self.anglular_acceleration)
                )
            else:
                self.angle = self.target_angle

        if self.aim_angle != self.aim_angle_target:

            if abs(self.aim_angle_target - self.angle) > 1:
                self.aim_angle = self.aim_angle + timedelta.mod(
                    los.get_angle_diff(self.aim_angle_target, self.aim_angle)
                    * (self.anglular_acceleration)
                )
            else:
                self.aim_angle = self.aim_angle_target

        times["angles"] = time.perf_counter() - t
        t = time.perf_counter()

        im = pygame.transform.rotate(self.im, (360-self.aim_angle))
        center = im.get_rect().center
        self.app.screen_copy.blit(im, func.minus(func.minus(self.pos, self.app.camera_pos, op = "-"), center, op = "-"))

        times["blit"] = time.perf_counter() - t
        t = time.perf_counter()

        for x in times:
            if x not in self.app.soldier_cache:
                self.app.soldier_cache[x] = times[x]
            else:
                self.app.soldier_cache[x] = self.app.soldier_cache[x] * (59/60) + times[x] * (1/60)


        #if self.calculating:
        if phase == 6:
            t = "PATROL LEADER" if (self is self.patrol.patrol_leader) else "TROOP"
            text = terminal.render(f"{t} {self.state} {self.collisions_with_walls}", False, [255, 255, 255])
            self.app.screen_copy.blit(text, func.minus(self.pos, self.app.camera_pos, op = "-"))
            pygame.draw.line(self.app.screen_copy, GREEN, func.minus(self.pos, self.app.camera_pos, op = "-"), func.minus(self.aim_at, self.app.camera_pos, op = "-"))

            last_pos = self.pos.copy()

            route = self.route.copy() + [self.target_pos]

            for x in route:

                pygame.draw.line(self.app.screen_copy, WHITE_COLOR if state_tick else RED_COLOR, func.minus(last_pos, self.app.camera_pos, op = "-"), func.minus(x, self.app.camera_pos, op = "-"))
                last_pos = x.copy()
