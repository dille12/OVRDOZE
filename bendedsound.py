import pygame
class bendedSound:
    def __init__(self, sound, bended_sound):
        self.sound = sound
        self.bended_sound = bended_sound
        print("Created a bended sound file")

        if not (isinstance(self.sound, pygame.mixer.Sound) and isinstance(self.bended_sound, pygame.mixer.Sound)):
            print("WARNING: NO SOUND FILE FOR:", self)
    def play(self):
        if 0 < playerhealth.health < 30:
            self.bended_sound.play()
        else:
            self.sound.play()

    def stop(self):
        self.sound.stop()
        self.bended_sound.stop()

    def set_volume(self, volume):
        self.sound.set_volume(volume)
        self.bended_sound.set_volume(volume)

    def get_num_channels(self):
        return self.sound.get_num_channels()

class PlayerHealth:
    def __init__(self):
        self.health = 100

playerhealth = PlayerHealth()
