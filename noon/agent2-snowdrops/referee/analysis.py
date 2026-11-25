"""Referee's blind recomputation. Written before opening snowdrops.py.
Usage: python -I analysis.py [daymode]   daymode in {true, jultag}
  true   = day of year computed from Eintrittsdatum (1 Jan of Referenzjahr = 1, 31 Dec before = 0)
  jultag = the service's Jultag column as given
"""
import sys, collections, datetime
sys.path.insert(0, '/home/agent2/referee-snowdrops')
import numpy as np
from load import read_records, read_stations, read_temp, true_doy

MODE = sys.argv[1] if len(sys.argv) > 1 else 'true'
TOL = 2  # a record is dropped if |Jultag - true day| > TOL (gives the README's "4 disagree")


def doy_to_date(x, leapyear=False):
    """calendar date of (possibly fractional) day number x in a non-leap year (or leap)"""
    y = 2024 if leapyear else 2023
    d = datetime.date(y, 1, 1) + datetime.timedelta(days=int(np.floor(x)) - 1)
    return d.strftime('%d %b')


hdr, R, bad = read_records()
sid, yr, qn, obj, ph, date, qb, jul = R.T
td = np.array([true_doy(int(y), int(d)) for y, d in zip(yr, date)])
N0 = len(R)
print('MODE =', MODE)
print('1. records in file:', N0)
doubt = qb == 5
print('   doubtful (QB=5):', doubt.sum())
pre = (~doubt) & (yr < 1951)
print('   before 1951 (of the rest):', pre.sum())
y24 = (~doubt) & (yr >= 2024)
print('   2024 (of the rest):', y24.sum())
rest = (~doubt) & (yr >= 1951) & (yr <= 2023)
dis = rest & (np.abs(jul - td) > TOL)
print('   date and Jultag disagree by more than %d days (of the rest):' % TOL, dis.sum())
print('   (disagree by exactly-not-0 and not explained by leap/Dec rule would be 6; see explore2)')
keep = rest & ~dis
print('   KEPT:', keep.sum(), ' stations:', len(set(sid[keep].tolist())))
print('   kept dated in the previous calendar year:', (keep & (date // 10000 < yr)).sum())

day = (td if MODE == 'true' else jul).astype(float)
S = sid[keep]; Y = yr[keep]; X = day[keep]; DATE = date[keep]

# stations with >= 15 years
u, inv, cnt = np.unique(S, return_inverse=True, return_counts=True)
big = cnt >= 15
print('   stations with >=15 years:', big.sum(), ' records:', cnt[big].sum())
m15 = big[inv]
per_year = collections.Counter(Y[m15].tolist())
print('   stations (>=15y) reporting per year: min', min(per_year.values()), 'in', min(per_year, key=per_year.get),
      ' max', max(per_year.values()), 'in', max(per_year, key=per_year.get), ' years present:', len(per_year))

print('2. median day, all kept records:', np.median(X), '->', doy_to_date(np.median(X)), ' mean:', X.mean())
print('   median of >=15y subset:', np.median(X[m15]))
print('   quartiles:', np.percentile(X, [25, 75]))

# ---- registered method
S15 = S[m15]; Y15 = Y[m15]; X15 = X[m15]
us, si = np.unique(S15, return_inverse=True)
uy, yi = np.unique(Y15, return_inverse=True)
ns, ny = len(us), len(uy)
smean = np.bincount(si, X15) / np.bincount(si)
anom = X15 - smean[si]
grand = X15.mean()
yearfig = np.bincount(yi, anom) / np.bincount(yi) + grand
grand_st = smean.mean()
print('3. overall mean of records (>=15y):', grand, ' mean of station means:', grand_st)


def pm(v, a, b):
    m = (uy >= a) & (uy <= b)
    return v[m].mean()


d_reg = pm(yearfig, 1991, 2020) - pm(yearfig, 1961, 1990)
print('   registered method: 1961-90 mean %.3f, 1991-2020 mean %.3f, difference %.3f' % (pm(yearfig, 1961, 1990), pm(yearfig, 1991, 2020), d_reg))

# ---- two-way fixed effects, exact: absorb stations, solve for years
# model x = a_s + b_y ; normal equations reduced to years.
n_s = np.bincount(si, minlength=ns).astype(float)
n_y = np.bincount(yi, minlength=ny).astype(float)
# incidence counts N[s,y]
Nsy = np.zeros((ns, ny))
np.add.at(Nsy, (si, yi), 1.0)
Tsy_y = np.bincount(yi, X15, minlength=ny)
Ts = np.bincount(si, X15, minlength=ns)
A = np.diag(n_y) - Nsy.T @ (Nsy / n_s[:, None])
rhs = Tsy_y - Nsy.T @ (Ts / n_s)
# singular (one constant); pin by min-norm solution
b = np.linalg.lstsq(A, rhs, rcond=None)[0]
a = (Ts - Nsy @ b) / n_s
resid = X15 - a[si] - b[yi]
# normalise: yearly figure = b_y + mean station effect (so it is "the average station" in each year)
year_tw = b + a.mean()
year_tw_rec = b + np.average(a, weights=n_s)
d_tw = pm(b, 1991, 2020) - pm(b, 1961, 1990)
print('   station+year effects together: difference %.3f  (resid sd %.2f)' % (d_tw, resid.std()))
# check connectedness: rank of A
print('   rank of reduced year system:', np.linalg.matrix_rank(A), 'of', ny)

# other robustness: all stations (no 15-year rule) two-way
# ---- temperatures
t1 = read_temp(1); t2 = read_temp(2)
T = np.array([(t1[int(y)] + t2[int(y)]) / 2 for y in uy])
Tw = np.array([(31 * t1[int(y)] + (29 if (y % 4 == 0 and (y % 100 or y % 400 == 0)) else 28) * t2[int(y)]) /
               (31 + (29 if (y % 4 == 0 and (y % 100 or y % 400 == 0)) else 28)) for y in uy])
from scipy import stats
for name, v in (('registered', yearfig), ('two-way', year_tw)):
    r = stats.linregress(T, v)
    print('4. %s yearly figure vs Jan-Feb mean T: r = %.4f, r^2 = %.4f, slope = %.3f days/degC (se %.3f), n=%d' % (name, r.rvalue, r.rvalue ** 2, r.slope, r.stderr, len(T)))
    r2 = stats.linregress(Tw, v)
    print('     (day-weighted Jan-Feb mean: r = %.4f, slope = %.3f)' % (r2.rvalue, r2.slope))
    print('     Spearman rho = %.4f' % stats.spearmanr(T, v)[0])
    # with a linear year term: partial trend after temperature
    Z = np.column_stack([np.ones(ny), T, uy - uy.mean()])
    coef, *_ = np.linalg.lstsq(Z, v, rcond=None)
    res = v - Z @ coef
    s2 = res @ res / (ny - 3)
    cov = s2 * np.linalg.inv(Z.T @ Z)
    print('     date ~ T + year: T coef %.3f (se %.3f), year coef %.4f d/yr (se %.4f) = %.2f d/decade, t=%.2f' % (coef[1], cov[1, 1] ** .5, coef[2], cov[2, 2] ** .5, coef[2] * 10, coef[2] / cov[2, 2] ** .5))
    rt = stats.linregress(uy, v)
    print('     date ~ year alone: %.4f d/yr (se %.4f), r=%.3f' % (rt.slope, rt.stderr, rt.rvalue))
    # period dummy after temperature
    P = ((uy >= 1991)).astype(float)
    m = (uy >= 1961) & (uy <= 2020)
    Z = np.column_stack([np.ones(m.sum()), T[m], P[m]])
    coef, *_ = np.linalg.lstsq(Z, v[m], rcond=None)
    res = v[m] - Z @ coef
    s2 = res @ res / (m.sum() - 3)
    cov = s2 * np.linalg.inv(Z.T @ Z)
    print('     1961-2020, date ~ T + [1991-2020]: period shift left = %.2f d (se %.2f)' % (coef[2], cov[2, 2] ** .5))
    # residual trend of simple-regression residuals
    res1 = v - (r.intercept + r.slope * T)
    rr = stats.linregress(uy, res1)
    print('     trend in residuals of date~T: %.4f d/yr (se %.4f, p=%.3f); resid mean 1961-90 %.2f, 1991-2020 %.2f' % (rr.slope, rr.stderr, rr.pvalue, res1[(uy >= 1961) & (uy <= 1990)].mean(), res1[(uy >= 1991) & (uy <= 2020)].mean()))
rT = stats.linregress(uy, T)
print('   Jan-Feb T trend: %.4f degC/yr; mean 1961-90 %.3f, 1991-2020 %.3f, diff %.3f' % (rT.slope, pm(T, 1961, 1990), pm(T, 1991, 2020), pm(T, 1991, 2020) - pm(T, 1961, 1990)))

# ---- gradients
hdr2, ST, bad2 = read_stations()
missing = [s for s in us.tolist() if s not in ST]
print('5. >=15y stations missing from station file:', len(missing), '; all kept stations missing:', len([s for s in u.tolist() if s not in ST]))
lat = np.array([ST[s][1] for s in us.tolist()]); lon = np.array([ST[s][2] for s in us.tolist()]); alt = np.array([ST[s][3] for s in us.tolist()])
print('   lat range', lat.min(), lat.max(), ' lon range', lon.min(), lon.max(), ' alt range', alt.min(), alt.max())


def grad(si_, yi_, x_, ny_):
    # regression x ~ alt + lat + lon + year dummies ; done by demeaning within year
    cnt_y = np.bincount(yi_, minlength=ny_)
    cols = []
    for v in (alt[si_] / 100.0, lat[si_], lon[si_], x_):
        mu = np.bincount(yi_, v, minlength=ny_) / np.maximum(cnt_y, 1)
        cols.append(v - mu[yi_])
    Z = np.column_stack(cols[:3]); yv = cols[3]
    return np.linalg.lstsq(Z, yv, rcond=None)[0]


g = grad(si, yi, X15, ny)
print('   gradients: %.3f d/100 m, %.3f d/deg lat, %.3f d/deg lon' % tuple(g))
# cluster bootstrap over stations
rng = np.random.default_rng(12345)
order = np.argsort(si, kind='stable')
starts = np.concatenate([[0], np.cumsum(np.bincount(si, minlength=ns))])
bs = []
for it in range(300):
    pick = rng.integers(0, ns, ns)
    idx = np.concatenate([order[starts[p]:starts[p + 1]] for p in pick])
    bs.append(grad(si[idx], yi[idx], X15[idx], ny))
bs = np.array(bs)
lo, hi = np.percentile(bs, [2.5, 97.5], axis=0)
for k, nm in enumerate(('alt /100m', 'lat /deg', 'lon /deg')):
    print('   %s: %.3f  [%.3f, %.3f] (station bootstrap, 300, 2.5-97.5%%), sd %.3f' % (nm, g[k], lo[k], hi[k], bs[:, k].std()))
# Hopkins: 4 days per degree latitude, per 5 deg longitude (eastward later in N America), per 400 ft (121.9 m)
print('   Hopkins reference: 4 d/deg lat; 4 d per 5 deg lon = 0.8 d/deg; 4 d per 400 ft = %.2f d/100 m' % (4 / 1.2192))
print('   correlation among predictors (station level): alt-lat %.3f, alt-lon %.3f, lat-lon %.3f' % (np.corrcoef(alt, lat)[0, 1], np.corrcoef(alt, lon)[0, 1], np.corrcoef(lat, lon)[0, 1]))

# ---- extremes
print('6. yearly figures (registered | two-way):')
o = np.argsort(yearfig)
for k in list(o[:3]) + list(o[-3:]):
    print('   %d  registered %.2f (%s)   two-way %.2f (%s)  JF T %.2f' % (uy[k], yearfig[k], doy_to_date(round(yearfig[k])), year_tw[k], doy_to_date(round(year_tw[k])), T[k]))
o2 = np.argsort(year_tw)
print('   two-way earliest:', [(int(uy[k]), round(float(year_tw[k]), 2)) for k in o2[:3]], ' latest:', [(int(uy[k]), round(float(year_tw[k]), 2)) for k in o2[-3:]])
np.savez('/home/agent2/referee-snowdrops/ref_%s.npz' % MODE, years=uy, reg=yearfig, tw=year_tw, T=T, nrec=n_y)
print('   full series:')
for k in range(ny):
    print('   %d %7.2f %7.2f %6.2f %5d' % (uy[k], yearfig[k], year_tw[k], T[k], n_y[k]))
