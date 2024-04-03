from values import *
import os, sys
import pygame
import math
import random
import time
import func
from networking.server_object import MP_Object
import los
import classes

terminal = pygame.font.Font(fp("texture/terminal.ttf"), 20)
terminal2 = pygame.font.Font(fp("texture/terminal.ttf"), 30)
prompt = pygame.font.Font(fp("texture/terminal.ttf"), 14)

class Player_Multi(MP_Object):
    def __init__(self, username, app, weapons = None):
        self.app = app
        super().__init__()
        self.name = username
        self.pos = [0, 0]
        self.draw_pos = [0,0]
        self.hp = 100
        self.angle = 0
        self.draw_angle = 0
        self.player_blit = player
        self.killed = False

        self.last_tick = time.time()
        self.vel = [0, 0]
        self.acc = [0, 0]
        self.last_tick_pos = [0, 0]
        self.interpolations2 = []
        self.interpolations = []
        self.idle_ticks = 0
        self.time_overridden = None
        self.time_overridden_g = None
        self.weapons = weapons
        self.set_gun(0, "M1911")

    def set_gun(self, time, gun):

        if self.time_overridden_g == None:
            self.time_overridden_g = time
        else:
            if self.time_overridden_g > time:
                return
        self.time_overridden_g = time

        self.equipped_gun = self.weapons[gun].copy()
        self.equipped_gun.owner = self
        self.equipped_gun.app = self.app

    def set_hp(self, hp):
        self.hp = hp

    def check_if_alive(self):
        if self.killed:
            return False
        else:
            return True

    def kill_actor(self, camera_pos, dict, draw_blood_parts, player_actor):

        if self.killed:
            return

        func.list_play(death_sounds)
        func.list_play(kill_sounds)
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
        self.killed = True

    def force_player_damage(self, damage):
        if self.hp > 0:
            self.hp -= damage
            func.list_play(pl_hit)
        else:
            self.kill_actor(camera_pos, actor_list, map_render, player_actor)

    def hit_detection(
        self, camera_pos, pos, lastpos, damage, actor_list, map_render, player_actor
    ):

        if self.killed == True and self.hp == 100:
            self.killed = False

        if self.hp <= 0:
            return False

        points_1 = [[self.pos[0], self.pos[1] - 25], [self.pos[0], self.pos[1] + 25]]
        points_2 = [[self.pos[0] - 25, self.pos[1]], [self.pos[0] + 25, self.pos[1]]]

        if los.intersect(pos, lastpos, points_1[0], points_1[1]) or los.intersect(
            pos, lastpos, points_2[0], points_2[1]
        ):

            if self.hp - damage < 0:
                self.kill_actor(camera_pos, actor_list, map_render, player_actor)

            else:
                func.list_play(hit_sounds)

            return True
        return False

    def tick(self, screen, player_pos, camera_pos, walls, player_actor, map_render):

        if self.hp > 0:
            self.killed = False
        else:
            self.kill_actor(camera_pos, dict, map_render, player_actor)

        if self.killed:
            return

        if self.interpolations != []:
            self.pos = self.interpolations[0]
            self.interpolations.remove(self.interpolations[0])
            self.idle_ticks = 0
        else:
            self.idle_ticks += 1


        self.draw_pos = [
            self.draw_pos[0]
            + (-self.draw_pos[0] + self.pos[0]) * 0.4,
            self.draw_pos[1]
            + (-self.draw_pos[1] + self.pos[1]) * 0.4,
        ]

        self.draw_angle = self.draw_angle + (-self.draw_angle + self.angle) * 0.1

        # pygame.draw.circle(screen, [255,255,255], func.minus(self.pos,camera_pos, "-"),8)

        if (
            los.get_dist_points(player_pos, self.pos) > 1000
            or self.hp <= 0
            or los.check_los(player_pos, self.pos, walls) == False
        ):
            return

        if self.equipped_gun.name in ["GLOCK", "M1911", "FN57-S", "DESERTEAGLE"]:
            pl = player_pistol
        else:
            pl = player


        player_rotated, player_rotated_rect = func.rot_center(
            pl, self.draw_angle, self.draw_pos[0], self.draw_pos[1]
        )

        player_pos_center = player_rotated.get_rect().center
        player_pos_center = [
            self.draw_pos[0] - player_pos_center[0],
            self.draw_pos[1] - player_pos_center[1],
        ]
        offset = [
            player_rotated_rect[0] - self.draw_pos[0] - camera_pos[0],
            player_rotated_rect[1] - self.draw_pos[1] - camera_pos[1],
        ]
        screen.blit(player_rotated, [self.draw_pos[0] + offset[0], self.draw_pos[1] + offset[1]])

        # screen.blit(self.player_blit, func.minus_list(self.pos,camera_pos))
        self.name_text = prompt.render(self.name + str(self.hp), False, [255, 255, 255])
        text_rect = self.name_text.get_rect().size

        screen.blit(
            self.name_text,
            func.minus_list(
                func.minus_list(self.draw_pos, camera_pos), [text_rect[0] / 2, 25]
            ),
        )

        # for interpo in self.interpolations2:
        #     pygame.draw.circle(screen, [255,0,0], func.minus(interpo,camera_pos, "-"),5)

    def set_values(self, time, pos, angle):
        if self.time_overridden == None:
            self.time_overridden = time
        else:
            if self.time_overridden > time:
                return
        self.time_overridden = time
        self.pos = [pos[0] * multiplier2, pos[1] * multiplier2]
        self.angle = angle

    # def set_values(self, x, y, a, hp):
    #     if int(x) != self.pos[0] or int(y) != self.pos[1]:
    #
    #         interpolation = time.time() - self.last_tick
    #         self.last_tick = time.time()
    #         # print("INTERP:", interpolation)
    #
    #         inter_ticks = round(interpolation / (1 / 60))
    #
    #         self.interpolations = []
    #         for i in range(1, inter_ticks):
    #             i /= inter_ticks
    #             curve = func.BezierInterpolation(
    #                 [
    #                     self.pos,
    #                     [self.vel[0] + self.pos[0], self.vel[1] + self.pos[1]],
    #                     [int(x), int(y)],
    #                 ],
    #                 i,
    #             )
    #             self.interpolations.append(curve)
    #             self.interpolations2.append(curve)
    #
    #         self.vel = [(int(x) - self.pos[0]), (int(y) - self.pos[1])]
    #
    #         # print("VELO:", self.vel)
    #
    #     else:
    #         self.vel = [0, 0]
    #
    #     # self.pos = [int(x), int(y)]
    #     self.angle = int(a)
    #     self.hp = int(hp)
