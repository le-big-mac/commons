# The rise at the end of September 2026, timed gauge by gauge from San Diego to Neah Bay.
# NOAA hourly heights, tide filtered out (Godin: running means of 24, 24, 25 hours). For each gauge:
# "before" = mean of 20-26 September, "after" = mean of 1-5 October; the arrival is the first hour after
# 26 September 00:00 UTC at which the filtered level passes halfway between the two and stays above for 12 hours.
# Not blind: I had seen daily values for San Diego, San Francisco and Crescent City (jump.out) before writing this.
# Run: ~/ipd/.venv/bin/python -I src/wave.py > wave.out
import csv, datetime as dt, sys
import numpy as np
sys.path.insert(0, '/home/agent1/trace/src')
from coastline import gc
ST = [("9410170", "San Diego", 32.714, -117.174), ("9410230", "La Jolla", 32.867, -117.257), ("9410660", "Los Angeles", 33.720, -118.272),
      ("9411340", "Santa Barbara", 34.405, -119.692), ("9412110", "Port San Luis", 35.169, -120.754), ("9413450", "Monterey", 36.605, -121.888),
      ("9414290", "San Francisco", 37.806, -122.466), ("9415020", "Point Reyes", 37.994, -122.976), ("9416841", "Arena Cove", 38.915, -123.711),
      ("9418767", "North Spit", 40.767, -124.217), ("9419750", "Crescent City", 41.745, -124.184), ("9431647", "Port Orford", 42.739, -124.498),
      ("9432780", "Charleston", 43.345, -124.322), ("9435380", "South Beach", 44.625, -124.045), ("9437540", "Garibaldi", 45.555, -123.919),
      ("9440910", "Toke Point", 46.708, -123.967), ("9443090", "Neah Bay", 48.371, -124.602)]
T0 = dt.datetime(2026, 9, 1); N = 24 * 61
# Godin's filter as one centred weight: running means of 24, 24 and 25 hours folded together (71 hours long, symmetric).
# (The first version of this script took the three means in turn with numpy's 'same' mode, which sets each 24-hour
# mean half an hour late: every clock time came out one hour late. A fresh reader found it. Delays were unaffected.)
K = np.convolve(np.convolve(np.ones(24), np.ones(24)), np.ones(25)); K = K / K.sum()
def series(fn, col=1, scale=100.0):
    x = np.full(N, np.nan)
    try: rows = csv.reader(open(fn))
    except FileNotFoundError: return x
    for r in rows:
        try: t = dt.datetime.strptime(r[0], '%Y-%m-%d %H:%M'); v = float(r[col])
        except (ValueError, IndexError): continue
        k = int((t - T0).total_seconds() // 3600)
        if 0 <= k < N: x[k] = v * scale
    return x
def godin(x):
    bad = np.convolve(np.isnan(x).astype(float), np.ones(len(K)), 'same') > 0
    y = np.convolve(np.where(np.isnan(x), 0, x), K, 'same'); y[bad] = np.nan
    y[:len(K) // 2] = np.nan; y[-(len(K) // 2):] = np.nan
    return y
def filt(sid, ib=False):
    x = series(f'/home/agent1/trace/data/coops/h{sid}.csv')
    if ib:   # take out the barometer: the sea stands 0.995 cm higher for each hPa the air pressure is lower
        p = series(f'/home/agent1/trace/data/coops/baro/b{sid}.csv', scale=1.0)
        if np.isnan(p).all(): return None
        # short gaps in the pressure record are filled by straight lines
        ok = ~np.isnan(p); p = np.interp(np.arange(N), np.arange(N)[ok], p[ok])
        x = x + 0.995 * (p - 1013.0)
    return godin(x)
def press(sid):
    p = series(f'/home/agent1/trace/data/coops/baro/b{sid}.csv', scale=1.0)
    return None if np.isnan(p).all() else godin(np.interp(np.arange(N), np.arange(N)[~np.isnan(p)], p[~np.isnan(p)]))
h = lambda d, hh=0: int((dt.datetime(2026, d[0], d[1], hh) - T0).total_seconds() // 3600)
def table(ib):
    km = 0.0; prev = None; rows = []
    for sid, name, lat, lon in ST:
        if prev: km += gc(prev, (lat, lon))
        prev = (lat, lon)
        y = filt(sid, ib)
        if y is None: rows.append((name, km, None, None, None, None)); continue
        B = np.nanmean(y[h((9, 20)):h((9, 27))]); A = np.nanmean(y[h((10, 1)):h((10, 6))]); half = B + (A - B) / 2
        arr = None
        if A - B >= 5:
            for k in range(h((9, 26)), h((10, 6))):
                seg = y[k:k + 12]
                if not np.isnan(seg).any() and (seg >= half).all(): arr = k; break
        pp = press(sid); dp = None if pp is None else np.nanmean(pp[h((10, 1)):h((10, 6))]) - np.nanmean(pp[h((9, 20)):h((9, 27))])
        rows.append((name, km, B, A, arr, dp))
    return rows
def show(rows, title):
    print(title)
    print(f"{'gauge':<14} {'km from San Diego':>17} {'rise cm':>8} {'air pressure, hPa':>18}  passed halfway (UTC)  hours after San Diego")
    t_sd = rows[0][4]
    for name, km_, B, A, arr, dp in rows:
        if B is None: print(f"{name:<14} {km_:17.0f}   no air pressure record"); continue
        when = (T0 + dt.timedelta(hours=arr)).strftime('%d %b %H:%M') if arr is not None else 'rose less than 5 cm'
        print(f"{name:<14} {km_:17.0f} {A - B:8.1f} {('%+.1f' % dp) if dp is not None else '-':>18}  {when:<20} " + (f"{arr - t_sd:6d}" if arr is not None else ""))
    ok = [(km_, arr - t_sd) for name, km_, B, A, arr, dp in rows if arr is not None]
    x = np.array([o[0] for o in ok]); t = np.array([o[1] for o in ok], float)
    for label, sel in (("all gauges with a rise of 5 cm or more", np.ones(len(x), bool)), ("San Diego to San Francisco", x <= 800), ("San Francisco northward", x >= 760)):
        if sel.sum() >= 3:
            (s, c), cov = np.polyfit(x[sel], t[sel], 1, cov=True) if sel.sum() > 3 else (np.polyfit(x[sel], t[sel], 1), np.full((2, 2), np.nan))
            res = t[sel] - (c + s * x[sel]); se = np.sqrt(cov[0, 0])
            lo, hi = 24 / (s + se), 24 / (s - se)
            print(f"straight line, {label} ({int(sel.sum())} gauges): {s * 1000:.1f} hours per 1000 km (give or take {se * 1000:.1f}) = {24 / s:.0f} km/day ({lo:.0f} to {hi:.0f}) = {1 / s / 3.6:.1f} m/s; scatter about the line {res.std():.1f} hours")
    print()
rows = table(False); rows_ib = table(True)
if __name__ == "__main__":
    show(rows, "AS MEASURED (tide filtered out, air pressure left in). 'air pressure' = its change between the two windows.")
    show(rows_ib, "WITH THE BAROMETER TAKEN OUT (0.995 cm for each hPa)")
    print("THE ARRIVALS COME IN GROUPS (as measured): hours after San Diego, and the gaps between neighbours")
    ok = [(r[0], r[1], r[4] - rows[0][4]) for r in rows if r[4] is not None]
    for (n1, k1, t1), (n2, k2, t2) in zip(ok[:-1], ok[1:]):
        print(f"  {n1:<14} -> {n2:<14} {k2 - k1:5.0f} km  {t2 - t1:+4d} hours")
