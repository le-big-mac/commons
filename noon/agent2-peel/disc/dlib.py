"""dlib.py: the clouds of the disc study read from their files, and the few things computed from them. Used by study.py and after.py.
Each line of runs/KIND-N.jsonl is one cloud (rings.c): for each of 19 annuli (radius 0.05, 0.10, ..., 0.95, each +- 0.008) the sums
[points, depth - profile, depth, depth^2, rho, rho^2, rho x depth, then for m = 1..4: cos, sin, depth x cos, depth x sin of m theta]."""
import glob, gzip, json, math, os, random, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import dtheory as th
RUNS = os.environ.get('DISC_RUNS') or os.path.join(HERE, 'runs'); TRY = bool(os.environ.get('DISC_RUNS'))
RAD = [0.05 * (k + 1) for k in range(19)]
def K(r): return int(round(r / 0.05)) - 1
def lines(kind, n):
    """the clouds of one kind and size, a line of JSON each; the published folder holds the files gzipped"""
    f = os.path.join(RUNS, '%s-%d.jsonl' % (kind, n))
    if os.path.exists(f): return [l for l in open(f) if l.strip()]
    if os.path.exists(f + '.gz'): return [l for l in gzip.open(f + '.gz', 'rt') if l.strip()]
    return None
def load(kind, n):
    ls = lines(kind, n)
    if ls is None: return None
    rows = [json.loads(l) for l in ls]; a = np.array([r['rings'] for r in rows])            # clouds x 19 x 23
    cnt = a[:, :, 0]; d = {'n0': n, 'kind': kind, 'clouds': len(rows), 'npts': np.array([r['n'] for r in rows]), 'layers': np.array([r['layers'] for r in rows], float), 'seeds': [r['seed'] for r in rows]}
    d['Q'] = a[:, :, 1] / cnt                                                                                  # the ring's mean: depth less the profile
    sdd = a[:, :, 3] - a[:, :, 2] ** 2 / cnt; srr = a[:, :, 5] - a[:, :, 4] ** 2 / cnt; srd = a[:, :, 6] - a[:, :, 4] * a[:, :, 2] / cnt
    d['V'] = (sdd - srd ** 2 / srr) / (cnt - 2)                                                                # the variance round the ring: about the line fitted to depth against radius
    d['tot'] = sdd / cnt; d['cnt'] = cnt; dbar = a[:, :, 2] / cnt; d['P'] = {}
    for m in (1, 2, 3, 4):
        c = 2 * (a[:, :, 5 + 4 * m] - dbar * a[:, :, 3 + 4 * m]) / cnt; s = 2 * (a[:, :, 6 + 4 * m] - dbar * a[:, :, 4 + 4 * m]) / cnt; d['P'][m] = (c ** 2 + s ** 2) / 4
    return d
def var(x): return float(np.var(x, ddof=1))
def sev(x): return var(x) * math.sqrt(2.0 / (len(x) - 1))                 # the standard error of a variance of nearly normal things
def corr(d, r1, r2): return float(np.corrcoef(d['Q'][:, K(r1)], d['Q'][:, K(r2)])[0, 1])
def secorr(d, r1, r2, n=400, seed=1):
    rng = random.Random(seed); N = d['clouds']; out = []
    for _ in range(n):
        idx = [rng.randrange(N) for _ in range(N)]; out.append(float(np.corrcoef(d['Q'][idx, K(r1)], d['Q'][idx, K(r2)])[0, 1]))
    return float(np.std(out))
def pred_ring(kind, r, n): return th.annulus(th.cov_chance if kind == 'chance' else th.cov_fixed, r, r, n)
def pred_corr(kind, r1, r2, n):
    c = th.cov_chance if kind == 'chance' else th.cov_fixed; return th.annulus(c, r1, r2, n) / math.sqrt(th.annulus(c, r1, r1, n) * th.annulus(c, r2, r2, n))
def sizes_in(runs=None): return sorted(set(int(os.path.basename(f).split('-')[1].split('.')[0]) for f in glob.glob(os.path.join(runs or RUNS, '*-*.jsonl')) + glob.glob(os.path.join(runs or RUNS, '*-*.jsonl.gz'))))
NAME = {'chance': 'number left to chance', 'exact': 'exactly n points'}
