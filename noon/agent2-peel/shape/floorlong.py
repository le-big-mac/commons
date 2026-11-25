"""floorlong.py: the search of floor.py again, with more patience. Not on any sheet.   python -I floorlong.py run [WORKERS [FIRST LAST]]; python -I floorlong.py
(FIRST and LAST: which of the ten starts to run; each start's record is kept in floorlong-N.json, and the table is made from whichever are there.)
The sealed search (floor.py) stops a start when the best has not improved by 0.00001 in 30 generations. In 25 numbers that is
impatient: the three starts at the rounded triangle stopped after 31 generations with nothing gained, though the same strategy
needs some 190 generations to find the bottom of a plain bowl (floortest.py). Here: 14 shapes a generation (the usual number for
25 unknowns), up to 250 generations, stopped when the best has not improved by 0.00001 in 100. Ten starts:
  1, 2   the rounded equilateral triangle, small steps (0.05)
  3      a right triangle swollen by 0.2;   4   a square with a corner cut off, swollen by 0.2 (1.3105, the lowest non-triangle I had)
  5      a square swollen by 0.2;           6   a regular pentagon swollen by 0.2 (72 degrees is not among the directions: the nearest five)
  7 - 10 polygons drawn at random, as in floor.py
The best of each start is run again at 1,440 angles."""
import json, math, os, sys
import numpy as np
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
ARGV = sys.argv; sys.argv = [ARGV[0]]          # floor.py runs its own search, and writes floor.json, when "run" is on the command line of whatever
import floor as F                              # brings it in: the first time this program was run it did exactly that, and wrote over the sealed
sys.argv = ARGV                                # search's record (which was then made again; see the README). So floor.py is shown a bare command line.
def cma(x0, sigma, seed, pool, lam=14, gens=250, patience=100):
    rng = np.random.default_rng(seed); n = len(x0); mu = lam // 2; w = np.log(mu + 0.5) - np.log(np.arange(1, mu + 1)); w /= w.sum(); mueff = 1 / (w ** 2).sum()
    cc = (4 + mueff / n) / (n + 4 + 2 * mueff / n); cs = (mueff + 2) / (n + mueff + 5); c1 = 2 / ((n + 1.3) ** 2 + mueff); cmu = min(1 - c1, 2 * (mueff - 2 + 1 / mueff) / ((n + 2) ** 2 + mueff)); damps = 1 + 2 * max(0, math.sqrt((mueff - 1) / (n + 1)) - 1) + cs
    chiN = math.sqrt(n) * (1 - 1 / (4 * n) + 1 / (21 * n * n)); m = np.array(x0, float); C = np.eye(n); pc = np.zeros(n); ps = np.zeros(n); best = (2.0, None); hist = []; since = 0
    for g in range(gens):
        ev, B = np.linalg.eigh(C); ev = np.maximum(ev, 1e-20); D = np.sqrt(ev); Z = rng.standard_normal((lam, n)); Y = (Z * D) @ B.T; X = m + sigma * Y
        f = np.array(list(pool.map(F.Q_of, X))); order = np.argsort(f)
        if f[order[0]] < best[0] - 1e-5: since = 0
        else: since += 1
        if f[order[0]] < best[0]: best = (float(f[order[0]]), X[order[0]].copy())
        hist.append(float(f[order[0]])); ysel = Y[order[:mu]]; yw = w @ ysel; m = m + sigma * yw
        ps = (1 - cs) * ps + math.sqrt(cs * (2 - cs) * mueff) * (B @ ((B.T @ yw) / D)); hs = np.linalg.norm(ps) / math.sqrt(1 - (1 - cs) ** (2 * (g + 1))) / chiN < 1.4 + 2 / (n + 1)
        pc = (1 - cc) * pc + (hs * math.sqrt(cc * (2 - cc) * mueff)) * yw
        C = (1 - c1 - cmu) * C + c1 * (np.outer(pc, pc) + (0 if hs else cc * (2 - cc)) * C) + cmu * (ysel.T * w) @ ysel; C = (C + C.T) / 2
        sigma *= math.exp((cs / damps) * (np.linalg.norm(ps) / chiN - 1))
        if since >= patience: break
    return best, hist, float(sigma)
