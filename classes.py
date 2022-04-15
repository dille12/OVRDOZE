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
width, height = size

terminal = pygame.font.Font('texture/terminal.ttf', 20)
terminal2 = pygame.font.Font('texture/terminal.ttf', 30)
prompt = pygame.font.Font('texture/terminal.ttf', 14)





class Item:
    def __init__(self, name, desc, im, max_stack = 1, pick_up_sound = None, consumable = False, sanity_buff = 0):
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

            if r_click_tick:
                return (True,"consume")

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

items = {"HE Grenade": Item("HE Grenade", "Fragmentation grenade.", "grenade.png", max_stack = 1, pick_up_sound = grenade_pickup),
        "Heroin": Item("Heroin", "Restores +40% sanity.", "heroin.png", max_stack = 1, pick_up_sound = needle_pickup, consumable = True, sanity_buff = 40),
        "Cocaine": Item("Cocaine", "Restores +20% sanity.", "coca.png", max_stack = 1, pick_up_sound = sniff_sound, consumable = True, sanity_buff = 20),
        "Diazepam": Item("Diazepam", "Restores +7.5% sanity.", "pills.png", max_stack = 1, pick_up_sound = pill_pickup, consumable = True, sanity_buff = 7.5),
        "45 ACP": Item("45 ACP", "Pistol ammo.", "45acp.png", max_stack = 40, pick_up_sound = bullet_pickup),
        "50 CAL": Item("50 CAL", "Sniper ammo.", "50cal.png", max_stack = 5, pick_up_sound = bullet_pickup),
        "9MM": Item("9MM", "Submachine gun ammo.", "9mm.png", max_stack = 25, pick_up_sound = bullet_pickup),
        "12 GAUGE": Item("12 GAUGE", "Shotgun cartridge.", "gauge.png", max_stack = 8, pick_up_sound = bullet_pickup),
        "7.62x39MM": Item("7.62x39MM", "Assault rifle ammo.", "762.png", max_stack = 30, pick_up_sound = bullet_pickup)}




class Inventory:
    def __init__(self, list, player = False):
        self.inventory_open = False
        self.contents = {1: {"item": items["45 ACP"], "amount": 999}, 2: {"item": items["50 CAL"], "amount": 999}, 3: {"item": items["7.62x39MM"], "amount": 999}, 4: {"item": items["12 GAUGE"], "amount": 999}, 5: {"item": items["9MM"], "amount": 999} ,6 : {"item": items["HE Grenade"], "amount": 999}}
        self.search_obj = None
        self.item_in_hand = None
        self.hand_tick = 0
        self.picked_up_slot = None
        self.player = player




        self.click = False

        self.interctables_reference = list

    def drop_inventory(self, pos):
        for slot in self.contents:
            print("Dropping:", self.contents[slot])
            self.interctables_reference.append(Intercatable(pos, self, type = "item", item = items[self.contents[slot]["item"].__dict__["name"]].copy(), amount = self.contents[slot]["amount"]))

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
            self.interctables_reference.append(Intercatable(player_pos, self, type = "item", item = items[self.item_in_hand["item"].__dict__["name"]].copy(), amount = self.item_in_hand["amount"]))
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
        amount = 0
        for slot in self.contents:
            if self.contents[slot]["item"].get_name() == name:
                amount += self.contents[slot]["amount"]
        return amount

    def append_to_inv(self, type, amount):
        amount_in_start = amount
        print(type.get_name(), amount)
        for slot in self.contents:
            if self.contents[slot]["item"].get_name() == type.get_name():
                if self.contents[slot]["amount"] + amount <= self.contents[slot]["item"].__dict__["max_stack"]:
                    self.contents[slot]["amount"] += amount

                    if self.player:
                        type.sound().play()

                    return True
                else:
                    amount -= self.contents[slot]["item"].__dict__["max_stack"] - self.contents[slot]["amount"]
                    self.contents[slot]["amount"] = self.contents[slot]["item"].__dict__["max_stack"]

        for slot in range(1,10):
            if slot not in self.contents:
                self.contents[slot] = {"item": type, "amount": amount}
                if self.player:
                    type.sound().play()
                return True
        if amount_in_start != amount and self.player:
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

    def draw_contents(self, screen, x_d, y_d, content, default_pos, mouse_pos, clicked, r_click_tick, player_actor):
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
                if self.item_in_hand == None and type == "pickup":
                    self.item_in_hand = content[slot]
                    self.hand_tick = 3
                    print("PICKING UP ITEM")
                    self.picked_up_slot = slot

                elif self.item_in_hand == None and type == "consume" and content[slot]["item"].__dict__["consumable"]:
                    self.picked_up_slot = slot
                    self.hand_tick = 3
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

                self.draw_contents(screen, x_d, y_d, self.search_obj.__dict__["contents"], [634-62,160], mouse_pos, clicked, r_click_tick, player_actor)

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
                        self.interctables_reference.append(Intercatable(player_pos, self, type = "item", item = items[self.item_in_hand["item"].__dict__["name"]].copy(), amount = self.item_in_hand["amount"]))
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









