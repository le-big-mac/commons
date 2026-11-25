"""After the referee: its checks redone with my code, and my runs set against the exact law of K that it supplied.
usage: python after.py > after.out      (the exact law is K_law() in referee/ref_Kkraw.py, imported as it stands; I have not re-derived it)"""
import sys, os, json, math, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'referee'))
import numpy as np
import aztec as A
from ref_Kkraw import K_law
rng = np.random.default_rng(1)
def scan(x):
    a, b, c, d = (p.copy() for p in A.parts(x)); n = a.shape[0]; out = np.zeros((n, n), bool)
    for i in range(n):
        for j in range(n):
            if a[i, j] or b[i, j] or c[i, j] or d[i, j]: continue
            if i > 0 and (c[i - 1, j] or d[i - 1, j]): continue
            if i < n - 1 and (a[i + 1, j] or b[i + 1, j]): continue
            if j > 0 and (b[i, j - 1] or d[i, j - 1]): continue
            if j < n - 1 and (a[i, j + 1] or c[i, j + 1]): continue
            out[i, j] = True; a[i, j] = d[i, j] = True
    return out
def empty_before(x):                                   # the blocks of the new array that hold nothing before step 2
    n2 = x.shape[0]; y = np.zeros((n2 + 2, n2 + 2), bool); y[1:-1, 1:-1] = x; a, b, c, d = A.parts(y); return ~(a | b | c | d), int((a & d).sum() + (b & c).sum())
print("1. The rule in holes() against a plain scan in reading order, and against 'the blocks that were empty before the deletion'")
x = np.zeros((2, 2), bool); w = A.holes(x); A.fill(x, w, rng.random(int(w.sum())) < 0.5); same_scan = same_pre = True; counts = True
for order in range(2, 201):
    pre, dele = empty_before(x); y = A.shuffle(x); h = A.holes(y)
    if order <= 60: same_scan &= bool((h == scan(y)).all())
    same_pre &= bool((h == pre).all()); counts &= int(h.sum()) == order + dele
    A.fill(y, h, rng.random(int(h.sum())) < 0.5); x = y
print(f"   orders 2 to 60: equal to the plain scan at every step: {same_scan}; orders 2 to 200: equal to the blocks empty before the deletion: {same_pre}; holes = order + deleted pairs at every step: {counts}")
print("2. The rule as sealed, order 3: what the 80 configurations are")
def rec(x, order, target, found, rule):
    if order == target: found.append((x.tobytes(), A.is_tiling(x))); return
    y = A.shuffle(x) if order else np.zeros((2, 2), bool); w = rule(y)
    for toss in itertools.product((False, True), repeat=int(w.sum())):
        z = y.copy(); A.fill(z, w, np.array(toss, bool)); rec(z, order + 1, target, found, rule)
bad = []; rec(None, 0, 3, bad, A.fillable); good = []; rec(None, 0, 3, good, A.holes)
tb = {k for k, ok in bad if ok}; tg = {k for k, ok in good}
print(f"   {len({k for k, _ in bad})} configurations: {len(tb)} tilings and {len({k for k, ok in bad if not ok})} that are not; {len(tg - tb)} of the {len(tg)} tilings never appear")
print("3. The referee's exact law of K against every tiling of orders 4 and 5 (my own enumeration)")
for n in (4, 5):
    found = []; rec(None, 0, n, found, A.holes); T = {k for k, _ in found}; ks = []
    for k in T:
        xx = np.frombuffer(k, dtype=bool).reshape(2 * n, 2 * n); a, b, c, d = A.parts(xx); oa = np.diagonal(a & ~b & ~c & ~d); ks.append(int(np.argmin(oa)) if not oa.all() else n)
    mine = np.bincount(ks, minlength=n + 1) / len(ks); law = K_law(n, kmax=n)['pmf']
    print(f"   order {n}: share of the {len(T):,} tilings with K = 0, 1, ...: {', '.join(f'{v:.6f}' for v in mine[:n])}; the law: {', '.join(f'{v:.6f}' for v in law[:n])}; largest difference {np.abs(mine[:n] - law[:n]).max():.1e}")
print("4. My hundred runs against the exact law")
R = json.load(open('runs.json')); sizes = [100, 200, 400, 800, 1600]; lim = (1 - 1 / math.sqrt(2)) / 2; ex = {n: K_law(n) for n in sizes}
for n in sizes:
    K = np.array([r[str(n)]['K'] for r in R]); e = ex[n]
    print(f"   n = {n:5d}: mean K {K.mean():.2f} (exact {e['mean']:.3f}; z = {(K.mean() - e['mean']) / (e['sd'] / 10):+.1f}); sd {K.std(ddof=1):.2f} (exact {e['sd']:.3f}); excess over the circle {K.mean() - lim * n:.2f} blocks = {(K.mean() - lim * n) / n ** (1 / 3):.2f} n^(1/3) (exact {(e['mean'] - lim * n) / n ** (1 / 3):.3f})")
sd = [np.std([r[str(n)]['K'] for r in R], ddof=1) for n in sizes]
print(f"   exponent of the sd: five sizes {np.polyfit(np.log(sizes), np.log(sd), 1)[0]:.3f}; without 1,600: {np.polyfit(np.log(sizes[:4]), np.log(sd[:4]), 1)[0]:.3f}; the exact law over the five sizes: {np.polyfit(np.log(sizes), np.log([ex[n]['sd'] for n in sizes]), 1)[0]:.3f}")
Km = np.array([[r[str(n)]['K'] for n in sizes] for r in R]); print("   correlation of K between neighbouring sizes of the same growth: " + ", ".join(f"{np.corrcoef(Km[:, i], Km[:, i + 1])[0, 1]:.2f}" for i in range(4)))
print("5. How much is deleted at each step (one growth, read at orders 200, 400, 800)")
x = np.zeros((2, 2), bool); w = A.holes(x); A.fill(x, w, rng.random(int(w.sum())) < 0.5)
for order in range(2, 801):
    pre, dele = empty_before(x)
    if order in (200, 400, 800):
        n = order - 1; a, b, c, d = A.parts(x); two = (a & d) | (b & c); one = (a | b | c | d) & ~two
        print(f"   going to order {order}: {dele:,} facing pairs deleted = {2 * dele / (n * (n + 1)):.2f} of the {n * (n + 1):,} dominoes; fills {order + dele:,}")
    y = A.shuffle(x); h = A.holes(y); A.fill(y, h, rng.random(int(h.sum())) < 0.5); x = y
