# Tide gauges from Callao to Ketchikan: monthly anomalies (rule L), late-summer comparison of
# 1997, 2015 and 2026, and day-to-day travel. Scores the lines T1 to T8 of expectations.md.
# Run: ~/ipd/.venv/bin/python -I src/trace.py > trace.out
# Choices made after the seal and before any result (not in expectations.md):
#   a running mean is defined where at least 80% of its window is valid;
#   a lagged correlation needs at least 150 days in common.
import csv, sys, datetime as dt
import numpy as np
sys.path.insert(0, '/home/agent1/trace/src')
from coastline import distances, SANTA_CRUZ_TO_COAST

D = '/home/agent1/trace/data/'
G = [("093", "Callao", -12.07), ("091", "La Libertad", -2.22), ("030", "Santa Cruz", -0.76), ("003", "Baltra", -0.44),
     ("087", "Quepos", 9.43), ("082", "Acajutla", 13.57), ("569", "San Diego", 32.71), ("554", "La Jolla", 32.87),
     ("551", "San Francisco", 37.81), ("556", "Crescent City", 41.75), ("592", "South Beach", 44.63),
     ("558", "Neah Bay", 48.37), ("542", "Tofino", 49.15), ("540", "Prince Rupert", 54.32), ("571", "Ketchikan", 55.33)]
dist = distances(); dist["Santa Cruz"] = -SANTA_CRUZ_TO_COAST; dist["Baltra"] = -SANTA_CRUZ_TO_COAST

def load(sid):
    d = {}
    for r in csv.reader(open(D + f'd{sid}.csv')):
        if len(r) >= 4 and int(r[3]) > -30000:
            d[dt.date(int(r[0]), int(r[1]), int(r[2]))] = int(r[3]) / 10.0   # cm
    return d

def monthly(d):
    acc = {}
    for day, v in d.items(): acc.setdefault((day.year, day.month), []).append(v)
    return {k: float(np.mean(v)) for k, v in acc.items() if len(v) >= 20}

def ruleL(m):
    keys = [k for k in m if 1990 <= k[0] <= 2025]
    if len(keys) < 300: return None, len(keys)
    t = np.array([k[0] + (k[1] - 0.5) / 12 for k in keys]); y = np.array([m[k] for k in keys])
    def X(t):
        return np.column_stack([np.ones_like(t), t - 2008, np.cos(2*np.pi*t), np.sin(2*np.pi*t), np.cos(4*np.pi*t), np.sin(4*np.pi*t)])
    c = np.linalg.lstsq(X(t), y, rcond=None)[0]
    return (lambda yy, mm: float(X(np.array([yy + (mm - 0.5) / 12]))[0] @ c)), len(keys), c[1]

daily = {name: load(sid) for sid, name, lat in G}
mon = {name: monthly(daily[name]) for sid, name, lat in G}
fit = {}
print("RULE L: fit of constant, line, annual and half-yearly wave to monthly means of 1990-2025")
print(f"{'gauge':<14} {'lat':>6} {'months':>6} {'trend mm/yr':>11}")
for sid, name, lat in G:
    r = ruleL(mon[name])
    if r[0] is None:
        print(f"{name:<14} {lat:6.1f} {r[1]:6d}   too few months for rule L"); continue
    fit[name] = r[0]
    print(f"{name:<14} {lat:6.1f} {r[1]:6d} {r[2]*10:11.2f}")

def anom(name, y, m):
    if name not in fit or (y, m) not in mon[name]: return None
    return mon[name][(y, m)] - fit[name](y, m)

def f(x, w=6): return f"{x:{w}.1f}" if x is not None else " " * (w - 1) + "-"

for year in (1982, 1997, 2015, 2023, 2026):
    print(f"\nMONTHLY ANOMALIES, rule L, cm, {year}")
    print(f"{'gauge':<14}" + "".join(f"{m:>6}" for m in "JFMAMJJASOND"))
    for sid, name, lat in G:
        if name in fit: print(f"{name:<14}" + "".join(f(anom(name, year, m)) for m in range(1, 13)))

