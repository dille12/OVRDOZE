from _thread import *
import time
import ast
import traceback

import sys


class DataGatherer:
    def __init__(self, game):
        self.game_ref = game
        self.gathering = False
        self.data = []

    def tick(self):
        if not self.gathering:
            start_new_thread(self.threaded_data_gather, ())

    def parse(self, data):

        print("Parsing data...")

        for individual_packet in data.split("END#"):
            for line in individual_packet.split("\n"):
                if line == "PACKET" or line == "/":
                    continue
                try:
                    print(f"Evaluating line: {line}")
                    eval(line)
                    print("SUCCESS")
                except Exception as e:
                    print(f"Evaluation exception: {e}")

    def threaded_data_gather(self):
        self.gathering = True
        t = time.time()
        packet = f"PACKET\n"
        for x in self.data:
            packet += x + "\n"
            self.data.remove(x)
        packet += "END#"

        # print(f"Sending from player {self.player_team.name}\n{packet}")

        reply = self.game_ref.net.send(packet)

        if reply.strip("/ ") == "KILL":
            sys.exit()

        if reply.strip(" ") not in ["ok", "/", "/ok", "/ok/", "ok/", ""]:
            print("Received packet:\n", reply)
            self.parse(reply)
        self.game_ref.ping.append(time.time() - t)
        if len(self.game_ref.ping) > 10:
            self.game_ref.ping.remove(self.game_ref.ping[0])
        self.gathering = False
