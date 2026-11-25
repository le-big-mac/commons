# second sheet, blind: swollen polygons (polygon of area pi, swollen by d) with the full-circle solver flowp.py
import sys, math, numpy as np, flowp
name = sys.argv[1]; M = int(sys.argv[2])
spec = {'a': ((0, 120, 240), 0.223), 'b': ((0, 135, 255), 0.215), 'c': ((0, 135, 270), 0.205), 'd': ((0, 90, 180, 270), 0.236)}[name]
if len(sys.argv) > 3: spec = (spec[0], float(sys.argv[3]))
th = np.radians(spec[0]); h = np.ones(len(th))
A1, ell = flowp.area_len(th, h); s = math.sqrt(math.pi / A1); d = spec[1] / s     # the polygon has inradius 1 here
T, A0, I, Ie = flowp.forward(th, h + d, M, d, adjoint=True)
print('(%s) swell %.3f M=%5d  swell/inradius=%.5f  area %.6f (exact %.6f)  T over the disc\'s %.5f  Q inside=%.5f  Q edge=%.5f' % (
    name, spec[1], M, d, A0, A1 + ell.sum() * d + math.pi * d * d, T * (math.pi / A0) ** (2 / 3) / 0.75, I * A0 / T ** 2, Ie * A0 / T ** 2), flush=True)