class Intercatable:
    def __init__(self, pos, player_inventory, list = [], name = "Box", type = "crate", item = None, amount = 1, collide = False, map = None):
        self.pos = pos
        self.button_prompt = ""

        self.alive = True



        self.type = type
        if self.type == "crate":
            self.name = name
            self.image = pygame.image.load("texture/box.png").convert()
        elif self.type == "item":
            self.lifetime = 3000
            print(self.pos)
            self.pos = [self.pos[0] + random.randint(-10,10), self.pos[1] + random.randint(-10,10)]
            print(self.pos)
            self.name = item.__dict__["name"]
            self.item = item
            self.amount = amount
            self.image = pygame.transform.scale(pygame.image.load("texture/items/" + self.item.__dict__["im"]), [20,20]).convert_alpha()

        self.center_pos = [self.pos[0] + self.image.get_rect().center[0], self.pos[1] + self.image.get_rect().center[1]]
        self.inv_save = player_inventory
        self.contents = {}

        if self.type == "crate":
            while True:
                item_1 = func.pick_random_from_dict(items).copy()
                self.contents[random.randint(1,9)] = {"amount": random.randint(1,item_1.__dict__["max_stack"]), "item": item_1,"token" : str(random.uniform(0,1))}
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
            self.lifetime -= 1

            if self.lifetime == 0:
                self.alive = False

        screen.blit(self.image, func.minus_list(self.pos,camera_pos))

        if los.get_dist_points(player_pos, self.center_pos) < 100:
            self.button_prompt = button_prompt(self)

        else:
            self.inv_save.try_deleting_self(self, player_pos)



    def interact(self):
        if self.type == "crate":
            self.inv_save.set_search(self)
            self.inv_save.toggle_inv(True)
        elif self.type == "item":
            cond = self.inv_save.append_to_inv(self.item, self.amount)
            if cond == True:
                self.alive = False
            elif cond != None:
                self.amount = cond








    def get_pos(self, center = False):
        if center:
            return self.center_pos
        return self.pos

    def kill_bp(self):
        self.button_prompt = ""


class button_prompt:
    def __init__(self, object):

        self.object = object
        if self.object.__dict__["type"] == "crate":
            self.text_render = prompt.render("F to search", False, [255,255,255])
            if self.object.__dict__["contents"] == {}:
                self.text_render2 = prompt.render(self.object.__dict__["name"] + " (Empty)", False, [255,255,255])
            else:
                self.text_render2 = prompt.render(self.object.__dict__["name"], False, [255,255,255])
        else:
            self.text_render2 = prompt.render(self.object.__dict__["name"] + " (" + str(self.object.__dict__["amount"]) + ")", False, [255,255,255])
            self.text_render = prompt.render("F to pick up", False, [255,255,255])
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
        for x in range(kills):
            self.x_poses.append(start_x)

            start_x += 50

    def tick(self, screen, cam_delta, kill_counter):
        for x in self.x_poses:
            if self.lifetime <= 20:
                y = 400 + 1/((self.lifetime+1)**1.5)*200
            elif 20 < self.lifetime <= 100:
                y = 400
            else:
                y = 400 + 1/((123 - self.lifetime)**1.2)*(200)




            func.rgb_render(self.images, len(self.x_poses)  , [x,y], cam_delta, screen)
        self.lifetime += 1
        if self.lifetime <= 120:
            del kill_counter







