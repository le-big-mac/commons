# The quick rises at San Diego with the barometer taken out. Scores B1 to B5 of expectations-6.md. Hashed before the run.
# Pressure: NOAA's daily summaries for San Diego's airport (sea-level pressure, 1949-2025; data/gsod/), and for 2025 and
# 2026 the tide gauge's own barometer (hourly, daily means of 18 hours or more), shifted by its mean difference from
# the airport's over August-October 2024.
# Run: ~/ipd/.venv/bin/python -I src/baro_rises.py > baro_rises.out
import sys, io, contextlib, importlib.util, csv, os, datetime as dt
import numpy as np
from math import comb
def load(name):
    spec = importlib.util.spec_from_file_location(name, f'/home/agent1/trace/src/{name}.py'); m = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(m)
    return m
R = load('rises'); CO = R.CO; C = R.C; T = R.T
G = '/home/agent1/trace/data/gsod/'; BO = '/home/agent1/trace/data/coops/baro_old/'
slp = {}
for y in range(1949, 2026):
    fn = G + f'g{y}.csv'
    if not os.path.exists(fn): continue
    for r in csv.DictReader(open(fn)):
        v = r['SLP'].strip()
        if v not in ('9999.9', ''): slp[dt.date.fromisoformat(r['DATE'])] = float(v)
def gauge(y):
    acc = {}
    for r in csv.reader(open(BO + f'b9410170_{y}.csv')):
        try: t = dt.datetime.strptime(r[0], '%Y-%m-%d %H:%M'); v = float(r[1])
        except (ValueError, IndexError): continue
        acc.setdefault(t.date(), []).append(v)
    return {d: float(np.mean(v)) for d, v in acc.items() if len(v) >= 18}
g24 = gauge(2024)
both = [g24[d] - slp[d] for d in g24 if d in slp and d.month in (8, 9, 10)]
shift = float(np.mean(both))
print(f"the gauge's barometer less the airport's sea-level pressure, August-October 2024: mean {shift:+.2f} hPa over {len(both)} days (spread {np.std(both):.2f})")
for y in (2025, 2026):
    for d, v in gauge(y).items(): slp[d] = v - shift          # the gauge's own barometer for these two years
# the sea: 1949-2025 from the Hawaii file; 2026 carried through October with NOAA's hourly heights, as in composite.py
a = dict(R.a)
d26 = dict(T.daily["San Diego"]); d26.update({k: v for k, v in C.coops("9410170", "San Diego").items() if k > dt.date(2026, 9, 30)})
a.update({k: v - C.fitday("San Diego", k) for k, v in d26.items() if k.year == 2026})
ib = {d: v + 0.995 * (slp[d] - 1013.0) for d, v in a.items() if d in slp}
def events(series, floor, y0=1950, y1=2025):
    ev = []
    for y in range(y0, y1 + 1):
        vals = []; day = dt.date(y, 8, 1)
        while day <= dt.date(y, 10, 31):
            m = CO.measure(series, day)
            if m is not None and m[0] >= floor: vals.append((day, m[0], m[1], m[2]))
            day += dt.timedelta(days=1)
        runs = []
        for v in vals:
            if runs and (v[0] - runs[-1][-1][0]).days < 12: runs[-1].append(v)
            else: runs.append([v])
        for r in runs: ev.append(max(r, key=lambda v: v[1]))
    return ev
def tail(n, k, p): return sum(comb(n, j) * p**j * (1 - p)**(n - j) for j in range(k, n + 1))
tot = hh = 0
for y in range(1950, 2026):
    day = dt.date(y, 8, 1)
    while day <= dt.date(y, 10, 31):
        tot += 1; hh += bool(R.near(day, 64)); day += dt.timedelta(days=1)
rate = hh / tot
print(f"days of August-October 1950-2025 with a hurricane near: {100 * rate:.1f}%; days with pressure in those months: {sum(1 for d in slp if 1950 <= d.year <= 2025 and d.month in (8, 9, 10))} of {tot}")

print("\nTHE PRESENT LIST (pressure left in), each rise with the barometer taken out on the same days")
print("  day          rise   barometer out   barometer's part   two weeks on (out)   level before (out)   hurricane near")
part_h, part_n, still = [], [], 0
for d, r, af, base in R.events:
    m = CO.measure(ib, d); h = R.near(d, 64)
    if m is None: print(f"  {d}  {r:+5.1f}   no pressure"); continue
    (part_h if h else part_n).append(r - m[0]); still += bool(h) and m[0] >= 8
    print(f"  {d}  {r:+5.1f}  {m[0]:+10.1f}  {r - m[0]:+14.1f}  {m[1]:+16.1f}  {m[2]:18.1f}   {'; '.join(x.split(' (')[0] for x in h) or '-'}")
mp = CO.measure(ib, dt.date(2026, 9, 28)); mp0 = CO.measure(a, dt.date(2026, 9, 28))
print(f"  Polo, 2026-09-28: rise {mp0[0]:+.1f}, barometer out {mp[0]:+.1f}, barometer's part {mp0[0] - mp[0]:+.1f}, two weeks on (out) {mp[1]:+.1f}, level before (out) {mp[2]:.1f}")

for floor in (8, 10):
    ev = events(ib, floor); n = len(ev); k = sum(1 for e in ev if R.near(e[0], 64)); keep = sum(1 for e in ev if e[2] > e[1] / 2)
    print(f"\nTHE NEW LIST: quick rises of {floor} cm or more with the barometer out, August-October 1950-2025: {n}")
    print("  day          rise   two weeks on   level before   hurricane near")
    for d, r, af, base in ev: print(f"  {d}  {r:+5.1f}  {af:+6.1f}  {base:9.1f}        {'; '.join(x.split(' (')[0] for x in R.near(d, 64)) or '-'}")
    print(f"  with a hurricane near: {k} of {n} = {100 * k / n:.0f}%; the season's rate is {100 * rate:.0f}%, so chance gives {n * rate:.1f}; chance of {k} or more: {tail(n, k, rate):.6f}; kept more than half two weeks on: {keep}")
    if floor == 8: ev8 = ev; k8, n8 = k, n

print("\nTHE SEALED LINES")
print(f"B1: floor 8 cm, barometer out: {k8} of {n8} = {100 * k8 / n8:.0f}% with a hurricane near, against the season's {100 * rate:.0f}% -> " + ("HELD" if k8 / n8 >= 2 * rate else "FAILED"))
print(f"B2: of the ten hurricane rises of the present list, still 8 cm or more with the barometer out: {still} -> " + ("HELD" if still >= 6 else "FAILED"))
allr = sorted([e[1] for e in events(ib, 0.0)], reverse=True)
rank = 1 + sum(1 for x in allr if x > mp[0])
print(f"B3: Polo's rise with the barometer out, {mp[0]:+.1f} cm, ranks {rank} among all such rises since 1950 (the largest: " + ", ".join(f"{x:.1f}" for x in allr[:4]) + ") -> " + ("HELD" if rank <= 3 else "FAILED"))
hb = max(e[3] for e in ev8)
print(f"B4: level before Polo's rise, barometer out: {mp[2]:.1f} cm; the highest before any rise in the new list: {hb:.1f} -> " + ("HELD" if mp[2] > hb else "FAILED"))
print(f"B5: the barometer's part of the rise: with a hurricane {np.mean(part_h):+.1f} cm (n={len(part_h)}), without {np.mean(part_n):+.1f} cm (n={len(part_n)}); difference {np.mean(part_h) - np.mean(part_n):+.1f} -> " + ("HELD" if np.mean(part_h) - np.mean(part_n) >= 0.5 else "FAILED"))
