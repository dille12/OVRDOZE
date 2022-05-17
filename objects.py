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

import get_preferences

a, draw_los, a, a, ultraviolence, a = get_preferences.pref()


terminal = pygame.font.Font('texture/terminal.ttf', 20)
terminal2 = pygame.font.Font('texture/terminal.ttf', 30)
prompt = pygame.font.Font('texture/terminal.ttf', 14)


class Bullet:
    def __init__(self, pos,angle,damage, deal_damage_to_player = False, team = "hostile",speed = 20, piercing = False, mp = False):
        self.__pos = pos.copy()
        self.mp = mp
        self.__deal_damage_to_player = deal_damage_to_player

        self.speed = speed * random.uniform(0.9,1.1)

        self.im = bullet_length[round(self.speed)]

        self.team = team
        self.piercing = piercing
        self.actors_hit = []


        self.__angle = angle
        self.__angle_radians = math.radians(self.__angle) + math.pi/2
        self.__damage = damage
        rotated_image = pygame.transform.rotate(bullet, self.__angle)
        new_rect = rotated_image.get_rect(center = bullet.get_rect(center = self.__pos).center)

        self.__pos = [new_rect[0],new_rect[1]]

        self.lifetime = 30


    def get_string(self):
        string = "BULLET:" + str(round(self.__pos[0])) + "_" + str(round(self.__pos[1])) + "_"+ str(round(self.__angle)) + "_"+ str(round(self.__damage)) + "_"+ str(round(self.speed))
        return string
    def move_and_draw_Bullet(self,screen,camera_pos, map_boundaries, map, enemy_list, player, draw_blood_parts = screen, dummies = {}):
        self.lifetime -= 1
        if self.lifetime == 0:
            print("Bullet deleted")
            bullet_list.remove(self)
            return



        self.__last_pos = self.__pos.copy()
        self.__pos[0] += math.sin(self.__angle_radians)*self.speed
        self.__pos[1] += math.cos(self.__angle_radians)*self.speed
        try:
            angle_coll = map.check_collision(self.__pos, map_boundaries, return_only_collision = True, collision_box = 0)
            if angle_coll != False:
                func.list_play(rico_sounds)
                bullet_list.remove(self)
                for i in range(8):
                    particle_list.append(classes.Particle(angle_coll, magnitude = 1, pre_defined_angle = True, angle = 90-self.__angle, screen = screen))

        except Exception as e:
            print("exception")
            print(e)

        rot_bullet, rot_bullet_rect = func.rot_center(self.im,self.__angle,self.__pos[0],self.__pos[1])

        crystal_pay = False



        if self.team == "hostile":
            if classes.player_hit_detection(self.__pos, self.__last_pos, player, self.__damage):
                for i in range(3):
                    particle_list.append(classes.Particle(func.minus(self.__pos, camera_pos), type = "blood_particle", magnitude = 0.5, pre_defined_angle = True, screen = draw_blood_parts, angle = self.__angle + random.randint(45,135)))
                try:
                    if not self.piercing:
                        bullet_list.remove(self)
                except:
                    pass

        if dummies != {}:
            for x in dummies:
                if dummies[x].hit_detection(camera_pos, self.__pos, self.__last_pos,self.__damage, dummies, draw_blood_parts) == True:
                    particle_list.append(classes.Particle(func.minus(self.__pos, camera_pos), type = "blood_particle", magnitude = 0.5, pre_defined_angle = True, screen = draw_blood_parts, angle = self.__angle + random.randint(45,135)))
                    try:
                        if not self.piercing:
                            bullet_list.remove(self)
                    except:
                        pass

                    if dummies[x].check_if_alive():
                        return False
                    else:
                        return True



        dead = 0
        for x in enemy_list:
            if x.hit_detection(camera_pos, self.__pos, self.__last_pos,self.__damage, enemy_list, draw_blood_parts) == True:

                x.knockback(self.__damage, math.radians(self.__angle), daemon_bullet = self.mp)

                try:
                    if x.check_if_alive():
                        dead = False
                        for i in range(3):
                            particle_list.append(classes.Particle(func.minus(self.__pos, camera_pos), type = "blood_particle", magnitude = 0.5, pre_defined_angle = True, screen = draw_blood_parts, angle = self.__angle + random.randint(45,135)))
                    else:
                        dead += 1

                except:
                    print("")
                try:
                    if not self.piercing:
                        bullet_list.remove(self)
                except:
                    pass


        bullet_draw_pos = [rot_bullet_rect[0] , rot_bullet_rect[1] ]

        screen.blit(rot_bullet,func.draw_pos(self.__pos,camera_pos))
        return dead


