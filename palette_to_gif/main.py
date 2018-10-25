#!/usr/bin/python3

import numpy as np
from PIL import Image as im

def read_gif(gif):
    pass

def generate_palette(h1, h2, num_frames):

    h1 = (h1 * 255)/360
    h2 = (h2 * 255)/360

    colors = np.linspace(h1, h2, num_frames)

    sa = np.uint8(np.linspace(0, 255, 128))
    va = np.uint8(np.linspace(255, 0, 128))
    pad = np.uint8(np.linspace(255, 255, 128))

    lh = map(lambda x : np.uint8(np.full((256, 256), x)), colors)

    lsa = np.uint8(np.tile(sa.reshape(128, 1), 256))
    lva = np.uint8(np.tile(va.reshape(128, 1), 256))
    lpad = np.uint8(np.tile(pad.reshape(128, 1), 256))

    ls = np.concatenate((lsa, lpad), axis=0)
    lv = np.concatenate((lpad, lva), axis=0)

    list_hsv = map(lambda x : np.dstack((np.dstack((x, ls)), lv)), lh)

    return list(list_hsv)

def show_palette(palette):
    list(map(lambda x : im.fromarray(x, 'HSV').convert('RGB').show(), palette))

if __name__ == "__main__":
    palette = generate_palette(0, 240, 3)
    show_palette(palette)
