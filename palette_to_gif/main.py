#!/usr/bin/python3

import numpy as np
from PIL import Image as im

def read_gif(gif):
    frames = im.open(gif)
    out = []
    curr_frame = 0
    while frames:
        out.append(np.array(frames.convert('HSV'))[:,:,2])
        curr_frame += 1
        try:
            frames.seek(curr_frame)
        except EOFError:
            break
    out = np.array(out)
    return out

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

    return np.array(list(list_hsv))

def show_palette(palette):
    list(map(lambda x : im.fromarray(x, 'HSV').convert('RGB').show(), palette))

if __name__ == "__main__":
    gif_arr = read_gif('../test_images/magic.gif')
    # gif_arr = read_gif('../test_images/mind_blowing.gif')
    palette = generate_palette(0, 340, len(gif_arr))

    run_arr = list(map(lambda x : np.array(im.fromarray(x).convert('RGB')), gif_arr))
    out_arr = []

    for x in range(len(gif_arr)):
        run_arr[x] = palette[x][:, 1, :][gif_arr[x]]
        out_arr.append(im.fromarray(run_arr[x], 'HSV').convert('RGB'))

    out_arr[0].save('out1.gif', format='GIF', save_all=True, append_images=out_arr[1:], duration=100, loop=0)
