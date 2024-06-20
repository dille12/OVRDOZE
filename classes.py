import os, sys
import pygame
import math
import random
import time

pygame.init()
import func
from values import *
import level
import los
import pyperclip

width, height = size
import objects
import get_preferences
from dialog import *
import numpy as np
from unit_status import UnitStatus
from utilities.compareGuns import compareGuns
a, draw_los, a, a, ultraviolence, a, a, a, a, a, a, a = get_preferences.pref()


terminal = pygame.font.Font(fp("texture/terminal.ttf"), 20)
terminal2 = pygame.font.Font(fp("texture/terminal.ttf"), 30)
prompt = pygame.font.Font(fp("texture/terminal.ttf"), 14)


class Item:
    def __init__(
        self,
        name,
        desc,
        im,
        max_stack=1,
        pick_up_sound=None,
        consumable=False,
        sanity_buff=0,
        drop_weight=0,
        drop_stack=None,
    ):
        self.name = name
        self.desc = desc
        self.im = im
        self.image = pygame.transform.scale(
            pygame.image.load(fp("texture/items/" + im)), (45, 45)
        ).convert_alpha()
        self.center = self.image.get_rect().center
        self.rect = self.image.get_rect().size
        self.max_stack = max_stack
        self.pickup_sound = pick_up_sound
        self.consumable = consumable
        self.sanity_buff = sanity_buff
        self.token = str(random.uniform(0, 1))
        self.drop_weight = drop_weight
        if drop_stack != None:
            self.drop_stack = drop_stack
        else:
            self.drop_stack = self.max_stack

    def copy(self):
        return Item(
            self.name,
            desc=self.desc,
            im=self.im,
            max_stack=self.max_stack,
            pick_up_sound=self.pickup_sound,
            consumable=self.consumable,
            sanity_buff=self.sanity_buff,
        )

    def get_name(self):
        return self.name

    def sound(self):
        return self.pickup_sound

    def render(self, screen, pos, mouse_pos, clicked, r_click_tick, transfer = False):
        render_pos = [pos[0] - self.center[0], pos[1] - self.center[1]]
        screen.blit(self.image, render_pos)
        if transfer:
            print("Rendering item with transfer on")
        if (
            render_pos[0] < mouse_pos[0] < render_pos[0] + self.rect[0]
            and render_pos[1] < mouse_pos[1] < render_pos[1] + self.rect[1]
        ) or transfer:
            text = terminal2.render(self.name, False, [255, 255, 255])
            t_s = text.get_rect().size
            alpha_surf = pygame.Surface(t_s).convert()
            alpha_surf.fill((0, 0, 0))
            alpha_surf.set_alpha(200)
            screen.blit(alpha_surf, func.minus(mouse_pos, [0, 40]))
            screen.blit(text, func.minus(mouse_pos, [0, 40]))
            text = prompt.render(self.desc, False, [255, 255, 255])
            t_s2 = text.get_rect().size
            alpha_surf = pygame.Surface(t_s2).convert()
            alpha_surf.fill((0, 0, 0))
            alpha_surf.set_alpha(200)
            screen.blit(alpha_surf, func.minus(mouse_pos, [0, 40 + t_s[1]]))
            screen.blit(text, func.minus(mouse_pos, [0, 40 + t_s[1]]))
            pressed = pygame.key.get_pressed()
            if r_click_tick:
                return (True, "consume")

            elif (clicked and pressed[pygame.K_LSHIFT]) or transfer:
                print("Quick transfering")
                return (True, "append")

            elif clicked:
                return (True, "pickup")

        return False, False


# items = {"HE Grenade": Item("HE Grenade", "Fragmentation grenade agains personell on foot.", "grenade.png", max_stack = 1, pick_up_sound = grenade_pickup),
#         "Heroin": Item("Heroin", "Highly intoxicating opioid.", "heroin.png", max_stack = 1, pick_up_sound = needle_pickup, consumable = True, sanity_buff = 40),
#         "Cocaine": Item("Cocaine", "A potent stimulant.", "coca.png", max_stack = 1, pick_up_sound = needle_pickup, consumable = True, sanity_buff = 20),
#         "Diazepam": Item("Diazepam", "Mild anxienty relievant and sleeping pill.", "pills.png", max_stack = 1, pick_up_sound = pill_pickup, consumable = True, sanity_buff = 7.5),
#         "45 ACP": Item("45 ACP", "Generic subsonic pistol ammo.", "45acp.png", max_stack = 40, pick_up_sound = bullet_pickup),
#         "50 CAL": Item("50 CAL", "High energy cartiridge capable of penetrating armor.", "50cal.png", max_stack = 5, pick_up_sound = bullet_pickup),
#         "9MM": Item("9MM", "Common submachine gun ammo.", "9mm.png", max_stack = 25, pick_up_sound = bullet_pickup),
#         "12 GAUGE": Item("12 GAUGE", "Cartridges containing numerous projectiles.", "gauge.png", max_stack = 8, pick_up_sound = bullet_pickup),
#         "7.62x39MM": Item("7.62x39MM", "Supersonic assault rifle round with high stopping power.", "762.png", max_stack = 30, pick_up_sound = bullet_pickup)}

