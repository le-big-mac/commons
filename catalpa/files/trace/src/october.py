# October 2026 at the US gauges, by rule L, from NOAA CO-OPS hourly heights (verified, to 31 Oct 2026),
# tied to the Hawaii files by the mean difference of the monthly means of January to September 2026.
# Exploration after the sealed lines were scored. Run: ~/ipd/.venv/bin/python -I src/october.py > october.out
import csv, sys, datetime as dt
import numpy as np
sys.path.insert(0, '/home/agent1/trace/src')
import importlib.util, io, contextlib
spec = importlib.util.spec_from_file_location('trace', '/home/agent1/trace/src/trace.py')
T = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(T)
PAIRS = [("San Diego", "9410170"), ("La Jolla", "9410230"), ("San Francisco", "9414290"), ("Crescent City", "9419750"),
         ("South Beach", "9435380"), ("Neah Bay", "9443090"), ("Ketchikan", "9450460")]
print("OCTOBER 2026 AT THE US GAUGES, rule L (cm). 'tie' = CO-OPS minus Hawaii monthly means, Jan-Sep 2026: mean and spread")
print(f"{'gauge':<14} {'tie mean':>9} {'tie sd':>7} {'Sep (Hawaii)':>12} {'Sep (CO-OPS)':>12} {'Oct 2026':>9}   Oct 1982 / 1997 / 2015")
res = {}
for name, sid in PAIRS:
    acc = {}
    for r in csv.reader(open(f'/home/agent1/trace/data/coops/h{sid}.csv')):
        try: t = dt.datetime.strptime(r[0], '%Y-%m-%d %H:%M'); v = float(r[1])
        except (ValueError, IndexError): continue
        acc.setdefault((t.year, t.month, t.day), []).append(v * 100)
    days = {k: np.mean(v) for k, v in acc.items() if len(v) >= 20}
    mm = {}
    for (y, m, d), v in days.items(): mm.setdefault((y, m), []).append(v)
    mm = {k: float(np.mean(v)) for k, v in mm.items() if len(v) >= 20}
    diffs = [mm[(2026, m)] - T.mon[name][(2026, m)] for m in range(1, 10) if (2026, m) in mm and (2026, m) in T.mon[name]]
    tie, sd = float(np.mean(diffs)), float(np.std(diffs))
    sepc = mm[(2026, 9)] - tie - T.fit[name](2026, 9)
    octv = mm[(2026, 10)] - tie - T.fit[name](2026, 10) if (2026, 10) in mm else None
    res[name] = octv
    old = " / ".join(T.f(T.anom(name, y, 10)) for y in (1982, 1997, 2015))
    print(f"{name:<14} {tie:9.2f} {sd:7.2f} {T.anom(name, 2026, 9):12.1f} {sepc:12.1f} {T.f(octv, 9)}   {old}")
print()
for name in ("San Diego", "San Francisco"):
    best = max((T.anom(name, y, m), y, m) for y in range(1990, 2026) for m in range(1, 13) if T.anom(name, y, m) is not None)
    print(f"{name}: highest monthly anomaly of 1990-2025 by rule L: {best[0]:.1f} cm in {best[1]}-{best[2]:02d}; October 2026: {res[name]:.1f}")
