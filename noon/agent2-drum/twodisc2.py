"""Two even discs, one on the other, with free radii and a fixed added mass: the least largest miss, by differential evolution
(after3.py's section 3, at the weights of the table).   usage: python -u twodisc2.py WEIGHT     (one weight a run; unregistered)"""
import sys
src = open(__file__.replace("twodisc2.py", "after3.py")).read(); ns = {}; sys.argv, argv = [sys.argv[0], "none"], sys.argv; exec(src[:src.index("if '1' in SEC:")], ns); sys.argv = argv
from scipy.optimize import differential_evolution
tied, modes, discs = ns['tied'], ns['modes'], ns['discs']; M = float(sys.argv[1])
def g(y, N=800):
    ko, ki, share = max(y[0], y[1]), min(y[0], y[1]), y[2]; return tied(modes(discs([share * M / ko ** 2, (1 - share) * M / ki ** 2], [ko, ki], N), N))
best = None
for seed in (4, 5):
    r = differential_evolution(g, [(0.2, 0.7), (0.08, 0.5), (0.0, 1.0)], seed=seed, tol=1e-7, maxiter=150, popsize=15)
    if best is None or r.fun < best.fun: best = r
    print(f"   seed {seed}: {100 * r.fun:.3f}%", flush=True)
x = best.x; print(f"added mass {M:5.2f}: two discs with free radii, least largest miss {100 * best.fun:.3f}% ({100 * g(x, 4000):.3f}% with 4,000 cells); radii {max(x[0], x[1]):.3f} and {min(x[0], x[1]):.3f}; {100 * x[2]:.0f}% of the mass in the wider disc")
