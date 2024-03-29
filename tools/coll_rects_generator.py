import pygame
import math
import time
import random

pygame.init()


# if pxarray[x-1, y] == 0:
#
#     appender = None
#
#     for rect in rectangles:
#         if rect.x + rect.width == x and rect.y == y and pxarray[x, y - 1] != 0:
#             rect.width += 1
#
#
#         if rect.x + rect.width + 1 == x and pxarray[x, y - 1] != 0:
#             print(f"Appending a {x} {y} rectangle")
#             appender = [x,y]
#
#
#     if appender != None:
#         rectangles.append(pygame.Rect(x, y, 1, 1))
#
#
# if pxarray[x, y - 1] == 0:
#     for rect in rectangles:
#         if rect.y + rect.height == y and rect.x + rect.width - 1 == x:
#             rect.height += 1


def getcollisionspoint(tiles, point):
    return (tile for tile in tiles if tile.collidepoint(point))


def analyze_map_file(file_name):

    """
    Prints the approximate rectangles for collisions for a map image file. Black means wall, white means space where the player can move.
    """

    image = pygame.image.load(file_name).convert()
    pxarray = pygame.PixelArray(image)

    size = pxarray.shape
    print(f"Map size:{size}")

    rectangles = []
    last_pix = 1200

    for y in range(size[1]):
        if y%10 == 0:
            print(f"{y}/{size[1]}, {len(rectangles)}")

        for x in range(size[0]):



            if pxarray[x, y] == 0:
                if pxarray[x - 1, y] != 0 or x == 0:  ## CREATE NEW RECT

                    rectangles.append(pygame.Rect(x, y, 1, 1))

                else:

                    for i in (i for i in rectangles if i.y == y):
                        if i.x + i.width == x and y == i.y:
                            i.width += 1
                            break

        for i in (i for i in rectangles if i.y + i.height == y):

            if i.y + i.height != y:
                continue

            #print(i.y + i.height - 1, "y is supposed to be ", y - 1)

            for n in (n for n in rectangles if n.y == y):
                if n.x == i.x and n.width == i.width:
                    i.height += 1
                    rectangles.remove(n)


    return image, rectangles


if __name__ == "__main__":

    screen = pygame.display.set_mode([50, 50])

    map = input(
        "Transfer the collision image to the tool folder.\nInput the name for the map\n>"
    )
    image, rects = analyze_map_file(map)
    size = image.get_size()
    print("Job complete. Here are the rectangles")
    print("\n[")
    warnings = []
    for rect in rects:

        print(f"[{rect.x}, {rect.y}, {rect.width}, {rect.height}],")

        if rect.height <= 5:
            warnings.append(rect)

    print("]")
    print("\n\nWARNING: SOME RECTANGLES ARE TOO SHORT")
    for rect in warnings:
        print(f"[{rect.x}, {rect.y}, {rect.width}, {rect.height}],")



    mult = 800/size[0]

    image2 = pygame.transform.scale(image, [size[0] * mult, size[1]*mult])

    image2.set_alpha(50)

    screen = pygame.display.set_mode([800, round(size[1] * mult)])

    clock = pygame.time.Clock()

    while 1:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        clock.tick(60)

        screen.fill([0, 0, 0])

        screen.blit(image2, [0, 0])

        for rect in rects:

            if rect in warnings:
                pygame.draw.rect(screen, [255, 255, 0], [rect.x * mult, rect.y * mult, 20, 20], random.randint(1, 8))
            else:
                pygame.draw.rect(screen, [255, 0, 0], [rect.x * mult, rect.y * mult, rect.width * mult, rect.height * mult], random.randint(1, 8) if rect in warnings else 1)

        pygame.display.update()
