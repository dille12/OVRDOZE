import sys
import wave

def get_wav_length(file_path):
    with wave.open(file_path, 'rb') as wav_file:
        frames = wav_file.getnframes()
        rate = wav_file.getframerate()
        duration = frames / float(rate)
        return duration

try:
    droppedFile = sys.argv[1]
    print(droppedFile)
    tempo = int(input("Tempo: "))
    perSecond = 60/tempo
    length = get_wav_length(droppedFile)
    i = 0
    l = []
    while i < length:
        l.append(i)
        i += perSecond

    with open(f"{droppedFile}_timestamps.txt", "w") as f:
        f.write(str(l))

except Exception as e:
    print(e)
    input()


