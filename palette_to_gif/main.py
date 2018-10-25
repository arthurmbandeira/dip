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

def generate_luminance_palette(h1, h2, num_frames):

    h1 = (h1 * 255)/360
    h2 = (h2 * 255)/360

    colors = np.linspace(h1, h2, num_frames)

    sa = np.uint8(np.linspace(0, 255, 128))
    va = np.uint8(np.linspace(255, 0, 128))
    pad = np.uint8(np.linspace(255, 255, 128))

    # lh = np.uint8(np.full((256, 256), colors[4]))
    lh = map(lambda x : np.uint8(np.full((256, 256), x)), colors)

    lsa = np.uint8(np.tile(sa.reshape(128, 1), 256))
    lva = np.uint8(np.tile(va.reshape(128, 1), 256))
    lpad = np.uint8(np.tile(pad.reshape(128, 1), 256))

    ls = np.concatenate((lsa, lpad), axis=0)
    lv = np.concatenate((lpad, lva), axis=0)

    list_hsv = map(lambda x : np.dstack((np.dstack((x, ls)), lv)), lh)
    list_out = map(lambda x : im.fromarray(x, 'HSV').convert('RGB'), list_hsv)

    list(map(lambda x : x.show(), list(list_out)))

generate_luminance_palette(50, 100, 5)

# if __name__ == "__main__":
#     palette = generate_color_palette(130, 170)
#
#     im.fromarray(palette, mode='RGB').show()
#     # im.fromarray(palette[:, 0:1], mode='RGB').show()
