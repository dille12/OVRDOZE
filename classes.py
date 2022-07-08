import os, sys
import pygame
import math
import random
import time
pygame.init()
import func
from values import *
import classtest
import los
import pyperclip
width, height = size
import objects
import get_preferences

a, draw_los, a, a, ultraviolence, a = get_preferences.pref()


terminal = pygame.font.Font('texture/terminal.ttf', 20)
terminal2 = pygame.font.Font('texture/terminal.ttf', 30)
prompt = pygame.font.Font('texture/terminal.ttf', 14)





class Item:
    def __init__(self, name, desc, im, max_stack = 1, pick_up_sound = None, consumable = False, sanity_buff = 0, drop_weight = 0, drop_stack = None):
        self.name = name
        self.desc = desc
        self.im = im
        self.image = pygame.transform.scale(pygame.image.load("texture/items/" + im), (45,45)).convert_alpha()
        self.center = self.image.get_rect().center
        self.rect = self.image.get_rect().size
        self.max_stack = max_stack
        self.pickup_sound = pick_up_sound
        self.consumable = consumable
        self.sanity_buff = sanity_buff
        self.token = str(random.uniform(0,1))
        self.drop_weight = drop_weight
        if drop_stack != None:
            self.drop_stack = drop_stack
        else:
            self.drop_stack = self.max_stack

    def copy(self):
        return Item(self.name, desc = self.desc,
        im = self.im,
        max_stack = self.max_stack,
        pick_up_sound = self.pickup_sound,
        consumable = self.consumable,
        sanity_buff = self.sanity_buff)


    def get_name(self):
        return self.name

    def sound(self):
        return self.pickup_sound

    def render(self, screen, pos, mouse_pos, clicked, r_click_tick):
        render_pos = [pos[0] - self.center[0], pos[1] - self.center[1]]
        screen.blit(self.image, render_pos)

        if render_pos[0] < mouse_pos[0] < render_pos[0] + self.rect[0] and render_pos[1] < mouse_pos[1] < render_pos[1] + self.rect[1]:
            text = terminal2.render(self.name, False, [255,255,255])
            t_s = text.get_rect().size
            alpha_surf =  pygame.Surface(t_s).convert()
            alpha_surf.fill((0,0,0))
            alpha_surf.set_alpha(200)
            screen.blit(alpha_surf, func.minus(mouse_pos,[0,40]))
            screen.blit(text, func.minus(mouse_pos,[0,40]))
            text = prompt.render(self.desc, False, [255,255,255])
            t_s2 = text.get_rect().size
            alpha_surf =  pygame.Surface(t_s2).convert()
            alpha_surf.fill((0,0,0))
            alpha_surf.set_alpha(200)
            screen.blit(alpha_surf, func.minus(mouse_pos,[0,40+ t_s[1]]))
            screen.blit(text, func.minus(mouse_pos,[0,40+ t_s[1]]))
            pressed = pygame.key.get_pressed()
            if r_click_tick:
                return (True,"consume")

            elif clicked and pressed[pygame.K_LSHIFT]:
                return (True, "append")

            elif clicked:
                return (True,"pickup")

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

