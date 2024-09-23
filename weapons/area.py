import math
import core.los as los
import core.func as func
from core.values import *
import core.classes as classes
import core.level as level
from weapons.weapon import Weapon
from game_objects.objects import *
from game_objects.bullet import Bullet


class Grenade(Weapon):
    def __init__(self, pos, target_pos, type, mp=False):
        self.pos = pos
        self.mp = mp
        self.type = type
        self.angle_rad = math.atan2(target_pos[1] - pos[1], target_pos[0] - pos[0])
        self.velocity = los.get_dist_points(pos, target_pos) / 45

        if type == "HE":
            self.image = grenade

        elif type == "Molotov":
            self.image = molotov
        else:
            print("ERROR : ", type)

        self.target_pos = target_pos

        self.lifetime = 60
        self.angle = random.randint(0, 360)
        self.direction = func.pick_random_from_list([-1, 1])
        self.height = 0
        self.angular_velocity = self.velocity
        self.vert_vel = 5

    def get_string(self):
        return super().get_string("GRENADE")

    def molotov_explode(self, map):
        if self.type != "Molotov":
            return
        for i in range(15):
            random_angle = random.randint(0, 360)
            dist = random.randint(0, 130) * multiplier2
            pos = [
                self.pos[0] + math.cos(random_angle) * dist,
                self.pos[1] + math.sin(random_angle) * dist,
            ]
            if list(level.getcollisionspoint(map.rectangles, pos)) == []:
                burn_list.append(classes.Burn(map, pos, 3, random.randint(500, 600)))
        molotov_explode_sound.play()
        try:
            grenade_list.remove(self)
        except:
            pass

    def tick(
        self,
        screen,
        map_boundaries,
        player_pos,
        camera_pos,
        grenade_list,
        explosions,
        expl1,
        map,
        walls,
    ):

        self.last_pos = self.pos.copy()
        self.pos = [
            self.pos[0] + timedelta.mod(math.cos(self.angle_rad) * self.velocity),
            self.pos[1]
            + timedelta.mod(math.sin(self.angle_rad) * self.velocity - self.vert_vel),
        ]

        coll_pos, vert_coll, hor_coll = map.check_collision(
            self.pos.copy(), map_boundaries, collision_box=5, dir_coll=True
        )
        if coll_pos:
            self.molotov_explode(map)
            if vert_coll:
                self.angle_rad = math.pi - self.angle_rad

            elif hor_coll:
                self.angle_rad = 2 * math.pi - self.angle_rad
                self.vert_vel = 0
            self.pos = coll_pos
            self.velocity = self.velocity * 0.5

        if abs(self.velocity) > 0.25:
            self.vert_vel -= timedelta.mod(0.2)
            self.height += timedelta.mod(self.vert_vel)
            self.angle += timedelta.mod(self.direction * self.angular_velocity)
        st_i, st_rect = func.rot_center(
            self.image, self.angle, self.pos[0], self.pos[1]
        )
        if los.check_los(player_pos, self.pos, walls):
            screen.blit(st_i, func.minus_list(st_rect[:2], camera_pos))

        if self.height < 0 and abs(self.velocity) > 0.25:
            func.list_play(thuds)
            self.velocity = self.velocity * 0.5
            self.vert_vel = self.vert_vel * (-0.4)
            self.height = 0
            self.direction *= -1
            self.angular_velocity *= random.uniform(0.7, 1.4)
            self.molotov_explode(map)
        # else:
        #     self.velocity = 0
        #     self.vert_vel = 0
        self.lifetime -= timedelta.mod(1)
        if self.lifetime <= 0:
            grenade_list.remove(self)
            explosions.append(Explosion(self.pos, expl1, player_nade=True))
            for i in range(50):
                bullet_list.append(
                    Bullet(
                        [self.pos[0]/multiplier2, self.pos[1]/multiplier2],
                        random.uniform(0, 360),
                        15,
                        hostile=True,
                        speed=15,
                        piercing=False,
                    )
                )  # BULLET)


