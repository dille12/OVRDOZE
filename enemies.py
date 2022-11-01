import os, sys
import pygame
import math
import random
import time
from unit_status import UnitStatus
pygame.init()
import func
from values import *
import level
import los
import pyperclip

width, height = size
import classes
from classes import items, drop_index, drop_table
import get_preferences
import armory

a, draw_los, a, a, ultraviolence, a, a, a, a, a, a = get_preferences.pref()

from _thread import *


terminal = pygame.font.Font("texture/terminal.ttf", 20)
terminal2 = pygame.font.Font("texture/terminal.ttf", 30)
prompt = pygame.font.Font("texture/terminal.ttf", 14)




def get_zombie_by_id(id):
    return (zomb for zomb in enemy_list if zomb.identificator == id)
