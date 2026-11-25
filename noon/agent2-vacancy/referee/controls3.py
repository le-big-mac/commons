"""Usage: python -I controls3.py series.csv"""
import sys, numpy as np, pandas as pd
s = pd.read_csv(sys.argv[1], dtype={"month": str}).set_index("month").apply(pd.to_numeric, errors="coerce")
s.index = pd.PeriodIndex(s.index, freq="M")
o, u = s.openings_rate, s.unemployment_rate
for k in (1, 3, 6, 12):
    d = pd.concat([o - o.shift(k), u - u.shift(k)], axis=1).dropna()
    pre = d[d.index <= pd.Period("2020-02")]
    print(f"{k}-month changes openings v unemployment: all {np.corrcoef(d.iloc[:,0], d.iloc[:,1])[0,1]:+.3f} (n={len(d)}); to 2020-02 {np.corrcoef(pre.iloc[:,0], pre.iloc[:,1])[0,1]:+.3f} (n={len(pre)})")
me = np.array([.60,.92,.95,.85,.90,.90,.92,.70,.40,.60,.88,.80]); fo = np.array([.88,.96,.95,.95,.96,.95,.93,.13,.86,.89,.93,.48])
for nm, y8 in (("V8 half", .5), ("V8 failed", 0.)):
    y = np.ones(12); y[7] = y8; d = (me - y)**2 - (fo - y)**2
    print(f"{nm}: gap {d.mean():+.4f}; without V9 {np.delete(d, 8).mean():+.4f}; without V9 and V12 {np.delete(d, [8, 11]).mean():+.4f}; without V12 {np.delete(d, 11).mean():+.4f}")
