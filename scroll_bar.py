import pygame
from values import scroll_bar_clicks, menu_click2
import mixer

terminal = pygame.font.Font("texture/terminal.ttf", 20)

class ScrollBar:
    def __init__(self, name, pos, width, on_change_function, max_value=100, init_value = 75, app = None):
        self.name = name
        self.pos = pos
        self.width = width
        self.max_value = max_value
        self.on_change_function = on_change_function
        self.scroll_bar_width = 38
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.width, 30)
        self.value = init_value
        self.min_pos = self.pos[0] + self.scroll_bar_width/2+4
        self.max_pos = self.pos[0] + self.width - self.scroll_bar_width/2-4
        self.scroll_pos = 100
        self.active = False
        self.app = app
        self.step = 5

        self.get_pos()

    def get_pos(self):
        delt = self.max_pos-self.min_pos

        pos = delt*self.value*0.01

        self.scroll_pos = round((pos+self.scroll_bar_width/2+4)+self.pos[0])

    def get_value(self):

        delt = self.max_pos-self.min_pos
        self.value = round(((self.scroll_pos-self.scroll_bar_width/2-4)-self.pos[0])/delt * self.max_value)


    def tick(self, screen, mouse_pos, mouse_click, mouse_single_tick, arg = None):

        pygame.draw.rect(screen, [255,255,255], self.rect, 2)

        last_val = self.value

        if self.rect.collidepoint(mouse_pos) and mouse_click and (mouse_single_tick or self.active):
            self.scroll_pos  = mouse_pos[0]
            self.scroll_pos  = max(self.min_pos, self.scroll_pos)
            self.scroll_pos  = min(self.max_pos, self.scroll_pos)
            self.active = True

            if mouse_single_tick:
                menu_click2.play()

        elif not mouse_click:
            if self.active:
                menu_click2.play()
            self.active = False


        self.get_value()

        if self.value != last_val:
            for i in scroll_bar_clicks:
                i.stop()
            scroll_bar_clicks[round(self.value/4.16666666667)].play()
            self.on_change_function(arg, self.value/100)

        pygame.draw.rect(screen, [255,255,255] if not self.active else [255,0,0], (self.scroll_pos-self.scroll_bar_width/2, self.pos[1]+4, self.scroll_bar_width, 22), 2)

        text = terminal.render(self.name, False, [255,255,255])
        screen.blit(text, (self.pos[0], self.pos[1]-25))
        #print(self.value)
        text = terminal.render(str(self.value), False, [255,255,255] if not self.active else [255,0,0])
        x,y = text.get_rect().center
        screen.blit(text, (self.scroll_pos - x, self.pos[1]+15-y))