class Explosion:
    def __init__(
        self,
        pos,
        expl1,
        player_nade=False,
        range=200,
        particles="normal",
        color_override="red",
        player_damage_mult = 1,
        firedFrom = ""
    ):
        self.pos = pos
        if expl1 != "small":
            self.rect_cent = expl1[0].get_rect().center
            self.small = False
        else:
            self.small = True
        self.ticks = 0
        self.range = range
        self.images = expl1
        self.player = player_nade
        self.particles = particles
        self.c_o = color_override
        self.player_damage = player_damage_mult
        self.firedFrom = firedFrom

    def damage_actor(
        self,
        player_actor,
        actor,
        camera_pos,
        blood_surf=None,
        enemy=False,
        enemy_list=[],
        multi_kill=0,
        multi_kill_ticks=0,
        walls=[],
        mult = 1
    ):
        dist = func.get_dist_points(actor.get_pos(), self.pos)
        if dist < self.range*mult:
            if los.check_los(self.pos, actor.get_pos(), walls) == False:
                if self.player:
                    return multi_kill, multi_kill_ticks
                return None, None

            angle = math.atan2(
                actor.get_pos()[1] - self.pos[1], actor.get_pos()[0] - self.pos[0]
            )
            actor.set_hp(round(self.range - dist)*mult, reduce=True)
            try:
                actor.knockback(round(mult * (200 - dist) / 10), angle)
            except:
                pass
            if enemy and actor.get_hp() < 0:
                if self.player:
                    multi_kill += 1
                    multi_kill_ticks = 120
                actor.kill_actor(camera_pos, enemy_list, blood_surf, player_actor, firedFrom = self.firedFrom)

        if self.player:
            return multi_kill, multi_kill_ticks

        return None, None

    def tick(
        self,
        screen,
        player_actor,
        enemy_list,
        map_render,
        camera_pos,
        explosions,
        multi_kill,
        multi_kill_ticks,
        walls,
    ):
        if self.ticks == 0:

            if self.small:
                for aids in range(15):
                    particle_list.append(
                        classes.Particle(
                            self.pos,
                            magnitude=1.5,
                            screen=screen,
                            color_override = [random.randint(180,190), random.randint(110,130), random.randint(30,50)]
                            )
                    )
                explosions.remove(self)

            if self.particles == "blood":
                explosion_blood_sound.stop()
                explosion_blood_sound.play()
            else:
                if self.small:
                    func.list_play(sm_explosion_sound)
                else:
                    func.list_play(explosion_sound)

            if not self.small:

                st_i, st_rect = func.rot_center(
                    func.pick_random_from_list(stains),
                    random.randint(0, 360),
                    self.pos[0],
                    self.pos[1],
                )

            self.damage_actor(player_actor, player_actor, camera_pos, walls=walls, mult = self.player_damage)
            for x in enemy_list:
                multi_kill, multi_kill_ticks = self.damage_actor(
                    player_actor,
                    x,
                    camera_pos,
                    map_render,
                    enemy=True,
                    enemy_list=enemy_list,
                    multi_kill=multi_kill,
                    multi_kill_ticks=multi_kill_ticks,
                    walls=walls,
                )

            if self.particles != "blood" and not self.small:

                map_render.blit(
                    st_i, st_rect
                )  # func.minus_list(self.pos,stains[0].get_rect().center)

            if not self.small:

                if self.particles == "normal":
                    for aids in range(50):
                        particle_list.append(
                            classes.Particle(self.pos, magnitude=3, screen=screen)
                            )
                else:
                    for aids in range(50):
                        particle_list.append(
                            classes.Particle(
                                func.minus(self.pos, camera_pos),
                                magnitude=random.uniform(0.6, 1.7),
                                type="blood_particle",
                                screen=map_render,
                                color_override=self.c_o,
                            )
                        )
        if not self.small:
            screen.blit(
                self.images[min((round(self.ticks), len(self.images)-1))],
                func.minus_list(func.minus_list(self.pos, camera_pos), self.rect_cent),
            )
            self.ticks += timedelta.mod(1)

            if self.ticks > len(self.images):
                explosions.remove(self)

        return multi_kill, multi_kill_ticks
