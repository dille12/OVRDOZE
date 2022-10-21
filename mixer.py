import pygame
import time
import random
import os
from bendedsound import bendedSound




def get_Sound_All(folder):
    calm = get_Sound("calm", folder)
    hp_sound = get_Sound("lowhp", folder)
    hp_sound2 = get_Sound("lowhp2", folder)
    c1 = get_Sound("combat1", folder)
    c2 = get_Sound("combat2", folder)
    calm_e = []
    i = 1
    while True:
        try:
            name = "calm" + str(i)
            calm_e.append(get_Sound(name, folder))
            i += 1

        except:
            break
    print(len(calm_e))
    return calm, hp_sound, hp_sound2, c1, c2, calm_e

def set_music_volume(arg, volume):
    pygame.mixer.music.set_volume(volume)


def loop_over_list(list1, volume):
    for index in list1:
        if isinstance(index, pygame.mixer.Sound) or isinstance(index, bendedSound):
            index.set_volume(volume)

def loop_over_dict(dictionary, volume):
    for list_index in dictionary:
        if isinstance(dictionary[list_index], pygame.mixer.Sound) or isinstance(dictionary[list_index], bendedSound):
            dictionary[list_index].set_volume(volume)
        elif isinstance(dictionary[list_index], list):
            loop_over_list(dictionary[list_index], volume)

def set_sound_volume(global_vars, volume):
    for x in global_vars:
        if isinstance(global_vars[x], pygame.mixer.Sound) or isinstance(global_vars[x], bendedSound):
            global_vars[x].set_volume(volume)
        elif isinstance(global_vars[x], dict):
            loop_over_dict(global_vars[x], volume)
        elif isinstance(global_vars[x], list):
            loop_over_list(global_vars[x], volume)





def init(folder="random"):

    if folder == "random":
        folder = "song" + str(random.randint(1, 1))

    currently_playing = folder

    pygame.mixer.init()  # Initialize the mixer module.
    print(pygame.mixer.get_num_channels())
    with open(f"{folder}/bpm.txt", "r") as file:
        bpm = file.readline()
    time_int = 60 / (int(bpm)) * 32
    print(time_int)
    calm, hp_sound, hp_sound2, c1, c2, calm_e = get_Sound_All(folder)

    return calm, hp_sound, hp_sound2, c1, c2, calm_e, time_int, currently_playing


def main(
    combat,
    hp,
    level,
    calm,
    hp_sound,
    hp_sound2,
    c1,
    c2,
    calm_e,
    start,
    force,
    currently_playing,
    time_int,
    fade_in_time=0,
    mixing_opportunity=False,
):

    mix_in = False
    if mixing_opportunity == True and random.randint(1, 2) == 1 and False:
        print("Trying to mix")
        folder = "song" + str(random.randint(1, 4))
        if folder != currently_playing:
            print("Mixing song...")
            mix_in = True
            mix_in_song = get_Sound("mix_in", folder)
            calm.stop()
            for x in calm_e:
                x.stop()
            hp_sound.stop()
            hp_sound2.stop()
            mix_in_song.play()
            (
                calm,
                hp_sound,
                hp_sound2,
                c1,
                c2,
                calm_e,
                time_int,
                currently_playing,
            ) = init(folder)
            played = []
        else:
            print("Failed", folder)

    if mix_in == False:
        calm.stop()
        calm.play()  # Play the sound.

        played = []
        if hp == 1:
            hp_sound.stop()
            hp_sound2.play()
        if hp == 2:
            hp_sound2.stop()
            hp_sound.play()
        if combat == 1:
            c1.play()
        elif combat == 2:
            c2.play()
        if combat == 0 and start == False:
            if force == True:
                playable = random.randint(1, level)
            else:
                playable = random.randint(1, level)
            if playable > 4:
                playable = 4

            for x in calm_e:
                x.stop()

            for x in range(playable):
                index = random.randint(0, len(calm_e) - 1)
                if index not in played:
                    calm_e[index].play()
                    played.append(index)
            print("  (", len(played), ")")
            print()
    return (
        len(played),
        calm,
        hp_sound,
        hp_sound2,
        c1,
        c2,
        calm_e,
        time_int,
        currently_playing,
    )
