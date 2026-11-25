"""Fisher's sum redone on Mendel's counts, and the fingerprint of the tidying.   usage: python -I peas.py results.json
Counts come from data.py (checked against the paper's text by verify.py)."""
import sys, os, json, math
import numpy as np
from scipy.stats import chi2, norm
sys.path.insert(0, os.path.dirname(os.path.abspath(sys.argv[0])))
import data
R = {}
def chisq(counts, parts):
    n = sum(counts); e = [n * p / sum(parts) for p in parts]; return sum((c - x) ** 2 / x for c, x in zip(counts, e)), len(counts) - 1
print("1. Fisher's sum, group by group (the last column is what I remembered of Fisher's table)")
tot = dft = 0; G = {}
for g in data.FISHER:
    x = d = 0
    for e in data.E:
        if e[1] == g: a, b = chisq(e[2], e[3]); x += a; d += b
    G[g] = (x, d); tot += x; dft += d
    print(f"   {g:14s} {d:3d} degrees of freedom; chi-squared {x:8.4f};   remembered {data.FISHER[g][1]:.4f} on {data.FISHER[g][0]}")
plow = chi2.cdf(tot, dft); print(f"   {'all':14s} {dft:3d} degrees of freedom; chi-squared {tot:8.4f};   remembered 41.6056 on 84")
print(f"   chance of a total this small or smaller if every count were an honest sample: {plow:.3g} (1 in {1 / plow:,.0f}); of a larger one {1 - plow:.5f}")
R.update(groups={g: dict(chisq=G[g][0], df=G[g][1]) for g in G}, total=tot, df=dft, p_low=plow)
print("2. The six tests of 100 plants judged from ten offspring each")
six = [e for e in data.E if e[1] == "eight" and sum(e[2]) == 100]; h = sum(e[2][0] for e in six); n = sum(sum(e[2]) for e in six)
pf = (2 / 3) * (1 - 0.75 ** 10); z2 = (h - n * 2 / 3) / math.sqrt(n * (2 / 3) * (1 / 3)); zf = (h - n * pf) / math.sqrt(n * pf * (1 - pf))
print(f"   {h} hybrid to {n - h} constant of {n}. Against 2 to 1: {z2:+.2f} standard deviations. Against Fisher's corrected share {pf:.4f} (expected {n * pf:.1f}): {zf:+.2f}; chance of so many or more {norm.sf(zf):.3f}")
R.update(six_hybrid=h, six_n=n, six_z_fisher=zf, six_z_2to1=z2)
print("3. The 35 tests with one degree of freedom")
T35 = [e for e in data.E if e[1] in ("seven", "eight", "twenty plants")]; assert len(T35) == 35
def zscore(counts, parts):
    n = sum(counts); p = parts[0] / sum(parts); return (counts[0] - n * p) / math.sqrt(n * p * (1 - p))
z = np.array([zscore(e[2], e[3]) for e in T35]); x1 = z ** 2
for g in ("seven", "eight", "twenty plants"):
    zz = [f"{zscore(e[2], e[3]):+.2f}" for e in T35 if e[1] == g]; print(f"   z, {g}: " + " ".join(zz))
k = int(np.argmax(x1)); small = int((abs(z) < 0.3).sum())
print(f"   largest chi-squared {x1.max():.4f} ({T35[k][0]}, z = {z[k]:+.3f}); chance that 35 honest tests all stay at or below it: {(1 - chi2.sf(x1.max(), 1)) ** 35:.4f}")
print(f"   tests with |z| below 0.3: {small} of 35; an honest experimenter would expect {35 * (2 * norm.cdf(0.3) - 1):.1f}")
print(f"   mean of z squared {x1.mean():.4f}; positive deviations {int((z > 0).sum())}, negative {int((z < 0).sum())}; mean z {z.mean():+.3f}")
for lo, hi in ((0, 0.3), (0.3, 0.6), (0.6, 0.9), (0.9, 1.2), (1.2, 1.5), (1.5, 9)):
    print(f"      |z| from {lo} to {hi if hi < 9 else 'up'}: {int(((abs(z) >= lo) & (abs(z) < hi)).sum()):2d}; honest {35 * 2 * (norm.cdf(hi) - norm.cdf(lo)):.1f}")
