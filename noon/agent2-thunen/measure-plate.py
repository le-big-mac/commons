"""measure-plate.py -- the radii of the rings on plate I, measured off the scan.  For a trial centre, the darkness of the
picture is averaged round each half-circle above the centre: a ring's boundary is dark all the way round and gives a sharp
peak, while hatching averages out.  The centre is the one that makes the peaks sharpest.  The scale is taken from the bar
at the foot (the ticks at 5, 10, 15, 20 and 40 miles).   usage: python -I measure-plate.py plate-I-II.jpg"""
import sys, numpy as np
from PIL import Image
a = 255 - np.asarray(Image.open(sys.argv[1]).convert("L")).astype(float); H, W = a.shape
# the scale bar: the long horizontal line near the foot, and the tall ticks on it
band = a[2300:2440]; y0 = 2300 + int((band > 120).sum(axis=1).argmax()); cols = a[y0 - 13:y0 - 4].mean(axis=0); xs = np.where(cols > np.median(cols) + 45)[0]; xs = xs[(xs > 350) & (xs < 1250)]
groups = []; 
for x in xs:
    if groups and x - groups[-1][-1] <= 2: groups[-1].append(x)
    else: groups.append([x])
ticks = [float(np.mean(g)) for g in groups]; print("scale bar at row %d; tall ticks at x = %s" % (y0, ", ".join("%.1f" % t for t in ticks)))
labelled = ticks[-4:] if len(ticks) >= 4 else ticks      # the last four tall ticks: 10, 15, 20, 40 (the first part of the bar is irregular)
px = (labelled[-1] - labelled[-2]) / 20.0; print("20 to 40 miles is %.1f px: %.2f px to the mile; 10 to 20 is %.1f px (%.2f to the mile)" % (labelled[-1] - labelled[-2], px, labelled[-2] - labelled[-4], (labelled[-2] - labelled[-4]) / 10))
def profile(cx, cy, rmax=860):
    th = np.radians(np.arange(25, 156, 0.25)); r = np.arange(20, rmax, 0.5); X = cx + np.outer(r, np.cos(th)); Y = cy - np.outer(r, np.sin(th))
    ok = (X >= 0) & (X < W - 1) & (Y >= 0) & (Y < H - 1); v = np.where(ok, a[np.clip(Y.astype(int), 0, H - 1), np.clip(X.astype(int), 0, W - 1)], np.nan); return r, np.nanmean(v, axis=1)
def peaks(r, p, lo, hi, n):
    q = p - np.convolve(p, np.ones(41) / 41, mode="same"); m = (r >= lo) & (r <= hi); idx = np.where(m)[0]; out = []
    order = idx[np.argsort(-q[idx])]
    for i in order:
        if all(abs(r[i] - r[j]) > 12 for j in out): out.append(i)
        if len(out) == n: break
    return sorted(out), q
best = None
for cx in np.arange(760, 781, 2.0):
    for cy in np.arange(1325, 1356, 2.0):
        r, p = profile(cx, cy, 260); pk, q = peaks(r, p, 50, 250, 3); score = float(sum(q[i] for i in pk))
        if best is None or score > best[0]: best = (score, cx, cy)
print("inner rings: sharpest with the centre at x = %.0f, y = %.0f" % (best[1], best[2]))
r, p = profile(best[1], best[2], 260); pk, q = peaks(r, p, 50, 250, 3)
print("   radii of the three inner boundaries: " + ", ".join("%.0f px = %.2f miles" % (r[i], r[i] / px) for i in pk))
best2 = None
for cx in np.arange(760, 781, 2.0):
    for cy in np.arange(1295, 1356, 3.0):
        r, p = profile(cx, cy); pk, q = peaks(r, p, 420, 850, 3); score = float(sum(q[i] for i in pk))
        if best2 is None or score > best2[0]: best2 = (score, cx, cy)
print("outer rings: sharpest with the centre at x = %.0f, y = %.0f (%.1f miles above the inner centre)" % (best2[1], best2[2], (best[2] - best2[2]) / px))
r, p = profile(best2[1], best2[2]); pk, q = peaks(r, p, 420, 850, 3)
print("   radii of the three outer boundaries: " + ", ".join("%.0f px = %.2f miles" % (r[i], r[i] / px) for i in pk))
