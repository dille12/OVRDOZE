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

import get_preferences
import objects
import classes

a, draw_los, a, ultraviolence, a = get_preferences.pref()


terminal = pygame.font.Font('texture/terminal.ttf', 20)
terminal2 = pygame.font.Font('texture/terminal.ttf', 30)
prompt = pygame.font.Font('texture/terminal.ttf', 14)

class Melee:
    def __init__(self, mp = False,
            strike_count=2,
            damage=10,
            hostile = True,
            owner_object = None,
            strike_distance=150):
        self.owner = owner_object
        self.mp=mp;
        self.arc=1*math.pi;
        self.strike_distance = strike_range # what's a good melee range number? - lets see if we can't make this more adjustable  ## The attack distance for zombies is 100, so at least 150
        self.strikes_used=0;
        self.strikes=strike_count;
        self.damage = damage;


    def get_string(self):

        string = "MELEE:" + str(round(self.pos[0])) + "_" + str(round(self.pos[1])) + "_"+ str(round(self.target_pos[0])) + "_"+ str(round(self.target_pos[1]))
        return string


    def check_for_strike(self,r_click):
        if r_click == True and self.strikes_used < self.strikes: ##FIRE
            return True
        else:
            return False



    def tick(self,screen, r_click):

        pos = tuple(self.owner.get_pos())
        angle = self.owner.get_angle()

        if self.check_for_strike(r_click):
            melee_sound.stop()
            melee_sound.play()
            melee_list.append({"pos" : pos, "angle" : angle, "damage" : self.damage, "distance" : self.strike_distance, "arc" : self.arc})   #BULLET
            self.strikes_used += 1
        if self.strikes_used > 0:
            self.strikes_used -= 0.01
        else:
            self.strikes_used = 0




    def get_remaining_strikes(self):
        return self.__strikes-self._strikes_used





class Grenade:
    def __init__(self, pos, target_pos, type, mp = False):
        self.pos = pos
        self.mp = mp
        self.type = type
        self.angle_rad = math.atan2(target_pos[1] - pos[1], target_pos[0] - pos[0])
        self.velocity = los.get_dist_points(pos,target_pos) / 45

        if type == "HE Grenade":
            self.image = grenade

        elif type == "Molotov":
            self.image = molotov

        self.target_pos = target_pos

        self.lifetime = 60
        self.angle = random.randint(0,360)
        self.direction = func.pick_random_from_list([-1,1])
        self.height = 0
        self.angular_velocity = self.velocity
        self.vert_vel = 5
        print("GRENADE INIT")

    def get_string(self):
        return f"GRENADE:{self.type}_{str(round(self.pos[0]))}_{str(round(self.pos[1]))}_{str(round(self.target_pos[0]))}_{str(round(self.target_pos[1]))}"

    def molotov_explode(self, map):
        if self.type != "Molotov":
            return
        for i in range(15):
            random_angle = random.randint(0, 360)
            dist = random.randint(0,75)
            pos = [self.pos[0] + math.cos(random_angle)*dist, self.pos[1] + math.sin(random_angle)*dist]
            if list(classtest.getcollisionspoint(map.rectangles, pos)) == []:
                burn_list.append(classes.Burn(pos, 3, random.randint(500,600)))
        molotov_explode_sound.play()
        grenade_list.remove(self)


    def tick(self,screen, map_boundaries, player_pos, camera_pos, grenade_list, explosions, expl1, map, walls):

        self.last_pos = self.pos.copy()
        self.pos = [self.pos[0] + math.cos(self.angle_rad) * self.velocity, self.pos[1] + math.sin(self.angle_rad) *self.velocity - self.vert_vel ]

        coll_pos, vert_coll, hor_coll = map.check_collision(self.pos.copy(), map_boundaries, collision_box = 5, dir_coll = True)
        if coll_pos:
            print("HIT")
            self.molotov_explode(map)
            if vert_coll:
                self.angle_rad = math.pi - self.angle_rad

            elif hor_coll:
                self.angle_rad = 2*math.pi - self.angle_rad
                self.vert_vel = 0
            self.pos = coll_pos
            self.velocity = self.velocity * 0.5



        if abs(self.velocity) > 0.25:
            self.vert_vel -= 0.2
            self.height += self.vert_vel
            self.angle += self.direction * self.angular_velocity
        st_i, st_rect = func.rot_center(self.image, self.angle, self.pos[0], self.pos[1])
        if los.check_los(player_pos, self.pos, walls):
            screen.blit(st_i, func.minus_list(st_rect[:2],camera_pos))

        if self.height < 0 and abs(self.velocity) > 0.25:
            func.list_play(thuds)
            self.velocity = self.velocity * 0.5
            self.vert_vel = self.vert_vel*(-0.4)
            self.height = 0
            self.direction *= -1
            self.angular_velocity *= random.uniform(0.7,1.4)
            self.molotov_explode(map)
        # else:
        #     self.velocity = 0
        #     self.vert_vel = 0
        self.lifetime -= 1
        if self.lifetime == 0:
            grenade_list.remove(self)
            explosions.append(Explosion(self.pos, expl1, player_nade = True))






