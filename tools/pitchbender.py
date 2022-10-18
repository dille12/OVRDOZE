
import librosa
import soundfile as sf

i = input()

y, sr = librosa.load(i) # y is a numpy array of the wav file, sr = sample rate
for pitch in range(1,26):
    print("Bending.")
    y_shifted = librosa.effects.pitch_shift(y, sr, n_steps=pitch)
    sf.write(f"bended/file{pitch}.wav", y_shifted, 44100, 'PCM_24')
    print(f"{pitch} done")
