from values import *
import func

class Button:
    def __init__(self, pos, text, action, args, gameInstance, glitchInstance=None, locked = False):
        self.glitch = glitchInstance
        self.pygame = gameInstance
        self.pos = pos
        self.text = text
        self.terminal_button = self.pygame.font.Font("texture/terminal.ttf", 40)
        text_s = (
            self.terminal_button.render(self.text, False, [255, 255, 255])
            .get_rect()
            .size
        )

        self.size = list(text_s)

        self.size[1] += 8

        self.pos[0] -= text_s[0] / 2
        self.pos[1] -= text_s[1] / 2

        self.action = action
        self.args = args
        self.targeted = False
        self.anim_tick = 0
        self.target_tick = 0
        self.locked = locked

    def tick(self, screen, mouse_pos, click, glitch, arg=None):
        text = self.terminal_button.render(self.text, False, [255, 255, 255])

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
            self.pygame.draw.rect(
                screen,
                color,
                [self.pos[0], self.pos[1] - 4, text.get_rect().size[0] + 8, 52],
            )

        if self.targeted:
            func.render_text_glitch(screen, self.text, [self.pos[0] + 2, self.pos[1] + 2], glitch = self.target_tick)
            if self.target_tick > 1:
                self.target_tick -= 0.5

            if random.randint(1,30) == 1:
                self.target_tick += 5
        else:
            screen.blit(text, [self.pos[0] + 2, self.pos[1] + 2])

        if self.anim_tick != 0:
            self.pygame.draw.rect(
                screen,
                [255, 255, 255],
                [
                    self.pos[0],
                    self.pos[1] - 10 + 52 * self.anim_tick / 8,
                    text.get_rect().size[0] + 8,
                    2,
                ],
            )

            self.pygame.draw.rect(
                screen,
                color2,
                [self.pos[0], self.pos[1] - 4, text.get_rect().size[0] + 8, 52],
                round(self.anim_tick**0.5),
            )

            self.anim_tick -= 1
        else:
            if self.targeted:
                self.anim_tick = 8

            self.pygame.draw.rect(
                screen,
                color2,
                [self.pos[0], self.pos[1] - 4, text.get_rect().size[0] + 8, 52],
                2,
            )

        if (
            self.pos[0] < mouse_pos[0] < self.pos[0] + self.size[0] + 4
            and self.pos[1] - 2 < mouse_pos[1] < self.pos[1] + self.size[1]
            and not self.locked
        ):

            if self.targeted == False:
                self.targeted = True
                menu_click.play()
                self.target_tick = 10

            if click:
                menu_click2.play()
                if glitch != None:
                    glitch.glitch_tick = 5
                return self.action(arg) if arg != None else self.action(self.args)
        else:
            self.targeted = False
        if self.args == "2":
            return None, None
        if self.args == "3":
            return None, None, False
