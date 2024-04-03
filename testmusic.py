import utilities.highpassfilter
import librosa
import soundfile
import numpy as np
#utilities.highpassfilter.main("sound/songs/Octane.wav", 124, False)
import sys
import pygame
import os
import random
import time
import ast
from _thread import start_new_thread
import func
from values import fp
import get_preferences


def createMix(song1, tempo1, song2, tempo2, MInfo, output, easeCalc = 0):

    #song1 = f"sound/songs/{song1}.wav"
    #song2 = f"sound/songs/{song2}.wav"
    speedUp = MInfo.trackSpeedUp
    lastSpeedUp = MInfo.lastTrackSpeedUp
    t = time.perf_counter()
    
    tempo1 *= lastSpeedUp
    tempo2 *= speedUp

    print(f"Mixing {song1} ({tempo1:.0f}BPM) to {song2} ({tempo2:.0f}BPM)")
    print("Speed Factor:", speedUp)

    bars = 8
    print("Loading next song...")
    yOctOrig, sr = librosa.load(song2, sr=None, mono=False)

    if speedUp != 1:
        yOctOrig = utilities.highpassfilter.stretch_audio(yOctOrig, 1/speedUp)
    time.sleep(easeCalc)
    print("Chopping next song...")
    y2 = utilities.highpassfilter.getChunkOfAudio(yOctOrig, sr, tempo2, 0, bars)
    time.sleep(easeCalc)
    print("Stretching next song...")
    y_Octane = utilities.highpassfilter.gradual_stretch_audio(y2, tempo2/tempo1, 1)
    timestamp = int(bars * 4 * 60 * sr / tempo2)
    
    time.sleep(easeCalc)
    print("Applying next song...")
    yOctOrig = yOctOrig[:, timestamp:]
    yOctOrig = yOctOrig[:, :-timestamp]
    
    
    time.sleep(easeCalc)
    print("Applying highpass to next song...")
    y_Octane2 = utilities.highpassfilter.butter_highpass_filter(y_Octane, 300, sr)

    time.sleep(easeCalc)
    print("Loading current song...")
    y, sr = librosa.load(song1, sr=None, mono=False)

    if lastSpeedUp != 1:
        y = utilities.highpassfilter.stretch_audio(y, 1/lastSpeedUp)

    time.sleep(easeCalc)
    print("Chopping current song...")
    y_Narcosis = utilities.highpassfilter.getChunkOfAudio(y, sr, tempo1, 0, bars, fromEnd=True)

    
    time.sleep(easeCalc)
    y_Narcosis = utilities.highpassfilter.gradual_stretch_audio(y_Narcosis, 1, tempo1/tempo2)

    time.sleep(easeCalc)
    print("Applying lowpass to current song...")
    y_Narcosis2 = utilities.highpassfilter.butter_highpass_filter(y_Narcosis, 6000, sr, type = "low")
    
    time.sleep(easeCalc)
    print("Mixing current song...")
    y_Narcosis = utilities.highpassfilter.mix_audio_files2(y_Narcosis, y_Narcosis2, exponent = 1)
    
    time.sleep(easeCalc)
    print("Mixing next song...")
    y_Octane = utilities.highpassfilter.mix_audio_files2(y_Octane2, y_Octane, exponent = 1)
    
    time.sleep(easeCalc)
    print("Mixing songs together...")
    yTotal = utilities.highpassfilter.mix_audio_files2(y_Narcosis, y_Octane, exponent = 2, exponent2 = 5)
    #yTotal = y_Narcosis
    
    time.sleep(easeCalc)
    print("Concatenating...")
    yTotal = np.concatenate((yTotal, yOctOrig), axis=1)
   
    time.sleep(easeCalc)
    print("Writing to disk...")
    soundfile.write(get_preferences.get_path("ovrdoze_data/track1.wav") if output else get_preferences.get_path("ovrdoze_data/track2.wav"), yTotal.T, sr)
    print("Mix", "ovrdoze_data/track1.wav" if output else "ovrdoze_data/track2.wav", "created")

    timeUntilFullSwitch = y_Narcosis.shape[1] / sr
    timeOnSwitch = bars * 4 * 60 / tempo2

    print(f"Time elapsed: {time.perf_counter() - t:.4f}s")

    MInfo.lastTrackSpeedUp = speedUp

    return timeUntilFullSwitch, timeOnSwitch



pygame.mixer.init()
clock = pygame.time.Clock()

path = fp("sound/songs/")
songs = []
for file in os.listdir(path):
    if (
        file.endswith(".wav")
        and "menu_loop" not in file
        and "downtown" not in file
        and "overworld_loop" not in file
    ):
        songs.append(fp("sound/songs/" + file))

print(songs)

tempoLookUp = {
    'Lucid.wav' : 138, 
    'Narcosis.wav' : 137, 
    'Octane.wav' : 124, 
    'Palpitations.wav' : 132, 
    'Take Me High.wav' : 124, 
    'Thorn in my heart.wav' : 135, 
    'Veins.wav' : 135,
    "gamebegin.wav" : 130,
    "Call It Love.wav" : 132,
}