R.update(max_x1=float(x1.max()), max_name=T35[k][0], small=small, z=[float(v) for v in z], mean_z2=float(x1.mean()))
print("4. Two models of tidying fitted to the 35 values of z")
def fit(zv):
    s2 = float(np.mean(zv ** 2)); c = float(np.max(abs(zv))); n = len(zv)
    ll_shrunk = -0.5 * n * math.log(2 * math.pi * s2) - 0.5 * n                       # normal, spread fitted
    ll_cut = -0.5 * n * math.log(2 * math.pi) - 0.5 * float(np.sum(zv ** 2)) - n * math.log(2 * norm.cdf(c) - 1)   # standard normal, never beyond c
    ll_honest = -0.5 * n * math.log(2 * math.pi) - 0.5 * float(np.sum(zv ** 2))
    return s2, c, ll_shrunk, ll_cut, ll_honest
s2, c, lls, llc, llh = fit(z); lr = math.exp(llc - lls)
print(f"   shrunk: spread {math.sqrt(s2):.3f} of honest (every deviation reduced by {100 * (1 - math.sqrt(s2)):.0f}%); cut-off: nothing beyond {c:.3f} standard deviations")
print(f"   log-likelihood: honest {llh:.3f}, shrunk {lls:.3f}, cut-off {llc:.3f}; cut-off over shrunk: a factor of {lr:.1f}; shrunk over honest {math.exp(lls - llh):.1f}; cut-off over honest {math.exp(llc - llh):.1f}")
rng = np.random.default_rng(1865); N = 20000
sim = rng.normal(0, math.sqrt(s2), (N, 35)); lrs = np.array([(lambda f: f[3] - f[2])(fit(row)) for row in sim]); share = float((lrs >= llc - lls).mean())
print(f"   {N} sets of 35 drawn from the shrunk model as fitted: the cut-off model beats it by as much as observed, or more, in {100 * share:.1f}% of sets")
# the other way round: sets drawn from the cut-off model (standard normal redrawn until within c)
def trunc(size):
    u = rng.uniform(norm.cdf(-c), norm.cdf(c), size); return norm.ppf(u)
simc = trunc((N, 35)); lrc = np.array([(lambda f: f[3] - f[2])(fit(row)) for row in simc]); share_c = float((lrc <= llc - lls).mean())
print(f"   {N} sets drawn from the cut-off model as fitted: a ratio as small as observed or smaller in {100 * share_c:.1f}% of sets; median ratio {math.exp(float(np.median(lrc))):.1f} (from the shrunk model: {math.exp(float(np.median(lrs))):.2f})")
honest = rng.normal(0, 1, (N, 35)); print(f"   {N} honest sets: mean z squared as small as observed in {100 * float((np.mean(honest ** 2, axis=1) <= x1.mean()).mean()):.2f}%; largest |z| as small as observed in {100 * float((np.max(abs(honest), axis=1) <= c).mean()):.2f}%; {small} or fewer below 0.3 in {100 * float(((abs(honest) < 0.3).sum(axis=1) <= small).mean()):.0f}%")
R.update(spread=math.sqrt(s2), cut=c, lr=lr, share_shrunk_sim=share, share_cut_sim=share_c)
print("5. Optional stopping on the 35 tests (count on from half the reported number; stop when within half a standard deviation; stop at one and a half times regardless)")
def stopping(n, p, trials, band=0.5):
    lo, hi = math.ceil(n / 2), math.floor(3 * n / 2); out = np.empty(trials); done = 0
    while done < trials:
        b = min(trials - done, max(1, int(4e6 // hi))); cs = np.cumsum(rng.random((b, hi)) < p, axis=1)[:, lo - 1:]; kk = np.arange(lo, hi + 1)
        zz = (cs - kk * p) / np.sqrt(kk * p * (1 - p)); ok = abs(zz) <= band; first = np.where(ok.any(axis=1), ok.argmax(axis=1), hi - lo)
        out[done:done + b] = zz[np.arange(b), first] ** 2; done += b
    return out
res = []
for e in T35:
    n = sum(e[2]); p = e[3][0] / sum(e[3]); xs = stopping(n, p, 2000); res.append((n, xs.mean(), float((xs <= 0.25 + 1e-12).mean())))
m = float(np.mean([r[1] for r in res])); print(f"   mean chi-squared per test {m:.3f} (an honest count: 1.000); share of trials that stopped inside the band, averaged over tests: {np.mean([r[2] for r in res]):.2f}")
print(f"   by size of test: reported number below 60: {np.mean([r[1] for r in res if r[0] < 60]):.3f}; 60 to 200: {np.mean([r[1] for r in res if 60 <= r[0] <= 200]):.3f}; above 200: {np.mean([r[1] for r in res if r[0] > 200]):.3f}")
R.update(stopping_mean=m)
json.dump(R, open(sys.argv[1], 'w'), indent=1)