class Explosion:
    def __init__(self,pos,expl1, player_nade = False, range = 200, particles = "normal", color_override = "red"):
        print("EXPLOSION ADDED")
        self.pos = pos
        self.rect_cent = [100,100]
        self.ticks = 0
        self.range = range
        self.images = expl1
        self.player = player_nade
        self.particles = particles
        self.c_o = color_override

    def damage_actor(self, actor, camera_pos, enemy = False, enemy_list = [], blood_surf = screen, multi_kill = 0, multi_kill_ticks = 0, walls = []):
        dist = func.get_dist_points(actor.get_pos(), self.pos)
        if dist < self.range:
            if los.check_los(self.pos, actor.get_pos(), walls) == False:
                if self.player:
                    return multi_kill, multi_kill_ticks
                return

            angle = math.atan2(actor.get_pos()[1] - self.pos[1] , actor.get_pos()[0] - self.pos[0] )
            actor.set_hp(round(self.range -dist), reduce = True)
            try:
                actor.knockback(round((200-dist)/10), angle)
            except:
                pass
            if enemy and actor.get_hp() < 0:
                if self.player:
                    multi_kill += 1
                    multi_kill_ticks = 120
                actor.kill(camera_pos, enemy_list, blood_surf)

        if self.player:
            return multi_kill, multi_kill_ticks

        return None, None






    def tick(self,screen, player_actor, enemy_list ,map_render,camera_pos,explosions, multi_kill, multi_kill_ticks, walls):
        if self.ticks == 0:


            if self.particles == "blood":
                explosion_blood_sound.stop()
                explosion_blood_sound.play()
            else:
                func.list_play(explosion_sound)

            st_i, st_rect = func.rot_center(func.pick_random_from_list(stains), random.randint(0,360), self.pos[0], self.pos[1])
            self.damage_actor(player_actor, camera_pos, walls = walls)
            for x in enemy_list:
                multi_kill, multi_kill_ticks = self.damage_actor(x, camera_pos, enemy = True, enemy_list = enemy_list, blood_surf = map_render, multi_kill = multi_kill, multi_kill_ticks = multi_kill_ticks, walls = walls)



            if self.particles != "blood":

                map_render.blit(st_i, st_rect) #func.minus_list(self.pos,stains[0].get_rect().center)
            if self.particles == "normal":
                for aids in range(50):
                    particle_list.append(classes.Particle(self.pos, magnitude = 3, screen = screen))
            else:
                for aids in range(50):
                    particle_list.append(classes.Particle(func.minus(self.pos,camera_pos), magnitude = random.uniform(0.6,1.7), type = "blood_particle", screen = map_render, color_override = self.c_o ))

        screen.blit(self.images[self.ticks], func.minus_list(func.minus_list(self.pos,camera_pos),self.rect_cent))
        self.ticks += 1

        if self.ticks == len(self.images):
            explosions.remove(self)
        return multi_kill, multi_kill_ticks





