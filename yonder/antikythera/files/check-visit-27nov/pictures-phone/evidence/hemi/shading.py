"""Is the shading of the phone map the same landscape, in the same place, as the grid in wide.npz and as the wide map?
At a lattice of points every 30 km I work out the loss from the grid (my own interpolation) and so which of the seven shades
the point should have; then I read the colour of that point in each picture. Points that fall on ink, on a label or on a
white line are left out. Reads only."""
import os, math
import numpy as np
from PIL import Image
from matplotlib.colors import LinearSegmentedColormap
R_KM = 6371.0088; KM = math.pi * R_KM / 180
Wz = np.load('/home/agent3/hemi/out/wide.npz')
offs, G = Wz['offs'], Wz['G']
ext = offs * KM
loss = (np.nanmax(G) - G) * 100
LEVELS = [0.01, 0.05, 0.1, 0.2, 0.4, 0.8]
BLUE = LinearSegmentedColormap.from_list('blue', ['#eef5fd', '#cde2fb', '#9ec5f4', '#6da7ec', '#3987e5', '#256abf', '#184f95', '#0d366b'])
SHADES = np.array([[round(255 * c) for c in BLUE(v)[:3]] for v in (0.95, 0.8, 0.65, 0.5, 0.36, 0.22, 0.08)])
print('the seven shades, darkest first (loss under 0.01, 0.05, 0.1, 0.2, 0.4, 0.8, and over):', ['#%02x%02x%02x' % tuple(s) for s in SHADES])
def loss_at(x, y):
    fx = (x - ext[0]) / (ext[1] - ext[0]); fy = (y - ext[0]) / (ext[1] - ext[0])
    i = min(int(fx), len(ext) - 2); j = min(int(fy), len(ext) - 2); a = fx - i; b = fy - j
    return loss[j, i] * (1 - a) * (1 - b) + loss[j, i + 1] * a * (1 - b) + loss[j + 1, i] * (1 - a) * b + loss[j + 1, i + 1] * a * b
def band(v): return sum(v >= L for L in LEVELS)
pts = [(x, y) for x in np.arange(-870, 871, 30.0) for y in np.arange(-870, 871, 30.0)]
want = {p: band(loss_at(*p)) for p in pts}
# a point within 4 km of a line may fall either side of it in a picture: mark those
edge = {p: len({band(loss_at(p[0] + dx, p[1] + dy)) for dx in (-4, 0, 4) for dy in (-4, 0, 4)}) > 1 for p in pts}
got = {}
for n, frame in (('hemi-ridge-phone', (21.59, 248.92, 1036.41, 1263.74)), ('hemi-ridge', (17.85, 142.86, 1172.15, 1297.16))):   # the frames as the programs' own drawings give them (labels_dump.py)
    a = np.asarray(Image.open(f'/home/agent3/site/build/img/{n}.png').convert('RGB')).astype(int)
    x0, y0, x1, y1 = frame
    res = {}
    for (x, y) in pts:
        px = x0 + (x - ext[0]) / (ext[-1] - ext[0]) * (x1 - x0); py = y1 - (y - ext[0]) / (ext[-1] - ext[0]) * (y1 - y0)
        c = a[int(round(py)), int(round(px))]
        d = np.abs(SHADES - c).sum(axis=1)
        res[(x, y)] = int(d.argmin()) if d.min() <= 6 else None
    got[n] = res
    seen = [p for p in pts if res[p] is not None]
    same = sum(res[p] == want[p] for p in seen); diff = [p for p in seen if res[p] != want[p]]
    print(f'{n}: {len(pts)} points; {len(seen)} fall on plain shading; of those {same} have the shade the grid gives, {len(diff)} do not'
          + (f' (of which {sum(edge[p] for p in diff)} lie within 4 km of a line; the others: {[p for p in diff if not edge[p]][:8]})' if diff else ''))
both = [p for p in pts if got['hemi-ridge-phone'][p] is not None and got['hemi-ridge'][p] is not None]
print(f'phone map against wide map: {len(both)} points fall on plain shading in both; the same shade at {sum(got["hemi-ridge-phone"][p] == got["hemi-ridge"][p] for p in both)} of them')
print('points by shade in the grid:', {b: sum(1 for p in pts if want[p] == b) for b in range(7)})
