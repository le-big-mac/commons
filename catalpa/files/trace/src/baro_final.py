# After the seventh reading: 2026 measured as the others are (the largest day of its run), whether any earlier rise
# went on up afterwards, and the highest San Diego has stood in any month. Run: ~/ipd/.venv/bin/python -I src/baro_final.py > baro_final.out
import sys, io, contextlib, importlib.util, datetime as dt
import numpy as np
def load(name):
    spec = importlib.util.spec_from_file_location(name, f'/home/agent1/trace/src/{name}.py'); m = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(m)
    return m
BR = load('baro_rises'); ib = BR.ib; a = BR.a; CO = BR.CO; R = BR.R
def mean(series, d0, d1, need=0.8):
    v = [series[d0 + dt.timedelta(days=k)] for k in range((d1 - d0).days + 1) if (d0 + dt.timedelta(days=k)) in series]
    return float(np.mean(v)) if len(v) >= need * ((d1 - d0).days + 1) else None
print("A. 2026 BY THE SUM, day by day (rise as measured / barometer out / level before, barometer out)")
day = dt.date(2026, 9, 26)
while day <= dt.date(2026, 10, 10):
    m0, m1 = CO.measure(a, day), CO.measure(ib, day)
    if m0 and m1: print(f"   {day}  {m0[0]:+5.1f}  {m1[0]:+5.1f}  {m1[2]:5.1f}")
    day += dt.timedelta(days=1)
ev26 = BR.events(ib, 8, 2026, 2026); ev26m = R_ev = None
print("   by the list's rule (floor 8 cm, barometer out, largest day of the run): " + "; ".join(f"{d}: {r:+.1f} from {b:.1f}" for d, r, af, b in ev26))
ev30 = BR.events(ib, 8)
print(f"   the thirty earlier rises: largest {max(e[1] for e in ev30):+.1f} ({max(ev30, key=lambda e: e[1])[0]}); highest level before {max(e[3] for e in ev30):.1f} ({max(ev30, key=lambda e: e[3])[0]}); larger than 8.5: {sum(1 for e in ev30 if e[1] > 8.5)}; larger than 11.5: {sum(1 for e in ev30 if e[1] > 11.5)}")
# as measured, by the list's rule with floor 10
def events_m(y0, y1):
    ev = []
    for y in range(y0, y1 + 1):
        vals = []; day = dt.date(y, 8, 1)
        while day <= dt.date(y, 10, 31):
            m = CO.measure(a, day)
            if m is not None and m[0] >= 10: vals.append((day, m[0], m[1], m[2]))
            day += dt.timedelta(days=1)
        runs = []
        for v in vals:
            if runs and (v[0] - runs[-1][-1][0]).days < 12: runs[-1].append(v)
            else: runs.append([v])
        for r in runs: ev.append(max(r, key=lambda v: v[1]))
    return ev
print("   as measured, by the same rule with the floor at 10 cm, 2026: " + "; ".join(f"{d}: {r:+.1f} from {b:.1f}" for d, r, af, b in events_m(2026, 2026)) + f"; the eighteen: largest {max(e[1] for e in R.events):+.1f}, highest level before {max(e[3] for e in R.events):.1f}")

print("\nB. DID ANY EARLIER RISE GO ON UP? days 22-31 after the rise's day less days 1-5 after it (barometer out; the thirty of floor 8 cm)")
rows = []
for d, r, af, b in ev30:
    x1 = mean(ib, d + dt.timedelta(days=1), d + dt.timedelta(days=5)); x2 = mean(ib, d + dt.timedelta(days=22), d + dt.timedelta(days=31))
    if x1 is not None and x2 is not None: rows.append((x2 - x1, d))
rows.sort(reverse=True)
print(f"   {len(rows)} of the thirty have the days; stood higher at all: {sum(1 for r in rows if r[0] > 0)}; the most: " + ", ".join(f"{v:+.1f} ({d})" for v, d in rows[:3]) + f"; the middle one {np.median([r[0] for r in rows]):+.1f}")
for d in (dt.date(2026, 9, 28), dt.date(2026, 10, 4)):
    x1 = mean(ib, d + dt.timedelta(days=1), d + dt.timedelta(days=5)); x2 = mean(ib, d + dt.timedelta(days=22), d + dt.timedelta(days=31), need=0.3)
    n2 = sum(1 for k in range(22, 32) if (d + dt.timedelta(days=k)) in ib)
    print(f"   2026 from {d}: days 1-5 {x1:.1f}; days 22-31 {x2:.1f} ({n2} of the 10 days on file); difference {x2 - x1:+.1f}")
