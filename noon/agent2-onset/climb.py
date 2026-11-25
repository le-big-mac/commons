"""Afterwards: the climb before the fall.  Evenly spaced Gaussian tempos at K = 1, from random phases: how high does the run-averaged r get, and when, at four sizes?
usage: python climb.py climb.json        (step 0.1 for the two largest sizes; the referee found no effect of the step)"""
import sys, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import onset as O
from concurrent.futures import ProcessPoolExecutor
JOBS = [(1600, 32, 600, 0.05), (6400, 16, 600, 0.05), (25600, 8, 800, 0.1), (102400, 2, 1200, 0.1)]
def job(args):
    N, runs, T, dt, seed = args
    O.DT = dt; rng = np.random.default_rng(seed); om = O.regular('gauss', N, runs)
    _, _, _, rs = O.simulate(om, 1.0, T, rng, series=True); m = rs.mean(1); w = int(round(20 / dt))
    sm = np.convolve(m, np.ones(w) / w, mode='valid'); t = (np.arange(len(sm)) + w / 2) * dt; k = int(np.argmax(sm))
    return dict(N=N, runs=runs, T=T, dt=dt, peak=float(sm[k]), when=float(t[k]), start=float(m[0]), curve=[float(x) for x in sm[::int(round(5 / dt))]])
if __name__ == '__main__':
    with ProcessPoolExecutor(max_workers=4) as ex:
        res = list(ex.map(job, [(N, runs, T, dt, 900 + i) for i, (N, runs, T, dt) in enumerate(JOBS)][::-1]))[::-1]
    for q in res:
        print(f"N = {q['N']:6d}, {q['runs']:2d} runs: starts at {q['start']:.4f}; highest (running mean over 20 time units) {q['peak']:.4f} at t = {q['when']:.0f};  (2/t)^0.5 there = {(2 / q['when']) ** 0.5:.4f}")
    N = np.log([q['N'] for q in res])
    print(f"slope of log(height) against log N: {np.polyfit(N, np.log([q['peak'] for q in res]), 1)[0]:+.3f}; of log(time of the peak): {np.polyfit(N, np.log([q['when'] for q in res]), 1)[0]:+.3f}")
    json.dump(res, open(sys.argv[1], 'w'))
