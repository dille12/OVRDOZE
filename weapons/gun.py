tick_count = 60
import math
import sys
import os.path

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
)
from core.values import *
from game_objects.objects import *
import core.classes as classes

from weapons.weapon import Weapon
from hud_elements.unit_status import UnitStatus
from game_objects.casing import Casing
from utilities.powerWashParticle import powerWashParticle

class Gun(Weapon):
    def __init__(
        self,
        name="weapon",
        price=10,
        clip_s=10,
        fire_r=10,
        spread=10,
        spread_r=10,
        reload_r=10,
        damage=10,
        bullets_at_once=1,
        burst=False,
        burst_fire_rate=3,
        burst_bullets=3,
        shotgun=False,
        spread_per_bullet=1,
        handling=1,
        semi_auto=False,
        bullet_speed=20,
        piercing=1,
        ammo_cap_lvlup=5,
        ammo="9MM",
        image="",
        hostile=False,
        sounds={"fire": weapon_fire_Sounds, "reload": reload},
        view=0.03,
        energy_weapon=False,
        charge_up=False,
        charge_time=10,
        rocket_launcher = False,
        extra_bullet = True,
        ai_fire_rate_mod = 7,
        availableUpgrades = ["Paska", "Kulli", "Muna"],
        activatedUpgrades = [].copy(),
        explosive = False,
        ammo_per_shot = 1,
        rocket_explosion_range = 300,
        bullets_in_clip = -1,
        fragRounds = False,
        powerwasher = False,
        max_fire_r = 0,
        fire_r_time = 0,
        incremental_fire_r = False,
        skip_mags = False,

    ):
        super().__init__(
            name,
            price,
            damage,
            image,
            hostile,
            sounds,
            view,
            kind="guns",
            energy_weapon=energy_weapon,
        )
        self.extra_bullet = extra_bullet
        self._clip_size = clip_s
        if bullets_in_clip == -1:
            self._bullets_in_clip = clip_s + (1 if self.extra_bullet else 0)
        else:
            self._bullets_in_clip = bullets_in_clip
        self._bullet_per_min = fire_r
        self._firerate = tick_count / (fire_r / 60)

        self.ai_fire_rate_mod = ai_fire_rate_mod
        self.owner = None
        self.app = None
        self.activatedUpgrades = activatedUpgrades

        self.skip_mags = skip_mags

        self.max_fire_r = max_fire_r
        self.fire_r_time = fire_r_time
        self.incremental_fire_r = incremental_fire_r
        self.fire_r_time_curr = 0

        self.spread_per_bullet = spread_per_bullet
        self.piercing_bullets = piercing
        self._spread = spread
        self._spread_recovery = spread_r
        self._reload_rate = reload_r
        self._orig_fr = fire_r
        self.semi_auto = semi_auto
        self.semi_auto_click = False
        self._bullets_at_once = bullets_at_once
        self._shotgun = shotgun
        self._ammo_cap_lvlup = ammo_cap_lvlup
        self.bullet_speed = bullet_speed
        self._c_bullet_spread = 0
        self.ammo = ammo
        self.handling = handling
        self.random_reload_tick = random.randint(
            round(self._reload_rate / 4), round(3 * self._reload_rate / 4)
        )
        self.burst = burst
        self.burst_bullets = burst_bullets
        self.burst_fire_rate = burst_fire_rate
        self.burst_tick = 0
        self.current_burst_bullet = 0
        self.rocket_launcher = rocket_launcher
        self.ammo_per_shot = ammo_per_shot
        self.powerwasher = powerwasher
        self.charge_up = charge_up
        self.charge_time = charge_time

        self.availableUpgrades = availableUpgrades


        

        self.jammed = False
        self.explosive = explosive
        self.fired = False
        self.DPS = self.calcDPS()

        self.rocket_explosion_range = rocket_explosion_range

        if charge_up:
            self.charge_tick = GameTick(self.charge_time, oneshot=True)

        self.fragRounds = fragRounds

    def add_to_spread(self, amount):
        self._c_bullet_spread += amount

    def copy(self):
        x = self.name
        return Gun(
            name=self.name,
            price=self.price,
            clip_s=self._clip_size,
            fire_r=self._bullet_per_min,
            spread=self._spread,
            spread_r=self._spread_recovery,
            spread_per_bullet=self.spread_per_bullet,
            reload_r=self._reload_rate,
            damage=self._damage,
            bullets_at_once=self._bullets_at_once,
            sounds=self.soundBank,
            bullet_speed=self.bullet_speed,
            shotgun=self._shotgun,
            ammo_cap_lvlup=self._ammo_cap_lvlup,
            image=self.image_file_name,
            semi_auto=self.semi_auto,
            ammo=self.ammo,
            piercing=self.piercing_bullets,
            view=self.view,
            hostile=self.hostile,
            handling=self.handling,
            burst=self.burst,
            burst_bullets=self.burst_bullets,
            burst_fire_rate=self.burst_fire_rate,
            energy_weapon=self.energy_weapon,
            charge_up=self.charge_up,
            charge_time=self.charge_time,
            rocket_launcher=self.rocket_launcher,
            extra_bullet=self.extra_bullet,
            ai_fire_rate_mod = self.ai_fire_rate_mod,
            availableUpgrades = self.availableUpgrades,
            activatedUpgrades = self.activatedUpgrades.copy(),
            explosive = self.explosive,
            ammo_per_shot = self.ammo_per_shot,
            rocket_explosion_range = self.rocket_explosion_range,
            bullets_in_clip = self._bullets_in_clip,
            fragRounds = self.fragRounds,
            powerwasher = self.powerwasher,
            max_fire_r = self.max_fire_r,
            fire_r_time = self.fire_r_time,
            incremental_fire_r = self.incremental_fire_r,
            skip_mags = self.skip_mags,
        )

    def get_semi_auto(self):
        return self.semi_auto
    
    def calcDPS(self):

        damage = self._damage
        if self.rocket_launcher:
            damage = 200

        shots_per_second = self._bullet_per_min/60
        if self.semi_auto:
            shots_per_second = 5

        if self._shotgun:
            shots_per_second *= self._bullets_at_once

        magazineEmptyTime = self._clip_size/shots_per_second
        reloadTime = self._reload_rate/60

        damage_per_second_firing = damage * shots_per_second * (min(self.piercing_bullets, 2)**0.2)

        average_dps = damage_per_second_firing * magazineEmptyTime/(magazineEmptyTime + reloadTime)
        average_dps = average_dps**0.5
        return average_dps

    def visual_and_audio_fire(self, bul_pos, angle, screen):

        super().use()

        

        bul_pos = [bul_pos[0] * multiplier2, bul_pos[1] * multiplier2]

        for x in range(self._bullets_at_once):
            if self.energy_weapon:
                for x in range(random.randint(14, 23)):
                    particle_list.append(
                        classes.Particle(
                            bul_pos,
                            pre_defined_angle=True,
                            angle=angle + 90,
                            magnitude=self._damage**0.2 - 0.5,
                            screen=screen,
                            type="energy",
                        )
                    )

            else:
                for x in range(random.randint(8, 16)):
                    particle_list.append(
                        classes.Particle(
                            bul_pos,
                            pre_defined_angle=True,
                            angle=angle + 90,
                            magnitude=self._damage**0.1 - 0.5,
                            screen=screen,
                        )
                    )


    def powerwasherFire(self, app, bullet_pos, angle, screen, player_actor, velocity):
        super().use()
        particle_list.append(powerWashParticle(app, bullet_pos, angle, velocity))


    def fire(self, app, bullet_pos, angle, screen, player_actor, ai = False, distanceMP = None):

        if not ai and not self.powerwasher:
            index = (0.9 + 0.1*player_actor.sanity/100)**0.1

            if self.jammed:
                return
            if random.uniform(0, 1) > index and not self.energy_weapon:
                self.jammed = True
                UnitStatus(screen, player_actor, "GUN JAMMED!", [255,0,0])
                return
            
            app.storyTeller.ammoUpdate(self.ammo)


        radian_angle = math.radians(angle) - 0.16184 + math.pi / 2

        c = 198.59507 * 0.36919315403 / 1.875  * multiplier2



        x_offset = math.sin(radian_angle) * c
        y_offset = math.cos(radian_angle) * c
        bul_pos = [bullet_pos[0] + x_offset, bullet_pos[1] + y_offset]
        casing_pos = [bullet_pos[0] + x_offset*0.8, bullet_pos[1] + y_offset*0.8]

        bul_pos_apparent = [bul_pos[0] / multiplier2, bul_pos[1] / multiplier2]
        if not self.powerwasher:
            app.casings.append(Casing(app, screen, casing_pos, angle))

        if not self.powerwasher:
            self.visual_and_audio_fire(bul_pos_apparent, angle, screen)

        if self.owner:
            self.app.send_data(f"self.game_ref.multiplayer_actors['{self.owner.name}'].equipped_gun.visual_and_audio_fire({bul_pos_apparent}, {angle}, self.game_ref.screen_copy)")
        multiplier = 2 if self.get_double_damage_time() > 0 else 1
        spread_cumulative = 0

        bulletsAtOnce = self._bullets_at_once if self._shotgun else 1

        self.fired = True

        for x in range(bulletsAtOnce):

            if self._bullets_in_clip > 0:

                shooting_angle = angle + random.uniform(-self._spread - self._c_bullet_spread, self._spread + self._c_bullet_spread)

                if self.powerwasher:
                    self.powerwasherFire(app, bul_pos_apparent, shooting_angle, screen, player_actor, distanceMP/15)
                else:
                    bullet_temp = Bullet.Bullet(
                        bul_pos_apparent,
                        shooting_angle,
                        self._damage * multiplier,
                        hostile=self.hostile,
                        speed=self.bullet_speed,
                        piercing=self.piercing_bullets,
                        energy=self.energy_weapon,
                        rocket=self.rocket_launcher,
                        rocket_explosion_range = self.rocket_explosion_range,
                        owner=self,
                        explosive = self.explosive,
                        fragRounds = self.fragRounds,
                        firedFrom=self.name
                    )

                    bullet_list.append(bullet_temp)  # BULLET

                    if self.owner:
                        self.app.send_data(f"bullet_list.append(Bullet({bul_pos_apparent}, {shooting_angle}, {self._damage * multiplier}, speed={self.bullet_speed}, piercing={self.piercing_bullets}, energy={self.energy_weapon}, rocket={self.rocket_launcher}, daemon_bullet=True, id={bullet_temp.id}))")

                if self._shotgun == False:
                    self._bullets_in_clip -= self.ammo_per_shot

            spread_cumulative += self.spread_per_bullet

        self._c_bullet_spread += spread_cumulative

        if self._shotgun == True:
            self._bullets_in_clip -= self.ammo_per_shot

        if self.burst:
            self.burst_tick = timedelta.tick(self.burst_fire_rate)
            self.current_burst_bullet -= 1

        self.add_weapon_fire_tick(self._firerate)

    def spread_recoverial(self):
        self._c_bullet_spread *= timedelta.exp(self._spread_recovery)

    def check_for_Fire(self, click, player_inventory):

        if self.skip_mags:
            if self._bullets_in_clip > 1:
                player_inventory.append_to_inv(player_inventory.items[self.ammo], self._bullets_in_clip - 1)
                self._bullets_in_clip = 1

        if self.semi_auto:
            if click and self.semi_auto_click == False and self._bullets_in_clip > 0:
                self.semi_auto_click = True
                return True
            elif click == False:
                self.semi_auto_click = False
            return False

        elif self.burst:

            return bool(
                click
                and self.burst_tick <= 0
                and self.current_burst_bullet == 0
                and self._bullets_in_clip > 0
            )

        return click == True and self._bullets_in_clip > 0

    def get_Ammo(self):
        return self._bullets_in_clip

    def reload(self, player_inventory, player_actor, screen):
        self.random_reload_tick = random.randint(
            round(self._reload_rate / 4), round(3 * self._reload_rate / 4)
        )

        if self.ammo == "INF":
            availabe_ammo = 1000
        else:
            availabe_ammo = player_inventory.get_amount_of_type(self.ammo)

        if self._bullets_in_clip == 0:

            ammo_to_reload = self._clip_size
        else:
            ammo_to_reload = self._clip_size - round(self._bullets_in_clip) + (1 if self.extra_bullet else 0)

        if availabe_ammo == 0:
            return

        to_reload = ammo_to_reload if ammo_to_reload < availabe_ammo else availabe_ammo
        self.reload_sound.play()
        self.set_reload_tick(self.get_reload_rate())

        if to_reload == availabe_ammo and to_reload != 0:
            UnitStatus(screen, player_actor, "LAST MAG!", [255,255,0])

        self._bullets_in_clip += to_reload
        if self.ammo != "INF":
            player_inventory.remove_amount(self.ammo, to_reload)

    def get_firerate(self):
        return self._firerate

    def get_clip_size(self):
        return self._clip_size

    def upgrade_firerate(self):
        if self._shotgun == True:
            self._bullets_at_once += 1
        else:
            self._bullet_per_min += 50
            self._firerate = 60 / (self._bullet_per_min / 60)

    def upgrade_clip_size(self):
        self._clip_size += self._ammo_cap_lvlup
        if self._shotgun == False:
            self._clip_size += self._bullets_at_once - 1

    def set_hostile(self):
        super().set_hostile()

    def get_image(self):
        super().get_image()

    def get_reload_rate(self):
        return super().get_reload_rate()

    def set_reload_tick(self, val):
        super().set_reload_tick(val)

    def reload_tick(self):
        return super().get_reload_tick()

    def upgrade_damage(self):
        super().upgrade_damage()

    def get_double_damage_time(self):
        return super().get_double_damage_time()

    def double_damage(self, state):
        super().double_damage(state)

    def weapon_tick(self):
        super().weapon_tick()

    def weapon_fire_Tick(self):
        return super().weapon_fire_Tick()
