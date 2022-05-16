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

                players_info, bullets, grenades, zombies, z_events = network_parser.parse_packet(reply)

                name, x1, y1, angle, hp = players_info[0]

                players[conn]["x"] = x1
                players[conn]["y"] = y1
                players[conn]["a"] = angle
                players[conn]["hp"] = hp

                for connection in players:
                    if connection == conn:
                        continue
                    players[connection]["bullets"] += bullets
                    players[connection]["grenades"] += grenades
                    players[connection]["zombies"] += zombies
                    players[connection]["z_events"] += z_events



                # for x in bullets:
                #     xp, yp, ang, dam, speed = x
                #     for connection in players:
                #         if players[connection]["username"] == players[conn]["username"]:
                #             continue
                #         players[connection]["bullets"].append([xp, yp, ang, dam, speed])
                #         #print("BULLET APPENDED TO",players[connection]["username"] )
                # for x in grenades:
                #     for connection in players:
                #         if connection == conn:
                #             continue
                #         players[connection]["grenades"].append(x)
                #
                # for x in zombies:
                #
                #     print("ZOMBIE SPAWNED BY:", players[conn]["username"])
                #
                #     for connection in players:
                #         if connection == conn:
                #             continue
                #         players[connection]["zombies"].append(x)
                #         print("ZOMBIE APPENDED TO",players[connection]["username"] )




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
                    string += f"BULLET:{x}_{y}_{angle}_{damage}_{speed}\n"
                    players[conn]["bullets"].remove(bullet_1)

                for grenade_1 in players[conn]["grenades"]:
                    type, x, y ,t_x, t_y = grenade_1
                    string += f"GRENADE:{type}_{x}_{y}_{t_x}_{t_y}\n"
                    players[conn]["grenades"].remove(grenade_1)

                for zombie_1 in players[conn]["zombies"]:
                    x, y, id, target_name, power, type = zombie_1
                    string += f"ZOMBIE:{x}_{y}_{id}_{target_name}_{power}_{type}\n"
                    players[conn]["zombies"].remove(zombie_1)

                for z_event in players[conn]["z_events"]:
                    id, event = z_event
                    string += f"ZEVENT:{id}_{event}\n"
                    players[conn]["z_events"].remove(z_event)

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
        players[conn] = {"username": "", "x": "0", "y": "0", "a": "0", "hp": "100", "bullets": [], "grenades": [], "zombies" : [], "z_events" : []}

        start_new_thread(threaded_client, (conn,))
    stop_threads = True
    print("Server killed")
