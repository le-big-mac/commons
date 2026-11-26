"""The two slopes of the climb with their errors, from the four sizes in climb.json.
usage: python -I climbfit.py climb.json > climbfit.out      (numpy)
Added 26 November 2026: the page had the slopes without errors, and a reader showed that the time's slope cannot tell 2/5 from 1/2."""
import sys, json
sys.dont_write_bytecode = True
import numpy as np

def fit(x, y):
    A = np.vstack([x, np.ones(len(x))]).T
    coef, res, *_ = np.linalg.lstsq(A, y, rcond=None)
    se = np.sqrt(res[0] / (len(x) - 2) / ((x - x.mean()) ** 2).sum())
    return coef[0], se

if __name__ == '__main__':
    d = json.load(open(sys.argv[1]))
    N = np.array([q['N'] for q in d], float); h = np.array([q['peak'] for q in d], float); t = np.array([q['when'] for q in d], float)
    print("sizes", [int(n) for n in N], "runs", [q['runs'] for q in d])
    for name, y, rivals in (("height of the top", h, (-0.25, -0.27, -0.30)), ("time of the top", t, (0.5, 0.42, 0.4))):
        s, e = fit(np.log(N), np.log(y))
        print(f"{name}: slope {s:+.3f} +- {e:.3f} (least squares on the four points; the error is from their scatter about the line, two degrees of freedom)")
        print("   in standard errors from " + ", ".join(f"{r:+.2f}: {(s - r) / e:+.1f}" for r in rivals))
    for p in (0.25, 0.30):
        print(f"height x N^{p:.2f}: " + ", ".join(f"{a * n ** p:.2f}" for a, n in zip(h, N)))
