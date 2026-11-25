"""Afterwards: the size series at K = 1 for evenly spaced Gaussian tempos, with runs long enough to come to rest.   usage: python long.py long.json
At the critical point r falls as 1/sqrt(t/2) until it reaches its resting level r_s, so a run needs a time of several times 8/r_s^2."""
import sys, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import onset as O
from concurrent.futures import ProcessPoolExecutor
JOBS = [(100, 100, 4000), (200, 80, 4000), (400, 60, 4000), (800, 16, 6000), (1600, 8, 8000), (3200, 8, 12000), (6400, 4, 24000)]
def job(args):
    N, runs, T, seed = args
    rng = np.random.default_rng(seed); om = O.regular('gauss', N, runs); th = None; q = []
    for _ in range(4):                                  # four quarters, continuing; the second half is quarters three and four
        r, _, th, _ = O.simulate(om, 1.0, T / 4, rng, th=th); q.append(r)      # simulate() averages over the second half of what it is given, so each "quarter" reading is its later half
    q = np.array(q); half = (q[2] + q[3]) / 2
    return dict(N=N, runs=runs, T=T, r=float(half.mean()), sd=float(half.std(ddof=1)), quarters=[float(x.mean()) for x in q])
if __name__ == '__main__':
    with ProcessPoolExecutor(max_workers=7) as ex:
        res = list(ex.map(job, [(N, runs, T, 500 + i) for i, (N, runs, T) in enumerate(JOBS)][::-1]))[::-1]
    for q in res:
        print(f"N = {q['N']:5d}, {q['runs']:3d} runs, T = {q['T']:6d}: r = {q['r']:.4f} (sd {q['sd']:.4f}); later half of each quarter: " + ", ".join(f"{x:.4f}" for x in q['quarters']))
    b = np.polyfit(np.log([q['N'] for q in res]), np.log([q['r'] for q in res]), 1)[0]
    print(f"slope of log r against log N over the seven sizes: {b:+.3f}; over 400 to 6400: {np.polyfit(np.log([q['N'] for q in res[2:]]), np.log([q['r'] for q in res[2:]]), 1)[0]:+.3f}")
    json.dump(dict(sizes=res, slope=float(b)), open(sys.argv[1], 'w'))
