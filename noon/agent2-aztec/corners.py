"""The four-corner runs against the exact law of K (the referee's K_law).   usage: python corners.py corners-1.json corners-2.json > corners.out"""
import sys, os, json, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'referee'))
import numpy as np
from scipy.stats import chi2
from ref_Kkraw import K_law
R = [r for f in sys.argv[1:] for r in json.load(open(f))]; sizes = [100, 200, 400, 800, 1600]
print(f"{len(R)} growths, {4 * len(R)} readings a size")
V = {}; rows = {}
for n in sizes:
    K = np.array([r[str(n)] for r in R]); k = K.ravel(); law = K_law(n); N = len(k)
    sk = float(((k - k.mean()) ** 3).mean() / k.std() ** 3)
    cc = np.corrcoef(K.T); off = cc[np.triu_indices(4, 1)]
    # chi-square against the law, pooling the tails so that every cell expects at least 5
    pmf = law['pmf']; exp = N * pmf; lo = int(np.argmax(np.cumsum(exp) >= 5)); hi = len(exp) - 1 - int(np.argmax(np.cumsum(exp[::-1]) >= 5))
    cells = [exp[:lo + 1].sum()] + list(exp[lo + 1:hi]) + [exp[hi:].sum() + N * law['tail']]; obs = [(k <= lo).sum()] + [(k == v).sum() for v in range(lo + 1, hi)] + [(k >= hi).sum()]
    x2 = float(sum((o - e) ** 2 / e for o, e in zip(obs, cells))); p = float(chi2.sf(x2, len(cells) - 1))
    rows[n] = dict(mean=float(k.mean()), sd=float(k.std(ddof=1)), skew=sk, p=p, law=law)
    print(f"n = {n:5d}: mean {k.mean():.3f} (law {law['mean']:.3f}; {(k.mean() - law['mean']) / (law['sd'] / math.sqrt(N)):+.1f} se); sd {k.std(ddof=1):.3f} (law {law['sd']:.3f}; {(k.std(ddof=1) - law['sd']) / (law['sd'] / math.sqrt(2 * N)):+.1f} se); skewness {sk:+.3f} (law {law['skew']:+.3f}); chi-square {x2:.1f} on {len(cells) - 1}, p = {p:.3f}; corners correlate between {off.min():+.2f} and {off.max():+.2f}")
r = rows[1600]; V['B1'] = abs(r['mean'] - 239.645) <= 0.20; V['B2'] = abs(r['sd'] - 2.974) <= 0.15; V['B3'] = -0.40 <= r['skew'] <= -0.04
V['B4'] = all(rows[n]['skew'] < 0 for n in sizes); V['B5'] = abs(rows[800]['sd'] - 2.367) <= 0.13; V['B6'] = r['p'] > 0.01
for k_ in sorted(V): print(f"{k_}  {'held' if V[k_] else 'failed'}")
sd = [rows[n]['sd'] for n in sizes]; print(f"power of the standard deviation over the five sizes: {np.polyfit(np.log(sizes), np.log(sd), 1)[0]:.3f} (the law: {np.polyfit(np.log(sizes), np.log([rows[n]['law']['sd'] for n in sizes]), 1)[0]:.3f})")