class Turret:
    def __init__(self,pos,turning_speed,firerate,range,damage= 1,lifetime = 100):
        self.__pos = pos.copy()
        self.__turning_speed = turning_speed
        self.__firerate = firerate
        self.__angle = 0
        self.__turret_tick = firerate
        self.__range = range
        self.__lifetime = lifetime
        self.__lifetime2 =  lifetime
        self.__tick = 0
        self.__aiming_at = 0

        self.size = turret.get_rect().size[0]/2
        self.target = None

        self.__damage = damage

    def get_string(self):
        return f"TURRET:{str(round(self.__pos[0]))}_{str(round(self.__pos[1]))}_{str(self.__turning_speed)}_{str(self.__firerate)}_{str(self.__range)}_{str(self.__damage)}_{str(self.__lifetime)}"

    def scan_for_enemies(self,enemy_list, walls):
        lowest = 99999
        closest_enemy = None
        for x in enemy_list:
            if not los.check_los(self.__pos, x.get_pos(), walls):
                continue
            dist = los.get_dist_points(self.__pos, x.get_pos())
            if dist > self.__range:
                continue
            if dist < lowest and dist < self.__range:
                lowest = dist
                closest_enemy = x
        return closest_enemy

    def tick(self, screen ,camera_pos,enemy_list,tick, walls, player_pos):
        shoot = False
        aim_at = None
        if self.target == None:
            self.target = self.scan_for_enemies(enemy_list, walls)
        else:
            if los.check_los(self.__pos, self.target.get_pos(), walls) and los.get_dist_points(self.__pos, self.target.get_pos()) < self.__range and self.target.check_if_alive():
                aim_at = self.target.get_pos()
            else:
                self.target = None


        if aim_at != None:
            self.__aiming_at = func.get_angle(self.__pos,aim_at)
            shoot = True

        elif shoot == False and random.randint(1,300) == 1:
            self.__aiming_at = random.randint(0,round(360/self.__turning_speed)) * self.__turning_speed

        else:
            self.__angle = round(self.__angle/self.__turning_speed)*self.__turning_speed
            self.__aiming_at = round(self.__aiming_at/self.__turning_speed)*self.__turning_speed

        if abs((360-self.__aiming_at) - self.__angle) > self.__turning_speed * 2 -1 :
            angle2 = 360 - self.__aiming_at
            while angle2 >= 360:
                angle2 -= 360
            while angle2 < 0:
                angle2 += 360

            if angle2 - self.__angle > 180:
                angle2 -= 360

            if abs(angle2 - self.__angle) < self.__turning_speed:
                self.__angle = angle2
            else:
                if angle2 > self.__angle:
                    self.__angle += self.__turning_speed
                elif angle2 < self.__angle:
                    self.__angle -= self.__turning_speed
        else:

            angle2 = self.__angle

        turret2, turret_rect = func.rot_center(turret,self.__angle,self.__pos[0],self.__pos[1])

        if abs(los.get_angle_diff(360 - (func.get_angle(self.__pos,player_pos)), self.__angle)) < 20 or los.get_dist_points(player_pos, self.__pos) < 25:
            shoot = False

        if shoot == True and self.__turret_tick == 0 and abs(angle2-self.__angle) < self.__turning_speed * 2:
            turret_fire1.stop()
            turret_fire2.stop()
            turret_fire3.stop()

            func.pick_random_from_list(turret_fire).play()
            bullet_list.append(Bullet([self.__pos[0], self.__pos[1]],self.__angle+random.uniform(-10,10),self.__damage))

            for x in range(random.randint(4,6)):
                particle_list.append(classes.Particle([self.__pos[0], self.__pos[1]], pre_defined_angle = True, angle = self.__angle+90, magnitude = 2))

            self.__lifetime -= 1

            self.__turret_tick = self.__firerate
        elif self.__turret_tick != 0 and shoot == True:
            self.__turret_tick -= 1

        rad = math.radians(360-self.__angle)

        dp = func.draw_pos(self.__pos,camera_pos)
        screen.blit(turret_leg, [dp[0] - self.size, dp[1] - self.size])
        screen.blit(turret2,func.draw_pos(turret_rect,camera_pos))


        if self.__lifetime == 0:
            turret_list.remove(self)
        elif self.__lifetime/self.__lifetime2 <= 0.2:
            func.render_cool(huuto,[turret_rect[0]+35-camera_pos[0], turret_rect[1]+35-camera_pos[1]],self.__tick,16,True, screen = screen)
            self.__tick += 1



