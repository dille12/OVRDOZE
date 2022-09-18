import func
from values import *
import get_preferences
from button import Button

player_name, draw_los, a, a, ultraviolence, a, a = get_preferences.pref()

surf_back = pygame.Surface(size)
surf_back.fill([0, 0, 0])
surf_back.set_alpha(180)

terminal = pygame.font.Font("texture/terminal.ttf", 20)
terminal2 = pygame.font.Font("texture/terminal.ttf", 30)
terminal3 = pygame.font.Font("texture/terminal.ttf", 10)


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


def advance(arg):
    dialogue[0].linenumber += 1
    dialogue[0].letternumber = 0


shop_quit_button = Button(
    [7 * size[0] / 8, 7 * size[1] / 8],
    "Exit",
    advance,
    None,
    gameInstance=pygame,
    glitchInstance=None,
)
shop_buy_button = Button(
    [3 * size[0] / 8, 7 * size[1] / 8],
    "BUY",
    purchase_weapon,
    None,
    gameInstance=pygame,
    glitchInstance=None,
)


def open_shop(screen, click, mouse_pos, player_inventory, items, player_actor):
    screen.blit(surf_back, [0, 0])

    text = terminal2.render("RUPERTS WEAPON SHOP", False, [255, 255, 255])
    screen.blit(text, [20, 20])

    text = terminal.render("In stock:", False, [255, 255, 255])
    screen.blit(text, [20, 70])

    text = terminal2.render(f"Money : {player_actor.money}$", False, [255, 255, 255])
    screen.blit(text, [20, 400])

    shop_quit_button.tick(screen, mouse_pos, click, None)

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
            ["n", "And take that monstrosity of a\nrobot with you."],
        ],
    ]
}


class Dialogue:
    def __init__(self, name):
        self.name = name
        self.dialogue = func.pick_random_from_list(dialogues[name])
        self.linenumber = 0
        self.letternumber = 0
        self.y_pos_abs = 0
        self.y_pos = 0

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
    ):
        return_str = ""
        line = self.dialogue[self.linenumber]

        if isinstance(line, list):
            if line[0] == "n":
                talker = self.name
            else:
                talker = "You"
            return_str = [talker, line[1][: self.letternumber]]

            if self.letternumber < len(line[1]):

                self.letternumber += 1

                func.list_play(typing)

            if click:
                advance(None)

        else:

            if scroll[0] and self.y_pos_abs > 0:
                self.y_pos_abs -= 1

            elif scroll[1] and self.y_pos_abs < len(ruperts_shop_selections) - 3:
                self.y_pos_abs += 1
            line(screen, click, mouse_pos, player_inventory, items, player_actor)

        if self.linenumber >= len(self.dialogue):
            pygame_instance.pygame.mouse.set_visible(False)
            dialogue.clear()

        delta = (self.y_pos_abs - self.y_pos) * 0.2

        if abs(delta) < 0.02:
            self.y_pos = self.y_pos_abs
        else:

            self.y_pos += delta

        return return_str
