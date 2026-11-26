# The start of October 2026, day by day at the US gauges: NOAA's hourly heights with the tide filtered out
# (curves.coops), read at noon, minus rule L's line and waves, cm.
# Exploration. Run: ~/ipd/.venv/bin/python -I src/jump.py > jump.out
import sys, io, contextlib, importlib.util, datetime as dt
import numpy as np
spec = importlib.util.spec_from_file_location('curves', '/home/agent1/trace/src/curves.py')
C = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(C)
P = [("San Diego", "9410170"), ("La Jolla", "9410230"), ("San Francisco", "9414290"), ("Crescent City", "9419750"), ("South Beach", "9435380"), ("Neah Bay", "9443090")]
ser = {}
for name, sid in P:
    d = C.coops(sid, name)
    # tie to the Hawaii file (constant offset, see october.out) is below 0.2 cm and is left out
    ser[name] = {k: v - C.fitday(name, k) for k, v in d.items()}
# NOAA heights are in metres above station datum and the Hawaii files in mm above the same datum, so the fit applies directly
def run3(s, day): return s.get(day)
print("date        " + "".join(f"{n[:12]:>13}" for n, _ in P))
day = dt.date(2026, 9, 10)
while day <= dt.date(2026, 10, 30):
    print(f"{day}  " + "".join("            -" if run3(ser[n], day) is None else f"{run3(ser[n], day):13.1f}" for n, _ in P))
    day += dt.timedelta(days=1)
