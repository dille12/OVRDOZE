import os, sys
import pygame
import math
import random
import time
from unit_status import UnitStatus
pygame.init()
import func
from values import *
import level
import los
import pyperclip
import classes
from classes import items, drop_index, drop_table
import get_preferences
import armory
from _thread import *
import numpy as np

expl_blood = func.load_animation("anim/expl_blood", 0, 25)

class Zombie(pygame.sprite.Sprite):
    def __init__(
        self,
        app,
        pos,
        interctables,
        target_actor,
        NAV_MESH,
        walls,
        hp_diff=1,
        dam_diff=1,
        type="normal",
        wall_points=None,
        player_ref=None,
        identificator=random.randint(0, 4096),
        power=random.uniform(1.5, 2.75),
        map = None
    ):
        super().__init__()
        self.app = app
        self.identificator = identificator
        self.power = power
        self.pos = pos
        self.target_pos = pos
        self.tick_every = 1
        self.moving_speed = power*0.8
        self.detection_range = 300 * power
        self.detection_rate = 0.05 * self.tick_every
        self.target_angle = 0
        self.detected = False
        self.killed = False
        self.damage = round(3 * power * dam_diff)
        self.knockback_resistance = 1
        self.hp = 100 * hp_diff
        self.attack_speed = 30
        self.target = target_actor
        self.navmesh_ref = NAV_MESH.copy()
        self.wall_ref = walls
        self.player_ref = player_ref
        self.calculating = False
        self.class_type = "ZOMBIE"
        self.map = map


        if type == "normal":
            self.size = 10 * multiplier2
            self.image_template = zombie
            self.type = "normal"
            self.anglular_acceleration = 0.1
        elif type == "bomber":
            self.size = 13 * multiplier2
            self.image_template = bomber
            self.moving_speed *= 0.75
            self.hp *= 0.75
            self.explosion = expl_blood
            self.type = "bomber"
            self.attack_speed = 60
            self.anglular_acceleration = 0.025
        elif type == "runner":
            self.size = 10 * multiplier2
            self.image_template = zombie
            self.type = "runner"
            self.anglular_acceleration = 0.2
            self.moving_speed *= 1.75
            self.damage *= 0.75
        else:
            self.size = 20 * multiplier2
            self.image_template = zombie_big
            self.moving_speed *= 0.35
            self.damage *= 2
            self.hp *= 5
            self.knockback_resistance = 0.1
            self.anglular_acceleration = 0.05

            self.type = "big"



        self.attack_tick = 0
        self.route_tick = 0
        self.get_route_to_target()

        self.rect = self.image_template.get_rect()

        self.route = []
        self.stationary = 0

        self.tick_time = 0

        self.knockback_tick = 0
        self.knockback_angle = 0

        self.process_tick = 0

        self.times = {"total": 0}

        self.visible = False
        self.visible2 = False

        self.inventory = classes.Inventory(self.app, interctables)
        self.cached_route = False

        #app.zombiegroup.add(self)

        for i in range(random.randint(1, 9)):
            if random.uniform(0, 1) < 0.02:
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

        self.angle = 0

    def issue_event(self, event):
        zombie_events.append(f"ZEVENT:{self.identificator}_{event}")

    def kill_actor(
        self,
        camera_pos,
        list,
        draw_blood_parts,
        player_actor,
        silent=False,
        zevent=False,
    ):

        self.kill()
        list.remove(self)

        if not zevent:
            self.issue_event("terminate_1")

        if not silent:

            player_actor.money += random.randint(5, 10)
            money_tick.value = 0

            func.list_play(death_sounds)
            func.list_play(kill_sounds)

            if self.type == "bomber":
                explosions.append(
                    armory.Explosion(
                        func.minus(self.pos, [25, 25]),
                        expl_blood,
                        player_nade=True,
                        range=150,
                        particles="blood",
                        color_override="yellow",
                    )
                )

            self.inventory.drop_inventory(self.pos)

            if random.uniform(0,1) < 0.002:
                weapon = func.pick_random_from_dict(armory.guns, key = True)
                interactables.append(classes.Interactable(self.app, self.pos, self.target.inv, player_weapons = player_weapons, type = "gun_drop", item = armory.guns[weapon]))

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

    def get_string(self):
        return f"ZOMBIE:{str(round(self.pos[0]))}_{str(round(self.pos[1]))}_{str(self.identificator)}_{self.target.name}_{str(round(self.power,5))}_{self.type}"

    def set_hp(self, hp, reduce=False):
        if reduce:
            self.hp -= hp
        else:
            self.hp = hp

    def get_hp(self):
        return self.hp

    def get_hitbox(self):
        return [25, 25]

    def get_pos(self):
        return self.pos

    def knockback(self, amount, angle, daemon_bullet=False):

        self.knockback_tick = round(amount * self.knockback_resistance)
        self.knockback_angle = angle
        if not daemon_bullet:
            self.issue_event(f"setpos_{str(self.pos)}")

    def search_route(self):
        self.calculating = True
        self.route, self.cached_route = func.calc_route(
            self.pos, self.target.pos, self.navmesh_ref, [self.map.numpy_array_wall_los, self.map.numpy_array_wall_no_los], cache = self.app
        )
        self.issue_event(f"setroute_{str(self.route)}")
        self.issue_event(f"setpos_{str(self.pos)}")
        self.route_tick = 60
        self.calculating = False

    def get_route_to_target(self):

        if (
            self.route_tick == 0
            and self.target == self.player_ref
            and not self.calculating
        ):
            start_new_thread(self.search_route, ())

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

    def check_if_alive(self):
        if self.killed or self not in enemy_list:
            return False
        else:
            return True

    def tick(
        self,
        screen,
        map_boundaries,
        player_actor,
        camera_pos,
        map,
        walls,
        NAV_MESH,
        map_render,
        phase=0,
        wall_points=None,
    ):

        if self.route_tick != 0:
            self.route_tick -= 1

        if phase == 6:
            t_1 = time.time()

        if self.process_tick == self.tick_every:
            self.process_tick = 0
        else:
            self.process_tick += 1

        for melee_hit in melee_list:
            angle_to_melee = 360 - math.degrees(
                math.atan2(
                    self.pos[1] - melee_hit["pos"][1], self.pos[0] - melee_hit["pos"][0]
                )
            )
            if (
                los.get_dist_points(melee_hit["pos"], self.pos)
                < melee_hit["strike_range"]
                and los.get_angle_diff(abs(angle_to_melee), melee_hit["angle"])
                < melee_hit["arc"] / 2
            ):
                melee_hit_sound.stop()
                melee_hit_sound.play()
                self.knockback(melee_hit["damage"], math.radians(angle_to_melee))
                self.hp -= melee_hit["damage"]

        if self.attack_tick > 0:
            self.attack_tick -= timedelta.mod(1)

        self.temp_pos = func.minus_list(self.pos, camera_pos)
        player_pos = self.target.pos
        pl_temp_pos = func.minus_list(player_pos, camera_pos)

        last_pos = self.pos.copy()

        if self.knockback_tick > 0:

            self.pos = [
                self.pos[0]
                + timedelta.mod(math.cos(self.knockback_angle) * self.knockback_tick**0.5 * multiplier2),
                self.pos[1]
                - timedelta.mod(math.sin(self.knockback_angle) * self.knockback_tick**0.5 * multiplier2),
            ]
            self.knockback_tick -= timedelta.mod(1)

        if phase == 6:
            t_2 = time.time()

        if self.app.draw_los and self.process_tick == 0:

            self.visible = los.check_los_jit(player_actor.np_pos, np.array(self.pos), self.map.numpy_array_wall_los)
            self.visible2 = los.check_los_jit(player_actor.np_pos, np.array(self.pos), self.map.numpy_array_wall_no_los)

        if phase == 6:
            t_3 = time.time()

        # pygame.draw.rect(screen, [255,255,255],[self.temp_pos[0], self.temp_pos[1], 20, 20])

        for x in burn_list:
            if los.get_dist_points(x.pos, self.pos) < 40*multiplier2:
                self.hp -= timedelta.mod(1)

        self.target_angle = 180 - math.degrees(
            math.atan2(
                self.pos[1] - self.target_pos[1], self.pos[0] - self.target_pos[0]
            )
        )
        vis = False
        if self.visible or not self.app.draw_los:  ## Render
            rot, rect = func.rot_center(
                self.image_template, self.angle, self.temp_pos[0], self.temp_pos[1]
            )
            rect = rot.get_rect().center

            vis = True

        if vis:
            if not self.app.zombiegroup.has(self):
                self.app.zombiegroup.add(self)
        else:
            if self.app.zombiegroup.has(self):
                self.app.zombiegroup.remove(self)

        if self.app.zombiegroup.has(self):
            self.image = rot
            self.rect.x = self.temp_pos[0] - rect[0]
            self.rect.y = self.temp_pos[1] - rect[1]


        if phase == 6:
            t_4 = time.time()

        if self.visible and self.visible2:

            dist = los.get_dist_points(self.pos, player_pos)

            if dist < self.detection_range and self.target.hp > 0:

                if (
                    random.uniform(0, 1)
                    < (1 - dist / self.detection_range) * self.detection_rate
                ):
                    self.detected = True
            else:
                self.detected = False

        else:
            self.detected = False

        if phase == 6:
            t_5 = time.time()

        if self.detected:
            # self.target_angle = 180 - math.degrees(math.atan2(self.pos[1] - player_pos[1], self.pos[0] - player_pos[0]))
            if dist > 50 * multiplier2:

                self.target_pos = player_pos
                self.route = []

            else:
                self.target_pos = self.pos

                if self.attack_tick <= 0:
                    self.attack_tick = self.attack_speed
                    if self.type != "bomber":
                        self.target.hp -= self.damage
                        func.list_play(pl_hit)
                        self.app.screen_glitch = 5
                        try:
                            self.target.knockback(
                                self.damage, math.radians(90 + self.target_angle)
                            )
                        except:
                            pass
                    for i in range(3):
                        particle_list.append(
                            classes.Particle(
                                func.minus(self.target.pos, camera_pos),
                                type="blood_particle",
                                magnitude=0.5,
                                screen=map_render,
                            )
                        )

                elif (
                    0 < self.attack_tick < self.attack_speed / 2
                    and self.type == "bomber"
                ):
                    self.kill_actor(camera_pos, enemy_list, map_render, player_actor)

        if phase == 6:
            t_6 = time.time()

        if self.angle != self.target_angle:

            if abs(self.target_angle - self.angle) > 1:
                self.angle = self.angle + timedelta.mod(
                    los.get_angle_diff(self.target_angle, self.angle)
                    * (self.anglular_acceleration)
                )
            else:
                self.angle = self.target_angle

        if phase == 6:
            t_7 = time.time()

        if self.target_pos != self.pos:

            # self.angle_rad = math.pi*2 - math.atan2(self.target_pos[1] - self.pos[1], self.target_pos[0] - self.pos[0])
            self.angle_rad = math.radians(self.angle)
            self.pos = [
                self.pos[0]
                + timedelta.mod(math.cos(self.angle_rad) * self.moving_speed * multiplier2),
                self.pos[1]
                - timedelta.mod(math.sin(self.angle_rad) * self.moving_speed * multiplier2),
            ]

            if self.attack_tick <= 0:
                i = True
            else:
                i = False

            collision_types, coll_pos = map.checkcollision(
                self.pos,
                [
                    math.cos(self.angle_rad) * self.moving_speed,
                    self.pos[1] - math.sin(self.angle_rad) * self.moving_speed,
                ],
                self.size,
                map_boundaries,
                damage_barricades=i,
                damager=self,
            )
            self.pos = coll_pos
            if los.get_dist_points(self.pos, self.target_pos) < 50:
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

        if last_pos == self.pos and self.detected == False:

            self.stationary += 1
            if self.stationary > 10:
                self.get_route_to_target()
                try:
                    self.target_pos = self.route[0]
                except:
                    pass
        #
        else:
            self.stationary = 0

        if self.check_if_alive() and self.hp <= 0:
            self.kill_actor(camera_pos, enemy_list, map_render, player_actor)





        if phase == 6:
            t_9 = time.time()


        if phase == 6:


            if self.pos != self.target_pos:
                last_pos = self.target_pos

                if self.cached_route:
                    color = [255,0,0]
                else:
                    color = [255,255,255]

                pygame.draw.line(
                    screen,
                    color,
                    func.minus(self.pos, camera_pos, op="-"),
                    func.minus(self.target_pos, camera_pos, op="-"),
                )

                for tar in self.route:
                    pygame.draw.line(
                        screen,
                        color,
                        func.minus(last_pos, camera_pos, op="-"),
                        func.minus(tar, camera_pos, op="-"),
                    )
                    last_pos = tar
