"""Blind recomputation of V1..V12 (referee). Usage: python -I blind.py series.csv levels.csv"""
import sys
import numpy as np
import pandas as pd

s = pd.read_csv(sys.argv[1], dtype={"month": str}).set_index("month")
lv = pd.read_csv(sys.argv[2], dtype={"month": str}).set_index("month")
s = s.apply(pd.to_numeric, errors="coerce")
lv = lv.apply(pd.to_numeric, errors="coerce")
months = list(s.index)
# sanity: consecutive months
pi = pd.PeriodIndex(s.index, freq="M")
assert all((pi[i + 1] - pi[i]).n == 1 for i in range(len(pi) - 1)), "gap in months"
s.index = pi
lv.index = pd.PeriodIndex(lv.index, freq="M")
out = []
def P(*a):
    line = " ".join(str(x) for x in a)
    out.append(line)
    print(line)

def r(a, b):
    d = pd.concat([a, b], axis=1).dropna()
    return float(np.corrcoef(d.iloc[:, 0], d.iloc[:, 1])[0, 1]), len(d)

P("rows", len(s), "first", s.index[0], "last", s.index[-1])
for c in s.columns:
    v = s[c].dropna()
    P("  col", c, "n", len(v), "from", v.index[0], "to", v.index[-1], "gaps_inside", int(s[c].loc[v.index[0]:v.index[-1]].isna().sum()))

o, u = s.openings_rate, s.unemployment_rate
# V1
r1, n1 = r(o, u)
P(f"V1 corr(openings_rate, unemp_rate) all months = {r1:.4f} n={n1} -> held={r1 <= -0.5}")
# V2
sl = slice("2010-01", "2019-12")
r2, n2 = r(o.loc[sl], u.loc[sl])
P(f"V2 corr 2010-01..2019-12 = {r2:.4f} n={n2} -> held={r2 <= -0.9}")
# V3
def band_mean(y0, y1, lo=3.4, hi=4.5):
    d = s.loc[f"{y0}-01":f"{y1}-12"]
    d = d[(d.unemployment_rate >= lo) & (d.unemployment_rate <= hi)].dropna(subset=["openings_rate"])
    return d.openings_rate.mean(), len(d)
