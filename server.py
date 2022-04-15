import socket
from _thread import *
import sys
import traceback

players = {}

running = True

stop_threads = False

game_stage = "lobby"

def threaded_client(conn):
    global players, running, stop_threads, game_stage

    conn.send(str.encode("ok"))

    while running:
        try:
            data = conn.recv(2048)
            reply = data.decode('utf-8')

            if not data:
                conn.send(str.encode("Goodbye"))
                print("Connection closing")

                break

            if stop_threads:
                break

            if reply == "kill":
                conn.sendall(str.encode("/"))
                running = False

                for x in players:
                    x.close()
                    print(x, "closed")

                break

            if reply[:4] == "pl_i":

                split = reply[5:].split(":")
                grenade_info = None
                if len(split) == 2:

                    player_info, bullet_info = split
                else:
                    player_info, bullet_info, grenade_info = split
                li = player_info.split("_")

                players[conn]["x"] = li[0]
                players[conn]["y"] = li[1]
                players[conn]["a"] = li[2]
                players[conn]["hp"] = li[3]
                bullets = bullet_info.split(",")
                for x in bullets:
                    if x.strip() == "":
                        continue
                    try:
                        xp, yp, ang, dam, speed = x.strip().split("_")
                        print("success")
                    except Exception as e:
                        print("Cant parse", x)
                        print(e)
                        continue
                    for connection in players:
                        if connection == conn:
                            continue
                        print("SERVER SAVED BULLET:", [xp, yp, ang, dam, speed], "TO",players[connection]["username"])
                        players[connection]["bullets"].append([xp, yp, ang, dam, speed])

                if grenade_info != None:
                    for connection in players:
                        if connection == conn:
                            continue
                        players[connection]["grenades"].append(grenade_info)



                string = "%"
                for connection in players:
                    if connection == conn:
                        continue
                    string += players[connection]["username"] + "_"
                    string += players[connection]["x"] + "_"
                    string += players[connection]["y"] + "_"
                    string += players[connection]["a"] + "_"
                    string += players[connection]["hp"] + "%"
                string += "#"
                if players[conn]["bullets"] != []:
                    for bullet in players[conn]["bullets"]:
                        players[conn]["bullets"].remove(bullet)
                        for i in bullet:
                            string += i + "_"
                        string = string[:-1] + "%"
                    print("BULLET STRING TO", players[conn]["username"], ":", string)

                string += "#"
                if players[conn]["grenades"] != []:
                    for grenade in players[conn]["grenades"]:

                        print(players[conn]["grenades"])
                        string += grenade + "%"
                    players[conn]["grenades"] = []
                    print("GRENADE STRING TO", players[conn]["username"], ":", string)
                conn.send(str.encode(string))

            if (reply == "un" and game_stage == "start_game") or reply == "start_game" :
                print("STARTING GAME FOR CLIENT")
                game_stage = "start_game"
                conn.send(str.encode("start_game"))


            if players[conn]["username"] == "":
                players[conn]["username"] = reply


            if game_stage == "lobby":
                if reply == "un":
                    string = "clients:"
                    for x in players:
                        string += players[x]["username"] + "/"
                    conn.send(str.encode(string))





            conn.sendall(str.encode("/"))
        except Exception as e:
            print("SERVER ERROR", e)
            print(traceback.print_exc())
            break

    print("Connection Closed")
    del players[conn]
    conn.close()

def return_players():
    return players

def server_run():

    global players, running, stop_threads



    print(socket.gethostbyname(socket.gethostname()))



    #############

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    server = "25.65.144.154"
    port = 5555

    server_ip = socket.gethostbyname(server)

    try:
        s.bind((server, port))

    except socket.error as e:
        print(str(e))

    s.listen(2)
    print("Waiting for a connection")

    currentId = "0"

    while running:
        print("Server ticking...")
        conn, addr = s.accept()
        print("SERVER: Connected to: ", addr)
        players[conn] = {}
        players[conn]["username"] = ""
        players[conn]["x"] = "0"
        players[conn]["y"] = "0"
        players[conn]["a"] = "0"
        players[conn]["hp"] = "100"
        players[conn]["bullets"] = []
        players[conn]["grenades"] = []
        start_new_thread(threaded_client, (conn,))
    stop_threads = True
    print("Server killed")