class Barricade:
    def __init__(self, origin):
        self.pos = origin

        self.hp = 1000

        self.stage = "building_1"






    def tick(self, screen, camera_pos, mouse_pos = [0,0], clicked = False, map = None):

        if self.hp <= 0:
            map.__dict__["rectangles"].remove(self.rect)
            map.__dict__["barricade_rects"].remove([self.rect, self])
            return "KILL"

        if self.stage == "building_1":
            x = mouse_pos[0] + camera_pos[0]
            y = mouse_pos[1] + camera_pos[1]
            pygame.draw.circle(screen, [0,204,0], [x-camera_pos[0],y-camera_pos[1]], 5)

            if clicked:
                self.pos = [x,y]
                self.stage = "building_2"





        elif self.stage == "building_2":

            w =  (mouse_pos[0] + camera_pos[0])-self.pos[0]
            h = mouse_pos[1]+ camera_pos[1]-self.pos[1]



            x = self.pos[0]-camera_pos[0]
            y = self.pos[1]-camera_pos[1]


            if w < 0:
                x += w
                w = abs(w)

            if h < 0:
                y += h
                h = abs(h)

            area = w*h


            if area > 5000 or w < 20 or h < 20:
                clear = False
                color = [204,0,0]
            else:
                clear = True
                color = [0,204,0]

            rect_1 = pygame.Rect(x, y, w, h)

            rect_2 = pygame.Rect(x+camera_pos[0], y+camera_pos[1], w, h)

            collisions = list(classtest.getcollisions(map.__dict__["rectangles"], rect_2))
            if collisions:
                clear = False
                color = [204,0,0]


            pygame.draw.rect(screen, color, rect_1 ,3)

            if clicked and clear:
                self.width = w
                self.height = h
                self.stage = "built"
                self.pos = [x + camera_pos[0],y + camera_pos[1]]
                self.rect = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)

                self.surf = pygame.Surface([w,h]).convert()

                for x in range(round(w/100+0.49)):
                    for y in range(round(h/100+0.49)):
                        self.surf.blit(barricade_texture,[x*100,y*100], area = [0,0,self.width, self.height])
                        print("BLITTED IN:", x, y)

                map.__dict__["rectangles"].append(self.rect)
                map.__dict__["barricade_rects"].append([self.rect, self])

                print(map.__dict__["barricade_rects"])

                return True
            else:
                return "revert" if clicked else False



        else:
            screen.blit(self.surf, [self.pos[0]-camera_pos[0], self.pos[1]-camera_pos[1]]) #
            #pygame.draw.rect(screen, [61, 61, 41], pygame.Rect(self.pos[0]-camera_pos[0], self.pos[1]-camera_pos[1], self.width, self.height))
            pygame.draw.rect(screen, [round(((1000-self.hp)/1000)*255), round((self.hp/1000)*255), 0], pygame.Rect(self.pos[0]-camera_pos[0], self.pos[1]-camera_pos[1], self.width, self.height),2)
            pygame.draw.rect(screen, [0,0,0], pygame.Rect(self.pos[0]-camera_pos[0], self.pos[1]-camera_pos[1], self.width, self.height),1)
