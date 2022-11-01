import socket
from _thread import *
import sys
import traceback
from values import *
import time



map_index = 0


class Server:
    def __init__(self, game):
        self.game_ref = game
        self.players = {}
        self.teams = [blue_t, red_t, green_t, yellow_t]
        self.running = True
        self.stop_threads = False
        self.hostname = socket.gethostname()
        self.ip_address = socket.gethostbyname(self.hostname)



    def threaded_client(self, conn):
        conn.send(str.encode("ok"))
        print(conn, "accepted")

        while self.running:
            try:
                data = conn.recv(2048)
                reply = data.decode("utf-8")
                if self.stop_threads:
                    break

                if self.players[conn]["username"] == "":
                    self.players[conn]["username"] = reply
                    self.players[conn]["team"] = self.teams[len(self.players) - 1]
                    self.players[conn]["team"].name = self.players[conn]["username"]
                    self.game_ref.chat.append(
                        f"Assigned player {reply} to {self.teams[len(self.players)-1].color}"
                    )

                elif reply[:6] == "PACKET":
                    #time.sleep(0.1)
                    for individual_packet in reply.split("END#"):
                        for line in individual_packet.split("\n"):
                            if line == "PACKET" or line == "/" or line == "":
                                continue
                            for x in self.players:
                                if x == conn:
                                    continue
                                self.players[x]["data"].append(line)


                    if self.players[conn]["data"] != []:

                        data = "PACKET\n"
                        for line_2 in self.players[conn]["data"]:
                            data += line_2 + "\n"
                            self.players[conn]["data"].remove(line_2)
                        data += "END#"
                    else:
                        data = "/"
                    conn.send(str.encode(data))

                elif "STARTGAME" in reply.split("/"):
                    print("STARTING GAME!")
                    for x in self.players:
                        print("Sending", self.players[x]["username"], "to game ")
                        self.players[x]["ingame"] = True
                    conn.send(str.encode("ok"))

                elif reply == self.players[conn]["username"]:
                    if self.players[conn]["ingame"]:
                        print("SENDING START GAME TO", self.players[conn]["username"])
                        conn.send(str.encode("/STARTGAME/"))
                    else:
                        rep = ""
                        for x in self.players:
                            rep += (
                                self.players[x]["username"]
                                + "-"
                                + str(self.players[x]["team"].color)
                                + "-"
                                + str(self.players[x]["team"].str_team)
                                + "/"
                            )
                        conn.send(str.encode(rep))

                elif reply == "kill":
                    conn.sendall(str.encode("/"))
                    self.running = False

                    for x in self.players:
                        x.close()
                        print(x, "closed")

                    break
                conn.sendall(str.encode("/"))
            except Exception as e:
                self.game_ref.chat.append(f"SERVER ERROR: {e}")
                self.game_ref.chat.append(traceback.print_exc())
                break
        print("Connection Closed")
        del self.players[conn]
        conn.close()

    def kill_server(self):

        self.running = False

        self.game_ref.network.connect(self.ip_address)


    def server_run(self):

        print("Starting host")
        print(socket.gethostbyname(socket.gethostname()))

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


        port = 5555

        print("INITTING")
        try:
            print("Trying")
            s.bind((self.ip_address, port))

        except socket.error as e:
            print(str(e))

        s.listen(2)
        print("Waiting for a connection")

        currentId = "0"

        while self.running:
            print("Server ticking...")
            conn, addr = s.accept()
            if not self.running:
                break
            print("SERVER: Connected to: ", addr)
            self.players[conn] = {
                "username": "",
                "team": placeholder,
                "ingame": False,
                "data": [],
            }
            print("SERVER: CREATING A THREAD TO", addr)

            start_new_thread(self.threaded_client, (conn,))
        self.stop_threads = True
        print("Server killed")
