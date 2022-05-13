import socket
from _thread import *
import sys
import traceback

import network_parser

players = {}

running = True

stop_threads = False
map_index = 0
game_stage = "lobby"

def threaded_client(conn):
    global players, running, stop_threads, game_stage, map_index

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

            if reply[:6] == "PACKET":

                players_info, bullets, grenades = network_parser.parse_packet(reply)

                name, x1, y1, angle, hp = players_info[0]

                players[conn]["x"] = x1
                players[conn]["y"] = y1
                players[conn]["a"] = angle
                players[conn]["hp"] = hp
                for x in bullets:
                    xp, yp, ang, dam, speed = x

                    print("BULLET FIRED BY:", players[conn]["username"])

                    for connection in players:
                        if players[connection]["username"] == players[conn]["username"]:
                            continue
                        players[connection]["bullets"].append([xp, yp, ang, dam, speed])
                        print("BULLET APPENDED TO",players[connection]["username"] )
                for x in grenades:
                    for connection in players:
                        if connection == conn:
                            continue
                        players[connection]["grenades"].append(x)



                string = "PACKET\n"
                for connection in players:
                    if connection == conn:
                        continue
                    string += "PLAYER:"
                    string += players[connection]["username"] + "_"
                    string += players[connection]["x"] + "_"
                    string += players[connection]["y"] + "_"
                    string += players[connection]["a"] + "_"
                    string += players[connection]["hp"] + "\n"


                for bullet_1 in players[conn]["bullets"]:
                    x, y, angle, damage, speed = bullet_1
                    string += "BULLET:"
                    string += x + "_"
                    string += y + "_"
                    string += angle + "_"
                    string += damage + "_"
                    string += speed + "\n"
                    players[conn]["bullets"].remove(bullet_1)

                if players[conn]["grenades"] != []:
                    string += "GRENADE:"
                    for grenade in players[conn]["grenades"]:
                        for i in grenade:
                            string += i + "_"
                        string = string[:-1] + "\n"
                    players[conn]["grenades"] = []
                string += "#END"
                conn.send(str.encode(string))

            if (reply == "un" and game_stage == "start_game") or reply == "start_game" :
                game_stage = "start_game"
                conn.send(str.encode("start_game"))


            if players[conn]["username"] == "":
                players[conn]["username"] = reply


            if game_stage == "lobby":
                if reply[:5] == "index":
                    map_index = reply.split(":")[1]

                string = "players:"
                for x in players:
                    string += players[x]["username"] + "/"
                string += "\n"
                string += "index:" + str(map_index) + "\n"
                string += "#END"
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

    print("Starting host")

    print(socket.gethostbyname(socket.gethostname()))



    #############

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    print(ip_address)
    port = 5555

    #server_ip = socket.gethostbyname(server)
    print("INITTING")
    try:
        print("Trying")
        s.bind((ip_address, port))

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