songDrops = {
    "Palpitations.wav" : [[29.0, 72.72], [120, 163.63]],
    "Take Me High.wav" : [[48.38, 79.35], [129.67, 160.64]],
    "FullAuto.wav" : [[36.09, 79.39], [126.31, 169.62]],
    "New colors.wav" : [[43.30, 72.18], [122.70, 151.57]],
    "Octane.wav" : [[30.96, 77.41], [104.51, 150.96]],
    "ovrdoz.wav" : [[43.82, 68.87], [102.26, 127.30]],
    "Veins.wav" : [[32, 71.11], [110.22, 159.33]],
    "Narcosis.wav" : [[28.02, 70.07], [108.61, 150.65]],
    "Thorn in my heart.wav" : [[28.44, 71.11], [97.77, 140.44]],
    "Lucid.wav" : [[27.82, 69.56], [111.30, 153.04]],
    "Call It Love.wav" : [[45.45, 74.54], [105.45, 149.09]],
}

class MixInfo:
    def __init__(self, app=False):
        self.timeUntilSwitch = 0
        self.timeOnSwitch = 0
        self.trackMade = False
        self.nextup = ""
        self.lastSong = ""
        self.output = True
        self.app = app

        self.trackSpeedUp = 1
        self.lastTrackSpeedUp = 1
        self.currentSpeedUp = 1

    def startPlaying(self):

        self.lastSong = random.choice(songs)
        #MInfo.lastSong = "sound/songs/Octane.wav"
        self.lastSong = fp("sound/sfx/gamebegin.wav")
        self.nextup = self.lastSong
        #MInfo.nextup = "sound/songs/Narcosis.wav"

        while self.lastSong == self.nextup:
            self.nextup = random.choice(songs)
        self.output = True
        self.timeUntilSwitch, self.timeOnSwitch = createMix(self.lastSong, tempoLookUp[self.lastSong.split("/")[-1]], self.nextup, tempoLookUp[self.nextup.split("/")[-1]], self, self.output)
        self.lastSong = self.nextup

        pygame.mixer.music.load(get_preferences.get_path("ovrdoze_data/track1.wav") if self.output else get_preferences.get_path("ovrdoze_data/track2.wav"))
        pygame.mixer.music.play()

        self.i = 600

        self.switchDone = False

        self.trackTimer = False
        self.DROP = False
        self.timeIntoTrack = 0
        self.dropIndices = []
        self.beat_map = []
        self.beat_index = 0

    def handleLoop(self):
        if pygame.mixer.music.get_pos() > 30*1000 and not self.trackMade:
            start_new_thread(threadedMixCreation, (self, ))


        self.ii = pygame.mixer.music.get_pos()
        if self.ii+1000 < self.i:
            self.trackMade = False
            print("Track changed!")
            self.switchDone = False


        self.i = self.ii

        if self.i/1000 >= self.timeUntilSwitch and not self.switchDone:
            print("Full Switch!")
            self.switchDone = True
            self.currentlyPlaing = self.lastSong
            self.trackTimer = time.time() - self.timeOnSwitch
            print("Time on switch:", self.timeOnSwitch)
            self.beat_index = 16
            if self.app:
                self.app.musicDisplayTick.value = 0

            with open(
                f"{self.currentlyPlaing}_timestamps.txt"
            ) as file:  # Use file to refer to the file object
                self.beat_map = ast.literal_eval(file.read())

            song = self.currentlyPlaing.split("/")[-1]
            self.dropIndices = []
            self.currentSpeedUp = self.lastTrackSpeedUp

            if song in songDrops:
                drops = songDrops[song]

                for s, e in drops:
                    self.dropIndices.append(self.beat_map.index(func.closest_value(s, self.beat_map)))



        if self.trackTimer:
            dropFound = False
            for x in songDrops[self.currentlyPlaing.split("/")[-1]]:
                if time.time() - self.trackTimer > x[0] / self.currentSpeedUp and time.time() - self.trackTimer < x[1] / self.currentSpeedUp:
                    dropFound = True
                    break

            if dropFound:
                if not self.DROP:
                    print("DROP!")
                self.DROP = True
            else:
                if self.DROP:
                    print("Drop ended")
                self.DROP = False     

            self.timeIntoTrack = (time.time() - self.trackTimer) * self.currentSpeedUp









def threadedMixCreation(MInfo):
    MInfo.trackMade = True
    MInfo.nextup = MInfo.lastSong

    while MInfo.lastSong == MInfo.nextup:
        MInfo.nextup = random.choice(songs)

    MInfo.output = not MInfo.output

    MInfo.timeUntilSwitch, MInfo.timeOnSwitch = createMix(MInfo.lastSong, tempoLookUp[MInfo.lastSong], MInfo.nextup, tempoLookUp[MInfo.nextup], MInfo, MInfo.output, easeCalc = 0.5)
    
    MInfo.lastSong = MInfo.nextup
    
    pygame.mixer.music.queue("ovrdoze_data/track1.wav" if MInfo.output else "ovrdoze_data/track2.wav")


if __name__ == "__main__":
    MInfo = MixInfo()
    MInfo.startPlaying()
    pygame.init()
    while 1:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        MInfo.handleLoop()





        

        
