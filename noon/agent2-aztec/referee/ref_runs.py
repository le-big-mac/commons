"""Step 2: re-analysis of the author's runs.json (read only)."""
import json, math
import numpy as np

R = json.load(open("/home/agent2/aztec/runs.json"))
sizes = [100, 200, 400, 800, 1600]
get = lambda n, key: np.array([r[str(n)][key] for r in R])
lim = (1 - 1 / math.sqrt(2)) / 2
K = np.array([get(n, 'K') for n in sizes]).astype(float)       # 5 x 100
F = np.array([get(n, 'frozen') for n in sizes])
print("runs", K.shape[1])
for i, n in enumerate(sizes):
    k = K[i]
    vals, cnts = np.unique(k, return_counts=True)
    print(f"n={n}: mean {k.mean():.3f} sd {k.std(ddof=1):.3f} min {k.min():.0f} max {k.max():.0f}  hist {dict(zip(vals.astype(int).tolist(), cnts.tolist()))}")
    th = 0.25304 * n ** (1 / 3)
    print(f"      theory sd 0.2530 n^(1/3) = {th:.3f}, with +1/12 lattice variance {math.sqrt(th**2+1/12):.3f}; "
          f"observed/theory {k.std(ddof=1)/math.sqrt(th**2+1/12):.3f}; chi2-type p (two-sided, normal approx of sd, se=sd/sqrt(198)): z = {(k.std(ddof=1)-math.sqrt(th**2+1/12))/(math.sqrt(th**2+1/12)/math.sqrt(198)):+.2f}")
    exc = k.mean() - lim * n
    print(f"      excess {exc:.3f} = {exc/n**(1/3):.3f} n^(1/3) (se {k.std(ddof=1)/10/n**(1/3):.3f}); excess/sd = {exc/k.std(ddof=1):.3f} (Tracy-Widom beta=2: 1.964); 0.497 n^(1/3) - excess = {0.497*n**(1/3)-exc:.2f} blocks")
print("correlation of K between sizes of the same growth (rows/cols = sizes):")
print(np.round(np.corrcoef(K), 2))
print("correlation of frozen fraction between sizes:")
print(np.round(np.corrcoef(F), 2))
sd = K.std(axis=1, ddof=1)
lx = np.log(sizes)
print("log-log slope, all five:", round(np.polyfit(lx, np.log(sd), 1)[0], 3))
for drop in range(5):
    keep = [i for i in range(5) if i != drop]
    print(f"   leaving out n={sizes[drop]}: slope {np.polyfit(lx[keep], np.log(sd[keep]), 1)[0]:.3f}")
print("   local slopes between neighbouring sizes:", np.round(np.diff(np.log(sd)) / np.log(2), 3))
print("   first three sizes only:", round(np.polyfit(lx[:3], np.log(sd[:3]), 1)[0], 3), " last three only:", round(np.polyfit(lx[2:], np.log(sd[2:]), 1)[0], 3))
# bootstrap: author's way (independent resampling per size) and joint (resample growths)
rng = np.random.default_rng(1)
N = K.shape[1]
bi = [np.polyfit(lx, np.log([K[i][rng.integers(0, N, N)].std(ddof=1) for i in range(5)]), 1)[0] for _ in range(4000)]
bj = []
bj4 = []
for _ in range(4000):
    idx = rng.integers(0, N, N)
    s = K[:, idx].std(axis=1, ddof=1)
    bj.append(np.polyfit(lx, np.log(s), 1)[0]); bj4.append(np.polyfit(lx[:4], np.log(s[:4]), 1)[0])
print(f"bootstrap slope sd: sizes resampled independently (author) {np.std(bi):.3f}; growths resampled jointly {np.std(bj):.3f}; "
      f"joint 95% interval {np.percentile(bj,2.5):.3f}..{np.percentile(bj,97.5):.3f}; four sizes without 1600: slope sd {np.std(bj4):.3f}")