class Grenade:
    def __init__(self, pos, target_pos):
        self.pos = pos
        self.angle_rad = math.atan2(target_pos[1] - pos[1], target_pos[0] - pos[0])
        self.velocity = los.get_dist_points(pos,target_pos) / 30

        self.target_pos = target_pos

        self.lifetime = 120
        self.angle = random.randint(0,360)
        self.direction = func.pick_random_from_list([-1,1])
        self.height = 0
        self.angular_velocity = self.velocity
        self.vert_vel = 5
        print("GRENADE INIT")

    def get_string(self):
        string = str(round(self.pos[0])) + "_" + str(round(self.pos[1])) + "_"+ str(round(self.target_pos[0])) + "_"+ str(round(self.target_pos[1]))
        return string


    def tick(self,screen, player_pos, camera_pos, grenade_list, explosions, expl1, map, walls):
        self.last_pos = self.pos.copy()
        self.pos = [self.pos[0] + math.cos(self.angle_rad) * self.velocity, self.pos[1] + math.sin(self.angle_rad) *self.velocity - self.vert_vel ]

        coll_pos, vert_coll, hor_coll = map.check_collision(self.pos.copy(), collision_box = 5, dir_coll = True)
        if coll_pos:
            print("HIT")
            if vert_coll:
                self.angle_rad = math.pi - self.angle_rad

            elif hor_coll:
                self.angle_rad = 2*math.pi - self.angle_rad
                self.vert_vel = 0
            self.pos = coll_pos
            self.velocity = self.velocity * 0.5



        if abs(self.velocity) > 0.25:
            self.vert_vel -= 0.2
            self.height += self.vert_vel
            self.angle += self.direction * self.angular_velocity
        st_i, st_rect = func.rot_center(grenade, self.angle, self.pos[0], self.pos[1])
        if los.check_los(player_pos, self.pos, walls):
            screen.blit(st_i, func.minus_list(st_rect[:2],camera_pos))

        if self.height < 0 and abs(self.velocity) > 0.25:
            func.list_play(thuds)
            self.velocity = self.velocity * 0.5
            self.vert_vel = self.vert_vel*(-0.4)
            self.height = 0
            self.direction *= -1
            self.angular_velocity *= random.uniform(0.7,1.4)
        # else:
        #     self.velocity = 0
        #     self.vert_vel = 0
        self.lifetime -= 1
        if self.lifetime == 0:
            grenade_list.remove(self)
            explosions.append(Explosion(self.pos, expl1, player_nade = True))






class Explosion:
    def __init__(self,pos,expl1, player_nade = False):
        self.pos = pos
        self.rect_cent = [100,100]
        self.ticks = 0
        self.images = expl1
        self.player = player_nade

    def damage_actor(self, actor, camera_pos, enemy = False, enemy_list = [], blood_surf = screen, multi_kill = 0, multi_kill_ticks = 0, walls = []):
        dist = func.get_dist_points(actor.get_pos(), self.pos)
        if dist < 200:
            if los.check_los(self.pos, actor.get_pos(), walls) == False:
                if self.player:
                    return multi_kill, multi_kill_ticks
                return

            angle = math.atan2(actor.get_pos()[1] - self.pos[1] , actor.get_pos()[0] - self.pos[0] )
            actor.set_hp(round(200-dist), reduce = True)
            try:
                actor.knockback(round((200-dist)/10), angle)
            except:
                pass
            if enemy and actor.get_hp() < 0:
                if self.player:
                    multi_kill += 1
                    multi_kill_ticks = 120
                actor.kill(camera_pos, enemy_list, blood_surf)

        if self.player:
            return multi_kill, multi_kill_ticks





    def tick(self,screen, player_actor, enemy_list ,map_render,camera_pos,explosions, multi_kill, multi_kill_ticks, walls):
        if self.ticks == 0:



            func.list_play(explosion_sound)

            st_i, st_rect = func.rot_center(func.pick_random_from_list(stains), random.randint(0,360), self.pos[0], self.pos[1])
            self.damage_actor(player_actor, camera_pos, walls = walls)
            for x in enemy_list:
                multi_kill, multi_kill_ticks = self.damage_actor(x, camera_pos, enemy = True, enemy_list = enemy_list, blood_surf = map_render, multi_kill = multi_kill, multi_kill_ticks = multi_kill_ticks, walls = walls)





            map_render.blit(st_i, st_rect) #func.minus_list(self.pos,stains[0].get_rect().center)
            for aids in range(50):
                particle_list.append(Particle(self.pos, magnitude = 3, screen = screen))
        screen.blit(self.images[self.ticks], func.minus_list(func.minus_list(self.pos,camera_pos),self.rect_cent))
        self.ticks += 1

        if self.ticks == len(self.images):
            explosions.remove(self)
        return multi_kill, multi_kill_ticks





class Particle:
    def __init__(self,pos, pre_defined_angle = False,angle = 0, magnitude = 1,type = "normal", screen = screen):
        self.__pos = pos
        self.__type = type
        if pre_defined_angle == False:
            self.__direction = math.radians(random.randint(0,360))
        else:
            self.__direction = math.radians(angle)

        self.__lifetime = round(random.randint(3,10) * magnitude)
        self.__magnitude = round(magnitude*3)
        self.__color2 = [random.randint(0,50),random.randint(155,255),random.randint(235,255)]
        self.__color3 = [random.randint(200,220),random.randint(0,50),random.randint(0,50)]
        self.draw_surface = screen

    def tick(self,screen,camera_pos):

        if self.__lifetime > 0:

            self.__pos = [self.__pos[0] + math.sin(self.__direction + random.uniform(-0.5,0.5))*self.__lifetime + random.randint(-2,2) , self.__pos[1] + math.cos(self.__direction + random.uniform(-0.3,0.3))*self.__lifetime + random.randint(-2,2)]
            if self.__type == "normal":
                self.__dim = [self.__pos[0]-round(self.__lifetime/2), self.__pos[1]-round(self.__lifetime/2), self.__lifetime/2,self.__lifetime/2]
                self.__color = [255,255 - 255/self.__lifetime ,0]


            elif self.__type == "death_particle":
                self.__dim = [self.__pos[0]-round(self.__lifetime), self.__pos[1]-round(self.__lifetime), self.__lifetime*2,self.__lifetime*2]
                self.__color = [self.__color2[0],self.__color2[1], self.__color2[2]]

            elif self.__type == "blood_particle":
                self.__dim = [self.__pos[0]-round(self.__lifetime), self.__pos[1]-round(self.__lifetime), self.__lifetime*2,self.__lifetime*2]
                self.__color = [self.__color3[0]/((2+self.__lifetime)**0.4),self.__color3[1]/self.__lifetime, self.__color3[2]/self.__lifetime]


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

