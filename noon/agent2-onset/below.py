"""Afterwards: the fluctuations below the onset.  N x mean r^2 at K = 0.5 with its standard error; random against evenly spaced tempos; two sizes.
usage: python below.py below.json"""
import sys, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import onset as O
from concurrent.futures import ProcessPoolExecutor
def job(args):
    kind, N, runs, K, seed = args
    rng = np.random.default_rng(seed); om = O.regular('gauss', N, runs) if kind == 'regular' else O.random('gauss', N, runs, rng)
    _, r2, _, _ = O.simulate(om, K, 200, rng); x = N * r2
    return dict(kind=kind, N=N, runs=runs, K=K, value=float(x.mean()), se=float(x.std(ddof=1) / np.sqrt(runs)))
if __name__ == '__main__':
    jobs = [(kind, N, 100, K, 700 + i) for i, (kind, N, K) in enumerate([('random', 1000, 0.5), ('regular', 1000, 0.5), ('random', 4000, 0.5), ('regular', 4000, 0.5), ('random', 1000, 0.0), ('regular', 1000, 0.0), ('random', 1000, 0.25), ('random', 1000, 0.75)])]
    with ProcessPoolExecutor(max_workers=8) as ex: res = list(ex.map(job, jobs))
    for q in res:
        print(f"{q['kind']:8s} N = {q['N']:5d}, K = {q['K']:.2f}, {q['runs']} runs: N x mean r^2 = {q['value']:.3f} +- {q['se']:.3f}   (1/(1 - K) = {1 / (1 - q['K']):.2f})")
    json.dump(res, open(sys.argv[1], 'w'))
