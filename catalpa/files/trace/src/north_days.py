# Each of the eighteen rises day by day at every gauge (and 2026), for reading by eye: the filtered level at
# 12:00 UTC less its mean over days -8 to -2, where day 0 is the day of San Diego's halfway hour.
# Run: ~/ipd/.venv/bin/python -I src/north_days.py > north_days.out
import sys, io, contextlib, importlib.util, datetime as dt
import numpy as np
def load(name):
    spec = importlib.util.spec_from_file_location(name, f'/home/agent1/trace/src/{name}.py'); m = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(m)
    return m
H = load('north_hourly'); N = load('north')
def table(tag, Y, h0, d0):
    print(f"\n{tag}; day 0 = {d0}; columns are days -3 to +8")
    for i, (sid, name, la, lo) in enumerate(H.ST[:len(Y)]):
        y = Y[i]
        if y is None: continue
        base = np.nanmean(y[h0 - 8 * 24: h0 - 24]); v = [y[h0 + d * 24 + 12] - base for d in range(-3, 9)]
        top = int(np.nanargmax(v)) - 3
        print(f"   {name:<14} " + " ".join(f"{x:+5.1f}" for x in v) + f"   highest on day {top:+d}")
for e in H.EV:
    k = e["k"]; h0 = (k // 24) * 24; t0 = dt.datetime(e["D"].year, e["D"].month, e["D"].day) - dt.timedelta(days=30)
    table(f"{e['D']} in the list" + (" (hurricane near)" if e["hur"] else ""), e["Y"], h0, (t0 + dt.timedelta(hours=h0)).date())
table("2026", H.Y26, 27 * 24, dt.date(2026, 9, 28))
rows = N.rows; sf_h = [r[3][0] for r in rows if r[5]]; sf_n = [r[3][0] for r in rows if not r[5]]; sf_n2 = [r[3][0] for r in rows if not r[5] and r[0] != dt.date(2004, 10, 16)]
print(f"\nSheet 7's line G5 again: San Francisco, largest daily sum of lags 0 to 4: with a hurricane near {np.mean(sf_h):+.1f} ({len(sf_h)}); without {np.mean(sf_n):+.1f} ({len(sf_n)}); without, leaving out 16 October 2004: {np.mean(sf_n2):+.1f} ({len(sf_n2)})")
tops = []
for e in H.EV:
    h0 = (e["k"] // 24) * 24; y = e["Y"][0]; base = np.nanmean(y[h0 - 8 * 24: h0 - 24]); v = [y[h0 + d * 24 + 12] - base for d in range(-3, 9)]; tops.append(int(np.nanargmax(v)) - 3)
print(f"San Diego's highest day of days -3 to +8, for the eighteen in the list's order: {tops}; day +4 or later in {sum(1 for t in tops if t >= 4)} of {len(tops)}")
