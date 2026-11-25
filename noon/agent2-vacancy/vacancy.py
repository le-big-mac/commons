"""Vacancies, unemployment, quits and pay in the United States since December 2000.   usage: python -I vacancy.py series.csv results.json
Rules are in expectations.md.  Details the sealed rules left open, settled after seeing the column names and the
number of months in each series (no values) and before computing:
 - the source is the Bureau of Labor Statistics' own API, not FRED, whose download timed out; the series are the same;
 - "all months" are the months in which both series of an expectation have a value;
 - job openings per unemployed person = the level of job openings over the number unemployed, both in thousands;
 - "the month of the highest rate" (or lowest) is the first month at which the extreme is reached;
 - a tie between two rates in a month does not count as "above";
 - a yearly mean is the mean over the months of that calendar year."""
import sys, csv, json
import numpy as np
SRC, OUT = sys.argv[1], sys.argv[2]
R = list(csv.DictReader(open(SRC)))
num = lambda s: float(s) if s not in ('', None, '-') else float('nan')
m = [r['month'] for r in R]
S = {k: np.array([num(r[k]) for r in R]) for k in R[0] if k != 'month'}
yr = np.array([int(x[:4]) for x in m])
fin = np.isfinite
res = {}
def say(tag, text, ok):
    res[tag] = bool(ok)
    print(f"{tag:4s} {text}  ->  {'held' if ok else 'failed'}")
def corr(a, b, sel=None):
    k = fin(a) & fin(b) if sel is None else fin(a) & fin(b) & sel
    return float(np.corrcoef(a[k], b[k])[0, 1]), int(k.sum())
jo, ur = S['openings_rate'], S['unemployment_rate']
print(f"{int(fin(jo).sum())} months of the JOLTS rates, {m[int(np.where(fin(jo))[0][0])]} to {m[int(np.where(fin(jo))[0][-1])]}; hourly earnings from {m[int(np.where(fin(S['hourly_earnings']))[0][0])]}")
r, n = corr(jo, ur); say('V1', f"job openings rate and unemployment rate, all {n} months: correlation {r:+.3f}", r <= -0.5)
r, n = corr(jo, ur, (yr >= 2010) & (yr <= 2019)); say('V2', f"the same, 2010 to 2019 ({n} months): {r:+.3f}", r <= -0.9)
band = (ur >= 3.4) & (ur <= 4.5) & fin(jo)
a = jo[band & (yr >= 2021) & (yr <= 2023)]; b = jo[band & (yr >= 2017) & (yr <= 2019)]
say('V3', f"months with unemployment from 3.4% to 4.5%: mean job openings rate {a.mean():.2f} in 2021-2023 ({len(a)} months), {b.mean():.2f} in 2017-2019 ({len(b)}); difference {a.mean() - b.mean():+.2f}", a.mean() - b.mean() >= 1.5)
ratio = S['openings_level'] / S['unemployed_level']
i = int(np.nanargmax(ratio)); say('V4', f"job openings per unemployed person: highest {ratio[i]:.2f} in {m[i]}", m[i].startswith('2022') and ratio[i] >= 1.9)
i = int(np.nanargmax(jo)); j = i + 24
say('V5', f"highest job openings rate {jo[i]:.1f} in {m[i]}; 24 months later ({m[j]}) {jo[j]:.1f}, a fall of {jo[i] - jo[j]:.1f}; unemployment {ur[i]:.1f} then {ur[j]:.1f}, a rise of {ur[j] - ur[i]:+.1f}",
    jo[i] - jo[j] >= 1.5 and ur[j] - ur[i] < 0.7)
