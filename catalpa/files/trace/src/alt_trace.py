# Satellite sea level along the coast, Callao to Neah Bay, June to November 2026, against 2017-2025.
# Scores the lines S1 to S6 of expectations-2.md. Written while the downloads ran, before any value was seen.
# Run: ~/ipd/.venv/bin/python -I src/alt_trace.py > alt_trace.out
import json, csv, datetime as dt, sys
import numpy as np
A = '/home/agent1/trace/data/alt/'
pts = json.load(open(A + 'points.json'))
D0, D1 = dt.date(2026, 5, 1), dt.date(2026, 11, 25); ND = (D1 - D0).days + 1
def doy(d): return d.timetuple().tm_yday
def read(fn):
    out = {}
    for r in csv.reader(open(fn)):
        if len(r) < 4 or not r[0][:1].isdigit() or r[3] in ('NaN', ''): continue
        out.setdefault((float(r[1]), float(r[2])), []).append((dt.date(int(r[0][:4]), int(r[0][5:7]), int(r[0][8:10])), float(r[3]) * 100))
    return out
raw = np.full((len(pts), ND), np.nan)
OVER = []
for i, p in enumerate(pts):
    tag = f"p{p['km']:+05d}"
    base, ca, cb = read(A + tag + '_base.csv'), read(A + tag + '_2026a.csv'), read(A + tag + '_2026b.csv')
    # two servers: the West Coast copy to 28 September, the origin from 19 September; the origin is used from 29 September
    cur = {}
    for c in set(ca) | set(cb):
        da, db = dict(ca.get(c, [])), dict(cb.get(c, []))
        for d in set(da) & set(db): OVER.append(abs(da[d] - db[d]))
        cur[c] = sorted(list(da.items()) + [(d, v) for d, v in db.items() if d > dt.date(2026, 9, 28)])
    acc = np.zeros(ND); n = np.zeros(ND)
    for c in map(tuple, p['cells']):
        if c not in base or c not in cur: continue
        bd = np.array([doy(d) for d, v in base[c]]); bv = np.array([v for d, v in base[c]])
        for d, v in cur[c]:
            k = (d - D0).days
            if not 0 <= k < ND: continue
            dd = np.abs(bd - doy(d)); dd = np.minimum(dd, 365 - dd); sel = dd <= 15
            if sel.sum() < 10: continue
            acc[k] += v - bv[sel].mean(); n[k] += 1
    ok = n >= max(1, len(p['cells']) / 2)
    raw[i, ok] = acc[ok] / n[ok]
def smooth(x, w=15):
    h = w // 2; out = np.full_like(x, np.nan)
    for k in range(h, len(x) - h):
        seg = x[k - h:k + h + 1]; ok = ~np.isnan(seg)
        if ok.sum() >= 0.8 * w: out[k] = seg[ok].mean()
    return out
sm = np.array([smooth(r) for r in raw])
km = np.array([p['km'] for p in pts])
ix = lambda d: (d - D0).days
np.save('/home/agent1/trace/alt_raw.npy', raw); np.save('/home/agent1/trace/alt_smooth.npy', sm)
with open('/home/agent1/trace/alt_anom.csv', 'w') as f:
    f.write("km,lat,lon," + ",".join(str(D0 + dt.timedelta(days=k)) for k in range(ND)) + "\n")
    for i, p in enumerate(pts): f.write(f"{p['km']},{p['lat']},{p['lon']}," + ",".join("" if np.isnan(v) else f"{v:.1f}" for v in raw[i]) + "\n")

print(f"the two servers on the days both hold (19-28 Sep 2026): {len(OVER)} cell-days, mean difference {np.mean(OVER):.3f} cm, largest {np.max(OVER):.3f} cm\n")
print("SATELLITE SEA LEVEL ALONG THE COAST, 2026 minus 2017-2025 for the time of year, 15-day running mean, cm")
print("(rows: distance along the coast from La Libertad, km; columns: date)")
dates = [dt.date(2026, 6, 1) + dt.timedelta(days=10 * k) for k in range(18) if dt.date(2026, 6, 1) + dt.timedelta(days=10 * k) <= dt.date(2026, 11, 18)]
print("    km    lat " + "".join(f"{d.strftime('%d%b'):>6}" for d in dates))
for i, p in enumerate(pts):
    if p['km'] % 400 == 0 or p['km'] in (-1200, 6800, 8800):
        print(f"{p['km']:6d} {p['lat']:6.1f} " + "".join("     -" if np.isnan(sm[i, ix(d)]) else f"{sm[i, ix(d)]:6.1f}" for d in dates))

def month_mean(i, d0, d1):
    seg = raw[i, ix(d0):ix(d1) + 1]; ok = ~np.isnan(seg)
    return float(seg[ok].mean()) if ok.sum() >= 0.6 * len(seg) else None
