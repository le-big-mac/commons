"""Afterwards: why does r sit at 0.064 for evenly spaced tempos at K = 1, whatever the size?   usage: python plateau.py plateau.json
Longer runs read in windows; a smaller time step; couplings just either side of 1."""
import sys, json, math, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import onset as O
from concurrent.futures import ProcessPoolExecutor

def windows(args):
    kind, N, runs, K, T, dt, seed = args
    O.DT = dt; rng = np.random.default_rng(seed)
    om = O.regular('gauss', N, runs) if kind == 'regular' else O.random('gauss', N, runs, rng)
    _, _, _, rs = O.simulate(om, K, T, rng, series=True); t = np.arange(rs.shape[0]) * dt
    edges = [0, 50, 100, 200, 300, 600, 1200, 2400, 4800]
    w = [(a, b, float(rs[(t >= a) & (t < b)].mean())) for a, b in zip(edges, edges[1:]) if b <= T + 1e-9]
    return dict(kind=kind, N=N, runs=runs, K=K, T=T, dt=dt, windows=w, start=float(rs[0].mean()))

if __name__ == '__main__':
    jobs = [('regular', 1600, 8, 1.0, 2400, 0.05, 1), ('regular', 3200, 8, 1.0, 2400, 0.05, 2), ('regular', 6400, 4, 1.0, 1200, 0.05, 3), ('regular', 12800, 4, 1.0, 1200, 0.05, 4),
            ('regular', 3200, 8, 1.0, 600, 0.025, 5), ('regular', 3200, 8, 1.0, 600, 0.1, 6),
            ('regular', 3200, 8, 0.98, 600, 0.05, 7), ('regular', 3200, 8, 0.99, 600, 0.05, 8), ('regular', 3200, 8, 0.995, 600, 0.05, 9), ('regular', 3200, 8, 1.005, 600, 0.05, 10), ('regular', 3200, 8, 1.01, 600, 0.05, 11),
            ('regular', 12800, 4, 0.99, 600, 0.05, 12), ('regular', 12800, 4, 1.01, 600, 0.05, 13), ('random', 3200, 16, 1.0, 2400, 0.05, 14)]
    with ProcessPoolExecutor(max_workers=8) as ex:
        res = list(ex.map(windows, jobs))
    for q in res:
        print(f"{q['kind']:8s} N = {q['N']:6d}, K = {q['K']:.3f}, step {q['dt']}, {q['runs']} runs: start {q['start']:.4f}; " + "; ".join(f"{a}-{b}: {v:.4f}" for a, b, v in q['windows']))
    print("the limit of many oscillators: r = %.4f at K = 1.005, %.4f at 1.01" % (O.r_theory('gauss', 1.005), O.r_theory('gauss', 1.01)))
    json.dump(res, open(sys.argv[1], 'w'))
