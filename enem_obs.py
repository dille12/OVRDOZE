import os, sys
import pygame
import math
import random
import time

pygame.init()
import func
from values import *
import level
import los
import pyperclip

width, height = size
import classes
from classes import items, drop_index, drop_table
import get_preferences
import armory
from classes import Inventory


class Enemy:
    def __init__(self, pos, weapon, interctables):
        self.pos = pos
        self.target_pos = pos
        self.moving_speed = random.uniform(1.5, 2.75)
        self.detection_range = random.randint(400, 600)
        self.detection_rate = 0.05
        self.target_angle = 0
        self.detected = False

        self.knockback_tick = 0
        self.knockback_angle = 0

        self.hp = 100

        self.weapon = weapon

        self.inventory = Inventory(interctables)
        for i in range(random.randint(2, 3)):
            if self.weapon.ammo != "INF":
                self.inventory.append_to_inv(
                    items[self.weapon.__dict__["ammo"]],
                    items[self.weapon.__dict__["ammo"]].__dict__["max_stack"],
                )
        self.weapon.set_hostile()

        self.angle = 0

    def kill(self, camera_pos, list, draw_blood_parts):
        list.remove(self)
        func.list_play(death_sounds)
        func.list_play(kill_sounds)

        # self.inventory.drop_inventory(self.pos)

        for i in range(5):
            particle_list.append(
                classes.Particle(
                    func.minus(self.pos, camera_pos),
                    type="blood_particle",
                    magnitude=1,
                    screen=draw_blood_parts,
                )
            )
        print("KILLED")

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

        self.knockback_tick = amount
        self.knockback_angle = angle

    def hit_detection(self, camera_pos, pos, lastpos, damage, enemy_list, map_render):
        points_1 = [[self.pos[0], self.pos[1] - 25], [self.pos[0], self.pos[1] + 25]]
        points_2 = [[self.pos[0] - 25, self.pos[1]], [self.pos[0] + 25, self.pos[1]]]

        if los.intersect(pos, lastpos, points_1[0], points_1[1]) or los.intersect(
            pos, lastpos, points_2[0], points_2[1]
        ):

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
        self.temp_pos = func.minus_list(self.pos, camera_pos)
        player_pos = player_actor.get_pos()
        pl_temp_pos = func.minus_list(player_pos, camera_pos)

        if self.knockback_tick != 0:

            self.pos = [
                self.pos[0] + math.cos(self.knockback_angle) * self.knockback_tick,
                self.pos[1] - math.sin(self.knockback_angle) * self.knockback_tick,
            ]
            self.knockback_tick -= 1

        # pygame.draw.rect(screen, [255,255,255],[self.temp_pos[0], self.temp_pos[1], 20, 20])

        if los.check_los(player_pos, self.pos, walls):  ## Render

            rot, rect = func.rot_center(
                player, self.angle, self.temp_pos[0], self.temp_pos[1]
            )
            rect = rot.get_rect().center
            screen.blit(rot, [self.temp_pos[0] - rect[0], self.temp_pos[1] - rect[1]])

            dist = los.get_dist_points(self.pos, player_pos)

            if dist < self.detection_range and player_actor.get_hp() > 0:

                if (
                    random.uniform(0, 1)
                    < (1 - dist / self.detection_range) * self.detection_rate
                ):
                    self.detected = True

                if self.detected:
                    self.target_angle = 180 - math.degrees(
                        math.atan2(
                            self.pos[1] - player_pos[1], self.pos[0] - player_pos[0]
                        )
                    )
                    if player_actor.get_hp() > 0:
                        func.weapon_fire(
                            self.weapon,
                            self.inventory,
                            self.angle,
                            self.pos,
                            screen,
                            ai=True,
                        )

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
                self.angle = (
                    self.angle + los.get_angle_diff(self.target_angle, self.angle) * 0.1
                )
            else:
                self.angle = self.target_angle

        if self.target_pos != self.pos:

            self.angle_rad = math.pi * 2 - math.atan2(
                self.target_pos[1] - self.pos[1], self.target_pos[0] - self.pos[0]
            )
            self.pos = [
                self.pos[0] + math.cos(self.angle_rad) * self.moving_speed,
                self.pos[1] - math.sin(self.angle_rad) * self.moving_speed,
            ]
            coll_pos = map.check_collision(self.pos, map_boundaries, collision_box=10)
            if coll_pos:
                self.pos = coll_pos
            if los.get_dist_points(self.pos, self.target_pos) < 50:
                self.target_pos = self.pos

        else:
            point = map.get_random_point(None, max_tries=1)
            if los.check_los(point, self.pos, walls):
                print("Wandering")
                self.target_angle = 180 - math.degrees(
                    math.atan2(self.pos[1] - point[1], self.pos[0] - point[0])
                )

                self.target_pos = point
                print("to", self.target_pos)
