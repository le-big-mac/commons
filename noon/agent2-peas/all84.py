"""All 84 degrees of freedom of Fisher's table as single tests of one degree each, and three models of tidying fitted to them.
usage: python -I all84.py all84.json        The decomposition is the one stated in all84-prediction.md."""
import sys, os, math, json
import numpy as np
from scipy.stats import norm, kstest
sys.path.insert(0, os.path.dirname(os.path.abspath(sys.argv[0])))
import data
rng = np.random.default_rng(84)
def states(label, loci):
    out = []
    for L in loci:
        l = L.lower(); out.append('H' if L + l in label else 'D' if L in label else 'R' if l in label else '?')
    assert '?' not in out, label; return tuple(out)
def decompose(classes, nloci, name):
    """classes: list of (states, count). Returns (description, a, b) for tests of 1 to 1, character by character."""
    tests = []
    def rec(prefix, i):
        if i == nloci: return
        sub = [(s, c) for s, c in classes if s[:i] == prefix]; tot = {}
        for s, c in sub: tot[s[i]] = tot.get(s[i], 0) + c
        where = ("within " + "".join(prefix) if prefix else "margin")
        if len(tot) == 3:
            tests.append((f"{name}: character {i + 1}, hybrid against constant, {where}", tot['H'], tot['D'] + tot['R'])); tests.append((f"{name}: character {i + 1}, one constant form against the other, {where}", tot['D'], tot['R']))
        else:
            ks = sorted(tot); assert len(ks) == 2; tests.append((f"{name}: character {i + 1}, {where}", tot[ks[0]], tot[ks[1]]))
        for k in sorted(tot): rec(prefix + (k,), i + 1)
    rec((), 0); return tests
def zscore(counts, parts):
    n = sum(counts); p = parts[0] / sum(parts); return (counts[0] - n * p) / math.sqrt(n * p * (1 - p))
T35 = [e for e in data.E if e[1] in ("seven", "eight", "twenty plants")]
Z = [(e[0], zscore(e[2], e[3])) for e in T35]
nine = [e for e in data.E if e[1] == "nine kinds"][0]; labs9 = ("AB", "Ab", "aB", "ab", "ABb", "aBb", "AaB", "Aab", "AaBb")
new = decompose([(states(l, "AB"), c) for l, c in zip(labs9, nine[2])], 2, "two characters")
new += decompose([(states(l, "ABC"), c) for l, c in data.K27], 3, "three characters")
BC = {"back-cross 1": ("AB", "ABb", "AaB", "AaBb"), "back-cross 3": ("AB", "ABb", "AaB", "AaBb"), "back-cross 2": ("AaBb", "Aab", "aBb", "ab"), "back-cross 4": ("AaBb", "Aab", "aBb", "ab"),
      "back-cross, flower colour and stem": ("AaBb", "aBb", "Aab", "ab")}
for e in data.E:
    if e[1] == "back-crosses": new += decompose([(states(l, "AB"), c) for l, c in zip(BC[e[0]], e[2])], 2, e[0])
assert len(new) == 49, len(new)
Z += [(nm, (a - b) / math.sqrt(a + b)) for nm, a, b in new]; names = [n for n, _ in Z]; z = np.array([v for _, v in Z]); n = len(z); assert n == 84
print(f"1. {n} tests of one degree of freedom: 35 as before and {len(new)} from the seven tests with several classes")
for nm, a, b in new:
    if abs((a - b) / math.sqrt(a + b)) >= 1.2: print(f"      {nm}: {a} against {b}, z = {(a - b) / math.sqrt(a + b):+.3f}")
print(f"   sum of z squared {float((z ** 2).sum()):.4f} (Fisher's total on the classes as he grouped them: 41.6055); the 49 new ones {float((z[35:] ** 2).sum()):.4f} (as grouped: 21.8064)")
k = int(np.argmax(abs(z))); small = int((abs(z) < 0.3).sum()); print(f"   largest |z| {abs(z).max():.4f} ({names[k]}); honest chance that 84 tests all stay at or below it: {(2 * norm.cdf(abs(z).max()) - 1) ** 84:.5f}")
print(f"   |z| below 0.3: {small} of 84 (of the 49 new ones: {int((abs(z[35:]) < 0.3).sum())}); an honest experimenter would expect {84 * (2 * norm.cdf(0.3) - 1):.1f}")
for lo, hi in ((0, 0.3), (0.3, 0.6), (0.6, 0.9), (0.9, 1.2), (1.2, 1.5), (1.5, 1.8), (1.8, 9)):
    print(f"      |z| from {lo} to {hi if hi < 9 else 'up'}: {int(((abs(z) >= lo) & (abs(z) < hi)).sum()):2d}; honest {84 * 2 * (norm.cdf(hi) - norm.cdf(lo)):.1f}")
