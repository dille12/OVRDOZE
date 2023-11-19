import func
from values import *
import get_preferences
from button import Button
from upgrade_button import upgradeButton
from armory import upgradeMap, statMap

player_name, draw_los, a, a, ultraviolence, a, a, a, a, a, a, a = get_preferences.pref()

surf_back = pygame.Surface(size)
surf_back.fill([0, 0, 0])
surf_back.set_alpha(180)

terminal = pygame.font.Font("texture/terminal.ttf", 20)
terminal2 = pygame.font.Font("texture/terminal.ttf", 30)
terminal3 = pygame.font.Font("texture/terminal.ttf", 10)

def upgrade_backpack(arg):
    player_inventory, items, player_actor = arg
    player_actor.money -= player_inventory.columns*1000
    player_inventory.columns += 1
    dialogue[0].dialogue.append(["n", "Good choice."])
    advance(None)


def purchase_weapon(arg):
    player_inventory, items, player_actor = arg
    for x in ruperts_shop_selections:
        if x.active:
            player_weapons.append(x.weapon.copy())

            player_actor.money -= x.weapon.price

            x.active = False
            if x.weapon.ammo != "INF":

                amount = max([50, x.weapon._clip_size * 3])

                amount = min([amount, 300])

                player_inventory.append_to_inv(items[x.weapon.ammo], amount)


def upgrade_weapon(arg):
    player_inventory, items, player_actor = arg
    for x in player_actor.upgradeButtons:
        if x.active:

            w = x.weapon
            u = w.availableUpgrades[x.upgradeI]


            upgradeInstructions = upgradeMap[u]

            if "addval" in upgradeInstructions:
                w.__dict__[upgradeInstructions["stat"]] += upgradeInstructions["addval"]

            if "set" in upgradeInstructions:
                w.__dict__[upgradeInstructions["stat"]] = upgradeInstructions["set"]

                if upgradeInstructions["stat"] == "burst" and upgradeInstructions["set"] == True:
                    w.semi_auto = False

            if "multval" in upgradeInstructions:
                w.__dict__[upgradeInstructions["stat"]] *= upgradeInstructions["multval"]

            w.activatedUpgrades.append(x.upgradeI)

            w._firerate = 60 / (w._bullet_per_min / 60)

            player_inventory.remove_amount("Upgrade Token", 1)


            break






def advance(arg):
    dialogue[0].linenumber += 1
    dialogue[0].letternumber = 0
    money_tick.value = 0


shop_quit_button = Button(
    [7 * size[0] / 8, 7 * size[1] / 8],
    "Exit",
    advance,
    None,
    gameInstance=None,
    glitchInstance=None,
)
shop_buy_button = Button(
    [3 * size[0] / 8, 7 * size[1] / 8],
    "BUY",
    purchase_weapon,
    None,
    gameInstance=None,
    glitchInstance=None,
)

shop_upgrade_button = Button(
    [3 * size[0] / 8, 7 * size[1] / 8],
    "Upgrade",
    upgrade_weapon,
    None,
    gameInstance=None,
    glitchInstance=None,
)


upgrade_backpack_button = Button(
    [3 * size[0] / 8, 7 * size[1] / 8],
    "UPGRADE",
    upgrade_backpack,
    None,
    gameInstance=None,
    glitchInstance=None,
)

def refresh_player_buttons(screen, click, mouse_pos, player_inventory, items, player_actor, map):
    player_actor.upgradeButtons = []
    for i, x in enumerate(player_weapons):
        player_actor.upgradeButtons.append(upgradeButton(x, i))
    advance(None)

def give_player_money(screen, click, mouse_pos, player_inventory, items, player_actor, map):
    player_actor.money += 1000
    money_tick.value = 0
    advance(None)

def open_basement(screen, click, mouse_pos, player_inventory, items, player_actor, map):
    phone_ring.stop()
    for x in interactables:
        if x.name == "Basement":
            x.active = True
        elif x.name == "Payphone":
            x.active = False

    advance(None)


def open_upgrade_station(screen, click, mouse_pos, player_inventory, items, player_actor, map):
    screen.blit(surf_back, [0, 0])
    text = terminal2.render("UPGRADE STATION", False, [255, 255, 255])
    screen.blit(text, [20, 20])
    dialogue[0].max_y_pos = len(player_actor.upgradeButtons)
    shop_quit_button.tick(screen, mouse_pos, click, None)

    tokens = player_inventory.get_amount_of_type("Upgrade Token")

    if tokens > 0:
        shop_upgrade_button.locked = False
    else:
        shop_upgrade_button.locked = True

    text = terminal.render(f"Tokens: {tokens}", False, [255, 255, 255])
    screen.blit(text, [20, 45])


    pygame.draw.rect(screen, [255, 255, 255], [5, 100, 10, 267], 1)

    l = max(3, len(player_actor.upgradeButtons))

    scroll_bar = pygame.Rect(
        7,
        102 + 263 * dialogue[0].y_pos / l,
        6,
        263 * (3 / l),
    )

    pygame.draw.rect(screen, [255, 255, 255], scroll_bar)


    for x in player_actor.upgradeButtons:
        x.tick(screen, dialogue[0].y_pos, mouse_pos, click, player_actor)

        if x.active and not x.owned and x.upgradeI not in x.weapon.activatedUpgrades:
            shop_upgrade_button.tick(
                    screen,
                    mouse_pos,
                    click,
                    None,
                    arg=[player_inventory, items, player_actor],
                )


