"""Referee controls. Usage: python -I controls.py series.csv levels.csv ledger.csv"""
import sys
import numpy as np
import pandas as pd

s = pd.read_csv(sys.argv[1], dtype={"month": str}).set_index("month").apply(pd.to_numeric, errors="coerce")
lv = pd.read_csv(sys.argv[2], dtype={"month": str}).set_index("month").apply(pd.to_numeric, errors="coerce")
s.index = pd.PeriodIndex(s.index, freq="M"); lv.index = pd.PeriodIndex(lv.index, freq="M")
s = s.join(lv)
P = print
def r(a, b):
    d = pd.concat([a, b], axis=1).dropna()
    if len(d) < 3: return float("nan"), len(d)
    return float(np.corrcoef(d.iloc[:, 0], d.iloc[:, 1])[0, 1]), len(d)
o, u, q = s.openings_rate, s.unemployment_rate, s.quits_rate

P("=== A. Beveridge correlation and the cuts")
for a, b in [("2000-12", "2019-12"), ("2000-12", "2020-02"), ("2001-01", "2009-12"), ("2010-01", "2019-12"), ("2020-01", "2026-12"),
             ("2001-01", "2007-12"), ("2008-01", "2019-12"), ("2001-01", "2010-12"), ("2011-01", "2019-12"), ("2000-12", "2008-12"), ("2009-01", "2019-12"),
             ("2005-01", "2014-12"), ("2007-01", "2016-12"), ("2015-01", "2024-12"),
             ("2020-01", "2020-12"), ("2021-01", "2026-12"), ("2020-07", "2026-12"), ("2022-03", "2026-12"), ("2021-01", "2023-12"), ("2024-01", "2026-12")]:
    rr, n = r(o.loc[a:b], u.loc[a:b]); P(f"  {a}..{b}: r={rr:+.3f} n={n}")
# all months leaving out 2020-03..2020-12 only
k = ~((s.index >= pd.Period("2020-03")) & (s.index <= pd.Period("2020-12")))
P("  all months without 2020-03..2020-12: r=%+.3f n=%d" % r(o[k], u[k]))
k = ~((s.index >= pd.Period("2020-03")) & (s.index <= pd.Period("2021-12")))
P("  all months without 2020-03..2021-12: r=%+.3f n=%d" % r(o[k], u[k]))
# rolling 120-month windows
d = pd.concat([o, u], axis=1).dropna()
rol = [(str(d.index[i]), np.corrcoef(d.iloc[i:i + 120, 0], d.iloc[i:i + 120, 1])[0, 1]) for i in range(0, len(d) - 119)]
rv = np.array([x[1] for x in rol])
P(f"  rolling 120-month windows: n={len(rol)}; min {rv.min():+.3f} (start {rol[int(rv.argmin())][0]}), max {rv.max():+.3f} (start {rol[int(rv.argmax())][0]}); windows starting 2001-01..2010-01 range {min(x[1] for x in rol if x[0] <= '2010-01'):+.3f}..{max(x[1] for x in rol if x[0] <= '2010-01'):+.3f}")
for st in ["2001-01", "2003-01", "2005-01", "2007-01", "2009-01", "2010-01", "2011-01", "2013-01", "2015-01"]:
    P("    window from", st, "%+.3f" % dict(rol)[st])
# Spearman all
P("  spearman all months: %+.3f" % d.corr(method="spearman").iloc[0, 1])

P("=== B. V3 band / years robustness")
def bm(y0, y1, lo, hi):
    x = s.loc[f"{y0}-01":f"{y1}-12"]; x = x[(x.unemployment_rate >= lo - 1e-9) & (x.unemployment_rate <= hi + 1e-9)].dropna(subset=["openings_rate"])
    return x