items = {
    "HE Grenade": Item(
        "HE Grenade",
        "Fragmentation grenade.",
        "grenade.png",
        max_stack=10,
        pick_up_sound=grenade_pickup,
        drop_weight=4,
        drop_stack=2,
    ),
    "Heroin": Item(
        "Heroin",
        "Restores +25% sanity.",
        "heroin.png",
        max_stack=1,
        pick_up_sound=needle_pickup,
        consumable=True,
        sanity_buff=50,
        drop_weight=0.1,
    ),
    "Cocaine": Item(
        "Cocaine",
        "Restores +10% sanity.",
        "coca.png",
        max_stack=3,
        pick_up_sound=sniff_sound,
        consumable=True,
        sanity_buff=20,
        drop_weight=0.8,
        drop_stack=1,
    ),
    "Diazepam": Item(
        "Diazepam",
        "Restores +2.5% sanity.",
        "pills.png",
        max_stack=5,
        pick_up_sound=pill_pickup,
        consumable=True,
        sanity_buff=10,
        drop_weight=2.5,
        drop_stack=2,
    ),

    "50 CAL": Item(
        "50 CAL",
        "Very heavy ammo.",
        "50cal.png",
        max_stack=100,
        pick_up_sound=bullet_pickup,
        drop_weight=3,
        drop_stack=40,
    ),
    "45 ACP" : Item(
        "45 ACP",
        "Generic subsonic pistol ammo.", 
        "45acp.png",
        max_stack=440,
        pick_up_sound=bullet_pickup,
        drop_weight=7,
        drop_stack=120,
    ),
    "9MM": Item(
        "9MM",
        "Pistol and submachine gun ammo.",
        "9mm.png",
        max_stack=400,
        pick_up_sound=bullet_pickup,
        drop_weight=6,
        drop_stack=70,
    ),
    "12 GAUGE": Item(
        "12 GAUGE",
        "Shotgun cartridge.",
        "gauge.png",
        max_stack=120,
        pick_up_sound=bullet_pickup,
        drop_weight=3,
        drop_stack=50,
    ),
    "7.62x39MM": Item(
        "7.62x39MM",
        "Assault rifle ammo.",
        "762.png",
        max_stack=360,
        pick_up_sound=bullet_pickup,
        drop_weight=3,
        drop_stack=120,
    ),
    "Sentry Turret": Item(
        "Sentry Turret",
        "Automatic turret that fires upon enemies",
        "turret.png",
        max_stack=3,
        pick_up_sound=turret_pickup,
        consumable=True,
        drop_weight=1.8,
        drop_stack=2,
    ),
    "Moving Turret": Item(
        "Moving Turret",
        "Turret that protects you on the go.",
        "turretMov.png",
        max_stack=1,
        pick_up_sound=turret_pickup,
        consumable=True,
        drop_weight=0.4,
        drop_stack=1,
    ),
    "Barricade": Item(
        "Barricade",
        "Blocks passage.",
        "barricade.png",
        max_stack=3,
        pick_up_sound=turret_pickup,
        consumable=True,
        drop_weight=0.5,
        drop_stack=1,
    ),
    "Molotov": Item(
        "Molotov",
        "Makeshift firebomb.",
        "molotov.png",
        max_stack=10,
        pick_up_sound=molotov_pickup,
        drop_weight=3,
        drop_stack=1,
    ),
    "5.56x45MM NATO": Item(
        "5.56x45MM NATO",
        "Powerful LMG ammo.",
        "556.png",
        max_stack=999,
        pick_up_sound=bullet_pickup,
        drop_weight=0.1,
        drop_stack=999,
    ),
    "Energy Cell": Item(
        "Energy Cell",
        "Illegal energy weapon ammo.",
        "energy_cell.png",
        max_stack=300,
        pick_up_sound=energy_cell_sound,
        drop_weight=1,
        drop_stack=99,
    ),
    "Upgrade Token": Item(
        "Upgrade Token",
        "Vagabond will trade you these for upgrades.",
        "upgradeToken.png",
        max_stack = 3,
        pick_up_sound=energy_cell_sound,
        drop_weight = 1,
        drop_stack = 1,
    ),
}


drop_table = {}
drop_index = 0

for item_1 in items:
    drop_table[drop_index] = item_1

    drop_index += items[item_1].__dict__["drop_weight"]




