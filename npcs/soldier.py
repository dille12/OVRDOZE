import os, sys
import pygame
import math
import random
import time
from unit_status import UnitStatus
pygame.init()
import func
from values import *
import classtest
import los
import pyperclip
import classes
from classes import items, drop_index, drop_table
import get_preferences
from armory import guns
from _thread import *


class Soldier:
    def __init__(
        self,
        app,
        pos,
        interactables,
        target_actor,
        NAV_MESH,
        walls,
    ):
        self.app = app
        self.pos = pos
        self.interactables = interactables
        self.target_actor = target_actor
        self.NAV_MESH = NAV_MESH
        self.walls = walls
        self.im = player
        self.targeting_angle = 45
        self.angle = 0
        self.aim_at = 0
        self.move_at = pos.copy()

        self.weapon = func.pick_random_from_list([guns["AK"], guns["P90"]]).copy()
