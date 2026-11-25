# last step: do the other shapes' clouds (first and second sheets) carry the disc's constant?  r predicted = k - 0.0414 / V_theory
import json, glob, os, math
import numpy as np
al, D, D2, b = 1.3259, 1.081, 1.0894, -0.0414
Q = {'disc': 4/3, 'disc0': 4/3, 'ellipse': 4/3, 'triangle': 4/3, 'square': 4/3, 'hexagon': 4/3, 'halfdisc': 1.33038, 'quarter': 1.33115, 'rtriangle': 1.30562}
rows = []
for folder in ('/home/agent2/peel/shape/runs', '/home/agent2/peel/shape/runs-after'):
    for f in sorted(glob.glob(folder + '/*.jsonl')):
        bn = os.path.basename(f)
        if bn.startswith('n3-') or bn.startswith('n4-'): continue
        with open(f) as fh: first = json.loads(fh.readline())
        if first['kind'] != 'exact': continue
        sh = first['shape']; n0 = first['n0']
        if sh not in Q: continue
        x = np.array([json.loads(l)['layers'] for l in open(f)], float); K = len(x); m = x.mean(); v = x.var(ddof=1); m4 = ((x - m)**4).mean(); se = math.sqrt((m4 - v*v) / K)
        q = Q[sh]; line = D / al**2 * q - 4/9; vth = line * m * m / n0; k = (D2 * q - 4/9 * al**2) / (D * q - 4/9 * al**2)
        rows.append((os.path.basename(folder) + '/' + bn, 'disc' if sh == 'disc0' else sh, n0, K, v, se, vth, k * vth + b))
def pool(sel, name):
    q = [(v - vp, se, K) for (f, sh, n0, K, v, se, vth, vp) in rows if sel(f, sh, n0)]
    if not q: return
    w = np.array([1 / s**2 for d, s, K in q]); d = np.array([d for d, s, K in q]); mu = (w * d).sum() / w.sum(); e = 1 / math.sqrt(w.sum())
    print('%-58s files %2d clouds %7d  variance less (1.0169.. x theory - 0.0414): %+.4f (%.4f)  %+.1f errors; chi2 %.1f on %d' % (name, len(q), sum(K for d, s, K in q), mu, e, mu / e, (w * (d - mu)**2).sum(), len(q) - 1))
first8 = 'runs/exact-quarter-100000.jsonl'
for sh in ('disc', 'ellipse', 'triangle', 'rtriangle', 'square', 'hexagon', 'halfdisc', 'quarter'):
    pool(lambda f, s, n: s == sh and f != first8, sh + ', every set but the first 8,000 quarter discs')
pool(lambda f, s, n: s == 'quarter' and 'q2-' in f, 'quarter, the four sealed sets of the second sheet')
pool(lambda f, s, n: s == 'quarter' and 'q2-' in f and n == 100000, 'quarter, sealed, 100,000')
pool(lambda f, s, n: s == 'quarter' and 'q2-' in f and n == 30000, 'quarter, sealed, 30,000')
pool(lambda f, s, n: s in ('triangle', 'square', 'hexagon', 'quarter', 'halfdisc', 'rtriangle') and f != first8, 'every shape with corners or flat sides')
pool(lambda f, s, n: s in ('triangle', 'square', 'hexagon') and f != first8, 'the polygons')
pool(lambda f, s, n: s in ('disc', 'ellipse'), 'discs and the ellipse (earlier sets)')
pool(lambda f, s, n: s not in ('disc', 'ellipse') and f != first8 and n == 30000, 'shapes other than discs, 30,000')
pool(lambda f, s, n: s not in ('disc', 'ellipse') and f != first8 and n == 100000, 'shapes other than discs, 100,000')
