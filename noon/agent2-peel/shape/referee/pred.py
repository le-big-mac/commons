# Referee's predictions (from flow.py, extrapolated by hand in grid and corner radius; see flow*.out) beside the runs.
import json, glob, os, math
import numpy as np
al, D = 1.3259, 1.081
TI = {  # shape: (T, I) at area pi, with my error estimates in the report
 'disc': (0.75, 3 / (4 * math.pi)), 'disc0': (0.75, 3 / (4 * math.pi)), 'ellipse': (0.75, 3 / (4 * math.pi)),
 'square': (0.786063, 0.262242), 'triangle': (0.819926, 0.285315), 'rtriangle': (0.803421, 0.268259),
 'hexagon': (0.765121, 0.248459), 'halfdisc': (0.771335, 0.25194), 'quarter': (0.778766, 0.25695)}
A = math.pi
def pred(shape, n):
    T, I = TI[shape]
    mean = al * (n / A) ** (2 / 3) * T
    ch = D * I * n ** (1 / 3) / A ** (1 / 3)
    ex = ch - (4 / 9) * al ** 2 * T ** 2 * n ** (1 / 3) / A ** (4 / 3)
    return mean, ch, ex, I * A / T ** 2
for s in ['disc', 'square', 'triangle', 'rtriangle', 'hexagon', 'halfdisc', 'quarter']:
    m, ch, ex, Q = pred(s, 1e5)
    print('%-9s T=%.4f I=%.5f Q=%.4f  n=1e5: mean %.2f  var chance %.3f  var exact %.3f   n=3e4: exact %.3f' % (s, TI[s][0], TI[s][1], Q, m, ch, ex, pred(s, 3e4)[2]))
print()
zs = []
for f in sorted(glob.glob('/home/agent2/shape-referee/runs/*.jsonl')):
    Dd = [json.loads(l) for l in open(f) if l.strip()]
    x = np.array([d['layers'] for d in Dd], float); N = len(x)
    shape, kind, n0 = Dd[0]['shape'], Dd[0]['kind'], Dd[0]['n0']
    mean = x.mean(); var = x.var(ddof=1); m4 = ((x - mean) ** 4).mean()
    sev = math.sqrt((m4 - (N - 3) / (N - 1) * var ** 2) / N); sem = math.sqrt(var / N)
    pm, ch, ex, Q = pred(shape, n0)
    pv = ch if kind == 'chance' else ex
    z = (var - pv) / sev; zs.append((kind, n0, z, var / pv, sev / pv))
    print('%-6s %-9s %6d  N=%5d  mean %8.3f +-%.3f (pred %8.2f, diff %+.2f)  var %6.3f +-%.3f  pred %6.3f  z=%+.1f  ratio %.3f' % (
        kind, shape, n0, N, mean, sem, pm, mean - pm, var, sev, pv, z, var / pv))
for sel, name in [(lambda k, n: k == 'exact' and n == 100000, 'exact 1e5'), (lambda k, n: k == 'exact' and n == 30000, 'exact 3e4'), (lambda k, n: k == 'chance', 'chance 1e5'), (lambda k, n: True, 'all')]:
    q = [(z, r, s) for k, n, z, r, s in zs if sel(k, n)]
    w = np.array([1 / s ** 2 for z, r, s in q]); r = np.array([r for z, r, s in q])
    print('%-10s files %2d  sum z^2 = %.1f  weighted mean of measured/predicted = %.4f +- %.4f' % (name, len(q), sum(z * z for z, r, s in q), (w * r).sum() / w.sum(), 1 / math.sqrt(w.sum())))