def open_shop_backpack(screen, click, mouse_pos, player_inventory, items, player_actor, map):
    screen.blit(surf_back, [0, 0])

    text = terminal2.render("ALANS BOOTLEG BACKPACKS", False, [255, 255, 255])
    screen.blit(text, [20, 20])

    text = terminal.render(f"Upgrade your backpack from {player_inventory.columns*3} to {(player_inventory.columns+1)*3} slots!", False, [255, 255, 255])
    screen.blit(text, [20, 70])

    text = terminal2.render(f"Cost : {player_inventory.columns*1000}$", False, [255, 255, 255])
    screen.blit(text, [20, 120])

    text = terminal2.render(f"Money : {player_actor.money}$", False, [255, 255, 255])
    screen.blit(text, [20, 340])

    x_len = text.get_size()[0]

    shop_quit_button.tick(screen, mouse_pos, click, None)

    if player_inventory.columns*1000 < player_actor.money:
        upgrade_backpack_button.tick(screen, mouse_pos, click, None, arg=[player_inventory, items, player_actor])
    # else:
    #     text = terminal2.render(f"You are missing {player_inventory.columns*1000-player_actor.money}$", False, [255, 0, 0])
    #     screen.blit(text, [40+x_len, 400])


def open_shop(screen, click, mouse_pos, player_inventory, items, player_actor, map):
    screen.blit(surf_back, [0, 0])

    text = terminal2.render("RUPERTS WEAPON SHOP", False, [255, 255, 255])
    screen.blit(text, [20, 20])

    text = terminal.render("In stock:", False, [255, 255, 255])
    screen.blit(text, [20, 70])

    text = terminal2.render(f"Money : {player_actor.money}$", False, [255, 255, 255])
    screen.blit(text, [20, 400])

    shop_quit_button.tick(screen, mouse_pos, click, None)

    dialogue[0].max_y_pos = len(ruperts_shop_selections)

    pygame.draw.rect(screen, [255, 255, 255], [5, 100, 10, 267], 1)
    scroll_bar = pygame.Rect(
        7,
        102 + 263 * dialogue[0].y_pos / len(ruperts_shop_selections),
        6,
        263 * (3 / len(ruperts_shop_selections)),
    )

    pygame.draw.rect(screen, [255, 255, 255], scroll_bar)

    for x in ruperts_shop_selections:
        x.tick(screen, dialogue[0].y_pos, mouse_pos, click)

        if x.active and not x.owned and x.weapon.price <= player_actor.money:
            shop_buy_button.tick(
                screen,
                mouse_pos,
                click,
                None,
                arg=[player_inventory, items, player_actor],
            )


