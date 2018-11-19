#!/usr/bin/python3

import numpy as np
from PIL import Image as im

def translate_coords(v, w, tx, ty):
    v, w = np.asarray(v), np.asarray(w)
    return v + tx, w + ty

def translate_image(img, tx, ty):
    sh, sw = img.shape
    cx, cy = translate_coords([0, sw, sw, 0], [0, 0, sh, sh], tx, ty)

    dw, dh = (int(c.max()) for c in (cx, cy))

    dx, dy = np.meshgrid(np.arange(dw), np.arange(dh))

    sx, sy = translate_coords(dx, dy, -tx, -ty)

    mask = (0 <= sx) & (sx < sw) & (0 <= sy) & (sy < sh)

    dest = np.empty(shape=(dh, dw), dtype=img.dtype)

    dest[dy[mask], dx[mask]] = img[sy[mask], sx[mask]]

    return dest

def rotate_coords(v, w, theta):
    v, w = np.asarray(v), np.asarray(w)
    return v * np.cos(theta) - w * np.sin(theta), v * np.sin(theta) + w * np.cos(theta)

def rotate_image(img, theta):
    theta = np.deg2rad(theta)
    theta = -theta

    sh, sw = img.shape

    cx, cy = rotate_coords([0, sw, sw, 0], [0, 0, sh, sh], theta)

    dw, dh = (int(np.ceil(c.max() - c.min())) for c in (cx, cy))

    dx, dy = np.meshgrid(np.arange(dw), np.arange(dh))

    sx, sy = rotate_coords(dx + cx.min(), dy + cy.min(), -theta)

    sx, sy = sx.round().astype(int), sy.round().astype(int)

    mask = (0 <= sx) & (sx < sw) & (0 <= sy) & (sy < sh)

    dest = np.empty(shape=(dh, dw), dtype=img.dtype)

    dest[dy[mask], dx[mask]] = img[sy[mask], sx[mask]]

    return dest

def scale_coords(v, w, cx, cy):
    v, w = np.asarray(v), np.asarray(w)
    return cx * v, cy * w

def scale_image(img, ex, ey):
    sh, sw = img.shape

    cx, cy = scale_coords([0, sw, sw, 0], [0, 0, sh, sh], ex, ey)

    dw, dh = (int(c.max()) for c in (cx, cy))

    dx, dy = np.meshgrid(np.arange(dw), np.arange(dh))

    sx, sy = scale_coords(dx, dy, 1/ex, 1/ey)

    sx, sy = sx.round().astype(int), sy.round().astype(int)

    mask = (0 <= sx) & (sx < sw) & (0 <= sy) & (sy < sh)

    dest = np.empty(shape=(dh, dw), dtype=img.dtype)

    dest[dy[mask], dx[mask]] = img[sy[mask], sx[mask]]

    return dest

if __name__ == "__main__":
    img = im.open('../test_images/mandril_color.tif')
    hsv = img.convert('HSV')
    np_img = np.array(hsv)
    rot_im = rotate_image(np_img[:,:,2], 45)
    im.fromarray(rot_im).convert('L').show()

    tr_im = translate_image(np_img[:,:,2], 100, 100)
    im.fromarray(tr_im).convert('L').show()

    sc_im = scale_image(np_img[:,:,2], 2, 0.5)
    im.fromarray(sc_im).convert('L').show()
