# Things the fourth reading raised, recomputed here before the pages were rewritten (26 Nov, 21:25 on).
# Run: ~/ipd/.venv/bin/python -I src/after4.py > after4.out
import sys, io, contextlib, importlib.util, csv, json, datetime as dt
import numpy as np
def load(name):
    spec = importlib.util.spec_from_file_location(name, f'/home/agent1/trace/src/{name}.py'); m = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(m)
    return m
CO = load('composite'); PS = CO.PS; C = CO.C; T = CO.T; W = CO.W; B = load('buoys')
from coastline import gc
SD = (32.714, -117.174)
def tracks(y0=1990, y1=2025):
    out = {}; cur = None
    for l in open('/home/agent1/trace/data/hurdat/nepac.txt'):
        w = [x.strip() for x in l.split(',')]
        if w[0][:2] in ('EP', 'CP') and len(w[0]) == 8: cur = (w[0], w[1]); continue
        if cur is None or len(w) < 7: continue
        d = dt.datetime.strptime(w[0] + w[1], '%Y%m%d%H%M')
        if not (y0 <= d.year <= y1): continue
        lat = float(w[4][:-1]); lon = -float(w[5][:-1]) if w[5][-1] == 'W' else float(w[5][:-1])
        out.setdefault(cur, []).append((d, lat, lon, int(w[6])))
    return out
TR = tracks()
print("A. THE EIGHTEEN, by how near each came to San Diego while at tropical-storm strength (34 knots) or more, with its rise and 'two weeks on' at San Diego (cm)")
rows = []
for e in CO.EV:
    pts = TR[(e[0], e[1])]; near = min(gc(SD, (p[1], p[2])) for p in pts if p[3] >= 34)
    m = CO.measure(CO.A["San Diego"], e[2].date()); rows.append((near, e[1], e[2].date(), m[0], m[1]))
for r in sorted(rows): print(f"   {r[1]:<10} {r[2]}  nearest {r[0]:5.0f} km   rise {r[3]:+5.1f}   two weeks on {r[4]:+5.1f}")
close = [r for r in rows if r[0] < 400]; far = [r for r in rows if r[0] >= 400]
print(f"   came within 400 km of San Diego ({len(close)}): mean rise {np.mean([r[3] for r in close]):+.1f}; stayed further off ({len(far)}): mean rise {np.mean([r[3] for r in far]):+.1f}, {sum(1 for r in far if r[3] > 0)} of {len(far)} above zero; Polo's nearest to San Diego was 813 km (polo.out)")
print("   of the twelve that rose: 'two weeks on' is under half the rise in " + str(sum(1 for r in rows if r[3] > 0 and r[4] < r[3] / 2)) + "; not in: " + ", ".join(f"{r[1]} {r[2].year} ({r[3]:+.1f}, then {r[4]:+.1f})" for r in rows if r[3] > 0 and r[4] >= r[3] / 2))

print("\nB. LINDA, September 2015 (not on the list: never within 300 km of the line)")
pts = TR[[k for k in TR if k[1] == 'LINDA' and k[0].endswith('2015')][0]]
hu = [(p[0], p[1], p[2], p[3], PS.near(p[1], p[2])[0]) for p in pts if p[3] >= 64 and p[1] >= 22.0]
print("   points at hurricane strength north of 22 N: " + "; ".join(f"{p[0].strftime('%d %b %H:%M')} {p[1]:.1f}N {abs(p[2]):.1f}W {p[3]} kt, {p[4]:.0f} km off the line" for p in hu))
D = hu[0][0].date()
for name in ("San Diego", "San Francisco"):
    a = CO.A[name]; base = CO.span(a, D, -10, -4, 5)
    print(f"   {name}, day D = {D}: base {base:.1f}; rise (days 1-5) {CO.span(a, D, 1, 5, 4) - base:+.1f}; days 9-13 {CO.span(a, D, 9, 13, 4) - base:+.1f}; days 16-20 {CO.span(a, D, 16, 20, 4) - base:+.1f}; days 23-27 {CO.span(a, D, 23, 27, 4) - base:+.1f}")
