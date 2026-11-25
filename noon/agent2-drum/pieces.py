"""A second method for the ringed load, not tied to the 40 rings: three even pieces with free edges (a core disc, a hoop, a wider
ring), of a fixed added mass, searched by differential evolution on cells that an edge may cut (as in after3.py).
usage: python -u pieces.py WEIGHT SEED     (unregistered; one line a run)"""
import sys, json
import numpy as np
src = open(__file__.replace("pieces.py", "after3.py")).read(); ns = {}; argv = sys.argv; sys.argv = [argv[0], "none"]; exec(src[:src.index("if '1' in SEC:")], ns); sys.argv = argv
from scipy.optimize import differential_evolution
tied, modes, discs = ns['tied'], ns['modes'], ns['discs']; M = float(sys.argv[1]); seed = int(sys.argv[2])
def shape(y):
    r1, r2, r3, r4, r5 = np.sort(y[:5]); s1, s2 = y[5], y[6]; s3 = 1 - s1 - s2; areas = (r1 ** 2, r3 ** 2 - r2 ** 2, r5 ** 2 - r4 ** 2)
    if s3 < 0 or min(areas) < 2e-4: return None
    L = [s * M / a for s, a in zip((s1, s2, s3), areas)]; return (r1, r2, r3, r4, r5), L
def g(y, N=800):
    sh = shape(y)
    if sh is None: return 1.0
    (r1, r2, r3, r4, r5), L = sh; return tied(modes(discs([L[0], L[1], -L[1], L[2], -L[2]], [r1, r3, r2, r5, r4], N), N))
r = differential_evolution(g, [(0.02, 0.6)] * 5 + [(0.0, 1.0)] * 2, seed=seed, tol=1e-8, maxiter=400, popsize=14, polish=True); (r1, r2, r3, r4, r5), L = shape(r.x)
print(f"added mass {M:5.2f}, seed {seed}: three pieces, least largest miss {100 * r.fun:.3f}% ({100 * g(r.x, 4000):.3f}% with 4,000 cells): a core of +{L[0]:.1f} inside {r1:.3f}; a hoop of +{L[1]:.1f} from {r2:.3f} to {r3:.3f}; a ring of +{L[2]:.1f} from {r4:.3f} to {r5:.3f}", flush=True)
json.dump(dict(weight=M, seed=seed, miss=float(r.fun), miss4000=float(g(r.x, 4000)), radii=[float(x) for x in (r1, r2, r3, r4, r5)], loads=[float(x) for x in L]), open(f"pieces-{M:g}-{seed}.json", "w"))
