"""Referee step 3: Hopkins checks (linearity, collinearity), station file oddities, robustness of residual trend."""
import sys, collections
sys.path.insert(0, '/home/agent2/referee-snowdrops')
import numpy as np
from scipy import stats
from load import read_records, read_stations, read_temp, true_doy

hdr, R, bad = read_records()
sid, yr, qn, obj, ph, date, qb, jul = R.T
td = np.array([true_doy(int(y), int(d)) for y, d in zip(yr, date)])
keep = (qb != 5) & (yr >= 1951) & (yr <= 2023) & (np.abs(jul - td) <= 1)
S = sid[keep]; Y = yr[keep]; X = jul[keep].astype(float)
u, inv, cnt = np.unique(S, return_inverse=True, return_counts=True)
m15 = (cnt >= 15)[inv]
S = S[m15]; Y = Y[m15]; X = X[m15]
hdr2, ST, bad2 = read_stations()
print('station file: rows parsed', len(ST), ' problem rows', len(bad2))
for b in bad2[:5]:
    print('   ', b[0], repr(b[1][:120]))
us, si = np.unique(S, return_inverse=True)
uy, yi = np.unique(Y, return_inverse=True)
lat_s = np.array([ST[s][1] for s in us.tolist()]); lon_s = np.array([ST[s][2] for s in us.tolist()]); alt_s = np.array([ST[s][3] for s in us.tolist()])
print('stations used with altitude 0:', (alt_s == 0).sum(), [ST[s][0][:30] for s in us[alt_s == 0].tolist()][:8])
print('stations used with altitude <= 2 m:', (alt_s <= 2).sum(), '; > 900 m:', [(ST[s][0][:30], ST[s][3]) for s in us[alt_s > 900].tolist()])
# semicolons inside names would shift columns: check field count of the station file
import io
counts = collections.Counter()
with open('/home/agent2/downloads/dwd-phenology/PH_Beschreibung_Phaenologie_Stationen_Jahresmelder.txt', encoding='latin-1', newline='') as f:
    f.readline()
    for line in f:
        counts[line.count(';')] += 1
print('station file: number of semicolons per row:', dict(counts))

alt = alt_s[si] / 100.0; lat = lat_s[si]; lon = lon_s[si]
ny = len(uy)


def within(v, yi_=yi):
    mu = np.bincount(yi_, v, minlength=ny) / np.bincount(yi_, minlength=ny)
    return v - mu[yi_]


def fit(cols, y, yi_=yi):
    Z = np.column_stack([within(c, yi_) for c in cols]); yv = within(y, yi_)
    coef = np.linalg.lstsq(Z, yv, rcond=None)[0]
    r2 = 1 - ((yv - Z @ coef) ** 2).sum() / (yv ** 2).sum()
    return coef, r2


c, r2 = fit([alt, lat, lon], X)
print('gradients (Jultag): %.3f /100 m, %.3f /deg N, %.3f /deg E; within-year R2 %.3f' % (c[0], c[1], c[2], r2))
# one at a time (shows what the collinearity does)
for nm, col in (('altitude alone', [alt]), ('latitude alone', [lat]), ('longitude alone', [lon]), ('altitude+latitude', [alt, lat])):
    cc, rr = fit(col, X)
    print('   %-18s' % nm, np.round(cc, 3), 'R2 %.3f' % rr)
# linearity of altitude: slope within latitude bands
print('altitude slope within latitude bands (lat, lon linear inside the band too):')
for a, b in ((47, 49), (49, 50), (50, 51), (51, 52), (52, 53), (53, 56)):
    m = (lat >= a) & (lat < b)
    uyb, yib = np.unique(Y[m], return_inverse=True)

    def w(v):
        mu = np.bincount(yib, v) / np.bincount(yib)
        return v - mu[yib]
    Z = np.column_stack([w(alt[m]), w(lat[m]), w(lon[m])]); yv = w(X[m])
    cc = np.linalg.lstsq(Z, yv, rcond=None)[0]
    print('   lat %d-%d: n=%6d stations=%4d  alt %.2f  lat %.2f  lon %.2f   (alt range %.0f-%.0f m)' % (a, b, m.sum(), len(set(S[m].tolist())), cc[0], cc[1], cc[2], 100 * alt[m].min(), 100 * alt[m].max()))
