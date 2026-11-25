"""reach.py -- what an open reach would show.  The papers measure a reach's length over the straight distance between its
two ends.  Here stretches of a given length are taken out of the long-run rivers of the LX = 400 runs (snapshots from the
second half), starting every 5 units along the stream, and measured that way.
usage: python reach.py out/extra/LX400-s1.snap out/extra/LX400-s2.snap"""
import sys, numpy as np
LX = 400.0
rows = {}
for fn in sys.argv[1:]:
    lines = open(fn).read().strip().split("\n"); T = float(lines[-1].split()[0])
    for line in lines:
        f = line.split(); t = float(f[0])
        if t < T / 2 - 1e-6: continue
        xy = np.array(f[2:], float).reshape(-1, 2)
        xy2 = np.concatenate([xy, xy + [LX, 0]])                       # two periods, so that a stretch may run over the seam
        seg = np.hypot(*np.diff(np.concatenate([xy2, xy2[:1] + [2 * LX, 0]]), axis=0).T); s = np.concatenate([[0], np.cumsum(seg)[:-1]])
        L = s[len(xy)]
        for ell in (25, 50, 100, 200, 400, 800):
            if ell > 0.75 * L: continue
            starts = np.arange(0, L, 5.0); i0 = np.searchsorted(s, starts); i1 = np.searchsorted(s, starts + ell)
            d = np.hypot(*(xy2[i1] - xy2[i0]).T); ok = d > 0
            rows.setdefault(ell, []).append((ell / d[ok], d[ok], L / LX))
print("# stretches of the long-run river (P = 3, dc = 0.4, LX = 400), measured as an open reach would be: length over the straight distance between the ends")
print("# length of stretch   stretches   median   mean   middle 90% of stretches     length / mean distance   share above 6")
for ell in sorted(rows):
    tau = np.concatenate([r[0] for r in rows[ell]]); d = np.concatenate([r[1] for r in rows[ell]])
    print("%12g %14d %9.2f %7.2f      %5.2f to %5.2f %22.2f %15.3f" % (ell, len(tau), np.median(tau), tau.mean(), np.quantile(tau, 0.05), np.quantile(tau, 0.95), ell / d.mean(), (tau > 6).mean()))
S = np.array([r[2] for r in rows[25]])
print("# the same snapshots, whole river over valley length: mean %.3f over %d snapshots" % (S.mean(), len(S)))
