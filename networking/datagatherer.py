from _thread import *
import time
import ast
import traceback
from core.values import *
import sys

from game_objects.bullet import Bullet
from weapons.area import Grenade


class DataGatherer:
    def __init__(self, game):
        self.game_ref = game
        self.gathering = False
        self.data = []

    def tick(self):
        if not self.gathering:
            start_new_thread(self.threaded_data_gather, ())

    def parse(self, data):


        for individual_packet in data.split("END#"):
            for line in individual_packet.split("\n"):
                if line == "PACKET" or line == "/" or not line:
                    continue
                try:
                    line = line.strip(" ")
                    eval(line)
                except Exception as e:
                    print(line)
                    print(f"Evaluation exception:", traceback.print_exc())

    def threaded_data_gather(self):
        self.gathering = True
        t = time.perf_counter()
        packet = f"PACKET\n"
        for x in self.data:
            packet += x + "\n"
            self.data.remove(x)

        packet += "END#"

        # print(f"Sending from player {self.player_team.name}\n{packet}")

        reply = self.game_ref.net.send(packet)

        reply = reply.replace("/", "")
        reply = reply.replace(" ", "")

        if reply.strip("/ ") == "KILL":
            sys.exit()

        if reply.strip(" ") not in ["ok", "/", "/ok", "/ok/", "ok/", ""]:
            self.parse(reply)
        self.game_ref.ping.append(time.perf_counter() - t)
        if len(self.game_ref.ping) > 10:
            self.game_ref.ping.remove(self.game_ref.ping[0])
        self.gathering = False
        self.game_ref.pos_sent = False