for lo, hi in [(3.4, 4.5), (3.5, 4.0), (3.4, 3.9), (3.6, 4.4), (3.8, 4.5), (4.0, 4.5), (3.4, 5.0), (3.5, 3.7)]:
    line = f"  band {lo}-{hi}:"
    for (a0, a1), (b0, b1) in [((2021, 2023), (2017, 2019)), ((2021, 2023), (2018, 2019)), ((2021, 2023), (2015, 2019)), ((2022, 2023), (2017, 2019)), ((2022, 2024), (2017, 2019)), ((2024, 2026), (2017, 2019)), ((2025, 2026), (2017, 2019))]:
        A, B = bm(a0, a1, lo, hi), bm(b0, b1, lo, hi)
        if len(A) and len(B): line += f" {a0}-{str(a1)[2:]}v{b0}-{str(b1)[2:]} {A.openings_rate.mean() - B.openings_rate.mean():+.2f}({len(A)},{len(B)});"
        else: line += f" {a0}-{str(a1)[2:]}v{b0}-{str(b1)[2:]} n/a({len(A)},{len(B)});"
    P(line)
# matched on exact unemployment value
def matched(a0, a1, b0, b1, lo=3.4, hi=4.5):
    A, B = bm(a0, a1, lo, hi), bm(b0, b1, lo, hi)
    ga, gb = A.groupby(A.unemployment_rate.round(1)).openings_rate, B.groupby(B.unemployment_rate.round(1)).openings_rate
    ma, mb, na, nb = ga.mean(), gb.mean(), ga.count(), gb.count()
    common = sorted(set(ma.index) & set(mb.index))
    w = np.array([min(na[c], nb[c]) for c in common]); dd = np.array([ma[c] - mb[c] for c in common])
    return common, dd, w, A.unemployment_rate.mean(), B.unemployment_rate.mean()
for (a0, a1, b0, b1) in [(2021, 2023, 2017, 2019), (2024, 2026, 2017, 2019), (2025, 2026, 2017, 2019)]:
    c, dd, w, ua, ub = matched(a0, a1, b0, b1)
    P(f"  matched on exact unemployment rate {a0}-{a1} v {b0}-{b1}: mean u in band {ua:.2f} v {ub:.2f}; values {c}; diffs {np.round(dd, 2).tolist()}; weighted mean diff {np.average(dd, weights=w):+.2f}; min diff {dd.min():+.2f}")
x = s.loc["2017-01":"2019-12"]; x = x[(x.unemployment_rate >= 3.4) & (x.unemployment_rate <= 4.5)]
sl = np.polyfit(x.unemployment_rate, x.openings_rate, 1); P(f"  2017-19 in-band line: openings = {sl[1]:.2f} + {sl[0]:.2f}*u")
for a0, a1 in [(2021, 2023), (2024, 2026), (2025, 2026)]:
    A = bm(a0, a1, 3.4, 4.5); P(f"  {a0}-{a1} in band: mean openings minus the 2017-19 line at the same u: {(A.openings_rate - (sl[1] + sl[0] * A.unemployment_rate)).mean():+.2f} (n={len(A)})")
P("  months in band by year:", {y: int(((s.unemployment_rate[s.index.year == y] >= 3.4) & (s.unemployment_rate[s.index.year == y] <= 4.5) & s.openings_rate[s.index.year == y].notna()).sum()) for y in range(2016, 2027)})

P("=== C. soft landing horizons from 2022-03")
m0 = o.dropna().idxmax()
for h in (6, 12, 18, 24, 30, 36, 42, 48, 54):
    m1 = m0 + h
    if m1 in s.index and pd.notna(o.get(m1, np.nan)):
        do, du = o[m1] - o[m0], u[m1] - u[m0]
        P(f"  +{h:2d} ({m1}): openings {o[m1]} ({do:+.1f}); unemployment {u[m1]} ({du:+.1f}); held={(do <= -1.5 + 1e-9) and (du < 0.7 - 1e-9)}")
after = u.loc[m0:]
P(f"  unemployment after {m0}: min {after.min()} first {after.idxmin()}; max {after.max()} first {after.idxmax()}; latest {after.dropna().iloc[-1]} at {after.dropna().index[-1]}; rise low->max {after.max() - after.min():.1f}; peak-month->max {after.max() - u[m0]:.1f}")
P(f"  openings rate latest {o.dropna().iloc[-1]} at {o.dropna().index[-1]}; min after peak {o.loc[m0:].min()} at {o.loc[m0:].idxmin()}")
o3 = o.rolling(3, center=True).mean(); P(f"  peak of centred 3-month mean openings rate: {o3.idxmax()} ({o3.max():.2f}); peak of openings level: {s.openings_level.idxmax()}")
P("  other large falls of openings rate for comparison: 2000-12..2003-xx and 2007..2009")
for a, b in [("2000-12", "2003-12"), ("2007-01", "2009-12")]:
    oo = o.loc[a:b]; pk = oo.idxmax(); m1 = pk + 24
    P(f"    peak {pk} {oo.max()} -> +24 {m1}: openings {o[m1]} ({o[m1]-oo.max():+.1f}), unemployment {u[pk]} -> {u[m1]} ({u[m1]-u[pk]:+.1f})")