class Weapon:
    def __init__(self,name,clip_s,fire_r,spread,spread_r,reload_r,damage, bullets_at_once = 1, shotgun = False, spread_per_bullet = 1, semi_auto = False, bullet_speed = 20, ammo_cap_lvlup = 5, ammo = "9MM", image = "", enemy_weapon = False, sounds = {"fire": weapon_fire_Sounds, "reload": reload}):
        self.__clip_size = clip_s
        self.__bullets_in_clip = 0
        self.__bullet_per_min = fire_r
        self.__firerate = tick_count/(fire_r/60)

        self.spread_per_bullet = spread_per_bullet

        self.__name = name
        self.__spread = spread
        self.__spread_recovery = spread_r
        self.__reload_rate = reload_r
        self.__damage = damage
        self.__orig_fr = fire_r
        self.semi_auto = semi_auto
        self.semi_auto_click = False
        self.__doubledamage_time = 0
        self.__bullets_at_once = bullets_at_once
        self.__shotgun = shotgun
        self.__ammo_cap_lvlup = ammo_cap_lvlup
        self.bullet_speed = bullet_speed
        self.__c_bullet_spread = 0
        self.__reload_tick = 0
        self.__weapon_fire_Tick = 0
        self.enemy_weapon = enemy_weapon
        self.sounds = sounds["fire"]
        self.reload_sound = sounds["reload"]
        self.image_dir = image
        self.ammo = ammo
        if enemy_weapon:
            self.team = "hostile"
        else:
            self.team = "friendly"

        if image != "":

            self.picture = func.colorize(pygame.image.load("texture/guns/" + image),pygame.Color(255,255,255))
            print("Image loaded")

    def add_to_spread(self, amount):
        self.__c_bullet_spread += amount


    def copy(self):
        return Weapon(self.__name, clip_s = self.__clip_size,
        fire_r = self.__bullet_per_min,
        spread = self.__spread,
        spread_r = self.__spread_recovery,
        spread_per_bullet = self.spread_per_bullet,
        reload_r = self.__reload_rate,
        damage = self.__damage,
        bullets_at_once = self.__bullets_at_once,
        sounds = {"fire": self.sounds, "reload": self.reload_sound},
        bullet_speed = self.bullet_speed,
        shotgun = self.__shotgun,
        ammo_cap_lvlup = self.__ammo_cap_lvlup,
        image = self.image_dir,
        semi_auto = self.semi_auto,
        ammo = self.ammo)




    def set_hostile(self):
        self.team = "hostile"

    def get_image(self):
        return self.picture

    def get_semi_auto(self):
        return self.semi_auto


    def fire(self,bullet_pos,angle, screen):

        radian_angle = math.radians(angle) - 0.16184 + math.pi/2

        c = 198.59507*0.36919315403/1.875

        x_offset = math.sin(radian_angle)*c
        y_offset = math.cos(radian_angle)*c
        bul_pos = [bullet_pos[0]+x_offset,bullet_pos[1]+y_offset]
        if self.__doubledamage_time == True:
            multiplier = 2
        else:
            multiplier = 1
        func.list_play(self.sounds)
        for x in range(self.__bullets_at_once):



            if self.__bullets_in_clip > 0:
                bullet_list.append(Bullet(camera_pos, bul_pos,angle+random.uniform(-self.__spread-self.__c_bullet_spread,self.__spread+self.__c_bullet_spread),self.__damage * multiplier, team = self.team, speed = self.bullet_speed))   #BULLET
                for x in range(random.randint(8,16)):
                    particle_list.append(Particle(bul_pos, pre_defined_angle = True, angle = angle+90,magnitude = self.__damage**0.1- 0.5, screen = screen))

                if self.__shotgun == False:
                    self.__bullets_in_clip -= 1

            self.__c_bullet_spread += self.spread_per_bullet


        if self.__shotgun == True:
            self.__bullets_in_clip -= 1

        self.__weapon_fire_Tick += self.__firerate



    def spread_recoverial(self):
        self.__c_bullet_spread *= self.__spread_recovery

    def check_for_Fire(self,click):

        if self.semi_auto:
            if click and self.semi_auto_click == False and self.__bullets_in_clip > 0:
                self.semi_auto_click = True
                return True
            elif click == False:
                self.semi_auto_click = False
            return False

        if click == True and self.__bullets_in_clip > 0: ##FIRE
            return True
        else:
            return False

    def get_Ammo(self):
        return self.__bullets_in_clip

    def reload(self, player_inventory):

        availabe_ammo = player_inventory.get_amount_of_type(self.ammo)

        if self.__bullets_in_clip == 0:

            ammo_to_reload = self.__clip_size
        else:
            ammo_to_reload = self.__clip_size - self.__bullets_in_clip + 1

        if availabe_ammo == 0:
            return

        if ammo_to_reload < availabe_ammo:
            to_reload = ammo_to_reload
        else:
            to_reload = availabe_ammo

        self.reload_sound.play()
        self.__reload_tick = self.__reload_rate

        self.__bullets_in_clip += to_reload

        player_inventory.remove_amount(self.ammo, to_reload)



    def get_reload_rate(self):
        return self.__reload_rate

    def get_firerate(self):
        return self.__firerate

    def get_clip_size(self):
        return self.__clip_size

    def upgrade_firerate(self):
        if self.__shotgun == True:
            self.__bullets_at_once += 1
        else:
            self.__bullet_per_min += 50
            self.__firerate = 60/(self.__bullet_per_min/60)

    def reload_tick(self):
        return self.__reload_tick


    def upgrade_clip_size(self):
        self.__clip_size += self.__ammo_cap_lvlup
        if self.__shotgun == False:
            self.__clip_size += self.__bullets_at_once - 1


    def upgrade_damage(self):
        self.__damage += 0.5

    def double_damage(self, state):
        self.__doubledamage_time = state

    def weapon_tick(self):
        if self.__reload_tick != 0:
            self.__reload_tick -= 1
        if self.__weapon_fire_Tick > 0:
            self.__weapon_fire_Tick -= 1

    def weapon_fire_Tick(self):
        return self.__weapon_fire_Tick