# residuals of the five points about the fitted line
p = np.polyfit(lx, np.log(sd), 1)
res = np.log(sd) - np.polyfit(lx, np.log(sd), 1)[0] * lx - p[1]
print("residuals of log sd about the line, in units of 1/sqrt(198):", np.round(res * math.sqrt(198), 2), " chi2 (3 dof, if independent):", round(float((res**2).sum()*198), 2))
# is the 1600 sd driven by a few runs?
k = K[4]
order = np.argsort(k)
print("K at 1600 sorted:", k[order].astype(int).tolist())
for trim in (1, 2, 3):
    kk = k[order][trim:]
    print(f"   dropping the {trim} lowest: sd {kk.std(ddof=1):.3f}; dropping {trim} lowest and {trim} highest: sd {k[order][trim:-trim].std(ddof=1):.3f}")
print("   robust sd (1.4826*MAD), each size:", [round(1.4826*np.median(np.abs(K[i]-np.median(K[i]))), 2) for i in range(5)],
      " IQR/1.349:", [round((np.percentile(K[i],75)-np.percentile(K[i],25))/1.349, 2) for i in range(5)])
# the run(s) with lowest K at 1600: what did they read at other sizes?
for j in order[:3]:
    print("   run index", j, "seed", 100 + j, "K at sizes:", K[:, j].astype(int).tolist(), "frozen:", np.round(F[:, j], 4).tolist())
# excess coefficient fits
exc = K.mean(axis=1) - lim * np.array(sizes)
se = sd / 10
n13 = np.array(sizes) ** (1 / 3)
w = 1 / se**2
c0 = (w * exc * n13).sum() / (w * n13**2).sum()
chi0 = (w * (exc - c0 * n13)**2).sum()
A = np.vstack([n13, np.ones(5)]).T
coef, *_ = np.linalg.lstsq(A * np.sqrt(w)[:, None], exc * np.sqrt(w), rcond=None)
chi1 = (w * (exc - A @ coef)**2).sum()
cov = np.linalg.inv((A * w[:, None]).T @ A)
print(f"excess = c n^(1/3): c = {c0:.3f}, chi2 {chi0:.2f} (4 dof, treating sizes as independent)")
print(f"excess = c n^(1/3) + d: c = {coef[0]:.3f} +- {math.sqrt(cov[0,0]):.3f}, d = {coef[1]:.2f} +- {math.sqrt(cov[1,1]):.2f}, chi2 {chi1:.2f} (3 dof)")
chiT = (w * (exc - (0.497 * n13 - 0.4))**2).sum()
print(f"excess = 0.497 n^(1/3) - 0.4 (Tracy-Widom constant from memory, offset from referee's blind runs): chi2 {chiT:.2f} (5 dof)")
p = np.polyfit(lx, np.log(exc), 1)
print(f"free power law for the excess: exponent {p[0]:.3f}")
fe = F.mean(axis=1) - (1 - math.pi / 4)
print("frozen-fraction excess * n^(2/3):", np.round(fe * np.array(sizes) ** (2 / 3), 3), "; fit c - d n^(-1/3):",
      np.round(np.polyfit(np.array(sizes) ** (-1 / 3), fe * np.array(sizes) ** (2 / 3), 1), 3), "; free exponent of the excess:",
      round(np.polyfit(lx, np.log(fe), 1)[0], 3))
cen = np.array([[r[str(n)]['centre'] for r in R] for n in sizes])
for i, n in enumerate(sizes):
    print(f"centre shares n={n}: mean {np.round(cen[i].mean(0),5)}, per-growth sd {np.round(cen[i].std(0,ddof=1),5)}, se of mean {np.round(cen[i].std(0,ddof=1)/10,5)}")
t = np.array([get(n, 'tosses') for n in sizes]).astype(float)
print("tosses mean:", t.mean(1), " over n(n+1)/2:", np.round(t.mean(1) / (np.array(sizes) * (np.array(sizes) + 1) / 2), 3), " over n^3:", np.round(t.mean(1) / np.array(sizes) ** 3., 5))
