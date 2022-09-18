import pygame
import numpy as np


def colorize(image, newColor):
    """
    Create a "colorized" copy of a surface (replaces RGB values with the given color, preserving the per-pixel alphas of
    original).
    :param image: Surface to create a colorized copy of
    :param newColor: RGB color to use (original alpha values are preserved)
    :return: New colorized Surface instance
    """
    image = image.copy()

    # zero out RGB values
    image.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
    # add in new RGB values
    image.fill(newColor[0:3] + (0,), None, pygame.BLEND_RGBA_ADD)

    return image


def colorize_alpha(image, newColor, alpha):

    image2 = colorize(image, newColor)
    image2.set_alpha(alpha)
    image.blit(image2, [0, 0])
    return image


def greyscale(surface: pygame.Surface):
    arr = pygame.surfarray.array3d(surface)
    # calulates the avg of the "rgb" values, this reduces the dim by 1
    mean_arr = np.mean(arr, axis=2)
    # restores the dimension from 2 to 3
    mean_arr3d = mean_arr[..., np.newaxis]
    # repeat the avg value obtained before over the axis 2
    new_arr = np.repeat(mean_arr3d[:, :, :], 3, axis=2)
    # return the new surface
    return pygame.surfarray.make_surface(new_arr)
