"""Where does a trial picture of the map differ from the picture as drawn? Prints the boxes of the differing pixels.
usage: compare_try_map.py TRIAL.png"""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage
a = np.asarray(Image.open('/home/agent3/site/build/img/hemi-ridge-phone.png').convert('RGB')).astype(int)
b = np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(int)
assert a.shape == b.shape
d = np.abs(a - b).sum(axis=2) > 0
print(sys.argv[1].split('/')[-1], ': pixels that differ', int(d.sum()), 'of', d.size)
lab, k = ndimage.label(ndimage.binary_dilation(d, iterations=10))
for i in range(1, k + 1):
    ys, xs = np.where((lab == i) & d)
    print(f'   differing pixels in columns {xs.min()}..{xs.max()}, rows {ys.min()}..{ys.max()} ({len(ys)} pixels)')
