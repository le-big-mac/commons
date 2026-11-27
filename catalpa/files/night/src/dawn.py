# Is it darkest just before dawn? Rules fixed in expectations.md before any reading was looked at.
# Reads the 2024 monthly files of sixteen STARS4ALL TESS-W photometers (data/ida/, fetched by src/fetch_ida.sh).
# Run: ~/ipd/.venv/bin/python -I src/dawn.py > dawn.out      (writes dawn_nights.csv)
import sys, os, re, glob, csv, math, datetime as dt, importlib.util
import numpy as np
spec = importlib.util.spec_from_file_location('sky', '/home/agent1/night/src/sky.py'); sky = importlib.util.module_from_spec(spec); spec.loader.exec_module(sky)
IDA = '/home/agent1/night/data/ida/'
STATIONS = ['stars1', 'stars4', 'stars7', 'stars9', 'stars19', 'stars24', 'stars33', 'stars35', 'stars36', 'stars52', 'stars62', 'stars76', 'stars225', 'stars289', 'stars426', 'stars477']
def runmed(x, w):
    # centred running median, window shortened at the ends
    n = len(x); h = w // 2; out = np.empty(n)
    for i in range(n): out[i] = np.median(x[max(0, i - h):min(n, i + h + 1)])
    return out
def darkest(t, m):
    # t in hours from the end of dusk, m the readings; returns the hour of the darkest moment
    sm = runmed(m, 31); return t[int(np.argmax(sm))]
def spread(m):
    r = m - runmed(m, 61); return 1.4826 * np.median(np.abs(r - np.median(r)))
def slope(t, m): return float(np.polyfit(t, m, 1)[0])
# ---- the test on made-up nights
rng = np.random.default_rng(1650); tt = np.arange(0, 8, 1 / 60)
def trial(shape, n=400):
    f = []
    for _ in range(n):
        m = shape(tt) + rng.normal(0, 0.02, len(tt)); f.append(darkest(tt, m) / tt[-1])
    f = np.array(f); return f
for name, shape in (("flat, with noise", lambda t: 21.0 + 0 * t), ("darkening steadily, 0.05 an hour", lambda t: 18.0 + 0.05 * t), ("darkest in the middle", lambda t: 21.0 - 0.01 * (t - 4) ** 2), ("darkening, then brightening in the last hour", lambda t: 18.0 + 0.05 * np.minimum(t, 7) - 0.10 * np.maximum(t - 7, 0))):
    f = trial(shape); print(f"made-up nights, {name}: middle f {np.median(f):.2f}; f of 0.9 or more in {100 * np.mean(f >= 0.9):.0f} in 100; f over 0.5 in {100 * np.mean(f > 0.5):.0f} in 100")
# ---- reading the files
def read(st):
    T, M, lat, lon, place = [], [], None, None, ''
    for fn in sorted(glob.glob(IDA + st + '_2024-??.dat')):
        txt = open(fn, encoding='utf-8', errors='replace').read()
        if '# END OF HEADER' not in txt: continue
        head, body = txt.split('# END OF HEADER', 1)
        m = re.search(r'# Position: ([-\d.]+), ([-\d.]+)', head)
        if m: lat, lon = float(m.group(1)), float(m.group(2))
        m = re.search(r'# Location name: (.*)', head)
        if m: place = m.group(1).strip()
        for line in body.splitlines():
            p = line.split(';')
            if len(p) < 6: continue
            try: v = float(p[5])
            except ValueError: continue
            if v <= 0: continue
            try: t = dt.datetime.strptime(p[0][:19], '%Y-%m-%dT%H:%M:%S')
            except ValueError: continue
            T.append(t); M.append(v)
    o = np.argsort(np.array(T, dtype='datetime64[s]')) if T else []
    return [T[i] for i in o], np.array([M[i] for i in o]), lat, lon, place
def cross(lat, lon, t0, t1, rising):
    # the moment between t0 and t1 at which the Sun passes -18 degrees (bisection)
    f = lambda t: sky.sun_alt(t, lat, lon) + 18.0
    a, b = t0, t1
    for _ in range(22):
        mid = a + (b - a) / 2
        if (f(mid) > 0) == (f(a) > 0): a = mid
        else: b = mid
    return a + (b - a) / 2
