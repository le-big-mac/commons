"""Where does each trial picture differ from the picture as drawn? Reads the two files, prints the boxes of the differing pixels
and whether any pixel of a blue or orange line changed."""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage
for old, new in (('/home/agent3/site/build/img/dial-kept-phone.png', '/home/agent3/site/check-pictures-phone/tryfix/dial-kept-phone-try.png'),
                 ('/home/agent3/site/build/img/handshake-popsize-phone.png', '/home/agent3/site/check-pictures-phone/tryfix/handshake-popsize-phone-try.png')):
    a = np.asarray(Image.open(old).convert('RGB')).astype(int); b = np.asarray(Image.open(new).convert('RGB')).astype(int)
    assert a.shape == b.shape
    d = np.abs(a - b).sum(axis=2) > 0
    def near(x, hexcol, tol):
        c = np.array([int(hexcol[i:i + 2], 16) for i in (1, 3, 5)]); return np.abs(x - c).sum(axis=2) < tol
    line_old = near(a, '#2a78d6', 70) | near(a, '#eb6834', 70); line_new = near(b, '#2a78d6', 70) | near(b, '#eb6834', 70)
    print(new.split('/')[-1], ': pixels that differ', int(d.sum()), '; blue or orange pixels that changed', int((line_old != line_new).sum()))
    lab, k = ndimage.label(ndimage.binary_dilation(d, iterations=12))
    for i in range(1, k + 1):
        ys, xs = np.where((lab == i) & d)
        print(f'   differing pixels in columns {xs.min()}..{xs.max()}, rows {ys.min()}..{ys.max()}')