print("2. Three models of tidying, each with one fitted number, on the 84 values")
def fits(zv):
    m = len(zv); s2 = float(np.mean(zv ** 2)); c = float(np.max(abs(zv))); p = 2 * norm.sf(abs(zv))
    ll_h = 0.0                                                                             # log-likelihoods relative to the honest model (density of p equal to 1)
    ll_s = float(np.sum(-math.log(math.sqrt(s2)) - zv ** 2 / (2 * s2) + zv ** 2 / 2))       # every deviation shrunk to a share sqrt(s2)
    ll_c = -m * math.log(2 * norm.cdf(c) - 1)                                              # nothing beyond c
    # between two data values the likelihood rises with the threshold, so its supremum is just below a data value (or at 1); corrected after the referee's report
    ps = np.sort(p); cs = np.concatenate([[0.0], np.cumsum(np.log(2 * ps))]); best = (-1e18, None)
    for k in range(m + 1):
        a = float(ps[k]) if k < m else 1.0; l = float(cs[k] + (m - k) * math.log(1 + a))
        if l > best[0]: best = (l, a)
    return dict(s=math.sqrt(s2), c=c, a=best[1], ll_s=ll_s, ll_c=ll_c, ll_a=best[0], small=int((abs(zv) < 0.3).sum()))
F = fits(z); p = 2 * norm.sf(abs(z))
print(f"   shrunk: every deviation {F['s']:.3f} of honest; log-likelihood over honest {F['ll_s']:+.3f}")
print(f"   cut-off: nothing beyond {F['c']:.3f} standard deviations (a chance of a worse fit below {2 * norm.sf(F['c']):.3f}); {F['ll_c']:+.3f}")
print(f"   better of two (Pires and Branco's rule): done again when the chance of a worse fit is below {F['a']:.4f} (the supremum, approached from below); {F['ll_a']:+.3f};   at their own value, 0.201: {float(np.sum(np.where(p <= 0.201, np.log(2 * p), math.log(1.201)))):+.3f}")
lr = math.exp(F['ll_c'] - F['ll_s']); print(f"   cut-off over shrunk: a factor of {lr:.2f}; better-of-two over shrunk: {math.exp(F['ll_a'] - F['ll_s']):.2f}; cut-off over better-of-two: {math.exp(F['ll_c'] - F['ll_a']):.2f}")
N = 20000; sim = rng.normal(0, F['s'], (N, n)); S = [fits(r) for r in sim[:N]]
share_lr = float(np.mean([s['ll_c'] - s['ll_s'] >= F['ll_c'] - F['ll_s'] for s in S])); share_small = float(np.mean([s['small'] <= small for s in S])); share_a = float(np.mean([s['ll_a'] - s['ll_s'] >= F['ll_a'] - F['ll_s'] for s in S]))
print(f"   {N} sets of 84 from the shrunk model as fitted: cut-off beats it by as much or more in {100 * share_lr:.1f}% of sets; better-of-two beats it by as much or more in {100 * share_a:.1f}%; {small} or fewer values below 0.3 in {100 * share_small:.1f}% (on average {np.mean([s['small'] for s in S]):.1f})")
def sim_best2(a, size):
    u = rng.random(size); v = rng.random(size); return np.where(u < a, np.maximum(u, v), u)          # p-values under the better-of-two rule
pa = sim_best2(F['a'], (N, n)); za = norm.isf(pa / 2) * rng.choice([-1, 1], (N, n))
print(f"   {N} sets from the better-of-two rule as fitted: mean sum of z squared {float((za ** 2).sum(axis=1).mean()):.1f} (observed {float((z ** 2).sum()):.1f}); a sum as small as observed in {100 * float(((za ** 2).sum(axis=1) <= (z ** 2).sum()).mean()):.1f}%; largest |z| as small as observed in {100 * float((abs(za).max(axis=1) <= abs(z).max()).mean()):.1f}%; values below 0.3 on average {float((abs(za) < 0.3).sum(axis=1).mean()):.1f}")
print(f"      under that rule: {small} or fewer values below 0.3 in {100 * float(((abs(za) < 0.3).sum(axis=1) <= small).mean()):.1f}% of sets; a sum as large as observed or larger in {100 * float(((za ** 2).sum(axis=1) >= (z ** 2).sum()).mean()):.1f}%")
uc = rng.uniform(norm.cdf(-F['c']), norm.cdf(F['c']), (N, n)); zc = norm.ppf(uc)
print(f"   {N} sets from the cut-off model as fitted: mean sum of z squared {float((zc ** 2).sum(axis=1).mean()):.1f}; a sum as small as observed in {100 * float(((zc ** 2).sum(axis=1) <= (z ** 2).sum()).mean()):.1f}%; values below 0.3 on average {float((abs(zc) < 0.3).sum(axis=1).mean()):.1f}")
print("3. How the chances of a worse fit (p) are spread: Kolmogorov's distance from each model")
cdf_h = lambda x: x
cdf_c = lambda x: np.clip((x - 2 * norm.sf(F['c'])) / (1 - 2 * norm.sf(F['c'])), 0, 1)
cdf_s = lambda x: 2 * norm.sf(norm.isf(x / 2) / F['s'])
cdf_a = lambda x: np.where(x <= F['a'], x ** 2, (1 + F['a']) * x - F['a'])
for nm, f in (("honest", cdf_h), ("shrunk", cdf_s), ("cut-off", cdf_c), ("better of two", cdf_a)):
    r = kstest(p, f); print(f"   {nm:14s} distance {r.statistic:.4f}" + (f"; chance of a larger one {r.pvalue:.4f}" if nm == "honest" else "  (its number was fitted to these data, so no chance is given)"))
json.dump(dict(z=[float(v) for v in z], names=names, sum=float((z ** 2).sum()), max=float(abs(z).max()), max_name=names[k], small=small, lr=lr, share_lr=share_lr, share_small=share_small, fit=F), open(sys.argv[1], 'w'), indent=1)
