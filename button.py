from values import *
import func
import pygame

class Button:
    def __init__(self, pos, text, action, args, gameInstance, glitchInstance=None, locked = False, controller = -1, click_sound = menu_click2):
        self.glitch = glitchInstance
        self.app = gameInstance
        self.pos = pos
        self.text = text
        self.terminal_button = pygame.font.Font(fp("texture/terminal.ttf"), 40)
        text_s = (
            self.terminal_button.render(self.text, False, [255, 255, 255])
            .get_rect()
            .size
        )

        self.red_tick = 10

        self.size = list(text_s)
        self.controller = controller
        self.size[1] += 8

        self.pos_tick = 0

        self.pos[0] -= text_s[0] / 2
        self.pos[1] -= text_s[1] / 2

        self.action = action
        self.args = args
        self.targeted = False
        self.anim_tick = 0
        self.target_tick = 0
        self.locked = locked
    
        self.click_sound = click_sound

    def tick(self, screen, mouse_pos, click, glitch, arg=None):
        text = self.terminal_button.render(self.text, False, [255, 255-155*(self.red_tick/10), 255-155*(self.red_tick/10)] if not self.locked else [100,100,100])

        pos_der = self.pos.copy()

        pos = [pos_der[0] - round(self.pos_tick**2.5), pos_der[1]]


        if self.pos_tick > 0:
            self.pos_tick -= 1

        if self.targeted:
            color = [255*random.uniform(0.5,1), 100, 100]
            color2 = [255, 255, 255]
        elif self.locked:
            color = [100, 100, 100]
            color2 = [66, 66, 66]
        else:
            color = [100, 100, 100]
            color2 = [133, 66, 66]
        if self.targeted:
            pygame.draw.rect(
                screen,
                color,
                [pos[0], pos[1] - 4, text.get_rect().size[0] + 8, 52],
            )

        if self.targeted:
            func.render_text_glitch(screen, self.text, [pos[0] + 2, pos[1] + 2], glitch = self.target_tick)
            if self.target_tick > 1:
                self.target_tick -= 0.5

            if random.randint(1,30) == 1:
                self.target_tick += 5
        else:
            screen.blit(text, [pos[0] + 2, pos[1] + 2])



        if self.anim_tick != 0:
            pygame.draw.rect(
                screen,
                [255, 255, 255],
                [
                    pos[0],
                    pos[1] - 10 + 52 * self.anim_tick / 8,
                    text.get_rect().size[0] + 8,
                    2,
                ],
            )

            pygame.draw.rect(
                screen,
                color2,
                [pos[0], pos[1] - 4, text.get_rect().size[0] + 8, 52],
                round(self.anim_tick**0.5),
            )

            self.anim_tick -= 1
        else:
            if self.targeted:
                self.anim_tick = 8

            pygame.draw.rect(
                screen,
                color2,
                [pos[0], pos[1] - 4, text.get_rect().size[0] + 8, 52],
                2,
            )

        CI = False
        if self.controller != -1:
            CI = self.controller in self.app.joystickEvents
            if CI:
                self.app.joystickEvents = []

        if (
            pos[0] < mouse_pos[0] < pos[0] + self.size[0] + 4
            and pos[1] - 2 < mouse_pos[1] < pos[1] + self.size[1]
            and not self.locked
        ) or CI:

            if self.targeted == False:
                self.targeted = True
                menu_click.play()
                self.target_tick = 10

            if click or CI:
                self.click_sound.stop()
                self.click_sound.play()

                GV.blockClick = True
                print("GV CHANGED!", GV.blockClick)

                if self.app:
                    for x in self.app.buttons:
                        x.pos_tick = 9

                if glitch != None:
                    glitch.glitch_tick = 5
                return self.action(arg) if arg != None else self.action(self.args)
        else:
            self.targeted = False

        if self.red_tick > 0:
            self.red_tick -= 1

        if self.args == "2":
            return None, None
        if self.args == "3":
            return None, None, False