rows_m = []
for d, r, af, b in R.events:
    x1 = mean(a, d + dt.timedelta(days=1), d + dt.timedelta(days=5)); x2 = mean(a, d + dt.timedelta(days=22), d + dt.timedelta(days=31))
    if x1 is not None and x2 is not None: rows_m.append((x2 - x1, d))
rows_m.sort(reverse=True)
x1 = mean(a, dt.date(2026, 9, 29), dt.date(2026, 10, 3)); x2 = mean(a, dt.date(2026, 10, 20), dt.date(2026, 10, 29))
print(f"   as measured, the eighteen: stood higher at all: {sum(1 for r in rows_m if r[0] > 0)} of {len(rows_m)}; the most {rows_m[0][0]:+.1f} ({rows_m[0][1]}); 2026 from 28 September: {x2 - x1:+.1f}")

print("\nC. THE HIGHEST FIVE DAYS, as measured (cm above rule L), 1950-2025")
def highest(series, months, w=5, top=4):
    best = {}
    for d in sorted(series):
        if not (1950 <= d.year <= 2025) or d.month not in months: continue
        m = mean(series, d, d + dt.timedelta(days=w - 1))
        key = (d.year if d.month > 6 else d.year - 1)   # one a winter
        if m is not None and (key not in best or m > best[key][0]): best[key] = (m, d)
    return sorted(best.values(), reverse=True)[:top]
print("   August to October: " + "; ".join(f"{m:.1f} from {d}" for m, d in highest(a, (8, 9, 10))))
print("   any month: " + "; ".join(f"{m:.1f} from {d}" for m, d in highest(a, range(1, 13))))
print("   barometer out, August to October: " + "; ".join(f"{m:.1f} from {d}" for m, d in highest(ib, (8, 9, 10))))
for w, d0 in ((5, dt.date(2026, 10, 20)), (5, dt.date(2026, 10, 25)), (10, dt.date(2026, 10, 20))):
    print(f"   2026, {w} days from {d0}: as measured {mean(a, d0, d0 + dt.timedelta(days=w - 1)):.1f}; barometer out {mean(ib, d0, d0 + dt.timedelta(days=w - 1)):.1f}")
best5 = max((mean(a, dt.date(2026, 10, 1) + dt.timedelta(days=k), dt.date(2026, 10, 5) + dt.timedelta(days=k)) or -99, dt.date(2026, 10, 1) + dt.timedelta(days=k)) for k in range(25))
print(f"   2026, its highest five days of October as measured: {best5[0]:.1f} from {best5[1]}")

print("\nD. AFTER THE TWO EARLIER RISES THAT LEFT SAN DIEGO AS HIGH (barometer out), week by week")
for d in (dt.date(1997, 10, 18), dt.date(2015, 10, 11)):
    print(f"   {d}: " + ", ".join(f"days {k}-{k + 6} {mean(ib, d + dt.timedelta(days=k), d + dt.timedelta(days=k + 6)):.1f}" for k in (1, 8, 15, 22, 29, 36)))

# ---- after the eighth reading: a figure that does not depend on the day the rise is taken on
print("\nE. THREE TO FOUR WEEKS ON, ABOVE THE LEVEL BEFORE THE RISE (days 22-31 after the rise's day, less days 10 to 4 before it)")
A2 = load('after2')
six = A2.six("9410170")                                  # November 2026 from the six-minute file, tide filtered out
a26 = dict(a); a26.update({k: v - BR.C.fitday("San Diego", k) for k, v in six.items() if k > max(d for d in a if d.year == 2026)})
ib26 = dict(ib); ib26.update({d: v + 0.995 * (BR.slp[d] - 1013.0) for d, v in a26.items() if d.year == 2026 and d in BR.slp and d not in ib})
print(f"   2026 carried on: as measured to {max(d for d in a26 if d.year == 2026)}, barometer out to {max(d for d in ib26 if d.year == 2026)}")
def later(series, d): 
    x0 = mean(series, d - dt.timedelta(days=10), d - dt.timedelta(days=4)); x2 = mean(series, d + dt.timedelta(days=22), d + dt.timedelta(days=31))
    return None if x0 is None or x2 is None else x2 - x0
