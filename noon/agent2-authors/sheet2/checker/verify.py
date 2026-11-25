#!/usr/bin/env python
"""Second, differently-written pass (pandas/numpy, integer tenths) used only to
cross-check check.py. Writes nothing. Usage: python -I verify.py <monthly> <smoothed> <yearly>"""
import sys
import numpy as np
import pandas as pd


def tenths(col):
    # printed one-decimal strings -> exact integer tenths
    out = []
    for s in col:
        s = s.strip()
        neg = s.startswith("-")
        a, _, b = s.lstrip("-").partition(".")
        assert len(b) <= 1, s
        v = int(a) * 10 + (int(b) if b else 0)
        out.append(-v if neg else v)
    return np.array(out, dtype=np.int64)


mon = pd.read_csv(sys.argv[1], sep=";", header=None, dtype=str)
smo = pd.read_csv(sys.argv[2], sep=";", header=None, dtype=str)
yr = pd.read_csv(sys.argv[3], sep=";", header=None, dtype=str)

n_m = 12 * mon[0].astype(int).to_numpy() + mon[1].astype(int).to_numpy()
R = tenths(mon[3])
n_s = 12 * smo[0].astype(int).to_numpy() + smo[1].astype(int).to_numpy()
S = tenths(smo[3])
assert (np.diff(n_m) == 1).all() and (np.diff(n_s) == 1).all()
Yy = np.floor(yr[0].astype(float).to_numpy()).astype(int)
Y = tenths(yr[1])
assert (np.diff(Yy) == 1).all()


def lab(n):
    return "%04d-%02d" % ((n - 1) // 12, (n - 1) % 12 + 1)


# minima via sliding windows
mins = []
for i in range(60, len(S) - 60):
    w = S[i - 60:i + 61]
    if (w < 0).any():
        continue
    if (w[:60] > S[i]).all() and (w[61:] >= S[i]).all():
        mins.append(i)
print("minima:", len(mins), [lab(n_s[i]) for i in mins])

# which minima have an equal value somewhere in the following 60 months (tie rule exercised)
for i in mins:
    eq = [j for j in range(i + 1, i + 61) if S[j] == S[i]]
    if eq:
        print("  tie at minimum", lab(n_s[i]), "S=%.1f" % (S[i] / 10), "also at", [lab(n_s[j]) for j in eq])

rows = []
for a, b in zip(mins, mins[1:]):
    seg = S[a + 1:b]
    j = a + 1 + int(np.argmax(seg))  # argmax returns first occurrence
    rows.append((j - a, b - j, b - a, S[j], n_s[j]))
c = pd.DataFrame(rows, columns=["rise", "fall", "length", "peak10", "maxn"], index=range(1, len(rows) + 1))
print("B1", len(mins), len(c), c.length.mean())
print("B2", int((c.rise < c.fall).sum()))
i = int(np.argmax(R)); print("B3", R[i] / 10, lab(n_m[i]), int((R == R[i]).sum()))
rho = np.corrcoef(c.rise.rank(method="average"), c.peak10.rank(method="average"))[0, 1]
print("B4", rho, "pandas spearman:", c.rise.corr(c.peak10, method="spearman"))
o = np.argsort(-Y, kind="stable")[:4]; print("B5", [(int(Yy[k]), Y[k] / 10) for k in o])
x = Y / 10.0; d = x - x.mean()
r = lambda k: float((d[:-k] * d[k:]).sum() / (d * d).sum())
print("B6", r(10), r(11), r(11) > r(10))
pk = c.peak10 / 10
print("B7", pk.loc[15:24].idxmin(), pk.loc[15:24].min(), pk[14], pk[24])
print("B8", sum(pk[e + 1] > pk[e] for e in range(2, 23, 2)), sum(pk[e + 1] == pk[e] for e in range(2, 23, 2)))
print("B9", pk.idxmin(), pk.min(), int((pk == pk.min()).sum()), pk[5])
seg = S[mins[-1] + 1:]; ok = seg >= 0; top = seg[ok].max()
print("B10", top / 10, [lab(n_s[mins[-1] + 1 + j]) for j in np.nonzero(seg == top)[0]])
late = Y[(Yy >= 1900) & (Yy <= 2025)]; early = Y[(Yy >= 1749) & (Yy <= 1899)]
print("B11", late.mean() / 10, len(late), early.mean() / 10, len(early), late.mean() / early.mean(),
      "exact>=1.15:", int(late.sum()) * len(early) * 100 >= 115 * int(early.sum()) * len(late))
z = np.nonzero(R == 0)[0]; print("B12", len(z), lab(n_m[z[-1]]))
print("any negative R:", int((R < 0).sum()), "any negative Y:", int((Y < 0).sum()))

# what a 'latest tied month' convention would give (NOT the sheet's rule; information only)
mins2 = []
for i in range(60, len(S) - 60):
    w = S[i - 60:i + 61]
    if (w < 0).any():
        continue
    if (w[:60] >= S[i]).all() and (w[61:] > S[i]).all():
        mins2.append(i)
print("latest-tie convention minima:", len(mins2), [lab(n_s[i]) for i in mins2 if i not in mins])

# B1/B2/B4 under the 'latest tied month' convention (NOT the sheet's rule; information only)
rows2 = []
for a, b in zip(mins2, mins2[1:]):
    seg = S[a + 1:b]
    j = a + 1 + int(np.argmax(seg))
    rows2.append((j - a, b - j, b - a, S[j]))
c2 = pd.DataFrame(rows2, columns=["rise", "fall", "length", "peak10"], index=range(1, len(rows2) + 1))
print("latest-tie: B1 mean", c2.length.mean(), "B2", int((c2.rise < c2.fall).sum()),
      "B4", c2.rise.corr(c2.peak10, method="spearman"), "peaks same:", bool((c2.peak10.values == c.peak10.values).all()))
# provisional tail excluded (rows after the last present smoothed value) -- information only
keep = n_m <= n_s[np.nonzero(S >= 0)[0][-1]]
i2 = int(np.argmax(R[keep])); print("monthly up to last present S: max", R[keep][i2] / 10, lab(n_m[keep][i2]))