P("=== D. settled details: flips?")
d = s[["quits_rate", "layoffs_rate"]].dropna(); P(f"  V7 ties as above: {100*(d.quits_rate >= d.layoffs_rate).mean():.1f}%")
d = s[["hires_rate", "separations_rate"]].dropna(); P(f"  V8 ties as above: {100*(d.hires_rate >= d.separations_rate).mean():.1f}%  (bar 70) ; strict {100*(d.hires_rate > d.separations_rate).mean():.1f}%")
P(f"  V8 ties: by period {d[d.hires_rate == d.separations_rate].groupby(lambda p: p.year // 5 * 5).size().to_dict()}")
dl = s[["hires_level", "separations_level"]].dropna(); gap = (dl.hires_level - dl.separations_level)
tie = d.hires_rate == d.separations_rate
P(f"  V8 on levels in the 52 tie months: hires above in {(gap[tie] > 0).sum()}, below in {(gap[tie] < 0).sum()}; on levels overall {100*(gap > 0).mean():.1f}%")
P(f"  V8 on levels: months where rate ordering contradicts level ordering: {int(((d.hires_rate > d.separations_rate) & (gap < 0)).sum() + ((d.hires_rate < d.separations_rate) & (gap > 0)).sum())}")
vr = (s.openings_rate / s.unemployment_rate).dropna(); P(f"  V4 with rates in place of levels: peak {vr.max():.3f} at {vr.idxmax()}")
vu = (s.openings_level / s.unemployed_level).dropna(); P(f"  V4 levels: top 3 {[(str(k), round(v, 3)) for k, v in vu.sort_values(ascending=False).head(3).items()]}")
o9 = o.loc["2009-01":"2009-12"]; u9 = u.loc["2009-01":"2009-12"]
P(f"  V11 last month of extreme: openings low last {o9[o9 == o9.min()].index[-1]}, unemployment high last {u9[u9 == u9.max()].index[-1]}; on openings LEVEL lowest in 2009: {s.openings_level.loc['2009-01':'2009-12'].idxmin()}; unemployed LEVEL highest in 2009: {s.unemployed_level.loc['2009-01':'2009-12'].idxmax()}; whole record unemployed-level/ rate max 2008-2011: {u.loc['2008-01':'2011-12'].idxmax()} {s.unemployed_level.loc['2008-01':'2011-12'].idxmax()}; openings level min 2008-2011: {s.openings_level.loc['2008-01':'2011-12'].idxmin()}")
l = s.layoffs_rate.dropna(); P(f"  V6: months at max {[str(x) for x in l[l == l.max()].index]}")

P("=== E. V12: rounding and definitions")
# employment implied by levels and rounded rates; three estimates
E1 = s.hires_level / (s.hires_rate / 100); E2 = s.separations_level / (s.separations_rate / 100); E3 = s.openings_level * (100 - s.openings_rate) / s.openings_rate
E = pd.concat([E1, E2, E3], axis=1).median(axis=1)
Elo = pd.concat([s.hires_level / ((s.hires_rate + 0.05) / 100), s.separations_level / ((s.separations_rate + 0.05) / 100), s.openings_level * (100 - (s.openings_rate + 0.05)) / (s.openings_rate + 0.05)], axis=1).max(axis=1)
Ehi = pd.concat([s.hires_level / ((s.hires_rate - 0.05) / 100), s.separations_level / ((s.separations_rate - 0.05) / 100), s.openings_level * (100 - (s.openings_rate - 0.05)) / (s.openings_rate - 0.05)], axis=1).min(axis=1)
P(f"  implied employment: months where the three rounding intervals do not overlap: {int((Elo > Ehi).sum())} of {int(Elo.notna().sum())}; mean relative width of the feasible interval {((Ehi - Elo) / E).mean():.4f}")
def unr(Ex): return (s.hires_level / s.openings_level) * (1 + s.openings_level / Ex)
for nm, Ex in [("median E", E), ("lowest feasible E", Elo), ("highest feasible E", Ehi)]:
    ru = unr(Ex).dropna(); ym = ru.groupby(ru.index.year).mean()
    P(f"  hires rate / openings rate from unrounded levels ({nm}): 2020 mean-of-ratios {ym[2020]:.4f}; 2013 {ym[2013]:.4f}; 2014 {ym[2014]:.4f}; 2015 {ym[2015]:.4f}; 2018 {ym[2018]:.4f}; all 2001-13 >1: {all(ym[y] > 1 for y in range(2001, 2014))}; all 2018-24 <1: {all(ym[y] < 1 for y in range(2018, 2025))}")
