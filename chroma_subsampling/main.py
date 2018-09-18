#!/usr/bin/python3

import numpy as np
from PIL import Image as im

pil_img = im.open('../test_images/mandril_color.tif')
# pil_img = im.open('../test_images/lena_color_512.tif')

ycbcr = pil_img.convert('YCbCr')
np_img = np.array(ycbcr)

band_y = np_img[:,:,0]
# band_cb = np_img[:,:,1]
# band_cr = np_img[:,:,2]
band_cb_down_2 = np_img[::2,::2,1]
band_cr_down_2 = np_img[::2,::2,2]

# band_cb_down_4 = np_img[::4,::4,1]
# band_cr_down_4 = np_img[::4,::4,2]

new_band_cb_2 = np.repeat((np.repeat(band_cb_down_2,2,axis=1)),2,axis=0)
new_band_cr_2 = np.repeat((np.repeat(band_cr_down_2,2,axis=1)),2,axis=0)

# new_band_cb_4 = np.repeat((np.repeat(band_cb_down_4,4,axis=1)),4,axis=0)
# new_band_cr_4 = np.repeat((np.repeat(band_cr_down_4,4,axis=1)),4,axis=0)

# joined_img = np.dstack((band_y, new_band_cb, new_band_cr))
joined_img = np.dstack((band_y, new_band_cb_2, new_band_cr_2))
# joined_img = np.dstack((band_y, new_band_cb_4, new_band_cr_4))
out_img = im.fromarray(joined_img, 'YCbCr').convert('RGB')

pil_img.show()
out_img.show()
# out_img.save('../out_images/mandril_cs_2.tif')
