#!/usr/bin/python3

import numpy as np
from skimage import measure
from PIL import Image as im

def chroma_subsampling(img, J, a, b):
    ycbcr = img.convert('YCbCr')
    np_img = np.array(ycbcr)

    band_y = np_img[:,:,0]

    if (a == 4 and b == 4):
        band_cb = np_img[:,:,1]
        band_cr = np_img[:,:,2]
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
        pass

# pil_img = im.open('../test_images/mandril_color.tif')
pil_img = im.open('../test_images/lena_color_512.tif')
out_img = chroma_subsampling(pil_img, 4, 1, 1)

print(calc_error(pil_img, out_img, 'PSNR'))

# pil_img.show()
# out_img.show()
