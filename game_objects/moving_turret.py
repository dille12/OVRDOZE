from game_objects.game_object import Game_Object
from game_objects.bullet import Bullet
from core.values import *
import core.los as los
import core.classes as classes
import core.func as func
import math
import numpy as np



class MovingTurret(Game_Object):
    def __init__(
        self,
        pos,
        turning_speed,
        firerate,
        _range,
        damage=1,
        lifetime=100,
        NAV_MESH=[],
        walls=[],
        map=None,
        app = None,
    ):
        super().__init__(
            "turret", pos, False, 0, damage, lifetime=lifetime, texture=turret
        )
        self._turning_speed = turning_speed
        self._firerate = firerate
        self._turret_tick = firerate
        self._range = _range
        self._lifetime2 = lifetime
        self._tick = 0
        self._aiming_at = 0
        self.base_angle = 0
        self.moving_speed = 4 * multiplier2
        self.turning_speed = 3
        self.route_tick = 0
        self.stationary = 0

        self.acceleration = 0.5

        self.target_move_pos = pos

        # self.navmesh_ref = NAV_MESH.copy()
        # self.wall_ref = walls
        self.map = map

        self.route = []

        self.velocity = 0
        self.angle_rad = 0

        self.size = turret.get_rect().size[0] / 2
        self.target = None

        self.app = app

        self.back_up_ticks = 0
        self.back_up_dir = 1
        self.back_up_random_dir = 0
        self.force_teleport = 0
    def get_string(self):
        return super().get_string("MOVINGTURRET")

    def scan_for_enemies(self, enemy_list, walls):
        lowest = 99999
        closest_enemy = None
        for x in enemy_list:
            if not los.check_los_jit(np.array(self._pos), np.array(x.pos), self.map.numpy_array_wall_los):

                continue
            dist = los.get_dist_points(self._pos, x.get_pos())
            if dist > self._range:
                continue
            if dist < lowest and dist < self._range:
                lowest = dist
                closest_enemy = x
        return closest_enemy

    def shoot(self, shoot, angle2):
        if (
            shoot == True
            and self._turret_tick <= 0
            and abs(angle2 - self._angle) < self._turning_speed * 4
        ):
            mov_fire.stop()

            mov_fire.play()
            bullet_list.append(
                Bullet(
                    [self._pos[0], self._pos[1]],
                    self._angle + random.uniform(-10, 10),
                    self._damage,
                    hostile=False,
                    speed=25,
                )
            )

            for x in range(random.randint(4, 6)):
                particle_list.append(
                    classes.Particle(
                        [self._pos[0], self._pos[1]],
                        pre_defined_angle=True,
                        angle=self._angle + 90,
                        magnitude=2,
                    )
                )
            if self._lifetime > 0:
                self._lifetime -= 1

            self._turret_tick = self._firerate
        elif self._turret_tick > 0 and shoot == True:
            self._turret_tick -= timedelta.mod(1)

    def handle_scanning(self, enemy_list, walls, los):
        shoot = False
        aim_at = None
        if self.target == None:
            self.target = self.scan_for_enemies(enemy_list, walls)
        else:
            if (
                los.check_los_jit(np.array(self._pos), np.array(self.target.get_pos()), self.map.numpy_array_wall_los)
                and los.get_dist_points(self._pos, self.target.get_pos()) < self._range
                and self.target.check_if_alive()
            ):
                aim_at = self.target.get_pos()
            else:
                self.target = None

        if aim_at != None:
            self._aiming_at = func.get_angle(self._pos, aim_at)
            shoot = True

        elif shoot == False and random.randint(1, 300) == 1:
            self._aiming_at = (
                random.randint(0, round(360 / self._turning_speed))
                * self._turning_speed
            )

        else:
            self._angle = round(self._angle / self._turning_speed) * self._turning_speed
            self._aiming_at = (
                round(self._aiming_at / self._turning_speed) * self._turning_speed
            )
        return shoot, aim_at

    def draw_bead_on(self, aim_at, shoot):
        angle2 = 0
        if abs((360 - self._aiming_at) - self._angle) > self._turning_speed * 2 - 1:
            angle2 = 360 - self._aiming_at
            while angle2 >= 360:
                angle2 -= 360
            while angle2 < 0:
                angle2 += 360

            if angle2 - self._angle > 180:
                angle2 -= 360

            if abs(angle2 - self._angle) < self._turning_speed:
                self._angle = angle2
            else:
                if angle2 > self._angle:
                    self._angle += timedelta.mod(self._turning_speed)
                elif angle2 < self._angle:
                    self._angle -= timedelta.mod(self._turning_speed)
        else:

            angle2 = self._angle

        turret2, turret_rect = func.rot_center(
            mov_turret_gun, self._angle - 90, self._pos[0], self._pos[1]
        )

        if (
            abs(
                los.get_angle_diff(
                    360 - (func.get_angle(self._pos, player_pos)), self._angle
                )
            )
            < 20
            or los.get_dist_points(player_pos, self._pos) < 25
        ):
            shoot = False

        return shoot, angle2, turret2, turret_rect

    def draw(self, screen, camera_pos, turret2, turret_rect):

        dp = func.draw_pos(self._pos, camera_pos)

        turret_base, turret_base_rect = func.rot_center(
            mov_turret_base, self.base_angle - 90, self._pos[0], self._pos[1]
        )

        screen.blit(
            turret_base, func.draw_pos(turret_base_rect, camera_pos)
        )  # func.minus_list, [self.size, self.size])
        screen.blit(turret2, func.draw_pos(turret_rect, camera_pos))
        if self._lifetime / self._lifetime2 <= 0.2:
            func.render_cool(
                huuto,
                [
                    turret_rect[0] + 35 - camera_pos[0],
                    turret_rect[1] + 35 - camera_pos[1],
                ],
                self._tick,
                16,
                True,
                screen=screen,
            )
            self._tick += 1

        # if self._pos != self.target_move_pos:
        #     last_pos = self._pos
        #     for tar in self.route:
        #         pygame.draw.line(screen, [255,255,255], func.minus(last_pos,camera_pos, op="-"), func.minus(tar,camera_pos, op="-"))
        #         last_pos = tar
        #     pygame.draw.line(screen, [255,255,255], func.minus(last_pos,camera_pos, op="-"), func.minus(player_pos,camera_pos, op="-"))
        # pygame.draw.circle(screen, [255,0,0], func.minus(self.target_move_pos,camera_pos, op="-"), 10)

    def clean_up(self):
        if self._lifetime == 0:
            super().clean_up(turret_bro)

    def get_route_to_target(self, target):
        if self.route_tick == 0:
            self.route_tick = 60
            self.route, a = func.calc_route(
                self._pos, target, self.navmesh_ref, [self.map.numpy_array_wall_los, self.map.numpy_array_wall_no_los], quick=False
            )
        lpos = 0
        r2 = []
        for x in self.route:

            if lpos:
                r2.append([(x[0] + lpos[0]) / 2, (x[1] + lpos[1]) / 2])
            r2.append(x)
            lpos = x

        self.route = r2



    def move(self, player_pos):

        if self.force_teleport > 0:
            self.force_teleport -= 0.01

        if self.route_tick != 0:
            self.route_tick -= 1
        last_pos = self._pos.copy()

        if self.back_up_ticks > 0:
            self.velocity = -self.back_up_ticks / 20 * self.back_up_dir


            collision_types, coll_pos = self.map.checkcollision(
                self._pos,
                [
                    math.cos(self.angle_rad) * self.moving_speed,
                    self._pos[1] - math.sin(self.angle_rad) * self.moving_speed,
                ],
                self.size,
                self.map.size_converted,
                ignore_barricades=True,
            )

            self._pos = coll_pos

            self.mov_angle = 180 - math.degrees(
                math.atan2(
                    self._pos[1] - self.target_move_pos[1],
                    self._pos[0] - self.target_move_pos[0],
                )
            ) + self.back_up_random_dir

            if self.mov_angle != self.base_angle:
                angle_diff = los.get_angle_diff(self.mov_angle, self.base_angle)
                if abs(angle_diff) <= self.turning_speed:
                    self.base_angle = self.mov_angle
                else:

                    self.base_angle += timedelta.mod(
                        angle_diff / abs(angle_diff) * self.turning_speed
                    )
            # else:





        else:

            if los.get_dist_points(self._pos, self.target_move_pos) > 20:

                self.moving = True

                self.mov_angle = 180 - math.degrees(
                    math.atan2(
                        self._pos[1] - self.target_move_pos[1],
                        self._pos[0] - self.target_move_pos[0],
                    )
                )

                if self.mov_angle != self.base_angle:
                    angle_diff = los.get_angle_diff(self.mov_angle, self.base_angle)
                    if abs(angle_diff) <= self.turning_speed:
                        self.base_angle = self.mov_angle
                    else:

                        self.base_angle += timedelta.mod(
                            angle_diff / abs(angle_diff) * self.turning_speed
                        )
                # else:

                self.angle_rad = math.radians(self.base_angle)

                angle_diff2 = los.get_angle_diff(self.mov_angle, self.base_angle)

                if (1 - abs(angle_diff2) / 90) < 0:
                    self.diff_from_angle = (1 - abs(angle_diff2) / 90) ** 9
                else:
                    self.diff_from_angle = 1 - abs(angle_diff2) / 90

                self.diff_from_angle *= 1.25
                self.diff_from_angle -= 0.25

                self.velocity += (
                    self.acceleration * self.diff_from_angle * timedelta.timedelta
                )



                # func.minus(self.velocity,[math.cos(self.angle_rad) *self.acceleration * diff_from_angle, - math.sin(self.angle_rad) * self.acceleration * diff_from_angle ]) #-

                if self.velocity > timedelta.mod(self.moving_speed):
                    self.velocity = timedelta.mod(self.moving_speed)

                nextPosEase = timedelta.mod(los.get_dist_points(self._pos, self.target_move_pos) / 10) ** 1.1

                if self.velocity > timedelta.mod(self.moving_speed):
                    self.velocity = timedelta.mod(self.moving_speed)

                if self.velocity > nextPosEase:
                    self.velocity = nextPosEase


                collision_types, coll_pos = self.map.checkcollision(
                    self._pos,
                    [
                        math.cos(self.angle_rad) * self.moving_speed,
                        self._pos[1] - math.sin(self.angle_rad) * self.moving_speed,
                    ],
                    self.size,
                    self.map.size_converted,
                    ignore_barricades=True,
                )

                if self._pos != coll_pos:
                    self.back_up_ticks = 15
                    self.force_teleport += 1
                    self.back_up_random_dir = random.randint(-50, 50)
                    if self.velocity < 0:
                        self.back_up_dir = -1
                    else:
                        self.back_up_dir = 1

                    if self.force_teleport > 10:
                        self._pos = player_pos.copy()
                        coll_pos = self._pos
                        self.force_teleport = 0

                self._pos = coll_pos
                if (
                    los.get_dist_points(self._pos, self.target_move_pos) < 20
                    or los.get_dist_points(self._pos, player_pos) < 50
                ):
                    self.target_move_pos = self._pos

            else:

                # self._pos = func.minus(self._pos, self.velocity)
                #
                # self.velocity = func.mult(self.velocity,0.9)

                if self.route != []:
                    if los.check_los_jit(np.array(player_pos), np.array(self._pos), self.map.numpy_array_wall_los):
                        self.route = []
                        self.target_move_pos = player_pos.copy()
                    else:

                        for route in self.route:

                            self.target_move_pos = route
                            self.route.remove(route)

                            if self._pos != self.target_move_pos:
                                break

                elif los.get_dist_points(self._pos, player_pos) > 120:
                    if los.check_los_jit(np.array(player_pos), np.array(self._pos), self.map.numpy_array_wall_los):
                        self.target_move_pos = player_pos.copy()
                    else:
                        self.get_route_to_target(player_pos.copy())

        self._pos = func.minus(
            self._pos,
            [
                math.cos(self.angle_rad) * self.velocity,
                -math.sin(self.angle_rad) * self.velocity,
            ],
        )

        if self.back_up_ticks > 0:
            self.back_up_ticks -= timedelta.mod(1)

            if not self.back_up_ticks > 0:
                if not los.check_los_jit(np.array(self.target_move_pos), np.array(self._pos), self.map.numpy_array_wall_los):
                    self.route = []
                    self.get_route_to_target(player_pos.copy())


        self.velocity *= timedelta.exp(0.965)


    def move_fix(self, player_pos):

        if self.route_tick != 0:
            self.route_tick -= 1

        if self.route:

            self.target_move_pos = self.route[0]


            self.mov_angle = 180 - math.degrees(
                math.atan2(
                    self._pos[1] - self.target_move_pos[1],
                    self._pos[0] - self.target_move_pos[0],
                )
            )

            if self.mov_angle != self.base_angle:
                angle_diff = los.get_angle_diff(self.mov_angle, self.base_angle)
                if abs(angle_diff) <= self.turning_speed:
                    self.base_angle = self.mov_angle
                else:

                    self.base_angle += timedelta.mod(
                        angle_diff / abs(angle_diff) * self.turning_speed
                    )




    def tick(self, screen, camera_pos, enemy_list, tick, walls, player_pos):
        shoot, aim_at = self.handle_scanning(enemy_list, walls, los)
        self.move(player_pos)


        shoot, angle2, turret2, turret_rect = self.draw_bead_on(aim_at, shoot)
        self.shoot(shoot, angle2)
        self.draw(screen, camera_pos, turret2, turret_rect)
        self.clean_up()

        if self.app.phase == 6:
            lpos = self._pos
            for x in self.route:

                pygame.draw.line(
                    screen,
                    [255,0,0],
                    func.minus(lpos, camera_pos, op="-"),
                    func.minus(x, camera_pos, op="-"),
                )
                lpos = x

            if self.target_move_pos:

                pygame.draw.line(
                    screen,
                    [255,0,0],
                    func.minus(lpos, camera_pos, op="-"),
                    func.minus(self.target_move_pos, camera_pos, op="-"),
                )
