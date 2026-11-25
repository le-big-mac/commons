# last step: my own poolings of every exact-n set (sheet 1, the chase, sheet 2), quarter discs and other shapes
import json, glob, os, math
import numpy as np
al, D = 1.3259, 1.081
Q = {'disc': 4/3, 'disc0': 4/3, 'ellipse': 4/3, 'triangle': 4/3, 'square': 4/3, 'hexagon': 4/3, 'halfdisc': 1.33038, 'quarter': 1.33115, 'rtriangle': 1.30562}
line = {s: D / al**2 * q - 4/9 for s, q in Q.items()}; line['quarter'] = 0.37408
rows = []
for folder in ('/home/agent2/peel/shape/runs', '/home/agent2/peel/shape/runs-after'):
    for f in sorted(glob.glob(folder + '/*.jsonl')):
        Dd = [json.loads(l) for l in open(f) if l.strip()]
        if Dd[0]['kind'] != 'exact': continue
        shape = Dd[0]['shape']; n0 = Dd[0]['n0']; x = np.array([d['layers'] for d in Dd], float); K = len(x)
        sh = 'disc' if shape in ('disc0',) else shape
        if sh not in line:
            print('unknown shape', shape, os.path.basename(f)); continue
        m = x.mean(); v = x.var(ddof=1); m4 = ((x - m)**4).mean(); se = math.sqrt((m4 - (K - 3) / (K - 1) * v * v) / K)
        r = v * n0 / m**2 / line[sh]; rows.append((os.path.basename(folder) + '/' + os.path.basename(f), sh, n0, K, r, r * se / v))
for t in rows: print('%-48s %-9s %6d K=%6d r=%.4f (%.4f)' % t)
def pool(sel, name):
    q = [(r, s, K) for (f, sh, n0, K, r, s) in rows if sel(f, sh, n0)]
    w = np.array([1 / s**2 for r, s, K in q]); r = np.array([r for r, s, K in q]); mu = (w * r).sum() / w.sum(); se = 1 / math.sqrt(w.sum())
    print('%-86s files %2d clouds %7d  r %.4f (%.4f) %+.1f errors; chi2 %.1f on %d' % (name, len(q), sum(K for r, s, K in q), mu, se, (mu - 1) / se, (w * (r - mu)**2).sum(), len(q) - 1)); return mu, se
first8 = 'runs/exact-quarter-100000.jsonl'; firstdisc = 'runs/exact-disc-100000.jsonl'
a = pool(lambda f, s, n: s == 'quarter' and n == 100000 and f != first8, 'quarter, 100,000, all but the first 8,000')
b = pool(lambda f, s, n: s == 'quarter' and n == 30000, 'quarter, 30,000')
print('   lean, quarter discs, all lawful: %+.4f (%.4f) = %+.1f errors' % (a[0] - b[0], math.hypot(a[1], b[1]), (a[0] - b[0]) / math.hypot(a[1], b[1])))
c = pool(lambda f, s, n: s != 'quarter' and n == 100000, 'other shapes, 100,000, every set')
c2 = pool(lambda f, s, n: s != 'quarter' and n == 100000 and f != firstdisc, 'other shapes, 100,000, without the first sheet\'s disc set')
d = pool(lambda f, s, n: s != 'quarter' and n == 30000, 'other shapes, 30,000')
print('   lean, other shapes: %+.4f (%.4f) = %+.1f errors' % (c[0] - d[0], math.hypot(c[1], d[1]), (c[0] - d[0]) / math.hypot(c[1], d[1])))
e = pool(lambda f, s, n: n == 100000 and f != first8, 'every exact set at 100,000 but the first 8,000 quarter discs')
g = pool(lambda f, s, n: n == 30000, 'every exact set at 30,000')
print('   lean, everything: %+.4f (%.4f) = %+.1f errors' % (e[0] - g[0], math.hypot(e[1], g[1]), (e[0] - g[0]) / math.hypot(e[1], g[1])))
e2 = pool(lambda f, s, n: n == 100000 and f != first8 and 'q2-' in f or (n == 100000 and s != 'quarter'), '100,000: the sealed quarter sets and the other shapes (no chase)')
print('   lean, sealed quarter sets and other shapes: %+.4f (%.4f) = %+.1f errors' % (e2[0] - g[0], math.hypot(e2[1], g[1]), (e2[0] - g[0]) / math.hypot(e2[1], g[1])))
cq = pool(lambda f, s, n: s == 'quarter' and f != first8 and 'numpy' not in f, 'quarter, cloud.c, both sizes, all but the first 8,000')
nq = pool(lambda f, s, n: s == 'quarter' and 'numpy' in f, 'quarter, numpy, both sizes')
print('   cloud.c less numpy, all lawful quarter discs: %+.4f (%.4f) = %+.1f errors' % (cq[0] - nq[0], math.hypot(cq[1], nq[1]), (cq[0] - nq[0]) / math.hypot(cq[1], nq[1])))
pool(lambda f, s, n: 'own-' in f or 'disc0' in f, 'peel\'s own generator, all shapes, 100,000')
pool(lambda f, s, n: s == 'quarter' and n == 100000 and 'cloud' not in f and 'numpy' not in f and f != first8, 'the chase by cloud.c alone (76,000)')