rows = sorted(((later(ib, d), d) for d, r, af, b in ev30 if later(ib, d) is not None), reverse=True)
print(f"   barometer out, the thirty: {len(rows)} have the days; the most " + ", ".join(f"{v:+.1f} ({d})" for v, d in rows[:3]) + f"; the middle one {np.median([r[0] for r in rows]):+.1f}")
print(f"   2026: from its first day (28 September) {later(ib26, dt.date(2026, 9, 28)):+.1f}; from the largest day of its run (4 October) {later(ib26, dt.date(2026, 10, 4)):+.1f}")
rows_m = sorted(((later(a, d), d) for d, r, af, b in R.events if later(a, d) is not None), reverse=True)
print(f"   as measured, the eighteen: {len(rows_m)} have the days; the most " + ", ".join(f"{v:+.1f} ({d})" for v, d in rows_m[:3]))
print(f"   2026 as measured: from 28 September {later(a26, dt.date(2026, 9, 28)):+.1f}; from the largest day of its run (5 October) {later(a26, dt.date(2026, 10, 5)):+.1f}")
x1 = mean(ib26, dt.date(2026, 10, 5), dt.date(2026, 10, 9)); x2 = mean(ib26, dt.date(2026, 10, 26), dt.date(2026, 11, 4))
print(f"   days 22-31 less days 1-5 for 2026 from 4 October, with all ten days: {x2 - x1:+.1f} ({x1:.1f} to {x2:.1f}); the most after any of the thirty: {rows and max((mean(ib, d + dt.timedelta(days=22), d + dt.timedelta(days=31)) - mean(ib, d + dt.timedelta(days=1), d + dt.timedelta(days=5))) for d, r, af, b in ev30 if mean(ib, d + dt.timedelta(days=22), d + dt.timedelta(days=31)) is not None and mean(ib, d + dt.timedelta(days=1), d + dt.timedelta(days=5)) is not None):+.1f}")
print("   2026 week by week from 29 September, barometer out: " + ", ".join(f"{mean(ib26, dt.date(2026, 9, 29) + dt.timedelta(days=7 * k), dt.date(2026, 10, 5) + dt.timedelta(days=7 * k)):.1f}" for k in range(7) if mean(ib26, dt.date(2026, 9, 29) + dt.timedelta(days=7 * k), dt.date(2026, 10, 5) + dt.timedelta(days=7 * k)) is not None))
print("   by half of the record, floor 8 cm, barometer out: " + "; ".join(f"{y0}-{y1}: {sum(1 for e in ev30 if y0 <= e[0].year <= y1 and R.near(e[0], 64))} of {sum(1 for e in ev30 if y0 <= e[0].year <= y1)} with a hurricane near" for y0, y1 in ((1950, 1989), (1990, 2025))))
def rate_of(y0, y1):
    t = h = 0
    for y in range(y0, y1 + 1):
        day = dt.date(y, 8, 1)
        while day <= dt.date(y, 10, 31):
            t += 1; h += bool(R.near(day, 64)); day += dt.timedelta(days=1)
    return h / t
for y0, y1 in ((1950, 1989), (1990, 2025)):
    n = sum(1 for e in ev30 if y0 <= e[0].year <= y1); k = sum(1 for e in ev30 if y0 <= e[0].year <= y1 and R.near(e[0], 64))
    own = rate_of(y0, y1)
    print(f"   {y0}-{y1}: {k} of {n}; that half's own rate of days with a hurricane near is {100 * own:.1f}%, so chance gives {n * own:.1f}; by the whole record's rate {100 * BR.rate:.1f}% chance gives {n * BR.rate:.1f}; chance of {k} or more at the half's own rate: {BR.tail(n, k, own):.5f}")
