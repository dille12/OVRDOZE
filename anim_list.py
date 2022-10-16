from values import *
import pygame
def load_animation(directory, start_frame, frame_count, alpha=255, intro = False):
    list_anim = []


    for x in range(frame_count):
        x = x + start_frame
        im_dir = directory + "/" + (4 - len(str(x))) * "0" + str(x) + ".png"

        im = load(im_dir, double=True)

        if intro:
            if x - start_frame > frame_count-10:
                i = (x - start_frame) - (frame_count-10)
                i = (i/10) ** 3 + 1
                size = list(im.get_size())
                size[0] *= i
                size[1] *= i

                im = pygame.transform.scale(im, size)

        if alpha != 255:
            im2 = pygame.Surface(im.get_size())
            im2.fill((0, 0, 0))
            im.set_alpha(alpha)
            im2.blit(im, (0, 0))
            list_anim.append(im2)
        else:
            list_anim.append(im)

    return list_anim

expl1 = load_animation("anim/expl1", 0, 31)