def player_hit_detection(pos, lastpos, player, damage):
    player_pos = player.get_pos()

    points_1 = [[player_pos[0], player_pos[1] -25], [player_pos[0], player_pos[1] + 25]]
    points_2 = [[player_pos[0]-25, player_pos[1]], [player_pos[0]+25, player_pos[1]]]

    if los.intersect(pos, lastpos, points_1[0], points_1[1]) or los.intersect(pos, lastpos, points_2[0], points_2[1]):
        player.set_hp(damage, reduce = True)
        func.list_play(hit_sounds)
        return True


    return False

class Enemy:
    def __init__(self,pos, weapons, interctables):
        self.pos = pos
        self.target_pos = pos
        self.moving_speed = random.uniform(1.5,2.75)
        self.detection_range = random.randint(400,600)
        self.detection_rate = 0.05
        self.target_angle = 0
        self.detected = False



        self.knockback_tick = 0
        self.knockback_angle = 0

        self.hp = 100

        self.weapon = func.pick_random_from_dict(weapons)

        self.inventory = Inventory(interctables)
        for i in range(random.randint(2,3)):
            self.inventory.append_to_inv(items[self.weapon.__dict__["ammo"]], items[self.weapon.__dict__["ammo"]].__dict__["max_stack"])
        self.weapon.set_hostile()

        self.angle = 0

    def kill(self, camera_pos, list, draw_blood_parts):
        list.remove(self)
        func.list_play(death_sounds)
        func.list_play(kill_sounds)

        #self.inventory.drop_inventory(self.pos)

        for i in range(5):
            particle_list.append(Particle(func.minus(self.pos,camera_pos), type = "blood_particle", magnitude = 1, screen = draw_blood_parts))
        print("KILLED")


    def set_hp(self, hp, reduce = False):
        if reduce:
            self.hp -= hp
        else:
            self.hp = hp

    def get_hp(self):
        return self.hp

    def get_hitbox(self):
        return [25,25]

    def get_pos(self):
        return self.pos

    def knockback(self,amount,angle):

        self.knockback_tick = amount
        self.knockback_angle = angle





    def hit_detection(self,camera_pos, pos, lastpos, damage, enemy_list, map_render):
        points_1 = [[self.pos[0], self.pos[1] -25], [self.pos[0], self.pos[1] + 25]]
        points_2 = [[self.pos[0]-25, self.pos[1]], [self.pos[0]+25, self.pos[1]]]

        if los.intersect(pos, lastpos, points_1[0], points_1[1]) or los.intersect(pos, lastpos, points_2[0], points_2[1]):

            self.hp -= damage
            if self.hp < 0:
                self.kill(camera_pos, enemy_list, map_render)


            else:
                func.list_play(hit_sounds)

            return True
        return False

    def check_if_alive(self):
        if self.hp > 0:
            return True
        else:
            return False



    def tick(self, screen, player_actor, camera_pos, map, walls):
        self.temp_pos = func.minus_list(self.pos,camera_pos)
        player_pos = player_actor.get_pos()
        pl_temp_pos = func.minus_list(player_pos,camera_pos)

        if self.knockback_tick != 0:

            self.pos = [self.pos[0] + math.cos(self.knockback_angle) * self.knockback_tick, self.pos[1] - math.sin(self.knockback_angle) *self.knockback_tick]
            self.knockback_tick -= 1



        #pygame.draw.rect(screen, [255,255,255],[self.temp_pos[0], self.temp_pos[1], 20, 20])




        if los.check_los(player_pos, self.pos, walls):  ## Render

            rot, rect= func.rot_center(player, self.angle, self.temp_pos[0], self.temp_pos[1])
            rect = rot.get_rect().center
            screen.blit(rot, [self.temp_pos[0] - rect[0], self.temp_pos[1] - rect[1]])

            dist = los.get_dist_points(self.pos, player_pos)

            if dist < self.detection_range and player_actor.get_hp() > 0:

                if random.uniform(0,1) < (1 - dist/self.detection_range)*self.detection_rate:
                    self.detected = True

                if self.detected:
                    self.target_angle = 180 - math.degrees(math.atan2(self.pos[1] - player_pos[1], self.pos[0] - player_pos[0]))
                    if player_actor.get_hp() > 0:
                        func.weapon_fire(self.weapon, self.inventory, self.angle, self.pos, screen, ai = True)

                    if dist > 50:

                        self.target_pos = player_pos

                    else:
                        self.target_pos = self.pos

            else:
                self.detected = False

        # if player_actor.get_hp() < 0:
        #     self.target_pos = self.pos

        if self.angle != self.target_angle:

            if abs(self.target_angle - self.angle) > 1:
                self.angle = self.angle + los.get_angle_diff(self.target_angle, self.angle)*0.1
            else:
                self.angle = self.target_angle

        if self.target_pos != self.pos:

            self.angle_rad = math.pi*2 - math.atan2(self.target_pos[1] - self.pos[1], self.target_pos[0] - self.pos[0])
            self.pos = [self.pos[0] + math.cos(self.angle_rad) *self.moving_speed, self.pos[1] - math.sin(self.angle_rad) *self.moving_speed]
            coll_pos = map.check_collision(self.pos, collision_box = 10)
            if coll_pos:
                self.pos = coll_pos
            if los.get_dist_points(self.pos,self.target_pos) < 10:
                self.target_pos = self.pos

        else:
            point = map.get_random_point(None, max_tries = 1)
            if los.check_los(point, self.pos, walls):
                print("Wandering")
                self.target_angle = 180 - math.degrees(math.atan2(self.pos[1] - point[1], self.pos[0] - point[0]))

                self.target_pos = point
                print("to", self.target_pos)