hrE = (s.hires_level.groupby(s.index.year).sum() / s.openings_level.groupby(s.index.year).sum())
P(f"  2020 ratio of yearly sums on unrounded levels x(1+O/E): {(s.hires_level.loc['2020'].sum() / E.loc['2020'].sum()) / (s.openings_level.loc['2020'].sum() / (E.loc['2020'] + s.openings_level.loc['2020']).sum()):.4f}")
rr_ = (s.hires_rate / s.openings_rate)
P("  2020 monthly, rounded rates ratio vs unrounded:", [(str(k)[5:], round(float(rr_[k]), 3), round(float(unr(E)[k]), 3)) for k in s.loc["2020-01":"2020-12"].index])
lr = (s.hires_level / s.openings_level).dropna(); yl = lr.groupby(lr.index.year).mean()
P(f"  hires LEVEL / openings LEVEL yearly mean: 2020 {yl[2020]:.4f}; 2013 {yl[2013]:.4f}; 2014 {yl[2014]:.4f}; 2015 {yl[2015]:.4f}; min 2001-13 {min(yl[y] for y in range(2001, 2014)):.4f}; max 2018-24 {max(yl[y] for y in range(2018, 2025)):.4f}; years above 1: {[int(y) for y in yl.index if yl[y] > 1]}")
ym = rr_.dropna().groupby(rr_.dropna().index.year).mean()
ymed = rr_.dropna().groupby(rr_.dropna().index.year).median()
P(f"  rounded rates 2020: mean-of-ratios {ym[2020]:.5f}; ratio-of-means {s.hires_rate.loc['2020'].mean() / s.openings_rate.loc['2020'].mean():.5f}; median of monthly ratios {ymed[2020]:.4f}; months above 1 in 2020: {int((rr_.loc['2020'] > 1).sum())}; without 2020-05 and 2020-06: {rr_.loc['2020'].drop([pd.Period('2020-05'), pd.Period('2020-06')]).mean():.4f}")
# rounding monte-carlo on rounded rates: jitter each rate uniformly within +-0.05
rng = np.random.default_rng(1); h20 = s.hires_rate.loc["2020"].values; o20 = s.openings_rate.loc["2020"].values
sim = np.array([((h20 + rng.uniform(-.05, .05, 12)) / (o20 + rng.uniform(-.05, .05, 12))).mean() for _ in range(20000)])
P(f"  rounded rates jittered within +-0.05: 2020 mean ratio 2.5%..97.5% = {np.percentile(sim, 2.5):.4f}..{np.percentile(sim, 97.5):.4f}; share above 1: {(sim > 1).mean():.3f}")

P("=== F. quits and pay")
ahe = s.hourly_earnings
w12 = 100 * (ahe / ahe.shift(12) - 1)
def prof(qs, ws, lags, keep=None):
    res = {}
    for k in lags:
        wk = ws.shift(-k)  # wage growth k months later, aligned on the quits month
        d = pd.concat([qs, wk], axis=1).dropna()
        if keep is not None:
            d = d[[keep(t, t + k) for t in d.index]]
        res[k] = (np.corrcoef(d.iloc[:, 0], d.iloc[:, 1])[0, 1], len(d))
    return res
