# For each fitted circle, find the drawn line along rays, then express as distance from the town centre.
import sys
import numpy as np
from PIL import Image
p = sys.argv[1]
a = np.asarray(Image.open(p).convert('L')).astype(float)
H, W = a.shape
ink = (255 - a) / 255.0

def bil(x, y):
    x0 = np.floor(x).astype(int); y0 = np.floor(y).astype(int)
    fx = x - x0; fy = y - y0
    x0 = np.clip(x0, 0, W - 2); y0 = np.clip(y0, 0, H - 2)
    return (ink[y0, x0] * (1 - fx) * (1 - fy) + ink[y0, x0 + 1] * fx * (1 - fy)
            + ink[y0 + 1, x0] * (1 - fx) * fy + ink[y0 + 1, x0 + 1] * fx * fy)

TOWN = (773.5, 1342.0)          # centre of the star / middle of the dividing band
PXMILE = 20.04                  # from the scale bar, ticks 5..40
fits = {'free': (772., 1342., 83.), 'forest': (774., 1342., 150.), 'FWW': (772., 1341., 208.),
        'KW': (774., 1323., 482.), 'DFW': (774., 1324., 617.), 'Vieh(40)': (775., 1318., 780.)}
angs = [8, 20, 40, 60, 80, 90, 100, 120, 140, 160, 172]
print('distance of the drawn line from the town centre (773.5,1342), in miles at %.2f px/mile' % PXMILE)
print('%-9s' % 'angle' + ''.join('%7d' % t for t in angs))
for name, (cx, cy, R) in fits.items():
    out = []; res = []
    for t in angs:
        vals = []
        # average over a small fan of +-1 degree to beat the hatching
        for dt in np.arange(-1.0, 1.01, 0.25):
            th = np.radians(t + dt)
            rr = np.arange(R - 9, R + 9.01, 0.25)
            x = cx + rr * np.cos(th); y = cy - rr * np.sin(th)
            if x.min() < 1 or x.max() > W - 2:
                vals = None; break
            vals.append(bil(x, y))
        if vals is None:
            out.append(None); res.append(None); continue
        v = np.mean(vals, axis=0)
        k = np.ones(5) / 5
        v = np.convolve(v, k, mode='same')
        i = int(np.argmax(v))
        r = R - 9 + 0.25 * i
        th = np.radians(t)
        px = cx + r * np.cos(th); py = cy - r * np.sin(th)
        out.append(np.hypot(px - TOWN[0], py - TOWN[1]) / PXMILE)
        res.append(r - R)
    print('%-9s' % name + ''.join('   n/a ' if o is None else '%7.2f' % o for o in out))
    print('%-9s' % ' resid px' + ''.join('   n/a ' if o is None else '%7.1f' % o for o in res))
