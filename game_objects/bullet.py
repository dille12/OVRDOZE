from game_objects.game_object import Game_Object
from values import *
import func
import classes
from anim_list import *
from classtest import getcollisionspoint


class Bullet(Game_Object):
    def __init__(
        self,
        pos,
        angle,
        damage,
        hostile=True,
        speed=20,
        piercing=False,
        mp=False,
        energy=False,
        rocket=False
    ):
        super().__init__(
            name="bullet",
            pos=pos,
            hostile=hostile,
            angle=angle,
            damage=damage,
            friendly_fire=False,
            lifetime=30,
            texture=energy_bullet_length[round(speed)] if energy else bullet_length[round(speed)],
        )
        self.mp = mp
        self.speed = speed * random.uniform(0.9, 1.1)
        self.energy = energy
        self.rocket = rocket
        if type != "shrapnel":
            if self.energy:
                self.im = energy_bullet_length[round(self.speed)]
            elif self.rocket:
                self.im = rocket_texture
            else:
                self.im = bullet_length[round(self.speed)]
            self.type = "bullet"
        else:
            self.type = "shrapnel"

        self.piercing = piercing

        self.added_explosion = False


    def get_string(self):
        return super().get_string("BULLET")

    def move(self):
        self._last_pos = self._pos.copy()
        self._pos[0] += math.sin(self._angle_radians) * self.speed * timedelta.timedelta * multiplier2
        self._pos[1] += math.cos(self._angle_radians) * self.speed * timedelta.timedelta * multiplier2
        pass

    def draw(self):
        pass

    def detect_collision(self):
        pass

    def kill_bullet(self, add_expl = True):

        if self.rocket and add_expl and not self.added_explosion:
            append_explosions.append([self._pos, expl1])
            self.added_explosion = True
            #explosions.append(Explosion(self._pos, expl1))

        bullet_list.remove(self)


    def move_and_draw_Bullet(
        self,
        screen,
        camera_pos,
        map_boundaries,
        map,
        enemy_list,
        player,
        draw_blood_parts=screen,
        dummies={},
    ):
        super().update_life(bullet_list)
        last_pos = self._pos.copy()
        self.move()

        if self.energy:
            for i in range(random.randint(1,3)):
                particle_list.append(
                    classes.Particle(
                        self._pos,
                        pre_defined_angle=True,
                        angle=self._angle + 270,
                        magnitude=self._damage**0.2 - 0.5,
                        screen=screen,
                        type="energy",
                    )
                )

        elif self.rocket:
            for i in range(random.randint(1,5)):
                particle_list.append(
                    classes.Particle(
                        self._pos,
                        pre_defined_angle=True,
                        angle=self._angle + 270,
                        magnitude=self._damage**0.2 - 0.5,
                        screen=screen,
                    )
                )
            colls = list(getcollisionspoint(map.block_vis_rects, self._pos))
            if len(colls) != 0:
                print(colls)
                append_explosions.append([last_pos, expl1])
                self.kill_bullet(add_expl=False)
                return 0


        self.detect_collision()
        self.draw()
        try:
            # angle_coll = map.check_collision(
            #     self._pos, map_boundaries, return_only_collision=True, collision_box=0
            # )

            coll_types, pos = map.checkcollision(self._pos, [0,0], round(self.speed/4)*multiplier2, map_boundaries, ignore_barricades=True, bullet = True)

            if coll_types != {
                "left": False,
                "right": False,
                "top": False,
                "bottom": False,
            }:
                func.list_play(rico_sounds)
                self.kill_bullet()

                if coll_types["left"] or coll_types["right"]:
                    ang = 270 - self._angle
                else:
                    ang = 90 - self._angle


                for i in range(round(self._damage**0.5)):
                    particle_list.append(
                        classes.Particle(
                            pos,
                            magnitude=1,
                            pre_defined_angle=True,
                            angle=ang,
                            screen=screen,
                        )
                    )

        except Exception as e:
            print("exception")
            print(e)

        if self.type == "bullet":

            rot_bullet, rot_bullet_rect = func.rot_center(
                self.im, self._angle, self._pos[0], self._pos[1]
            )

        crystal_pay = False

        if self.team == "hostile":
            if classes.player_hit_detection(
                self._pos, self._last_pos, player, self._damage
            ):
                for i in range(3):
                    particle_list.append(
                        classes.Particle(
                            func.minus(self._pos, camera_pos),
                            type="blood_particle",
                            magnitude=0.5,
                            pre_defined_angle=True,
                            screen=draw_blood_parts,
                            angle=self._angle + random.randint(45, 135),
                        )
                    )
                try:
                    if not self.piercing:
                        self.kill_bullet()
                except:
                    pass

        if dummies != {}:
            for x in dummies:
                if (
                    dummies[x].hit_detection(
                        camera_pos,
                        self._pos,
                        self._last_pos,
                        self._damage,
                        dummies,
                        draw_blood_parts,
                        player,
                    )
                    == True
                ):
                    particle_list.append(
                        classes.Particle(
                            func.minus(self._pos, camera_pos),
                            type="blood_particle",
                            magnitude=0.5,
                            pre_defined_angle=True,
                            screen=draw_blood_parts,
                            angle=self._angle + random.randint(45, 135),
                        )
                    )



                    try:
                        if not self.piercing:
                            self.kill_bullet()
                    except:
                        pass

                    if dummies[x].check_if_alive():
                        return False
                    else:
                        return True

        dead = 0
        for x in enemy_list:
            if (
                x.hit_detection(
                    camera_pos,
                    self._pos,
                    self._last_pos,
                    self._damage,
                    enemy_list,
                    draw_blood_parts,
                    player,
                )
                == True
            ):

                x.knockback(
                    self._damage, math.radians(self._angle), daemon_bullet=self.mp
                )

                for i in range(random.randint(5,10)):
                    particle_list.append(
                        classes.Particle(
                            x.pos,
                            type="flying_blood",
                            pre_defined_angle=True,
                            angle=self._angle + random.randint(75, 115),
                            magnitude=random.uniform(2,3),
                            screen=screen,
                        )
                    )

                try:
                    if x.check_if_alive():
                        dead = False
                        for i in range(3):
                            particle_list.append(
                                classes.Particle(
                                    func.minus(self._pos, camera_pos),
                                    type="blood_particle",
                                    magnitude=0.5,
                                    pre_defined_angle=True,
                                    screen=draw_blood_parts,
                                    angle=self._angle + random.randint(45, 135),
                                )
                            )
                    else:
                        dead += 1

                except:
                    print("")
                try:
                    if not self.piercing:
                        self.kill_bullet()
                except:
                    pass

        if self.type == "bullet":

            x,y = rot_bullet.get_rect().center

            draw_pos = func.draw_pos([self._pos[0] - x, self._pos[1] - y], camera_pos)

            screen.blit(rot_bullet, draw_pos)

        else:
            pygame.draw.circle(screen, [255, 153, 0], draw_pos, 3)
        return dead
