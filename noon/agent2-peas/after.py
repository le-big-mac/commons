"""Checks made after the sealed lines were scored; none was registered.   usage: python -I after.py"""
import sys, os, math
import numpy as np
from scipy.stats import chi2, norm
sys.path.insert(0, os.path.dirname(os.path.abspath(sys.argv[0])))
import data
rng = np.random.default_rng(1936)
def chisq(counts, parts):
    n = sum(counts); e = [n * p / sum(parts) for p in parts]; return sum((c - x) ** 2 / x for c, x in zip(counts, e)), len(counts) - 1
def zscore(counts, parts):
    n = sum(counts); p = parts[0] / sum(parts); return (counts[0] - n * p) / math.sqrt(n * p * (1 - p))
T35 = [e for e in data.E if e[1] in ("seven", "eight", "twenty plants")]; z = np.array([zscore(e[2], e[3]) for e in T35]); c = float(abs(z).max()); p0 = float(chi2.sf(c * c, 1)); s2 = float(np.mean(z ** 2))
print("A. Each of Fisher's groups on its own: chi-squared per degree of freedom, and the chance of so small a value if honest")
for g in data.FISHER:
    x = sum(chisq(e[2], e[3])[0] for e in data.E if e[1] == g); d = sum(chisq(e[2], e[3])[1] for e in data.E if e[1] == g); print(f"   {g:14s} {x:8.4f} on {d:2d}: {x / d:.3f} a degree; chance {chi2.cdf(x, d):.4f}")