items = {"HE Grenade": Item("HE Grenade", "Fragmentation grenade.", "grenade.png", max_stack = 5, pick_up_sound = grenade_pickup, drop_weight = 4, drop_stack = 2),
        "Heroin": Item("Heroin", "Restores +40% sanity.", "heroin.png", max_stack = 1, pick_up_sound = needle_pickup, consumable = True, sanity_buff = 40, drop_weight = 0.55),
        "Cocaine": Item("Cocaine", "Restores +20% sanity.", "coca.png", max_stack = 3, pick_up_sound = sniff_sound, consumable = True, sanity_buff = 20, drop_weight = 1, drop_stack = 1),
        "Diazepam": Item("Diazepam", "Restores +7.5% sanity.", "pills.png", max_stack = 5, pick_up_sound = pill_pickup, consumable = True, sanity_buff = 7.5, drop_weight = 2, drop_stack = 2),
        "45 ACP": Item("45 ACP", "Pistol ammo.", "45acp.png", max_stack = 9999, pick_up_sound = bullet_pickup, drop_weight = 7, drop_stack = 150),
        "50 CAL": Item("50 CAL", "Sniper ammo.", "50cal.png", max_stack = 999, pick_up_sound = bullet_pickup, drop_weight = 3, drop_stack = 40),
        "9MM": Item("9MM", "Submachine gun ammo.", "9mm.png", max_stack = 999, pick_up_sound = bullet_pickup, drop_weight = 6, drop_stack = 150),
        "12 GAUGE": Item("12 GAUGE", "Shotgun cartridge.", "gauge.png", max_stack = 999, pick_up_sound = bullet_pickup, drop_weight = 3, drop_stack = 50),
        "7.62x39MM": Item("7.62x39MM", "Assault rifle ammo.", "762.png", max_stack = 999, pick_up_sound = bullet_pickup, drop_weight = 3, drop_stack = 120),
        "Sentry Turret": Item("Sentry Turret", "Automatic turret that fires upon enemies", "turret.png", max_stack = 3, pick_up_sound = turret_pickup, consumable = True, drop_weight = 3, drop_stack = 2),
        "Barricade" : Item("Barricade", "Blocks passage.", "barricade.png", max_stack = 3, pick_up_sound = turret_pickup, consumable = True, drop_weight = 2, drop_stack = 1),
        "Molotov" : Item("Molotov", "Makeshift firebomb.", "molotov.png", max_stack = 5, pick_up_sound = molotov_pickup, drop_weight = 3, drop_stack = 1),
        "5.56x45MM NATO" : Item("5.56x45MM NATO", "Powerful LMG ammo.", "556.png", max_stack = 999, pick_up_sound = bullet_pickup, drop_weight = 0.1, drop_stack = 999)
        }




drop_table = {}
drop_index = 0

for item_1 in items:
    drop_table[drop_index] = item_1

    drop_index += items[item_1].__dict__["drop_weight"]


print(drop_table)


