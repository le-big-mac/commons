"""The referee's controls, redone here from data.py.   usage: python -I after2.py expectations.md
Three lawful pairs of contrasts for splitting an experiment with several classes, every order of the characters, the better-of-two
account maximised properly, the stopping rule with wider bands, and the sealed sheet's remembered counts against the page's."""
import sys, os, math, re, itertools
import numpy as np
from scipy.stats import norm, binom
sys.path.insert(0, os.path.dirname(os.path.abspath(sys.argv[0])))
import data
rng = np.random.default_rng(72)
def states(label, loci):
    return tuple('H' if L + L.lower() in label else 'D' if L in label else 'R' for L in loci)
def zt(a, b, pa):                                    # a against b, a expected with share pa
    n = a + b; return (a - n * pa) / math.sqrt(n * pa * (1 - pa))
def split(classes, order, scheme):
    out = []
    def rec(fixed, i):
        if i == len(order): return
        L = order[i]; sub = [(s, c) for s, c in classes if all(s[k] == v for k, v in fixed)]; tot = {}
        for s, c in sub: tot[s[L]] = tot.get(s[L], 0) + c
        if len(tot) == 3:
            D, H, R = tot['D'], tot['H'], tot['R']
            if scheme == 'hyb': out.extend([zt(H, D + R, 0.5), zt(D, R, 0.5)])                    # hybrid against constant; one constant against the other
            elif scheme == 'pheno': out.extend([zt(D + H, R, 0.75), zt(H, D, 2 / 3)])             # by appearance, 3 to 1; then hybrid against constant among dominants, 2 to 1
            else: out.extend([zt(D, H + R, 0.25), zt(H, R, 2 / 3)])                               # constant dominant against the rest, 1 to 3; then hybrid against recessive, 2 to 1
        else:
            ks = sorted(tot); out.append(zt(tot[ks[0]], tot[ks[1]], 0.5))
        for k in sorted(tot): rec(fixed + ((L, k),), i + 1)
    rec((), 0); return out
def zsimple(counts, parts):
    n = sum(counts); p = parts[0] / sum(parts); return (counts[0] - n * p) / math.sqrt(n * p * (1 - p))
T35 = [e for e in data.E if e[1] in ("seven", "eight", "twenty plants")]; z35 = [zsimple(e[2], e[3]) for e in T35]
nine = [e for e in data.E if e[1] == "nine kinds"][0]; C9 = [(states(l, "AB"), c) for l, c in zip(("AB", "Ab", "aB", "ab", "ABb", "aBb", "AaB", "Aab", "AaBb"), nine[2])]
C27 = [(states(l, "ABC"), c) for l, c in data.K27]
BC = {"back-cross 1": ("AB", "ABb", "AaB", "AaBb"), "back-cross 3": ("AB", "ABb", "AaB", "AaBb"), "back-cross 2": ("AaBb", "Aab", "aBb", "ab"), "back-cross 4": ("AaBb", "Aab", "aBb", "ab"), "back-cross, flower colour and stem": ("AaBb", "aBb", "Aab", "ab")}
CB = [[(states(l, "AB"), c) for l, c in zip(BC[e[0]], e[2])] for e in data.E if e[1] == "back-crosses"]
def all84(scheme, o3, o2, ob):
    z = list(z35) + split(C9, o2, scheme) + split(C27, o3, scheme)
    for cb in CB: z += split(cb, ob, scheme)
    assert len(z) == 84; return np.array(z)
def fits(zv):
    m = len(zv); s2 = float(np.mean(zv ** 2)); c = float(np.max(abs(zv))); p = np.sort(2 * norm.sf(abs(zv)))
    ll_s = float(np.sum(-0.5 * math.log(s2) - zv ** 2 / (2 * s2) + zv ** 2 / 2)); ll_c = -m * math.log(2 * norm.cdf(c) - 1)
    # better of two: density 2p for p <= a, 1 + a above. Between data values the likelihood rises with a, so the supremum is just below a data value (or at 1)
    best = (-1e18, None); cs = np.concatenate([[0.0], np.cumsum(np.log(2 * p))])
    for k in range(m + 1):                                   # k values at or below a; a just below p[k] (or 1 when k == m)
        a = p[k] if k < m else 1.0; l = cs[k] + (m - k) * math.log(1 + a)
        if l > best[0]: best = (float(l), float(a))
    return ll_s, ll_c, best[0], best[1], c, math.sqrt(s2)
