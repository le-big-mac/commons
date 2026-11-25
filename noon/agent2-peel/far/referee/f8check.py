import contextlib, io, os, runpy, sys
import numpy as np
FAR = sys.argv[1]
with contextlib.redirect_stdout(io.StringIO()): G = runpy.run_path(os.path.join(FAR, 'study.py'))
W, offsets_at, PERIOD, STEP, FIRST, NEAR = (G[k] for k in ('W', 'offsets_at', 'PERIOD', 'STEP', 'FIRST', 'NEAR'))
ch = []; dn = []
for w in W:
    off = offsets_at(w); nodes = list(range(FIRST, w['HM'] + 1, STEP))
    for i in range(len(nodes) - 1):
        ch.append(off[i + 1] - off[i]); dn.append((w['c'][nodes[i] - NEAR // 2:nodes[i + 1] - NEAR // 2].sum() - PERIOD * STEP) / PERIOD)
ch = np.array(ch); dn = np.array(dn)
b0 = (ch * dn).mean() / (dn * dn).mean()
c = np.cov(ch, dn, ddof=1); b1 = c[0, 1] / c[1, 1]; r = np.corrcoef(ch, dn)[0, 1]
n = len(ch); se = np.sqrt((1 - r * r) / (n - 2) * c[0, 0] / c[1, 1])
print('n', n, 'STEP', STEP, 'NEAR', NEAR, 'FIRST', FIRST, 'PERIOD', PERIOD)
print('mean change %.4f (sd %.4f); mean excess count per unit width %.4f (sd %.4f)' % (ch.mean(), ch.std(ddof=1), dn.mean(), dn.std(ddof=1)))
print('slope through the origin (the README figure) %.4f; slope about the means %.4f +- %.4f; correlation %.4f' % (b0, b1, se, r))
print('D %.4f; carried by count with centred slope %.4f' % (PERIOD * c[0, 0] / STEP, PERIOD * (r * r * c[0, 0]) / STEP))