ld = S['layoffs_rate']; i = int(np.nanargmax(ld)); say('V6', f"highest layoffs-and-discharges rate {ld[i]:.1f} in {m[i]}", m[i] == '2020-03')
q = S['quits_rate']; k = fin(q) & fin(ld); sh = float((q[k] > ld[k]).mean()); say('V7', f"quits rate above layoffs rate in {int((q[k] > ld[k]).sum())} of {int(k.sum())} months = {100 * sh:.1f}%", sh >= 0.8)
h, ts = S['hires_rate'], S['separations_rate']; k = fin(h) & fin(ts); sh = float((h[k] > ts[k]).mean())
say('V8', f"hires rate above total separations rate in {int((h[k] > ts[k]).sum())} of {int(k.sum())} months = {100 * sh:.1f}% (equal in {int((h[k] == ts[k]).sum())})", sh >= 0.7)
ahe = S['hourly_earnings']; wg = np.full(len(ahe), np.nan); wg[12:] = 100 * (ahe[12:] / ahe[:-12] - 1)
r0, n0 = corr(q, wg); say('V9', f"quits rate and wage growth in the same month: correlation {r0:+.3f} over {n0} months", r0 >= 0.5)
lead = np.full(len(wg), np.nan); lead[:-12] = wg[12:]
r12, n12 = corr(q, lead); say('V10', f"quits rate and wage growth twelve months later: {r12:+.3f} over {n12} months, against {r0:+.3f} in the same month", r12 > r0)
y9 = yr == 2009; i = int(np.where(y9)[0][0] + np.nanargmin(jo[y9])); j = int(np.where(y9)[0][0] + np.nanargmax(ur[y9]))
say('V11', f"in 2009 the job openings rate was lowest ({jo[i]:.1f}) first in {m[i]}; the unemployment rate highest ({ur[j]:.1f}) first in {m[j]}", i < j)
hp = {y: float(np.nanmean((h / jo)[yr == y])) for y in range(2001, 2026)}
say('V12', "hires per opening, yearly means: " + ", ".join(f"{y}: {hp[y]:.2f}" for y in range(2001, 2026)),
    all(hp[y] > 1 for y in range(2001, 2014)) and all(hp[y] < 1 for y in range(2018, 2025)))

print("afterwards, not registered:")
for lag in (0, 3, 6, 9, 12, 18, 24):
    ld_ = np.full(len(wg), np.nan); ld_[:len(wg) - lag] = wg[lag:]
    print(f"   quits rate against wage growth {lag:2d} months later: {corr(q, ld_)[0]:+.3f} ({corr(q, ld_)[1]} months)", end=';')
print()
pre = np.array([not ('2020-03' <= x <= '2021-06') for x in m])
print(f"   the same month, leaving out March 2020 to June 2021 (when the mix of who was at work swung pay): {corr(q, wg, pre)[0]:+.3f}; twelve months later, same months left out: {corr(q, lead, pre)[0]:+.3f}")
for a_, b_ in ((2001, 2009), (2010, 2019), (2020, 2026)):
    sel = (yr >= a_) & (yr <= b_)
    print(f"   openings and unemployment, {a_}-{b_}: correlation {corr(jo, ur, sel)[0]:+.3f} ({corr(jo, ur, sel)[1]} months)")
dj = np.diff(jo); du = np.diff(ur)
print(f"   month-to-month changes of the two rates: correlation {corr(dj, du)[0]:+.3f}")
json.dump(dict(verdicts=res, months=m, jo=[None if not fin(x) else float(x) for x in jo], ur=[float(x) for x in ur], q=[None if not fin(x) else float(x) for x in q],
               wg=[None if not fin(x) else float(x) for x in wg], hp=hp, ratio=[None if not fin(x) else float(x) for x in ratio]), open(OUT, 'w'))

# ---- afterwards: a control for each thing a summary sentence will rest on
# V8 failed by the letter because the published rates are rounded to one decimal (52 ties); on levels it would hold.
# V12 held by the letter for the same reason (the referee's finding).  Verdicts stay as sealed.
import os
print("afterwards: controls")
lv = os.path.join(os.path.dirname(SRC), 'levels.csv')
if os.path.exists(lv):
    L = {r['month']: (num(r['hires_level']), num(r['separations_level'])) for r in csv.DictReader(open(lv))}
    hl = np.array([L.get(x, (np.nan, np.nan))[0] for x in m]); sl = np.array([L.get(x, (np.nan, np.nan))[1] for x in m]); k2 = fin(hl) & fin(sl)
    print(f"   V8 with levels in place of rates rounded to one decimal: hires above separations in {int((hl[k2] > sl[k2]).sum())} of {int(k2.sum())} months = {100 * (hl[k2] > sl[k2]).mean():.1f}% (equal in {int((hl[k2] == sl[k2]).sum())})")
k = fin(h) & fin(ts)
print(f"   V8 with the rates: above {int((h[k] > ts[k]).sum())}, equal {int((h[k] == ts[k]).sum())}, below {int((h[k] < ts[k]).sum())}; counting an equal month as half: {100 * ((h[k] > ts[k]).sum() + 0.5 * (h[k] == ts[k]).sum()) / k.sum():.1f}%")
for a_, b_ in ((2007, 2019), (2021, 2026)):
    sel = (yr >= a_) & (yr <= b_)
    print(f"   quits and wage growth, {a_}-{b_}: same month {corr(q, wg, sel)[0]:+.3f} ({corr(q, wg, sel)[1]} months); twelve months later {corr(q, lead, sel)[0]:+.3f}")
