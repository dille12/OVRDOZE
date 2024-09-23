from utilities.get_preferences import get_path
import os

def write_default_highscore():
    path = get_path("ovrdoze_data/highscore.dat")
    if os.path.isfile(path):
        return

    with open(path, "w", encoding="UTF8") as file:
        file.write(
            "{}")

def checkHighscores(app):
    path = get_path("ovrdoze_data/highscore.dat")

    with open(path, "r", encoding="UTF8") as file:
        data = file.read()
    data = eval(data)

    for i in app.levels:
        if i not in data:
            data[i] = {"NORMAL": [0, 0], "HARD": [0, 0], "ONSLAUGHT": [0, 0]}

    print(data)
    path = get_path("ovrdoze_data/highscore.dat")
    with open(path, "w", encoding="UTF8") as file:
        file.write(str(data))


    app.highscore = data

def saveHighscore(app):
    path = get_path("ovrdoze_data/highscore.dat")
    with open(path, "w", encoding="UTF8") as file:
        file.write(str(app.highscore))
