from game_objects.game_object import Game_Object
from game_objects.bullet import Bullet
from values import *
import los
import classes
import func
class Turret(Game_Object):
    def __init__(self,pos,turning_speed,firerate,_range,damage= 1,lifetime = 100):
        super().__init__("turret", pos, False, 0, damage,lifetime=lifetime,texture=turret)
        self._turning_speed = turning_speed
        self._firerate = firerate
        self._turret_tick = firerate
        self._range = _range
        self._lifetime2 =  lifetime
        self._tick = 0
        self._aiming_at = 0

        self.size = turret.get_rect().size[0]/2
        self.target = None

    def get_string(self):
        return super().get_string("TURRET")

    def scan_for_enemies(self,enemy_list, walls):
        lowest = 99999
        closest_enemy = None
        for x in enemy_list:
            if not los.check_los(self._pos, x.get_pos(), walls):
                continue
            dist = los.get_dist_points(self._pos, x.get_pos())
            if dist > self._range:
                continue
            if dist < lowest and dist < self._range:
                lowest = dist
                closest_enemy = x
        return closest_enemy
    def shoot(self,shoot,angle2):
        if shoot == True and self._turret_tick == 0 and abs(angle2-self._angle) < self._turning_speed * 2:
            turret_fire1.stop()
            turret_fire2.stop()
            turret_fire3.stop()

            func.pick_random_from_list(turret_fire).play()
            bullet_list.append(Bullet([self._pos[0], self._pos[1]],self._angle+random.uniform(-10,10),self._damage))

            for x in range(random.randint(4,6)):
                particle_list.append(classes.Particle([self._pos[0], self._pos[1]], pre_defined_angle = True, angle = self._angle+90, magnitude = 2))

            self._lifetime -= 1

            self._turret_tick = self._firerate
        elif self._turret_tick != 0 and shoot == True:
            self._turret_tick -= 1

    def handle_scanning(self,enemy_list,walls,los):
        shoot = False
        aim_at = None
        if self.target == None:
            self.target = self.scan_for_enemies(enemy_list, walls)
        else:
            if los.check_los(self._pos, self.target.get_pos(), walls) and los.get_dist_points(self._pos, self.target.get_pos()) < self._range and self.target.check_if_alive():
                aim_at = self.target.get_pos()
            else:
                self.target = None


        if aim_at != None:
            self._aiming_at = func.get_angle(self._pos,aim_at)
            shoot = True

        elif shoot == False and random.randint(1,300) == 1:
            self._aiming_at = random.randint(0,round(360/self._turning_speed)) * self._turning_speed

        else:
            self._angle = round(self._angle/self._turning_speed)*self._turning_speed
            self._aiming_at = round(self._aiming_at/self._turning_speed)*self._turning_speed
        return shoot,aim_at

    def draw_bead_on(self,aim_at,shoot):
        angle2=0;
        if abs((360-self._aiming_at) - self._angle) > self._turning_speed * 2 -1 :
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
                    self._angle += self._turning_speed
                elif angle2 < self._angle:
                    self._angle -= self._turning_speed
        else:

            angle2 = self._angle

        turret2, turret_rect = func.rot_center(turret,self._angle,self._pos[0],self._pos[1])

        if abs(los.get_angle_diff(360 - (func.get_angle(self._pos,player_pos)), self._angle)) < 20 or los.get_dist_points(player_pos, self._pos) < 25:
            shoot = False

        return shoot,angle2, turret2,turret_rect

    def draw(self, screen,camera_pos,turret2,turret_rect):

        dp = func.draw_pos(self._pos,camera_pos)
        screen.blit(turret_leg, [dp[0] - self.size, dp[1] - self.size])
        screen.blit(turret2,func.draw_pos(turret_rect,camera_pos))
        if self._lifetime/self._lifetime2 <= 0.2:
            func.render_cool(huuto,[turret_rect[0]+35-camera_pos[0], turret_rect[1]+35-camera_pos[1]],self._tick,16,True, screen = screen)
            self._tick += 1

    def clean_up(self):
        if self._lifetime<=0:
            super().clean_up(turret_list)



    def tick(self, screen ,camera_pos,enemy_list,tick, walls, player_pos):
        shoot,aim_at = self.handle_scanning(enemy_list, walls, los)
        shoot,angle2,turret2,turret_rect = self.draw_bead_on(aim_at, shoot)
        self.shoot(shoot,angle2)
        self.draw(screen,camera_pos,turret2,turret_rect)
        self.clean_up()
