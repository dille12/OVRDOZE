import librosa
import time
import numpy as np
import os
from os import listdir
from os.path import isfile, join
import audioread

def beat_map(file):
    y, sr = librosa.load(file)
    onset_env = librosa.onset.onset_strength(y=y, sr=sr,
                                             aggregate=np.median)
    tempo, beats = librosa.beat.beat_track(onset_envelope=onset_env,
                                           sr=sr)
    time_stamps = librosa.frames_to_time(beats, sr=sr).tolist()

    with open(f"{file}_timestamps.txt", 'w') as f:
        f.write(str(time_stamps))

def compute(game = None, path = ""):
    print("Beginning beatmap generation.")
    mypath = os.path.abspath(os.getcwd()) + path
    print(mypath)
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f)) and f[-3:] == "wav"]
    files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    print(onlyfiles)
    for x in onlyfiles:

        if f"{x}_timestamps.txt" in files:
            print(f"Beatmap for {x} already exists.")
            continue
        if game != None:
            game.loading = f"Generating beatmap for file: {x}"
        beat_map(mypath + "/" + x)

if __name__ == '__main__':
    compute()