class Player_Multi:
    def __init__(self, username):
        self.name = username
        self.pos = [0,0]
        self.hp = 100
        self.angle = 0
        self.player_blit = player
        self.killed = False
        self.name_text  = prompt.render(self.name,False, [255,255,255])

    def check_if_alive(self):
        if self.killed:
            return False
        else:
            return True


    def kill(self, camera_pos, dict, draw_blood_parts):

        if self.killed:
            return


        func.list_play(death_sounds)
        func.list_play(kill_sounds)
        for i in range(5):
            particle_list.append(Particle(func.minus(self.pos,camera_pos), type = "blood_particle", magnitude = 1, screen = draw_blood_parts))
        print("KILLED")
        self.killed = True

    def hit_detection(self,camera_pos, pos, lastpos, damage, actor_list, map_render):

        if self.killed == True and self.hp == 100:
            self.killed = False

        if self.hp <= 0:
            return False

        points_1 = [[self.pos[0], self.pos[1] -25], [self.pos[0], self.pos[1] + 25]]
        points_2 = [[self.pos[0]-25, self.pos[1]], [self.pos[0]+25, self.pos[1]]]

        if los.intersect(pos, lastpos, points_1[0], points_1[1]) or los.intersect(pos, lastpos, points_2[0], points_2[1]):

            if self.hp - damage < 0:
                self.kill(camera_pos, actor_list, map_render)


            else:
                func.list_play(hit_sounds)

            return True
        return False

    def tick(self, screen, player_pos,camera_pos, walls):
        if los.get_dist_points(player_pos, self.pos) > 1000 or self.hp <= 0 or los.check_los(player_pos, self.pos, walls) == False:
            return

        player_rotated, player_rotated_rect = func.rot_center(self.player_blit,self.angle,self.pos[0],self.pos[1])

        player_pos_center = player_rotated.get_rect().center
        player_pos_center = [self.pos[0]-player_pos_center[0],self.pos[1]-player_pos_center[1]]
        offset = [player_rotated_rect[0]-self.pos[0]-camera_pos[0], player_rotated_rect[1]-self.pos[1]-camera_pos[1]]
        screen.blit(player_rotated,[self.pos[0]+offset[0],self.pos[1]+offset[1]])

        #screen.blit(self.player_blit, func.minus_list(self.pos,camera_pos))

        screen.blit(self.name_text, func.minus_list(self.pos,camera_pos))

    def set_values(self, x, y, a, hp):
        self.pos = [int(x), int(y)]
        self.angle = int(a)
        self.hp = int(hp)