lags = list(range(-24, 37, 3))
pf = prof(q, w12, lags)
P("  full sample, 12-month wage growth; lag(months wage after quits): r")
P("   ", "  ".join(f"{k:+d}:{v[0]:+.2f}" for k, v in pf.items()))
pm = prof(q, w12, range(0, 31)); best = max(pm, key=lambda k: pm[k][0]); P(f"    monthly lags 0..30: maximum at +{best} ({pm[best][0]:+.3f}); +12 {pm[12][0]:+.3f}; +6 {pm[6][0]:+.3f}")
W0, W1 = pd.Period("2020-03"), pd.Period("2021-06")
noon = lambda t, tw: not (W0 <= t <= W1)
either = lambda t, tw: not (W0 <= t <= W1) and not (W0 <= tw <= W1)
wide = lambda t, tw: not (W0 <= t <= pd.Period("2022-03")) and not (W0 <= tw <= pd.Period("2022-03"))
prepan = lambda t, tw: t <= pd.Period("2020-02") and tw <= pd.Period("2020-02")
no2123 = lambda t, tw: not (2021 <= t.year <= 2023) and not (2021 <= tw.year <= 2023)
post = lambda t, tw: t >= pd.Period("2021-07") and tw >= pd.Period("2021-07")
for nm, kf in [("Noon's exclusion (quits month in 2020-03..2021-06)", noon), ("either month in 2020-03..2021-06", either), ("either month in 2020-03..2022-03", wide),
               ("before the pandemic only (both months <= 2020-02)", prepan), ("without 2021-2023 (either month)", no2123), ("both months >= 2021-07", post)]:
    pk = prof(q, w12, [-12, -6, 0, 3, 6, 9, 12, 18, 24], kf)
    P(f"  {nm}:"); P("   ", "  ".join(f"{k:+d}:{v[0]:+.2f}(n{v[1]})" for k, v in pk.items()))
# shorter wage windows: the 12-month growth at t+12 is growth over t..t+12
for win in (1, 3, 6):
    wshort = 100 * ((ahe / ahe.shift(win)) ** (12 / win) - 1)
    for nm, kf in [("all", None), ("either month outside 2020-03..2021-06", either), ("pre-pandemic", prepan)]:
        pk = prof(q, wshort, range(-12, 31), kf); bestk = max(pk, key=lambda k: pk[k][0])
        P(f"  {win}-month annualised wage growth [{nm}]: r at 0 {pk[0][0]:+.2f}, +3 {pk[3][0]:+.2f}, +6 {pk[6][0]:+.2f}, +9 {pk[9][0]:+.2f}, +12 {pk[12][0]:+.2f}, -6 {pk[-6][0]:+.2f}; max at {bestk:+d} ({pk[bestk][0]:+.2f})")
# forward 12-month growth is exactly w12 shifted; centre the window: quits_t vs growth over t-6..t+6 is lag +6
# differences
dq12 = q - q.shift(12); dw12 = w12 - w12.shift(12)
pd12 = prof(dq12, dw12, lags)
P("  12-month changes of both: ", "  ".join(f"{k:+d}:{v[0]:+.2f}" for k, v in pd12.items()))
pd12e = prof(dq12, dw12, [-12, 0, 6, 12, 18, 24], lambda t, tw: all(not (W0 <= x <= pd.Period("2022-06")) for x in (t, tw)))
P("  12-month changes, neither month (nor its base) in 2020-03..2022-06: ", "  ".join(f"{k:+d}:{v[0]:+.2f}(n{v[1]})" for k, v in pd12e.items()))
pd12p = prof(dq12, dw12, [-12, 0, 6, 12, 18, 24], prepan)
P("  12-month changes, pre-pandemic only: ", "  ".join(f"{k:+d}:{v[0]:+.2f}(n{v[1]})" for k, v in pd12p.items()))
for dn in (1, 3):
    dqn = q - q.shift(dn); dwn = w12 - w12.shift(dn)
    pp = prof(dqn, dwn, [-12, -6, 0, 3, 6, 9, 12, 18]); P(f"  {dn}-month changes of both: ", "  ".join(f"{k:+d}:{v[0]:+.2f}" for k, v in pp.items()))
# linear detrend
def detr(x):
    x = x.dropna(); t = np.arange(len(x)); c = np.polyfit(t, x.values, 1); return pd.Series(x.values - np.polyval(c, t), index=x.index)
