from classtest import *
from values import *
import classes
fs_size = 1920, 1080
mouse_conversion = fs_size[0] / size[0]
maps = [Map("Requiem", "map.png", "nav_mesh_requiem.txt", [0,0], mouse_conversion, [2000,1500],
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

[
classes.Intercatable([5,5], None, name = "Box"),

classes.Intercatable([170,295], None, name = "Box"),

classes.Intercatable([560,210], None, name = "Box"),

classes.Intercatable([820,5], None, name = "Box"),

classes.Intercatable([845,585], None, name = "Box"),

classes.Intercatable([281,295], None, name = "Box"),

classes.Intercatable([2,622], None, name = "Box")

]
),

Map("Manufactory", "map2.png", "nav_mesh_manufactory.txt", [0,0], mouse_conversion, [2500,2500],
[ #x,y,width,height
[467,2,156,74],
[2,312,621,155],
[476,233,147,78],
[311,781,156,783],
[311,1565, 939, 156],
[2, 2034, 465, 156],
[781, 2034, 312, 156],
[937,2191,156, 290],
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

[
classes.Intercatable([5,5], None, name = "Box"),

classes.Intercatable([560,210], None, name = "Box"),

classes.Intercatable([210,605], None, name = "Box"),

classes.Intercatable([830,700], None, name = "Box"),

classes.Intercatable([770,530], None, name = "Box"),

classes.Intercatable([970,5], None, name = "Box"),

classes.Intercatable([5,980], None, name = "Box")
]
)
]