class Inventory:
    def __init__(self, list, player = False):
        self.inventory_open = False
        self.contents = {}
        self.search_obj = None
        self.item_in_hand = None
        self.hand_tick = 0
        self.picked_up_slot = None
        self.player = player




        self.click = False

        self.interctables_reference = list

    def set_inventory(self, dict):
        self.contents = dict

    def drop_inventory(self, pos):
        for slot in self.contents:
            print("Dropping:", self.contents[slot])
            self.interctables_reference.append(Interactable(pos, self, type = "item", item = items[self.contents[slot]["item"].__dict__["name"]].copy(), amount = self.contents[slot]["amount"]))

        self.contents = {}

    def toggle_inv(self, b = None, player_pos = [0,0]):



        start_b = self.inventory_open

        if b != None:
            self.inventory_open = b
        else:
            if self.inventory_open:
                self.inventory_open = False
            else:
                self.inventory_open = True

        if self.inventory_open == False and self.item_in_hand != None:
            self.interctables_reference.append(Interactable(player_pos, self, type = "item", item = items[self.item_in_hand["item"].__dict__["name"]].copy(), amount = self.item_in_hand["amount"]))
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
            self.toggle_inv(False, player_pos = player_pos)

    def get_amount_of_type(self, name):
        return sum(self.contents[slot]["amount"] for slot in self.contents if self.contents[slot]["item"].get_name() == name)

    def append_to_inv(self, type, amount, scan_only = False):
        amount_in_start = amount
        for slot in self.contents:
            if self.contents[slot]["item"].get_name() == type.get_name():
                if self.contents[slot]["amount"] + amount <= self.contents[slot]["item"].__dict__["max_stack"]:

                    if scan_only == False:

                        self.contents[slot]["amount"] += amount

                        if self.player:
                            type.sound().play()

                    return 0
                else:
                    amount -= self.contents[slot]["item"].__dict__["max_stack"] - self.contents[slot]["amount"]
                    if scan_only == False:
                        self.contents[slot]["amount"] = self.contents[slot]["item"].__dict__["max_stack"]

        for slot in range(1,10):
            if slot not in self.contents:
                if scan_only == False:
                    self.contents[slot] = {"item": type, "amount": amount}
                    if self.player:
                        type.sound().play()
                return 0
        if amount_in_start != amount and self.player and scan_only == False:
            type.sound().play()
        return amount



    def remove_amount(self, name, amount2):
        amount = amount2

        delete_slots = []

        for slot in self.contents:
            if self.contents[slot]["item"].get_name() == name:
                print("STILL TO BE REMOVED:",amount, "STACK AMOUNT:", self.contents[slot]["amount"] )
                if self.contents[slot]["amount"] > amount:
                    self.contents[slot]["amount"] -= amount
                    print(amount)
                    break
                else:
                    amount -= self.contents[slot]["amount"]
                    print(amount)
                    delete_slots.append(slot)
                    if amount <= 0:
                        break

        for x in delete_slots:
            print("DELETING SLOT")
            del self.contents[x]



    def get_inv(self):
        return self.inventory_open

    def draw_contents(self, screen, x_d, y_d, content, default_pos, mouse_pos, clicked, r_click_tick, player_actor, inv_2 = False):
        global barricade_in_hand, turret_bullets
        self.picked_up_slot = None

        for slot in content:

            if self.item_in_hand == content[slot]:
                continue

            if slot <= 3:
                y = 1
            elif slot <= 6:
                y = 2
            else:
                y = 3

            x = (slot-1)%3+1

            pos = [default_pos[0] + x*62 + x_d, default_pos[1] + y*62 + y_d]

            item_clicked, type = content[slot]["item"].render(screen, pos, mouse_pos, clicked, r_click_tick)

            if item_clicked and self.hand_tick == 0:

                if type == "append" and inv_2:
                    amount = self.append_to_inv(content[slot]["item"], content[slot]["amount"])
                    if amount == 0:
                        self.picked_up_slot = slot
                    else:
                        content[slot]["amount"] = amount



                elif self.item_in_hand == None and type == "pickup":
                    self.item_in_hand = content[slot]
                    self.hand_tick = 3
                    print("PICKING UP ITEM")
                    self.picked_up_slot = slot





                elif self.item_in_hand == None and type == "consume" and content[slot]["item"].__dict__["consumable"]:
                    content[slot]["amount"] -= 1

                    if content[slot]["amount"] == 0:

                        self.picked_up_slot = slot
                    self.hand_tick = 3
                    if content[slot]["item"].__dict__["name"] == "Sentry Turret":
                        pos_player = player_actor.get_pos()

                        turret_bullets = player_actor.__dict__["turret_bullets"]
                        turr = objects.Turret.Turret(pos_player,8,10,500,20,500*turret_bullets)
                        turret_list.append(turr)
                        if "turrets" not in packet_dict:
                            packet_dict["turrets"] = []
                        packet_dict["turrets"].append(turr)
                        turret_pickup.play()
                    elif content[slot]["item"].__dict__["name"] == "Barricade":
                        pos_player = player_actor.get_pos()
                        player_actor.__dict__["barricade_in_hand"] = objects.Barricade.Barricade(pos_player,pygame)
                        turret_pickup.play()
                    else:
                        player_actor.set_sanity(content[slot]["item"].__dict__["sanity_buff"], add= True)
                        drug_use.play()




            else:
                if content[slot]["item"].__dict__["max_stack"] != 1:
                    text = prompt.render(str(content[slot]["amount"]), False, [255,255,255])
                    t_s = text.get_rect().size
                    alpha_surf =  pygame.Surface(t_s).convert()
                    alpha_surf.fill((0,0,0))
                    alpha_surf.set_alpha(200)
                    screen.blit(alpha_surf, [pos[0]+ 25 - t_s[0], pos[1]+25 - t_s[1]])

                    screen.blit(text,[pos[0]+ 25  - t_s[0], pos[1]+25  - t_s[1]])

        if self.picked_up_slot != None:
            del content[self.picked_up_slot]
            print("DELETED ITEM")



    def draw_inventory(self, screen, x_d, y_d, mouse_pos, clicked,player_pos, r_click_tick, player_actor):

        if clicked and self.click == False and self.inventory_open:
            inv_click.play()
            self.click = True
        elif clicked == False:
            self.click = False



        if self.inventory_open:
            screen.blit(inv_image,[15+x_d,150+y_d])
            text = terminal2.render("INVENTORY", False, [255,255,255])
            screen.blit(text, (32+x_d, 161+y_d)) #

            default_pos = [-10,160]

            if self.hand_tick != 0 and clicked == False:
                self.hand_tick -= 1




            self.draw_contents(screen, x_d, y_d, self.contents, [-10,160], mouse_pos, clicked, r_click_tick, player_actor)



            if self.search_obj  != None:
                screen.blit(inv_image,[600+x_d,150+y_d])
                text = terminal2.render(self.search_obj.get_name(), False, [255,255,255])
                screen.blit(text, (617+x_d, 161+y_d)) #

                self.draw_contents(screen, x_d, y_d, self.search_obj.__dict__["contents"], [634-62,160], mouse_pos, clicked, r_click_tick, player_actor, inv_2 = True)

            if self.item_in_hand != None:
                if clicked and self.hand_tick == 0:
                    inserted = False
                    for def_pos in [[24-62,133], [542,133]]:
                        for slot in range(1,10):

                            if slot <= 3:
                                y = 1
                            elif slot <= 6:
                                y = 2
                            else:
                                y = 3

                            x = (slot-1)%3+1

                            pos = [def_pos[0] + x*62 +x_d, def_pos[1] + y*62 +y_d]

                            #pygame.draw.rect(screen,[255,0,0],[pos[0], pos[1], 62, 62],2)



                            if pos[0] < mouse_pos[0] < pos[0] + 62 and pos[1] < mouse_pos[1] < pos[1] + 62:
                                inserted = True
                                self.hand_tick = 3
                                print("SLOT:", slot, x, y)
                                if def_pos == [24-62,133]:
                                    if slot in self.contents:
                                        if self.item_in_hand["item"].get_name() == self.contents[slot]["item"].get_name():
                                            if self.contents[slot]["amount"] + self.item_in_hand["amount"] <= self.item_in_hand["item"].__dict__["max_stack"]:
                                                self.contents[slot]["amount"] += self.item_in_hand["amount"]
                                                self.item_in_hand["item"].sound().play()
                                                self.item_in_hand = None
                                                print("Combining stack")
                                            else:
                                                self.item_in_hand["amount"] -= self.item_in_hand["item"].__dict__["max_stack"] - self.contents[slot]["amount"]
                                                self.contents[slot]["amount"] = self.item_in_hand["item"].__dict__["max_stack"]
                                                self.item_in_hand["item"].sound().play()
                                                print("Combining stack")

                                        else:

                                            print("Setting item in place of another")
                                            item_1 = self.contents[slot]
                                            self.contents[slot] = self.item_in_hand
                                            self.item_in_hand = item_1
                                    else:
                                        print("Setting item in slot")
                                        self.contents[slot] = self.item_in_hand
                                        self.item_in_hand["item"].sound().play()
                                        self.item_in_hand = None

                                elif self.search_obj != None:
                                    if slot in self.search_obj.__dict__["contents"]:
                                        if self.item_in_hand["item"].get_name() == self.search_obj.__dict__["contents"][slot]["item"].get_name():
                                            self.search_obj.__dict__["contents"][slot]["amount"] += self.item_in_hand["amount"]
                                            self.item_in_hand["item"].sound().play()
                                            self.item_in_hand = None
                                        else:
                                            item_1 = self.search_obj.__dict__["contents"][slot]
                                            self.search_obj.__dict__["contents"][slot] = self.item_in_hand["amount"]
                                            self.item_in_hand = item_1
                                    else:
                                        self.search_obj.__dict__["contents"][slot] = self.item_in_hand
                                        self.item_in_hand["item"].sound().play()
                                        self.item_in_hand = None

                    if inserted == False:
                        self.interctables_reference.append(Interactable(player_pos, self, type = "item", item = items[self.item_in_hand["item"].__dict__["name"]].copy(), amount = self.item_in_hand["amount"]))
                        self.item_in_hand = None





                else:

                    self.item_in_hand["item"].render(screen, mouse_pos, mouse_pos, clicked, r_click_tick)
                    text = prompt.render(str(self.item_in_hand["amount"]), False, [255,255,255])
                    t_s = text.get_rect().size
                    alpha_surf =  pygame.Surface(t_s).convert()
                    alpha_surf.fill((0,0,0))
                    alpha_surf.set_alpha(200)
                    screen.blit(alpha_surf, [mouse_pos[0]+ 25 - t_s[0], mouse_pos[1]+25 - t_s[1]])

                    screen.blit(text,[mouse_pos[0]+ 25  - t_s[0], mouse_pos[1]+25  - t_s[1]])









