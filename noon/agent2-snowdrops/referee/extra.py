"""Referee's extra blind checks: which shift estimate is right; is a trend left after winter temperature."""
import sys, collections
sys.path.insert(0, '/home/agent2/referee-snowdrops')
import numpy as np
from scipy import stats
from load import read_records, read_stations, read_temp, true_doy

hdr, R, bad = read_records()
sid, yr, qn, obj, ph, date, qb, jul = R.T
td = np.array([true_doy(int(y), int(d)) for y, d in zip(yr, date)])
keep = (qb != 5) & (yr >= 1951) & (yr <= 2023) & (np.abs(jul - td) <= 2)
S = sid[keep]; Y = yr[keep]; X = td[keep].astype(float)
t1 = read_temp(1); t2 = read_temp(2)


def twoway(S, Y, X):
    us, si = np.unique(S, return_inverse=True)
    uy, yi = np.unique(Y, return_inverse=True)
    ns, ny = len(us), len(uy)
    n_s = np.bincount(si, minlength=ns).astype(float)
    n_y = np.bincount(yi, minlength=ny).astype(float)
    Nsy = np.zeros((ns, ny)); np.add.at(Nsy, (si, yi), 1.0)
    Ty = np.bincount(yi, X, minlength=ny); Ts = np.bincount(si, X, minlength=ns)
    A = np.diag(n_y) - Nsy.T @ (Nsy / n_s[:, None])
    rhs = Ty - Nsy.T @ (Ts / n_s)
    b = np.linalg.lstsq(A, rhs, rcond=None)[0]
    a = (Ts - Nsy @ b) / n_s
    return uy, b + a.mean(), us, a


def registered(S, Y, X):
    us, si = np.unique(S, return_inverse=True)
    uy, yi = np.unique(Y, return_inverse=True)
    sm = np.bincount(si, X) / np.bincount(si)
    an = X - sm[si]
    return uy, np.bincount(yi, an) / np.bincount(yi) + X.mean()


def shift(uy, v):
    return v[(uy >= 1991) & (uy <= 2020)].mean() - v[(uy >= 1961) & (uy <= 1990)].mean()


def after_T(uy, v, label):
    T = np.array([(t1[int(y)] + t2[int(y)]) / 2 for y in uy])
    r = stats.linregress(T, v)
    Z = np.column_stack([np.ones(len(uy)), T, uy - uy.mean()])
    coef, *_ = np.linalg.lstsq(Z, v, rcond=None)
    res = v - Z @ coef
    cov = (res @ res / (len(uy) - 3)) * np.linalg.inv(Z.T @ Z)
    dT = T[(uy >= 1991) & (uy <= 2020)].mean() - T[(uy >= 1961) & (uy <= 1990)].mean()
    sh = shift(uy, v)
    # Durbin-Watson of residuals
    dw = np.sum(np.diff(res) ** 2) / np.sum(res ** 2)
    print('%-34s shift %.2f | r %.3f slope %.2f | slope*dT = %.2f (%.0f%% of shift) | year term after T: %.3f d/yr (t=%.2f) | DW %.2f' % (
        label, sh, r.rvalue, r.slope, r.slope * dT, 100 * r.slope * dT / sh, coef[2], coef[2] / cov[2, 2] ** .5, dw))


u, inv, cnt = np.unique(S, return_inverse=True, return_counts=True)
for minyears in (1, 15, 30, 50):
    m = (cnt >= minyears)[inv]
    uy, v = registered(S[m], Y[m], X[m]); after_T(uy, v, 'registered, stations >=%d y (%d)' % (minyears, (cnt >= minyears).sum()))
    uy, v, us_, a_ = twoway(S[m], Y[m], X[m]); after_T(uy, v, 'two-way,    stations >=%d y' % minyears)

# near model-free check: stations with many years in BOTH periods
print('--- stations well observed in both 1961-90 and 1991-2020: plain difference of the station period means')
for need in (20, 25, 28, 30):
    c1 = collections.Counter(S[(Y >= 1961) & (Y <= 1990)].tolist())
    c2 = collections.Counter(S[(Y >= 1991) & (Y <= 2020)].tolist())
    good = np.array([s for s in u.tolist() if c1.get(s, 0) >= need and c2.get(s, 0) >= need])
    if len(good) == 0:
        print('   need >=%d years in each: 0 stations' % need); continue
    m = np.isin(S, good)
    ds = []
    for s in good.tolist():
        ms = S == s
        ds.append(X[ms & (Y >= 1991) & (Y <= 2020)].mean() - X[ms & (Y >= 1961) & (Y <= 1990)].mean())
    ds = np.array(ds)
    uy, v = registered(S[m], Y[m], X[m]); uy2, v2, _, _ = twoway(S[m], Y[m], X[m])
    print('   need >=%d years in each: %d stations; mean station difference %.2f (se %.2f); registered within subset %.2f; two-way within subset %.2f' % (
        need, len(good), ds.mean(), ds.std(ddof=1) / len(ds) ** .5, shift(uy, v), shift(uy2, v2)))

# raw yearly mean (no station adjustment) for reference
uy, yi = np.unique(Y, return_inverse=True)
raw = np.bincount(yi, X) / np.bincount(yi)
after_T(uy, raw, 'raw yearly mean, all stations')
# median by year
med = np.array([np.median(X[Y == y]) for y in uy])
after_T(uy, med, 'raw yearly median, all stations')

# altitude / latitude composition over time (why raw and adjusted differ)
hdr2, ST, bad2 = read_stations()
alt = np.array([ST[s][3] for s in S.tolist()]); lat = np.array([ST[s][1] for s in S.tolist()])
for a, b in ((1951, 1960), (1961, 1990), (1991, 2020), (2011, 2023)):
    m = (Y >= a) & (Y <= b)
    print('   %d-%d: mean altitude of reporting records %.0f m, mean latitude %.2f, n=%d' % (a, b, alt[m].mean(), lat[m].mean(), m.sum()))
