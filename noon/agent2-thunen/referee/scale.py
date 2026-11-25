import sys
import numpy as np
from PIL import Image
p = sys.argv[1]
a = np.asarray(Image.open(p).convert('L')).astype(float)
ink = 255 - a
# ticks: column sums in a band above and below the bar
for (y0, y1) in ((2352, 2368), (2378, 2392)):
    band = ink[y0:y1, 360:1200].sum(axis=0)
    base = np.median(band)
    xs = np.arange(360, 1200)
    pk = []
    thr = base + 0.35 * (band.max() - base)
    i = 0
    while i < len(band):
        if band[i] > thr:
            j = i
            while j < len(band) and band[j] > thr:
                j += 1
            w = band[i:j] - base
            c = (xs[i:j] * w).sum() / w.sum()
            pk.append((round(float(c), 2), j - i))
            i = j
        else:
            i += 1
    print('band', y0, y1, pk)
# bar ends, per row
for y in range(2368, 2378):
    row = ink[y] > 100
    xs_ = np.where(row[300:1300])[0] + 300
    if len(xs_):
        print(y, xs_.min(), xs_.max(), len(xs_))
