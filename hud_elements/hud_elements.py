import pygame
from core.values import *

pygame.init()
terminal = pygame.font.Font(fp("texture/terminal.ttf"), 20)


class text_box:
    def __init__(self, pos, default):
        self.pos = pos
        self.box = pygame.Rect(self.pos[0], self.pos[1], 140, 32)
        self.color_active = pygame.Color("dodgerblue2")
        self.color_inactive = pygame.Color("lightskyblue3")
        self.color = self.color_inactive
        self.font = terminal
        self.text = str(default)
        self.active = False

    def tick(self, screen, clicked, mouse_pos, events):
        if clicked:

            # If the user clicked on the input_box rect.
            if (
                self.box.collidepoint(mouse_pos)
                or pygame.key.get_pressed()[pygame.K_RETURN]
            ):
                menu_click2.play()
                # Toggle the active variable.
                self.active = not self.active
            else:
                if self.active:
                    menu_click2.play()

                self.active = False
            # Change the current color of the input box.
            self.color = self.color_active if self.active else self.color_inactive
        if self.active:
            paste_ticks = 0
            if pygame.key.get_pressed()[pygame.K_BACKSPACE]:
                self.backspace_tick += 1
                if self.backspace_tick > 30:
                    self.text = self.text[:-1]
            else:
                self.backspace_tick = 0
            for event in events:
                if event.type == pygame.KEYDOWN and self.active:
                    menu_click.play()
                    if (
                        pygame.key.get_pressed()[pygame.K_v]
                        and pygame.key.get_pressed()[pygame.K_LCTRL]
                    ):
                        self.text = pyperclip.paste()
                        print("PASTED")
                        break
                    elif event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    else:
                        self.text += event.unicode

        # Render the current text.
        txt_surface = self.font.render(self.text, False, (255, 255, 255))
        # Resize the box if the text is too long.
        width = max(200, txt_surface.get_width() + 10)
        self.box.w = width
        # Blit the text.
        screen.blit(txt_surface, (self.pos[0] + 5, self.pos[1] + 5))
        # Blit the input_box rect.
        pygame.draw.rect(screen, self.color, self.box, 2)


class Checkbox:
    def __init__(
        self,
        surface,
        x,
        y,
        color=(230, 230, 230),
        caption="",
        outline_color=(0, 0, 0),
        check_color=(0, 0, 0),
        font_size=22,
        font_color=(0, 0, 0),
        text_offset=(28, 1),
        cant_uncheck=False,
    ):
        self.surface = surface
        self.x = x
        self.y = y
        self.color = color
        self.caption = caption
        self.oc = outline_color
        self.cc = check_color
        self.fs = font_size
        self.fc = font_color
        self.to = text_offset
        self.font = pygame.font.Font(fp("texture/terminal.ttf"), 22)
        # checkbox object
        self.checkbox_obj = pygame.Rect(self.x, self.y, 30, 30)
        self.inner_rect = pygame.Rect(self.x + 8, self.y + 8, 14, 14)
        self.checkbox_outline = self.checkbox_obj.copy()
        # variables to test the different states of the checkbox
        self.checked = False
        self.active = False
        self.unchecked = True
        self.click = False
        self.single_click = False
        self.cant_uncheck = cant_uncheck

    def _draw_button_text(self):
        self.font_surf = self.font.render(self.caption, False, self.fc)
        w, h = self.font.size(self.caption)
        self.font_pos = (self.x + self.to[0], self.y + self.to[1])
        self.surface.blit(self.font_surf, self.font_pos)

    def render_checkbox(self):
        if self.checked:
            pygame.draw.rect(self.surface, self.color, self.inner_rect)

            # pygame.draw.circle(self.surface, self.cc, (self.x + 6, self.y + 6), 4)

        if self.active:
            pygame.draw.rect(self.surface, [255, 255, 255], self.checkbox_outline, 3)
        else:
            pygame.draw.rect(self.surface, [155, 155, 155], self.checkbox_outline, 3)
        self._draw_button_text()

    def _update(self, mouse_pos):
        x, y = mouse_pos
        # self.x, self.y, 12, 12
        px, py, w, h = self.checkbox_obj  # getting check box dimensions
        if px < x < px + w and py < y < py + h:
            if self.active == False:
                menu_click.play()
            self.active = True
        else:
            self.active = False

    def _mouse_up(self):
        if self.active and not self.checked and self.single_click:
            self.checked = True
            menu_click2.play()
        elif self.checked and self.cant_uncheck == False:
            self.checked = False
            self.unchecked = True
            menu_click2.play()

        if self.click is True and self.active is False:
            if self.checked:
                self.checked = True
            if self.unchecked:
                self.unchecked = True
            self.active = False

    def update_checkbox(self, event_object, mouse_pos, part_of_list=None):
        self.single_click = False
        self._update(mouse_pos)
        if event_object.type == pygame.MOUSEBUTTONDOWN and self.active:

            if self.click == False:
                self.single_click = True

            self.click = True
        else:
            self.click = False

        # self._mouse_down()
        if self.single_click:
            self._mouse_up()

        if self.checked and part_of_list != None:
            for aids in part_of_list:
                if aids == self:
                    continue
                aids.__dict__["checked"] = False

    def is_checked(self):
        return self.checked is True

    def is_unchecked(self):
        return self.checked is False
