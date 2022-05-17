import ast

def pref():
    file = open("settings.txt", encoding='UTF8')
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

    return username,draw_los, dev, fs, ultraviolence, last_ip


def write_prefs(name, draw_los, dev, fs, ultraviolence, last_ip):
    file = open("settings.txt", "w", encoding='UTF8')
    file.write("username=" + str(name) + "\n")
    file.write("FOV=" + str(draw_los) + "\n")
    file.write("DEV=" + str(dev) + "\n")
    file.write("FS=" + str(fs) + "\n")
    file.write("ULTRA=" + str(ultraviolence) + "\n")
    file.write("LASTIP=" + str(last_ip) + "\n")