def late(name, y):
    a, b = anom(name, y, 8), anom(name, y, 9)
    return None if a is None or b is None else (a + b) / 2

print("\nLATE SUMMER (mean of August and September anomalies), rule L, cm")
print(f"{'gauge':<14} {'km':>6} {'1982':>6} {'1997':>6} {'2015':>6} {'2023':>6} {'2026':>6} {'26/97':>6} {'26/15':>6}")
for sid, name, lat in G:
    if name not in fit: continue
    v = {y: late(name, y) for y in (1982, 1997, 2015, 2023, 2026)}
    r97 = v[2026] / v[1997] if v[2026] is not None and v[1997] else None
    r15 = v[2026] / v[2015] if v[2026] is not None and v[2015] else None
    print(f"{name:<14} {dist.get(name, float('nan')):6.0f} " + " ".join(f(v[y]) for y in (1982, 1997, 2015, 2023, 2026)) + f" {f(r97) if r97 is None else format(r97, '6.2f')} {f(r15) if r15 is None else format(r15, '6.2f')}")

print("\nTHE SEALED LINES")
def ratio(name, y):
    a, b = late(name, 2026), late(name, y)
    return None if a is None or b is None else (a / b, b)
for tag, y in (("T1", 1997), ("T2", 2015)):
    r = {n: ratio(n, y) for n in ("San Diego", "La Libertad", "Santa Cruz")}
    if any(v is None for v in r.values()): print(f"{tag}: cannot be scored (a value is missing): {r}"); continue
    void = any(v[1] < 5 for v in r.values())
    held = r["San Diego"][0] > r["La Libertad"][0] and r["San Diego"][0] > r["Santa Cruz"][0]
    print(f"{tag}: ratio 2026/{y}: San Diego {r['San Diego'][0]:.2f}, La Libertad {r['La Libertad'][0]:.2f}, Santa Cruz {r['Santa Cruz'][0]:.2f}"
          f" ({y} anomalies {r['San Diego'][1]:.1f}, {r['La Libertad'][1]:.1f}, {r['Santa Cruz'][1]:.1f} cm) -> " + ("VOID" if void and tag == "T1" else ("HELD" if held else "FAILED")) + (" (note: an anomaly of the earlier year is below 5 cm)" if void and tag != "T1" else ""))
a = late("La Libertad", 2026)
print(f"T3: La Libertad late summer 2026 = {a:.1f} cm; between 15 and 35 -> " + ("HELD" if 15 <= a <= 35 else "FAILED"))
ma = mon["Acajutla"]
try:
    d4 = (ma[(2026, 8)] + ma[(2026, 9)]) / 2 - (ma[(2015, 8)] + ma[(2015, 9)]) / 2
    print(f"T4: Acajutla, plain mean Aug-Sep 2026 minus 2015 = {d4:+.1f} cm; more than +3 -> " + ("HELD" if d4 > 3 else "FAILED"))
except KeyError as e: print("T4: cannot be scored, month missing:", e)
north = [late(n, 2026) for n in ("Neah Bay", "Tofino", "Prince Rupert", "Ketchikan")]
sd = late("San Diego", 2026)
if None in north: print("T5: cannot be scored, a northern value is missing:", north)
else:
    nm = float(np.mean(north))
    print(f"T5: north mean {nm:.1f} cm ({', '.join(f'{x:.1f}' for x in north)}); San Diego {sd:.1f}; a third of it {sd/3:.1f} -> " + ("HELD" if nm < sd / 3 else "FAILED"))

# ---- day-to-day travel
def series(name, y):
    d = daily[name]; t0 = dt.date(y - 1, 11, 1); n = (dt.date(y, 10, 31) - t0).days + 1
    x = np.full(n, np.nan)
    for i in range(n):
        v = d.get(t0 + dt.timedelta(days=i))
        if v is not None: x[i] = v
    # fill gaps of up to 3 days
    i = 0
    while i < n:
        if np.isnan(x[i]):
            j = i
            while j < n and np.isnan(x[j]): j += 1
            if i > 0 and j < n and j - i <= 3:
                x[i:j] = np.interp(np.arange(i, j), [i - 1, j], [x[i - 1], x[j]])
            i = j
        else: i += 1
    def run(x, w):
        h = w // 2; out = np.full(n, np.nan)
        for k in range(h, n - h):
            seg = x[k - h:k + h + 1]; ok = ~np.isnan(seg)
            if ok.sum() >= 0.8 * w: out[k] = seg[ok].mean()
        return out
    b = run(x, 7) - run(x, 61)
    i0 = (dt.date(y, 1, 1) - t0).days; i1 = (dt.date(y, 8, 31) - t0).days
    return b, i0, i1

