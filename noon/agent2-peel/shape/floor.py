"""floor.py: how far below the ceiling can a convex shape fall? A search, in a family wide enough to hold shapes I have not thought of.
python -I floor.py run [WORKERS]   makes floor.json;   python -I floor.py   prints from it.

The family. A polygon whose sides have outward normals among the 24 directions 0, 15, ..., 345 degrees: the set of points x with
x.n_k <= h_k for all k (a line that does not touch the set gives no side). The polygon is scaled to area pi and then swollen by a disc
of radius rho (every corner becomes an arc of that radius). 25 numbers: log h_k and log rho. Moving the origin and scaling h change
nothing, so the family has 22 dimensions; it holds every triangle, quadrilateral, ... with sides in those directions, sharp or rounded.
A shape more than 3 times as wide one way as another (over the 24 directions) is refused: flow.c is less sure of long thin shapes, and
an affine map would make such a shape a rounder one with corners that are not arcs of circles, which this family does not hold.

The figure. Q = I A / T^2 by flow.c (I from the edge), at 240 angles, at step quality 2 and 1, carried to the limit (twice the
second less the first): about a second, and within 0.0002 of the figure at 1,440 angles on the three shapes I tried.

The search. CMA-ES (Hansen's (mu/mu_w, lambda) evolution strategy with rank-one and rank-mu updates of the covariance; written here),
24 shapes a generation, at most 120 generations, stopped early when the best has not improved by 0.00001 in 30. Eight starts: three
from the equilateral triangle swollen by 0.2 (step 0.15 in the logs), five from polygons drawn at random (log h normal with spread
0.25, rho 0.1 times a log-normal of spread 0.5; step 0.25). Seeds 1 to 8. The five best shapes of all, no two from the same start,
are then run again as the theory's table was: 1,440 angles, step quality 0.5 and 0.25."""
import json, math, os, subprocess, sys
import numpy as np
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); KEPT = os.path.join(HERE, 'floor.json'); NDIR = 24
ANG = np.radians(np.arange(NDIR) * 360.0 / NDIR); NX, NY = np.cos(ANG), np.sin(ANG)
def polygon(h):
    """the corners, counter-clockwise, of the set x.n_k <= h_k; None if it is empty or unbounded"""
    P = [(-50.0, -50.0), (50.0, -50.0), (50.0, 50.0), (-50.0, 50.0)]
    for k in range(NDIR):
        Q = []; n = len(P)
        for i in range(n):
            a, b = P[i], P[(i + 1) % n]; da, db = a[0] * NX[k] + a[1] * NY[k] - h[k], b[0] * NX[k] + b[1] * NY[k] - h[k]
            if da <= 0: Q.append(a)
            if (da < 0 < db) or (db < 0 < da): t = da / (da - db); Q.append((a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1])))
        P = Q
        if len(P) < 3: return None
    out = []
    for p in P:
        if not out or math.hypot(p[0] - out[-1][0], p[1] - out[-1][1]) > 1e-9: out.append(p)
    if len(out) > 1 and math.hypot(out[0][0] - out[-1][0], out[0][1] - out[-1][1]) <= 1e-9: out.pop()
    if len(out) < 3 or max(max(abs(p[0]), abs(p[1])) for p in out) > 49: return None
    return out
