#!/usr/bin/python3

import sys
import getopt

import numpy as np
from PIL import Image as im

def translate_coords(v, w, tx, ty):
    v, w = np.asarray(v), np.asarray(w)
    return v + tx, w + ty

def translate_image(img, tx, ty):
    tx, ty = int(tx), int(ty)

    img_grey = len(img.shape) == 2
    if img_grey:
        sh, sw = img.shape
    else:
        sh, sw, _ = img.shape

    cx, cy = translate_coords([0, sw, sw, 0], [0, 0, sh, sh], tx, ty)

    dw, dh = (int(c.max()) for c in (cx, cy))

    dx, dy = np.meshgrid(np.arange(dw), np.arange(dh))

    sx, sy = translate_coords(dx, dy, -tx, -ty)

    mask = (0 <= sx) & (sx < sw) & (0 <= sy) & (sy < sh)

    if img_grey:
        dest = np.empty(shape=(dh, dw), dtype=img.dtype)
        dest[dy[mask], dx[mask]] = img[sy[mask], sx[mask]]
        dest[dy[~mask], dx[~mask]] = 255
    else:
        dest_r = np.empty(shape=(dh, dw), dtype=img.dtype)
        dest_g = np.empty(shape=(dh, dw), dtype=img.dtype)
        dest_b = np.empty(shape=(dh, dw), dtype=img.dtype)

        dest_r[dy[mask], dx[mask]] = img[sy[mask], sx[mask], 0]
        dest_g[dy[mask], dx[mask]] = img[sy[mask], sx[mask], 1]
        dest_b[dy[mask], dx[mask]] = img[sy[mask], sx[mask], 2]

        dest_r[dy[~mask], dx[~mask]] = 255
        dest_g[dy[~mask], dx[~mask]] = 255
        dest_b[dy[~mask], dx[~mask]] = 255

        dest = np.dstack((dest_r, dest_g, dest_b))

    dest_img = im.fromarray(dest)

    return dest_img

def rotate_coords(v, w, theta):
    v, w = np.asarray(v), np.asarray(w)
    return v * np.cos(theta) - w * np.sin(theta), v * np.sin(theta) + w * np.cos(theta)

def rotate_image(img, theta):
    theta = np.deg2rad(theta)
    theta = -theta

    img_grey = len(img.shape) == 2
    if img_grey:
        sh, sw = img.shape
    else:
        sh, sw, _ = img.shape

    cx, cy = rotate_coords([0, sw, sw, 0], [0, 0, sh, sh], theta)

    dw, dh = (int(np.ceil(c.max() - c.min())) for c in (cx, cy))

    dx, dy = np.meshgrid(np.arange(dw), np.arange(dh))

    sx, sy = rotate_coords(dx + cx.min(), dy + cy.min(), -theta)

    sx, sy = sx.round().astype(int), sy.round().astype(int)

    mask = (0 <= sx) & (sx < sw) & (0 <= sy) & (sy < sh)

    if img_grey:
        dest = np.empty(shape=(dh, dw), dtype=img.dtype)
        dest[dy[mask], dx[mask]] = img[sy[mask], sx[mask]]
        dest[dy[~mask], dx[~mask]] = 255
    else:
        dest_r = np.empty(shape=(dh, dw), dtype=img.dtype)
        dest_g = np.empty(shape=(dh, dw), dtype=img.dtype)
        dest_b = np.empty(shape=(dh, dw), dtype=img.dtype)

        dest_r[dy[mask], dx[mask]] = img[sy[mask], sx[mask], 0]
        dest_g[dy[mask], dx[mask]] = img[sy[mask], sx[mask], 1]
        dest_b[dy[mask], dx[mask]] = img[sy[mask], sx[mask], 2]

        dest_r[dy[~mask], dx[~mask]] = 255
        dest_g[dy[~mask], dx[~mask]] = 255
        dest_b[dy[~mask], dx[~mask]] = 255

        dest = np.dstack((dest_r, dest_g, dest_b))

    dest_img = im.fromarray(dest)

    return dest_img

def scale_coords(v, w, cx, cy):
    v, w = np.asarray(v), np.asarray(w)
    return cx * v, cy * w

def scale_image(img, ex, ey):

    img_grey = len(img.shape) == 2
    if img_grey:
        sh, sw = img.shape
    else:
        sh, sw, _ = img.shape

    cx, cy = scale_coords([0, sw, sw, 0], [0, 0, sh, sh], ex, ey)

    dw, dh = (int(c.max()) for c in (cx, cy))

    dx, dy = np.meshgrid(np.arange(dw), np.arange(dh))

    sx, sy = scale_coords(dx, dy, 1/ex, 1/ey)

    sx, sy = sx.round().astype(int), sy.round().astype(int)

    mask = (0 <= sx) & (sx < sw) & (0 <= sy) & (sy < sh)

    if img_grey:
        dest = np.empty(shape=(dh, dw), dtype=img.dtype)
        dest[dy[mask], dx[mask]] = img[sy[mask], sx[mask]]
    else:
        dest_r = np.empty(shape=(dh, dw), dtype=img.dtype)
        dest_g = np.empty(shape=(dh, dw), dtype=img.dtype)
        dest_b = np.empty(shape=(dh, dw), dtype=img.dtype)

        dest_r[dy[mask], dx[mask]] = img[sy[mask], sx[mask], 0]
        dest_g[dy[mask], dx[mask]] = img[sy[mask], sx[mask], 1]
        dest_b[dy[mask], dx[mask]] = img[sy[mask], sx[mask], 2]

        dest = np.dstack((dest_r, dest_g, dest_b))

    dest_img = im.fromarray(dest)

    return dest_img

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hi:t:x:y:a:o:", ["image", "transformation", "x", "y", "theta", "out_image"])
    except getopt.GetoptError:
        print('main.py -i <image> -t <transformation> -x <value_x>  -y <value_y> -a <value_theta> -o <out_image>')
        sys.exit(2)
    theta, x, y = 0, 0, 0
    for opt, arg in opts:
        if opt == '-h':
            print('main.py -i <image> -t <transformation> -x <value_x>  -y <value_y> -a <value_theta> -o <out_image>')
            sys.exit()
        elif opt in ("-i", "--image"):
            image = arg
        elif opt in ("-t", "--transformation"):
            transformation = arg
        elif opt == '-x':
            x = float(arg)
        elif opt == '-y':
            y = float(arg)
        elif opt == '-a':
            theta = float(arg)
        elif opt in ("-o", "--out_image"):
            out_image = arg

    ext = image.split(".")[-1]
    ext = 'tiff' if ext == 'tif' else ext
    img = im.open(image)
    np_img = np.array(img)

    if transformation in ('r', 'rotate'):
        rot_im = rotate_image(np_img, theta)
        rot_im.save('{}_rotated_{}.{}'.format(out_image, theta, ext), format=ext)
    elif transformation in ('s', 'scale'):
        sc_im = scale_image(np_img, x, y)
        sc_im.save('{}_scaled_{}_{}.{}'.format(out_image, x, y, ext), format=ext)
    elif transformation in ('t', 'translate'):
        tr_im = translate_image(np_img, x, y)
        tr_im.save('{}_translated_{}_{}.{}'.format(out_image, x, y, ext), format=ext)
    else:
        raise ValueError('Transformation must be r: rotate, s: scale or t: translate.')

if __name__ == "__main__":
    main(sys.argv[1:])