def lagcorr(a, b, i0, i1, lag):
    # correlation of a(t) with b(t+lag), t from i0 to i1
    idx = np.arange(i0, i1 + 1); j = idx + lag
    ok = (j >= 0) & (j < len(b)); idx, j = idx[ok], j[ok]
    x, y = a[idx], b[j]; ok = ~np.isnan(x) & ~np.isnan(y)
    if ok.sum() < 150: return None
    return float(np.corrcoef(x[ok], y[ok])[0, 1])

def best(name, y, ref="Santa Cruz"):
    a, i0, i1 = series(ref, y); b, _, _ = series(name, y)
    cs = [(lagcorr(a, b, i0, i1, L), L) for L in range(-20, 61)]
    cs = [c for c in cs if c[0] is not None]
    if not cs: return None
    c, L = max(cs)
    return L, c, lagcorr(a, b, i0, i1, 0)

for y in (2026, 1997, 2015, 1982):
    print(f"\nDAY-TO-DAY TRAVEL, {y}: 7-day minus 61-day running mean, 1 Jan to 31 Aug; best lag after Santa Cruz (-20..+60 days)")
    print(f"{'gauge':<14} {'km':>6} {'lag d':>6} {'corr':>6} {'corr at 0':>9}")
    for sid, name, lat in G:
        if name == "Santa Cruz": continue
        r = best(name, y)
        if r is None: print(f"{name:<14} {dist.get(name, float('nan')):6.0f}   too little data"); continue
        print(f"{name:<14} {dist.get(name, float('nan')):6.0f} {r[0]:6d} {r[1]:6.2f} {r[2] if r[2] is not None else float('nan'):9.2f}")

r = {n: best(n, 2026) for n in ("La Libertad", "Acajutla", "San Diego")}
if any(v is None for v in r.values()): print("\nT6: cannot be scored:", r)
else:
    L = [r[n][0] for n in ("La Libertad", "Acajutla", "San Diego")]
    print(f"\nT6: 2026 lags after Santa Cruz: La Libertad {L[0]}, Acajutla {L[1]}, San Diego {L[2]} days -> " + ("HELD" if 0 < L[0] < L[1] < L[2] else "FAILED"))
years = []
for y in range(1990, 2027):
    b = best("San Diego", y)
    if b is not None: years.append((b[1], y, b[0]))
years.sort(reverse=True)
rank = [y for c, y, L in years].index(2026) + 1 if any(y == 2026 for c, y, L in years) else None
cut = round(8 / 37 * len(years))
print(f"T7: best correlation Santa Cruz - San Diego by year, {len(years)} years with enough data; the top {cut} count as 'among the 8 of 37'")
print("    " + ", ".join(f"{y} {c:.2f} ({L:+d} d)" for c, y, L in years))
print(f"    2026 ranks {rank} of {len(years)} -> " + ("HELD" if rank is not None and rank <= cut else "FAILED"))
r = {n: best(n, 1997) for n in ("La Libertad", "San Diego")}
if any(v is None for v in r.values()): print("T8: cannot be scored:", r)
else:
    l1, l2 = r["La Libertad"][0], r["San Diego"][0]
    sp = dist["San Diego"] * 1000 / ((l2 - l1) * 86400) if l2 > l1 else None
    print(f"T8: 1997 lags after Santa Cruz: La Libertad {l1}, San Diego {l2} days; speed La Libertad to San Diego "
          + (f"{sp:.2f} m/s" if sp else "undefined") + " -> " + ("HELD" if sp and l1 > 0 and 1.5 <= sp <= 4 else "FAILED"))