class Weapon:
    def __init__(self,name,clip_s,fire_r,spread,spread_r,reload_r,damage, bullets_at_once = 1, burst = False, burst_fire_rate = 3, burst_bullets = 3, shotgun = False, spread_per_bullet = 1, handling = 1, semi_auto = False, bullet_speed = 20, piercing = False, ammo_cap_lvlup = 5, ammo = "9MM", image = "", enemy_weapon = False, sounds = {"fire": weapon_fire_Sounds, "reload": reload}, view = 0.03):
        self.__clip_size = clip_s
        self.__bullets_in_clip = 0
        self.__bullet_per_min = fire_r
        self.__firerate = tick_count/(fire_r/60)

        self.spread_per_bullet = spread_per_bullet
        self.piercing_bullets = piercing

        self.__name = name
        self.__spread = spread
        self.__spread_recovery = spread_r
        self.__reload_rate = reload_r
        self.__damage = damage
        self.__orig_fr = fire_r
        self.semi_auto = semi_auto
        self.semi_auto_click = False
        self.__doubledamage_time = 0
        self.__bullets_at_once = bullets_at_once
        self.__shotgun = shotgun
        self.__ammo_cap_lvlup = ammo_cap_lvlup
        self.bullet_speed = bullet_speed
        self.__c_bullet_spread = 0
        self.__reload_tick = 0
        self.__weapon_fire_Tick = 0
        self.enemy_weapon = enemy_weapon
        self.sounds = sounds["fire"]
        self.reload_sound = sounds["reload"]
        self.image_dir = image
        self.ammo = ammo
        self.view = view
        self.handling = handling

        self.burst = burst
        self.burst_bullets = burst_bullets
        self.burst_fire_rate = burst_fire_rate
        self.burst_tick = 0
        self.current_burst_bullet = 0

        self.team = "hostile" if enemy_weapon else "friendly"
        if image != "":

            self.picture = func.colorize(pygame.image.load(f"texture/guns/{image}"), pygame.Color(hud_color[0], hud_color[1], hud_color[2]))

            print("Image loaded")

    def add_to_spread(self, amount):
        self.__c_bullet_spread += amount


    def copy(self):
        return Weapon(self.__name, clip_s = self.__clip_size,
        fire_r = self.__bullet_per_min,
        spread = self.__spread,
        spread_r = self.__spread_recovery,
        spread_per_bullet = self.spread_per_bullet,
        reload_r = self.__reload_rate,
        damage = self.__damage,
        bullets_at_once = self.__bullets_at_once,
        sounds = {"fire": self.sounds, "reload": self.reload_sound},
        bullet_speed = self.bullet_speed,
        shotgun = self.__shotgun,
        ammo_cap_lvlup = self.__ammo_cap_lvlup,
        image = self.image_dir,
        semi_auto = self.semi_auto,
        ammo = self.ammo,
        piercing = self.piercing_bullets,
        view = self.view,
        handling = self.handling,
        burst = self.burst,
        burst_bullets = self.burst_bullets,
        burst_fire_rate = self.burst_fire_rate)




    def set_hostile(self):
        self.team = "hostile"

    def get_image(self):
        return self.picture

    def get_semi_auto(self):
        return self.semi_auto


    def fire(self,bullet_pos,angle, screen):

        radian_angle = math.radians(angle) - 0.16184 + math.pi/2

        c = 198.59507*0.36919315403/1.875

        x_offset = math.sin(radian_angle)*c
        y_offset = math.cos(radian_angle)*c
        bul_pos = [bullet_pos[0]+x_offset,bullet_pos[1]+y_offset]
        multiplier = 2 if self.__doubledamage_time == True else 1
        func.list_play(self.sounds)
        spread_cumulative = 0
        for x in range(self.__bullets_at_once):



            if self.__bullets_in_clip > 0:
                bullet_list.append(objects.Bullet(bul_pos,angle+random.uniform(-self.__spread-self.__c_bullet_spread,self.__spread+self.__c_bullet_spread),self.__damage * multiplier, team = self.team, speed = self.bullet_speed, piercing = self.piercing_bullets))   #BULLET
                for x in range(random.randint(8,16)):
                    particle_list.append(classes.Particle(bul_pos, pre_defined_angle = True, angle = angle+90,magnitude = self.__damage**0.1- 0.5, screen = screen))

                if self.__shotgun == False:
                    self.__bullets_in_clip -= 1

            spread_cumulative += self.spread_per_bullet

        self.__c_bullet_spread += spread_cumulative


        if self.__shotgun == True:
            self.__bullets_in_clip -= 1

        if self.burst:
            self.burst_tick = self.burst_fire_rate
            self.current_burst_bullet -= 1

        self.__weapon_fire_Tick += self.__firerate



    def spread_recoverial(self):
        self.__c_bullet_spread *= self.__spread_recovery

    def check_for_Fire(self,click):

        if self.semi_auto:
            if click and self.semi_auto_click == False and self.__bullets_in_clip > 0:
                self.semi_auto_click = True
                return True
            elif click == False:
                self.semi_auto_click = False
            return False

        elif self.burst:

            return bool(click and self.burst_tick == 0 and self.current_burst_bullet == 0 and self.__bullets_in_clip > 0)

        return click == True and self.__bullets_in_clip > 0

    def get_Ammo(self):
        return self.__bullets_in_clip

    def reload(self, player_inventory):

        if self.ammo == "INF":
            availabe_ammo = 1000
        else:
            availabe_ammo = player_inventory.get_amount_of_type(self.ammo)

        if self.__bullets_in_clip == 0:

            ammo_to_reload = self.__clip_size
        else:
            ammo_to_reload = self.__clip_size - self.__bullets_in_clip + 1

        if availabe_ammo == 0:
            return

        to_reload = ammo_to_reload if ammo_to_reload < availabe_ammo else availabe_ammo
        self.reload_sound.play()
        self.__reload_tick = self.__reload_rate

        self.__bullets_in_clip += to_reload
        if self.ammo != "INF":
            player_inventory.remove_amount(self.ammo, to_reload)



    def get_reload_rate(self):
        return self.__reload_rate

    def get_firerate(self):
        return self.__firerate

    def get_clip_size(self):
        return self.__clip_size

    def upgrade_firerate(self):
        if self.__shotgun == True:
            self.__bullets_at_once += 1
        else:
            self.__bullet_per_min += 50
            self.__firerate = 60/(self.__bullet_per_min/60)

    def reload_tick(self):
        return self.__reload_tick


    def upgrade_clip_size(self):
        self.__clip_size += self.__ammo_cap_lvlup
        if self.__shotgun == False:
            self.__clip_size += self.__bullets_at_once - 1


    def upgrade_damage(self):
        self.__damage += 0.5

    def double_damage(self, state):
        self.__doubledamage_time = state

    def weapon_tick(self):
        if self.__reload_tick != 0:
            self.__reload_tick -= 1
        if self.__weapon_fire_Tick > 0:
            self.__weapon_fire_Tick -= 1

    def weapon_fire_Tick(self):
        return self.__weapon_fire_Tick
