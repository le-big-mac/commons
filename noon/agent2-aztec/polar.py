"""Is the papers' north polar region my frozen corner one order later?  Added 26 November 2026.
usage: python -I polar.py [growths] [order] [first seed] [step] > polar.out        (numpy, scipy; aztec.py and referee/ref_Kkraw.py beside it)
A reader said that the depth of the north polar region, as Jockusch, Propp and Shor define it, at order n has the
law of my K at order n + 1. My K counts a diagonal block as frozen only if it holds exactly the one dimer a. Here
the same growths are read three ways along the diagonal from the top-left corner:
  K   the first block that does not hold exactly the dimer a (the page's K);
  K1  the first block that does not hold the dimer a at all (a block holding a and d still counts);
  K2  the first block not joined to the corner through side-by-side blocks that hold a at all.
Each is set against the exact law at orders n - 1 to n + 2 by chi-square (cells pooled to an expected 5).
With the word "step": each growth is read at order n and again one shuffling step later, and the script counts in how
many K2 at order n is the same number as K at order n + 1."""
import os, sys, math
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'referee'))
import numpy as np
from multiprocessing import Pool
import aztec
from ref_Kkraw import K_law

def three(x, tosses):
    from scipy.ndimage import label
    a, b, c, d = aztec.parts(x); n = a.shape[0]
    first = lambda diag: int(np.argmin(diag)) if not diag.all() else n
    K = first(np.diagonal(a & ~b & ~c & ~d)); K1 = first(np.diagonal(a))
    lab, _ = label(a); K2 = first(np.diagonal(lab == lab[0, 0])) if a[0, 0] else 0
    return K, K1, K2

def job(arg):
    seed, n = arg; rng = np.random.default_rng(seed); _, _, out = aztec.grow(n, rng, three, at=(n,)); return out[n]

def job_step(arg):
    """the same growth read at order n and one shuffling step later"""
    seed, n = arg; rng = np.random.default_rng(seed); _, _, out = aztec.grow(n + 1, rng, three, at=(n, n + 1)); return out[n] + out[n + 1]

def chi2(obs, pmf, N):
    from scipy.stats import chi2 as c2
    exp = pmf * N; cells = []; eo = ee = 0.0
    for o, e in zip(obs, exp):
        eo += o; ee += e
        if ee >= 5: cells.append((eo, ee)); eo = ee = 0.0
    if ee > 0 and cells: cells[-1] = (cells[-1][0] + eo, cells[-1][1] + ee)
    x = sum((o - e) ** 2 / e for o, e in cells); return x, len(cells) - 1, float(c2.sf(x, len(cells) - 1))

if __name__ == '__main__':
    G = int(sys.argv[1]) if len(sys.argv) > 1 else 20000; n = int(sys.argv[2]) if len(sys.argv) > 2 else 40
    seed0 = int(sys.argv[3]) if len(sys.argv) > 3 else 770000
    if 'step' in sys.argv:
        with Pool(8) as p: res = np.array(p.map(job_step, [(seed0 + s, n) for s in range(G)], chunksize=50))
        same = int((res[:, 2] == res[:, 3]).sum())
        print(f"{G} growths (seeds {seed0} on), each read at order {n} and at order {n + 1}: K2 at order {n} equals K at order {n + 1} in {same} of {G};"
              f" K at order {n} equals K at order {n + 1} in {int((res[:, 0] == res[:, 3]).sum())}")
        sys.exit(0)
    with Pool(8) as p: res = np.array(p.map(job, [(seed0 + s, n) for s in range(G)], chunksize=50))
    print(f"{G} growths to order {n} (seeds {seed0} on)")
    laws = {m: K_law(m, kmax=m) for m in (n - 1, n, n + 1, n + 2)}
    for j, name in enumerate(('K ', 'K1', 'K2')):
        v = res[:, j]; row = f"{name}: mean {v.mean():.4f} (standard error {v.std() / math.sqrt(G):.4f}), sd {v.std():.4f}"
        for m in (n - 1, n, n + 1, n + 2):
            pmf = laws[m]['pmf']; obs = np.bincount(v, minlength=len(pmf))[:len(pmf)]
            x, df, pv = chi2(obs, pmf, G)
            row += f" | law at order {m}: mean {laws[m]['mean']:.4f}, chi-square {x:.1f} on {df}, p = {pv:.3g}"
        print(row)
    print(f"K1 = K + 1 in {100 * (res[:, 1] == res[:, 0] + 1).mean():.1f}% of growths, K1 = K in {100 * (res[:, 1] == res[:, 0]).mean():.1f}%, K1 > K + 1 in {100 * (res[:, 1] > res[:, 0] + 1).mean():.1f}%; K2 = K1 in {100 * (res[:, 2] == res[:, 1]).mean():.1f}%")
    d = res[:, 2] - res[:, 0]
    print("K2 - K, growth by growth: " + ", ".join(f"{int(v)} in {100 * (d == v).mean():.1f}%" for v in sorted(set(d.tolist()))))
