# Digital Image Processing Course Projects

## 1. Chroma Subsampling

```
$ ./main.py -i ../test_images/mandril_color.tif -j 4 -a 1 -b 1 -o results/out
```

## 2. Affine Transformations
```
$ ./main.py -i ../test_images/lena_color_512.tif -t s -x 0.8 -y 0.5 -o results/lena_color
```
```
$ ./main.py -i ../test_images/lena_gray_512.tif -t t -x 100 -y 50 -o results/lena_gray
```
```
$ ./main.py -i ../test_images/lena_color_512.tif -t r -a 60 -o results/lena_color
```

## 3. Generated Color Palette Applied to a Sequence of Images
```
$ ./main.py -i ../test_images/magic.gif -a 0 -b 320 -o results/out_magic
```
```
$ ./main.py -i ../test_images/rupaul.gif -a 0 -b 340 -o results/out_rupaul -p 1
```

## Members
 - Arthur Manuel Bandeira
 - Fábio Pinheli
