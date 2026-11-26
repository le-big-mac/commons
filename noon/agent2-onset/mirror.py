"""The mirror of shift.py: does the rule i/(N + 1) at a coupling of 1 - 1/N rest where the rule (i - 1/2)/N rests at 1?
Expectations sealed in mirror-prediction.md before this was run (26 November 2026).
usage: python -I mirror.py mirror.json        (numpy, scipy; onset.py beside it; five jobs on five cores)"""
import os, sys, json
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from scipy.stats import norm
import onset as O
from concurrent.futures import ProcessPoolExecutor
JOBS = [(100, 100, 4000), (200, 80, 4000), (400, 60, 4000), (800, 16, 6000), (1600, 8, 8000)]
OLD_HALF = {100: (0.1519, 0.0005), 200: (0.1159, 0.0006), 400: (0.0888, 0.0007), 800: (0.0682, 0.0015), 1600: (0.0523, 0.0014)}   # long6.json, 22 November: (i - 1/2)/N at K = 1
OLD_PLUS = {100: 0.1863, 200: 0.1396, 400: 0.1042, 800: 0.0796, 1600: 0.0599}                                                       # the same run: i/(N + 1) at K = 1

def job(args):
    N, runs, T, seed = args
    q = np.arange(1, N + 1) / (N + 1); K = 1.0 - 1.0 / N
    om = np.tile(np.sqrt(np.pi / 8) * norm.ppf(q), (runs, 1)); rng = np.random.default_rng(seed)
    r, r2, _, _ = O.simulate(om, K, T, rng)
    return dict(N=N, runs=runs, T=T, K=K, mean_r=float(r.mean()), se=float(r.std(ddof=1) / np.sqrt(runs)))

if __name__ == '__main__':
    jobs = [(N, runs, T, 3700 + i) for i, (N, runs, T) in enumerate(JOBS)]
    with ProcessPoolExecutor(max_workers=5) as ex: res = list(ex.map(job, jobs[::-1]))[::-1]
    json.dump(res, open(sys.argv[1], 'w'))
    D = {q['N']: q for q in res}; Ns = [j[0] for j in JOBS]
    print("size   (d) i/(N+1) at K=1-1/N    my rule at K=1, 22 Nov    (d)/mine-1 (% of mine)   in s.e. of the difference   the rule's own value at K=1 is above mine by")
    h1 = h3 = True
    for N in Ns:
        d = D[N]; a, ase = OLD_HALF[N]
        rel = d['mean_r'] / a - 1; relse = (d['mean_r'] / a) * np.hypot(d['se'] / d['mean_r'], ase / a); z = (d['mean_r'] - a) / np.hypot(d['se'], ase)
        print(f"{N:5d}   {d['mean_r']:.4f} +- {d['se']:.4f}        {a:.4f} +- {ase:.4f}        {100 * rel:+6.2f}% +- {100 * relse:.2f}          {z:+5.1f}                       {100 * (OLD_PLUS[N] / a - 1):4.1f}%")
        h1 &= abs(rel) < 0.05
        if N <= 400: h3 &= d['mean_r'] > a
    n = np.log(Ns); sd = np.polyfit(n, np.log([D[N]['mean_r'] for N in Ns]), 1)[0]; sa = np.polyfit(n, np.log([OLD_HALF[N][0] for N in Ns]), 1)[0]
    print(f"slopes over the five sizes: (d) {sd:+.4f}; my rule at K = 1 {sa:+.4f}; difference {sd - sa:+.4f}")
    print("the sealed lines:")
    print(f"  H1 (every size within 5% of my rule's value): {'held' if h1 else 'failed'}")
    print(f"  H2 (slope within 0.020 of -0.384): {sd:+.4f} -> {'held' if abs(sd - (-0.384)) < 0.020 else 'failed'}")
    print(f"  H3 ((d) above my rule's value at 100, 200 and 400): {'held' if h3 else 'failed'}")
