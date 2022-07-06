from game_objects.game_object import Game_Object
from values import *
import func
import classes
class Bullet(Game_Object):
    def __init__(self,
            pos,
            angle,
            damage,
            hostile = True,
            speed = 20,
            piercing = False,
            mp = False
        ):
        super().__init__(
            name="bullet",
            pos=pos,
            hostile=hostile,
            angle=angle,
            damage=damage,
            friendly_fire=False,
            lifetime=30,
            texture=bullet_texture)
        self.mp = mp
        self.speed = speed * random.uniform(0.9,1.1)
        self.im = bullet_length[round(self.speed)]

        


        self.piercing = piercing


    def get_string(self):
       return super().get_string("BULLET")
    def move(self):
        self._last_pos = self._pos.copy()
        self._pos[0] += math.sin(self._angle_radians)*self.speed
        self._pos[1] += math.cos(self._angle_radians)*self.speed
        pass
    def draw(self):
        pass
    def detect_collision(self):
        pass;
    def move_and_draw_Bullet(self,
            screen,
            camera_pos,
            map_boundaries,
            map, enemy_list,
            player,
            draw_blood_parts = screen,
            dummies = {}
        ):
        super().update_life(bullet_list)
        self.move()
        self.detect_collision()
        self.draw()
        try:
            angle_coll = map.check_collision(self._pos, map_boundaries, return_only_collision = True, collision_box = 0)
            if angle_coll != False:
                func.list_play(rico_sounds)
                bullet_list.remove(self)
                for i in range(8):
                    particle_list.append(classes.Particle(angle_coll, magnitude = 1, pre_defined_angle = True, angle = 90-self._angle, screen = screen))

        except Exception as e:
            print("exception")
            print(e)

        rot_bullet, rot_bullet_rect = func.rot_center(self.im,self._angle,self._pos[0],self._pos[1])

        crystal_pay = False



        if self.team == "hostile":
            if classes.player_hit_detection(self._pos, self._last_pos, player, self._damage):
                for i in range(3):
                    particle_list.append(classes.Particle(func.minus(self._pos, camera_pos), type = "blood_particle", magnitude = 0.5, pre_defined_angle = True, screen = draw_blood_parts, angle = self._angle + random.randint(45,135)))
                try:
                    if not self.piercing:
                        bullet_list.remove(self)
                except:
                    pass

        if dummies != {}:
            for x in dummies:
                if dummies[x].hit_detection(camera_pos, self._pos, self._last_pos,self._damage, dummies, draw_blood_parts) == True:
                    particle_list.append(classes.Particle(func.minus(self._pos, camera_pos), type = "blood_particle", magnitude = 0.5, pre_defined_angle = True, screen = draw_blood_parts, angle = self._angle + random.randint(45,135)))
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
            if x.hit_detection(camera_pos, self._pos, self._last_pos,self._damage, enemy_list, draw_blood_parts) == True:

                x.knockback(self._damage, math.radians(self._angle), daemon_bullet = self.mp)

                try:
                    if x.check_if_alive():
                        dead = False
                        for i in range(3):
                            particle_list.append(classes.Particle(func.minus(self._pos, camera_pos), type = "blood_particle", magnitude = 0.5, pre_defined_angle = True, screen = draw_blood_parts, angle = self._angle + random.randint(45,135)))
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

        screen.blit(rot_bullet,func.draw_pos(self._pos,camera_pos))
        return dead
