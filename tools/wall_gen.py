import los
import func
import pygame

def getcollisions(tiles,boxcollider):
    return (tile for tile in tiles if tile.colliderect(boxcollider))

def calc_how_many(point, list1):
    j = 0
    for i in list1:
        if point == i:
            j += 1
    return j


def remove_inside_walls(walls):

    remove_list = []
    app_walls = []
    print("Wallpoint calc")
    i = 0
    for wall1 in walls:

        for wall2 in walls:

            p1, p2 = wall1.get_points()
            p3, p4 = wall2.get_points()
            if los.intersect(p1,p2,p3,p4):
                remove_list.append(wall1)
                break

    for wall1 in remove_list:
        walls.remove(wall1)
