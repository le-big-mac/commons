"""Referee: two-gate control. With no third gate nothing bows the trail; do the two directions then share it?"""
import sys, numpy as np
for fn in sys.argv[1:]:
    d = np.load(fn); h = float(d['h']); lo = d['lo']; f6 = d['foot6']
    res = []
    for k in range(2):
        iy, ix = np.nonzero(f6[k]); w = f6[k][iy, ix]; x = lo[0] + ix * h; y = lo[1] + iy * h
        b = np.floor(x * 50).astype(int); ok = (b >= 0) & (b < 50)
        sw = np.bincount(b[ok], w[ok], 50); mu = np.bincount(b[ok], w[ok] * y[ok], 50) / sw
        sd = np.sqrt(np.maximum(np.bincount(b[ok], w[ok] * y[ok] ** 2, 50) / sw - mu ** 2, 0))
        res.append((mu, sd))
    p1 = f6[0] / f6[0].sum(); p2 = f6[1] / f6[1].sum()
    sep = np.abs(res[0][0] - res[1][0])[2:-2]
    print(f"{fn.split('/')[-1]}: cap {float(d['cap'])}: detour Noon's {float(d['detour']):.4f} (minus dt {float(d['detour']) - 1/320:.4f}); "
          f"largest |mean y| of either direction {max(np.abs(res[0][0]).max(), np.abs(res[1][0]).max()) / h:.2f} cells; out-vs-back separation: largest {sep.max() / h:.2f} cells, mean {sep.mean() / h:.2f} cells; "
          f"lateral sd {np.mean([r[1][2:-2].mean() for r in res]) / h:.2f} cells; common-cell share {np.minimum(p1, p2).sum():.3f}")
