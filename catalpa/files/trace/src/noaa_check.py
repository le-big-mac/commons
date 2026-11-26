# Cross-check of the US gauges with NOAA's own monthly means (the Hawaii file for San Francisco has a gap in
# February-May 2024 and two months about 30 cm too high after it). Rule L applied to NOAA's monthly mean sea level.
# Run: ~/ipd/.venv/bin/python -I src/noaa_check.py > noaa_check.out
import csv, sys, io, contextlib, importlib.util
import numpy as np
spec = importlib.util.spec_from_file_location('trace', '/home/agent1/trace/src/trace.py')
T = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(T)
PAIRS = [("San Diego", "9410170"), ("La Jolla", "9410230"), ("San Francisco", "9414290"), ("Crescent City", "9419750"),
         ("South Beach", "9435380"), ("Neah Bay", "9443090"), ("Ketchikan", "9450460")]
print("RULE L ON NOAA'S OWN MONTHLY MEANS (cm), beside the same from the Hawaii files (in brackets)")
print(f"{'gauge':<14} {'months':>6} {'late summer 1997':>18} {'2015':>14} {'2026':>14} {'Oct 1997':>9} {'Oct 2015':>9} {'Oct 2026':>9}  highest month 1990-2025")
for name, sid in PAIRS:
    m = {}
    for r in csv.reader(open(f'/home/agent1/trace/data/coops/m{sid}.csv')):
        try: y, mo, v = int(r[0]), int(r[1]), float(r[5]) * 100
        except (ValueError, IndexError): continue
        m[(y, mo)] = v
    fit, n, tr = T.ruleL(m)
    an = lambda y, mo: m[(y, mo)] - fit(y, mo) if (y, mo) in m else None
    late = lambda y: None if an(y, 8) is None or an(y, 9) is None else (an(y, 8) + an(y, 9)) / 2
    top = max((an(y, mo), y, mo) for (y, mo) in m if 1990 <= y <= 2025)
    print(f"{name:<14} {n:6d} " + " ".join(f"{T.f(late(y))} ({T.f(T.late(name, y)).strip():>5})" for y in (1997, 2015, 2026))
          + " " + " ".join(f"{T.f(an(y, 10), 9)}" for y in (1997, 2015, 2026)) + f"  {top[0]:.1f} ({top[1]}-{top[2]:02d})")