dialogues = {

    "Intro" : [
        [
            ["y" , "..."],
            ["" , "You wake up in an alley with an\ninfernal headache."],
            ["y" , "Shit my head... What happened?"],
            ["" , "You find a pistol in your pocket.\nStrange, you are not allowed\nto carry a weapon."],
            ["", "At least you can now protect\nyourself from thugs and zombies."],
            ["", "You feel your other pockets too\nin search for money,\nbut no luck."],
            ["y", "Another night, huh..."]
        ]
    ],

    "Payphone" : [
        [
            open_basement,
            ["" , "You answer the phone and say\nnothing. After few moments you can\nhear an unnaturally deep voice."],
            ["Mysterious voice" , f"{player_name} I presume."],
            ["" , "You glance over your shoulder."],
            ["y", "Who is this?"],
            ["Mysterious voice" , f"Your employer of course.\nI'm afraid that we need you to\ncontribute to our cause again."],
            ["y", "Again? Who the fuck are you?"],
            ["Mysterious voice" , f"It matters not. There's a bundle\nof 1000 dollars behind the phone.\nTake it."],
            ["" , "You feel behind the cover of the\npayphone and find a stack of cash."],
            give_player_money,
            ["Mysterious voice" , f"That's the prepayment for our\ntransaction. Use it how you will."],
            ["Mysterious voice" , f"That's but a tiny fraction what\nyou will earn, if you venture to\nthat basement behind you."],
            ["Mysterious voice" , f"Massacre everything that moves.\nDo NOT die.\nYou will be compensated handsomely."],
            ["y" , f"Why me?"],
            ["" , "The voice chuckles lightly,\nand promptly hangs up."],

        ],
        [
            open_basement,
            ["Mysterious voice", f"My superiors wanted to commend you\nfor clearing the first level\nof the basement."],
            ["y" , f"You sent me to die down there!"],
            ["Mysterious voice", f"And?"],
            ["Mysterious voice", f"Your life is a constant dice\nroll of fate as it is."],
            ["Mysterious voice", f"Yet you survived. There's a small\nprize for you behind the\npayphone again."],
            give_player_money,
            ["" , "You find some money behind\nthe payphone cover again."],
            ["y" , f"Do I need to do this again?"],
            ["Mysterious voice", f"As soon as you are ready,\nhead to the next level of the\nbasement."],
            ["Mysterious voice", f"Be swift, my superiors are\nspectating your exploits."],
            ["" , "The phone clicks as the\ncaller hangs up."],

        ],
        [
            open_basement,
            ["Mysterious voice", f"You keep on suprising us."],
            ["y" , f"I need to know who\nyou guys are if you want me to\nkeep doing this shit."],
            ["Mysterious voice", f"Do you think you are in\na place to make demands?"],
            ["Mysterious voice", f"You are replaceble. You need the\nmoney but we don't need you."],
            ["y", f"You said that we have worked\ntogether before. What was\nthat about?"],
            ["Mysterious voice", f"Never demand anything from us\nagain."],
            ["Mysterious voice", f"There will be no reward\ntoday. You will hear from us."],
            ["" , "The phone slams."],
        ],
        [
            open_basement,
            ["y", "What now?"],
            ["Mysterious voice", f"You are performing\nnotably well."],
            ["y", "..."],
            give_player_money,
        ],

    ],

    "Alan" : [
        [
            ["n", "I got some backbacks here\nif you'd like."],
            open_shop_backpack,
        ],
        [
            ["n", f"Sorry {player_name},\nI cant beat that backpack\nanymore."]
        ]

    ],

    "Vagabond" : [
        [
            ["n", "Let me see those\nguns of yours."],
            refresh_player_buttons,
            open_upgrade_station,
        ],

    ],

    "Upgrade Station" : [
        [
            refresh_player_buttons,
            open_upgrade_station,
        ],

    ],


    "Rupert": [
        [
            ["n", "Gotdamn what an eyesore!\nWhich sever did ya crawl out of?"],
            ["y", "Just let me see your wares."],
            ["n", "Hope you brought money if ye wanna\nkeep that shitty life of yers."],
            open_shop,
            ["n", "Now get out of my shop!"],
        ],
        [
            ["n", "Was hopin' I'd never see\nyou again."],
            ["y", "Just shut up Rupert and show me\nyour stock."],
            ["n", "Say please or I'll paint the\nwalls red with your brains."],
            ["y", "Please."],
            open_shop,
            ["n", "Get out."],
        ],
        [
            ["n", "You again."],
            ["y", "..."],
            ["n", "Let's get this over with."],
            open_shop,
            [
                "n",
                "Where the hell are you getting\nthis money? How many cars have\nyou stolen?",
            ],
            ["y", "None of your business."],
        ],
        [
            ["n", f"Back again {player_name}?\nThought you'd be dead by now."],
            ["y", "...."],
            open_shop,
            ["n", "Get out freak."],
        ],
    ]
}


class Dialogue:
    def __init__(self, name, app, bias = None):
        self.name = name
        self.app = app
        if bias == None:
            self.dialogue = func.pick_random_from_list(dialogues[name]).copy()
        else:
            self.dialogue = dialogues[name][bias].copy()
        print("BIAS:", bias)
        print(self.dialogue)
        self.linenumber = 0
        self.letternumber = 0
        self.y_pos_abs = 0
        self.y_pos = 0
        self.max_y_pos = 0

    def main(
        self,
        screen,
        mouse_pos,
        click,
        scroll,
        glitch,
        pygame_instance,
        player_inventory,
        items,
        player_actor,
        map,
    ):
        return_str = ""
        line = self.dialogue[self.linenumber]

        if isinstance(line, list):
            if line[0] == "n":
                talker = self.name
            elif line[0] == "":
                talker = ""
            elif line[0] == "y":
                talker = "You"
            else:
                talker = line[0]
            return_str = [talker, line[1][: self.letternumber]]

            if self.letternumber < len(line[1]):

                self.letternumber += 1

                if self.letternumber % 3 == 0:

                    func.list_play(typing)

            if click:
                advance(None)

        else:

            if scroll[0] and self.y_pos_abs > 0:
                self.y_pos_abs -= 1

            elif scroll[1] and self.y_pos_abs < self.max_y_pos - 3:
                self.y_pos_abs += 1
            line(screen, click, mouse_pos, player_inventory, items, player_actor, map)

        if self.linenumber >= len(self.dialogue):
            pygame_instance.pygame.mouse.set_visible(False)
            dialogue.clear()

        delta = (self.y_pos_abs - self.y_pos) * 0.2

        if abs(delta) < 0.02:
            self.y_pos = self.y_pos_abs
        else:

            self.y_pos += delta

        return return_str
