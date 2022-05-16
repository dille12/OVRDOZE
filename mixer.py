import pygame
import time
import random
import os



def get_sound_Variants(folder,name2):
    list = []
    i = 1
    while True:
        try:
            name = name2 + str(i)
            list.append(get_Sound(name,folder))
            i+=1

        except:
            return list

def get_Sound_All(folder):
    calm = get_Sound("calm",folder)
    hp_sound = get_Sound("lowhp",folder)
    hp_sound2 = get_Sound("lowhp2",folder)
    c1 = get_Sound("combat1",folder)
    c2 = get_Sound("combat2",folder)
    calm_e = []
    i = 1
    while True:
        try:
            name = "calm" + str(i)
            calm_e.append(get_Sound(name,folder))
            i+=1

        except:
            break
    print(len(calm_e))
    return calm, hp_sound, hp_sound2, c1,c2, calm_e


def get_Sound(sound,file):
    path = file + "/" + sound + ".wav"
    print(path)
    return pygame.mixer.Sound(path)

def init(folder="random"):

    if folder == "random":
        folder = "song" + str(random.randint(1,1))

    currently_playing = folder

    pygame.mixer.init()  # Initialize the mixer module.
    print(pygame.mixer.get_num_channels())
    with open(f"{folder}/bpm.txt", "r") as file:
        bpm = file.readline()
    time_int = 60/(int(bpm)) *32
    print(time_int)
    calm, hp_sound, hp_sound2, c1,c2, calm_e = get_Sound_All(folder)


    return calm, hp_sound, hp_sound2, c1,c2, calm_e, time_int, currently_playing


def main(combat,hp,level,calm, hp_sound, hp_sound2, c1,c2, calm_e, start, force, currently_playing, time_int, fade_in_time = 0, mixing_opportunity = False):


    mix_in = False
    if mixing_opportunity == True and random.randint(1,2) == 1 and False:
        print("Trying to mix")
        folder = "song" + str(random.randint(1,4))
        if folder != currently_playing:
            print("Mixing song...")
            mix_in = True
            mix_in_song = get_Sound("mix_in",folder)
            calm.stop()
            for x in calm_e:
                x.stop()
            hp_sound.stop()
            hp_sound2.stop()
            mix_in_song.play()
            calm, hp_sound, hp_sound2, c1,c2, calm_e, time_int, currently_playing = init(folder)
            played = []
        else:
            print("Failed",folder)




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
                playable = random.randint(1,level)
            else:
                playable = random.randint(1,level)
            if playable > 4:
                playable = 4


            for x in calm_e:
                x.stop()


            for x in range(playable):
                index = random.randint(0,len(calm_e)-1)
                if index not in played:
                    calm_e[index].play()
                    played.append(index)
            print("  (",len(played),")")
            print()
    return len(played), calm, hp_sound, hp_sound2, c1,c2, calm_e, time_int, currently_playing
