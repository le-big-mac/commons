# Wind over the sea from fourteen NOAA buoys, September-October 2026, on the days of the two rises at San Diego.
# Scores the lines V1 to V8 of expectations-3.md. Written and hashed before any wind value was looked at.
# Run: ~/ipd/.venv/bin/python -I src/buoys.py > buoys.out
import sys, io, contextlib, importlib.util, re, math, datetime as dt
import numpy as np
def load(name):
    spec = importlib.util.spec_from_file_location(name, f'/home/agent1/trace/src/{name}.py'); m = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(m)
    return m
W = load('wave')
from coastline import WAY, gc
D = '/home/agent1/trace/data/ndbc/'
IDS = "46086 46025 46053 46054 46011 46028 46042 46012 46026 46013 46014 46022 46027 46015".split()
T0, N = W.T0, W.N
h = lambda mo, d, hh=0: int((dt.datetime(2026, mo, d, hh) - T0).total_seconds() // 3600)
# positions
pos = {}
for l in open(D + 'station_table.txt', encoding='utf-8', errors='replace'):
    w = l.split('|')
    if w[0].strip() in IDS:
        m = re.search(r'([\d.]+) ([NS]) ([\d.]+) ([EW])', w[6]); pos[w[0].strip()] = (float(m.group(1)), -float(m.group(3)))
# the coast's bearing (south to north) and the distance along it from San Diego, at the point of the line nearest each buoy
cum = [0.0]
for i in range(1, len(WAY)): cum.append(cum[-1] + gc(WAY[i - 1][1:], WAY[i][1:]))
isd = [w[0] for w in WAY].index("San Diego")
def bearing(a, b):
    p1, p2 = math.radians(a[0]), math.radians(b[0]); dl = math.radians(b[1] - a[1])
    return math.degrees(math.atan2(math.sin(dl) * math.cos(p2), math.cos(p1) * math.sin(p2) - math.sin(p1) * math.cos(p2) * math.cos(dl))) % 360
geo = {}
for sid, p in pos.items():
    best = None
    for i in range(len(WAY) - 1):
        a, b = WAY[i][1:], WAY[i + 1][1:]
        for f in np.linspace(0, 1, 41):
            q = (a[0] + f * (b[0] - a[0]), a[1] + f * (b[1] - a[1])); dd = gc(p, q)
            if best is None or dd < best[0]: best = (dd, cum[i] + f * (cum[i + 1] - cum[i]) - cum[isd], bearing(a, b))
    geo[sid] = best   # (km off the line, km along the coast from San Diego, bearing of the coast)
def along(sid):
    acc = {}
    for mon in ("sep", "oct"):
        for l in open(D + f"{sid}_{mon}.txt"):
            if l.startswith('#'): continue
            w = l.split()
            if len(w) < 7 or w[5] in ('999', 'MM') or w[6] in ('99.0', 'MM'): continue
            t = dt.datetime(int(w[0]), int(w[1]), int(w[2]), int(w[3])); k = int((t - T0).total_seconds() // 3600)
            if not 0 <= k < N: continue
            sp, di = float(w[6]), float(w[5])
            acc.setdefault(k, []).append(sp * math.cos(math.radians((di + 180) - geo[sid][2])))
    x = np.full(N, np.nan)
    for k, v in acc.items(): x[k] = np.mean(v)
    # gaps of up to 6 hours filled by straight lines
    i = 0
    while i < N:
        if np.isnan(x[i]):
            j = i
            while j < N and np.isnan(x[j]): j += 1
            if i > 0 and j < N and j - i <= 6: x[i:j] = np.interp(np.arange(i, j), [i - 1, j], [x[i - 1], x[j]])
            i = j
        else: i += 1
    return x
RAW = {sid: along(sid) for sid in IDS}; AF = {sid: W.godin(RAW[sid]) for sid in IDS}
def grp(ids):
    m = np.array([AF[s] for s in ids]); ok = (~np.isnan(m)).sum(axis=0) >= 2
    out = np.full(N, np.nan); out[ok] = np.nanmean(m[:, ok], axis=0); return out
AF["Bight"] = grp(["46086", "46025", "46053"]); AF["Central"] = grp(["46028", "46042", "46012", "46026", "46013"])
def mean(x, a, b):   # hours a..b-1
    seg = x[a:b]; ok = ~np.isnan(seg)
    return float(seg[ok].mean()) if ok.sum() >= 0.8 * len(seg) else np.nan
def shift1(x, d): return mean(x, d + 11 * 24, d + 16 * 24) - mean(x, d, d + 7 * 24)     # seven days, a gap of four, five days
def shift2(x, d): return mean(x, d + 7 * 24, d + 17 * 24) - mean(x, d, d + 7 * 24)      # seven days, then ten
def yard(x, fn, last):
    return np.array([fn(x, d) for d in range(h(9, 3), last + 1, 24)])
Y1 = lambda x: yard(x, shift1, h(10, 14)); Y2 = lambda x: yard(x, shift2, h(10, 13))
def unusual(x, fn, d, ys):
    s = fn(x, d); others = ys[~np.isnan(ys)]
    frac = float((others < s).mean())
    return s, frac, (s > 0 and frac >= 0.8)

print("THE BUOYS: km along the coast from San Diego, km off the line, the coast's bearing there (degrees), hours with wind")
for sid in IDS: print(f"  {sid}  {geo[sid][1]:6.0f} {geo[sid][0]:5.0f} {geo[sid][2]:5.0f}   {int((~np.isnan(RAW[sid])).sum())} of {N}")

print("\nALONGSHORE WIND (71-hour weight), daily at 12:00 UTC, m/s; positive = the air moves towards the pole")
for a, b in ((dt.date(2026, 9, 18), dt.date(2026, 10, 8)), (dt.date(2026, 10, 10), dt.date(2026, 10, 29))):
    print("date        " + "".join(f"{s:>7}" for s in IDS) + "   Bight Central")
    day = a
    while day <= b:
        k = h(day.month, day.day, 12)
        print(f"{day}  " + "".join(f"{AF[s][k]:7.1f}" for s in IDS) + f" {AF['Bight'][k]:7.1f} {AF['Central'][k]:7.1f}")
        day += dt.timedelta(days=1)
    print()

print("SHIFTS in the alongshore wind (m/s, towards the pole positive), with the share of the yardstick's shifts that are smaller")
print(f"{'':10} {'rise 1: 20-26 Sep to 1-5 Oct':>32} {'rise 2: 13-19 Oct to 20-29 Oct':>34}   mean wind Sep / Oct")
for s in IDS + ["Bight", "Central"]:
    a = unusual(AF[s], shift1, h(9, 20), Y1(AF[s])); b = unusual(AF[s], shift2, h(10, 13), Y2(AF[s]))
    print(f"{s:<10} {a[0]:+12.1f}  above {100 * a[1]:3.0f}% {'UNUSUAL' if a[2] else '':>8} {b[0]:+14.1f}  above {100 * b[1]:3.0f}% {'UNUSUAL' if b[2] else '':>8}   {mean(AF[s], h(9, 3), h(10, 1)):+.1f} / {mean(AF[s], h(10, 1), h(10, 30)):+.1f}")

print("\nTHE SEALED LINES")
a = unusual(AF["Central"], shift1, h(9, 20), Y1(AF["Central"])); print(f"V1: rise 1, central group: shift {a[0]:+.1f} m/s, above {100 * a[1]:.0f}% of the yardstick -> " + ("HELD" if a[2] else "FAILED"))
a = unusual(AF["Bight"], shift1, h(9, 20), Y1(AF["Bight"])); print(f"V2: rise 1, Bight group: shift {a[0]:+.1f} m/s, above {100 * a[1]:.0f}% of the yardstick -> " + ("HELD" if a[2] else "FAILED"))
a = unusual(AF["Central"], shift2, h(10, 13), Y2(AF["Central"])); print(f"V3: rise 2, central group: shift {a[0]:+.1f} m/s, above {100 * a[1]:.0f}% of the yardstick -> " + ("HELD" if a[2] else "FAILED"))
ids4 = IDS[:IDS.index("46022") + 1]; a4, b4 = h(9, 28), h(10, 2, 12)
hrs = [a4 + int(np.nanargmax(AF[s][a4:b4 + 1])) for s in ids4]; xs = np.array([geo[s][1] for s in ids4])
sl, ic = np.polyfit(xs, np.array(hrs, float), 1)
print("V4: hour of the strongest poleward (or weakest equatorward) wind, 28 Sep 00:00 to 2 Oct 12:00: " + ", ".join(f"{s} {(T0 + dt.timedelta(hours=k)).strftime('%d %b %H:%M')}" for s, k in zip(ids4, hrs)))
print(f"    straight line: {sl * 1000:.1f} hours per 1000 km" + (f" = {24 / sl:.0f} km/day" if sl > 0 else " (not northward)") + " -> " + ("HELD" if sl > 0 and 300 <= 24 / sl <= 2000 else "FAILED"))
def history(x, tau=72.0, span=216):
    w = np.exp(-np.arange(span + 1) / tau); w /= w.sum(); out = np.full(N, np.nan)
    for k in range(span, N):
        seg = x[k - span:k + 1][::-1]
        if not np.isnan(seg).any(): out[k] = float((seg * w).sum())
    return out
def relate(gid, bid):
    y = W.filt(gid, ib=True); wh = history(AF[bid])
    t = np.arange(N); fit = (t >= h(9, 6)) & (t < h(10, 29)) & ~((t >= h(9, 20)) & (t < h(10, 6))) & ~np.isnan(y) & ~np.isnan(wh)
    def detr(v):
        c = np.polyfit(t[fit], v[fit], 1); return v[fit] - np.polyval(c, t[fit])
    yy, ww = detr(y), detr(wh)
    r = float(np.corrcoef(yy, ww)[0, 1]); b = float((yy * ww).sum() / (ww * ww).sum())
    dW = mean(wh, h(10, 1), h(10, 6)) - mean(wh, h(9, 20), h(9, 27)); rise = mean(y, h(10, 1), h(10, 6)) - mean(y, h(9, 20), h(9, 27))
    dW2 = mean(wh, h(10, 20), h(10, 30)) - mean(wh, h(10, 13), h(10, 20)); rise2 = mean(y, h(10, 20), h(10, 30)) - mean(y, h(10, 13), h(10, 20))
    return r, b, dW, rise, int(fit.sum()), dW2, rise2
r = relate("9414290", "46026"); print(f"V5: San Francisco and 46026, outside 20 Sep - 5 Oct ({r[4]} hours): correlation {r[0]:+.2f} -> " + ("HELD" if r[0] > 0.5 else "FAILED"))
q = relate("9410170", "46086"); print(f"V6: San Diego and 46086 ({q[4]} hours): correlation {q[0]:+.2f} -> " + ("HELD" if q[0] > 0.5 else "FAILED"))
sh = r[1] * r[2] / r[3]; print(f"V7: San Francisco: slope {r[1]:+.2f} cm per m/s of wind history; wind history changed {r[2]:+.2f} m/s across rise 1; that gives {r[1] * r[2]:+.1f} cm of the {r[3]:.1f} cm rise; share {sh:.2f} -> " + ("HELD" if sh >= 0.5 else "FAILED"))
sh = q[1] * q[2] / q[3]; print(f"V8: San Diego: slope {q[1]:+.2f} cm per m/s; wind history changed {q[2]:+.2f} m/s; that gives {q[1] * q[2]:+.1f} cm of the {q[3]:.1f} cm rise; share {sh:.2f} -> " + ("HELD" if sh >= 0.5 else "FAILED"))

print("\nEVERY GAUGE WITH THE BUOY NEAREST IT (the two sealed pairs and eight more, not sealed): the same relation")
print(f"{'gauge':<14} {'buoy':>6} {'corr':>6} {'cm per m/s':>11} {'rise 1: wind history':>21} {'gives cm':>9} {'of rise cm':>11} {'rise 2: wind history':>21} {'gives cm':>9} {'of rise cm':>11}")
for name, gid, bid in (("San Diego", "9410170", "46086"), ("Los Angeles", "9410660", "46025"), ("Santa Barbara", "9411340", "46053"), ("Port San Luis", "9412110", "46011"), ("Monterey", "9413450", "46042"),
                       ("San Francisco", "9414290", "46026"), ("Point Reyes", "9415020", "46013"), ("Arena Cove", "9416841", "46014"), ("North Spit", "9418767", "46022"), ("Crescent City", "9419750", "46027")):
    try: z = relate(gid, bid)
    except Exception as e: print(f"{name:<14} {bid:>6}  could not be fitted: {e}"); continue
    print(f"{name:<14} {bid:>6} {z[0]:+6.2f} {z[1]:+11.2f} {z[2]:+21.2f} {z[1] * z[2]:+9.1f} {z[3]:11.1f} {z[5]:+21.2f} {z[1] * z[5]:+9.1f} {z[6]:11.1f}")