class Interactable:
    def __init__(self, pos, player_inventory, list = [], name = "Box", type = "crate", item = None, amount = 1, collide = False, map = None):
        self.pos = pos
        self.button_prompt = ""

        self.alive = True



        self.type = type
        if self.type == "crate":
            self.name = name
            self.image =  pygame.transform.scale(pygame.image.load("texture/box.png"), [40,40]).convert()
        elif self.type == "item":
            self.lifetime = 3000
            self.pos = [self.pos[0] + random.randint(-35,35), self.pos[1] + random.randint(-35,35)]
            self.name = item.__dict__["name"]
            self.item = item
            self.amount = amount
            self.image = pygame.transform.scale(pygame.image.load("texture/items/" + self.item.__dict__["im"]), [20,20]).convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.inflate_ip(4,4)
            if items[self.name].drop_weight < 0.6:
                self.prompt_color = RED_COLOR
            elif items[self.name].drop_weight < 1.5:
                self.prompt_color = PURPLE_COLOR
            elif items[self.name].drop_weight < 3.5:
                self.prompt_color = CYAN_COLOR
            else:
                self.prompt_color = WHITE_COLOR

        self.center_pos = [self.pos[0] + self.image.get_rect().center[0], self.pos[1] + self.image.get_rect().center[1]]
        self.inv_save = player_inventory
        self.contents = {}

        if self.type == "crate":
            while True:

                drop = random.uniform(0, drop_index)
                keys = drop_table.keys()
                key_prox = {drop - key: [drop_table[key], key] for key in keys if drop - key >= 0}

                item, key = key_prox[min(key_prox.keys())]
                self.contents[random.randint(1,9)] =  {"amount": random.randint(1,items[item].__dict__["drop_stack"]), "item": items[item], "token" : str(random.uniform(0,1))}
                if random.randint(1,2) == 1:
                    break




        if collide:

            rect = self.image.get_rect().size
            map.append_polygon([self.pos[0], self.pos[1],rect[0], rect[1]])

    def tick_prompt(self, screen, player_pos, camera_pos, f_press = False):
        if self.button_prompt:
            self.button_prompt.tick(screen, player_pos, camera_pos, f_press)

    def prompt_dist(self, player_pos):
        if self.button_prompt:
            return los.get_dist_points(player_pos, self.center_pos)
        else:
            return False

    def get_name(self):
        return self.name



    def tick(self, screen, player_pos, camera_pos):

        if self.type == "item":
            self.rect.topleft = func.minus_list(self.pos,camera_pos)
            if self.lifetime % 18 < 9:
                pygame.draw.rect(screen, self.prompt_color, self.rect, 1+round(self.lifetime%18/5))
            self.lifetime -= 1

            if self.lifetime == 0:
                self.alive = False



        screen.blit(self.image, func.minus_list(self.pos,camera_pos))


        if los.get_dist_points(player_pos, self.center_pos) < 100:
            self.button_prompt = button_prompt(self, self.inv_save)

        else:
            self.inv_save.try_deleting_self(self, player_pos)



    def interact(self):
        if self.type == "crate":
            self.inv_save.set_search(self)
            self.inv_save.toggle_inv(True)
        elif self.type == "item":
            cond = self.inv_save.append_to_inv(self.item, self.amount)
            if cond == 0:
                self.alive = False
            else:
                self.amount = cond








    def get_pos(self, center = False):
        return self.center_pos if center else self.pos

    def kill_bp(self):
        self.button_prompt = ""


