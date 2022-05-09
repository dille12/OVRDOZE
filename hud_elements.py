import pygame
from values import *
pygame.init()



class Checkbox:
    def __init__(self, surface, x, y, color=(230, 230, 230), caption="", outline_color=(0, 0, 0),
            check_color=(0, 0, 0), font_size=22, font_color=(0, 0, 0), text_offset=(28, 1), cant_uncheck = False):
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
        self.font = pygame.font.Font('texture/terminal.ttf', 22)
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
        self.font_surf = self.font.render(self.caption, True, self.fc)
        w, h = self.font.size(self.caption)
        self.font_pos = (self.x+ self.to[0], self.y + self.to[1])
        self.surface.blit(self.font_surf, self.font_pos)

    def render_checkbox(self):
        if self.checked:
            pygame.draw.rect(self.surface, self.color, self.inner_rect)

            #pygame.draw.circle(self.surface, self.cc, (self.x + 6, self.y + 6), 4)



        if self.active:
            pygame.draw.rect(self.surface, [255,255,255], self.checkbox_outline, 3)
        else:
            pygame.draw.rect(self.surface, [155,155,155], self.checkbox_outline, 3)
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
            print("BUTTON CLICKED")
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

    def update_checkbox(self, event_object, mouse_pos, part_of_list = None):
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

        if self.checked:
            if part_of_list != None:
                for aids in part_of_list:
                    if aids == self:
                        continue
                    aids.__dict__["checked"] = False


    def is_checked(self):
        if self.checked is True:
            return True
        else:
            return False

    def is_unchecked(self):
        if self.checked is False:
            return True
        else:
            return False
