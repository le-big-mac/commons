"""Afterwards: evenly spaced Gaussian tempos, K = 1, N = 400.  The 600-unit recipe read 0.074 where the resting level is 0.090.  What does r(t) do in between?
usage: python dip.py dip.json"""
import sys, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import onset as O
from concurrent.futures import ProcessPoolExecutor
def job(seed):
    rng = np.random.default_rng(seed); om = O.regular('gauss', 400, 25)
    _, _, _, rs = O.simulate(om, 1.0, 2400, rng, series=True); return rs.mean(1)
if __name__ == '__main__':
    with ProcessPoolExecutor(max_workers=8) as ex: m = np.mean(list(ex.map(job, range(800, 808))), axis=0)      # 200 runs in eight batches
    dt = O.DT; t = np.arange(len(m)) * dt; w = int(50 / dt); sm = np.convolve(m, np.ones(w) / w, mode='valid'); ts = t[:len(sm)] + 25
    edges = [0, 25, 50, 100, 150, 200, 300, 400, 500, 600, 800, 1000, 1500, 2000, 2400]
    wins = [(a, b, float(m[(t >= a) & (t < b)].mean())) for a, b in zip(edges, edges[1:])]
    print("N = 400, 200 runs: mean r in windows: " + "; ".join(f"{a}-{b}: {v:.4f}" for a, b, v in wins))
    late = float(m[(t >= 1500) & (t < 2000)].mean()); k = int(np.argmin(sm[ts >= 100])); tmin = float(ts[ts >= 100][k]); vmin = float(sm[ts >= 100][k])
    print(f"running mean over 50 time units, from t = 100 on: lowest {vmin:.4f} at t = {tmin:.0f}; level between 1500 and 2000: {late:.4f}; the lowest is {100 * (1 - vmin / late):.1f}% below it")
    print(f"the falling curve 1/sqrt(1/r0^2 + t/2) from the peak would read {1 / np.sqrt(1 / max(m) ** 2 + 450 / 2):.4f} at t = 450 and {1 / np.sqrt(1 / max(m) ** 2 + 1750 / 2):.4f} at t = 1750 (peak {max(m):.4f} at t = {t[int(np.argmax(m))]:.0f})")
    json.dump(dict(windows=wins, tmin=tmin, vmin=vmin, late=late, curve=[float(x) for x in sm[::200]]), open(sys.argv[1], 'w'))
