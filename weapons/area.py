import math
import los
import func
from values import *
import classes
import classtest
from weapons.weapon import Weapon

class Grenade(Weapon):
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
        return super().get_string("GRENADE")

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

    def damage_actor(self, actor, camera_pos, blood_surf=None, enemy = False, enemy_list = [], multi_kill = 0, multi_kill_ticks = 0, walls = []):
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
                multi_kill, multi_kill_ticks = self.damage_actor(x, camera_pos, map_render, enemy = True, enemy_list = enemy_list, multi_kill = multi_kill, multi_kill_ticks = multi_kill_ticks, walls = walls)



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

