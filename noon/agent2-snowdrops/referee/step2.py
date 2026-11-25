"""Referee step 2: compare with Noon's results.npz and chase specific claims. Uses Jultag (Noon's choice) unless stated."""
import sys, collections, hashlib
sys.path.insert(0, '/home/agent2/referee-snowdrops')
import numpy as np
from scipy import stats
from load import read_records, read_stations, read_temp, true_doy, D

hdr, R, bad = read_records()
sid, yr, qn, obj, ph, date, qb, jul = R.T
td = np.array([true_doy(int(y), int(d)) for y, d in zip(yr, date)])
base = (qb != 5) & (yr >= 1951) & (yr <= 2023)
keep = base & (np.abs(jul - td) <= 1)
print('kept (tolerance 1):', keep.sum(), ' kept (tolerance 2):', (base & (np.abs(jul - td) <= 2)).sum())

# --- sha256 of the data files
for fn in ('PH_Jahresmelder_Wildwachsende_Pflanze_Schneegloeckchen_1925_2024_hist.txt', 'PH_Beschreibung_Phaenologie_Stationen_Jahresmelder.txt',
           'regional_averages_tm_01.txt', 'regional_averages_tm_02.txt', 'regional_averages_tm_12.txt'):
    print('sha256', hashlib.sha256(open(D + fn, 'rb').read()).hexdigest(), fn)

# --- Jultag consistency inside the kept set
leap = np.array([(y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)) for y in yr])
dy = date // 10000; mm = (date // 100) % 100; dd = date % 100
late = keep & leap & (dy == yr) & (td >= 60)        # 29 Feb or later in a leap year
print('kept records, leap years, dated 29 Feb or later:', late.sum())
print('   Jultag = calendar day - 1 (29 Feb omitted):', (late & (jul - td == -1)).sum())
print('   Jultag = calendar day (29 Feb counted):', (late & (jul - td == 0)).sum(), ' by year', sorted(collections.Counter(yr[late & (jul == td)].tolist()).items()))
f29 = keep & (mm == 2) & (dd == 29)
print('   kept records dated 29 Feb:', f29.sum(), ' Jultag values', sorted(collections.Counter(jul[f29].tolist()).items()))
print('   kept records with Jultag != calendar day:', (keep & (jul != td)).sum(), ' of which leap-late', (late & (jul != td)).sum(),
      ' December-before', (keep & (dy < yr) & (jul != td)).sum(), ' other', (keep & ~late & (dy == yr) & (jul != td)).sum())
print('   base records with Jultag != calendar day (what a strict first run would drop):', (base & (jul != td)).sum())

S = sid[keep]; Y = yr[keep]; XJ = jul[keep].astype(float); XT = td[keep].astype(float)
u, inv, cnt = np.unique(S, return_inverse=True, return_counts=True)
m15 = (cnt >= 15)[inv]
print('quartiles (Jultag) all kept:', np.percentile(XJ, [25, 50, 75]), ' >=15y stations:', np.percentile(XJ[m15], [25, 50, 75]))
print('   share of all kept records with Jultag in [45,70]: %.3f ; in [46,70]: %.3f ; in [46,69]: %.3f' % (((XJ >= 45) & (XJ <= 70)).mean(), ((XJ >= 46) & (XJ <= 70)).mean(), ((XJ >= 46) & (XJ <= 69)).mean()))


def registered(S, Y, X):
    us, si = np.unique(S, return_inverse=True)
    uy, yi = np.unique(Y, return_inverse=True)
    sm = np.bincount(si, X) / np.bincount(si)
    an = X - sm[si]
    return uy, np.bincount(yi, an) / np.bincount(yi) + X.mean()


def twoway(S, Y, X):
    us, si = np.unique(S, return_inverse=True)
    uy, yi = np.unique(Y, return_inverse=True)
    ns, ny = len(us), len(uy)
    n_s = np.bincount(si, minlength=ns).astype(float); n_y = np.bincount(yi, minlength=ny).astype(float)
    Nsy = np.zeros((ns, ny)); np.add.at(Nsy, (si, yi), 1.0)
    Ty = np.bincount(yi, X, minlength=ny); Ts = np.bincount(si, X, minlength=ns)
    A = np.diag(n_y) - Nsy.T @ (Nsy / n_s[:, None]); rhs = Ty - Nsy.T @ (Ts / n_s)
    b = np.linalg.lstsq(A, rhs, rcond=None)[0]
    a = (Ts - Nsy @ b) / n_s
    return uy, b + a.mean(), us, a


uy, reg = registered(S[m15], Y[m15], XJ[m15])
_, tw, us, a = twoway(S[m15], Y[m15], XJ[m15])
Z = np.load('/srv/commons/agent2-snowdrops/results.npz', allow_pickle=False)
print('results.npz keys:', list(Z.keys()))
print('max |my registered - Noon yearly|: %.2e' % np.abs(reg - Z['yearly']).max())
d2 = tw - Z['yearly2']
print('my exact two-way - Noon yearly2 (60 backfitting passes): mean %.4f, max |dev from mean| %.4f, slope of difference %.5f d/yr' % (d2.mean(), np.abs(d2 - d2.mean()).max(), np.polyfit(uy, d2, 1)[0]))
p1 = (uy >= 1961) & (uy <= 1990); p2 = (uy >= 1991) & (uy <= 2020)
print('shift: registered mine %.3f Noon %.3f | two-way mine %.3f Noon %.3f' % (reg[p2].mean() - reg[p1].mean(), Z['yearly'][p2].mean() - Z['yearly'][p1].mean(), tw[p2].mean() - tw[p1].mean(), Z['yearly2'][p2].mean() - Z['yearly2'][p1].mean()))
t1 = read_temp(1); t2 = read_temp(2); t12 = read_temp(12)
T = np.array([(t1[int(y)] + t2[int(y)]) / 2 for y in uy]); T3 = np.array([(t12[int(y) - 1] + t1[int(y)] + t2[int(y)]) / 3 for y in uy])
print('max |my T - Noon tjf| %.2e' % np.abs(T - Z['tjf']).max())
print('Noon coef', Z['coef'], 'lo', Z['lo'], 'hi', Z['hi'])


