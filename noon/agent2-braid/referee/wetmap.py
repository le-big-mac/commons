# referee: a coarse picture of where the water is on a saved bed (head at the left; every 4th row), '#' = Q > 0.35% of the river
import sys, math
import numpy as np
NY, NX = 256, 64
h = np.fromfile(sys.argv[1])[:NY*NX].reshape(NY, NX)
Q = np.zeros((NY, NX)); Q[0] = 1.0
for j in range(NY - 1):
    for i in range(NX):
        q = Q[j, i]
        if q == 0: continue
        tg = [ii for ii in (i - 1, i, i + 1) if 0 <= ii < NX]
        s = [(h[j, i] - h[j + 1, ii]) / (1.0 if ii == i else math.sqrt(2)) for ii in tg]
        w = [math.sqrt(x) if x > 0 else 0.0 for x in s] if any(x > 0 for x in s) else [1.0 / math.sqrt(abs(x) + 1e-12) for x in s]
        t = sum(w)
        for ii, ww in zip(tg, w): Q[j + 1, ii] += q * ww / t
wet = Q > 0.0035 * 64
for i in range(0, NX, 2):
    print(''.join('#' if wet[j, i] or wet[j, i + 1] else '.' for j in range(0, NY, 4)))
print('wet share by quarter of the length:', ' '.join('%.2f' % wet[a:b].mean() for a, b in [(1, 64), (64, 128), (128, 192), (192, 255)]))