class Inventory:
    def __init__(self, app, list, player=False):
        self.inventory_open = False
        self.contents = {}
        self.search_obj = None
        self.item_in_hand = None
        self.hand_tick = 0
        self.picked_up_slot = None
        self.player = player
        self.app = app

        self.click = False
        self.columns = 3

        self.interctables_reference = list

    def set_inventory(self, dict):
        self.contents = dict

    def drop_inventory(self, pos):
        for slot in self.contents:

            if not self.app.storyTeller.determineItemDropping(self.contents[slot]["item"], self.contents[slot]["amount"]):
                continue

            self.interctables_reference.append(
                Interactable(
                    self.app,
                    pos,
                    self,
                    type="item",
                    item=items[self.contents[slot]["item"].__dict__["name"]].copy(),
                    amount=self.contents[slot]["amount"],
                )
            )

        self.contents = {}

    def toggle_inv(self, app, b=None, player_pos=[0, 0]):

        start_b = self.inventory_open

        if b != None:
            self.inventory_open = b
        else:
            if self.inventory_open:
                self.inventory_open = False
            else:
                self.inventory_open = True

        if self.inventory_open == False and self.item_in_hand != None:
            self.interctables_reference.append(
                Interactable(
                    self.app,
                    player_pos,
                    self,
                    type="item",
                    item=items[self.item_in_hand["item"].__dict__["name"]].copy(),
                    amount=self.item_in_hand["amount"],
                )
            )
            self.item_in_hand = None

        if self.player:
            inv_close.stop()
            inv_open.stop()

        pygame.mouse.set_visible(self.inventory_open)

        if self.inventory_open == False and self.player:
            if start_b != self.inventory_open:
                inv_close.play()
        elif self.player:
            inv_open.play()

    def set_search(self, obj):
        self.search_obj = obj

    def try_deleting_self(self, obj, player_pos):
        if self.search_obj == obj:
            self.search_obj = None
            self.toggle_inv(None, False, player_pos=player_pos)

    def get_amount_of_type(self, name):
        return sum(
            self.contents[slot]["amount"]
            for slot in self.contents
            if self.contents[slot]["item"].get_name() == name
        )

    def append_to_inv(self, item_type, amount, scan_only=False):
        amount_in_start = amount

        for slot, slot_data in self.contents.items():
            if slot_data["item"].get_name() == item_type.get_name():
                max_stack = slot_data["item"].max_stack
                available_space = max_stack - slot_data["amount"]

                if amount <= available_space:
                    if not scan_only:
                        slot_data["amount"] += amount
                        if self.player:
                            item_type.sound().play()
                    return 0
                else:
                    amount -= available_space
                    if not scan_only:
                        slot_data["amount"] = max_stack

        for slot in range(1, (1 + self.columns * 3)):
            if slot not in self.contents:
                if not scan_only:
                    self.contents[slot] = {"item": item_type, "amount": amount}
                    if self.player:
                        item_type.sound().play()
                return 0

        if amount_in_start != amount and self.player and not scan_only:
            item_type.sound().play()

        return amount


    def remove_amount(self, name, amount2):
        amount = amount2

        delete_slots = []

        for slot in self.contents:
            if self.contents[slot]["item"].get_name() == name:
                if self.contents[slot]["amount"] > amount:
                    self.contents[slot]["amount"] -= amount
                    break
                else:
                    amount -= self.contents[slot]["amount"]
                    delete_slots.append(slot)
                    if amount <= 0:
                        break

        for x in delete_slots:
            del self.contents[x]

    def get_inv(self):
        return self.inventory_open
    
    def draw_contents(self, screen, x_d, y_d, obj, default_pos, mouse_pos, clicked, r_click_tick, player_actor, app, inv_2=False):
        self.picked_up_slot = None

        content = obj.contents
        auto_transfer = inv_2 and 3 in app.joystickEvents

        for slot, slot_data in content.items():
            if self.item_in_hand == slot_data:
                continue

            y = 1 if slot <= obj.columns else (2 if slot <= obj.columns * 2 else 3)
            x = (slot - 1) % obj.columns + 1
            pos = [default_pos[0] + x * 62 + x_d, default_pos[1] + y * 62 + y_d]

            item_clicked, item_type = slot_data["item"].render(screen, pos, mouse_pos, clicked, r_click_tick, transfer=auto_transfer)
            auto_transfer = False

            if item_clicked and self.hand_tick == 0:
                if item_type == "append" and inv_2:
                    amount = self.append_to_inv(slot_data["item"], slot_data["amount"])
                    if amount == 0:
                        self.picked_up_slot = slot
                    else:
                        slot_data["amount"] = amount
                elif self.item_in_hand is None and item_type == "pickup":
                    self.item_in_hand = slot_data
                    self.hand_tick = 3
                    self.picked_up_slot = slot
                elif self.item_in_hand is None and item_type == "consume" and slot_data["item"].consumable:
                    slot_data["amount"] -= 1
                    if slot_data["amount"] == 0:
                        self.picked_up_slot = slot
                    self.hand_tick = 3
                    self.handle_consumable_item(slot_data["item"], player_actor, app)

            self.display_stack_count(screen, slot_data["amount"], pos)

        if self.picked_up_slot is not None:
            del content[self.picked_up_slot]

    def handle_consumable_item(self, item, player_actor, app):
        if item.name == "Sentry Turret":
            self.handle_turret_pickup(player_actor)
        elif item.name == "Moving Turret":
            self.handle_moving_turret_pickup(player_actor, app.MovTurretData, app)
        elif item.name == "Barricade":
            self.handle_barricade_pickup(player_actor)
        else:
            player_actor.set_sanity(item.sanity_buff, add=True)
            drug_use.play()

    def handle_turret_pickup(self, player_actor):
        pos_player = player_actor.get_pos()
        turret_bullets = player_actor.turret_bullets
        turr = objects.Turret.Turret(pos_player, 8, 10, 500, 20, 500 * turret_bullets)
        turret_list.append(turr)
        packet_dict.setdefault("turrets", []).append(turr)
        turret_pickup.play()

    def handle_moving_turret_pickup(self, player_actor, turret_data, app):
        pos_player = player_actor.get_pos()
        map, NAV_MESH, walls_filtered = turret_data
        turret = objects.MovingTurret.MovingTurret(pos_player, 4, 5, 500, 20, 1000, NAV_MESH=NAV_MESH, walls=walls_filtered, map=map, app=app)
        turret._pos = pos_player.copy()
        turret.navmesh_ref = NAV_MESH.copy()
        turret.wall_ref = walls_filtered
        turret_bro.append(turret)
        turret_pickup.play()

    def handle_barricade_pickup(self, player_actor):
        pos_player = player_actor.get_pos()
        player_actor.barricade_in_hand = objects.Barricade.Barricade(pos_player, pygame)
        turret_pickup.play()

    def display_stack_count(self, screen, amount, pos):
        text = prompt.render(str(amount), False, [255, 255, 255])
        t_s = text.get_rect().size
        alpha_surf = pygame.Surface(t_s).convert()
        alpha_surf.fill((0, 0, 0))
        alpha_surf.set_alpha(200)
        screen.blit(alpha_surf, [pos[0] + 25 - t_s[0], pos[1] + 25 - t_s[1]])
        screen.blit(text, [pos[0] + 25 - t_s[0], pos[1] + 25 - t_s[1]])

    def draw_inventory(self, screen, x_d, y_d, mouse_pos, clicked, player_pos, r_click_tick, player_actor, app):
        self.handle_inventory_click(clicked)

        if self.inventory_open:
            self.draw_inventory_info(screen, x_d, y_d, player_actor)
            self.draw_inventory_contents(screen, x_d, y_d, mouse_pos, clicked, r_click_tick, player_actor, app)

    def handle_inventory_click(self, clicked):
        if clicked and not self.click and self.inventory_open:
            inv_click.play()
            self.click = True
        elif not clicked:
            self.click = False

    def draw_inventory_info(self, screen, x_d, y_d, player_actor):
        text = terminal.render(f"Money : {player_actor.money}$", False, [255, 255, 255])
        screen.blit(text, (15 + x_d, 130 + y_d))

        inv_images = {3: inv_image, 4: inv4_image, 5: inv5_image}
        screen.blit(inv_images.get(self.columns, inv_image), [15 + x_d, 150 + y_d])

        text = terminal2.render("INVENTORY", False, [255, 255, 255])
        screen.blit(text, (32 + x_d, 161 + y_d))

    def draw_inventory_contents(self, screen, x_d, y_d, mouse_pos, clicked, r_click_tick, player_actor, app):
        default_pos = [-10, 160]

        if self.hand_tick != 0 and not clicked:
            self.hand_tick -= 1

        self.draw_contents(
            screen,
            x_d,
            y_d,
            self,
            [-10, 160],
            mouse_pos,
            clicked,
            r_click_tick,
            player_actor,
            app,
        )

        if self.search_obj:
            self.draw_search_obj_contents(
                screen,
                x_d,
                y_d,
                mouse_pos,
                clicked,
                r_click_tick,
                player_actor,
                app,
            )

        if self.item_in_hand:
            self.draw_item_in_hand(screen, mouse_pos, clicked, r_click_tick, x_d, y_d, player_actor)

    def draw_search_obj_contents(self, screen, x_d, y_d, mouse_pos, clicked, r_click_tick, player_actor, app):
        screen.blit(inv_image, [size[0] - 254 + x_d, 150 + y_d])
        text = terminal2.render(self.search_obj.get_name(), False, [255, 255, 255])
        screen.blit(text, (size[0] - 237 + x_d, 161 + y_d))

        self.draw_contents(
            screen,
            x_d,
            y_d,
            self.search_obj,
            [size[0] - 284, 160],
            mouse_pos,
            clicked,
            r_click_tick,
            player_actor,
            app,
            inv_2=True,
        )

    def draw_item_in_hand(self, screen, mouse_pos, clicked, r_click_tick, x_d, y_d, player_actor):
        if clicked and self.hand_tick == 0:
            self.handle_item_placement(mouse_pos, x_d, y_d, player_actor)
        else:
            self.item_in_hand["item"].render(
                screen, mouse_pos, mouse_pos, clicked, r_click_tick
            )
            self.display_stack_count(screen, self.item_in_hand["amount"], mouse_pos)

    def handle_item_placement(self, mouse_pos, x_d, y_d, player_actor):
        inserted = False
        positions = [[24 - 62, 133], [542, 133]] if self.search_obj is None else [[24 - 62, 133], [size[0] - 316, 133]]
        columns = self.columns if self.search_obj is None else self.search_obj.columns

        for def_pos in positions:
            for slot in range(1, (1 + columns * 3)):
                y = 1 if slot <= columns else (2 if slot <= columns * 2 else 3)
                x = (slot - 1) % columns + 1
                pos = [def_pos[0] + x * 62 + x_d, def_pos[1] + y * 62 + y_d]

                if pos[0] < mouse_pos[0] < pos[0] + 62 and pos[1] < mouse_pos[1] < pos[1] + 62:
                    inserted = self.handle_item_insertion(def_pos, slot, columns)
                    break

        if not inserted:
            self.handle_item_interactable_creation(player_actor)

    def handle_item_insertion(self, def_pos, slot, columns):
        if def_pos == [24 - 62, 133]:
            if slot in self.contents:
                self.handle_item_insertion_within_inventory(slot)
            else:
                self.handle_item_insertion_outside_inventory(slot)
            return True
        elif self.search_obj:
            self.handle_item_insertion_within_search_obj(slot)
            return True
        return False

    def handle_item_insertion_within_inventory(self, slot):
        if (
            self.contents[slot]["item"].get_name()
            == self.item_in_hand["item"].get_name()
        ):
            if (
                self.contents[slot]["amount"] + self.item_in_hand["amount"]
                <= self.item_in_hand["item"].max_stack
            ):
                self.contents[slot]["amount"] += self.item_in_hand["amount"]
                self.item_in_hand["item"].sound().play()
                self.item_in_hand = None
            else:
                self.item_in_hand["amount"] -= (
                    self.item_in_hand["item"].max_stack
                    - self.contents[slot]["amount"]
                )
                self.contents[slot]["amount"] = self.item_in_hand["item"].max_stack
                self.item_in_hand["item"].sound().play()
        else:
            item_1 = self.contents[slot]
            self.contents[slot] = self.item_in_hand
            self.item_in_hand = item_1

    def handle_item_insertion_outside_inventory(self, slot):
        self.contents[slot] = self.item_in_hand
        self.item_in_hand["item"].sound().play()
        self.item_in_hand = None

    def handle_item_insertion_within_search_obj(self, slot):

        if slot not in self.search_obj.contents:
            self.search_obj.contents[slot] = self.item_in_hand
            self.item_in_hand["item"].sound().play()
            self.item_in_hand = None
            
        elif (
            self.item_in_hand["item"].get_name()
            == self.search_obj.contents[slot]["item"].get_name()
        ):
            self.search_obj.__dict__["contents"][slot]["amount"] += self.item_in_hand["amount"]
            self.item_in_hand["item"].sound().play()
            self.item_in_hand = None
        else:
            item_1 = self.search_obj.contents[slot]
            self.search_obj.contents[slot] = self.item_in_hand
            self.item_in_hand = item_1
            self.item_in_hand["item"].sound().play()

    def handle_item_interactable_creation(self, player_actor):
        self.interctables_reference.append(
            Interactable(
                self.app,
                player_actor.pos,
                self,
                type="item",
                item=items[self.item_in_hand["item"].__dict__["name"]].copy(),
                amount=self.item_in_hand["amount"],
            )
        )
        self.item_in_hand = None