qd, wd = detr(q.loc["2006-03":]), detr(w12)
pdd = prof(qd, wd, [-12, 0, 6, 12, 18]); P("  linearly detrended (from 2006-03 / 2007-03): ", "  ".join(f"{k:+d}:{v[0]:+.2f}" for k, v in pdd.items()))
# effective sample size
d0 = pd.concat([q, w12, w12.shift(-12)], axis=1).dropna(); d0.columns = ["q", "w", "wl"]
def ac(x, k): x = np.asarray(x) - np.mean(x); return float((x[k:] * x[:-k]).sum() / (x * x).sum())
for a, b in (("q", "w"), ("q", "wl")):
    ssum = 1 + 2 * sum(ac(d0[a], k) * ac(d0[b], k) for k in range(1, 61) )
    P(f"  effective n (Bartlett, 60 lags) for {a}~{b}: n={len(d0)} -> {len(d0) / ssum:.1f}; lag-1 autocorr {ac(d0[a], 1):.3f}, {ac(d0[b], 1):.3f}; lag-12 {ac(d0[a], 12):.2f}, {ac(d0[b], 12):.2f}")
# swings: crossings of own mean by 12-month centred averages
for nm, x in (("quits", q.loc["2006-03":].dropna()), ("wage growth", w12.dropna())):
    sm = x.rolling(12, center=True).mean().dropna(); sg = np.sign(sm - x.mean()); cr = [str(sm.index[i]) for i in range(1, len(sg)) if sg.iloc[i] != sg.iloc[i - 1] and sg.iloc[i] != 0]
    P(f"  {nm}: smoothed series crosses its mean {len(cr)} times: {cr}")
# moving-block bootstrap of r(+12) - r(0) on the common sample
rng = np.random.default_rng(7); n = len(d0); arr = d0.values
for B in (24, 36, 48):
    diffs = []
    for _ in range(4000):
        st = rng.integers(0, n - B + 1, int(np.ceil(n / B))); idx = np.concatenate([np.arange(x, x + B) for x in st])[:n]; a = arr[idx]
        diffs.append(np.corrcoef(a[:, 0], a[:, 2])[0, 1] - np.corrcoef(a[:, 0], a[:, 1])[0, 1])
    diffs = np.array(diffs); P(f"  block bootstrap (blocks of {B} months) of r(+12) - r(0): observed {np.corrcoef(arr[:,0],arr[:,2])[0,1]-np.corrcoef(arr[:,0],arr[:,1])[0,1]:+.3f}; 2.5%..97.5% {np.percentile(diffs, 2.5):+.3f}..{np.percentile(diffs, 97.5):+.3f}; share <= 0: {(diffs <= 0).mean():.3f}")
# same with the composition months removed (either month)
d1 = d0[[either(t, t + 12) and either(t, t) for t in d0.index]]
P(f"  common sample without pairs touching 2020-03..2021-06: n={len(d1)} same {np.corrcoef(d1.q, d1.w)[0,1]:+.3f}; +12 {np.corrcoef(d1.q, d1.wl)[0,1]:+.3f}")
P("  wage growth and quits around the composition swing:", [(str(k), round(float(w12[k]), 1), float(q[k])) for k in [pd.Period(x) for x in ("2020-02", "2020-04", "2020-06", "2020-12", "2021-04", "2021-06", "2021-12", "2022-03", "2022-12")]])
P(f"  peaks: quits max {q.max()} first {q.idxmax()} (months at max {[str(x) for x in q[q == q.max()].index]}); wage growth max since 2021 {w12.loc['2021-01':].max():.2f} at {w12.loc['2021-01':].idxmax()}; wage growth max overall {w12.max():.2f} at {w12.idxmax()}")
P(f"  troughs 2008-2013: quits min {q.loc['2008':'2013'].min()} first {q.loc['2008':'2013'].idxmin()}; wage growth min {w12.loc['2008':'2015'].min():.2f} at {w12.loc['2008':'2015'].idxmin()}")
# does unemployment/openings do the same job (third variable)?
vu_ = s.openings_level / s.unemployed_level
for nm, x in (("openings per unemployed", vu_), ("openings rate", o), ("unemployment rate", u)):
    pk = prof(x, w12, [-12, 0, 12]); P(f"  {nm} against wage growth: " + "  ".join(f"{k:+d}:{v[0]:+.2f}" for k, v in pk.items()))
