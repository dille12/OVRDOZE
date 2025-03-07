from core.values import *
import weapons.melee as Melee
import weapons.gun as W
from weapons.area import Grenade
from weapons.area import Explosion

guns = {
    "M1911": W.Gun(
        name="M1911",
        price=135,
        clip_s=8,
        fire_r=620,
        spread=7,
        spread_r=0.94,
        reload_r=45,
        damage=34,
        semi_auto=True,
        bullets_at_once=1,
        shotgun=False,
        ammo_cap_lvlup=1,
        image="m1911.png",
        ammo="45 ACP",
        view=0.005,
        handling=0.7,
        availableUpgrades = ["Full Auto", "Add Pierce", "Extended Mag"],
    ),

    "FN57-S": W.Gun(
        name="FN57-S",
        price=1000,
        clip_s=12,
        fire_r=500,
        spread=0.5,
        spread_r=0.9,
        reload_r=30,
        damage=45,
        bullet_speed=35,
        semi_auto=True,
        bullets_at_once=1,
        sounds=pistol_sounds_silenced,
        shotgun=False,
        ammo_cap_lvlup=1,
        image="fn.png",
        ammo="9MM",
        view=0.02,
        handling=0.9,
        burst_fire_rate = 2,
        availableUpgrades = ["3 Round Burst", "Add Pierce", "Extended Mag"],
    ),

    "DESERTEAGLE" : W.Gun(
        name="DESERTEAGLE",
        price=950,
        clip_s=7,
        fire_r=2000,
        spread=0.5,
        spread_r=0.955,
        spread_per_bullet = 20,
        reload_r=50,
        damage=75,
        bullet_speed=45,
        semi_auto=True,
        bullets_at_once=1,
        sounds=sniper_rifle_sounds,
        shotgun=False,
        ammo_cap_lvlup=1,
        image="desert.png",
        ammo="50 CAL",
        view=0.022,
        handling=0.35,
        piercing=3,
        ai_fire_rate_mod = 15,
        availableUpgrades = ["Quickdraw Mag", "Recoil Recovery", "Armor Annihilating"],

        
    ),

    "AR-15": W.Gun(
        name="AR-15",
        price=2900,
        clip_s=35,
        fire_r=500,
        spread=1,
        spread_r=0.93,
        bullet_speed=35,
        reload_r=60,
        damage=29,
        bullets_at_once=1,
        shotgun=False,
        sounds=assault_rifle_sounds,
        ammo_cap_lvlup=1,
        image="m16.png",
        ammo="7.62x39MM",
        piercing=2,
        view=0.032,
        handling=0.25,
        burst=True,
        burst_bullets=3,
        burst_fire_rate=2,
        availableUpgrades = ["Add Pierce", "Extended Mag", "Improved Firerate"],
    ),
    "AK47": W.Gun(
        name="AK47",
        price=2700,
        clip_s=30,
        fire_r=520,
        spread=3,
        spread_r=0.94,
        bullet_speed=40,
        reload_r=60,
        damage=34,
        bullets_at_once=1,
        shotgun=False,
        sounds=assault_rifle_sounds,
        ammo_cap_lvlup=1,
        image="ak.png",
        ammo="7.62x39MM",
        piercing=3,
        view=0.03,
        handling=0.35,
        availableUpgrades = ["Quickdraw Mag", "Fragmentation Rounds", "Improved Firerate"],
    ),
    "SCAR18": W.Gun(
        name="SCAR18",
        price=1700,
        clip_s=20,
        fire_r=240,
        spread=1,
        spread_r=0.945,
        bullet_speed=30,
        spread_per_bullet=2,
        reload_r=45,
        damage=45,
        bullets_at_once=1,
        shotgun=False,
        sounds=assault_rifle_sounds2,
        ammo_cap_lvlup=1,
        image="scar.png",
        ammo="50 CAL",
        piercing=4,
        view=0.035,
        handling=0.45,
        availableUpgrades = ["Quickdraw Mag", "Double Damage", "Double Firerate"],
    ),
    "M134-MINIGUN": W.Gun(
        name="M134-MINIGUN",
        price=6500,
        clip_s=999,
        fire_r=2300,
        spread=2,
        spread_r=0.96,
        bullet_speed=45,
        reload_r=200,
        damage=34,
        bullets_at_once=1,
        shotgun=False,
        sounds=assault_rifle_sounds,
        ammo_cap_lvlup=1,
        image="m134.png",
        ammo="5.56x45MM NATO",
        piercing=2,
        view=0.03,
        handling=0.05,
        availableUpgrades = ["Featherweight", "Double Damage", "Double Firerate"],
    ),
    "RPG-7": W.Gun(
        name="RPG-7",
        price=2300,
        clip_s=1,
        fire_r=2300,
        spread=2,
        spread_r=0.96,
        bullet_speed=25,
        reload_r=75,
        damage=1000,
        bullets_at_once=3,
        shotgun=False,
        sounds=rocket_launcher_sounds,
        ammo_cap_lvlup=1,
        image="rpg.png",
        ammo="HE Grenade",
        view=0.03,
        handling=0.2,
        rocket_launcher = True,
        semi_auto = True,
        extra_bullet = False,
        availableUpgrades = ["Quickdraw Mag", "Tri-Shot", "Bigger Blasts"],
    ),

    "USAS-15": W.Gun(
        name="USAS-15",
        price=2400,
        clip_s=8,
        fire_r=300,
        spread=8,
        spread_per_bullet=3,
        spread_r=0.94,
        reload_r=70,
        damage=15,
        bullet_speed=20,
        bullets_at_once=7,
        shotgun=True,
        semi_auto=False,
        sounds=shotgun_sounds,
        ammo_cap_lvlup=2,
        image="usas.png",
        ammo="12 GAUGE",
        view=0.01,
        handling=0.2,
        availableUpgrades = ["Explosive Ammo", "Improved Firerate", "Extended Mag"],
    ),

    "NRG-SHLL": W.Gun(
        name="NRG-SHLL",
        price=7000,
        clip_s=13,
        fire_r=180,
        spread=8,
        spread_per_bullet=1.5,
        spread_r=0.94,
        reload_r=70,
        damage=25,
        bullet_speed=15,
        bullets_at_once=10,
        shotgun=True,
        semi_auto=False,
        sounds=nrg_sounds,
        ammo_cap_lvlup=2,
        image="shll.png",
        ammo="Energy Cell",
        view=0.01,
        handling=0.2,
        piercing=10,
        energy_weapon=True,
        charge_up=True,
        charge_time=25,
        availableUpgrades = ["Energy Efficiency", "Quickdraw Mag", "Improved Firerate"],
    ),

    "SPAS-12": W.Gun(
        name="SPAS-12",
        price=1300,
        clip_s=6,
        fire_r=120,
        spread=5,
        spread_per_bullet=2,
        spread_r=0.93,
        reload_r=60,
        damage=22,
        bullet_speed=15,
        bullets_at_once=8,
        shotgun=True,
        semi_auto=True,
        sounds=shotgun_sounds,
        ammo_cap_lvlup=2,
        image="spas12.png",
        ammo="12 GAUGE",
        view=0.01,
        handling=0.2,
        availableUpgrades = ["Double Damage", "Double Pellets", "Add Pierce"],

    ),
    "P90": W.Gun(
        name="P90",
        price=900,
        clip_s=50,
        fire_r=950,
        spread=7,
        spread_r=0.94,
        reload_r=60,
        damage=21,
        bullets_at_once=1,
        shotgun=False,
        sounds=smg_sounds,
        ammo_cap_lvlup=2,
        image="p90.png",
        ammo="9MM",
        view=0.02,
        handling=0.5,
        availableUpgrades = ["Recoil Recovery", "Double Firerate", "Fragmentation Rounds"],
    ),
    "MP5": W.Gun(
        name="MP5",
        price=750,
        clip_s=40,
        fire_r=900,
        spread=2,
        spread_r=0.93,
        spread_per_bullet=3.4,
        reload_r=44,
        damage=24,
        bullets_at_once=1,
        shotgun=False,
        sounds=smg_sounds,
        ammo_cap_lvlup=2,
        image="mp5.png",
        ammo="45 ACP",
        view=0.02,
        handling=0.5,
        burst=True,
        burst_bullets=4,
        burst_fire_rate=1,
        availableUpgrades = ["Recoil Recovery", "Double Firerate", "Explosive Ammo"],
    ),
    "GLOCK": W.Gun(
        name="GLOCK",
        price=350,
        clip_s=20,
        fire_r=350,
        spread=3,
        spread_r=0.92,
        reload_r=30,
        damage=27,
        semi_auto=False,
        bullets_at_once=1,
        shotgun=False,
        ammo_cap_lvlup=1,
        image="glock.png",
        ammo="45 ACP",
        view=0.017,
        handling=0.9,
        burst=True,
        burst_bullets=3,
        burst_fire_rate=3,
        availableUpgrades = ["Double Firerate", "Extended Mag", "Explosive Ammo"],
    ),
    "AWP": W.Gun(
        name="AWP",
        price=1500,
        clip_s=10,
        fire_r=50,
        spread=1,
        spread_r=0.965,
        spread_per_bullet=25,
        reload_r=80,
        damage=200,
        bullets_at_once=3,
        sounds=sniper_rifle_sounds,
        bullet_speed=55,
        shotgun=False,
        ammo_cap_lvlup=1,
        image="awp.png",
        ammo="50 CAL",
        piercing=10,
        view=0.045,
        handling=0.15,
        semi_auto=True,
        ai_fire_rate_mod = 40,
        availableUpgrades = ["Recoil Recovery", "Extended Mag", "Tri-Shot"],
    ),
    "NRG-LMG.Mark1": W.Gun(
        name="NRG-LMG.Mark1",
        price=6700,
        clip_s=67,
        fire_r=600,
        spread=1,
        spread_r=0.935,
        spread_per_bullet=2.2,
        reload_r=80,
        damage=75,
        bullets_at_once=3,
        sounds=nrg_sounds,
        bullet_speed=45,
        shotgun=False,
        ammo_cap_lvlup=1,
        image="nrg.png",
        ammo="Energy Cell",
        piercing=10,
        view=0.035,
        handling=0.25,
        semi_auto=False,
        energy_weapon=True,
        charge_up=True,
        charge_time=30,
        availableUpgrades = ["Energy Efficiency", "Improved Firerate", "Tri-Shot"],
    ),
    "R13-TYPE2" : W.Gun(
        name = "R13-TYPE2",
        price=10000,
        clip_s=45,
        fire_r=300,
        max_fire_r=1400,
        fire_r_time=300,
        incremental_fire_r = True,
        spread=3,
        spread_r=0.935,
        spread_per_bullet=2.5,
        reload_r=180,
        damage=30,
        bullets_at_once=3,
        sounds=nrg_sounds,
        bullet_speed=45,
        shotgun=False,
        ammo_cap_lvlup=1,
        image="r13.png",
        ammo="Energy Cell",
        piercing=3,
        view=0.035,
        handling=0.35,
        semi_auto=False,
        energy_weapon=True,
        charge_up=True,
        charge_time=20,
        availableUpgrades = ["Energy Efficiency", "Improved Firerate", "Tri-Shot"],
        ammo_per_shot = 0.25,
        skip_mags=False,
    ),
    
}
melees = {}
grenades = {}

