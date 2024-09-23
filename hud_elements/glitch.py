import core.func as func


class Glitch:
    def __init__(self, screen):
        self.images = func.load_animation("anim/glitch", 1, 10)
        self.glitch_tick = 0
        self.screen = screen

    def tick(self):
        if self.glitch_tick != 0:
            self.glitch_tick -= 1
            return
            self.screen.blit(func.pick_random_from_list(self.images), (0, 0))