P("  quits against openings per unemployed, same month: %+.3f" % r(q, vu_)[0])
# partial correlation of q_t with w_{t+12} given w_t
d0c = d0; rq_wl, rq_w, rw_wl = np.corrcoef(d0c.q, d0c.wl)[0, 1], np.corrcoef(d0c.q, d0c.w)[0, 1], np.corrcoef(d0c.w, d0c.wl)[0, 1]
P(f"  partial r(quits_t, wage_t+12 | wage_t) = {(rq_wl - rq_w * rw_wl) / np.sqrt((1 - rq_w**2) * (1 - rw_wl**2)):+.3f}; r(wage_t, wage_t+12) = {rw_wl:+.3f}")

P("=== G. Brier and the ledger")
L = pd.read_csv(sys.argv[3])
def br(df, col, out): return float(((df[col] - out) ** 2).mean())
def variant(L, x10, v8):
    out = L.outcome.astype(float).copy()
    out[L.label == "X10"] = x10; out[L.label == "V8"] = v8
    return out
P(f"  ledger rows {len(L)}; studies {L.groupby('study').size().to_dict()}; halves entered: {L[L.outcome.astype(float) == 0.5].label.tolist()}")
for nm, x10, v8 in [("as entered (X10 half, V8 half)", .5, .5), ("V8 failed (letter), X10 as entered half", .5, 0), ("both by the letter (X10 held, V8 failed)", 1, 0), ("both by the substance (X10 failed, V8 held)", 0, 1), ("V8 held (substance), X10 half", .5, 1)]:
    out = variant(L, x10, v8)
    P(f"  {nm}: all 46: mine {br(L, 'my_odds', out):.4f} forecasters {br(L, 'forecasters_median', out):.4f} diff {br(L, 'my_odds', out) - br(L, 'forecasters_median', out):+.4f}")
    for st in L.study.unique():
        k = L.study == st; P(f"      {st}: mine {br(L[k], 'my_odds', out[k]):.4f} forecasters {br(L[k], 'forecasters_median', out[k]):.4f} diff {br(L[k], 'my_odds', out[k]) - br(L[k], 'forecasters_median', out[k]):+.4f}")
V = L[L.study == "vacancy"].reset_index(drop=True); me = V.my_odds.values; fo = V.forecasters_median.values
for nm, y8 in (("half", .5), ("failed", 0.), ("held", 1.)):
    y = np.ones(12); y[7] = y8
    d = (me - y) ** 2 - (fo - y) ** 2
    rng = np.random.default_rng(0); bs = [d[rng.integers(0, 12, 12)].mean() for _ in range(10000)]
    P(f"  vacancy, V8 {nm}: mine {((me - y)**2).mean():.4f} theirs {((fo - y)**2).mean():.4f} diff {d.mean():+.4f} resampled 2.5..97.5 {np.percentile(bs, 2.5):+.3f}..{np.percentile(bs, 97.5):+.3f}; closer mine {int((np.abs(me-y) < np.abs(fo-y) - 1e-9).sum())} theirs {int((np.abs(fo-y) < np.abs(me-y) - 1e-9).sum())}; per-item (mine-theirs): {dict(zip(V.label, np.round(d, 3)))}")
    cl = np.clip(me, 0.50, 0.85); P(f"     my odds clipped to the old 0.50-0.85 range: {((cl - y)**2).mean():.4f}; my squared errors: {dict(zip(V.label, np.round((me - y)**2, 3)))}; share from V9+V1+V10: {(((me - y)**2)[[8, 0, 9]].sum() / ((me - y)**2).sum()):.2f}")
    for c in (0.9, 0.95, 0.96): P(f"     constant {c}: {((c - y)**2).mean():.4f}", end="")
    P()
# earlier studies' range
for st in L.study.unique():
    k = L.study == st; P(f"  {st}: my odds {L[k].my_odds.min()}..{L[k].my_odds.max()}; forecasters {L[k].forecasters_median.min()}..{L[k].forecasters_median.max()}")
