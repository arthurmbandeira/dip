#!/usr/bin/python3

import numpy as np
from PIL import Image as im
from PIL import ImageColor as color

def read_gif(gif):
    pass

def generate_color_palette(h1, h2, seed=None):

    if (seed != None): np.random.seed(seed)

    if not((0 < h1 < 360) or (0 < h2 < 360)):
        raise ValueError('Colors must be between 0 and 360')

    # h1 = np.random.randint(0, 255)
    # h2 = np.random.randint(0, 255)

    color1 = color.getrgb('hsl({}, 100%, 50%)'.format(h1))
    color2 = color.getrgb('hsl({}, 100%, 50%)'.format(h2))

    r = np.linspace(color1[0], color2[0], 256)
    g = np.linspace(color1[1], color2[1], 256)
    b = np.linspace(color1[2], color2[2], 256)

    lr = np.uint8(np.tile(r.reshape(256, 1), 256))
    lg = np.uint8(np.tile(g.reshape(256, 1), 256))
    lb = np.uint8(np.tile(b.reshape(256, 1), 256))

    return np.dstack((np.dstack((lr, lg)), lb))

def generate_luminance_palette():
    pass

if __name__ == "__main__":
    palette = generate_color_palette(130, 170)
    im.fromarray(palette, mode='RGB').show()
