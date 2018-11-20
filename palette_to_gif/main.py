#!/usr/bin/python3

import sys
import getopt

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

    va = np.uint8(np.linspace(0, 255, 128))
    sa = np.uint8(np.linspace(255, 0, 128))
    pad = np.uint8(np.linspace(255, 255, 128))

    lh = map(lambda x : np.uint8(np.full((256, 256), x)), colors)

    lva = np.uint8(np.tile(va.reshape(128, 1), 256))
    lsa = np.uint8(np.tile(sa.reshape(128, 1), 256))
    lpad = np.uint8(np.tile(pad.reshape(128, 1), 256))

    lv = np.concatenate((lva, lpad), axis=0)
    ls = np.concatenate((lpad, lsa), axis=0)

    map_hsv = map(lambda x : np.dstack((np.dstack((x, ls)), lv)), lh)

    return np.array(list(map_hsv))

def show_palette(palette):
    list(map(lambda x : im.fromarray(x, 'HSV').convert('RGB').show(), palette))

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hi:a:b:o:p:", ["image", "color_a", "color_b", "out_image", "show_palette"])
    except getopt.GetoptError:
        print('main.py -i <image> -a <color_a> -b <color_b> -o <out_image> -p <show_pallete>')
        sys.exit(2)
    sp = False
    for opt, arg in opts:
        if opt == '-h':
            print('main.py -i <image> -a <color_a> -b <color_b> -o <out_image> -p <show_pallete>')
            sys.exit()
        elif opt in ("-i", "--image"):
            image = arg
        elif opt in ("-a", "--color_a"):
            color_a = int(arg)
        elif opt in ("-b", "--color_b"):
            color_b = int(arg)
        elif opt in ("-o", "--out_image"):
            out_image = arg
        elif opt in ("-p", "--show_palette"):
            sp = bool(arg)

    gif_arr = read_gif(image)
    palette = generate_palette(color_a, color_b, len(gif_arr))

    if sp: show_palette(palette)

    out_arr = [im.fromarray(palette[x][:, 1, :][gif_arr[x]], 'HSV').convert('RGB') for x in range(len(gif_arr))]
    out_arr[0].save(out_image + '.gif', format='GIF', save_all=True, append_images=out_arr[1:], duration=100, loop=0)

if __name__ == "__main__":
    main(sys.argv[1:])
