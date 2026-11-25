"""Referee follow-ups. Usage: python -I controls2.py series.csv levels.csv ledger.csv forecastdir"""
import sys, json
import numpy as np
import pandas as pd
s = pd.read_csv(sys.argv[1], dtype={"month": str}).set_index("month").apply(pd.to_numeric, errors="coerce")
lv = pd.read_csv(sys.argv[2], dtype={"month": str}).set_index("month").apply(pd.to_numeric, errors="coerce")
s.index = pd.PeriodIndex(s.index, freq="M"); lv.index = pd.PeriodIndex(lv.index, freq="M"); s = s.join(lv)
P = print
P("=== V12 on unrounded rates rebuilt from levels")
H, S_, O = s.hires_level, s.separations_level, s.openings_level
h, sp, orr = s.hires_rate, s.separations_rate, s.openings_rate
# feasible employment interval from the three published (rounded) rates: rate in [r-0.05, r+0.05)
lo = pd.concat([H / ((h + .05) / 100), S_ / ((sp + .05) / 100), O * (100 - (orr + .05)) / (orr + .05)], axis=1).max(axis=1)
hi = pd.concat([H / ((h - .05) / 100), S_ / ((sp - .05) / 100), O * (100 - (orr - .05)) / (orr - .05)], axis=1).min(axis=1)
ok = lo <= hi
P(f"  feasible interval non-empty in {int(ok.sum())} of {int(lo.notna().sum())} months (validates hires rate = H/E, openings rate = O/(E+O))")
# alternative (wrong) definition check: openings rate = O/E
lo2 = pd.concat([H / ((h + .05) / 100), S_ / ((sp + .05) / 100), O / ((orr + .05) / 100)], axis=1).max(axis=1)
hi2 = pd.concat([H / ((h - .05) / 100), S_ / ((sp - .05) / 100), O / ((orr - .05) / 100)], axis=1).min(axis=1)
P(f"  with openings rate taken as O/E instead: non-empty in {int((lo2 <= hi2).sum())} of {int(lo2.notna().sum())}")
for nm, E in (("E low", lo), ("E mid", (lo + hi) / 2), ("E high", hi)):
    hr_u = 100 * H / E; or_u = 100 * O / (E + O); ratio = hr_u / or_u
    rt = (hr_u.round(1) == h).mean(), (or_u.round(1) == orr).mean()
    y = ratio.groupby(ratio.index.year).mean(); rom = hr_u.groupby(hr_u.index.year).mean() / or_u.groupby(or_u.index.year).mean()
    P(f"  {nm}: rebuilt rates round to the published ones in {rt[0]:.3f}/{rt[1]:.3f} of months; 2020 mean of monthly ratios {y[2020]:.4f}; 2020 ratio of yearly mean rates {rom[2020]:.4f}; "
      f"other years closest to 1 (mean of ratios): {sorted([(int(k), round(float(v), 3)) for k, v in y.items() if 2001 <= k <= 2024], key=lambda t: abs(t[1] - 1))[:4]}")
    P(f"       verdict V12 on unrounded rates, mean of monthly ratios: {all(y[k] > 1 for k in range(2001, 2014)) and all(y[k] < 1 for k in range(2018, 2025))}; ratio of yearly means: {all(rom[k] > 1 for k in range(2001, 2014)) and all(rom[k] < 1 for k in range(2018, 2025))}")
E = (lo + hi) / 2
P("  2020 by month (H, O, published hires rate, openings rate, rebuilt):")
for k in s.loc["2020-01":"2020-12"].index:
    P(f"    {k}: H={H[k]:.0f} O={O[k]:.0f} E in [{lo[k]:.0f},{hi[k]:.0f}]  hires {h[k]} ~ {100*H[k]/E[k]:.3f}; openings {orr[k]} ~ {100*O[k]/(E[k]+O[k]):.3f}; ratio published {h[k]/orr[k]:.4f} rebuilt {(H[k]/O[k])*(1+O[k]/E[k]):.4f}")
# V8 on rebuilt rates
P(f"  V8 on rebuilt rates = on levels: {100*(H > S_)[H.notna()].mean():.1f}%")
# V7 can't be rebuilt (no quits/layoffs levels)
vu = (s.openings_level / s.unemployed_level)
P(f"  months with more than one opening per unemployed: {int((vu > 1).sum())}; since 2018-01: {int((vu.loc['2018-01':] > 1).sum())}; first {vu[vu > 1].index[0]}; latest value {vu.dropna().iloc[-1]:.3f} at {vu.dropna().index[-1]}")

P("=== ledger variants incl. V12")
L = pd.read_csv(sys.argv[3])
def sc(over):
    out = L.outcome.astype(float).copy()
    for k, v in over.items(): out[L.label == k] = v
    a, b = ((L.my_odds - out) ** 2), ((L.forecasters_median - out) ** 2)
    k = L.study == "vacancy"
    d = (a - b).values; rng = np.random.default_rng(0); bs = [d[rng.integers(0, len(d), len(d))].mean() for _ in range(10000)]
    dv = d[k.values]; bv = [dv[rng.integers(0, 12, 12)].mean() for _ in range(10000)]
    return f"vacancy mine {a[k].mean():.4f} theirs {b[k].mean():.4f} diff {a[k].mean()-b[k].mean():+.4f} [{np.percentile(bv,2.5):+.3f},{np.percentile(bv,97.5):+.3f}] | all 46 mine {a.mean():.4f} theirs {b.mean():.4f} diff {a.mean()-b.mean():+.4f} [{np.percentile(bs,2.5):+.3f},{np.percentile(bs,97.5):+.3f}]"
for nm, ov in [("as entered (V8 half, X10 half)", {}), ("V8 failed by the letter", {"V8": 0}), ("V8 held (levels)", {"V8": 1}), ("V8 half and V12 half (same rounding rule both ways)", {"V12": .5}),
               ("V8 held and V12 failed (unrounded rates throughout)", {"V8": 1, "V12": 0}), ("letter throughout (V8 failed, X10 held)", {"V8": 0, "X10": 1})]:
    P(f"  {nm}: {sc(ov)}")
F = np.array([[json.load(open(f"{sys.argv[4]}/f{k}.json"))[f"V{i}"] for i in range(1, 13)] for k in (1, 2, 3)])
P("  forecasters' pairwise correlations:", [round(float(np.corrcoef(F[a], F[b])[0, 1]), 3) for a, b in ((0, 1), (0, 2), (1, 2))], "; without V8 and V12:", [round(float(np.corrcoef(np.delete(F[a], [7, 11]), np.delete(F[b], [7, 11]))[0, 1]), 3) for a, b in ((0, 1), (0, 2), (1, 2))])
