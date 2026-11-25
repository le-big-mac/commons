import sys
import numpy as np
from PIL import Image
a = np.asarray(Image.open(sys.argv[1]).convert('L')).astype(float)
ink = 255 - a
# find the bar row near the foot
best = max(range(2250, 2450), key=lambda y: (ink[y, 300:1300] > 100).sum())
row = ink[best] > 100
xs = np.where(row[300:1300])[0] + 300
print('bar row', best, 'from', xs.min(), 'to', xs.max())
band = ink[best + 5:best + 18, 340:1220].sum(axis=0); base = np.median(band); thr = base + 0.35 * (band.max() - base)
x = np.arange(340, 1220); pk = []; i = 0
while i < len(band):
    if band[i] > thr:
        j = i
        while j < len(band) and band[j] > thr: j += 1
        w = band[i:j] - base; pk.append(round(float((x[i:j] * w).sum() / w.sum()), 1)); i = j
    else: i += 1
print('ticks below the bar:', pk)
band = ink[best - 18:best - 4, 340:1220].sum(axis=0); base = np.median(band); thr = base + 0.35 * (band.max() - base); pk = []; i = 0
while i < len(band):
    if band[i] > thr:
        j = i
        while j < len(band) and band[j] > thr: j += 1
        w = band[i:j] - base; pk.append(round(float((x[i:j] * w).sum() / w.sum()), 1)); i = j
    else: i += 1
print('ticks above the bar:', pk)
