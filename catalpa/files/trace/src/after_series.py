# San Diego day by day, 1 September to 15 November, in 2026, 1997 and 2015: cm above the usual for the day (rule L),
# as the gauge measured it and with air pressure allowed for. Writes after_series.csv and prints five-day means.
# Run: ~/ipd/.venv/bin/python -I src/after_series.py > after_series.out
import sys, io, contextlib, importlib.util, csv, datetime as dt
import numpy as np
def load(name):
    spec = importlib.util.spec_from_file_location(name, f'/home/agent1/trace/src/{name}.py'); m = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(m)
    return m
F = load('baro_final'); A = {2026: F.a26, 1997: F.a, 2015: F.a}; I = {2026: F.ib26, 1997: F.ib, 2015: F.ib}
days = [(9, 1 + k) for k in range(30)] + [(10, 1 + k) for k in range(31)] + [(11, 1 + k) for k in range(15)]
rows = []
for m, d in days:
    r = [f"{m:02d}-{d:02d}"]
    for y in (2026, 1997, 2015):
        k = dt.date(y, m, d); r += [f"{A[y][k]:.1f}" if k in A[y] else "", f"{I[y][k]:.1f}" if k in I[y] else ""]
    rows.append(r)
with open('/home/agent1/trace/after_series.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(["day", "2026 as measured", "2026 pressure allowed for", "1997 as measured", "1997 pressure allowed for", "2015 as measured", "2015 pressure allowed for"]); w.writerows(rows)
print("SAN DIEGO, cm above the usual for the day; five-day means (as measured / air pressure allowed for)")
print(f"  {'five days from':<15} {'2026':>13} {'1997':>13} {'2015':>13}")
for s in range(0, len(rows), 5):
    blk = rows[s:s + 5]; out = []
    for j in (1, 3, 5):
        a = [float(r[j]) for r in blk if r[j]]; b = [float(r[j + 1]) for r in blk if r[j + 1]]
        out.append(f"{np.mean(a):5.1f} /{np.mean(b):5.1f}" if a and b else "      -      ")
    print(f"  {blk[0][0]:<15} " + " ".join(f"{o:>13}" for o in out))
for y, j in ((2026, 2), (1997, 4), (2015, 6)):
    v = [(float(r[j]), r[0]) for r in rows if r[j]]; print(f"  {y}, air pressure allowed for: days on file {len(v)}; highest day {max(v)[0]:.1f} on {max(v)[1]}; mean of 20 October to 15 November {np.mean([x for x, d in v if d >= '10-20']):.1f}; mean of 1 to 25 September {np.mean([x for x, d in v if d <= '09-25']):.1f}")
for y, j in ((2026, 2), (1997, 4), (2015, 6)):
    v = [(float(r[j]), r[0]) for r in rows if r[j]]; lo = min(v); late = [x for x, d in v if d >= '10-20']; early = [x for x, d in v if d <= '09-25']
    print(f"  {y} for the chart's description: lowest day {lo[0]:.1f} on {lo[1]}; 1 to 25 September between {min(early):.1f} and {max(early):.1f}; 20 October to 15 November between {min(late):.1f} and {max(late):.1f}; last five days {np.mean([x for x, d in v[-5:]]):.1f}; 1 to 5 October {np.mean([x for x, d in v if '10-01' <= d <= '10-05']):.1f}; 6 to 12 October {np.mean([x for x, d in v if '10-06' <= d <= '10-12']):.1f}")
