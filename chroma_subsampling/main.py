#!/usr/bin/python3

import sys
import getopt

import numpy as np
from PIL import Image as im
from skimage import measure

def chroma_subsampling(img, J, a, b):
    ycbcr = img.convert('YCbCr')
    np_img = np.array(ycbcr)

    band_y = np_img[:,:,0]

    if (a == 4 and b == 4):
        band_cb = np_img[:,:,1]
        band_cr = np_img[:,:,2]
        a_value = int(J/a)
        b_value = 2 if (b == 0) else 1
    else:
        a_value = int(J/a)
        b_value = 2 if (b == 0) else 1

        band_cb = np_img[::b_value,::a_value,1]
        band_cr = np_img[::b_value,::a_value,2]

    new_band_cb = np.repeat((np.repeat(band_cb, a_value, axis=1)), b_value, axis=0)
    new_band_cr = np.repeat((np.repeat(band_cr, a_value, axis=1)), b_value, axis=0)

    joined_img = np.dstack((band_y, new_band_cb, new_band_cr))
    out_img = im.fromarray(joined_img, 'YCbCr').convert('RGB')

    return out_img

def calc_error(orig_img, proc_img, err='PSNR'):
    if (err == 'PSNR'):
        return measure.compare_psnr(np.array(orig_img), np.array(proc_img))
    elif (err == 'MSE'):
        return measure.compare_mse(np.array(orig_img), np.array(proc_img))
    else:
        raise ValueError('Error type accepted are: MSE or PSNR')

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hi:j:a:b:o:e:", ["image", "j", "a", "b", "out_image", "error"])
    except getopt.GetoptError:
        print('main.py -i <image> -j <j_value> -a <a_value> -b <b_value> -o <out_image> -e <error_measure>')
        sys.exit(2)
    error = ''
    for opt, arg in opts:
        if opt == '-h':
            print('main.py -i <image> -j <j_value> -a <a_value> -b <b_value> -o <out_image> -e <error_measure>')
            sys.exit()
        elif opt in ("-i", "--image"):
            image = arg
        elif opt == '-j':
            j = int(arg)
        elif opt == '-a':
            a = int(arg)
        elif opt == '-b':
            b = int(arg)
        elif opt in ("-o", "--out_image"):
            out_image = arg
        elif opt in ("-e", "--error"):
            error = arg

    ext = image.split(".")[-1]
    ext = 'tiff' if ext == 'tif' else ext

    pil_img = im.open(image)
    out_img = chroma_subsampling(pil_img, j, a, b)
    # out_img.save(out_image + j + a + b '.' + ext, format=ext)
    out_img.save('{}_{}{}{}.{}'.format(out_image, j, a, b, ext), format=ext)

    if error != '':
        print(error + ': ' + str(calc_error(pil_img, out_img, error)))
    else:
        sys.exit(2)

if __name__ == "__main__":
    main(sys.argv[1:])