class Interactable:
    def __init__(
        self,
        app,
        pos,
        player_inventory,
        player_weapons = [],
        list=[],
        name="Box",
        type="crate",
        item=None,
        amount=1,
        collide=False,
        map=None,
        image=None,
        door_dest=None,
        active=True,
        angle = 0,
        overrideSize = [119, 119],
        nonDayDoor = False,
        endlessOnly = False,
    ):

        self.init_values = [
            app,
            pos,
            player_inventory,
            player_weapons,
            list,
            name,
            type,
            item,
            amount,
            collide,
            map,
            image,
            door_dest,
            active,
            angle,
            overrideSize,
            nonDayDoor,
            endlessOnly,
        ]
        self.app = app
        self.endlessOnly = endlessOnly

        if type not in ("item", "gun_drop"):
            self.pos = func.mult(pos,multiplier2)
        else:
            self.pos = pos
        self.button_prompt = ""

        self.alive = True
        self.nonDayDoor = nonDayDoor

        self.active = active
        self.rarity = 10
        self.type = type
        if self.type == "crate":
            self.name = name
            self.image = load("texture/box.png", size = [80,80], alpha = False)
        elif self.type == "item" or self.type == "gun_drop":
            self.lifetime = 3000
            self.pos = [
                self.pos[0] + random.randint(-35, 35),
                self.pos[1] + random.randint(-35, 35),
            ]
            self.name = item.name
            self.item = item
            self.amount = amount
            if self.type == "item":
                self.rarity = item.drop_weight
                self.image = load("texture/items/" + self.item.im, size = [40,40])
            else:
                self.image = func.colorize(load(self.item.image_directory, size = [100, 34]), pygame.Color(200,200,200))

            self.rect = self.image.get_rect()
            self.rect.inflate_ip(4, 4)
            if self.type == "item":
                if items[self.name].drop_weight < 0.6:
                    self.prompt_color = RED_COLOR
                elif items[self.name].drop_weight < 1.5:
                    self.prompt_color = PURPLE_COLOR
                elif items[self.name].drop_weight < 3.5:
                    self.prompt_color = CYAN_COLOR
                else:
                    self.prompt_color = WHITE_COLOR
            else:
                self.prompt_color = (255, 106, 0)

        elif self.type == "NPC":
            self.name = name
            self.image = pygame.transform.scale(
                pygame.image.load(fp("texture/" + image)),
                [round(overrideSize[0] / multiplier), round(overrideSize[1] / multiplier)],
            ).convert_alpha()
            self.npc_active = False

        elif self.type == "door":
            self.name = name

            self.door_tick = GameTick(20)
            self.door_dest = door_dest

        if self.type != "door":
            self.center_pos = [
                self.pos[0] + self.image.get_rect().center[0],
                self.pos[1] + self.image.get_rect().center[1],
            ]
        else:
            self.center_pos = self.pos.copy()

        self.inv_save = player_inventory
        self.gun_save = player_weapons
        self.contents = {}
        self.dialogue_bias = None
        self.angle = angle
        if angle and self.type != "door":
            self.image = pygame.transform.rotate(self.image, angle)

        self.columns = 3

        if self.type == "crate":
            while True:

                drop = random.uniform(0, drop_index)
                keys = drop_table.keys()
                key_prox = {
                    drop - key: [drop_table[key], key]
                    for key in keys
                    if drop - key >= 0
                }

                item, key = key_prox[min(key_prox.keys())]
                self.contents[random.randint(1, 9)] = {
                    "amount": random.randint(1, items[item].__dict__["drop_stack"]),
                    "item": items[item],
                    "token": str(random.uniform(0, 1)),
                }
                if random.randint(1, 2) == 1:
                    break

        if collide:

            rect = self.image.get_rect().size
            map.append_polygon([self.pos[0], self.pos[1], rect[0], rect[1]])

    def tick_prompt(self, screen, player_pos, camera_pos, f_press=False):
        if self.button_prompt:

            if self.type == "gun_drop":
                if len(self.gun_save) == 5:
                    compareGuns(self.app, screen, self.app.c_weapon, self.item, player_pos, camera_pos, self.inv_save)
                else:
                    compareGuns(self.app, screen, False, self.item, player_pos, camera_pos, self.inv_save)
      
                self.button_prompt.tick(screen, player_pos, camera_pos, f_press)
            else:
                self.button_prompt.tick(screen, player_pos, camera_pos, f_press)

            
                


    def re_init(self):
        (app,
        pos,
        player_inventory,
        player_weapons,
        list,
        name,
        type,
        item,
        amount,
        collide,
        map,
        image,
        door_dest,
        active,
        angle,
        overrideSize,
        nonDayDoor,
        endlessOnly) = self.init_values

        self.__init__(
            app,
            pos,
            player_inventory,
            player_weapons = player_weapons,
            list = list,
            name = name,
            type = type,
            item = item,
            amount = amount,
            collide = collide,
            map = map,
            image = image,
            door_dest = door_dest,
            active = active,
            angle = angle,
            overrideSize = overrideSize,
            nonDayDoor = nonDayDoor,
            endlessOnly = endlessOnly,
        )


    def prompt_dist(self, player_pos):
        if self.button_prompt:
            return los.get_dist_points(player_pos, self.center_pos)
        else:
            return False

    def get_name(self):
        return self.name

    def ring_phone(self, player_pos):
        dist = max([1 - (los.get_dist_points(self.pos, player_pos) / 500 * multiplier2), 0])
        phone_ring.set_volume(dist)
        if phone_ring.get_num_channels() == 0:
            phone_ring.play()

    def tick(self, screen, player_pos, camera_pos):

        if self.name == "Payphone" and self.active:
            self.ring_phone(player_pos)
            if self.dialogue_bias == None:
                self.dialogue_bias = 0
        elif self.name == "Alan":
            if self.inv_save.columns == 5:
                self.dialogue_bias = 1
            else:
                self.dialogue_bias = 0

        if self.type == "item" or self.type == "gun_drop":
            self.rect.topleft = func.minus_list(self.pos, camera_pos)
            if round(self.lifetime) % 18 < 9:
                pygame.draw.rect(
                    screen,
                    self.prompt_color,
                    self.rect,
                    1 + round(self.lifetime % 18 / 5),
                )
            self.lifetime -= timedelta.mod(1)

            if self.lifetime < 0:
                self.alive = False

        if self.type == "door":

            if self.active:

                self.door_tick.tick()

                rect = pygame.Rect(
                    self.pos[0] - camera_pos[0], self.pos[1] - camera_pos[1], 0, 0
                )

                rect.inflate_ip(
                    (100 if not self.angle else 10) * self.door_tick.value / self.door_tick.max_value,
                    (100 if self.angle else 10) * self.door_tick.value / self.door_tick.max_value,
                )

                pygame.draw.rect(screen, [255, 255, 255], rect, 3)

        else:
            screen.blit(self.image, func.minus_list(self.pos, camera_pos))

        if self.active:

            if los.get_dist_points(player_pos, self.center_pos) < 100 * multiplier2:
                if self.type == "NPC" and dialogue != []:
                    return
                self.button_prompt = button_prompt(self, self.inv_save)

            else:
                self.inv_save.try_deleting_self(self, player_pos)

    def interact(self):
        if self.type == "crate":
            self.inv_save.set_search(self)
            self.inv_save.toggle_inv(None, True)
        elif self.type == "item":
            cond = self.inv_save.append_to_inv(self.item, self.amount)
            if cond == 0:
                self.alive = False
            else:
                self.amount = cond

        elif self.type == "gun_drop":
            able_to_append = True
            for i in self.gun_save:
                if i.name == self.name:
                    able_to_append = False
            if able_to_append:

                if len(self.gun_save) < 5:
                    self.gun_save.append(self.item.copy())
                else:
                    for i, x1 in enumerate(self.gun_save):
                        if x1.name == self.app.c_weapon.name:

                            interactables.append(Interactable(self.app, self.pos, self.inv_save, player_weapons = self.gun_save, type = "gun_drop", item = self.app.c_weapon.copy()))
                            self.app.weaponChangeTick.value = 0

                            self.gun_save[i] = self.item.copy()
                            self.app.c_weapon = self.gun_save[i]
                            break

                self.alive = False
                self.item.reload_sound.play()

        elif self.type == "NPC":
            self.npc_active = True
            dialogue.clear()
            dialogue.append(Dialogue(self.name, self.app, self.dialogue_bias))

        elif self.type == "door":
            loading_cue.append(self.door_dest)

            if self.nonDayDoor:
                self.app.dontIncreaseDay = True

            door_sound.play()

    def get_pos(self, center=False):
        return self.center_pos if center else self.pos

    def kill_bp(self):
        self.button_prompt = ""


