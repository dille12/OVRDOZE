import pygame
import math
import time
import random
pygame.init()

def getcollisionspoint(tiles, point):
    return (tile for tile in tiles if tile.collidepoint(point))

def analyze_map_file(file_name):

    """
    Prints the approximate rectangles for collisions for a map image file. Black means wall, white means space where the player can move.
    """



    image = pygame.image.load(file_name).convert()
    pxarray =  pygame.PixelArray(image)

    size = pxarray.shape
    print(f"Map size:{size}")

    rectangles = []

    for y in range(size[1]):


        for x in range(size[0]):

            if pxarray[x, y] == 0:
                if pxarray[x-1, y] != 0 and pxarray[x, y-1] != 0: ## CREATE NEW RECT

                    rectangles.append(pygame.Rect(x, y, 1, 1))



                if pxarray[x-1, y] == 0:

                    appender = None

                    for rect in rectangles:
                        if rect.x + rect.width == x and rect.y == y and pxarray[x, y - 1] != 0:
                            rect.width += 1


                        if rect.x + rect.width + 1 == x and pxarray[x, y - 1] != 0:
                            print(f"Appending a {x} {y} rectangle")
                            appender = [x,y]


                    if appender != None:
                        rectangles.append(pygame.Rect(x, y, 1, 1))


                if pxarray[x, y - 1] == 0:
                    for rect in rectangles:
                        if rect.y + rect.height == y and rect.x + rect.width - 1 == x:
                            rect.height += 1












    return image, rectangles




if __name__ == "__main__":

    screen = pygame.display.set_mode([50,50])

    map = input("Transfer the collision image to the tool folder.\nInput the name for the map\n>")
    image, rects = analyze_map_file(map)
    print("Job complete. Here are the rectangles")
    print("\n[")
    for rect in rects:
        print(f"[{rect.x}, {rect.y}, {rect.width}, {rect.height}],")

    print("]")

    image.set_alpha(50)

    screen = pygame.display.set_mode([1800,900])

    clock = pygame.time.Clock()

    while 1:

        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
        clock.tick(60)

        screen.fill([0,0,0])

        screen.blit(image, [0,0])

        for rect in rects:
            pygame.draw.rect(screen, [255,0,0], rect, random.randint(1,8))

        pygame.display.update()
