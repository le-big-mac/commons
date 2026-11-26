# November 2026 to date at San Diego and San Francisco from NOAA's six-minute water levels (verified to 31 October,
# preliminary after), tide filtered out (hourly means, then Godin's filter), minus rule L's line and waves.
# Scores the line N1 written in the journal before the fetch. Run: ~/ipd/.venv/bin/python -I src/november.py > november.out
import csv, sys, io, contextlib, importlib.util, datetime as dt
import numpy as np
spec = importlib.util.spec_from_file_location('curves', '/home/agent1/trace/src/curves.py')
C = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(C)
T0 = dt.datetime(2026, 10, 27); N = 24 * 31
for name, sid in (("San Diego", "9410170"), ("San Francisco", "9414290")):
    acc = {}; qual = {}
    for r in csv.reader(open(f'/home/agent1/trace/data/coops/nov/w{sid}.csv')):
        try: t = dt.datetime.strptime(r[0], '%Y-%m-%d %H:%M'); v = float(r[1])
        except (ValueError, IndexError): continue
        k = int((t - T0).total_seconds() // 3600); acc.setdefault(k, []).append(v * 100); qual[r[7].strip()] = qual.get(r[7].strip(), 0) + 1
    x = np.full(N, np.nan)
    for k, v in acc.items():
        if 0 <= k < N and len(v) >= 8: x[k] = np.mean(v)
    y = C.godin(x)
    days = {}
    for k in range(12, N, 24):
        if not np.isnan(y[k]):
            d = (T0 + dt.timedelta(hours=k)).date(); days[d] = y[k] - C.fitday(name, d)
    ver = C.coops(sid, name)
    both = [(days[d], ver[d] - C.fitday(name, d)) for d in days if d in ver]
    print(f"{name}: readings by quality flag {qual}; days with a filtered value: {min(days)} to {max(days)}")
    if both: print(f"  on the {len(both)} October days also in the hourly verified file, six-minute minus hourly: mean {np.mean([a - b for a, b in both]):+.2f} cm")
    nov = [v for d, v in days.items() if d.month == 11]
    print(f"  November, {len(nov)} days ({min(d for d in days if d.month == 11)} to {max(days)}): mean anomaly {np.mean(nov):.1f} cm; lowest day {min(nov):.1f}, highest {max(nov):.1f}")
    print("  every third day: " + ", ".join(f"{d.day} Nov {v:.0f}" for d, v in sorted(days.items()) if d.month == 11 and d.day % 3 == 1))
    if name == "San Diego":
        m = np.mean(nov); print(f"  N1: between 34 and 44 -> " + ("HELD" if 34 <= m <= 44 else "FAILED"))
