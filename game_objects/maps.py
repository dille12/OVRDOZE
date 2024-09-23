from core.level import Map
from core.values import *
import core.classes as classes
import os
import ast

mouse_conversion = fs_size[0] / size[0]

## mouse_conversion =  1920 / 854 = 2.25
## mouse_conversion =  2560 / 854 = 2.99


## 2.25^2/2.99

# 854x480


def getCustomLevels(app, maps):
    folder_path = 'ovrdoze_data/levels'

    if not os.path.isdir(folder_path):
        return maps

    # Get a list of all entries (files and directories) in the folder
    entries = os.listdir(folder_path)

    # Filter out only the directories
    folders = [entry for entry in entries if os.path.isdir(os.path.join(folder_path, entry))]

    # Print each folder name
    for mapName in folders:
        print(mapName)

        mapFolder = folder_path + f"/{mapName}"

        mapFile = mapFolder + "/map.png"
        temp = pygame.image.load(mapFile).convert()
        sizeMap = temp.get_size()

        with open(mapFolder + "/walls.txt", "r") as f:
            rects = f.read()

        rects = ast.literal_eval(rects)
        NAV_MESH = []
        with open(mapFolder + "/navmesh.txt", "r") as f:
            lines = f.readlines()
            lines = ''.join(lines)

            lines = ast.literal_eval(lines)

            for line in lines:
                ref_point = {"point": list(line), "connected": []}
                print(ref_point)
                ref_point["point"][0] *= multiplier2 / mouse_conversion
                ref_point["point"][1] *= multiplier2 / mouse_conversion
                NAV_MESH.append(ref_point)


        maps.append(Map(
            app,
            mapName,
            temp,
            NAV_MESH,
            [0,0],
            mouse_conversion,
            sizeMap,
            POLYGONS=rects,
            CUSTOM=True,
        ))

    return maps