class button_prompt:
    def __init__(self, object, player_inventory):

        self.object = object
        if self.object.__dict__["type"] == "crate":
            self.text_render = prompt.render("F to search", False, [255, 255, 255])
            if self.object.__dict__["contents"] == {}:
                self.text_render2 = prompt.render(
                    self.object.__dict__["name"] + " (Empty)", False, [255, 255, 255]
                )
            else:
                self.text_render2 = prompt.render(
                    self.object.__dict__["name"], False, [255, 255, 255]
                )
        elif self.object.type == "item":
            self.text_render2 = prompt.render(
                self.object.__dict__["name"]
                + " ("
                + str(self.object.__dict__["amount"])
                + ")",
                False,
                [255, 255, 255],
            )

            if (
                player_inventory.append_to_inv(
                    self.object, self.object.__dict__["amount"], scan_only=True
                )
                != self.object.__dict__["amount"]
            ):

                self.text_render = prompt.render("F to pick up", False, [255, 255, 255])

            else:

                self.text_render = prompt.render(
                    "NO ROOM IN INVENTORY", False, [255, 0, 0]
                )

        elif self.object.type == "gun_drop":
            self.text_render2 = prompt.render(
                self.object.name,
                False,
                [255, 255, 255],
            )

            able_to_append = True
            for i in self.object.gun_save:
                if i.name == self.object.name:
                    able_to_append = False
            if able_to_append:

                if len(self.object.gun_save) < 5:
                    self.text_render = prompt.render("F to pick up", False, [255, 255, 255])
                else:
                    self.text_render = prompt.render("F to switch with current weapon", False, [255, 255, 255])
                    

            else:
                self.text_render = prompt.render(
                    "ALREADY IN INVENTORY", False, [255, 0, 0]
                )

        elif self.object.type == "NPC":
            self.text_render2 = prompt.render(
                self.object.__dict__["name"], False, [255, 255, 255]
            )
            self.text_render = prompt.render("Hold F to talk", False, [255, 255, 255])

        elif self.object.type == "door":
            self.text_render2 = prompt.render(
                self.object.__dict__["name"], False, [255, 255, 255]
            )
            self.text_render = prompt.render("F to enter", False, [255, 255, 255])

        self.rect = self.text_render.get_rect().center
        self.rect2 = self.text_render2.get_rect().center

    def tick(self, screen, player_pos, camera_pos, f_press):

        self.pos = self.object.get_pos(center=True)

        pos = [(self.pos[0] + player_pos[0]) / 2, (self.pos[1] + player_pos[1]) / 2]

        if self.object.type != "gun_drop":
            screen.blit(
                self.text_render2,
                func.minus_list(func.minus_list(pos, self.rect2), camera_pos),
            )
            screen.blit(
                self.text_render,
                func.minus(
                    func.minus_list(func.minus_list(pos, self.rect), camera_pos), [0, 20]
                ),
            )

        if self.object.type in ["gun_drop", "NPC"]:
            initiator = self.object.app.f_press_cont
        else:
            initiator = f_press

        if initiator:
            self.object.interact()
            self.object.kill_bp()

        if los.get_dist_points(self.pos, player_pos) > 100 * multiplier2:
            self.object.kill_bp()