print("1. The better-of-two account maximised properly, on my split")
z = all84('hyb', (0, 1, 2), (0, 1), (0, 1)); ls, lc, la, a, c, s = fits(z)
print(f"   log-likelihood over honest: shrunk {ls:+.3f}, cut-off {lc:+.3f}, better of two {la:+.3f} (threshold just below {a:.4f}); that is {math.exp(ls):,.0f}, {math.exp(lc):,.0f} and {math.exp(la):,.0f} times honest counts")
print(f"   better of two over shrunk {math.exp(la - ls):.1f}; over cut-off {math.exp(la - lc):.1f}; cut-off over shrunk {math.exp(lc - ls):.2f}")
zz = z[np.argsort(-abs(z))][1:]; l2 = fits(zz); print(f"   without the single furthest value (83 tests): cut-off over shrunk {math.exp(l2[1] - l2[0]):.0f}; better of two over shrunk {math.exp(l2[2] - l2[0]):.0f}")
print(f"   within 0.9 standard deviations: {int((abs(z) < 0.9).sum())} of 84; honest {84 * (2 * norm.cdf(0.9) - 1):.1f} (standard deviation {math.sqrt(84 * (2 * norm.cdf(0.9) - 1) * (2 - 2 * norm.cdf(0.9))):.1f}); shrunk as fitted {84 * (2 * norm.cdf(0.9 / s) - 1):.1f}")
print("2. Seventy-two lawful splits: three pairs of contrasts, six orders of the three characters, two of the two, two for the back-crosses")
names = {'hyb': "hybrid against constant, then constant against constant (mine)", 'pheno': "by appearance 3 to 1, then hybrid against constant 2 to 1", 'dom': "constant dominant against the rest, then hybrid against recessive"}
allres = []
for scheme in ('hyb', 'pheno', 'dom'):
    res = []
    for o3 in itertools.permutations(range(3)):
        for o2 in itertools.permutations(range(2)):
            for ob in itertools.permutations(range(2)):
                zv = all84(scheme, o3, o2, ob); f = fits(zv); res.append((float(abs(zv).max()), int((abs(zv) < 0.3).sum()), float((zv ** 2).sum()), f[1] - f[0], f[2] - f[0], f[2] - f[1], int((abs(zv) < 0.9).sum())))
    r = np.array(res); allres += res
    print(f"   {names[scheme]}:\n      furthest count {r[:, 0].min():.3f} to {r[:, 0].max():.3f}; within 0.3: {int(r[:, 1].min())} to {int(r[:, 1].max())}; within 0.9: {int(r[:, 6].min())} to {int(r[:, 6].max())}; sum {r[:, 2].min():.2f} to {r[:, 2].max():.2f}; cut-off over shrunk {math.exp(r[:, 3].min()):.2f} to {math.exp(r[:, 3].max()):.0f}; better of two over shrunk {math.exp(r[:, 4].min()):.1f} to {math.exp(r[:, 4].max()):.0f}")
