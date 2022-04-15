import os, sys
import pygame
import math
import random
import time
from values import *
from _thread import *
from network import Network
import socket

import time
import server
import game




pygame.init()
pygame.font.init()
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

menu_status = "start"

name = "CLIENT" + str(random.randint(1,109))

terminal = pygame.font.Font('texture/terminal.ttf', 20)
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)
#print(socket.gethostbyname('DESKTOP-4KPI1C4')) # IP adress of remote computer
ip = "25.65.144.154"
port = 5555
def lobby_host(thread, ip):
    print("SERVER STARTING")
    server.server_run()


def start_mp_game(arg):
    reply = net.send("start_game")
    start_multiplayer_client()


def host_game(arg):
    print("HOSTING GAME")
    try:
        start_new_thread(lobby_host, ("1", ip) )
        return join_game(arg, True)
    except:
        return "start", None, None

def start_multiplayer_client():
    game.main(multiplayer = True, net = net, players = players, self_name = name)


def join_game(arg, host = False):
    try:
        net = Network()

        print("CLIENT: STARTING SEARCH")

        reply = net.send(name)
        if reply != [""]:



            print("CLIENT:", reply)
            print("CLIENT: CONNECTED")

            return "lobby", net, host
        else:
            print("CLIENT: No connection found")
            return "start", None, None
    except Exception as e:
        print("CLIENT: Connection failed")
        print(e)
        return "start", None, None


def main_menu(arg):
    return "start"




def quit(args):
    sys.exit()

def start_sp(arg):
    print("SP")
    game.main()

def start_mp(arg):
    return "mp_start"

def kill_server(arg):
    reply = net.send("kill")
    return "start"


host = False


class Button:
    def __init__(self, pos, text, action, args):
        self.pos = pos
        self.text = text
        self.action = action
        self.args = args

    def tick(self, screen, mouse_pos, click):
        text = terminal.render(self.text, False, [255,255,255])
        pygame.draw.rect(screen, [100,100,100], [self.pos[0], self.pos[1]-2, text.get_rect().size[0]+4 , 24])
        screen.blit(text, [self.pos[0] + 2, self.pos[1]+2])


        if self.pos[0] < mouse_pos[0] < self.pos[0]+text.get_rect().size[0]+4 and self.pos[1]-2 < mouse_pos[1] < self.pos[1]+24 and click:
            print("ACTION")
            return self.action(self.args)
        elif self.args == "2":
            return None, None
        elif self.args == "3":
            return None, None, False
button = Button([20,20], "Singleplayer", start_sp, None)
button2 = Button([20,50], "Multiplayer", start_mp, None)
button3 = Button([20,80], "Exit", quit, None)

button4 = Button([20,20], "Host", host_game, "3")
button5 = Button([20,50], "Join", join_game, "3")
button6 = Button([20,80], "Back", main_menu, None)

button7 = Button([200,100], "START GAME", start_mp_game, None)
button8 = Button([200,130], "Back", kill_server, None)

net = None

while 1:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    mouse_single_tick = False
    if pygame.mouse.get_pressed()[0] and clicked == False:
        clicked = True
        mouse_single_tick = True
    elif pygame.mouse.get_pressed()[0] == False:
        clicked = False

    mouse_pos = pygame.mouse.get_pos()
    screen.fill([0,0,0])

    if menu_status == "start":
        text = terminal.render("MAIN MENU", False, [255,255,255])
        screen.blit(text, [400,20])

        screen.blit(info, [20,150])

        s1 = button.tick(screen, mouse_pos, mouse_single_tick)
        s2= button2.tick(screen, mouse_pos, mouse_single_tick)
        button3.tick(screen, mouse_pos, mouse_single_tick)

        if s1 != None:
            menu_status = s1
            mouse_single_tick = False
        if s2 != None:
            menu_status  = s2
            mouse_single_tick = False


    if menu_status == "mp_start":



        text = terminal.render("MULTIPLAYER MENU", False, [255,255,255])
        screen.blit(text, [400,20])

        s4, net1, host = button4.tick(screen, mouse_pos, mouse_single_tick)
        s5, net2, a1  = button5.tick(screen, mouse_pos, mouse_single_tick)
        s6 = button6.tick(screen, mouse_pos, mouse_single_tick)

        if net == None and net1 != None:
            net = net1
            print("NETWORK SAVED")
        if net == None and net2 != None:
            net = net2
            print("NETWORK SAVED")



        if s4 != None:
            menu_status  = s4
            print("Game hosted")
            mouse_single_tick = False
        if s5 != None:
            menu_status  = s5
            mouse_single_tick = False
        if s6 != None:
            menu_status  = s6
            mouse_single_tick = False

    if menu_status == "lobby":
        if host:
            text = terminal.render("LOBBY (HOSTING)", False, [255,255,255])
        else:
            text = terminal.render("LOBBY", False, [255,255,255])
        screen.blit(text, [400,20])
        text = terminal.render("Players:", False, [255,255,255])

        screen.blit(text, [20,40])
        reply = net.send("un")


        if reply == "KILL":
            menu_status = "start"

        if reply == "start_game/":
            print("STARTING GAME")
            start_multiplayer_client()

        elif reply[:8] == "clients:":
            players = reply.split(":")[1]

        i = 60
        for y in players.split("/"):
            if y == "":
                continue
            i += 20
            text = terminal.render(y, False, [255,255,255])
            screen.blit(text, [30,i])
        if host:
            button7.tick(screen, mouse_pos, mouse_single_tick)
        s8 = button8.tick(screen, mouse_pos, mouse_single_tick)
        if s8 != None:
            menu_status  = s8



    text = terminal.render(ip_address, False, [255,255,255])
    screen.blit(text, [30,420])

    text = terminal.render("Joining to:" + ip, False, [255,255,255])
    screen.blit(text, [520,420])


    #print(thread.active_count())

    pygame.display.update()
