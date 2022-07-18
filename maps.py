from classtest import *
from values import *
import classes

mouse_conversion = fs_size[0] / size[0]

## mouse_conversion =  1920 / 854 = 2.25
## mouse_conversion =  2560 / 854 = 2.99


## 2.25^2/2.99

# 854x480


maps = [Map("Basement Lvl. 1", "map.png", "nav_mesh_requiem.txt", [0,0], mouse_conversion, [2000,1500],
POLYGONS = 
[ #x,y,width,height
[2,470,125,186],
[377,470,125,186],
[502,376,125,561],
[501,2,125,95],
[253,1219,1122,93], #
[502,1124,123,93],
[1125,1030,124,189], #
[1125,283,125,469],
[1126,2,125,93],
[1250,375,244,94],
[1748,376,252,93],
[1624,1218,376,93]

],



OBJECTS = [
classes.Interactable([5,5], None, name = "Box"),

classes.Interactable([170,295], None, name = "Box"),

classes.Interactable([560,210], None, name = "Box"),

classes.Interactable([820,5], None, name = "Box"),

classes.Interactable([845,585], None, name = "Box"),

classes.Interactable([281,295], None, name = "Box"),

classes.Interactable([2,622], None, name = "Box"),

classes.Interactable([390,0], None, name = "Exit", type = "door", door_dest = "Overworld", active = False)

],
SPAWNPOINT = [390,40],

),


Map("Overworld", "overworld.png", "nav_mesh_overworld.txt", [0,0], mouse_conversion, [2500,2500],
POLYGONS = [ #x,y,width,height
[2, 1503, 773, 553],
[1501, 2259, 506, 239],
[952, 1503, 550, 996],
[2008, 1503, 492, 996],
[828,2, 1670, 744],
[498, 685, 330, 57],
[2, 685, 242, 57]


],

OBJECTS = [
classes.Interactable([164,30], None, name = "Rupert", type = "NPC", image = "placeholder_npc.png"),
classes.Interactable([782,1005], None, name = "Basement", type = "door", door_dest = "Basement Lvl. 1")
],
SPAWNPOINT = [781,930],
GAMMA = [0.8,0.9,1.2],
TOP_LAYER = "overworld_top.png",
NO_LOS_POLYGONS = [
[52,190,657, 78],
[503, 559, 320, 124],
[722, 389, 106, 170]


]
),

Map("Manufactory", "map2.png", "nav_mesh_manufactory.txt", [0,0], mouse_conversion, [2500,2500],
POLYGONS = [ #x,y,width,height
[467,2,156,74],
[2,312,621,155],
[476,233,147,78],
[311,781,156,783],
[311,1565, 939, 156],
[2, 2034, 465, 156],
[781, 2034, 312, 156],
[937,2193,156, 290],
[1094, 311, 625, 156],
[1094, 466, 155, 313],
[1564, 467, 157, 1096],
[1094, 1095, 470, 155],
[1720, 1407, 470, 156],
[2034, 1562, 156, 627],
[1407, 2034, 628, 155],
[2034, 2, 146, 309],
[2034, 626, 157, 311],
[2190, 781, 311, 156]
],

OBJECTS = [
classes.Interactable([5,5], None, name = "Box"),

classes.Interactable([560,210], None, name = "Box"),

classes.Interactable([210,605], None, name = "Box"),

classes.Interactable([830,700], None, name = "Box"),

classes.Interactable([770,530], None, name = "Box"),

classes.Interactable([970,5], None, name = "Box"),

classes.Interactable([5,980], None, name = "Box")
],
SPAWNPOINT = [100,100]
)
]