def lines(idx, hs=None, rho=0.2):
    h = np.full(F.NDIR, 5.0); h[list(idx)] = 1.0 if hs is None else hs; return np.concatenate([np.log(h), [math.log(rho)]])
def starts():
    out = [('the rounded equilateral triangle', F.triangle_start(), 0.05), ('the rounded equilateral triangle', F.triangle_start(), 0.05),
           ('a right triangle swollen by 0.2', lines((18, 12, 3), [1, 1, math.sqrt(2)]), 0.1), ('a square with a corner cut off, swollen by 0.2', lines((18, 0, 3, 6, 12), [0.5, 0.5, 0.1 / math.sqrt(2), 0.5, 0.5]), 0.1),
           ('a square swollen by 0.2', lines((0, 6, 12, 18)), 0.1), ('a pentagon swollen by 0.2', lines((0, 5, 10, 14, 19)), 0.1)]
    for seed in range(7, 11): rng = np.random.default_rng(2000 + seed); out.append(('a polygon drawn at random', np.concatenate([rng.normal(0, 0.25, F.NDIR), [math.log(0.1) + rng.normal(0, 0.5)]]), 0.25))
    return out
if __name__ == '__main__' and len(sys.argv) > 1 and sys.argv[1] == 'run':          # only when this file is the program run, never when another brings it in
    workers = int(sys.argv[2]) if len(sys.argv) > 2 else 14; first, last = (int(sys.argv[3]), int(sys.argv[4])) if len(sys.argv) > 4 else (1, 10)
    with ThreadPoolExecutor(max_workers=workers) as pool:
        for seed, (kind, x0, sg) in enumerate(starts(), 1):
            if not (first <= seed <= last): continue
            (fb, xb), hist, sig = cma(x0, sg, 100 + seed, pool); r = {'seed': seed, 'start': kind, 'start_Q': F.Q_of(x0), 'best_Q': fb, 'x': [float(v) for v in xb], 'generations': len(hist), 'history': hist, 'last_step': sig}
            r['fine_Q'] = F.Q_of(np.array(r['x']), 1440, ('0.5', '0.25'), 1800)          # the start's best shape again, as the theory's table was run
            json.dump(r, open(os.path.join(HERE, 'floorlong-%d.json' % seed), 'w')); print('start %d (%s): from %.5f to %.5f in %d generations; at 1,440 angles %.5f' % (seed, kind, r['start_Q'], fb, len(hist), r['fine_Q']), flush=True)
have = [os.path.join(HERE, 'floorlong-%d.json' % k) for k in range(1, 11) if os.path.exists(os.path.join(HERE, 'floorlong-%d.json' % k))]
if __name__ == '__main__' and have:
    runs = [json.load(open(f)) for f in have]; print('start  from                                             Q at the start   best Q (240 angles)   generations   again at 1,440 angles   the best shape')
    for r in runs:
        d = F.describe(np.array(r['x'])); per = sum(L for a, L in d['sides']); big = sorted([(L / per, a) for a, L in d['sides'] if L / per > 0.03], reverse=True)
        print('%-2d     %-48s %.5f          %.5f               %3d           %s            %d sides over 3 in 100 of the flat edge (%s); %d sides in all; rho %.3f; %.2f times wider one way' % (r['seed'], r['start'], r['start_Q'], r['best_Q'], r['generations'], ('%.5f' % r['fine_Q']) if 'fine_Q' in r else '   -   ', len(big), ', '.join('%d deg %.2f' % (a, f) for f, a in big), len(d['sides']), d['rho'], d['aspect']))
    fin = [r for r in runs if 'fine_Q' in r]
    if fin: b = min(fin, key=lambda r: r['fine_Q']); print('the least, at 1,440 angles: %.5f (start %d)' % (b['fine_Q'], b['seed']))