class Player:
    def __init__(self):
        self.pos = [0,0]
        self.hp = 100
        self.sanity = 50
        self.sanity_change = None
        self.sanity_change_tick = 0
        self.angle = 0

    def set_pos(self,pos):
        self.pos = pos

    def set_angle(self, angle):
        self.angle = angle

    def get_angle(self):
        return self.angle


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



class Bullet:
    def __init__(self, camera_pos ,pos,angle,damage, deal_damage_to_player = False, team = "hostile",speed = 20):
        self.__pos = pos.copy()

        self.__deal_damage_to_player = deal_damage_to_player

        self.speed = speed * random.uniform(0.9,1.1)

        self.im = bullet_length[round(self.speed)]

        self.team = team


        self.__angle = angle
        self.__angle_radians = math.radians(self.__angle) + math.pi/2
        self.__damage = damage
        rotated_image = pygame.transform.rotate(bullet, self.__angle)
        new_rect = rotated_image.get_rect(center = bullet.get_rect(center = self.__pos).center)

        self.__pos = [new_rect[0],new_rect[1]]

        self.lifetime = 30


    def get_string(self):
        string = str(round(self.__pos[0])) + "_" + str(round(self.__pos[1])) + "_"+ str(round(self.__angle)) + "_"+ str(round(self.__damage)) + "_"+ str(round(self.speed))
        return string
    def move_and_draw_Bullet(self,screen,camera_pos, map, enemy_list, player, draw_blood_parts = screen, dummies = {}):
        self.lifetime -= 1
        if self.lifetime == 0:
            print("Bullet deleted")
            bullet_list.remove(self)
            return



        self.__last_pos = self.__pos.copy()
        self.__pos[0] += math.sin(self.__angle_radians)*self.speed
        self.__pos[1] += math.cos(self.__angle_radians)*self.speed
        try:
            angle_coll = map.check_collision(self.__pos, return_only_collision = True, collision_box = 0)
            if angle_coll != False:
                func.list_play(rico_sounds)
                bullet_list.remove(self)
                for i in range(8):
                    particle_list.append(Particle(angle_coll, magnitude = 1, pre_defined_angle = True, angle = 90-self.__angle, screen = screen))

        except Exception as e:
            pass

        rot_bullet, rot_bullet_rect = func.rot_center(self.im,self.__angle,self.__pos[0],self.__pos[1])

        crystal_pay = False



        if self.team == "hostile":
            if player_hit_detection(self.__pos, self.__last_pos, player, self.__damage):
                for i in range(3):
                    particle_list.append(Particle(func.minus(self.__pos, camera_pos), type = "blood_particle", magnitude = 0.5, pre_defined_angle = True, screen = draw_blood_parts, angle = self.__angle + random.randint(45,135)))
                try:
                    bullet_list.remove(self)
                except:
                    pass

        if dummies != {}:
            for x in dummies:
                if dummies[x].hit_detection(camera_pos, self.__pos, self.__last_pos,self.__damage, dummies, draw_blood_parts) == True:
                    particle_list.append(Particle(func.minus(self.__pos, camera_pos), type = "blood_particle", magnitude = 0.5, pre_defined_angle = True, screen = draw_blood_parts, angle = self.__angle + random.randint(45,135)))
                    try:
                        bullet_list.remove(self)
                    except:
                        pass

                    if dummies[x].check_if_alive():
                        return False
                    else:
                        return True




        for x in enemy_list:
            if x.hit_detection(camera_pos, self.__pos, self.__last_pos,self.__damage, enemy_list, draw_blood_parts) == True:

                x.knockback(5, math.radians(self.__angle))

                try:
                    if x.check_if_alive():
                        dead = False
                        for i in range(3):
                            particle_list.append(Particle(func.minus(self.__pos, camera_pos), type = "blood_particle", magnitude = 0.5, pre_defined_angle = True, screen = draw_blood_parts, angle = self.__angle + random.randint(45,135)))
                    else:
                        dead = True

                except:
                    print("")
                try:
                    bullet_list.remove(self)
                except:
                    pass
                if dead:
                    return True
                else:
                    return False

        bullet_draw_pos = [rot_bullet_rect[0] , rot_bullet_rect[1] ]
        screen.blit(rot_bullet,func.draw_pos(self.__pos,camera_pos))
        return player_hp

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

