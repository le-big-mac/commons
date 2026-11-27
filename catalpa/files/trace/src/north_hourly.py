# The eighteen quick rises at San Diego (rises.out), timed gauge by gauge up California from NOAA's hourly heights,
# singly by the rule used for 2026 and all together as one averaged rise. Rules fixed in expectations-8.md before
# this was run. Run: ~/ipd/.venv/bin/python -I src/north_hourly.py > north_hourly.out
import sys, io, contextlib, importlib.util, csv, datetime as dt
import numpy as np
def load(name):
    spec = importlib.util.spec_from_file_location(name, f'/home/agent1/trace/src/{name}.py'); m = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(m)
    return m
W = load('wave'); R = load('rises'); gc = load('coastline').gc
EVD = '/home/agent1/trace/data/coops/ev/'
ST = W.ST[:11]                                   # San Diego ... North Spit (Humboldt Bay), Crescent City
KM = [0.0]
for (s0, n0, la0, lo0), (s1, n1, la1, lo1) in zip(ST[:-1], ST[1:]): KM.append(KM[-1] + gc((la0, lo0), (la1, lo1)))
NH = 56 * 24                                     # each file: day D - 30 to D + 25
def hh(off): return (30 + off) * 24              # hour index of 00:00 UTC on day D + off
def fill_short(x, most=3):
    # straight-line fill of gaps of up to three hours, so that one lost hour does not cost 71 in the filter
    x = x.copy(); n = len(x); k = 0
    while k < n:
        if np.isnan(x[k]):
            j = k
            while j < n and np.isnan(x[j]): j += 1
            if 0 < k and j < n and j - k <= most: x[k:j] = np.interp(np.arange(k, j), [k - 1, j], [x[k - 1], x[j]])
            k = j
        else: k += 1
    return x
