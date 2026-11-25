# Classify the hatching of the plates by a structure tensor, and read ring boundaries along rays.
# classes: '.' blank or sparse dots, 'o' dots (free farming), 'F' forest "\" hatch, 'W' vertical hatch (Fruchtwechsel),
#          'K' horizontal hatch (Koppel), 'D' "/" hatch (Dreifelder)
import sys
import numpy as np
from PIL import Image

def load(p):
    return np.asarray(Image.open(p).convert('L')).astype(float)

def box(a, w):
    # mean over a (2w+1)^2 window via integral image
    H, W = a.shape
    ii = np.zeros((H + 1, W + 1)); ii[1:, 1:] = a.cumsum(0).cumsum(1)
    y0 = np.clip(np.arange(H) - w, 0, H); y1 = np.clip(np.arange(H) + w + 1, 0, H)
    x0 = np.clip(np.arange(W) - w, 0, W); x1 = np.clip(np.arange(W) + w + 1, 0, W)
    s = ii[y1][:, x1] - ii[y0][:, x1] - ii[y1][:, x0] + ii[y0][:, x0]
    return s / ((y1 - y0)[:, None] * (x1 - x0)[None, :])

def tensor(a, w=7):
    g = box(a, 1)
    gx = np.zeros_like(g); gy = np.zeros_like(g)
    gx[:, 1:-1] = g[:, 2:] - g[:, :-2]; gy[1:-1, :] = g[2:, :] - g[:-2, :]
    return box(gx * gx, w), box(gy * gy, w), box(gx * gy, w), box(255 - a, w)

def classify(Jxx, Jyy, Jxy, ink):
    E = Jxx + Jyy
    coh = np.sqrt((Jxx - Jyy) ** 2 + 4 * Jxy ** 2) / np.maximum(E, 1e-9)
    ang = np.degrees(0.5 * np.arctan2(2 * Jxy, Jxx - Jyy))     # 0: vertical lines; +-90: horizontal; +45: "/"; -45: "\"
    c = np.full(E.shape, '.', dtype='<U1')
    hatch = (E > 150) & (coh > 0.45)
    c[(E > 150) & ~hatch] = 'o'
    c[hatch & (np.abs(ang) < 22.5)] = 'W'
    c[hatch & (np.abs(ang) > 67.5)] = 'K'
    c[hatch & (ang >= 22.5) & (ang <= 67.5)] = 'D'
    c[hatch & (ang <= -22.5) & (ang >= -67.5)] = 'F'
    return c

def ray(c, cx, cy, deg, rmax, step=2):
    # deg measured from straight up, clockwise positive; returns string of classes every `step` px
    t = np.radians(deg); out = []
    for r in np.arange(0, rmax, step):
        x = int(round(cx + r * np.sin(t))); y = int(round(cy - r * np.cos(t)))
        out.append(c[y, x] if 0 <= x < c.shape[1] and 0 <= y < c.shape[0] else ' ')
    return ''.join(out)

def runs(s, step, pxmile, minlen=3):
    # collapse to runs, dropping runs shorter than minlen samples (boundary lines, ray lines)
    res = []; i = 0
    while i < len(s):
        j = i
        while j < len(s) and s[j] == s[i]: j += 1
        res.append([s[i], i, j]); i = j
    res = [r for r in res if r[2] - r[1] >= minlen]
    merged = []
    for r in res:
        if merged and merged[-1][0] == r[0]: merged[-1][2] = r[2]
        else: merged.append(r)
    return ' '.join('%s:%.1f-%.1f' % (k, a * step / pxmile, b * step / pxmile) for k, a, b in merged)

if __name__ == '__main__':
    p = sys.argv[1]; which = sys.argv[2]
    a = load(p); c = classify(*tensor(a))
    PX = float(sys.argv[5]) if len(sys.argv) > 5 else 20.04
    if which == 'I':
        for deg in (-80, -60, -30, -10, 10, 30, 60, 80):
            print('plate I  %4d deg: %s' % (deg, runs(ray(c, 773.5, 1342, deg, 830), 2, PX)))
    if which in ('III', 'IV'):
        cx, cy, sgn = (float(sys.argv[3]), float(sys.argv[4]), -1 if which == 'III' else 1)
        labels = ['1.50', '1.35', '1.20', '1.05', '0.90', '0.75', '0.60'] if which == 'III' else ['10', '9', '8', '7', '6', '5', '4']
        for k, lab in enumerate(labels):
            for off in (-4, 4) if 0 < k < 6 else ((4,) if k == 0 else (-4,)):
                deg = sgn * (30 * k + off)
                print('plate %s  %s (ray %+d deg): %s' % (which, lab, off, runs(ray(c, cx, cy, deg, 760), 2, PX)))