print("   the same further weeks for Nora (D = 1997-09-24) at San Diego: " + ", ".join(f"days {k0}-{k1} {CO.span(CO.A['San Diego'], dt.date(1997, 9, 24), k0, k1, 4) - CO.span(CO.A['San Diego'], dt.date(1997, 9, 24), -10, -4, 5):+.1f}" for k0, k1 in ((1, 5), (9, 13), (16, 20), (23, 27))))
print("   San Diego's level before each of the three (mean of days -10 to -4, cm above rule L): Nora 1997 " + f"{CO.span(CO.A['San Diego'], dt.date(1997, 9, 24), -10, -4, 5):.1f}; Linda 2015 {CO.span(CO.A['San Diego'], D, -10, -4, 5):.1f}; Polo 2026 {CO.mp[2]:.1f}")

print("\nC. WIND AND SEA TIMED BY THE SAME RULE across the first rise (before 20-26 Sep, after 1-5 Oct; first hour after 26 Sep past halfway and held 12 hours)")
def halfway(y):
    Bv = np.nanmean(y[W.h((9, 20)):W.h((9, 27))]); Av = np.nanmean(y[W.h((10, 1)):W.h((10, 6))]); half = Bv + (Av - Bv) / 2
    for k in range(W.h((9, 26)), W.h((10, 6))):
        seg = y[k:k + 12]
        if not np.isnan(seg).any() and (seg >= half).all(): return k, Av - Bv
    return None, Av - Bv
fmt = lambda k: (W.T0 + dt.timedelta(hours=k)).strftime('%d %b %H:%M') if k is not None else '-'
for gname, gid, bids in (("San Diego", "9410170", ["46086"]), ("Los Angeles", "9410660", ["46025"]), ("Port San Luis", "9412110", ["46054", "46011"]), ("Monterey", "9413450", ["46028", "46042"]),
                         ("San Francisco", "9414290", ["46012", "46026"]), ("Point Reyes", "9415020", ["46013"]), ("Arena Cove", "9416841", ["46014"]), ("North Spit", "9418767", ["46022"])):
    ks, rise = halfway(W.filt(gid, ib=True))
    print(f"   {gname:<14} sea (barometer out) {fmt(ks)} (+{rise:.1f} cm) | " + "; ".join(f"buoy {b}: wind {fmt(halfway(B.AF[b])[0])} ({halfway(B.AF[b])[1]:+.1f} m/s)" for b in bids))

print("\nD. DAY BY DAY, 30 September to 5 October, barometer out (noon values, cm above rule L, on the footing of after2.out H)")
for name, sid in (("San Diego", "9410170"), ("San Francisco", "9414290")):
    x = W.series(f'/home/agent1/trace/data/coops/h{sid}.csv'); pr = W.series(f'/home/agent1/trace/data/coops/baro/b{sid}.csv', scale=1.0)
    ok = ~np.isnan(pr); pr = np.interp(np.arange(W.N), np.arange(W.N)[ok], pr[ok]); ya, yb = W.godin(x), W.godin(x + 0.995 * (pr - 1013.0)); off = np.nanmean(ya) - np.nanmean(yb)
    days = [dt.date(2026, 9, 30) + dt.timedelta(days=k) for k in range(6)]
    print(f"   {name}: " + ", ".join(f"{yb[int((dt.datetime(d.year, d.month, d.day, 12) - W.T0).total_seconds() // 3600)] + off - C.fitday(name, d):.1f}" for d in days))

print("\nE. OREGON AND WASHINGTON at the end of October (as measured, cm above rule L, noon values)")
for name, sid in (("South Beach", "9435380"), ("Neah Bay", "9443090")):
    x = W.godin(W.series(f'/home/agent1/trace/data/coops/h{sid}.csv'))
    def per(a, b):
        v = []; day = a
        while day <= b:
            k = int((dt.datetime(day.year, day.month, day.day, 12) - W.T0).total_seconds() // 3600)
            if 0 <= k < W.N and not np.isnan(x[k]): v.append(x[k] - C.fitday(name, day))
            day += dt.timedelta(days=1)
        return float(np.mean(v)) if v else float('nan')
    print(f"   {name}: 1-12 Oct {per(dt.date(2026, 10, 1), dt.date(2026, 10, 12)):.1f}; 13-26 Oct {per(dt.date(2026, 10, 13), dt.date(2026, 10, 26)):.1f}; 27-29 Oct {per(dt.date(2026, 10, 27), dt.date(2026, 10, 29)):.1f}")
