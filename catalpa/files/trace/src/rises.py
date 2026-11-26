# Turned round: every quick rise of 10 cm or more at San Diego in August-October, 1950-2025, and whether a storm
# was then off the ocean side of Baja California. The definition is the fifth reading's (its zz_steps.py), written
# again here from its description and run on my own modules:
#   the composite's sum (mean of days +1..+5 less mean of days -10..-4) is 10 cm or more; of each run of such days
#   (runs at least 12 days apart) the day on which the sum is largest; a storm is "near" if it has a point at the
#   given strength, north of 20 N, west of Baja California's ocean-side line and within 600 km of it, on days -5 to +3.
# Also: 1982 day by day, and central California's wind and sea after the first rise of 2026.
# All of this was drawn up knowing what was being looked for. Run: ~/ipd/.venv/bin/python -I src/rises.py > rises.out
import sys, io, contextlib, importlib.util, datetime as dt
import numpy as np
def load(name):
    spec = importlib.util.spec_from_file_location(name, f'/home/agent1/trace/src/{name}.py'); m = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(m)
    return m
A4 = load('after4'); CO = A4.CO; PS = CO.PS; C = CO.C; T = CO.T; W = CO.W; B = A4.B
a = {k: v - C.fitday("San Diego", k) for k, v in T.daily["San Diego"].items() if k.year >= 1949}
TR = A4.tracks(1949, 2025)
def near(day, minkt):
    out = []
    for (code, name), pts in TR.items():
        best = None
        for t, lat, lon, kt in pts:
            if -5 <= (t.date() - day).days <= 3 and kt >= minkt and lat >= 20.0:
                d, west = PS.near(lat, lon)
                if west and d <= 600 and (best is None or kt > best[0]): best = (kt, d, t)
        if best: out.append(f"{name.title()} {best[0]} kt {best[1]:.0f} km ({best[2].strftime('%d %b')})")
    return out
events = []
for y in range(1950, 2026):
    vals = []; day = dt.date(y, 8, 1)
    while day <= dt.date(y, 10, 31):
        m = CO.measure(a, day)
        if m is not None and m[0] >= 10: vals.append((day, m[0], m[1], m[2]))
        day += dt.timedelta(days=1)
    runs = []
    for v in vals:
        if runs and (v[0] - runs[-1][-1][0]).days < 12: runs[-1].append(v)
        else: runs.append([v])
    for r in runs: events.append(max(r, key=lambda v: v[1]))
print(f"QUICK RISES OF 10 cm OR MORE AT SAN DIEGO, August-October, 1950-2025: {len(events)} in 76 autumns")
print("  day          rise   two weeks on   level before   hurricane near (64 kt)            |  any named storm near (34 kt)")
nh = ns = keep = 0
for d, r, af, base in events:
    h, s = near(d, 64), near(d, 34)
    nh += bool(h); ns += bool(s); keep += af > r / 2
    print(f"  {d}  {r:+5.1f}  {af:+6.1f}  {base:9.1f}        {('; '.join(h) or '-'):<34} |  {'; '.join(s) or '-'}")
tot = hh = ss = 0
for y in range(1950, 2026):
    day = dt.date(y, 8, 1)
    while day <= dt.date(y, 10, 31):
        tot += 1; hh += bool(near(day, 64)); ss += bool(near(day, 34)); day += dt.timedelta(days=1)
from math import comb
def tail(n, k, p): return sum(comb(n, j) * p**j * (1 - p)**(n - j) for j in range(k, n + 1))
n = len(events)
print(f"\n  with a hurricane near: {nh} of {n}; such a hurricane is near on {100 * hh / tot:.0f}% of all days of the season, so chance gives {n * hh / tot:.1f}; the chance of {nh} or more is {tail(n, nh, hh / tot):.5f}")
print(f"  with any named storm near: {ns} of {n}; near on {100 * ss / tot:.0f}% of days, chance gives {n * ss / tot:.1f}; the chance of {ns} or more is {tail(n, ns, ss / tot):.5f}")
print(f"  kept more than half of the rise two weeks on: {keep} of {n}")
print(f"  level before: lowest {min(e[3] for e in events):.1f}, highest {max(e[3] for e in events):.1f} cm; Polo, 28 September 2026: rise {CO.mp[0]:+.1f}, level before {CO.mp[2]:.1f}")
strong = {1957, 1965, 1972, 1982, 1987, 1991, 1997, 2015, 2023}
print("  (the track file is thin before the 1980s; 1957 and 1972 count for little)")

print("\n1982, San Diego day by day (cm above rule L), 18 September to 12 October, and the composite's sum for Paul's day (29 September):")
print("  " + ", ".join(f"{(dt.date(1982, 9, 18) + dt.timedelta(days=k)).strftime('%d %b')} {a[dt.date(1982, 9, 18) + dt.timedelta(days=k)]:.0f}" for k in range(25) if (dt.date(1982, 9, 18) + dt.timedelta(days=k)) in a))
m = CO.measure(a, dt.date(1982, 9, 29)); print(f"  Paul, 29 Sep 1982: rise {m[0]:+.1f}, two weeks on {m[1]:+.1f}, level before {m[2]:.1f}")
best = max((CO.measure(a, dt.date(1982, 9, 1) + dt.timedelta(days=k)) or (-99, 0, 0)) + (dt.date(1982, 9, 1) + dt.timedelta(days=k),) for k in range(61))
print(f"  the largest sum of September-October 1982: {best[0]:+.1f} on {best[3]}, two weeks on {best[1]:+.1f}")
for nm in ("PAUL", "OLIVIA"):
    pts = [p for (code, name), ps in TR.items() if name == nm and code.endswith('1982') for p in ps]
    q = [(p[0], PS.near(p[1], p[2])) for p in pts if p[3] >= 64 and p[1] >= 18]
    if q: print(f"  {nm.title()} 1982 at hurricane strength north of 18 N: " + "; ".join(f"{t.strftime('%d %b %H')}h {d:.0f} km {'west' if w else 'east'} of the line" for t, (d, w) in q[:8]))

print("\nAFTER THE FIRST RISE OF 2026: the wind off central California (mean of the five central buoys, m/s; negative = from the north-west)")
print("and the sea with the barometer out at three gauges, cm above its own level of 20-26 September")
hh_ = W.h
def span(x, a0, a1): return float(np.nanmean(x[hh_(a0):hh_(a1)]))
seas = {n_: W.filt(sid, ib=True) for n_, sid in (("Monterey", "9413450"), ("San Francisco", "9414290"), ("Point Reyes", "9415020"))}
for label, a0, a1 in (("20-26 Sep", (9, 20), (9, 27)), ("1-5 Oct", (10, 1), (10, 6)), ("6-9 Oct", (10, 6), (10, 10)), ("10-11 Oct", (10, 10), (10, 12)), ("13-19 Oct", (10, 13), (10, 20)), ("23-28 Oct", (10, 23), (10, 29))):
    print(f"  {label:<10} wind {span(B.AF['Central'], a0, a1):+5.1f}   sea: " + " / ".join(f"{span(seas[n_], a0, a1) - span(seas[n_], (9, 20), (9, 27)):.1f}" for n_ in seas))