dq = np.full(len(q), np.nan); dq[12:] = q[12:] - q[:-12]; dw = np.full(len(wg), np.nan); dw[12:] = wg[12:] - wg[:-12]
dlead = np.full(len(dw), np.nan); dlead[:-12] = dw[12:]
print(f"   changes over twelve months in place of levels: quits and wage growth in the same month {corr(dq, dw)[0]:+.3f}; wage growth twelve months later {corr(dq, dlead)[0]:+.3f}")
back = np.full(len(wg), np.nan); back[12:] = wg[:-12]
print(f"   the other way round: quits rate against wage growth twelve months EARLIER: {corr(q, back)[0]:+.3f}")
i9 = np.where(y9)[0]; lows = [m[x] for x in i9 if jo[x] == np.nanmin(jo[y9])]; highs = [m[x] for x in i9 if ur[x] == np.nanmax(ur[y9])]
print(f"   V11: months of 2009 at the lowest job openings rate: {lows}; at the highest unemployment rate: {highs}")
print(f"   V12: hires per opening in 2020: {hp[2020]:.4f}; in 2014: {hp[2014]:.3f}; in 2015: {hp[2015]:.3f}")
print(f"   V4: months with more than one opening per unemployed person: {int(np.nansum(ratio > 1))}, from {m[int(np.where(ratio > 1)[0][0])]} to {m[int(np.where(ratio > 1)[0][-1])]}; latest {ratio[int(np.where(fin(ratio))[0][-1])]:.2f} in {m[int(np.where(fin(ratio))[0][-1])]}")
last = int(np.where(fin(jo))[0][-1])
print(f"   latest month {m[last]}: job openings rate {jo[last]:.1f}, unemployment rate {ur[last]:.1f}; December 2019: {jo[m.index('2019-12')]:.1f} and {ur[m.index('2019-12')]:.1f}")
json.dump(dict(json.load(open(OUT)), verdicts=res), open(OUT, 'w'))

# ---- after the referee: its main points, recomputed here
print("after the referee:")
if os.path.exists(lv):
    Lv = {r['month']: num(r['hires_level']) for r in csv.DictReader(open(lv))}
    hlv = np.array([Lv.get(x, np.nan) for x in m])
    print(f"   V12 on levels (hires over job openings, yearly mean of monthly ratios): 2020 {np.nanmean((hlv / S['openings_level'])[yr == 2020]):.3f}; 2014 {np.nanmean((hlv / S['openings_level'])[yr == 2014]):.3f}; 2018 {np.nanmean((hlv / S['openings_level'])[yr == 2018]):.3f}")
pre20 = np.array([x <= '2019-12' for x in m]); post21 = yr >= 2021
print(f"   openings and unemployment: December 2000 to December 2019 {corr(jo, ur, pre20)[0]:+.3f}; 2021 on {corr(jo, ur, post21)[0]:+.3f}; all months without March 2020 to December 2021 {corr(jo, ur, np.array([not ('2020-03' <= x <= '2021-12') for x in m]))[0]:+.3f}")
ipk = int(np.nanargmax(jo))
print("   months after the peak of the openings rate: " + "; ".join(f"{k}: openings {jo[ipk + k] - jo[ipk]:+.1f}, unemployment {ur[ipk + k] - ur[ipk]:+.1f}" for k in (12, 18, 24, 30, 36, 42, 48, 54) if ipk + k < len(m) and fin(jo[ipk + k])))
back12 = np.full(len(wg), np.nan); back12[12:] = wg[:-12]
def trio(sel_q, sel_w):
    """same month, a year later, a year earlier, keeping a pair only if both its months pass"""
    out = []
    for arr, shift in ((wg, 0), (lead, 12), (back12, -12)):
        okw = np.zeros(len(m), bool)
        for i_ in range(len(m)):
            j_ = i_ + shift
            okw[i_] = 0 <= j_ < len(m) and sel_w[j_]
        out.append(corr(q, arr, sel_q & okw)[0])
    return out
allm = np.ones(len(m), bool)
prepan = np.array([x <= '2020-02' for x in m]); late = np.array([x >= '2021-07' for x in m]); clean = np.array([not ('2020-03' <= x <= '2021-06') for x in m])
for nm, sel in (("to February 2020", prepan), ("from July 2021", late), ("leaving out March 2020 to June 2021 on both sides", clean)):
    a_, b_, c_ = trio(sel, sel)
    print(f"   quits and pay growth, {nm}: same month {a_:+.2f}; a year later {b_:+.2f}; a year earlier {c_:+.2f}")
print(f"   the openings rate against pay growth: same month {corr(jo, wg)[0]:+.2f}; a year later {corr(jo, lead)[0]:+.2f}; a year earlier {corr(jo, back12)[0]:+.2f}")
print(f"   one month to the next: quits rate {corr(q[1:], q[:-1])[0]:+.2f}, pay growth {corr(wg[1:], wg[:-1])[0]:+.2f}")
