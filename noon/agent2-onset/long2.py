"""Afterwards: one more size for the long series (evenly spaced Gaussian tempos, K = 1): N = 12,800, four runs of 30,000 time units.
usage: python long2.py long2.json     (same reading as long.py: the later half of each quarter; r = mean of the third and fourth quarters)"""
import sys, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import onset as O
from concurrent.futures import ProcessPoolExecutor
N, T = 12800, 30000
def job(seed):
    rng = np.random.default_rng(seed); om = O.regular('gauss', N, 1); th = None; q = []
    for _ in range(4):
        r, _, th, _ = O.simulate(om, 1.0, T / 4, rng, th=th); q.append(float(r[0]))
    return q
if __name__ == '__main__':
    with ProcessPoolExecutor(max_workers=4) as ex: Q = np.array(list(ex.map(job, [600, 601, 602, 603])))
    half = (Q[:, 2] + Q[:, 3]) / 2; r = float(half.mean()); sd = float(half.std(ddof=1))
    print(f"N = {N}, 4 runs, T = {T}: r = {r:.4f} (sd {sd:.4f}); later half of each quarter: " + ", ".join(f"{x:.4f}" for x in Q.mean(0)) + "; each run: " + ", ".join(f"{x:.4f}" for x in half))
    L = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'long.json')))['sizes']
    n = np.array([q['N'] for q in L] + [N]); rr = np.array([q['r'] for q in L] + [r])
    print(f"slope over the eight sizes 100 to 12,800: {np.polyfit(np.log(n), np.log(rr), 1)[0]:+.3f}; from 6,400 to 12,800 alone: {np.log(r / L[-1]['r']) / np.log(2):+.2f}; the seven-size line extended to 12,800 gives {np.exp(np.polyval(np.polyfit(np.log(n[:-1]), np.log(rr[:-1]), 1), np.log(N))):.4f}")
    json.dump(dict(N=N, T=T, runs=4, r=r, sd=sd, quarters=Q.mean(0).tolist(), each=half.tolist()), open(sys.argv[1], 'w'))
