import ast
import os
import sys

def write_default_settings():

    path = get_path("ovrdoze_data/settings.dat")


    with open(path, "w", encoding="UTF8") as file:
        file.write(
            "username=Default\nFOV=True\nDEV=False\nFS=True\nULTRA=False\nLASTIP=\nFPS=60\nVSYNC=False\nRES=[854, 480]\nVOL=50\nMUSIC=50")


def get_path(path):

    if getattr(sys, 'frozen', False):
        path_sub = os.path.dirname(sys.executable)

    else:
        path_sub = ""

    return os.path.join(path_sub, path)



def pref():

    path = get_path("ovrdoze_data/settings.dat")
    path2 = get_path("ovrdoze_data/")


    print(path, path2)

    if not os.path.exists(path2):
        os.mkdir(path2)
        print("ovrdoze_data created.")

    if not os.path.isfile(path):
        print("NO SETTING FILE")

        write_default_settings()
        pref()

    file = open(path, encoding="UTF8")
    lines = file.readlines()
    file.close()
    for line in lines:
        attr = line.split("=")[0]
        value = line.split("=")[1].strip("\n")
        if attr == "username":
            username = value.strip("\n")
        if attr == "FOV":
            draw_los = ast.literal_eval(value.strip("\n"))
        if attr == "DEV":
            dev = ast.literal_eval(value.strip("\n"))
        if attr == "ULTRA":
            ultraviolence = ast.literal_eval(value.strip("\n"))
        if attr == "FS":
            fs = ast.literal_eval(value.strip("\n"))
        if attr == "LASTIP":
            last_ip = value.strip("\n")
        if attr == "FPS":
            fps = value.strip("\n")
        if attr == "VSYNC":
            vsync = ast.literal_eval(value.strip("\n"))
        if attr == "RES":
            res = ast.literal_eval(value.strip("\n"))
        if attr == "VOL":
            vol = ast.literal_eval(value.strip("\n"))
        if attr == "MUSIC":
            music = ast.literal_eval(value.strip("\n"))


    return username, draw_los, dev, fs, ultraviolence, last_ip, fps, vsync, res, vol, music


def write_prefs(name, draw_los, dev, fs, ultraviolence, last_ip, fps, vsync, res, vol, music):

    path = get_path("ovrdoze_data/settings.dat")

    file = open(path, "w", encoding="UTF8")
    file.write("username=" + str(name) + "\n")
    file.write("FOV=" + str(draw_los) + "\n")
    file.write("DEV=" + str(dev) + "\n")
    file.write("FS=" + str(fs) + "\n")
    file.write("ULTRA=" + str(ultraviolence) + "\n")
    file.write("LASTIP=" + str(last_ip) + "\n")
    file.write("FPS=" + str(fps) + "\n")
    file.write("VSYNC=" + str(vsync) + "\n")
    file.write("RES=" + str(res) + "\n")
    file.write("VOL=" + str(vol) + "\n")
    file.write("MUSIC=" + str(music) + "\n")
    file.close()


    print("Settings saved")