print("\nMONTHLY MEANS of the unsmoothed anomaly, cm (November = 1 to 25 November)")
print("    km    lat    Jun    Jul    Aug    Sep    Oct    Nov")
MM = {}
for i, p in enumerate(pts):
    v = [month_mean(i, dt.date(2026, m, 1), dt.date(2026, m + 1, 1) - dt.timedelta(days=1) if m < 11 else D1) for m in range(6, 12)]
    MM[p['km']] = v
    if p['km'] % 200 == 0: print(f"{p['km']:6d} {p['lat']:6.1f} " + " ".join("     -" if x is None else f"{x:6.1f}" for x in v))

def rank(a):
    a = np.asarray(a, float); order = a.argsort(); r = np.empty(len(a)); r[order] = np.arange(len(a))
    for v in np.unique(a): r[a == v] = r[a == v].mean()
    return r
print("\nTHE SEALED LINES")
sel = [i for i in range(len(pts)) if 0 <= km[i] <= 6800]
a, b = ix(dt.date(2026, 8, 1)), ix(D1)
dmax = []
for i in sel:
    seg = sm[i, a:b + 1]; dmax.append(np.nan if np.all(np.isnan(seg)) else a + int(np.nanargmax(seg)))
dmax = np.array(dmax, float); ok = ~np.isnan(dmax)
rho = float(np.corrcoef(rank(km[sel][ok]), rank(dmax[ok]))[0, 1])
print("S1: day of the highest smoothed anomaly (1 Aug - 25 Nov), by distance:")
print("    " + ", ".join(f"{int(km[i])}: {(D0 + dt.timedelta(days=int(d))).strftime('%d %b')}" for i, d in zip(sel, dmax) if km[i] % 400 == 0 and not np.isnan(d)))
print(f"    rank correlation with distance, {int(ok.sum())} points from 0 to 6,800 km: {rho:+.2f}; above +0.5 -> " + ("HELD" if rho > 0.5 else "FAILED"))
ref = np.nanmean(sm[[i for i in range(len(pts)) if km[i] in (0, 100, 200)]], axis=0)
t0, t1 = ix(dt.date(2026, 6, 1)), ix(D1)
def bestlag(x):
    best = None
    for L in range(-20, 61):
        t = np.arange(t0, t1 + 1); j = t + L; okk = (j >= 0) & (j < ND); t, j = t[okk], j[okk]
        u, v = ref[t], x[j]; g = ~np.isnan(u) & ~np.isnan(v)
        if g.sum() < 100: continue
        c = float(np.corrcoef(u[g], v[g])[0, 1])
        if best is None or c > best[0]: best = (c, L)
    return best
lags = [bestlag(sm[i]) for i in sel]
print("S2: lag of best correlation with the anomaly near La Libertad (days; correlation), by distance:")
print("    " + ", ".join(f"{int(km[i])}: {l[1]:+d} ({l[0]:.2f})" for i, l in zip(sel, lags) if l and km[i] % 400 == 0))
x = np.array([km[i] for i, l in zip(sel, lags) if l], float); y = np.array([l[1] for l in lags if l], float)
slope, icpt = np.polyfit(x, y, 1)
speed = (1 / slope) * 1000 / 86400 if slope > 0 else None
print(f"    straight line: lag = {icpt:.1f} + {slope * 1000:.2f} days per 1000 km; speed " + (f"{speed:.2f} m/s" if speed else "undefined (slope not positive)") + " -> " + ("HELD" if speed and 1.5 <= speed <= 4 else "FAILED"))
mex = [MM[k][4] for k in range(4000, 5401, 100) if k in MM and MM[k][4] is not None]; sd = MM[6800][4]
print(f"S3: October: along Mexico (4,000-5,400 km, {len(mex)} points) {np.mean(mex):.1f} cm; off San Diego {sd:.1f} cm -> " + ("HELD" if np.mean(mex) >= sd else "FAILED"))
def steep(i):
    best = None
    for t in range(ix(dt.date(2026, 9, 1)), ix(dt.date(2026, 10, 21)) + 1):
        d = sm[i, t + 10] - sm[i, t]
        if not np.isnan(d) and (best is None or d > best[0]): best = (d, t + 5)
    return best
ic, isd = list(km).index(5400), list(km).index(6800)
sc, ss = steep(ic), steep(isd)
print(f"S4: steepest 10-day rise, 1 Sep - 31 Oct: near Cabo San Lucas {sc[0]:+.1f} cm centred {(D0 + dt.timedelta(days=sc[1])).strftime('%d %b')}; off San Diego {ss[0]:+.1f} cm centred {(D0 + dt.timedelta(days=ss[1])).strftime('%d %b')}; San Diego later by {ss[1] - sc[1]} days -> " + ("HELD" if 2 <= ss[1] - sc[1] <= 12 else "FAILED"))
ll = [(MM[k][3], MM[k][4]) for k in (0, 100, 200)]
s, o = np.mean([v[0] for v in ll]), np.mean([v[1] for v in ll])
print(f"S5: near La Libertad: September {s:.1f} cm, October {o:.1f} cm -> " + ("HELD" if o > s else "FAILED"))
print(f"S6: off San Diego: October {MM[6800][4]:.1f} cm, 1-25 November {MM[6800][5]:.1f} cm; lower by more than 3 -> " + ("HELD" if MM[6800][5] < MM[6800][4] - 3 else "FAILED"))
