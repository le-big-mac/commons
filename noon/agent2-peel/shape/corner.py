"""corner.py: an equilateral triangle whose round corners have a radius of curvature that varies across the corner. On no sheet.
python -I corner.py run [WORKERS]   makes corner.json;   python -I corner.py   prints from it.
The referee's blind step for the second sheet found, in four minutes, a shape lower than my search's lowest: the same triangle with
corners gentler beside the sides and sharper at the tip. Here that family is searched with my own program (flow2.c, which is flow.c
with an option to add waves to the support function). The triangle has inradius 1; across each corner (120 degrees of the normal's
angle, x running from 0 to 360 degrees across it) the radius of curvature is
        R = d (1 - s cos x - t cos 2x - u cos 3x),
so d is the mean radius, and s = t = u = 0 is the corner that is an arc of a circle. R must stay positive. The search: the
evolution strategy of floor.py in these four numbers, 8 shapes a generation, 70 generations, from the referee's shape
(d = 0.34, s = -0.6); each shape at 720 angles, step quality 1 and 0.5, carried to the limit. The best is run again at 1,440
angles (0.5 and 0.25), and so are the circular corner and the referee's shape."""
import json, math, os, subprocess, sys
import numpy as np
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); KEPT = os.path.join(HERE, 'corner.json'); SC = math.sqrt(math.pi / (3 * math.sqrt(3)))
XS = np.linspace(0, 2 * math.pi, 721)
def Q(p, M=720, qs=('1', '0.5')):
    d, s, t, u = p
    if not (0.02 < d < 1.5) or (1 - s * np.cos(XS) - t * np.cos(2 * XS) - u * np.cos(3 * XS)).min() <= 0.02: return 2.0
    out = []
    for q in qs:
        cmd = ['nice', '-n', '19', os.path.join(HERE, 'flow2'), 'triangle', str(M), '-q', q, '-rho0', '%.10f' % (d * SC)]
        for m, c in ((3, s / 8.0), (6, t / 35.0), (9, u / 80.0)):                 # R = h + h'': a wave cos(m theta) in h is -(m^2 - 1) cos(m theta) in R
            if c: cmd += ['-add', str(m), '%.12f' % (d * SC * c), '30']
        try: o = json.loads(subprocess.run(cmd, capture_output=True, text=True, timeout=600).stdout)
        except Exception: return 2.0
        out.append(o['I_edge'] * o['area'] / o['T'] ** 2)
    v = 2 * out[1] - out[0]; return v if 1.0 < v < 1.4 else 2.0
def cma(f, x0, sigma, seed, pool, lam=8, gens=70):
    rng = np.random.default_rng(seed); n = len(x0); mu = lam // 2; w = np.log(mu + 0.5) - np.log(np.arange(1, mu + 1)); w /= w.sum(); mueff = 1 / (w ** 2).sum()
    cc = (4 + mueff / n) / (n + 4 + 2 * mueff / n); cs = (mueff + 2) / (n + mueff + 5); c1 = 2 / ((n + 1.3) ** 2 + mueff); cmu = min(1 - c1, 2 * (mueff - 2 + 1 / mueff) / ((n + 2) ** 2 + mueff)); damps = 1 + 2 * max(0, math.sqrt((mueff - 1) / (n + 1)) - 1) + cs
    chiN = math.sqrt(n) * (1 - 1 / (4 * n) + 1 / (21 * n * n)); m = np.array(x0, float); C = np.eye(n); pc = np.zeros(n); ps = np.zeros(n); best = (2.0, None); hist = []
    for g in range(gens):
        ev, B = np.linalg.eigh(C); D = np.sqrt(np.maximum(ev, 1e-20)); Y = (rng.standard_normal((lam, n)) * D) @ B.T; X = m + sigma * Y; fv = np.array(list(pool.map(f, X))); order = np.argsort(fv)
        if fv[order[0]] < best[0]: best = (float(fv[order[0]]), X[order[0]].copy())
        hist.append(float(fv[order[0]])); ysel = Y[order[:mu]]; yw = w @ ysel; m = m + sigma * yw
        ps = (1 - cs) * ps + math.sqrt(cs * (2 - cs) * mueff) * (B @ ((B.T @ yw) / D)); hs = np.linalg.norm(ps) / math.sqrt(1 - (1 - cs) ** (2 * (g + 1))) / chiN < 1.4 + 2 / (n + 1)
        pc = (1 - cc) * pc + (hs * math.sqrt(cc * (2 - cc) * mueff)) * yw; C = (1 - c1 - cmu) * C + c1 * (np.outer(pc, pc) + (0 if hs else cc * (2 - cc)) * C) + cmu * (ysel.T * w) @ ysel; C = (C + C.T) / 2
        sigma *= math.exp((cs / damps) * (np.linalg.norm(ps) / chiN - 1))
    return best, hist, [float(v) for v in m], float(sigma)
if __name__ == '__main__' and len(sys.argv) > 1 and sys.argv[1] == 'run':          # only when this file is the program run, never when another brings it in
    workers = int(sys.argv[2]) if len(sys.argv) > 2 else 8; circ = [0.223 / SC, 0, 0, 0]; ref = [0.34, -0.6, 0, 0]
    with ThreadPoolExecutor(max_workers=workers) as pool:
        (fb, xb), hist, mean, sig = cma(Q, ref, 0.08, 1, pool)
        fine = list(pool.map(lambda p: Q(p, 1440, ('0.5', '0.25')), [circ, ref, list(xb), mean]))
    json.dump({'history': hist, 'best720': fb, 'best': [float(v) for v in xb], 'mean': mean, 'last_step': sig, 'fine': {'circular': fine[0], 'referee': fine[1], 'best': fine[2], 'mean': fine[3]}, 'circular': circ, 'referee': ref}, open(KEPT, 'w'), indent=1)
if __name__ == '__main__' and os.path.exists(KEPT):
    j = json.load(open(KEPT)); d, s, t, u = j['best']; x = XS; R = d * (1 - s * np.cos(x) - t * np.cos(2 * x) - u * np.cos(3 * x))
    print('I A/T^2 at 1,440 angles:  the corner an arc of a circle (d = %.3f): %.5f;   the referee\'s shape (d = 0.34, s = -0.6): %.5f;   the search\'s best: %.5f;   where the search\'s mean ended: %.5f' % (j['circular'][0], j['fine']['circular'], j['fine']['referee'], j['fine']['best'], j['fine']['mean']))
    print('the search\'s best: d = %.3f, s = %.3f, t = %.3f, u = %.3f (in inradii); the radius of curvature across the corner runs from %.3f beside a side through %.3f a quarter of the way and %.3f at the tip; the least and greatest %.3f, %.3f' % (d, s, t, u, R[0], R[180], R[360], R.min(), R.max()))
    print('the search: the best of each tenth generation at 720 angles: ' + ' '.join('%.5f' % v for v in j['history'][::10]) + '; the last ' + '%.5f' % j['history'][-1] + '; the step ended at %.4f' % j['last_step'])