class kill_count_render:
    def __init__(self, kills, rgb_list):
        mid = size[0] / 2
        start_x = mid - kills * 50 / 2
        self.x_poses = []
        self.images = rgb_list
        self.lifetime = 0
        self.max_lifetime = 45
        for x in range(kills):
            self.x_poses.append(start_x)

            start_x += 50

    def tick(self, screen, cam_delta, kill_counter):

        if len(self.x_poses) >= 10:
            if self.lifetime <= self.max_lifetime / 6:
                y = size[1] - 80 + 1 / ((self.lifetime + 1) ** 1.5) * 200
            elif self.max_lifetime / 6 < self.lifetime <= 4 * self.max_lifetime / 6:
                y = size[1] - 80
            else:
                y = size[1] - 80 + 1 / ((self.max_lifetime + 3 - self.lifetime) ** 1.2) * (200)

            func.rgb_render(
                self.images,
                min([len(self.x_poses), 30]),
                [size[0] / 2 - 50, y],
                cam_delta,
                screen,
            )

            func.rgb_render(
                kill_counter_texts[len(self.x_poses)],
                min([len(self.x_poses), 30]),
                [size[0]  / 2, y],
                cam_delta,
                screen,
            )

        else:

            for x in self.x_poses:
                if self.lifetime <= self.max_lifetime / 6:
                    y = size[1] - 80 + 1 / ((self.lifetime + 1) ** 1.5) * 200
                elif self.max_lifetime / 6 < self.lifetime <= 4 * self.max_lifetime / 6:
                    y = size[1] - 80
                else:
                    y = size[1] - 80 + 1 / ((self.max_lifetime + 3 - self.lifetime) ** 1.2) * (
                        200
                    )

                func.rgb_render(
                    self.images, min([len(self.x_poses), 7]), [x, y], cam_delta, screen
                )
        self.lifetime += timedelta.mod(1)
        if self.lifetime >= self.max_lifetime:
            del kill_counter


