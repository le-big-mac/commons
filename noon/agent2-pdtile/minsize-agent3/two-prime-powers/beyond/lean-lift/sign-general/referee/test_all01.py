# every nonzero 0/1 function on the 3 x 5 box: least fraction of good patterns (all levels), over Q and F_7
import sys, time, numpy as np
from fractions import Fraction
from boxlib import *
sides = [3, 5]
LV = all_levels(2)
t0 = time.time()
for q in (0, 7):
    least = None; n = 0
    for code in range(1, 2 ** 15):
        if time.time() - t0 > (25 if q == 0 else 50): break
        g = np.array([(code >> i) & 1 for i in range(15)]).reshape(3, 5)
        res, _ = good_table(g, sides, q, LV)
        c = int(res.sum()); n += 1
        if least is None or c < least[0]: least = (c, code)
    print('3x5, q=%d: 0/1 functions tested %d of 32767, least number of good patterns %d of 256 (bound 64), at code %d' % (q, n, least[0], least[1]))