def ols(Zm, v):
    coef, *_ = np.linalg.lstsq(Zm, v, rcond=None)
    res = v - Zm @ coef
    cov = (res @ res / (len(v) - Zm.shape[1])) * np.linalg.inv(Zm.T @ Zm)
    return coef, np.sqrt(np.diag(cov)), res


print('\n=== "the winter explains nearly all of it" / "no trend is left" ===')
for name, v in (('registered (Noon yearly)', Z['yearly']), ('two-way (Noon yearly2)', Z['yearly2']), ('two-way (my exact)', tw)):
    for tn, TT in (('Jan-Feb', T), ('Dec-Feb', T3)):
        r = stats.linregress(TT, v)
        res = v - (r.intercept + r.slope * TT)
        rr = stats.linregress(uy, res)
        dT = TT[p2].mean() - TT[p1].mean(); sh = v[p2].mean() - v[p1].mean()
        c, se, _ = ols(np.column_stack([np.ones(len(uy)), TT, (uy - uy.mean()) / 10]), v)
        print('%-26s %-7s r %.3f slope %.2f | shift %.2f, slope*dT %.2f = %.0f%% | residual trend (Noon two-step) %+.2f d/decade (p=%.3f) | joint: T %.2f, year %+.2f d/decade (se %.2f, t %.2f) | resid mean 61-90 %+.2f, 91-20 %+.2f' % (
            name, tn, r.rvalue, r.slope, sh, r.slope * dT, 100 * r.slope * dT / sh, 10 * rr.slope, rr.pvalue, c[1], c[2], se[2], c[2] / se[2], res[p1].mean(), res[p2].mean()))
# detrended (first-difference) sensitivity: not contaminated by any trend bias
for name, v in (('registered', Z['yearly']), ('two-way', tw)):
    r = stats.linregress(np.diff(T), np.diff(v))
    print('   first differences, %s: slope %.2f d/degC, r %.3f' % (name, r.slope, r.rvalue))

print('\n=== "Most of the move happened in the late 1980s; before that the date was drifting later" ===')
for name, v in (('registered', Z['yearly']), ('two-way', tw), ('Jan-Feb T', T)):
    a_ = stats.linregress(uy, v); b_ = stats.linregress(uy[uy <= 1987], v[uy <= 1987]); c_ = stats.linregress(uy[uy >= 1988], v[uy >= 1988])
    print('%-11s trend 1951-2023 %+.2f/decade (se %.2f); 1951-1987 %+.2f (se %.2f, p=%.2f); 1988-2023 %+.2f (se %.2f, p=%.2f); mean 1951-87 %.2f, 1988-2023 %.2f, step %.2f' % (
        name, 10 * a_.slope, 10 * a_.stderr, 10 * b_.slope, 10 * b_.stderr, b_.pvalue, 10 * c_.slope, 10 * c_.stderr, c_.pvalue, v[uy <= 1987].mean(), v[uy >= 1988].mean(), v[uy >= 1988].mean() - v[uy <= 1987].mean()))
    print('            decade means:', ' '.join('%d0s %.1f' % (d // 10, v[(uy >= d) & (uy < d + 10)].mean()) for d in range(1951, 2021, 10)), '| 2021-23 %.1f' % v[uy >= 2021].mean())
    # best single breakpoint for a step function
    best = min(((np.sum((v[uy < y] - v[uy < y].mean()) ** 2) + np.sum((v[uy >= y] - v[uy >= y].mean()) ** 2)), y) for y in range(1956, 2019))
    print('            least-squares single step falls at', best[1])

print('\n=== Noon\'s first-run mistake: drop every record whose Jultag != calendar day ===')
strict = base & (jul == td)
print('records dropped by strict rule:', (base & (jul != td)).sum(), '; leap-year late dates among them:', (base & (jul != td) & leap & (dy == yr) & (td >= 60)).sum())
Ss = sid[strict]; Ys = yr[strict]; Xs = jul[strict].astype(float)
u2, inv2, cnt2 = np.unique(Ss, return_inverse=True, return_counts=True)
ms = (cnt2 >= 15)[inv2]
uy2, regs = registered(Ss[ms], Ys[ms], Xs[ms])
print('registered shift under strict rule: %.2f' % (regs[(uy2 >= 1991) & (uy2 <= 2020)].mean() - regs[(uy2 >= 1961) & (uy2 <= 1990)].mean()))

print('\n=== S7 ===')
v = Z['yearly']
print('sd %.2f; min %.2f (%d); max %.2f (%d); gap %.2f' % (v.std(ddof=1), v.min(), uy[v.argmin()], v.max(), uy[v.argmax()], v.max() - v.min()))
print('two-way: sd %.2f; min %.2f (%d); max %.2f (%d); gap %.2f' % (tw.std(ddof=1), tw.min(), uy[tw.argmin()], tw.max(), uy[tw.argmax()], tw.max() - tw.min()))
np.savez('/home/agent2/referee-snowdrops/step2_series.npz', years=uy, reg=reg, tw=tw, T=T, T3=T3)
