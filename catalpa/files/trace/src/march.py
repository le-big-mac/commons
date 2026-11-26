# How the band filled from the south: for each coastal point, the first day (from 1 July) on which the smoothed
# satellite anomaly passed a level and stayed above it for 10 days; and the day it passed halfway between its
# July mean and its mean of 1-22 November. Exploration after the sealed lines; reads alt_smooth.npy.
import json, datetime as dt
import numpy as np
pts = json.load(open('/home/agent1/trace/data/alt/points.json')); sm = np.load('/home/agent1/trace/alt_smooth.npy')
D0 = dt.date(2026, 5, 1); ix = lambda d: (d - D0).days
def first(x, level, start):
    for k in range(start, len(x) - 10):
        seg = x[k:k + 10]
        if not np.isnan(seg).any() and (seg >= level).all(): return k
    return None
print("    km    lat  July mean  Nov mean   passed 20 cm   passed 30 cm   passed halfway (level)")
rows = []
for i, p in enumerate(pts):
    x = sm[i]; jul = np.nanmean(x[ix(dt.date(2026, 7, 1)):ix(dt.date(2026, 8, 1))]); nov = np.nanmean(x[ix(dt.date(2026, 11, 1)):ix(dt.date(2026, 11, 23))])
    half = (jul + nov) / 2
    k20, k30, kh = first(x, 20, ix(dt.date(2026, 7, 1))), first(x, 30, ix(dt.date(2026, 7, 1))), first(x, half, ix(dt.date(2026, 7, 1)))
    rows.append((p['km'], k20, k30, kh, nov - jul))
    fmt = lambda k: (D0 + dt.timedelta(days=k)).strftime('%d %b') if k is not None else '   -  '
    if p['km'] % 400 == 0: print(f"{p['km']:6d} {p['lat']:6.1f} {jul:9.1f} {nov:9.1f}   {fmt(k20):>12}   {fmt(k30):>12}   {fmt(kh):>12} ({half:.0f})")
def band(a, b, col):
    v = [r[col] for r in rows if a <= r[0] <= b and r[col] is not None]
    return (D0 + dt.timedelta(days=int(np.median(v)))).strftime('%d %b') if v else '-', len(v)
print("\nmedian day by stretch of coast (number of points):")
print("stretch                                   passed 20 cm     passed 30 cm     passed halfway")
for name, a, b in (("Peru and Ecuador (-1,200 to 400 km)", -1200, 400), ("Colombia to Costa Rica (500 to 2,000)", 500, 2000), ("El Salvador to Acapulco (2,100 to 4,000)", 2100, 4000),
                   ("Acapulco to Cabo San Lucas (4,100 to 5,400)", 4100, 5400), ("Baja California, Pacific side (5,500 to 6,600)", 5500, 6600),
                   ("San Diego to Point Conception (6,700 to 7,100)", 6700, 7100), ("central California (7,200 to 7,800)", 7200, 7800), ("north of Cape Mendocino (7,900 to 8,800)", 7900, 8800)):
    print(f"{name:<48} " + "   ".join(f"{band(a, b, c)[0]:>7} ({band(a, b, c)[1]:2d})" for c in (1, 2, 3)))
x = np.array([r[0] for r in rows if r[3] is not None and 0 <= r[0] <= 7700], float); t = np.array([r[3] for r in rows if r[3] is not None and 0 <= r[0] <= 7700], float)
s, c = np.polyfit(x, t, 1)
print(f"\nhalfway day against distance, points from 0 to 7,700 km ({len(x)}): {s * 1000:.1f} days per 1000 km" + (f" = {1 / s:.0f} km/day" if s > 0 else "") + f"; scatter {np.std(t - (c + s * x)):.0f} days")
