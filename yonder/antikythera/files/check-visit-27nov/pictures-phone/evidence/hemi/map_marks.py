"""Read the five marks and the scale bar back out of the two pictures of the map and compare with my own working of where they
should stand (out/places_km.json, written by recompute_hemi.py from wide.npz and the places' latitudes and longitudes).
The map's frame is found in the picture itself (the square of blue); the grid runs from -889.6 to +889.6 km across it.
A mark is a patch of the paper's colour ringed with ink; I look for it within 20 km of where it should be. Reads only."""
import json, os, math
import numpy as np
from PIL import Image
from scipy import ndimage
HERE = os.path.dirname(os.path.abspath(__file__))
P = json.load(open(f'{HERE}/out/places_km.json'))
e0, e1 = P['ext0'], P['ext1']
MARKS = {'southern summit': 'circle', 'northern summit': 'circle', 'Nantes': 'square', 'Ile Dumet': 'triangle', 'Tarragona': 'diamond'}
for n in ['hemi-ridge-phone', 'hemi-ridge']:
    a = np.asarray(Image.open(f'/home/agent3/site/build/img/{n}.png').convert('RGB')).astype(int)
    H, W = a.shape[:2]
    blue = (a[..., 2] - a[..., 0] > 15)                      # the shades of the map are all bluer than the paper
    cols = np.where(blue.mean(axis=0) > 0.3)[0]; rws = np.where(blue.mean(axis=1) > 0.3)[0]
    fx0, fx1, fy0, fy1 = cols.min(), cols.max() + 1, rws.min(), rws.max() + 1
    ppk = (fx1 - fx0) / (e1 - e0)
    print(f'\n{n}: {W} x {H}; map square found at columns {fx0}..{fx1}, rows {fy0}..{fy1} ({fx1 - fx0} by {fy1 - fy0} pixels); one km = {ppk:.4f} px across, {(fy1 - fy0) / (e1 - e0):.4f} px up')
    topx = lambda x, y: (fx0 + (x - e0) * ppk, fy1 - (y - e0) * (fy1 - fy0) / (e1 - e0))
    white = (a.min(axis=2) >= 246)
    ink = (a.max(axis=2) <= 70)
    lab, k = ndimage.label(white)
    found = {}
    for name, shape in MARKS.items():
        ex, ey = topx(*P[name])
        best = None
        r = int(20 * ppk) + 2
        ids = set(np.unique(lab[int(ey) - r:int(ey) + r + 1, int(ex) - r:int(ex) + r + 1])) - {0}
        for i in ids:
            ys, xs = np.where(lab == i)
            if not (25 <= len(ys) <= 900): continue
            cx, cy = xs.mean(), ys.mean(); d = math.hypot(cx - ex, cy - ey)
            fill = len(ys) / ((xs.max() - xs.min() + 1) * (ys.max() - ys.min() + 1))
            if best is None or d < best[0]: best = (d, cx, cy, len(ys), fill, xs.max() - xs.min() + 1, ys.max() - ys.min() + 1)
        if best is None: print(f'  {name}: NO pale patch within 20 km of ({ex:.1f}, {ey:.1f})'); continue
        d, cx, cy, npx, fill, wx, wy = best
        found[name] = (cx, cy)
        print(f'  {name:16s} ({shape:8s}) should be at pixel ({ex:6.1f}, {ey:6.1f}); pale patch of {npx:3d} px, {wx} by {wy}, filling {fill:.2f} of its box, centred ({cx:6.1f}, {cy:6.1f}): {d / ppk:4.1f} km off')
    if 'southern summit' in found and 'northern summit' in found:
        (sx, sy), (nx_, ny_) = found['southern summit'], found['northern summit']
        print(f'  the two summits\' patches are {math.hypot(sx - nx_, sy - ny_) / ppk:.0f} km apart in the picture (the programs print 797 km; the northern patch is partly under the triangle)')
    # the scale bar: the longest level run of ink in the lower left quarter of the map
    sub = ndimage.binary_erosion(ink, structure=np.ones((5, 1)))[(fy0 + fy1) // 2:fy1, fx0:(fx0 + fx1) // 2]      # only strokes at least five pixels thick: the bar, not the thin joining lines
    best = (0, 0, 0)
    for j in range(sub.shape[0]):
        row = sub[j]; s = None
        for i, v in enumerate(list(row) + [False]):
            if v and s is None: s = i
            if not v and s is not None:
                if i - s > best[0]: best = (i - s, s, j)
                s = None
    L, s, j = best
    print(f'  scale bar: {L} px long, from column {fx0 + s} at row {(fy0 + fy1) // 2 + j} = {L / ppk:.0f} km (lettered "200 km")')