r = np.array(allres); none = (2 * norm.cdf(r[:, 0]) - 1) ** 84
print(f"   all 72: furthest count {r[:, 0].min():.3f} to {r[:, 0].max():.3f} (honest counts would put {84 * 2 * norm.sf(r[:, 0].max()):.1f} of 84 beyond the larger); chance of none beyond it if honest: 1 in {1 / none.max():,.0f} to 1 in {1 / none.min():,.0f}")
print(f"   within 0.3: {int(r[:, 1].min())} to {int(r[:, 1].max())}; 25 or more in {int((r[:, 1] >= 25).sum())} splits, 21 or fewer in {int((r[:, 1] <= 21).sum())}; within 0.9: {int(r[:, 6].min())} to {int(r[:, 6].max())}")
print(f"   cut-off over shrunk: {math.exp(r[:, 3].min()):.2f} to {math.exp(r[:, 3].max()):.0f}; the largest factor between any two of the three accounts: {math.exp(np.abs(r[:, 3:6]).max(axis=1).min()):.1f} to {math.exp(np.abs(r[:, 3:6]).max()):.0f}")
print(f"   splits in which the cut-off is the most likely of the three: {int(((r[:, 3] > 0) & (r[:, 5] < 0)).sum())}; better of two: {int(((r[:, 4] > 0) & (r[:, 5] > 0)).sum())}; shrunk: {int(((r[:, 3] < 0) & (r[:, 4] < 0)).sum())}")
print("3. Counting on until it looks right, with wider bands (the 35 simple tests; 400 tables each)")
def stopping_z(n, p, trials, band):
    lo, hi = math.ceil(n / 2), math.floor(3 * n / 2); out = np.empty(trials); done = 0
    while done < trials:
        b = min(trials - done, max(1, int(4e6 // hi))); cs = np.cumsum(rng.random((b, hi)) < p, axis=1)[:, lo - 1:]; kk = np.arange(lo, hi + 1)
        w = (cs - kk * p) / np.sqrt(kk * p * (1 - p)); ok = abs(w) <= band; first = np.where(ok.any(axis=1), ok.argmax(axis=1), hi - lo); out[done:done + b] = w[np.arange(b), first]; done += b
    return out
zo = np.array(z35); seen_in = int((abs(zo) <= 0.5).sum())
for band in (0.5, 1.0, 1.25):
    Z = np.array([stopping_z(sum(e[2]), e[3][0] / sum(e[3]), 400, band) for e in T35]); inside = (abs(Z) <= 0.5).sum(axis=0)
    print(f"   stop within {band} standard deviations: mean chi-squared {float((Z ** 2).mean()):.3f}; within 0.5 on average {inside.mean():.1f} of 35 (seen {seen_in}; so few in {100 * float((inside <= seen_in).mean()):.1f}% of tables); sum as small as seen in {100 * float(((Z ** 2).sum(axis=0) <= (zo ** 2).sum()).mean()):.0f}%; nothing beyond 1.424 in {100 * float((abs(Z).max(axis=0) <= abs(zo).max() + 1e-9).mean()):.1f}%")
print("4. Exact binomial chances")
pf = (2 / 3) * (1 - 0.75 ** 10); print(f"   399 or more hybrids of 600 at a share of {pf:.4f}: {binom.sf(398, 600, pf):.4f} (1 in {1 / binom.sf(398, 600, pf):.0f})")
for a, b, npl in ((43, 2, 253), (14, 15, 253), (32, 1, 258), (20, 19, 258)):
    n = a + b; one = binom.sf(a - 1, n, 0.75) if a > 0.75 * n else binom.cdf(a, n, 0.75); print(f"   a single plant with {a}:{b}: one-sided chance {one:.5f}; at least one such among {npl} honest plants of that size: {1 - (1 - one) ** npl:.2f}")
print("5. What the sealed sheet remembered against what the page prints")
sheet = open(sys.argv[1]).read(); block = sheet[sheet.index("What I remember"):sheet.index("- Fisher's table")]
found = [int(x) for x in re.findall(r"\d+", block.replace(",", "") if False else block)]      # every whole number in that part of the sheet
want = {"seven": [c for e in data.E if e[1] == "seven" for c in e[2]], "eight": [c for e in data.E if e[1] == "eight" for c in e[2]], "nine": list(nine[2]), "27 by hybrid count": sorted(data.K27_COUNTS),
        "back-crosses 1, 2 and the fifth": [c for e in data.E if e[0] in ("back-cross 1", "back-cross 2", "back-cross, flower colour and stem") for c in e[2]], "twenty plants": [c for e in data.E if e[1] == "twenty plants" for c in e[2]]}
pool = list(found); tot = 0
for k, v in want.items():
    ok = True
    for x in v:
        if x in pool: pool.remove(x)
        else: ok = False
    tot += len(v) if ok else 0; print(f"   {k:32s} {len(v):3d} counts: {'all on the sheet as printed' if ok else 'NOT all on the sheet'}")
print(f"   {tot} counts on the sheet agree with the page; the 8 counts of back-crosses 3 and 4 are not on the sheet (it says so)")
