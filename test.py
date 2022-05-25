import sys
import os
cwd = os.getcwd();
sys.path.append(f'{cwd}/test')
from test_func import *
from test_values import *
#from test_server import *
#broken from test_run import *
from test_objects import *
#from test_network import *
from test_network_parser import *
from test_maps import *
#from test_map_generator import *
from test_los import *
from test_hud_elements import *
from test_get_preferences import *
from test_game import *
from test_enemies import *
from test_classes import *
from test_armory import *
from test_glitch import *
from test_button import *
from test_weapon import *
from test_gun import *
from test_area import *
from test_barricade import *
from test_bullet import *
from test_game_object import *
from test_turret import *
from test_menu import *