# piecewise-linear altitude and latitude (knots), joint
print('piecewise fits:')
for knots_alt, knots_lat in (((2.0, 4.0), ()), ((), (50.0, 53.0)), ((2.0, 4.0), (50.0, 53.0))):
    cols = [alt] + [np.maximum(alt - k, 0) for k in knots_alt] + [lat] + [np.maximum(lat - k, 0) for k in knots_lat] + [lon]
    cc, rr = fit(cols, X)
    na = 1 + len(knots_alt); nl = 1 + len(knots_lat)
    sa = np.cumsum(cc[:na]); sl = np.cumsum(cc[na:na + nl])
    print('   alt knots %s -> segment slopes %s d/100 m | lat knots %s -> segment slopes %s d/deg | lon %.2f | R2 %.3f' % (knots_alt, np.round(sa, 2), knots_lat, np.round(sl, 2), cc[-1], rr))
# is the altitude gradient the same if stations are weighted equally (station effects regression)?
Zs = np.load('/srv/commons/agent2-snowdrops/results.npz', allow_pickle=False)
A = np.column_stack([np.ones(len(Zs['st_alt'])), Zs['st_alt'] / 100, Zs['st_lat'], Zs['st_lon']])
cs = np.linalg.lstsq(A, Zs['st_eff'], rcond=None)[0]
print('station-level regression of Noon station effects (each station once): alt %.2f, lat %.2f, lon %.2f' % (cs[1], cs[2], cs[3]))
print('per 100 km: latitude %.2f d, longitude at 51N %.2f d' % (c[1] / 1.1119, c[2] / (1.1119 * np.cos(np.radians(51)))))
print('Dutch-to-Polish border, 6.0E-14.6E:', round(c[2] * 8.6, 1), ' ; lon range of stations', lon.min(), lon.max())

# ---- residual trend robustness for the unbiased series: quadratic in T, robust regression, leave-one-out
z = np.load('/home/agent2/referee-snowdrops/step2_series.npz')
yrs, reg, tw, T, T3 = z['years'], z['reg'], z['tw'], z['T'], z['T3']


def ols(Zm, v):
    coef, *_ = np.linalg.lstsq(Zm, v, rcond=None)
    res = v - Zm @ coef
    cov = (res @ res / (len(v) - Zm.shape[1])) * np.linalg.inv(Zm.T @ Zm)
    return coef, np.sqrt(np.diag(cov)), res


t = (yrs - yrs.mean()) / 10
for nm, v in (('registered', reg), ('two-way', tw)):
    c1, s1, _ = ols(np.column_stack([np.ones(len(t)), T, T ** 2, t]), v)
    print('%s: date ~ T + T^2 + year: T^2 coef %.3f (t %.2f); year %+.2f d/decade (t %.2f)' % (nm, c1[2], c1[2] / s1[2], c1[3], c1[3] / s1[3]))
    c2, s2, _ = ols(np.column_stack([np.ones(len(t)), z['T'], z['T3'] * 3 - z['T'] * 2, t]), v)   # Jan-Feb mean and December separately
    print('%s: date ~ T(JF) + T(Dec) + year: JF %.2f, Dec %.2f (t %.2f), year %+.2f d/decade (t %.2f)' % (nm, c2[1], c2[2], c2[2] / s2[2], c2[3], c2[3] / s2[3]))
    # leave-one-year-out range of the year coefficient
    loo = []
    for k in range(len(t)):
        m = np.arange(len(t)) != k
        cc, ss, _ = ols(np.column_stack([np.ones(m.sum()), T[m], t[m]]), v[m])
        loo.append(cc[2])
    print('%s: year term after T, leave-one-year-out range: %+.2f to %+.2f d/decade' % (nm, min(loo), max(loo)))
    # starting 1961 only
    m = yrs >= 1961
    cc, ss, _ = ols(np.column_stack([np.ones(m.sum()), T[m], t[m]]), v[m])
    print('%s: 1961-2023 only: year term after T %+.2f d/decade (t %.2f)' % (nm, cc[2], cc[2] / ss[2]))
    # Theil-Sen slope of the residuals from date~T
    r = stats.linregress(T, v); res = v - r.intercept - r.slope * T
    ts = stats.theilslopes(res, yrs)
    print('%s: Theil-Sen slope of residuals %+.2f d/decade (95%% %+.2f to %+.2f); Kendall tau p=%.3f' % (nm, 10 * ts[0], 10 * ts[2], 10 * ts[3], stats.kendalltau(yrs, res)[1]))
