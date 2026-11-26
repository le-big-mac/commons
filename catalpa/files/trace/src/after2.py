# Things a second reading of the page raised, recomputed here before they were put on the page (26 Nov, 17:55 on).
# Run: ~/ipd/.venv/bin/python -I src/after2.py > after2.out
import sys, io, contextlib, importlib.util, csv, json, datetime as dt
import numpy as np
def load(name):
    spec = importlib.util.spec_from_file_location(name, f'/home/agent1/trace/src/{name}.py'); m = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(m)
    return m
W = load('wave'); C = load('curves'); T = C.T
print("A. THE DIP IN AIR PRESSURE, 28 September to 2 October 2026: when the filtered pressure was lowest at each gauge,")
print("   and when the sea (barometer taken out) passed halfway, in hours after the pressure low at the same gauge")
print(f"{'gauge':<14} {'km':>5}  pressure lowest (UTC)  hours after San Diego  depth hPa   sea halfway, hours after the local low")
rows = []
for (sid, name, lat, lon), r, rb in zip(W.ST, W.rows, W.rows_ib):
    p = W.press(sid)
    if p is None: continue
    a, b = W.h((9, 28)), W.h((10, 2), 12)
    k = a + int(np.nanargmin(p[a:b])); depth = p[k] - np.nanmean(p[W.h((9, 20)):W.h((9, 27))])
    rows.append((name, r[1], k, depth, rb[4]))
k0 = rows[0][2]
for name, km, k, depth, arr in rows:
    print(f"{name:<14} {km:5.0f}  {(W.T0 + dt.timedelta(hours=k)).strftime('%d %b %H:%M'):<21} {k - k0:10d} {depth:14.1f}   " + (f"{arr - k:+d}" if arr is not None else "-"))
for label, lim in (("San Diego to Arena Cove", 940), ("San Diego to Crescent City", 1260)):
    x = np.array([r[1] for r in rows if r[1] <= lim], float); t = np.array([r[2] - k0 for r in rows if r[1] <= lim], float)
    s, c = np.polyfit(x, t, 1); print(f"   line through the pressure lows, {label} ({len(x)} gauges): {s * 1000:.0f} hours per 1000 km = {24 / s:.0f} km/day")

print("\nB. SAN DIEGO WHEN THE TROPICS STOOD AT 32 TO 37 cm, the same month and the month after (rule L, cm)")
P = load('pairs')
for y, m, trop in ((1997, 11, P.trop(1997, 11)), (1997, 12, P.trop(1997, 12)), (2026, 9, P.trop(2026, 9)), (2026, 10, 37.1)):
    ny, nm = (y, m + 1) if m < 12 else (y + 1, 1)
    nxt = 32.3 if (ny, nm) == (2026, 11) else P.g("San Diego", ny, nm)
    print(f"   tropics {y}-{m:02d} {trop:.1f}{' (satellite)' if (y, m) == (2026, 10) else ''}: San Diego the same month {P.g('San Diego', y, m):.1f}, the month after {nxt:.1f}")
print("   San Diego's highest month in each earlier event: 1982-83 19.7, 1997-98 16.9, 2015-16 17.5 (facts.out); the tropics' highest: 29.9, 36.1, 19.3")

print("\nC. THE HIGHEST DAYS BY RULE L (daily value minus the fit for that day), cm")
for name in ("La Libertad", "Santa Cruz", "Baltra"):
    d = {k: v - C.fitday(name, k) for k, v in T.daily[name].items() if dt.date(1997, 11, 15) <= k <= dt.date(1997, 12, 31)}
    k = max(d, key=d.get); print(f"   {name}: highest day of 15 Nov - 31 Dec 1997: {d[k]:.1f} on {k}; mean of December 1997: {np.mean([v for kk, v in d.items() if kk.month == 12]):.1f}")
for name in ("La Libertad", "Santa Cruz", "Baltra"):
    v = [T.daily[name][k] - C.fitday(name, k) for k in T.daily[name] if dt.date(2026, 9, 26) <= k <= dt.date(2026, 9, 30)]
    print(f"   {name}: mean of 26-30 September 2026: {np.mean(v):.1f}")

