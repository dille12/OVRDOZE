from core.testmusic import MixInfo
import sys
import pygame

class SaveData:
    def __init__(self, beats, drops, INTENSEBEATS):
        self.beats = beats
        self.drops = drops
        self.intensebeats = INTENSEBEATS

if __name__ == "__main__":
    MInfo = MixInfo(initalSpeed=1.25)
    MInfo.startPlaying(firstTrack=False, nextup="C:\\Users\\Reset\\Documents\\GitHub\\OVRDOZE\\assets/sound/songs/So Shy.wav")
    pygame.init()
    pygame.mixer.init()
    clock = pygame.time.Clock()
    while 1:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        MInfo.handleLoop()
