from game_objects.game_object import Game_Object
from values import *
import func
import classes
from anim_list import *
from level import getcollisionspoint
import los


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
        rocket=False,
        daemon_bullet=False,
        id=-1,
        owner=None,
    ):
        self.id = id
        self.owner = owner

        pos = func.mult(pos, multiplier2)

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

        self.daemon_bullet = daemon_bullet

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
        self.actors_hit = []

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

        self.kill_id()

        if self.rocket and add_expl and not self.added_explosion:
            append_explosions.append([self._pos, expl1])
            self.added_explosion = True
            #explosions.append(Explosion(self._pos, expl1))
        if self in bullet_list:
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
                        magnitude=self._damage**0.2 - 1,
                        screen=screen,
                    )
                )
            if not self.daemon_bullet:
                colls = list(getcollisionspoint(map.block_vis_rects, self._pos))
                if len(colls) != 0:
                    append_explosions.append([last_pos, expl1])
                    self.kill_bullet(add_expl=False)
                    return 0


        self.detect_collision()
        self.draw()

        for i in getcollisionspoint(map.block_vis_rects, self._pos):
            self.kill_bullet()
            return

        try:

            coll_types, pos = map.checkcollision(self._pos, [0,0], round(self.speed/4)*multiplier2, map_boundaries, ignore_barricades=True, bullet = True)

            if coll_types != {
                "left": False,
                "right": False,
                "top": False,
                "bottom": False,
            }:
                func.list_play(rico_sounds)


                if coll_types["left"] or coll_types["right"]:
                    ang = 270 - self._angle
                else:
                    ang = 90 - self._angle

                if abs(los.get_angle_diff(ang + 90, self._angle)) > 100:
                    self._angle = ang - 90
                    self._angle_radians = math.radians(self._angle) + math.pi / 2
                    self.speed *= 0.9
                    self.move()
                else:
                    self.kill_bullet()
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
            print("exception at bullet rico")
            print(e)

        if self.type == "bullet":

            rot_bullet, rot_bullet_rect = func.rot_center(
                self.im, self._angle, self._pos[0], self._pos[1]
            )

        crystal_pay = False

        if self.type == "bullet":

            x,y = rot_bullet.get_rect().center

            draw_pos = func.draw_pos([self._pos[0] - x, self._pos[1] - y], camera_pos)

            screen.blit(rot_bullet, draw_pos)

        else:
            pygame.draw.circle(screen, [255, 153, 0], draw_pos, 3)

        if self.daemon_bullet:
            return 0

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
            for x in (x for x in dummies if x not in self.actors_hit):
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

                    if self.owner:
                        if not self.piercing:
                            self.owner.app.send_data(f"ID_container.nwobjects[{self.id}].kill_bullet()")
                        self.owner.app.send_data(f"self.game_ref.player_actor_ref.force_player_damage({self._damage})")

                    try:
                        if not self.piercing:
                            self.kill_bullet()
                    except:
                        pass
                    self.actors_hit.append(x)

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
                if x.class_type == "SOLDIER":
                    if x.state != "attacking":
                        rad = 2*math.pi - math.radians(self._angle + 180)
                        x.aim_at = [math.cos(rad) * 100 + x.pos[0], math.sin(rad) * 100 + x.pos[1]]
                        x.random_aim_tick = 120


                x.knockback(
                    self._damage, math.radians(self._angle), daemon_bullet=self.mp
                )

                for i in range(min([round(self._damage/3), 50])):
                    particle_list.append(
                        classes.Particle(
                            [x.pos[0] + random.randint(-10,10), x.pos[1] + random.randint(-10,10)],
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



        return dead