print("\nD. DO THE SATELLITES RUN LATE? The gauge put through the satellites' own rule (daily anomaly, 15-day running mean,")
print("   the day it passes halfway between its July mean and its mean of 1-22 November and stays above for ten days)")
pts = json.load(open('/home/agent1/trace/data/alt/points.json')); sm = np.load('/home/agent1/trace/alt_smooth.npy'); D0 = dt.date(2026, 5, 1)
def halfway(x, d0):
    ix = lambda d: (d - d0).days
    jul = np.nanmean(x[ix(dt.date(2026, 7, 1)):ix(dt.date(2026, 8, 1))]); nov = np.nanmean(x[ix(dt.date(2026, 11, 1)):ix(dt.date(2026, 11, 23))]); h = (jul + nov) / 2
    for k in range(ix(dt.date(2026, 7, 1)), len(x) - 10):
        seg = x[k:k + 10]
        if not np.isnan(seg).any() and (seg >= h).all(): return d0 + dt.timedelta(days=k), jul, nov
    return None, jul, nov
def smooth(x, w=15):
    out = np.full(len(x), np.nan); hh = w // 2
    for k in range(hh, len(x) - hh):
        seg = x[k - hh:k + hh + 1]
        if (~np.isnan(seg)).sum() >= 0.8 * w: out[k] = np.nanmean(seg)
    return out