class button_prompt:
    def __init__(self, object, player_inventory):

        self.object = object
        if self.object.__dict__["type"] == "crate":
            self.text_render = prompt.render("F to search", False, [255,255,255])
            if self.object.__dict__["contents"] == {}:
                self.text_render2 = prompt.render(self.object.__dict__["name"] + " (Empty)", False, [255,255,255])
            else:
                self.text_render2 = prompt.render(self.object.__dict__["name"], False, [255,255,255])
        else:
            self.text_render2 = prompt.render(self.object.__dict__["name"] + " (" + str(self.object.__dict__["amount"]) + ")", False, [255,255,255])

            if player_inventory.append_to_inv(self.object, self.object.__dict__["amount"], scan_only = True) != self.object.__dict__["amount"]:

                self.text_render = prompt.render("F to pick up", False, [255,255,255])

            else:

                self.text_render = prompt.render("NO ROOM IN INVENTORY", False, [255,0,0])

        self.rect = self.text_render.get_rect().center
        self.rect2 = self.text_render2.get_rect().center

    def tick(self, screen, player_pos, camera_pos, f_press):

        self.pos = self.object.get_pos(center = True)

        pos = [(self.pos[0] + player_pos[0])/2, (self.pos[1] + player_pos[1])/2]

        screen.blit(self.text_render2, func.minus_list(func.minus_list(pos,self.rect2),camera_pos))
        screen.blit(self.text_render, func.minus(func.minus_list(func.minus_list(pos,self.rect),camera_pos),[0,20]))
        pressed = pygame.key.get_pressed()


        if f_press:
            self.object.interact()
            self.object.kill_bp()

        if los.get_dist_points(self.pos, player_pos) > 100:
            self.object.kill_bp()




