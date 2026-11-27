# After the sixth sheet was scored (exploration): San Diego with the barometer out, on the footing of baro_rises.py,
# through the weeks after Polo's rise, and the highest it had stood in any earlier August-October.
# Run: ~/ipd/.venv/bin/python -I src/baro_after.py > baro_after.out
import sys, io, contextlib, importlib.util, datetime as dt
import numpy as np
def load(name):
    spec = importlib.util.spec_from_file_location(name, f'/home/agent1/trace/src/{name}.py'); m = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(m)
    return m
BR = load('baro_rises'); ib = BR.ib; a = BR.a
def mean(series, d0, d1, need=0.8):
    v = [series[d0 + dt.timedelta(days=k)] for k in range((d1 - d0).days + 1) if (d0 + dt.timedelta(days=k)) in series]
    return float(np.mean(v)) if len(v) >= need * ((d1 - d0).days + 1) else None
print("SAN DIEGO 2026, cm above rule L: as measured / barometer out")
for label, d0, d1 in (("18-24 Sep (the sum's 'before')", dt.date(2026, 9, 18), dt.date(2026, 9, 24)), ("29 Sep-3 Oct (the sum's 'after')", dt.date(2026, 9, 29), dt.date(2026, 10, 3)), ("1-5 Oct", dt.date(2026, 10, 1), dt.date(2026, 10, 5)),
                      ("6-12 Oct", dt.date(2026, 10, 6), dt.date(2026, 10, 12)), ("13-19 Oct", dt.date(2026, 10, 13), dt.date(2026, 10, 19)), ("20-29 Oct", dt.date(2026, 10, 20), dt.date(2026, 10, 29))):
    print(f"  {label:<32} {mean(a, d0, d1):5.1f} / {mean(ib, d0, d1):5.1f}")
def highest(series, w, y0=1950, y1=2025):
    best = []
    for y in range(y0, y1 + 1):
        top = None; day = dt.date(y, 8, 1)
        while day + dt.timedelta(days=w - 1) <= dt.date(y, 10, 31):
            m = mean(series, day, day + dt.timedelta(days=w - 1))
            if m is not None and (top is None or m > top[0]): top = (m, day)
            day += dt.timedelta(days=1)
        if top: best.append(top)
    return sorted(best, reverse=True)[:5]
for w in (5, 7, 10):
    print(f"\nthe highest {w}-day means of August-October, 1950-2025 (one a year):")
    print("  as measured:   " + "; ".join(f"{m:.1f} from {d}" for m, d in highest(a, w)))
    print("  barometer out: " + "; ".join(f"{m:.1f} from {d}" for m, d in highest(ib, w)))
print("\nafter the two earlier rises that left San Diego about as high (barometer out):")
for d in (dt.date(1997, 10, 18), dt.date(2015, 10, 11), dt.date(2015, 9, 10), dt.date(1997, 9, 25)):
    base = mean(ib, d - dt.timedelta(days=10), d - dt.timedelta(days=4))
    print(f"  {d}: before {base:.1f}; days 1-5 {mean(ib, d + dt.timedelta(days=1), d + dt.timedelta(days=5)):.1f}; days 9-13 {mean(ib, d + dt.timedelta(days=9), d + dt.timedelta(days=13)):.1f}; days 16-22 {mean(ib, d + dt.timedelta(days=16), d + dt.timedelta(days=22)):.1f}")
d = dt.date(2026, 9, 28); base = mean(ib, d - dt.timedelta(days=10), d - dt.timedelta(days=4))
print(f"  {d}: before {base:.1f}; days 1-5 {mean(ib, d + dt.timedelta(days=1), d + dt.timedelta(days=5)):.1f}; days 9-13 {mean(ib, d + dt.timedelta(days=9), d + dt.timedelta(days=13)):.1f}; days 16-22 {mean(ib, d + dt.timedelta(days=16), d + dt.timedelta(days=22)):.1f}")
allr = sorted([e[1] for e in BR.events(ib, 0.0)], reverse=True); mp = BR.mp[0]
print(f"\nrises (barometer out, largest of each run, all sizes) larger than Polo's {mp:.1f}: {sum(1 for x in allr if x > mp)} since 1950")
