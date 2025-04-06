import pygame
import numpy as np
import sounddevice as sd
from pydub import AudioSegment
from pydub.utils import get_array_type
import time
import pickle
import os
# Initialize pygame
pygame.init()


TERMINAL = pygame.font.Font("assets/texture/terminal.ttf", 20)

SONGNAME = "So Shy"

# Load audio file and set parameters
audio_file = f"assets/sound/songs/{SONGNAME}.wav"  # Replace with your audio file path
tempo = 132  # Beats per minute (can adjust this)

# Configuration
WIDTH, HEIGHT = 800, 400
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

class SaveData:
    def __init__(self, beats, drops, INTENSEBEATS):
        self.beats = beats
        self.drops = drops
        self.intensebeats = INTENSEBEATS

# Display parameters
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Waveform Scrolling Beat Mapper")

# Audio and waveform functions
def load_waveform(file_path):
    """Load audio file and return normalized waveform as numpy array."""
    audio = AudioSegment.from_file(file_path)
    bit_depth = audio.sample_width * 8
    array_type = get_array_type(bit_depth)
    raw_data = np.array(audio.get_array_of_samples(), dtype=array_type)
    num_channels = audio.channels
    # Handle stereo audio
    if num_channels == 2:
        raw_data = raw_data.reshape((-1, 2))  # Reshape to (samples, channels)
        waveform = raw_data.mean(axis=1)  # Generate mono waveform for display
    else:
        waveform = raw_data
    # Normalize waveform for display
    waveform = waveform / np.max(np.abs(waveform))
    return waveform, audio.frame_rate, num_channels, raw_data

def play_segment(audio, start_time, duration, frame_rate, num_channels, MT):
    """Play a segment of audio starting from start_time for duration seconds."""
    segment = audio[start_time * 1000 : ]
    samples = np.array(segment.get_array_of_samples(), dtype=np.float32)
    if num_channels == 2:
        samples = samples.reshape((-1, 2))  # Ensure correct shape for stereo
    else:
        samples = samples.reshape((-1, 1))  # Mono channel
    # Normalize to [-1, 1] for sounddevice
    samples /= np.max(np.abs(samples))
    sd.play(samples, samplerate=frame_rate)
    MT.stream = sd.get_stream()
    MT.timer = time.time()
    MT.playing = True
    MT.startTime = start_time
    MT.lastBeatCrossed = 0