def nights(lat, lon):
    out = []; d = dt.date(2023, 12, 31)
    while d <= dt.date(2024, 12, 31):
        noon = dt.datetime(d.year, d.month, d.day, 12) - dt.timedelta(hours=lon / 15)
        ts = [noon + dt.timedelta(minutes=10 * k) for k in range(145)]; al = [sky.sun_alt(t, lat, lon) for t in ts]
        dusk = dawn = None
        for k in range(144):
            if al[k] >= -18 > al[k + 1] and dusk is None: dusk = cross(lat, lon, ts[k], ts[k + 1], False)
            if al[k] < -18 <= al[k + 1] and dusk is not None and dawn is None: dawn = cross(lat, lon, ts[k], ts[k + 1], True)
        if dusk and dawn and (dawn - dusk).total_seconds() >= 5 * 3600:
            moon = max(sky.moon_alt(dusk + dt.timedelta(minutes=10 * k), lat, lon) for k in range(int((dawn - dusk).total_seconds() // 600) + 2))
            out.append((d, dusk, dawn, moon))
        d += dt.timedelta(days=1)
    return out
rows = []; summary = []
for st in STATIONS:
    T, M, lat, lon, place = read(st)
    if not T or lat is None: print(f"{st}: no readings or no position"); continue
    tsec = np.array([(t - dt.datetime(2024, 1, 1)).total_seconds() for t in T]); step = float(np.median(np.diff(tsec))) if len(tsec) > 1 else 60.0
    cand = []
    for d, dusk, dawn, moon in nights(lat, lon):
        if moon >= 0: continue
        a = (dusk - dt.datetime(2024, 1, 1)).total_seconds(); b = (dawn - dt.datetime(2024, 1, 1)).total_seconds()
        i0, i1 = np.searchsorted(tsec, a), np.searchsorted(tsec, b)
        if i1 - i0 < 10: continue
        # one reading a minute: the median within each minute of the night
        mins = np.floor((tsec[i0:i1] - a) / 60).astype(int); nmin = int((b - a) // 60)
        um = np.unique(mins)
        if len(um) < 0.9 * nmin: continue
        m = np.array([np.median(M[i0:i1][mins == k]) for k in um]); t = (um + 0.5) / 60
        cand.append((d, (b - a) / 3600, t, m, spread(m)))
    if not cand: print(f"{st} ({place}): no moonless covered night"); continue
    floor = float(np.percentile([c[4] for c in cand], 20)); clear = [c for c in cand if c[4] <= 2 * floor]
    for d, L, t, m, s in clear:
        f = darkest(t, m) / L; rows.append((st, d, L, f, slope(t, m), float(np.median(m)), s, float(np.max(runmed(m, 31)) - np.median(m[-30:]))))
    mine = [r for r in rows if r[0] == st]; fs = np.array([r[3] for r in mine]); level = float(np.median([r[5] for r in mine]))
    south = lat < 0; summer = [r[3] for r in mine if (r[1].month in (5, 6, 7, 8)) != south and (r[1].month in (5, 6, 7, 8, 11, 12, 1, 2))]; winter = [r[3] for r in mine if (r[1].month in (11, 12, 1, 2)) != south and (r[1].month in (5, 6, 7, 8, 11, 12, 1, 2))]
    summary.append(dict(st=st, place=place, lat=lat, lon=lon, step=step, ncand=len(cand), n=len(mine), floor=floor, level=level, med=float(np.median(fs)), late=float(np.mean(fs >= 0.9)), early=float(np.mean(fs <= 0.1)), second=float(np.mean(fs > 0.5)),
                        slope=float(np.median([r[4] for r in mine])), summer=summer, winter=winter))
with open('/home/agent1/night/dawn_nights.csv', 'w', newline='') as fh:
    w = csv.writer(fh); w.writerow(['station', 'evening of', 'night length h', 'f', 'slope mag per h', 'median reading', 'spread', 'darkest less last half hour'])
    for r in rows: w.writerow([r[0], r[1], f"{r[2]:.2f}", f"{r[3]:.3f}", f"{r[4]:.4f}", f"{r[5]:.2f}", f"{r[6]:.4f}", f"{r[7]:.3f}"])
print("\nSTATION BY STATION (2024; clear moonless nights; level in magnitudes per square arcsecond, larger is darker)")
print(f"  {'station':<9} {'lat':>6} {'lon':>7} {'nights':>6} {'of':>4} {'level':>6} {'middle f':>8} {'last tenth':>10} {'first tenth':>11} {'2nd half':>8} {'slope/h':>8}  place")
for s in sorted(summary, key=lambda s: s['level']):
    print(f"  {s['st']:<9} {s['lat']:6.1f} {s['lon']:7.1f} {s['n']:6d} {s['ncand']:4d} {s['level']:6.2f} {s['med']:8.2f} {100 * s['late']:9.0f}% {100 * s['early']:10.0f}% {100 * s['second']:7.0f}% {s['slope']:+8.3f}  {s['place'][:60]}")
F = np.array([r[3] for r in rows]); print(f"\nALL {len(F)} NIGHTS: f by tenths of the night, nights in each: " + ", ".join(str(int(np.sum((F >= k / 10) & (F < (k + 1) / 10 if k < 9 else F <= 1)))) for k in range(10)))
print(f"   darkest moment just before dawn (f of 0.9 or more): {100 * np.mean(F >= 0.9):.0f} in 100; in the second half: {100 * np.mean(F > 0.5):.0f} in 100; middle f {np.median(F):.2f}")
ok = [s for s in summary if s['n'] >= 10]; lit = [s for s in ok if s['level'] < 19.5]; dark = [s for s in ok if s['level'] >= 21.0]
def line(tag, text, cls, test):
    if not cls: print(f"{tag} ({text}): VOID, no station in the class"); return
    k = sum(1 for s in cls if test(s)); return k, len(cls)
print("\nTHE LINES OF expectations.md")
print(f"L1 (fewer than half just before dawn, all nights): {100 * np.mean(F >= 0.9):.0f} in 100 -> " + ("HELD" if np.mean(F >= 0.9) < 0.5 else "FAILED"))
print(f"L2 (more than 60 in 100 in the second half): {100 * np.mean(F > 0.5):.0f} in 100 -> " + ("HELD" if np.mean(F > 0.5) > 0.6 else "FAILED"))
for tag, text, cls, test, need in (("L3", "lit stations: middle f of 0.7 or more at two thirds", lit, lambda s: s['med'] >= 0.7, 2 / 3), ("L4", "lit stations: over a quarter just before dawn at half of them", lit, lambda s: s['late'] > 0.25, 0.5),
                                   ("L5", "dark stations: middle f between 0.3 and 0.7 at two thirds", dark, lambda s: 0.3 <= s['med'] <= 0.7, 2 / 3), ("L6", "lit stations: middle slope 0.02 to 0.10 an hour at two thirds", lit, lambda s: 0.02 <= s['slope'] <= 0.10, 2 / 3),
                                   ("L7", "dark stations: middle slope within 0.02 an hour of nothing at two thirds", dark, lambda s: abs(s['slope']) <= 0.02, 2 / 3)):
    r = line(tag, text, cls, test)
    if r: print(f"{tag} ({text}): {r[0]} of {r[1]} -> " + ("HELD" if r[0] / r[1] >= need - 1e-9 else "FAILED"))
if lit:
    k = sum(1 for s in lit if s['summer'] and s['winter'] and np.mean(np.array(s['summer']) >= 0.9) > np.mean(np.array(s['winter']) >= 0.9)); n = len(lit)
    print(f"L8 (lit stations: just before dawn commoner in the four summer months than the four winter ones, at more than half): {k} of {n} -> " + ("HELD" if k > n / 2 else "FAILED"))
    for s in lit: print(f"     {s['st']}: summer {len(s['summer'])} nights, {100 * np.mean(np.array(s['summer']) >= 0.9) if s['summer'] else float('nan'):.0f} in 100; winter {len(s['winter'])} nights, {100 * np.mean(np.array(s['winter']) >= 0.9) if s['winter'] else float('nan'):.0f} in 100")
else: print("L8: VOID, no lit station")
print(f"\nclasses: lit {[s['st'] for s in lit]}; dark {[s['st'] for s in dark]}; between {[s['st'] for s in ok if s not in lit and s not in dark]}; under ten nights {[s['st'] for s in summary if s['n'] < 10]}")