class Turret:
    def __init__(self,pos,turning_speed,firerate,range,damage= 1,lifetime = 100):
        self.__pos = pos.copy()
        self.__turning_speed = turning_speed
        self.__firerate = firerate
        self.__angle = 0
        self.__turret_tick = firerate
        self.__range = range
        self.__lifetime = lifetime
        self.__lifetime2 =  lifetime
        self.__tick = 0
        self.__aiming_at = 0

        self.__damage = damage

    def scan_for_enemies(self,enemy_list):
        lowest = 99999
        closest_enemy = [0,0]
        for x in enemy_list:
            hb_s = x.get_hitbox()
            enemy_pos = x.get_pos()
            enemy_pos = [enemy_pos[0]  + hb_s[0] / 4,enemy_pos[1]  + hb_s[1] / 4]
            x_diff = self.__pos[0] - enemy_pos[0]
            y_diff = self.__pos[1] - enemy_pos[1]
            dist = math.sqrt(x_diff**2 + y_diff** 2)
            if dist < lowest and dist < self.__range:
                lowest = dist
                closest_enemy = enemy_pos
        return closest_enemy

    def tick(self, screen ,camera_pos,enemy_list,tick):
        if func.check_for_render(camera_pos, self.__pos):
            return
        shoot = False
        aim_at = self.scan_for_enemies(enemy_list)
        if aim_at != [0,0]:
            self.__aiming_at = func.get_angle(self.__pos,aim_at)
            shoot = True

        elif shoot == False and random.randint(1,300) == 1:
            self.__aiming_at = random.randint(0,round(360/self.__turning_speed)) * self.__turning_speed

        else:
            self.__angle = round(self.__angle/self.__turning_speed)*self.__turning_speed
            self.__aiming_at = round(self.__aiming_at/self.__turning_speed)*self.__turning_speed

        if abs((360-self.__aiming_at) - self.__angle) > self.__turning_speed * 2 -1 :
            angle2 = 360 - self.__aiming_at
            while angle2 >= 360:
                angle2 -= 360
            while angle2 < 0:
                angle2 += 360

            if angle2 - self.__angle > 180:
                angle2 -= 360

            if abs(angle2 - self.__angle) < self.__turning_speed:
                self.__angle = angle2
            else:
                if angle2 > self.__angle:
                    self.__angle += self.__turning_speed
                elif angle2 < self.__angle:
                    self.__angle -= self.__turning_speed
        else:

            angle2 = self.__angle

        turret2, turret_rect = func.rot_center(turret,self.__angle,self.__pos[0],self.__pos[1])

        if shoot == True and self.__turret_tick == 0 and abs(angle2-self.__angle) < self.__turning_speed * 2:
            turret_fire1.stop()
            turret_fire2.stop()
            turret_fire3.stop()

            pick_random_from_list(turret_fire).play()
            bullet_list.append(Bullet([self.__pos[0]+35, self.__pos[1]+35],self.__angle+random.uniform(-10,10),self.__damage))

            for x in range(random.randint(4,6)):
                particle_list.append(Particle([self.__pos[0]+35, self.__pos[1]+35], pre_defined_angle = True, angle = self.__angle+90, magnitude = 2))

            self.__lifetime -= 1

            self.__turret_tick = self.__firerate
        elif self.__turret_tick != 0 and shoot == True:
            self.__turret_tick -= 1

        rad = math.radians(360-self.__angle)

        dp = func.draw_pos(self.__pos,camera_pos)
        screen.blit(turret_leg, dp)
        screen.blit(turret2,func.draw_pos(turret_rect,camera_pos,35,35))

        if tick <= 5:
            line_width = round(3 - 2 * (tick/5) )

            pygame.draw.line(screen, [255 - 50/(tick+1),255/(tick+1),255/(tick+1)],[dp[0]+35 - math.cos(rad) * 13 , dp[1]+35 - math.sin(rad) * 13], [dp[0]+35 + math.cos(rad) * self.__range, dp[1]+35 + math.sin(rad) * self.__range], width = line_width)

        if self.__lifetime == 0:
            turret_list.remove(self)
        elif self.__lifetime/self.__lifetime2 <= 0.2:
            render_cool(huuto,[turret_rect[0]+35, turret_rect[1]+35],self.__tick,16,True)
            self.__tick += 1