class Particle:
    def __init__(
        self,
        pos,
        pre_defined_angle=False,
        angle=0,
        magnitude=1,
        type="normal",
        screen=screen,
        dont_copy=False,
        color_override="red",
        fire_velocity_mod=1,
        app = None,
    ):
        self.pos = pos
        self.type = type
        self.fire_velocity_mod = fire_velocity_mod
        self.fire_x_vel = random.randint(-1, 1) * self.fire_velocity_mod
        self.intensity = random.uniform(0.03, 0.10)

        #if len(particle_list) > 500:
        #    particle_list.remove(particle_list[0])

        if pre_defined_angle == False:
            self.direction = math.radians(random.randint(0, 360))
        else:
            self.direction = math.radians(angle)

        if self.type == "blood_particle":
            magnitude *= 1.3

        if ultraviolence:
            if dont_copy == False:
                for i in range(4):
                    particle_list.append(
                        Particle(
                            pos,
                            pre_defined_angle=pre_defined_angle,
                            angle=angle,
                            magnitude=magnitude,
                            type=type,
                            screen=screen,
                            dont_copy=True,
                        )
                    )

            self.lifetime = round(
                random.randint(3, 10) * magnitude * random.uniform(1, 1.3)
            )

            self.max_life = 10 * magnitude * 1.3

            self.magnitude = round(magnitude * 3 * random.uniform(1, 1.3))




        else:
            self.lifetime = round(random.randint(3, 10) * magnitude)
            self.magnitude = round(magnitude * 3)
            self.start_lt = self.lifetime
            self.max_life = 10 * magnitude

        self.color2 = [
            random.randint(0, 50),
            random.randint(155, 255),
            random.randint(235, 255),
        ]
        self.color_override = color_override
        if self.color_override == "red":
            self.color3 = [
                random.randint(200, 220),
                random.randint(0, 50),
                random.randint(0, 50),
            ]
        elif self.color_override == "yellow":
            self.color3 = [
                random.randint(220, 255),
                random.randint(220, 255),
                random.randint(0, 50),
            ]
            self.intensity *= 2
        elif isinstance(self.color_override, list):
            self.color3 = self.color_override

        self.draw_surface = screen

    def tick(self, screen, camera_pos, map=None):

        if round(self.lifetime) > 0:

            if self.type == "fire":
                self.fire_x_vel += random.uniform(-0.5, 0.7) * self.fire_velocity_mod
                self.pos = [
                    self.pos[0] + timedelta.mod(self.fire_x_vel),
                    self.pos[1] - timedelta.mod(random.randint(1, 4) * self.fire_velocity_mod),
                ]
                self.color = [
                    255,
                    round(255 * (round(self.lifetime) / (self.max_life + 5))),
                    round(255 * ((round(self.lifetime) / (self.max_life + 5)) ** 2)),
                ]
                self.dim = [
                    self.pos[0] - round(self.lifetime / 2),
                    self.pos[1] - round(self.lifetime / 2),
                    2 * self.lifetime / 3,
                    2 * self.lifetime / 3,
                ]
            elif self.type == "flying_blood":
                self.pos = [
                    self.pos[0] + timedelta.mod(
                    math.sin(self.direction) * self.lifetime),
                    self.pos[1] + timedelta.mod(
                    math.cos(self.direction) * self.lifetime)
                ]

            else:
                self.pos = [
                    self.pos[0] + timedelta.mod(
                    math.sin(self.direction + random.uniform(-0.5, 0.5))
                    * self.lifetime
                    + random.randint(-2, 2)),
                    self.pos[1] + timedelta.mod(
                    math.cos(self.direction + random.uniform(-0.3, 0.3))
                    * self.lifetime
                    + random.randint(-2, 2)),
                ]

            if self.type == "normal":
                self.dim = [
                    self.pos[0] - timedelta.mod(round(self.lifetime / 2)),
                    self.pos[1] - timedelta.mod(round(self.lifetime / 2)),
                    self.lifetime / 2,
                    self.lifetime / 2,
                ]
                self.color = [255, 255 - 255 / round(self.lifetime), 0]

            elif self.type == "flying_blood":

                self.dim = [
                    self.pos[0],
                    self.pos[1],
                    self.lifetime ** 0.5,
                    self.lifetime ** 0.5,
                ]

                self.color = [random.randint(175,220), 255 / round(self.lifetime+5), 255 / round(self.lifetime+5)]


            elif self.type == "energy":
                self.dim = [
                    self.pos[0] - timedelta.mod(round(self.lifetime / 2)),
                    self.pos[1] - timedelta.mod(round(self.lifetime / 2)),
                    self.lifetime / 2,
                    self.lifetime / 2,
                ]

                delta = (self.lifetime / self.start_lt) ** 3

                self.color = [255, 255 * delta, 255 * delta]

            elif self.type == "death_particle":
                self.dim = [
                    self.pos[0] - round(self.lifetime),
                    self.pos[1] - round(self.lifetime),
                    self.lifetime * 2,
                    self.lifetime * 2,
                ]
                self.color = [self.color2[0], self.color2[1], self.color2[2]]

            elif self.type == "blood_particle":

                self.dim = [
                    self.pos[0] - round(self.lifetime),
                    self.pos[1] - round(self.lifetime),
                    self.lifetime * 2,
                    self.lifetime * 2,
                ]
                if self.color_override == "red":
                    self.color = [
                        self.color3[0],
                        self.color3[1] / self.lifetime,
                        self.color3[2] / self.lifetime,
                    ]
                elif self.color_override == "yellow":
                    self.color = [
                        self.color3[0],
                        self.color3[1],
                        self.color3[2] / self.lifetime,
                    ]



                # if map != None:
                #     if (
                #         list(level.getcollisionspoint(map.rectangles, self.pos))
                #         != []
                #     ):
                #         particle_list.remove(self)
                #         return

            elif self.type == "item_particle":
                self.dim = [
                    self.pos[0] - round(self.lifetime / 2),
                    self.pos[1] - round(self.lifetime / 2),
                    self.lifetime,
                    self.lifetime,
                ]
                self.color = [
                    255 - 255 / self.lifetime**7,
                    255 - 255 / self.lifetime**0.2,
                    255 - 255 / self.lifetime**0.2,
                ]

            if isinstance(self.color_override, list):
                self.color = [
                    self.color3[0],
                    self.color3[1],
                    self.color3[2] / self.lifetime,
                ]

            pos = func.draw_pos([self.dim[0], self.dim[1]], camera_pos)
            pos.append(self.dim[2]*multiplier2)
            pos.append(self.dim[3]*multiplier2)
            if self.type in ["blood_particle"]:
                for i in range(random.randint(2,4)):
                    try:
                        surf = pygame.Surface((round(pos[2])-random.randint(-2,2), round(pos[3])-random.randint(-2,2)))
                    except:
                        continue
                    surf.fill([round(255-self.color[0])*self.intensity, round(255-self.color[1])*self.intensity, round(255-self.color[2])*self.intensity])
                    self.draw_surface.blit(surf, (pos[0]-random.randint(-2,2), pos[1]-random.randint(-2,2)), None, pygame.BLEND_RGB_SUB)
                mult = random.uniform(0.25,0.75)
                pygame.draw.rect(self.draw_surface,
                    [round(self.color[0] * mult), round(self.color[1] * mult), round(self.color[2] * mult)],
                    [pos[0] + random.randint(-10,10) + random.randint(0, round(pos[2])), pos[1] + random.randint(-10,10) + random.randint(0,round(pos[3])), random.randint(1,3), random.randint(1,3)],
                )
                map.bloodPoints[round(pos[0]/BLOODSINK_TILESIZE), round(pos[1]/BLOODSINK_TILESIZE)] += 0.01
                map.bloodPoints[round(pos[0]/BLOODSINK_TILESIZE), round(pos[1]/BLOODSINK_TILESIZE)] = min(map.bloodPoints[round(pos[0]/BLOODSINK_TILESIZE), round(pos[1]/BLOODSINK_TILESIZE)], 1)


            elif self.type == "fire":
                surf = pygame.Surface((round(pos[2]), round(pos[3])))
                surf.fill(self.color)
                self.draw_surface.blit(surf, (pos[0], pos[1]), None, pygame.BLEND_ADD)
            else:
                pygame.draw.rect(self.draw_surface, self.color, pos)
            self.lifetime -= timedelta.mod(1)
        else:
            particle_list.remove(self)




