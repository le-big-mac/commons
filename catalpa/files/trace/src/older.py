# The rises at San Diego after Kay (D = 8 September 2022) and Nora (D = 24 September 1997), timed gauge by gauge
# from San Diego to Humboldt Bay by the rule used for Polo (D = 28 September 2026), with the same offsets from D.
# Scores K1 and K2 of expectations-5.md. Hashed before the run.
# Run: ~/ipd/.venv/bin/python -I src/older.py > older.out
import sys, io, contextlib, importlib.util, csv, datetime as dt
import numpy as np
def load(name):
    spec = importlib.util.spec_from_file_location(name, f'/home/agent1/trace/src/{name}.py'); m = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(m)
    return m
W = load('wave')
from coastline import gc
ST = W.ST[:10]
def run(tag, year, D, t0):
    n = 24 * 50
    def series(sid):
        x = np.full(n, np.nan)
        fn = f'/home/agent1/trace/data/coops/old/h{sid}_{year}.csv' if year != 2026 else f'/home/agent1/trace/data/coops/h{sid}.csv'
        for r in csv.reader(open(fn)):
            try: t = dt.datetime.strptime(r[0], '%Y-%m-%d %H:%M'); v = float(r[1])
            except (ValueError, IndexError): continue
            k = int((t - t0).total_seconds() // 3600)
            if 0 <= k < n: x[k] = v * 100
        return W.godin(x)
    hh = lambda day: int((dt.datetime(day.year, day.month, day.day) - t0).total_seconds() // 3600)
    b0, b1 = hh(D - dt.timedelta(days=8)), hh(D - dt.timedelta(days=1)); a0, a1 = hh(D + dt.timedelta(days=3)), hh(D + dt.timedelta(days=8))
    s0, s1 = hh(D - dt.timedelta(days=2)), hh(D + dt.timedelta(days=8))
    km = 0.0; prev = None; rows = []
    for sid, name, lat, lon in ST:
        if prev: km += gc(prev, (lat, lon))
        prev = (lat, lon); y = series(sid)
        if np.isnan(y[b0:a1]).mean() > 0.2: rows.append((name, km, None, None)); continue
        B, A = np.nanmean(y[b0:b1]), np.nanmean(y[a0:a1]); arr = None
        if A - B >= 5:
            half = B + (A - B) / 2
            for k in range(s0, s1):
                seg = y[k:k + 12]
                if not np.isnan(seg).any() and (seg >= half).all(): arr = k; break
        rows.append((name, km, A - B, arr))
    print(f"{tag}: D = {D}; before = D-8 to D-2, after = D+3 to D+7")
    print(f"{'gauge':<14} {'km':>5} {'rise cm':>8}  passed halfway (UTC)  hours after San Diego")
    ref = rows[0][3]
    for name, km_, rise, arr in rows:
        if rise is None: print(f"{name:<14} {km_:5.0f}   no record"); continue
        when = (t0 + dt.timedelta(hours=arr)).strftime('%d %b %H:%M') if arr is not None else 'under 5 cm'
        print(f"{name:<14} {km_:5.0f} {rise:8.1f}  {when:<20} " + (f"{arr - ref:6d}" if arr is not None and ref is not None else ""))
    ok = [(km_, arr) for name, km_, rise, arr in rows if arr is not None]
    if len(ok) >= 3:
        x = np.array([o[0] for o in ok]); t = np.array([o[1] for o in ok], float); s, c = np.polyfit(x, t, 1)
        sp = 24 / s if s > 0 else None
        print(f"   {len(ok)} gauges with a rise of 5 cm or more; line: {s * 1000:.1f} hours per 1000 km" + (f" = {sp:.0f} km/day" if sp else " (not northward)") + f"; scatter {np.std(t - (c + s * x)):.1f} hours")
        return len(ok), sp
    print(f"   {len(ok)} gauges with a rise of 5 cm or more: no line"); return len(ok), None
r0 = run("POLO 2026 (for comparison; as in wave.out)", 2026, dt.date(2026, 9, 28), dt.datetime(2026, 9, 5)); print()
r1 = run("KAY 2022", 2022, dt.date(2022, 9, 8), dt.datetime(2022, 8, 16)); print()
r2 = run("NORA 1997", 1997, dt.date(1997, 9, 24), dt.datetime(1997, 9, 2)); print()
for tag, r in (("K1 (Kay 2022)", r1), ("K2 (Nora 1997)", r2)):
    held = r[0] >= 5 and r[1] is not None and 250 <= r[1] <= 700
    print(f"{tag}: {r[0]} gauges; " + (f"{r[1]:.0f} km/day" if r[1] else "no northward line") + " -> " + ("HELD" if held else "FAILED"))
