"""Is the rule i/(N + 1) for evenly spaced tempos the same as a coupling of 1 + 1/N with the rule (i - 1/2)/N?
Expectations sealed in shift-prediction.md before this was run (26 November 2026).
usage: python -I shift.py shift.json        (numpy, scipy; onset.py beside it; ten jobs on five cores)"""
import os, sys, json
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from scipy.stats import norm
import onset as O
from concurrent.futures import ProcessPoolExecutor
JOBS = [(100, 100, 4000), (200, 80, 4000), (400, 60, 4000), (800, 16, 6000), (1600, 8, 8000)]
OLD_PLUS = {100: (0.1863, 0.0007), 200: (0.1396, 0.0009), 400: (0.1042, 0.0009), 800: (0.0796, 0.0014), 1600: (0.0599, 0.0014)}   # long6.json, 22 November
OLD_HALF = {100: 0.1519, 200: 0.1159, 400: 0.0888, 800: 0.0682, 1600: 0.0523}

def job(args):
    which, N, runs, T, seed = args
    if which == 'c':
        q = (np.arange(1, N + 1) - 0.5) / N; K = 1.0 + 1.0 / N
    else:
        q = np.arange(1, N + 1) / (N + 1); K = 1.0
    om = np.tile(np.sqrt(np.pi / 8) * norm.ppf(q), (runs, 1)); rng = np.random.default_rng(seed)
    r, r2, _, _ = O.simulate(om, K, T, rng)
    return dict(which=which, N=N, runs=runs, T=T, K=K, mean_r=float(r.mean()), se=float(r.std(ddof=1) / np.sqrt(runs)))

if __name__ == '__main__':
    jobs = [(w, N, runs, T, 2600 + 10 * j + i) for j, w in enumerate(('c', 'b')) for i, (N, runs, T) in enumerate(JOBS)]
    with ProcessPoolExecutor(max_workers=5) as ex: res = list(ex.map(job, jobs[::-1]))[::-1]
    json.dump(res, open(sys.argv[1], 'w'))
    C = {q['N']: q for q in res if q['which'] == 'c'}; B = {q['N']: q for q in res if q['which'] == 'b'}
    Ns = [j[0] for j in JOBS]
    print("size   (c) (i-1/2)/N at K=1+1/N    (b) i/(N+1) at K=1, fresh    (c)/(b)-1     22 Nov (b)        fresh-old in s.e.   my recipe at K=1 was below old (b) by")
    g1 = g2 = g3 = True
    for N in Ns:
        c, b = C[N], B[N]; ob, ose = OLD_PLUS[N]
        rel = c['mean_r'] / b['mean_r'] - 1; relse = abs(c['mean_r'] / b['mean_r']) * np.hypot(c['se'] / c['mean_r'], b['se'] / b['mean_r'])
        z = (b['mean_r'] - ob) / np.hypot(b['se'], ose)
        print(f"{N:5d}   {c['mean_r']:.4f} +- {c['se']:.4f}          {b['mean_r']:.4f} +- {b['se']:.4f}          {100 * rel:+5.1f}% +- {100 * relse:.1f}   {ob:.4f} +- {ose:.4f}   {z:+5.1f}              {100 * (1 - OLD_HALF[N] / ob):4.1f}%")
        g1 &= abs(rel) < 0.05; g2 &= abs(z) < 3
        if N <= 400: g3 &= b['mean_r'] > c['mean_r']
    n = np.log(Ns)
    sc = np.polyfit(n, np.log([C[N]['mean_r'] for N in Ns]), 1)[0]; sb = np.polyfit(n, np.log([B[N]['mean_r'] for N in Ns]), 1)[0]
    print(f"slopes over the five sizes: (c) {sc:+.4f}, fresh (b) {sb:+.4f}; difference {sc - sb:+.4f}")
    print("the sealed lines:")
    print(f"  G1 (every size within 5%): {'held' if g1 else 'failed'}")
    print(f"  G2 (fresh (b) within three standard errors of 22 November's at every size): {'held' if g2 else 'failed'}")
    print(f"  G3 ((b) above (c) at 100, 200 and 400): {'held' if g3 else 'failed'}")
    print(f"  G4 (slopes within 0.015): {'held' if abs(sc - sb) < 0.015 else 'failed'}")
