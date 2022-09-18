import os, sys
import pygame
import math
import random
import time
import mixer
from classtest import *
from _thread import *
import threading
import server
import copy
import los
from network import Network
import ast
import network_parser
from app import App
from button import Button
from glitch import Glitch
from values import *
import classes
from classes import items
import func

# import path_finding

import armory
import objects
import enemies
import RUN
import hud_elements


def main(app):
    mouse_conversion = fs_size[0] / size[0]
    full_screen_mode = True
    full_screen = pygame.display.set_mode(fs_size, pygame.FULLSCREEN)

    map_size = [2000, 1500]

    while 1:
        clock.tick(60)
        events = app.pygame.event.get()
        mouse_pos = app.pygame.mouse.get_pos()
        mouse_pos = [mouse_pos[0] / mouse_conversion, mouse_pos[1] / mouse_conversion]
        for event in events:
            if event.type == app.pygame.QUIT:
                sys.exit()

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_ESCAPE]:
            sys.exit()

        screen.fill(BLACK)

        app.pygame.transform.scale(screen, full_screen.get_rect().size, full_screen)

        app.pygame.display.update()


if __name__ == "__main__":
    main(App(pygame, server))