def describe(x):
    """the polygon of the 25 numbers x, scaled to area pi: corners, sides (direction in degrees, length), rho, how many times wider one way than another"""
    P = polygon(np.exp(x[:NDIR]))
    if P is None: return None
    A = 0.5 * sum(P[i][0] * P[(i + 1) % len(P)][1] - P[(i + 1) % len(P)][0] * P[i][1] for i in range(len(P)))
    if A < 1e-9: return None
    s = math.sqrt(math.pi / A); P = [(p[0] * s, p[1] * s) for p in P]; sides = []
    for i in range(len(P)):
        a, b = P[i], P[(i + 1) % len(P)]; L = math.hypot(b[0] - a[0], b[1] - a[1]); d = math.degrees(math.atan2(-(b[0] - a[0]), b[1] - a[1])) % 360.0       # the outward normal of a side run counter-clockwise
        sides.append((round(d / 15.0) * 15 % 360, L))
    rho = float(np.exp(x[NDIR])); w = [max(p[0] * NX[k] + p[1] * NY[k] for p in P) - min(p[0] * NX[k] + p[1] * NY[k] for p in P) + 2 * rho for k in range(NDIR // 2)]
    return {'corners': P, 'sides': sides, 'rho': rho, 'aspect': max(w) / min(w)}
def Q_of(x, M=240, qs=('2', '1'), timeout=90):
    d = describe(x)
    if d is None or not (1e-3 <= d['rho'] <= 1.5) or d['aspect'] > 3: return 2.0
    name = 'poly:' + ','.join('%.12f,%.12f' % p for p in d['corners']); out = []
    for q in qs:
        try: o = json.loads(subprocess.run(['nice', '-n', '19', os.path.join(HERE, 'flow'), name, str(M), '-q', q, '-rho0', '%.10f' % d['rho']], capture_output=True, text=True, timeout=timeout).stdout)
        except Exception: return 2.0
        out.append(o['I_edge'] * o['area'] / o['T'] ** 2)
    v = 2 * out[1] - out[0]
    return v if 1.0 < v < 1.4 else 2.0
def triangle_start():
    h = np.full(NDIR, 5.0); h[[2, 10, 18]] = 1.0        # normals at 30, 150 and 270 degrees: an equilateral triangle; the other lines far off
    return np.concatenate([np.log(h), [math.log(0.2)]])
def cma(x0, sigma, seed, pool, lam=24, gens=120):
    rng = np.random.default_rng(seed); n = len(x0); mu = lam // 2; w = np.log(mu + 0.5) - np.log(np.arange(1, mu + 1)); w /= w.sum(); mueff = 1 / (w ** 2).sum()
    cc = (4 + mueff / n) / (n + 4 + 2 * mueff / n); cs = (mueff + 2) / (n + mueff + 5); c1 = 2 / ((n + 1.3) ** 2 + mueff); cmu = min(1 - c1, 2 * (mueff - 2 + 1 / mueff) / ((n + 2) ** 2 + mueff)); damps = 1 + 2 * max(0, math.sqrt((mueff - 1) / (n + 1)) - 1) + cs
    chiN = math.sqrt(n) * (1 - 1 / (4 * n) + 1 / (21 * n * n)); m = np.array(x0, float); C = np.eye(n); pc = np.zeros(n); ps = np.zeros(n); best = (2.0, None); hist = []; since = 0
    for g in range(gens):
        ev, B = np.linalg.eigh(C); ev = np.maximum(ev, 1e-20); D = np.sqrt(ev); Z = rng.standard_normal((lam, n)); Y = (Z * D) @ B.T; X = m + sigma * Y
        f = np.array(list(pool.map(Q_of, X))); order = np.argsort(f)
        if f[order[0]] < best[0] - 1e-5: since = 0
        else: since += 1
        if f[order[0]] < best[0]: best = (float(f[order[0]]), X[order[0]].copy())
        hist.append(float(f[order[0]])); ysel = Y[order[:mu]]; yw = w @ ysel; m = m + sigma * yw
        ps = (1 - cs) * ps + math.sqrt(cs * (2 - cs) * mueff) * (B @ ((B.T @ yw) / D)); hs = np.linalg.norm(ps) / math.sqrt(1 - (1 - cs) ** (2 * (g + 1))) / chiN < 1.4 + 2 / (n + 1)
        pc = (1 - cc) * pc + (hs * math.sqrt(cc * (2 - cc) * mueff)) * yw
        C = (1 - c1 - cmu) * C + c1 * (np.outer(pc, pc) + (0 if hs else cc * (2 - cc)) * C) + cmu * (ysel.T * w) @ ysel; C = (C + C.T) / 2
        sigma *= math.exp((cs / damps) * (np.linalg.norm(ps) / chiN - 1))
        if since >= 30: break
    return best, hist
if len(sys.argv) > 1 and sys.argv[1] == 'run':
    workers = int(sys.argv[2]) if len(sys.argv) > 2 else 6; res = []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        for seed in range(1, 9):
            rng = np.random.default_rng(1000 + seed)
            if seed <= 3: x0, sg, kind = triangle_start(), 0.15, 'the rounded equilateral triangle'
            else: x0, sg, kind = np.concatenate([rng.normal(0, 0.25, NDIR), [math.log(0.1) + rng.normal(0, 0.5)]]), 0.25, 'a polygon drawn at random'
            (fb, xb), hist = cma(x0, sg, seed, pool); res.append({'seed': seed, 'start': kind, 'start_Q': Q_of(x0), 'best_Q': fb, 'x': [float(v) for v in xb], 'generations': len(hist), 'history': hist})
            json.dump({'runs': res}, open(KEPT, 'w'))
            print('start %d (%s): from %.5f to %.5f in %d generations' % (seed, kind, res[-1]['start_Q'], fb, len(hist)), flush=True)
        top = sorted(res, key=lambda r: r['best_Q'])[:5]; fine = list(pool.map(lambda r: Q_of(np.array(r['x']), 1440, ('0.5', '0.25'), 1800), top))
    for r, v in zip(top, fine): r['fine_Q'] = v
    json.dump({'runs': res}, open(KEPT, 'w'))
if __name__ == '__main__' and os.path.exists(KEPT):
    runs = json.load(open(KEPT))['runs']; print('start  from                               Q at the start   best Q (240 angles)   generations   again at 1,440 angles   the best shape')
    for r in runs:
        d = describe(np.array(r['x'])); per = sum(L for a, L in d['sides']); big = sorted([(L / per, a) for a, L in d['sides'] if L / per > 0.03], reverse=True)
        print('%d      %-34s %.5f          %.5f               %3d           %s            %d sides over 3 in 100 of the flat edge (%s); rho %.3f; %.2f times wider one way' % (r['seed'], r['start'], r['start_Q'], r['best_Q'], r['generations'], ('%.5f' % r['fine_Q']) if 'fine_Q' in r else '   -   ', len(big), ', '.join('%d deg %.2f' % (a, f) for f, a in big), d['rho'], d['aspect']))
    fin = [r for r in runs if 'fine_Q' in r]
    if fin: b = min(fin, key=lambda r: r['fine_Q']); print('the least, at 1,440 angles: %.5f (start %d); the rounded triangle of the runs has 1.30562 and the equilateral triangle swollen by 0.25 has 1.30555' % (b['fine_Q'], b['seed']))
