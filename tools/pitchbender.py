import os
import librosa
import soundfile as sf

def bend25():
    i = input("file: ")
    y, sr = librosa.load(i) # y is a numpy array of the wav file, sr = sample rate
    for pitch in range(1,26):
        print("Bending.")
        y_shifted = librosa.effects.pitch_shift(y, sr, n_steps=pitch)

        sf.write(f"bended/file{pitch}.wav", y_shifted, 44100, 'PCM_24')
        print(f"{pitch} done")


def bend_all():
    Direc = input(r"Enter the path of the folder: ")
    print(f"Files in the directory: {Direc}")



    files = os.listdir(Direc)
    files = [f for f in files if os.path.isfile(Direc+'/'+f)] #Filtering only the files.
    for x in files:
        file_name = x.removesuffix(".wav")
        y, sr = librosa.load(str(Direc + "\\" + x), sr = None, mono = True)
        print("Samplerate:", sr)
        y_fast = librosa.effects.time_stretch(y, rate=0.5)

        y_fast = librosa.effects.pitch_shift(y_fast, sr = sr, n_steps=-12)

        sf.write(f"C:/Users/Reset/Documents/GitHub/OVRDOZE/bended/{file_name}_bended.wav", y_fast, sr, 'PCM_24')
        print(f"{x} done")


if __name__ == '__main__':
    bend_all()
