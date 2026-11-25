"""Afterwards: does the slope at rest depend on how r is averaged, or on exactly how the evenly spaced tempos are placed?
Sizes 100 to 1,600 at K = 1, run lengths and numbers of runs as in long.py; r read over the second half of each run.
usage: python long6.py long6.json"""
import sys, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from scipy.stats import norm
import onset as O
from concurrent.futures import ProcessPoolExecutor
JOBS = [(100, 100, 4000), (200, 80, 4000), (400, 60, 4000), (800, 16, 6000), (1600, 8, 8000)]
def job(args):
    recipe, N, runs, T, seed = args
    q = (np.arange(1, N + 1) - 0.5) / N if recipe == 'half' else np.arange(1, N + 1) / (N + 1)
    om = np.tile(np.sqrt(np.pi / 8) * norm.ppf(q), (runs, 1)); rng = np.random.default_rng(seed)
    r, r2, _, _ = O.simulate(om, 1.0, T, rng)
    return dict(recipe=recipe, N=N, runs=runs, T=T, mean_r=float(r.mean()), se=float(r.std(ddof=1) / np.sqrt(runs)), rms=float(np.sqrt(r2.mean())))
if __name__ == '__main__':
    jobs = [(rec, N, runs, T, 900 + 10 * j + i) for j, rec in enumerate(('half', 'plus')) for i, (N, runs, T) in enumerate(JOBS)]
    with ProcessPoolExecutor(max_workers=8) as ex: res = list(ex.map(job, jobs[::-1]))[::-1]
    for rec, name in (('half', "tempos at the quantiles (i - 1/2)/N, as everywhere else"), ('plus', "tempos at the quantiles i/(N + 1)")):
        R = [q for q in res if q['recipe'] == rec]; n = np.log([q['N'] for q in R])
        print(f"{name}:")
        print("   mean r over the second half: " + ", ".join(f"{q['mean_r']:.4f}" for q in R) + f"; slope {np.polyfit(n, np.log([q['mean_r'] for q in R]), 1)[0]:+.3f}")
        print("   root mean square of r:       " + ", ".join(f"{q['rms']:.4f}" for q in R) + f"; slope {np.polyfit(n, np.log([q['rms'] for q in R]), 1)[0]:+.3f}")
    json.dump(res, open(sys.argv[1], 'w'))