class kill_count_render:
    def __init__(self,kills, rgb_list):
        mid = 854/2
        start_x = mid - kills*50/2
        self.x_poses = []
        self.images = rgb_list
        self.lifetime = 0
        self.max_lifetime = 45
        for x in range(kills):
            self.x_poses.append(start_x)

            start_x += 50

    def tick(self, screen, cam_delta, kill_counter):

        if len(self.x_poses) >= 10:
            if self.lifetime <= self.max_lifetime/6:
                y = 400 + 1/((self.lifetime+1)**1.5)*200
            elif self.max_lifetime/6 < self.lifetime <= 4*self.max_lifetime/6:
                y = 400
            else:
                y = 400 + 1/((self.max_lifetime+3 - self.lifetime)**1.2)*(200)


            func.rgb_render(self.images, min([len(self.x_poses),30])  , [854/2-50,y], cam_delta, screen)


            func.rgb_render(kill_counter_texts[len(self.x_poses)], min([len(self.x_poses),30])  , [854/2,y], cam_delta, screen)





        else:

            for x in self.x_poses:
                if self.lifetime <= self.max_lifetime/6:
                    y = 400 + 1/((self.lifetime+1)**1.5)*200
                elif self.max_lifetime/6 < self.lifetime <= 4*self.max_lifetime/6:
                    y = 400
                else:
                    y = 400 + 1/((self.max_lifetime+3 - self.lifetime)**1.2)*(200)




                func.rgb_render(self.images, min([len(self.x_poses),7])  , [x,y], cam_delta, screen)
        self.lifetime += 1
        if self.lifetime >= self.max_lifetime:
            del kill_counter