def six(sid):
    acc = {}
    for r in csv.reader(open(f'/home/agent1/trace/data/coops/nov/w{sid}.csv')):
        try: t = dt.datetime.strptime(r[0], '%Y-%m-%d %H:%M'); v = float(r[1])
        except (ValueError, IndexError): continue
        acc.setdefault(int((t - dt.datetime(2026, 10, 27)).total_seconds() // 3600), []).append(v * 100)
    x = np.full(24 * 31, np.nan)
    for k, v in acc.items():
        if 0 <= k < len(x) and len(v) >= 8: x[k] = np.mean(v)
    y = C.godin(x)
    return {(dt.datetime(2026, 10, 27) + dt.timedelta(hours=k)).date(): float(y[k]) for k in range(12, len(x), 24) if not np.isnan(y[k])}
for name, sid, km in (("San Diego", "9410170", 6800), ("San Francisco", "9414290", 7600)):
    d = dict(T.daily[name]); d.update({k: v for k, v in C.coops(sid, name).items() if k > dt.date(2026, 9, 30)}); d.update({k: v for k, v in six(sid).items() if k > dt.date(2026, 10, 31)})
    n = (dt.date(2026, 11, 25) - D0).days + 1
    x = np.array([d[D0 + dt.timedelta(days=k)] - C.fitday(name, D0 + dt.timedelta(days=k)) if (D0 + dt.timedelta(days=k)) in d else np.nan for k in range(n)])
    g, jul, nov = halfway(smooth(x), D0); i = [p['km'] for p in pts].index(km); s, sj, sn = halfway(sm[i], D0)
    print(f"   {name}: gauge passes halfway on {g} (July {jul:.1f}, November {nov:.1f} cm); the satellite point at {km} km on {s} (July {sj:.1f}, November {sn:.1f}); the satellite is {(s - g).days} days later")
name = "La Libertad"; n = (dt.date(2026, 9, 30) - D0).days + 1
x = smooth(np.array([T.daily[name][D0 + dt.timedelta(days=k)] - C.fitday(name, D0 + dt.timedelta(days=k)) if (D0 + dt.timedelta(days=k)) in T.daily[name] else np.nan for k in range(n)]))
i = [p['km'] for p in pts].index(0); y = sm[i][:n]; best = None
for L in range(-5, 21):
    a = x[30:n - 20]; b = y[30 + L:n - 20 + L]; ok = ~np.isnan(a) & ~np.isnan(b)
    if ok.sum() > 60:
        c = np.corrcoef(a[ok], b[ok])[0, 1]
        if best is None or c > best[0]: best = (c, L)
print(f"   La Libertad (gauge ends 30 September, so no halfway day): the satellite curve best matches the gauge's when slid {best[1]} days later (correlation {best[0]:.2f})")
print("\nE. OREGON AND WASHINGTON IN OCTOBER (rule L, monthly, from october.out): South Beach September 11.8, October 8.2; Neah Bay 11.4, 6.3")

print("\nF. THE SATELLITE POINTS ONE BY ONE")
raw = np.load('/home/agent1/trace/alt_raw.npy')
def hw(i):
    return halfway(sm[i], D0)[0]
cal = [(p['km'], p['lat'], hw(i)) for i, p in enumerate(pts) if 6700 <= p['km'] <= 7800]
print("   San Diego to Cape Mendocino (6,700 to 7,800 km), halfway days: " + ", ".join(f"{k}: {d.strftime('%d %b')}" for k, la, d in cal))
print(f"   earliest {min(d for k, la, d in cal).strftime('%d %b')}, latest {max(d for k, la, d in cal).strftime('%d %b')}")
north = [(p['km'], p['lat'], hw(i)) for i, p in enumerate(pts) if 7900 <= p['km'] <= 8800]
print("   north of Cape Mendocino (7,900 to 8,800 km): latitudes " + ", ".join(f"{la:.1f}" for k, la, d in north) + f"; points north of 42 N (Oregon and Washington): {sum(1 for k, la, d in north if la > 42.0)} of {len(north)}; halfway days from {min(d for k, la, d in north).strftime('%d %b')} to {max(d for k, la, d in north).strftime('%d %b')}")
a, b = (dt.date(2026, 10, 1) - D0).days, (dt.date(2026, 11, 1) - D0).days
octs = [(p['km'], float(np.nanmean(raw[i, a:b]))) for i, p in enumerate(pts) if -1200 <= p['km'] <= 6600]
print(f"   October means of single points from Peru to Baja California (-1,200 to 6,600 km, {len(octs)} points): lowest {min(v for k, v in octs):.1f} cm (at {min(octs, key=lambda t: t[1])[0]} km), highest {max(v for k, v in octs):.1f} cm (at {max(octs, key=lambda t: t[1])[0]} km)")
print("\nG. THE SAN DIEGO GAUGE, how much of its rise from July to November came with the quick rise")
name = "San Diego"; d = dict(T.daily[name]); d.update({k: v for k, v in C.coops("9410170", name).items() if k > dt.date(2026, 9, 30)}); d.update({k: v for k, v in six("9410170").items() if k > dt.date(2026, 10, 31)})
an = {k: v - C.fitday(name, k) for k, v in d.items()}
m = lambda a, b: float(np.mean([v for k, v in an.items() if a <= k <= b]))
print(f"   July mean {m(dt.date(2026, 7, 1), dt.date(2026, 7, 31)):.1f}; 20-26 September {m(dt.date(2026, 9, 20), dt.date(2026, 9, 26)):.1f}; 1-5 October {m(dt.date(2026, 10, 1), dt.date(2026, 10, 5)):.1f}; October mean {m(dt.date(2026, 10, 1), dt.date(2026, 10, 31)):.1f}; 1-24 November {m(dt.date(2026, 11, 1), dt.date(2026, 11, 24)):.1f}")
print(f"   La Libertad, Santa Cruz, Baltra: change from 27 to 29 September 2026: " + ", ".join(f"{T.daily[n][dt.date(2026, 9, 29)] - T.daily[n][dt.date(2026, 9, 27)]:+.1f}" for n in ("La Libertad", "Santa Cruz", "Baltra")) + " cm")

print("\nH. SAN DIEGO THROUGH SEPTEMBER AND OCTOBER 2026, cm above rule L (after the third reading: how much of the")
print("   step from September's average to October's had come by 1-5 October)")
x = W.series('/home/agent1/trace/data/coops/h9410170.csv'); pr = W.series('/home/agent1/trace/data/coops/baro/b9410170.csv', scale=1.0)
ok = ~np.isnan(pr); pr = np.interp(np.arange(W.N), np.arange(W.N)[ok], pr[ok])
ya, yb = W.godin(x), W.godin(x + 0.995 * (pr - 1013.0))
def per(y, a, b):
    v = []
    day = a
    while day <= b:
        k = int((dt.datetime(day.year, day.month, day.day, 12) - W.T0).total_seconds() // 3600)
        if 0 <= k < W.N and not np.isnan(y[k]): v.append(y[k] - C.fitday("San Diego", day))
        day += dt.timedelta(days=1)
    return float(np.mean(v)), len(v)
spans = [("September (from 4 Sep: the filter needs three days)", dt.date(2026, 9, 1), dt.date(2026, 9, 30)), ("20-26 September", dt.date(2026, 9, 20), dt.date(2026, 9, 26)), ("1-5 October", dt.date(2026, 10, 1), dt.date(2026, 10, 5)),
         ("6-12 October", dt.date(2026, 10, 6), dt.date(2026, 10, 12)), ("13-19 October", dt.date(2026, 10, 13), dt.date(2026, 10, 19)), ("20-29 October", dt.date(2026, 10, 20), dt.date(2026, 10, 29)), ("October (to the 29th)", dt.date(2026, 10, 1), dt.date(2026, 10, 31))]
# the barometer-out series is put on the same footing by giving it the same September-October mean as the measured one
off = np.nanmean(ya) - np.nanmean(yb)
res = {}
print(f"   {'span':<52} {'as measured':>12} {'barometer out':>14}  days")
for label, a, b in spans:
    m1, n1 = per(ya, a, b); m2, n2 = per(yb + off, a, b); res[label] = (m1, m2)
    print(f"   {label:<52} {m1:12.1f} {m2:14.1f}  {n1}")
s = res[spans[0][0]]; o = res[spans[-1][0]]; f = res["1-5 October"]
print(f"   of the way from September's average to October's reached by 1-5 October: as measured {100 * (f[0] - s[0]) / (o[0] - s[0]):.0f}%, barometer out {100 * (f[1] - s[1]) / (o[1] - s[1]):.0f}%")
print(f"   from 13-19 October to 20-29 October: as measured {res['20-29 October'][0] - res['13-19 October'][0]:+.1f} cm, barometer out {res['20-29 October'][1] - res['13-19 October'][1]:+.1f} cm")

print("\nI. SAN DIEGO AND SAN FRANCISCO BEFORE AND AFTER THE TWO STORMS (as measured; cm above rule L; noon values of the filtered hourly heights)")
for name, sid in (("San Diego", "9410170"), ("San Francisco", "9414290")):
    xx = W.godin(W.series(f'/home/agent1/trace/data/coops/h{sid}.csv'))
    def per2(a, b):
        v = []; day = a
        while day <= b:
            k = int((dt.datetime(day.year, day.month, day.day, 12) - W.T0).total_seconds() // 3600)
            if 0 <= k < W.N and not np.isnan(xx[k]): v.append(xx[k] - C.fitday(name, day))
            day += dt.timedelta(days=1)
        return float(np.mean(v))
    vals = [per2(dt.date(2026, 9, 20), dt.date(2026, 9, 26)), per2(dt.date(2026, 9, 30), dt.date(2026, 10, 5)), per2(dt.date(2026, 10, 6), dt.date(2026, 10, 12)), per2(dt.date(2026, 10, 13), dt.date(2026, 10, 19)), per2(dt.date(2026, 10, 20), dt.date(2026, 10, 29))]
    print(f"   {name}: 20-26 Sep {vals[0]:.1f}; 30 Sep-5 Oct {vals[1]:.1f}; 6-12 Oct {vals[2]:.1f}; 13-19 Oct {vals[3]:.1f}; 20-29 Oct {vals[4]:.1f}")
    days = [dt.date(2026, 9, 30) + dt.timedelta(days=k) for k in range(6)]
    print("      day by day, 30 Sep to 5 Oct: " + ", ".join(f"{xx[int((dt.datetime(d.year, d.month, d.day, 12) - W.T0).total_seconds() // 3600)] - C.fitday(name, d):.1f}" for d in days))
print("   the mean curve of the eighteen earlier hurricanes at San Diego (composite.out): +4.0 on day 5, +1.7 on day 6, -0.4 on day 7; day 7 after Polo is 5 October")