def series(sid, D):
    t0 = dt.datetime(D.year, D.month, D.day) - dt.timedelta(days=30); x = np.full(NH, np.nan)
    try: rows = list(csv.reader(open(EVD + f'h{sid}_{D}.csv')))
    except FileNotFoundError: return None
    for r in rows:
        try: t = dt.datetime.strptime(r[0], '%Y-%m-%d %H:%M'); v = float(r[1])
        except (ValueError, IndexError): continue
        k = int((t - t0).total_seconds() // 3600)
        if 0 <= k < NH: x[k] = v * 100
    if np.isnan(x).mean() > 0.5: return None
    return W.godin(fill_short(x))
def cross(y, half, s0, s1):
    for k in range(s0, s1):
        seg = y[k:k + 12]
        if not np.isnan(seg).any() and (seg >= half).all(): return k
    return None
def anchor(y, D):
    # San Diego's own halfway hour between the list's two windows: days D-10..D-4 and D+1..D+5
    b = y[hh(-10):hh(-3)]; a = y[hh(1):hh(6)]
    if np.isnan(b).mean() > 0.2 or np.isnan(a).mean() > 0.2: return None, None, None
    B, A = np.nanmean(b), np.nanmean(a); k = cross(y, (A + B) / 2, hh(-3), hh(1))
    return k, A - B, (k == hh(-3))
def single(Y, h0):
    # the rule used for 2026 (older.py): before = days D*-8..D*-2, after = days D*+3..D*+7, first hour from D*-2 past halfway and held 12 h
    b0, b1, a0, a1, s0, s1 = h0 - 8 * 24, h0 - 24, h0 + 3 * 24, h0 + 8 * 24, h0 - 2 * 24, h0 + 8 * 24
    rows = []
    for y in Y:
        if y is None or np.isnan(y[b0:a1]).mean() > 0.2: rows.append(None); continue
        B, A = np.nanmean(y[b0:b1]), np.nanmean(y[a0:a1]); k = cross(y, B + (A - B) / 2, s0, s1) if A - B >= 5 else None
        rows.append((A - B, k, k == s0))
    return rows
def line(km, t):
    if len(km) < 2: return None, None
    s, c = np.polyfit(np.array(km), np.array(t, float), 1); return s, float(np.std(np.array(t) - (c + s * np.array(km))))
def speed(s): return 24 / s if s and s > 0 else None
# ---- 2026 through the same function, as a check (wave.out gives 440 km/day)
Y26 = [W.filt(sid) for sid, *_ in ST[:10]]; r26 = single(Y26, 27 * 24)
ok = [(KM[i], r[1]) for i, r in enumerate(r26) if r and r[1] is not None and not r[2]]
s26, sc26 = line([o[0] for o in ok], [o[1] for o in ok])
print(f"CHECK, 2026 through this script's rule (D* = 28 September): {len(ok)} gauges, {speed(s26):.0f} km/day, scatter {sc26:.1f} hours (wave.out and older.out: 440)")
# ---- each of the eighteen
print("\nEACH OF THE EIGHTEEN, SINGLY (hours after San Diego at which each gauge passed halfway; '.' under 5 cm, 'e' already past halfway when the search began, '-' no record)")
print(f"  {'day D':<11} {'San Diego halfway':<18} " + " ".join(f"{n[:5]:>5}" for s, n, *_ in ST) + "   timed  km/day  scatter h")
EV = []
for e in R.events:
    D = e[0]; Y = [series(sid, D) for sid, *_ in ST]
    if Y[0] is None: print(f"  {D}  no hourly record at San Diego"); continue
    k, rise, edge = anchor(Y[0], D)
    if k is None: print(f"  {D}  San Diego's halfway hour not found (rise by the hourly record {rise if rise is None else round(rise, 1)})"); continue
    t0 = dt.datetime(D.year, D.month, D.day) - dt.timedelta(days=30); tstar = t0 + dt.timedelta(hours=k); h0 = (k // 24) * 24
    rows = single(Y, h0); ref = rows[0][1] if rows[0] and rows[0][1] is not None else None
    cells = []
    for r in rows:
        if r is None: cells.append("    -")
        elif r[1] is None: cells.append("    .")
        elif r[2]: cells.append("    e")
        else: cells.append(f"{r[1] - ref:5d}" if ref is not None else f"{r[1] - k:5d}")
    ok = [(KM[i], r[1]) for i, r in enumerate(rows[:10]) if r and r[1] is not None and not r[2]]
    s, sc = line([o[0] for o in ok], [o[1] for o in ok]) if len(ok) >= 5 else (None, None)
    sp = speed(s)
    cls = None if len(ok) < 5 else ("travelled" if sp and 150 <= sp <= 1000 else "together or out of order")
    print(f"  {D}  {tstar.strftime('%d %b %H:%M'):<18} " + " ".join(cells) + f"   {len(ok):5d}  " + (f"{sp:6.0f}" if sp else ("     -" if s is None else "  none")) + (f"  {sc:6.1f}" if sc is not None else "") + ("  (anchor at the edge)" if edge else ""))
    EV.append(dict(D=D, k=k, edge=edge, Y=Y, cls=cls, sp=sp, hur=bool(R.near(D, 64))))
timed = [e for e in EV if e["cls"]]
print(f"\n  singly timed (five or more of the ten gauges to Humboldt Bay): {len(timed)} of {len(EV)}; of these, northward at 150 to 1000 km/day: {sum(1 for e in timed if e['cls'] == 'travelled')}; speeds: " + ", ".join(f"{e['sp']:.0f}" if e['sp'] else "none" for e in timed))
# ---- all together: the averaged rise, lined up on San Diego's halfway hour
TAU = np.arange(-10 * 24, 12 * 24 + 1)
def curves(events):
    out = []
    for i in range(len(ST)):
        xs = []
        for e in events:
            y = e["Y"][i]
            if y is None: continue
            seg = y[e["k"] + TAU[0]: e["k"] + TAU[-1] + 1]; base = y[e["k"] - 8 * 24: e["k"] - 2 * 24]
            if np.isnan(seg).mean() > 0.1 or np.isnan(base).mean() > 0.2: continue
            xs.append(seg - np.nanmean(base))
        out.append((len(xs), np.nanmean(np.array(xs), axis=0) if xs else None))
    return out
def timing(c):
    z = int(np.where(TAU == 0)[0][0]); A = float(np.nanmean(c[z + 3 * 24: z + 8 * 24]))
    k = cross(c, A / 2, z - 2 * 24, z + 8 * 24) if A >= 3 else None
    steep = max(range(z - 3 * 24, z + 8 * 24), key=lambda j: c[j + 12] - c[j - 12])
    return A, (None if k is None else k - z), steep - z
def fit(cv, upto=10):
    pts = [(KM[i], timing(c)[1]) for i, (n, c) in enumerate(cv[:upto]) if c is not None and timing(c)[1] is not None]
    if len(pts) < 6: return len(pts), None
    s, sc = line([p[0] for p in pts], [p[1] for p in pts]); return len(pts), s
good = [e for e in EV if not e["edge"]]
cv = curves(good)
print(f"\nALL TOGETHER: the mean of {len(good)} rises lined up on San Diego's halfway hour (those anchored at the edge left out: {len(EV) - len(good)})")
print(f"  {'gauge':<14} {'km':>5} {'rises':>5} {'rise cm':>8} {'halfway, h after San Diego':>27} {'steepest 24 h, h':>17}   level at days -5, -2, 0, +1, +2, +3, +5, +8, +11")
tt = []
for i, (sid, name, la, lo) in enumerate(ST):
    n, c = cv[i]
    if c is None: print(f"  {name:<14} {KM[i]:5.0f}   no record"); tt.append(None); continue
    A, k, st = timing(c); tt.append((A, k, st)); z = 10 * 24
    print(f"  {name:<14} {KM[i]:5.0f} {n:5d} {A:8.1f} {('under 3 cm' if k is None else str(k)):>27} {st:17d}   " + " ".join(f"{c[z + d * 24]:+5.1f}" for d in (-5, -2, 0, 1, 2, 3, 5, 8, 11)))
ref = tt[0][1]
npts, s = fit(cv)
print(f"  line through the halfway hours, San Diego to Humboldt Bay: {npts} gauges; " + ("no line" if s is None else (f"{s * 1000:.1f} hours per 1000 km = {speed(s):.0f} km/day" if s > 0 else f"{s * 1000:.1f} hours per 1000 km (not northward)")))
pts2 = [(KM[i], t[2]) for i, t in enumerate(tt[:10]) if t is not None and t[0] >= 3]
s2, sc2 = line([p[0] for p in pts2], [p[1] for p in pts2])
print(f"  line through the hours of steepest rise ({len(pts2)} gauges): {s2 * 1000:.1f} hours per 1000 km" + (f" = {speed(s2):.0f} km/day" if s2 > 0 else " (not northward)"))
rng = np.random.default_rng(20261127); sp = []; none = 0; NB = 1000
for b in range(NB):
    pick = [good[j] for j in rng.integers(0, len(good), len(good))]; n_, s_ = fit(curves(pick))
    if s_ is None or s_ <= 0: none += 1
    else: sp.append(24 / s_)
sp = np.array(sp)
print(f"  drawing the {len(good)} rises afresh {NB} times (with repeats): no northward line in {none}; otherwise km/day 5th, 50th, 95th of the draws: " + (", ".join(f"{np.percentile(sp, q):.0f}" for q in (5, 50, 95)) if len(sp) else "-") + f"; share of all draws between 250 and 700: {100 * np.sum((sp >= 250) & (sp <= 700)) / NB:.0f}%; under 250: {100 * np.sum(sp < 250) / NB:.0f}%")
for tag, sub in (("with a hurricane near", [e for e in good if e["hur"]]), ("without", [e for e in good if not e["hur"]])):
    c2 = curves(sub); n2, s_ = fit(c2); A7 = timing(c2[6][1])[0] if c2[6][1] is not None else float('nan')
    print(f"  {tag} ({len(sub)}): San Francisco's rise {A7:.1f} cm; line: " + ("none" if s_ is None else (f"{speed(s_):.0f} km/day" if s_ > 0 else "not northward")) + f" ({n2} gauges)")
# ---- the lines of expectations-8.md
print("\nTHE LINES OF expectations-8.md")
first7 = [t for t in tt[:7]]
p1 = all(t is not None and t[0] >= 3 for t in first7)
print("P1 (the averaged rise is 3 cm or more at each of the seven gauges from San Diego to San Francisco): " + ", ".join("-" if t is None else f"{t[0]:.1f}" for t in first7) + " -> " + ("HELD" if p1 else "FAILED"))
sf = tt[6]; d = None if sf is None or sf[1] is None or ref is None else sf[1] - ref
print(f"P2 (the averaged rise passes halfway at San Francisco 12 hours or more after San Diego): " + ("not timed" if d is None else f"{d} hours") + " -> " + ("HELD" if d is not None and d >= 12 else "FAILED"))
v = speed(s) if s is not None else None
print("P3 (line through six or more gauges, northward at 250 to 700 km/day): " + ("no northward line" if v is None else f"{v:.0f} km/day, {npts} gauges") + " -> " + ("HELD" if v is not None and 250 <= v <= 700 else "FAILED"))
print("P4 (the same line, northward and slower than 250 km/day): " + ("HELD" if v is not None and v < 250 else "FAILED"))
nt = len(timed); ng = sum(1 for e in timed if e["cls"] == "travelled")
print(f"P5 (of the rises timed singly, at least half northward at 150 to 1000 km/day): {ng} of {nt} -> " + ("HELD" if nt > 0 and ng >= nt / 2 else "FAILED"))