class Particle:
    def __init__(self,pos, pre_defined_angle = False,angle = 0, magnitude = 1,type = "normal", screen = screen, dont_copy = False, color_override = "red"):
        self.__pos = pos
        self.__type = type
        self.fire_x_vel = random.randint(-1,1)
        if pre_defined_angle == False:
            self.__direction = math.radians(random.randint(0,360))
        else:
            self.__direction = math.radians(angle)


        if ultraviolence:
            if dont_copy == False:
                for i in range(4):
                    particle_list.append(Particle(pos, pre_defined_angle = pre_defined_angle,angle = angle, magnitude = magnitude,type = type, screen = screen, dont_copy = True))


            self.__lifetime = round(random.randint(3,10) * magnitude*random.uniform(1,1.3))

            self.max_life = 10 * magnitude * 1.3

            self.__magnitude = round(magnitude*3* random.uniform(1,1.3))

        else:
            self.__lifetime = round(random.randint(3,10) * magnitude)
            self.__magnitude = round(magnitude*3)
            self.max_life = 10 * magnitude

        self.__color2 = [random.randint(0,50),random.randint(155,255),random.randint(235,255)]
        self.color_override = color_override
        if self.color_override == "red":
            self.__color3 = [random.randint(200,220),random.randint(0,50),random.randint(0,50)]
        elif self.color_override == "yellow":
            self.__color3 = [random.randint(200,220), random.randint(200,220), random.randint(0,50)]
        self.draw_surface = screen

    def tick(self,screen,camera_pos, map = None):

        if self.__lifetime > 0:

            if self.__type == "fire":
                self.fire_x_vel += random.uniform(-0.5,0.7)
                self.__pos = [self.__pos[0] + self.fire_x_vel, self.__pos[1] - random.randint(1,4)]
                self.__color = [255,round(255*(self.__lifetime/(self.max_life+5))), round(255*((self.__lifetime/(self.max_life+5))**2))]
                self.__dim = [self.__pos[0]-round(self.__lifetime/2), self.__pos[1]-round(self.__lifetime/2), 2*self.__lifetime/3,2*self.__lifetime/3]
            else:
                self.__pos = [self.__pos[0] + math.sin(self.__direction + random.uniform(-0.5,0.5))*self.__lifetime + random.randint(-2,2) , self.__pos[1] + math.cos(self.__direction + random.uniform(-0.3,0.3))*self.__lifetime + random.randint(-2,2)]



            if self.__type == "normal":
                self.__dim = [self.__pos[0]-round(self.__lifetime/2), self.__pos[1]-round(self.__lifetime/2), self.__lifetime/2,self.__lifetime/2]
                self.__color = [255,255 - 255/self.__lifetime ,0]


            elif self.__type == "death_particle":
                self.__dim = [self.__pos[0]-round(self.__lifetime), self.__pos[1]-round(self.__lifetime), self.__lifetime*2,self.__lifetime*2]
                self.__color = [self.__color2[0],self.__color2[1], self.__color2[2]]

            elif self.__type == "blood_particle":

                self.__dim = [self.__pos[0]-round(self.__lifetime), self.__pos[1]-round(self.__lifetime), self.__lifetime*2,self.__lifetime*2]
                if self.color_override == "red":
                    self.__color = [self.__color3[0]/((2+self.__lifetime)**0.4),self.__color3[1]/self.__lifetime, self.__color3[2]/self.__lifetime]
                elif self.color_override == "yellow":
                    self.__color = [self.__color3[0]/((2+self.__lifetime)**0.4),self.__color3[1]/((2+self.__lifetime)**0.4), self.__color3[2]/self.__lifetime]
                if map != None:
                    if list(classtest.getcollisionspoint(map.rectangles, self.__pos)) != []:
                        print("PARTICLE IN WALL, KILLING")
                        particle_list.remove(self)
                        return


            elif self.__type == "item_particle":
                self.__dim = [self.__pos[0]-round(self.__lifetime/2), self.__pos[1]-round(self.__lifetime/2), self.__lifetime,self.__lifetime]
                self.__color = [255 - 255/self.__lifetime ** 7 ,255 - 255/self.__lifetime **0.2 ,255 - 255/self.__lifetime**0.2]

            pos = func.draw_pos([self.__dim[0],self.__dim[1]],camera_pos)
            pos.append(self.__dim[2])
            pos.append(self.__dim[3])
            pygame.draw.rect(self.draw_surface, self.__color , pos)
            self.__lifetime -= 1
        else:
            particle_list.remove(self)