powerWasher = W.Gun("POWERWASHER", image = "powerwasher.png", powerwasher = True, handling=0.9, view=0.017, spread_r = 0.9, clip_s=999, fire_r=2000, spread=3, ammo="INF", bullets_at_once = 1, charge_up=True, charge_time=30,
                    sounds = washer_sounds)

__weapons_map = {"gun": guns, "melee": melees, "grenade": grenades, "powerwasher" : {"POWERWASHER" : powerWasher}}

upgradeMap = {
    "Full Auto" : {"Desc" : "Turns the weapon to fully automatic.", "stat": "semi_auto", "set" : False},
    "Extended Mag" : {"Desc" : "Adds 10 bullets to the magazine.", "stat": "_clip_size", "addval" : 10},
    "Add Pierce" : {"Desc" : "Bullets pierce one enemy more.", "stat": "piercing_bullets", "addval" : 1},
    "3 Round Burst" : {"Desc" : "The weapon shoots 3 round bursts.", "stat": "burst", "set" : True},
    "Explosive Ammo" : {"Desc" : "Bullets explode after expiring.", "stat": "explosive", "set" : True},
    "Improved Firerate" : {"Desc" : "Weapon fires more rounds per minute.", "stat": "_bullet_per_min", "addval" : 200},
    "Quickdraw Mag" : {"Desc" : "Weapon is reloaded twice as fast.", "stat" : "_reload_rate", "multval" : 0.5},
    "Double Firerate" : {"Desc" : "Weapon fires twice as fast.", "stat" : "_bullet_per_min", "multval" : 2},
    "Recoil Recovery" : {"Desc" : "Recoil recovers faster.", "stat" : "_spread_recovery", "addval" : -0.03},
    "Tri-Shot" : {"Desc" : "Shoots three devastiting bullets at once.", "stat" : "_shotgun", "set" : True},
    "Double Pellets" : {"Desc" : "Shoots double shotgun pellets.", "stat" : "_bullets_at_once", "multval" : 2},
    "Double Damage" : {"Desc" : "Bullets do double damage.", "stat" : "_damage", "multval" : 2},
    "Infinite Ammo" : {"Desc" : "No need to pick any ammo anymore.", "stat" : "ammo", "set" : "INF"},
    "Energy Efficiency" : {"Desc" : "Energy depletes half as fast.", "stat" : "ammo_per_shot", "multval" : 0.5},
    "Armor Annihilating" : {"Desc" : "The bullet wont stop for anything.", "stat" : "piercing_bullets", "set" : 50},
    "Bigger Blasts" : {"Desc" : "Yeah be careful with this one.", "stat" : "rocket_explosion_range", "set" : 600},
    "Fragmentation Rounds" : {"Desc" : "Bullets fragment into three bullets after impact.", "stat" : "fragRounds", "set" : True},
    "Featherweight" : {"Desc" : "Handling of the weapon becomes incredibly easy.", "stat" : "handling", "set" : 0.99},


}

statMap = {
    "semi_auto" : "Semi automatic",
    "_clip_size" : "Clip size",
    "piercing_bullets" : "Bullet piercing",
    "burst" : "Burst fire",
    "explosive" : "Explosive ammo",
    "_bullet_per_min" : "Fire rate",
    "_reload_rate" : "Reload rate",
    "_spread_recovery" : "Spread recovery",
    "rocket_explosion_range" : "Explosion range",
    "ammo_per_shot" : "Ammo cost per shot",
    "Tri-Shot" : "_shotgun",
    "_bullets_at_once" : "Bullets per shot",
    "_damage" : "Damage per shot",
    "ammo" : "Ammo type",
    "fragRounds" : "Frag rounds",
    "handling" : "Handling",
    "_shotgun" : "Tri-Shot",
}
