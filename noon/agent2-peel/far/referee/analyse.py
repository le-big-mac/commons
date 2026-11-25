import sys
import numpy as np
W = float(sys.argv[1]); Htot = float(sys.argv[2]); files = sys.argv[3:]
dy = 0.25; nb = int(round(Htot / dy)); Hm = Htot - 50.0
data = []
for f in files:
    a = np.loadtxt(f); arr = np.zeros((nb, 5)); idx = a[:, 0].astype(int); ok = idx < nb
    arr[idx[ok]] = a[ok, 1:6]; data.append(arr)
data = np.array(data); nw = len(files)
n, sy, sd, sd2, sd3 = [data[:, :, i] for i in range(5)]
yc = (np.arange(nb) + 0.5) * dy
mean = sd / n; ym = sy / n
print(f"W={W} Htot={Htot} usable to {Hm}, windows={nw}, points/window ~ {n.sum()/nw:.0f}")
def se(v): v = np.asarray(v); return v.std(ddof=1) / np.sqrt(len(v)) if len(v) > 1 else float('nan')
# (a) slope
def slopes(lo, hi):
    m = (yc >= lo) & (yc < hi)
    return np.array([np.polyfit(ym[w, m], mean[w, m], 1) for w in range(nw)])
print("(a) slope of mean depth vs height")
for lo, hi in [(Hm / 2, Hm), (Hm / 2, 0.75 * Hm), (0.75 * Hm, Hm), (Hm / 8, Hm / 4), (Hm / 4, Hm / 2)]:
    s = slopes(lo, hi)
    print(f"   range [{lo:.0f},{hi:.0f}]: slope {s[:,0].mean():.5f} +- {se(s[:,0]):.5f}   intercept {s[:,1].mean():.3f} +- {se(s[:,1]):.3f}")
sl = slopes(Hm / 2, Hm); alpha = sl[:, 0].mean(); alpha_se = se(sl[:, 0])
# (b),(c)
var = (sd2 / n - mean**2) * n / (n - 1) - alpha**2 * dy**2 / 12
m3 = sd3 / n - 3 * mean * sd2 / n + 2 * mean**3
skew = m3 / (sd2 / n - mean**2)**1.5
hs = [h for h in [12.5, 25, 50, 100, 200, 400, 800, 1000, 1600, 2000] if h * 1.1 <= Hm + 1e-9 or h == Hm]
if Hm * 0.909 not in hs: hs.append(round(Hm / 1.1, 1))
hs = sorted(set(hs))
print("(b,c) within-band variance (band 0.25 thick, pooled over heights within +-10%), about each window's own band mean")
print("    y     meandepth   var +- se     var/sqrt(meandepth) +- se   var/sqrt(alpha*y)   skew +- se")
V = []
for h in hs:
    m = (yc >= 0.9 * h) & (yc < 1.1 * h)
    v = var[:, m].mean(axis=1); sk = skew[:, m].mean(axis=1); md = mean[:, m].mean()
    V.append(v)
    print(f"  {h:7.1f} {md:9.2f}  {v.mean():7.4f} {se(v):.4f}   {v.mean()/np.sqrt(md):.4f} {se(v)/np.sqrt(md):.4f}    {v.mean()/np.sqrt(alpha*h):.4f}     {sk.mean():+.4f} {se(sk):.4f}")
V = np.array(V); lh = np.log(hs)
print("   local exponents between successive heights:")
for i in range(len(hs) - 1):
    e = np.log(V[i + 1] / V[i]) / (lh[i + 1] - lh[i])
    print(f"     {hs[i]:7.1f} -> {hs[i+1]:7.1f}: {e.mean():.4f} +- {se(e):.4f}")
for lo in [50, 100, 200, 400]:
    k = [i for i, h in enumerate(hs) if h >= lo]
    if len(k) < 2: continue
    e = np.array([np.polyfit(lh[k], np.log(V[k, w]), 1)[0] for w in range(nw)])
    print(f"   power-law fit, heights >= {lo}: exponent {e.mean():.4f} +- {se(e):.4f} (window scatter)")
# fit on fine grid of all bands
for lo in [50, 100, 200, 400]:
    m = (yc >= lo) & (yc < Hm)
    e = np.array([np.polyfit(np.log(yc[m]), np.log(var[w, m]), 1)[0] for w in range(nw)])
    print(f"   power-law fit on all thin bands in [{lo},{Hm:.0f}): exponent {e.mean():.4f} +- {se(e):.4f}")
# var = a sqrt(depth)+b
m = (yc >= 50) & (yc < Hm)
ab = np.array([np.polyfit(np.sqrt(mean[w, m]), var[w, m], 1) for w in range(nw)])
print(f"   fit var = a*sqrt(meandepth)+b over [50,{Hm:.0f}): a = {ab[:,0].mean():.4f} +- {se(ab[:,0]):.4f}, b = {ab[:,1].mean():.3f} +- {se(ab[:,1]):.3f}")
# (d)
q = 8  # thick band = 2.0
nt = nb // q
N2 = n[:, :nt * q].reshape(nw, nt, q).sum(axis=2); SY = sy[:, :nt * q].reshape(nw, nt, q).sum(axis=2); SD = sd[:, :nt * q].reshape(nw, nt, q).sum(axis=2)
R = (SD - alpha * SY) / N2; yt = (np.arange(nt) + 0.5) * q * dy
print(f"(d) R(y) = mean depth in band of thickness {q*dy} over whole window - {alpha:.5f}*y ;  D = W var(change)/step")
VT = var[:, :nt * q].reshape(nw, nt, q).mean(axis=2); C = VT / N2   # sampling noise of a band mean (points sample the field at random x)
def Dest(step, lo, hi):
    k = int(round(step / (q * dy))); i0 = int(lo / (q * dy)); i1 = int(hi / (q * dy))
    ii = np.arange(i0, i1 - k + 1, k)
    ch = R[:, ii + k] - R[:, ii]            # (nw, nsteps)
    d_raw = W * (ch**2).mean(axis=1) / step  # per window, about zero
    d_cor = W * (ch**2 - C[:, ii + k] - C[:, ii]).mean(axis=1) / step
    chc = ch - ch.mean(axis=0, keepdims=True)
    d_c = W * (chc**2).sum() / ((nw - 1) * ch.shape[1]) / step
    return d_raw.mean(), se(d_raw), d_c, ch.shape[1], d_cor.mean(), se(d_cor), d_cor.mean() * np.sqrt(2.0 / ch.size)
for lo, hi in [(100, Hm), (100, Hm / 2), (Hm / 2, Hm), (25, 100)]:
    print(f"   heights [{lo:.0f},{hi:.0f}]")
    res = {}
    for step in [2, 10, 25, 50, 100, 200, 400]:
        if step > (hi - lo) / 2: continue
        r = Dest(step, lo, hi); res[step] = r
        print(f"     step {step:4d}: D raw = {r[0]:.4f} +- {r[1]:.4f} | about per-step mean {r[2]:.4f} | D minus sampling noise = {r[4]:.4f} +- {r[5]:.4f} (window scatter; chi2 guess {r[6]:.4f}) | steps/window {r[3]}")
    for s1, s2 in [(25, 50), (50, 100), (25, 100), (100, 200), (50, 200)]:
        if s1 in res and s2 in res:
            print(f"     differenced D (raw) from steps {s1},{s2}: {(res[s2][0]*s2-res[s1][0]*s1)/(s2-s1):.4f}")