def get_maps(app):


    maps = [
        Map(
            app,
            "Overworld",
            "overworld.png",
            "nav_mesh_overworld.txt",
            [0, 0],
            mouse_conversion,
            [2500, 2500],
            POLYGONS=[  # x,y,width,height
                [2, 1503, 773, 553],
                [1501, 2259, 506, 239],
                [952, 1503, 550, 996],
                [2008, 1503, 492, 996],
                [828, 2, 1670, 744],
                [498, 685, 330, 57],
                [2, 685, 242, 57],
            ],
            OBJECTS=[
                classes.Interactable(
                    app, [164, 30], None, name="Rupert", type="NPC", image="placeholder_npc.png"
                ),

                classes.Interactable(
                    app, [495, 630], None, name="Alan", type="NPC", image="npc_alley.png", angle = 180
                ),

                classes.Interactable(
                    app, [560, 330], None, name="Payphone", type="NPC", image="payphone.png"
                ),

                classes.Interactable(
                    app, [782, 1005], None, name="Basement", type="door", door_dest="Liberation", active = False,
                ),

                classes.Interactable(
                    app, [0, 505], None, name="Downtown", type="door", door_dest="Downtown", active = True, angle = 90
                ),

                classes.Interactable(
                    app, [270, 910], None, name="Vagabond", type="NPC", image="npc2.png"
                ),

            ],
            SPAWNPOINT=[781, 930],
            GAMMA=[0.8, 0.9, 1.2],
            TOP_LAYER="overworld_top.png",
            NO_LOS_POLYGONS=[
                [52, 190, 657, 78],
                [503, 559, 320, 124],
                [722, 389, 106, 170],
            ],
        ),
        Map(
            app,
            "Requiem",
            "map.png",
            "nav_mesh_requiem.txt",
            [0, 0],
            mouse_conversion,
            [2000, 1500],
            POLYGONS=[[ 500, 0, 125, 93 ],
                [ 500, 375, 125, 93 ],
                [ 375, 468, 250, 187 ],
                [ 500, 656, 125, 281 ],
                [ 0, 468, 124, 187 ],
                [ 500, 1125, 124, 93 ],
                [ 250, 1218, 1125, 93 ],
                [ 1124, 1031, 124, 187 ],
                [ 1625, 1218, 374, 93 ],
                [ 1124, 281, 124, 468 ],
                [ 1249, 375, 250, 93 ],
                [ 1750, 375, 249, 93 ],
                [ 1124, 0, 124, 93 ],
                ],
            OBJECTS=[
                classes.Interactable(app, [5, 5], None, name="Box"),
                classes.Interactable(app, [170, 295], None, name="Box"),
                classes.Interactable(app, [560, 210], None, name="Box"),
                classes.Interactable(app, [820, 5], None, name="Box"),
                classes.Interactable(app, [845, 585], None, name="Box"),
                classes.Interactable(app, [281, 295], None, name="Box"),
                classes.Interactable(app, [2, 622], None, name="Box"),
                classes.Interactable(
                    app, [5, 100], None, name="Upgrade Station", type="NPC", image="energywell.png", endlessOnly=True
                ),
                classes.Interactable(app,
                    [390, 0],
                    None,
                    name="Exit",
                    type="door",
                    door_dest="Overworld",
                    active=False,
                ),
            ],
            SPAWNPOINT=[390, 40],
        ),
        Map(
            app,
            "Manufactory",
            "map2.png",
            "nav_mesh_manufactory.txt",
            [0, 0],
            mouse_conversion,
            [2500, 2500],
            POLYGONS=[
                [468, 0, 155, 76],
                [2034, 0, 156, 310],
                [467, 233, 156, 78],
                [0, 311, 623, 156],
                [1095, 312, 468, 155],
                [1564, 312, 155, 783],
                [1095, 467, 154, 313],
                [2034, 625, 154, 156],
                [2034, 781, 466, 156],
                [311, 782, 155, 782],
                [1094, 1095, 625, 154],
                [1564, 1249, 155, 159],
                [1564, 1408, 626, 155],
                [2034, 1563, 155, 471],
                [311, 1564, 938, 155],
                [0, 2034, 466, 156],
                [781, 2034, 312, 156],
                [1407, 2034, 782, 155],
                [938, 2190, 155, 310],
            ],
            OBJECTS=[
                classes.Interactable(app, [5, 5], None, name="Box"),
                classes.Interactable(app, [560, 210], None, name="Box"),
                classes.Interactable(app, [210, 605], None, name="Box"),
                classes.Interactable(app, [830, 700], None, name="Box"),
                classes.Interactable(app, [770, 530], None, name="Box"),
                classes.Interactable(app, [970, 5], None, name="Box"),
                classes.Interactable(
                    app, [210, 350], None, name="Upgrade Station", type="NPC", image="energywell.png", endlessOnly=True
                ),
                classes.Interactable(app, [5, 980], None, name="Box"),
                classes.Interactable(app,
                    [400, 0],
                    None,
                    name="Exit",
                    type="door",
                    door_dest="Overworld",
                    active=False,
                ),
            ],
            SPAWNPOINT=[100, 100],
        ),
        Map(
            app,
            "Liberation",
            "map3.png",
            "nav_mesh3.txt",
            [0, 0],
            mouse_conversion,
            [2500, 2500],
            POLYGONS=[
                [1251, 0, 113, 219],
                [449, 219, 112, 115],
                [1251, 219, 342, 115],
                [1824, 219, 457, 113],
                [334, 334, 457, 113],
                [1022, 334, 342, 113],
                [219, 447, 228, 114],
                [1022, 447, 112, 345],
                [219, 561, 113, 688],
                [2168, 563, 332, 113],
                [2168, 676, 113, 344],
                [792, 792, 457, 113],
                [563, 1136, 686, 113],
                [1136, 1249, 113, 460],
                [2053, 1251, 228, 113],
                [2053, 1364, 113, 345],
                [219, 1480, 113, 229],
                [219, 1709, 342, 113],
                [792, 1709, 801, 113],
                [1824, 1709, 342, 113],
                [219, 1822, 113, 117],
                [792, 1822, 113, 231],
                [2053, 1822, 113, 230],
                [0, 1939, 332, 113],
                [563, 2053, 801, 113],
                [1652, 2111, 113, 112],
                [1251, 2166, 113, 115],
                [2053, 2282, 113, 218],
                [563, 2397, 113, 103],
            ],

            OBJECTS=[
                classes.Interactable(app, [5, 5], None, name="Box"),
                classes.Interactable(app, [560, 210], None, name="Box"),
                classes.Interactable(app, [455, 570], None, name="Box"),
                classes.Interactable(app, [830, 700], None, name="Box"),
                classes.Interactable(app, [770, 530], None, name="Box"),
                classes.Interactable(app, [970, 5], None, name="Box"),
                classes.Interactable(app, [5, 980], None, name="Box"),
                classes.Interactable(
                    app, [507, 253], None, name="Upgrade Station", type="NPC", image="energywell.png", endlessOnly=True
                ),
                classes.Interactable(app,
                    [400, 0],
                    None,
                    name="Exit",
                    type="door",
                    door_dest="Overworld",
                    active=False,
                ),
            ],
            SPAWNPOINT=[400, 60],
        ),

        Map(
            app,
            "Contamination",
            "map4.png",
            "nav_mesh4.txt",
            [0, 0],
            mouse_conversion,
            [3000, 3000],
            POLYGONS=[
                [2101, 0, 151, 149],
                [449, 299, 602, 151],
                [2101, 448, 151, 150],
                [449, 449, 152, 149],
                [900, 449, 151, 301],
                [299, 598, 302, 152],
                [2101, 598, 601, 151],
                [299, 750, 152, 449],
                [2101, 750, 151, 150],
                [2551, 750, 151, 600],
                [900, 1049, 151, 601],
                [299, 1199, 302, 151],
                [2101, 1199, 151, 150],
                [1650, 1349, 602, 152],
                [600, 1650, 451, 150],
                [2551, 1650, 151, 150],
                [0, 1800, 150, 151],
                [2101, 1800, 601, 151],
                [449, 1801, 302, 151],
                [600, 1951, 151, 149],
                [600, 2100, 451, 152],
                [2101, 2251, 601, 151],
                [900, 2252, 151, 299],
                [2251, 2402, 151, 150],
                [0, 2551, 150, 151],
                [449, 2552, 602, 150],
                [2251, 2852, 151, 148],
                ],
            NO_LOS_POLYGONS=[
                [1332,0,336,764],
                [1332,1034,336,1534],
                [1332, 2828, 336, 172],
            ],
            OBJECTS=[
                classes.Interactable(app, [5, 5], None, name="Box"),
                classes.Interactable(app, [560, 210], None, name="Box"),
                classes.Interactable(app, [210, 605], None, name="Box"),
                classes.Interactable(app, [830, 700], None, name="Box"),
                classes.Interactable(app, [745, 555], None, name="Box"),
                classes.Interactable(app, [1005, 5], None, name="Box"),
                classes.Interactable(app, [340, 805], None, name="Box"),
                classes.Interactable(app, [5, 980], None, name="Box"),
                classes.Interactable(
                    app, [890, 550], None, name="Upgrade Station", type="NPC", image="energywell.png", endlessOnly=True
                ),
                classes.Interactable(app,
                    [400, 0],
                    None,
                    name="Exit",
                    type="door",
                    door_dest="Overworld",
                    active=False,
                ),
            ],
            SPAWNPOINT=[667, 400],
            ),

        Map(
            app,
            "Downtown",
            "map5.png",
            "nav_mesh5.txt",
            [0, 0],
            mouse_conversion,
            [6650, 7000],
            TOP_LAYER="map5_top.png",
            GAMMA=[0.8, 0.9, 1.2],
            OBJECTS = [
                classes.Interactable(
                    app, [0, 505], None, name="Overworld", type="door", door_dest="Overworld", active = True, angle = 90, nonDayDoor=True
                ),
            ],
            POLYGONS=[

                    [673, 0, 1015, 122],
                    [2030, 0, 451, 122],
                    [2936, 0, 222, 300],
                    [5083, 0, 563, 297],
                    [5989, 0, 450, 297],
                    [673, 122, 450, 263],
                    [6553, 125, 97, 1135],
                    [3840, 211, 1015, 174],
                    [6215, 297, 224, 438],
                    [1352, 300, 450, 86],
                    [2257, 300, 449, 86],
                    [2936, 300, 563, 261],
                    [4066, 385, 224, 351],
                    [4631, 385, 224, 351],
                    [1352, 386, 1354, 436],
                    [335, 561, 788, 261],
                    [2936, 561, 675, 436],
                    [5197, 561, 337, 614],
                    [3840, 736, 563, 261],
                    [4631, 736, 338, 174],
                    [335, 822, 562, 350],
                    [4179, 997, 224, 700],
                    [1126, 1000, 903, 347],
                    [2370, 1175, 563, 522],
                    [3161, 1175, 224, 611],
                    [3613, 1175, 224, 435],
                    [4631, 1175, 790, 260],
                    [335, 1261, 562, 174],
                    [5649, 1261, 224, 350],
                    [1805, 1347, 224, 263],
                    [673, 1435, 224, 176],
                    [5197, 1435, 224, 440],
                    [1352, 1525, 223, 261],
                    [4631, 1525, 338, 172],
                    [673, 1611, 450, 174],
                    [5649, 1611, 449, 86],
                    [6328, 1611, 322, 86],
                    [5876, 1697, 222, 264],
                    [0, 1700, 445, 347],
                    [673, 1785, 224, 262],
                    [1352, 1786, 677, 349],
                    [3161, 1786, 676, 175],
                    [4406, 1875, 336, 960],
                    [5197, 1875, 337, 436],
                    [2257, 1961, 449, 350],
                    [3161, 1961, 903, 86],
                    [5876, 1961, 563, 86],
                    [3613, 2047, 451, 700],
                    [0, 2225, 218, 172],
                    [448, 2225, 449, 436],
                    [5989, 2225, 661, 260],
                    [1352, 2311, 336, 175],
                    [1918, 2311, 1128, 261],
                    [4971, 2311, 563, 174],
                    [4971, 2485, 223, 526],
                    [6441, 2485, 209, 525],
                    [1239, 2486, 449, 174],
                    [1352, 2660, 336, 90],
                    [0, 2661, 105, 174],
                    [335, 2661, 562, 174],
                    [1352, 2750, 902, 172],
                    [2370, 2750, 788, 172],
                    [448, 2835, 449, 87],
                    [4179, 2835, 337, 262],
                    [3613, 2836, 451, 264],
                    [560, 2922, 224, 88],
                    [2596, 2922, 450, 700],
                    [4858, 3011, 336, 264],
                    [4179, 3097, 111, 439],
                    [3388, 3100, 676, 85],
                    [3727, 3185, 337, 262],
                    [335, 3275, 1353, 260],
                    [3388, 3275, 223, 261],
                    [4631, 3275, 563, 435],
                    [5536, 3275, 450, 347],
                    [6441, 3361, 209, 964],
                    [560, 3535, 903, 525],
                    [3388, 3536, 449, 261],
                    [3954, 3536, 336, 699],
                    [0, 3711, 332, 349],
                    [3613, 3797, 224, 178],
                    [1691, 3800, 676, 522],
                    [4631, 3886, 224, 439],
                    [2596, 3975, 1241, 260],
                    [2484, 4235, 562, 175],
                    [1918, 4322, 449, 178],
                    [0, 4325, 1463, 347],
                    [3161, 4325, 563, 350],
                    [4066, 4325, 224, 350],
                    [4631, 4325, 1242, 347],
                    [6328, 4325, 322, 347],
                    [1918, 4500, 675, 435],
                    [2709, 4500, 337, 522],
                    [900, 4672, 563, 88],
                    [4631, 4672, 224, 175],
                    [5310, 4672, 336, 439],
                    [3161, 4675, 1129, 172],
                    [3727, 4847, 563, 264],
                    [0, 4850, 105, 85],
                    [335, 4850, 336, 85],
                    [5876, 4850, 336, 522],
                    [6328, 4850, 322, 522],
                    [448, 4935, 223, 786],
                    [3161, 4936, 450, 525],
                    [2822, 5022, 224, 439],
                    [900, 5025, 675, 262],
                    [1918, 5025, 675, 522],
                    [3727, 5111, 1242, 174],
                    [5197, 5111, 449, 174],
                    [3727, 5285, 1128, 87],
                    [0, 5286, 105, 86],
                    [335, 5286, 113, 86],
                    [670, 5285, 445, 436],
                    [3727, 5372, 337, 175],
                    [1116, 5286, 458, 86],
                    [4292, 5372, 563, 700],
                    [5310, 5372, 788, 175],
                    [2822, 5461, 789, 86],
                    [6215, 5461, 435, 611],
                    [3388, 5547, 223, 264],
                    [5310, 5636, 788, 436],
                    [1918, 5811, 675, 349],
                    [2709, 5811, 337, 349],
                    [3388, 5811, 676, 261],
                    [0, 5900, 105, 347],
                    [221, 5900, 902, 85],
                    [221, 5986,  1697, 174], #
                    [221, 6160, 902, 175],
                    [2822, 6160, 224, 525],
                    [5310, 6161, 450, 89],
                    [6441, 6161, 209, 89],
                    [5310, 6250, 1340, 347],
                    [900, 6335, 223, 175],
                    [3727, 6600, 449, 172],
                    [4406, 6600, 563, 175],
                    [3388, 6772, 449, 228],
                    [900, 6775, 223, 225],
                    [2822, 6775, 224, 225],
                    [4745, 6776, 1128, 224],

                ],
            NO_LOS_POLYGONS=[

            ],

            SPAWNPOINT=[40, 505],
            )

    ]

    maps = getCustomLevels(app, maps)



    return maps
