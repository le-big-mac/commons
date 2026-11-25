# Referee, step 2: my own statistics of runs-after/ and the pooled "excess" figures, several lawful ways.
import json, glob, os, math, sys
import numpy as np
al, D = 1.3259, 1.081
Q = {'disc': 4/3, 'disc0': 4/3, 'ellipse': 4/3, 'triangle': 4/3, 'square': 4/3, 'hexagon': 4/3,
     'halfdisc': 1.33038, 'quarter': 1.33115, 'rtriangle': 1.30562}      # the author's I A/T^2 (mine agree within my error)
line = {s: D / al**2 * q - 4/9 for s, q in Q.items()}
rng = np.random.default_rng(12345)
def stats(x, n):
    K = len(x); m = x.mean(); v = x.var(ddof=1); wn = v * n / m**2
    m4 = ((x - m)**4).mean(); sev = math.sqrt((m4 - (K - 3) / (K - 1) * v * v) / K)
    return K, m, v, sev, wn, wn * sev / v      # se of wn: the mean's part is negligible
rows = []
def load(f):
    Dd = [json.loads(l) for l in open(f) if l.strip()]
    return Dd[0]['shape'], Dd[0]['kind'], Dd[0]['n0'], np.array([d['layers'] for d in Dd], float), np.array([d['same'] for d in Dd]), np.array([d['seed'] for d in Dd])
seen = {}
for folder, tag in (('/home/agent2/peel/shape/runs', 'sheet'), ('/home/agent2/peel/shape/runs-after', 'fresh')):
    for f in sorted(glob.glob(folder + '/*.jsonl')):
        shape, kind, n0, x, same, seeds = load(f)
        K, m, v, sev, wn, sewn = stats(x, n0)
        dup = len(set(seeds.tolist()) & seen.get('all', set())); seen.setdefault('all', set()).update(seeds.tolist())
        if kind != 'exact': continue
        r = wn / line[shape]; rows.append((tag, shape, n0, K, wn, sewn, r, sewn / line[shape], os.path.basename(f)))
        if tag == 'fresh':
            print('fresh %-28s K=%6d mean %.3f var %.4f +-%.4f  w n %.4f +-%.4f  line %.4f  ratio %.4f +-%.4f  z=%+.1f  same=1: %d  seeds %d..%d shared with earlier files: %d' % (
                os.path.basename(f), K, m, v, sev, wn, sewn, line[shape], r, sewn / line[shape], (wn - line[shape]) / sewn, (same == 1).sum(), seeds.min(), seeds.max(), dup))
def pool(sel, name):
    q = [(r, s) for (tag, shape, n0, K, wn, sewn, r, s, f) in rows if sel(tag, shape, n0, f)]
    w = np.array([1 / s**2 for r, s in q]); r = np.array([r for r, s in q]); mu = (w * r).sum() / w.sum()
    chi = (w * (r - mu)**2).sum(); below = int((r < 1).sum())
    print('%-78s sets %2d (below their line: %d)  ratio %.4f +-%.4f  (%+.1f errors from 1)  chi2 among them %.1f on %d' % (name, len(q), below, mu, 1 / math.sqrt(w.sum()), (mu - 1) * math.sqrt(w.sum()), chi, len(q) - 1))
    return mu, 1 / math.sqrt(w.sum())
print()
pool(lambda t, s, n, f: n == 100000 and t == 'sheet', '100,000: the sheet\'s 9 sets')
a = pool(lambda t, s, n, f: n == 100000, '100,000: all 13 files (12 "sets")')
pool(lambda t, s, n, f: n == 100000 and t == 'fresh', '100,000: fresh clouds only (4 files)')
pool(lambda t, s, n, f: n == 100000 and s != 'quarter', '100,000: all but the quarter disc')
pool(lambda t, s, n, f: n == 100000 and s != 'quarter' and f != 'exact-disc-100000.jsonl' or (n == 100000 and t == 'fresh' and s == 'disc'), '100,000: all but the quarter disc and the sheet\'s disc set (the "high draw")')
pool(lambda t, s, n, f: n == 100000 and s == 'quarter', '100,000: the quarter disc, 84,000 clouds, against its own line')
pool(lambda t, s, n, f: n == 100000 and s == 'quarter' and t == 'fresh', '100,000: the quarter disc, fresh 76,000')
pool(lambda t, s, n, f: n == 100000 and s in ('disc', 'triangle', 'rtriangle'), '100,000: the three shapes also run at 30,000 (disc sets both)')
b = pool(lambda t, s, n, f: n == 30000, '30,000: 3 sets')
print('difference 100,000 less 30,000: %.4f +- %.4f' % (a[0] - b[0], math.hypot(a[1], b[1])))
pool(lambda t, s, n, f: True, 'both sizes, every exact set')
# the quarter disc against the ceiling and against "the common level"
q = [(wn, s) for (tag, shape, n0, K, wn, s, r, sr, f) in rows if shape == 'quarter']
w = np.array([1 / s**2 for wn, s in q]); wq = (w * np.array([x for x, s in q])).sum() / w.sum(); sq = 1 / math.sqrt(w.sum())
print('quarter disc, 84,000 clouds: w n = %.4f +- %.4f; own line %.4f (%+.1f); ceiling %.4f (%+.1f)' % (wq, sq, line['quarter'], (wq - line['quarter']) / sq, line['disc'], (wq - line['disc']) / sq))
for nm, sel in (('six ceiling sets of the sheet', lambda t, s, n, f: t == 'sheet' and n == 100000 and s in ('disc', 'disc0', 'ellipse', 'triangle', 'square', 'hexagon')),
                ('the same with the fresh discs in place of the sheet\'s', lambda t, s, n, f: n == 100000 and ((t == 'sheet' and s in ('disc0', 'ellipse', 'triangle', 'square', 'hexagon')) or (t == 'fresh' and s == 'disc')))):
    qq = [(wn, s) for (tag, shape, n0, K, wn, s, r, sr, f) in rows if sel(tag, shape, n0, f)]
    w = np.array([1 / s**2 for wn, s in qq]); lv = (w * np.array([x for x, s in qq])).sum() / w.sum(); sl = 1 / math.sqrt(w.sum())
    fq = [(wn, s) for (tag, shape, n0, K, wn, s, r, sr, f) in rows if shape == 'quarter' and tag == 'fresh']
    w2 = np.array([1 / s**2 for wn, s in fq]); wf = (w2 * np.array([x for x, s in fq])).sum() / w2.sum(); sf = 1 / math.sqrt(w2.sum())
    like = lv * line['quarter'] / line['disc']
    print('%s: level %.4f +- %.4f (%+.1f from the ceiling); fresh quarter %.4f +- %.4f is %+.1f errors from that level as printed, %+.1f from the level scaled to the quarter\'s own line (%.4f); all 84,000: %+.1f' % (
        nm, lv, sl, (lv - line['disc']) / sl, wf, sf, (wf - lv) / math.hypot(sf, sl), (wf - like) / math.hypot(sf, sl), like, (wq - like) / math.hypot(sq, sl)))