tests = [(e[0], *chisq(e[2], e[3])) for e in data.E]; ups = sorted((chi2.sf(x, d), nm, d) for nm, x, d in tests)
print(f"   the 42 separate tests: smallest chance of a worse fit {ups[0][0]:.3f} ({ups[0][1]}), then {ups[1][0]:.3f} ({ups[1][1]}), {ups[2][0]:.3f} ({ups[2][1]}); if honest, all 42 would stay above {ups[0][0]:.3f} with chance {(1 - ups[0][0]) ** 42:.4f}")
print("B. Optional stopping's own fingerprint: the share of the 35 inside the band (|z| at or below 0.5)")
def stopping_z(n, p, trials, band=0.5):
    lo, hi = math.ceil(n / 2), math.floor(3 * n / 2); out = np.empty(trials); done = 0
    while done < trials:
        b = min(trials - done, max(1, int(4e6 // hi))); cs = np.cumsum(rng.random((b, hi)) < p, axis=1)[:, lo - 1:]; kk = np.arange(lo, hi + 1)
        zz = (cs - kk * p) / np.sqrt(kk * p * (1 - p)); ok = abs(zz) <= band; first = np.where(ok.any(axis=1), ok.argmax(axis=1), hi - lo); out[done:done + b] = zz[np.arange(b), first]; done += b
    return out
inside = []; trials = 1000
allz = np.array([stopping_z(sum(e[2]), e[3][0] / sum(e[3]), trials) for e in T35])          # 35 x trials
per_set = (abs(allz) <= 0.5).sum(axis=0); obs_in = int((abs(z) <= 0.5).sum())
print(f"   observed {obs_in} of 35; honest expectation {35 * (2 * norm.cdf(0.5) - 1):.1f}; under optional stopping {per_set.mean():.1f} on average, and {obs_in} or fewer in {100 * float((per_set <= obs_in).mean()):.1f}% of {trials} simulated tables; largest |z| under stopping: median {np.median(abs(allz).max(axis=0)):.2f}")
print("C. Do the two models fitted to the 35 simple tests account for the whole table of 84 degrees of freedom?")
others = [(nm, x, d) for nm, x, d in tests if d > 1]; N = 200000
def cut_total(pcut):
    tot = np.zeros(N)
    for d, k in ((1, 35),) + tuple((d, 1) for _, _, d in others):
        u = rng.uniform(0, 1 - pcut, (N, k)); tot += chi2.ppf(u, d).sum(axis=1)
    return tot
tc = cut_total(p0); obs_total = sum(x for _, x, _ in tests)
print(f"   cut-off (a test is done again whenever its chance of a worse fit is below {p0:.3f}, the cut fitted on the 35): expected total {tc.mean():.1f}; a total at or below the observed {obs_total:.2f} in {100 * float((tc <= obs_total).mean()):.2f}% of {N} tables")
for nm, x, d in others:
    u = rng.uniform(0, 1 - p0, 200000); m = chi2.ppf(u, d).mean(); print(f"      {nm:36s} observed {x:6.3f} on {d:2d}; honest {d}; cut-off {m:5.2f}; shrunk {d * s2:5.2f}")
print(f"   shrunk (every deviation reduced to {math.sqrt(s2):.3f} of itself): expected total {84 * s2:.1f}; a total at or below the observed with chance {chi2.cdf(obs_total / s2, 84):.3f}")
x35 = float((z ** 2).sum()); print(f"   the 35 alone: observed {x35:.2f}; cut-off expects {35 * (1 - 2 * c * norm.pdf(c) / (2 * norm.cdf(c) - 1)):.2f}; shrunk {35 * s2:.2f} (fitted to it)")
rest = obs_total - x35; print(f"   the other 49 degrees (seven multi-class tests): observed {rest:.2f}, that is {rest / 49:.3f} a degree; chance if honest {chi2.cdf(rest, 49):.2g}")
print("D. The 35 in two halves: fifteen experiments, twenty single plants")
def fit(zv):
    s2 = float(np.mean(zv ** 2)); cc = float(np.max(abs(zv))); n = len(zv)
    return s2, cc, -0.5 * n * math.log(2 * math.pi * s2) - 0.5 * n, -0.5 * n * math.log(2 * math.pi) - 0.5 * float(np.sum(zv ** 2)) - n * math.log(2 * norm.cdf(cc) - 1)
for name, zz in (("fifteen experiments", z[:15]), ("twenty plants", z[15:])):
    a, b, ls, lc = fit(zz); sim = rng.normal(0, math.sqrt(a), (20000, len(zz))); l = np.array([(lambda f: f[3] - f[2])(fit(r)) for r in sim])
    print(f"   {name:20s} mean z squared {a:.3f}; largest |z| {b:.3f} (honest chance of none larger {(2 * norm.cdf(b) - 1) ** len(zz):.3f}); cut-off over shrunk {math.exp(lc - ls):.1f}; as large or larger under the shrunk model in {100 * float((l >= lc - ls).mean()):.1f}% of sets")
print("E. The six tests of 100 plants against Fisher's corrected expectation in place of Mendel's 2 to 1")
pf = (2 / 3) * (1 - 0.75 ** 10); six = [e for e in data.E if e[1] == "eight" and sum(e[2]) == 100]; zf = [(e[2][0] - 100 * pf) / math.sqrt(100 * pf * (1 - pf)) for e in six]
print("   z: " + " ".join(f"{v:+.2f}" for v in zf) + f"; sum of squares {sum(v * v for v in zf):.2f} on 6 (against 2 to 1: {sum(zscore(e[2], e[3]) ** 2 for e in six):.2f})")
print("F. How many peas is the shrinking? Experiment 1 (7,324 seeds)")
n = 7324; sd = math.sqrt(n * 0.1875); print(f"   one standard deviation is {sd:.1f} seeds; an honest count misses by {sd * math.sqrt(2 / math.pi):.1f} on average; shrinking every miss by {100 * (1 - math.sqrt(s2)):.0f}% would move {sd * math.sqrt(2 / math.pi) * (1 - math.sqrt(s2)):.1f} seeds, {100 * sd * math.sqrt(2 / math.pi) * (1 - math.sqrt(s2)) / n:.2f}% of them")
print("G. The cut-off as a rule about first attempts")
print(f"   share of honest first attempts beyond {c:.3f} standard deviations: {p0:.3f}; among 15 experiments that is {15 * p0:.1f} done again on average, among 35 tests {35 * p0:.1f}")
print("H. The extremes Mendel reports among his plants (43 round to 2 angular; 14 to 15; 32 yellow to 1 green; 20 to 19)")
for a, b, nplants in ((43, 2, 253), (14, 15, 253), (32, 1, 258), (20, 19, 258)):
    zz = zscore((a, b), (3, 1)); pp = 2 * norm.sf(abs(zz)); print(f"   {a}:{b}  z = {zz:+.2f}; among {nplants} honest plants at least one so extreme with chance about {1 - (1 - pp) ** nplants:.2f} (normal approximation)")