def player_hit_detection(pos, lastpos, player, damage):

    if player.get_hp() <= 0:
        return False

    player_pos = player.get_pos()

    points_1 = [[player_pos[0], player_pos[1] -25], [player_pos[0], player_pos[1] + 25]]
    points_2 = [[player_pos[0]-25, player_pos[1]], [player_pos[0]+25, player_pos[1]]]

    if los.intersect(pos, lastpos, points_1[0], points_1[1]) or los.intersect(pos, lastpos, points_2[0], points_2[1]):
        player.set_hp(damage, reduce = True)
        func.list_play(pl_hit)
        return True


    return False





class Player:
    def __init__(self, name,  turret_bullets = 1):
        self.pos = [0,0]
        self.name = name
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

    def set_pos(self,pos):
        self.pos = pos

    def set_angle(self, angle):
        self.angle = angle

    def set_aim_at(self,angle):
        self.aim_angle = angle

    def get_angle(self):
        return self.angle

    def knockback(self,amount,angle, daemon_bullet = False):

        self.knockback_tick = round(amount)
        self.knockback_angle = angle


    def get_pos(self):
        return self.pos

    def get_hp(self):
        return self.hp

    def get_sanity_change(self):
        if self.sanity_change != None:
            amount = self.sanity_change
            if self.sanity_change_tick != 0:
                self.sanity_change_tick -= 1
            else:
                self.sanity_change = None
            return amount, self.sanity_change_tick
        return False, 0


    def set_sanity(self, amount, add= False):
        if add:

            self.sanity += amount
            self.sanity_change = amount
            self.sanity_change_tick = 90


        else:

            self.sanity -= amount

        if self.sanity > 100:
            self.sanity = 100
        elif self.sanity < 0:
            self.sanity = 0


    def set_hp(self, hp, reduce = False):
        if reduce:

            self.hp -= hp

        else:
            self.hp = hp





class Wall:
    def __init__(self,start,end):
        global walls
        self.__start = start
        self.__end = end
        self.__center = [(start[0] + end[0])/2,(start[1] + end[1])/2]



    def get_center(self):
        return self.__center

    def get_points(self):
        return self.__start, self.__end




class Burn:
    def __init__(self, pos, magnitude, lifetime):
        self.pos = pos
        self.magnitude = magnitude
        self.life_max = lifetime
        self.lifetime = lifetime

    def tick(self, screen, map_render = None):

        if self.lifetime <= 0:
            burn_list.remove(self)
            return

        for x in range(1):
            particle_list.append(Particle([self.pos[0]+random.randint(-4,4)*2,self.pos[1]+random.randint(-4,4)*2], type = "fire", magnitude = (self.magnitude * (self.lifetime/self.life_max)**0.7),screen = screen))

        if map_render != None and self.lifetime / self.life_max > random.randint(0, 2):
            random_angle = random.randint(0, 360)
            dist = random.randint(0,1000)**0.5

            #size = 4*dist/(1000**0.5)

            pos = [self.pos[0] + math.cos(random_angle)*dist, self.pos[1] + math.sin(random_angle)*dist]

            pygame.draw.rect(map_render,[0,0,0],[pos[0], pos[1],random.randint(1,7),random.randint(1,7)])

        self.lifetime -= timedelta.mod(1)