a, na = band_mean(2021, 2023)
b, nb = band_mean(2017, 2019)
P(f"V3 mean openings rate, u in [3.4,4.5]: 2021-23 = {a:.4f} (n={na}); 2017-19 = {b:.4f} (n={nb}); diff = {a-b:.4f} -> held={a-b >= 1.5}")
# V4
vu = (s.openings_level / s.unemployed_level).dropna()
pk = vu.idxmax()
P(f"V4 openings per unemployed peak = {vu.max():.4f} at {pk} (first max) -> held={(pk.year == 2022) and vu.max() >= 1.9}")
# V5
od = o.dropna()
m0 = od.idxmax()
m1 = m0 + 24
do = o[m1] - o[m0]
du = u[m1] - u[m0]
P(f"V5 openings-rate max {od.max()} first at {m0} (months at max: {[str(x) for x in od[od == od.max()].index]}); +24 = {m1}: openings {o[m0]} -> {o[m1]} (change {do:.2f}); unemp {u[m0]} -> {u[m1]} (change {du:.2f}) -> held={(do <= -1.5) and (du < 0.7)}")
# V6
l = s.layoffs_rate.dropna()
P(f"V6 max layoffs rate = {l.max()} first at {l.idxmax()} (months at max: {[str(x) for x in l[l == l.max()].index]}) -> held={str(l.idxmax()) == '2020-03'}")
P("   top 5 layoffs months:", [(str(k), v) for k, v in l.sort_values(ascending=False).head(5).items()])
# V7
d = s[["quits_rate", "layoffs_rate"]].dropna()
ab = (d.quits_rate > d.layoffs_rate).sum(); ti = (d.quits_rate == d.layoffs_rate).sum()
P(f"V7 quits > layoffs in {ab}/{len(d)} = {100*ab/len(d):.2f}% (ties {ti}) -> held={ab/len(d) >= 0.8}")
# V8
d = s[["hires_rate", "separations_rate"]].dropna()
ab = (d.hires_rate > d.separations_rate).sum(); ti = (d.hires_rate == d.separations_rate).sum(); be = (d.hires_rate < d.separations_rate).sum()
P(f"V8 hires > separations (rates) in {ab}/{len(d)} = {100*ab/len(d):.2f}% (ties {ti}, below {be}) -> held={ab/len(d) >= 0.7}")
P(f"   ties as above: {100*(ab+ti)/len(d):.2f}%; ties excluded from denominator: {100*ab/(ab+be):.2f}%; ties as half: {100*(ab+0.5*ti)/len(d):.2f}%")
dl = lv[["hires_level", "separations_level"]].dropna()
abl = (dl.hires_level > dl.separations_level).sum(); til = (dl.hires_level == dl.separations_level).sum()
P(f"   levels: hires > separations in {abl}/{len(dl)} = {100*abl/len(dl):.2f}% (ties {til})")
# V9
w = 100 * (s.hourly_earnings / s.hourly_earnings.shift(12) - 1)
q = s.quits_rate
r9, n9 = r(q, w)
P(f"V9 corr(quits, wage growth same month) = {r9:.4f} n={n9} -> held={r9 >= 0.5}")
# V10
wl = w.shift(-12)  # wage growth twelve months later aligned to quits month
r10, n10 = r(q, wl)
we = w.shift(12)
r10b, n10b = r(q, we)
P(f"V10 corr(quits_t, wage growth_t+12) = {r10:.4f} n={n10}; same month {r9:.4f} n={n9}; wage growth_t-12 {r10b:.4f} n={n10b} -> held={r10 > r9}")
# same-sample comparison
d = pd.concat([q, w, wl], axis=1).dropna(); d.columns = ["q", "w", "wl"]
P(f"    on the common sample (n={len(d)}): same {np.corrcoef(d.q, d.w)[0,1]:.4f}, +12 {np.corrcoef(d.q, d.wl)[0,1]:.4f}")
# V11
o9 = o.loc["2009-01":"2009-12"]; u9 = u.loc["2009-01":"2009-12"]
P(f"V11 2009: openings min {o9.min()} first {o9.idxmin()} last {o9[o9 == o9.min()].index[-1]}; unemp max {u9.max()} first {u9.idxmax()} last {u9[u9 == u9.max()].index[-1]} -> held={o9.idxmin() < u9.idxmax()}")
om = o.loc["2007-01":"2012-12"]; um = u.loc["2007-01":"2012-12"]
P(f"    2007-2012: openings min {om.min()} months {[str(x) for x in om[om == om.min()].index]}; unemp max {um.max()} months {[str(x) for x in um[um == um.max()].index]}")
# V12
ratio = (s.hires_rate / s.openings_rate).dropna()
ym = ratio.groupby(ratio.index.year).mean()
rm = (s.hires_rate.groupby(s.index.year).mean() / s.openings_rate.groupby(s.index.year).mean())
cnt = ratio.groupby(ratio.index.year).count()
ok1 = all(ym[y] > 1 for y in range(2001, 2014)); ok2 = all(ym[y] < 1 for y in range(2018, 2025))
P(f"V12 yearly mean of hires_rate/openings_rate (mean of monthly ratios): above 1 in all 2001-2013 = {ok1}; below 1 in all 2018-2024 = {ok2} -> held={ok1 and ok2}")
for y in ym.index:
    P(f"    {y} n={cnt[y]} mean-of-ratios {ym[y]:.4f} ratio-of-means {rm[y]:.4f}")
open(sys.argv[3], "w").write("\n".join(out) + "\n")