def draw_waveform(waveform, start_sample, num_samples, color=GREEN):
    """Draw a snippet of the waveform with averaged values for each pixel column."""
    bucket_size = max(1, num_samples // WIDTH)  # Calculate the number of samples per pixel column
    midline = HEIGHT // 2

    # For each pixel column, calculate the average amplitude in the corresponding sample range
    for x in range(WIDTH):
        bucket_start = start_sample + x * bucket_size
        bucket_end = bucket_start + bucket_size
        if bucket_end <= len(waveform):
            bucket_values = np.abs(waveform[bucket_start:bucket_end])
            avg_amplitude = np.mean(bucket_values)
            # Scale the average amplitude to fit in the height of the screen
            y_top = midline - int(avg_amplitude * (HEIGHT // 2))
            y_bottom = midline + int(avg_amplitude * (HEIGHT // 2))
            pygame.draw.line(screen, color, (x, y_top), (x, y_bottom))

def draw_beats(tempo, curr_time, snippet_duration, BEATS, DROPS, MT, color=RED):
    """Draw beats only when intervals are defined in the DROPS list."""
    if len(DROPS) >= 2:
        # Initialize an empty list to store the filtered beats
        filtered_beats = []

        # Iterate over DROPS in pairs (start, end)
        for i in range(0, len(DROPS) - 1, 2):
            start_point = DROPS[i]
            end_point = DROPS[i + 1]
            # Add beats that fall within this interval
            filtered_beats += [beat for beat in BEATS if start_point <= beat <= end_point]

        # If there's an unmatched starting point, include beats from it to the end
        if len(DROPS) % 2 == 1:
            start_point = DROPS[-1]
            filtered_beats += [beat for beat in BEATS if start_point <= beat]

        drawn_beats = filtered_beats
    else:
        drawn_beats = BEATS  # Default to drawing all beats if insufficient DROPS

    MT.drawn_beats = drawn_beats

    # Draw the filtered beats
    for beat in BEATS:
        if curr_time <= beat <= curr_time + snippet_duration:
            xPos = WIDTH * (beat - curr_time) / snippet_duration
            if beat in drawn_beats:
                pygame.draw.line(screen, color, (xPos, 0), (xPos, HEIGHT))
            else:
                pygame.draw.line(screen, [150,0,0], (xPos, 100), (xPos, HEIGHT-100))



output_file = audio_file.removesuffix(".wav") + ".pkl"
waveform, sample_rate, num_channels, full_audio = load_waveform(audio_file)
song = AudioSegment.from_file(audio_file)
song_length = len(song) / 1000  # Song length in seconds



if not os.path.exists(output_file):
    # Calculate beat times
    BEATS = [x * (60 / tempo) for x in range(round(song_length // (60 / tempo)))]
    DROPS = []
    INTENSEBEATS = []
else:
    dbfile = open(output_file, 'rb')
    db = pickle.load(dbfile)    
    BEATS = db.beats
    DROPS = db.drops
    INTENSEBEATS = db.intensebeats

# Time window and sample window parameters
snippet_duration = 10  # Duration of the snippet shown in seconds
num_samples = int(sample_rate * snippet_duration)  # Number of samples in snippet

# Initialize control variables
current_time = 0  # Start time in seconds for waveform display
scroll_speed = 0.5  # Speed of scrolling when keys are pressed (seconds per key press)

# Main loop
running = True
clock = pygame.time.Clock()

def beatToTime(beat):
    return beat * 60/tempo

def timeToPixel(t):
    return ((t-current_time)/snippet_duration) * WIDTH



class MusicTimer:
    def __init__(self):
        self.playing = False
        self.timer = 0
        self.stream = None
        self.lastStream = None
        self.lastBeatCrossed = 0
        self.red = 0
        self.drawn_beats = []
    def advanceBeat(self):

        if self.lastBeatCrossed + 1 >= len(BEATS):
            return

        if self.startTime + time.time() - self.timer >= BEATS[self.lastBeatCrossed + 1]:
            self.lastBeatCrossed += 1
            if BEATS[self.lastBeatCrossed] in self.drawn_beats:
                self.red = 1
            self.advanceBeat()

        for x in INTENSEBEATS:
            bt = beatToTime(x)
            bte = beatToTime(x+1)
            t = self.startTime + time.time() - self.timer
            if bt <= t <= bte:
                self.red = 1

MT = MusicTimer()


while running:
    screen.fill([0, 0, MT.red * 200])

    # Convert current_time to the corresponding sample in the waveform
    start_sample = int(current_time * sample_rate)
    num_samples = int(sample_rate * snippet_duration)  # Number of samples in snippet
    COLLIDINGRECTDROP = None


    for x in INTENSEBEATS:
        sTime = x * 60/tempo
        eTime = (x+1) * 60/tempo
        spos = ((sTime-current_time)/snippet_duration) * WIDTH
        epos = ((eTime-current_time)/snippet_duration) * WIDTH
        pygame.draw.rect(screen, [100,100,100], [spos, 0, epos-spos, HEIGHT])

    # Draw waveform snippet and beat lines
    draw_waveform(waveform, start_sample, num_samples)
    draw_beats(tempo, current_time, snippet_duration, BEATS, DROPS, MT)


    for i, x in enumerate(DROPS):
        if not i % 2:
            dropStart = DROPS[i]

            if len(DROPS) <= i+1:
                dropEnd = song_length
            else:
                dropEnd = DROPS[i+1]

            sPos = ((dropStart-current_time)/snippet_duration) * WIDTH
            ePos = ((dropEnd-current_time)/snippet_duration) * WIDTH

            r = pygame.Rect([sPos, 0, ePos-sPos, 30])
            if r.collidepoint(pygame.mouse.get_pos()):
                COLLIDINGRECTDROP = i

            pygame.draw.rect(screen, [100,0,MT.red*150], r)

            t = TERMINAL.render("DROP", True, [255,255,255])
            screen.blit(t, r.center)

    mixInS = 0
    mixInE = 32 * 60 / tempo
    sPos = ((mixInS-current_time)/snippet_duration) * WIDTH
    ePos = ((mixInE-current_time)/snippet_duration) * WIDTH
    r = pygame.Rect([sPos, 0, ePos-sPos, 30])
    pygame.draw.rect(screen, [0, 100, MT.red*150], r)
    t = TERMINAL.render("MIX IN", True, [255,255,255])
    screen.blit(t, r.center)


    mixOutS = song_length - 32 * 60 / tempo
    mixOutE = song_length
    sPos = ((mixOutS-current_time)/snippet_duration) * WIDTH
    ePos = ((mixOutE-current_time)/snippet_duration) * WIDTH
    r = pygame.Rect([sPos, 0, ePos-sPos, 30])
    pygame.draw.rect(screen, [0, 100, MT.red*150], r)
    t = TERMINAL.render("MIX OUT", True, [255,255,255])
    screen.blit(t, r.center)


    mouse_x = pygame.mouse.get_pos()[0]
    mouse_time = current_time + (mouse_x / WIDTH) * snippet_duration

    previous_beat = mouse_time // (60 / tempo)
    mouse_beat = mouse_time / (60 / tempo)
    interval = round(4*(mouse_beat-previous_beat)) / 4

    CLOSESTBEAT = previous_beat + interval

    CBTime = CLOSESTBEAT * (60 / tempo)
    pos = timeToPixel(CBTime)
    
    pygame.draw.line(screen, [255,255,0], (pos, 0), (pos, HEIGHT))

    if MT.playing:
        t = MT.startTime + time.time() - MT.timer
        pos = ((t-current_time)/snippet_duration) * WIDTH
        pygame.draw.line(screen, WHITE, (pos, 0), (pos, HEIGHT))

        MT.advanceBeat()

        MT.red *= 0.9
        MT.red = max(0, MT.red)


    pygame.display.flip()
    clock.tick(60)  # Cap the frame rate at 30 FPS

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEWHEEL:
            # Get the mouse position and calculate the time it corresponds to
            mouse_x = pygame.mouse.get_pos()[0]
            mouse_time = current_time + (mouse_x / WIDTH) * snippet_duration

            # Adjust snippet duration
            snippet_duration += event.y  # Zoom in/out with mouse wheel
            snippet_duration = max(1, snippet_duration)

            # Update current_time so mouse_time remains constant
            current_time = mouse_time - (mouse_x / WIDTH) * snippet_duration
            current_time = max(0, min(current_time, song_length - snippet_duration))

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x = pygame.mouse.get_pos()[0]
            mouse_time = current_time + (mouse_x / WIDTH) * snippet_duration

            previous_beat = int(mouse_time // (60 / tempo))
            if previous_beat in INTENSEBEATS:
                INTENSEBEATS.remove(previous_beat)
            else:
                INTENSEBEATS.append(previous_beat)


        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:

            if COLLIDINGRECTDROP == None:

                DROPS.append(CBTime)

                DROPS.sort()

                if not len(DROPS) % 2:
                    print(DROPS)

            else:
                
                if len(DROPS) > COLLIDINGRECTDROP + 1:
                    DROPS.remove(DROPS[COLLIDINGRECTDROP+1])

                DROPS.remove(DROPS[COLLIDINGRECTDROP])

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i:  # Example: 'i' key to insert beats
                duplicate = False
                for x in BEATS:
                    if abs(x - CBTime) < 0.0005:
                        duplicate = True
                        break
                if not duplicate:
                    BEATS.append(CBTime)
                BEATS.sort()

            elif event.key == pygame.K_u:
                for x in BEATS:
                    if abs(x - CBTime) < 0.0005:
                        BEATS.remove(x)
                        break
                
                BEATS.sort()

            elif event.key == pygame.K_p:
                x = current_time + snippet_duration * (pygame.mouse.get_pos()[0] / WIDTH)
                sd.stop()
                play_segment(song, CBTime, snippet_duration, sample_rate, num_channels, MT)

            elif event.key == pygame.K_s:
                

                s = SaveData(BEATS, DROPS, INTENSEBEATS)
                with open(output_file, "bw") as f:
                    pickle.dump(s, f)
                print("Saved data")



            if event.key == pygame.K_SPACE:

                if not MT.playing:
                    play_segment(song, 0, snippet_duration, sample_rate, num_channels, MT)
                else:
                    # Toggle playback when space is pressed
                    sd.stop()
                    MT.playing = False

            

    # Handle keyboard input for panning
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:  # Scroll right
        current_time += scroll_speed
    elif keys[pygame.K_LEFT]:  # Scroll left
        current_time -= scroll_speed
    # Ensure current_time stays within bounds
    current_time = max(0, min(current_time, song_length - snippet_duration))

pygame.quit()
