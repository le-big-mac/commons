"""Afterwards: evenly spaced Gaussian tempos at K = 1, runs long enough to come to rest, read by eighths, resumable.
usage: python long4.py N T RUNS SEED0 FIRST LAST [plus]     (computes eighths FIRST..LAST of each run, continuing from long4-state/; prints the readings so far;
       with "plus" the tempos sit at the quantiles i/(N + 1) instead of (i - 1/2)/N)
A background command here may run for two hours at most, so the long runs are done in parts."""
import sys, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from scipy.stats import norm
import onset as O
from concurrent.futures import ProcessPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); STATE = os.path.join(HERE, 'long4-state')
def job(args):
    N, T, seed, first, last, recipe = args; tag = os.path.join(STATE, f"N{N}-T{T}-s{seed}" + ("-plus" if recipe == 'plus' else ""))
    done = json.load(open(tag + '.json')) if os.path.exists(tag + '.json') else []
    th = np.load(tag + '.npy') if done else None; rng = np.random.default_rng(seed)
    om = O.regular('gauss', N, 1) if recipe != 'plus' else (np.sqrt(np.pi / 8) * norm.ppf(np.arange(1, N + 1) / (N + 1)))[None, :]
    for k in range(len(done) + 1, last + 1):
        if k < first: raise SystemExit(f"{tag}: eighth {k} has not been computed yet")
        _, _, th, rs = O.simulate(om, 1.0, T / 8, rng, th=th, series=True); done.append(float(rs.mean()))
        np.save(tag + '.npy', th); json.dump(done, open(tag + '.json', 'w'))
    return done
if __name__ == '__main__':
    N, T, runs, seed0, first, last = (int(x) for x in sys.argv[1:7]); recipe = sys.argv[7] if len(sys.argv) > 7 else 'half'
    with ProcessPoolExecutor(max_workers=8) as ex: Q = np.array(list(ex.map(job, [(N, T, seed0 + i, first, last, recipe) for i in range(runs)])))
    print(f"N = {N}, T = {T}, {runs} runs, eighths 1 to {Q.shape[1]}: mean reading by eighth: " + ", ".join(f"{x:.4f}" for x in Q.mean(0)))
    if Q.shape[1] == 8:
        lastq = Q[:, 6:].mean(1); style = (Q[:, 5] + Q[:, 7]) / 2
        print(f"   last quarter: {lastq.mean():.4f}, standard error {lastq.std(ddof=1) / np.sqrt(runs):.4f}; each run: " + ", ".join(f"{x:.4f}" for x in lastq))
        print(f"   seventh and eighth eighths: {Q[:, 6].mean():.4f} and {Q[:, 7].mean():.4f}, apart by {abs(Q[:, 6].mean() - Q[:, 7].mean()) / Q[:, 6:].mean():.1%} of their mean; sixth and eighth (the reading long.py used): {style.mean():.4f}")
        json.dump(dict(N=N, T=T, runs=runs, eighths=Q.tolist(), last_quarter=float(lastq.mean()), se=float(lastq.std(ddof=1) / np.sqrt(runs))), open(os.path.join(HERE, f"long4-{'plus-' if recipe == 'plus' else ''}N{N}.json"), 'w'))