def player_hit_detection(pos, lastpos, player, damage):

    if player.get_hp() <= 0:
        return False

    player_pos = player.get_pos()

    points_1 = [
        [player_pos[0], player_pos[1] - 25],
        [player_pos[0], player_pos[1] + 25],
    ]
    points_2 = [
        [player_pos[0] - 25, player_pos[1]],
        [player_pos[0] + 25, player_pos[1]],
    ]

    if los.intersect(pos, lastpos, points_1[0], points_1[1]) or los.intersect(
        pos, lastpos, points_2[0], points_2[1]
    ):
        player.set_hp(damage, reduce=True)
        func.list_play(pl_hit)
        return True

    return False


class Player:
    def __init__(self, app, name, turret_bullets=1, inv = None):
        self.pos = [0, 0]
        self.name = name
        self.app = app
        self.hp = 100
        self.sanity = 100
        self.sanity_change = None
        self.sanity_change_tick = 0
        self.angle = 0
        self.aim_angle = 0
        self.barricade_in_hand = None
        self.turret_bullets = turret_bullets
        self.knockback_tick = 0
        self.knockback_angle = 0
        self.money = 0
        self.money_last_tick = 0
        self.unitstatuses = []
        self.np_pos = np.array([0,0], dtype = float)
        self.preferred_nade = "HE Grenade"
        self.inv = inv
        self.scrollLimit = len(ruperts_shop_selections)
        self.bloodSink = 0
        self.sinking = False

    def update_nade(self, inventory):
        nade_types = ["HE Grenade", "Molotov"]

        if inventory.get_amount_of_type(self.preferred_nade) == 0:
            for x in nade_types:
                if inventory.get_amount_of_type(x) != 0:
                    self.preferred_nade = x

    def change_nade(self, inventory):
        nade_types = ["HE Grenade", "Molotov"]

        for x in nade_types:
            if inventory.get_amount_of_type(x) != 0 and x != self.preferred_nade:
                self.preferred_nade = x
                return




    def set_pos(self, pos):
        self.pos = pos
        self.np_pos[0] = pos[0]
        self.np_pos[1] = pos[1]

    def set_angle(self, angle):
        self.angle = angle

    def set_aim_at(self, angle):
        self.aim_angle = angle

    def get_angle(self):
        return self.angle

    def knockback(self, amount, angle, daemon_bullet=False):

        self.knockback_tick = round(amount)
        self.knockback_angle = angle

    def get_pos(self):
        return self.pos

    def get_hp(self):
        return self.hp

    def get_sanity_change(self):
        if self.sanity_change != None:
            amount = self.sanity_change
            if self.sanity_change_tick > 0:
                self.sanity_change_tick -= timedelta.mod(1)
            else:
                self.sanity_change = None
            return amount, self.sanity_change_tick
        return False, 0

    def set_sanity(self, amount, add=False):
        if add:

            self.sanity += amount
            if self.sanity_change_tick > 0:
                self.sanity_change += amount
            else:
                self.sanity_change = amount
            self.sanity_change_tick = 90


        else:

            self.sanity -= amount

        if self.sanity > 100:
            self.sanity = 100
        elif self.sanity < 0:
            self.sanity = 0

    def set_hp(self, hp, reduce=False):
        if reduce:
            self.hp -= hp
        else:
            self.hp = hp
        if self.app.multiplayer:
            self.app.send_data(f"self.game_ref.multiplayer_actors['{self.name}'].set_hp({round(self.hp)})")



    def force_player_damage(self, damage):
        if self.hp > 0:
            self.set_hp(damage, reduce=True)
            func.list_play(pl_hit)


class Wall:
    def __init__(self, start, end):
        global walls
        self.__start = start
        self.__end = end
        self.__center = [(start[0] + end[0]) / 2, (start[1] + end[1]) / 2]

    def __str__(self):
        return "WALL: " + str(self.__start) + " " + str(self.__end)

    def get_center(self):
        return self.__center

    def get_points(self):
        return self.__start, self.__end


class Burn:
    def __init__(self, map, pos, magnitude, lifetime, infinite=False, magnitude2=1):
        self.pos = pos
        self.magnitude = magnitude
        self.life_max = lifetime
        self.lifetime = lifetime
        self.infinite = infinite
        self.magnitude2 = magnitude2
        self.quadrantType = 2
        map.setToQuadrant(self, self.pos)

    def tick(self, screen, map_render=None):

        if self.lifetime <= 0:
            burn_list.remove(self)
            self.quadrant.fires.remove(self)
            return

        for x in range(1):
            particle_list.append(
                Particle(
                    [
                        self.pos[0] + random.randint(-4, 4) * 2 * multiplier2,
                        self.pos[1] + random.randint(-4, 4) * 2 * multiplier2,
                    ],
                    type="fire",
                    magnitude=(self.magnitude * (self.lifetime / self.life_max) ** 0.7),
                    screen=screen,
                    fire_velocity_mod=self.magnitude2,
                )
            )

        if map_render != None and self.lifetime / self.life_max > random.randint(0, 2):
            random_angle = random.randint(0, 360)
            dist = random.randint(0, 1000) ** 0.5

            # size = 4*dist/(1000**0.5)

            pos = [
                self.pos[0] + math.cos(random_angle) * dist,
                self.pos[1] + math.sin(random_angle) * dist,
            ]

            if not self.infinite:
                size = random.randint(1,7)
                surf = pygame.Surface((size,size))
                surf.fill((30,30,30))
                map_render.blit(surf, pos, None, pygame.BLEND_RGB_SUB)



        if not self.infinite:
            self.lifetime -= timedelta.mod(1)
