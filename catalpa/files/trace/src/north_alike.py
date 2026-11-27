# After the ninth reading (check/check-trace-9.md), my own recomputation of its points. Not sealed.
#  A. 2026 put through what the eighteen are put through (anchored from the list's day, not from a day set by hand),
#     and the eighteen put through what 2026 was (anchored from the first day of each run).
#  B. Made-up rises: a clean step added to quiet records and sent north at 440 km a day. How often does each way of
#     timing call it "north in order"?
#  C. A third way with a search that favours neither direction: each gauge's correlation with San Diego at every shift
#     from 120 hours before to 120 after, averaged over the eighteen.
#  D. On all days: San Francisco against San Diego at shifts before as well as after.
#  E. Who chooses the days: the list's rule applied at San Francisco.
# Run: ~/ipd/.venv/bin/python -I src/north_alike.py > north_alike.out
import sys, io, contextlib, importlib.util, csv, datetime as dt
import numpy as np
def load(name):
    spec = importlib.util.spec_from_file_location(name, f'/home/agent1/trace/src/{name}.py'); m = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(m)
    return m
LG = load('north_lag'); H = LG.H; N = load('north'); R = H.R; CO = R.CO; W = H.W; KM = H.KM; ST = H.ST
def anchor_at(y, i0, end=24):
    # San Diego's halfway hour between the means of days -10..-4 and +1..+5 round the day whose 00:00 is hour i0
    b = y[i0 - 240:i0 - 72]; a = y[i0 + 24:i0 + 144]
    if np.isnan(b).mean() > 0.2 or np.isnan(a).mean() > 0.2: return None, None
    B, A = np.nanmean(b), np.nanmean(a); k = H.cross(y, (A + B) / 2, i0 - 72, i0 + end)
    return k, (k == i0 - 72)
def kind1(Y, k, floor=5.0):
    rows = H.single(Y, (k // 24) * 24)
    ok = [(KM[i], r[1]) for i, r in enumerate(rows[:10]) if r and r[1] is not None and not r[2] and r[0] >= floor]
    if len(ok) < 5: return None, None, None, len(ok), rows
    s, sc = H.line([o[0] for o in ok], [o[1] for o in ok]); sp = 24 / s if s > 0 else None
    return ("no order" if sc > 10 else ("north in order" if sp and 150 <= sp <= 1000 else "at once")), sp, sc, len(ok), rows
def kind2(Y, k):
    out, n, s1000, sc, kind = LG.event(Y, k); return kind, (24000 / s1000 if s1000 and s1000 > 0 else None), sc, n, s1000
def show(tag, Y, k, edge=False):
    c1, sp1, sc1, n1, rows = kind1(Y, k); c2, sp2, sc2, n2, s1000 = kind2(Y, k)
    f = lambda c, sp, sc, n: f"{n:2d} gauges, " + ("too few" if c is None else (f"{sp:5.0f} km/day" if sp else "not northward") + f", scatter {sc:4.1f} h: {c}")
    print(f"   {tag:<34} first way: {f(c1, sp1, sc1, n1):<52} second way: {f(c2, sp2, sc2, n2)}" + ("   (San Diego already past halfway when the search began)" if edge else ""))
    return c1, c2, rows
print("A. LIKE AGAINST LIKE")
Y26 = H.Y26; i = lambda d: (d - dt.date(2026, 9, 1)).days * 24
print("   2026 (its run of days with a sum of 10 cm or more, as measured: 27 September to 7 October; largest day 5 October)")
show("anchored by hand, 28 Sep 16:00", Y26, i(dt.date(2026, 9, 28)) + 16)
k, e = anchor_at(Y26[0], i(dt.date(2026, 10, 5))); c1, c2, rows26 = show(f"from its largest day (list's rule)", Y26, k, e); t26 = dt.datetime(2026, 9, 1) + dt.timedelta(hours=k)
print(f"      anchor found: {t26:%d %b %H:%M}; sizes by the eighteen's rule (San Diego, Los Angeles, Port San Luis, San Francisco, Humboldt Bay): " + ", ".join(f"{rows26[j][0]:.1f}" for j in (0, 2, 4, 6, 9)))
print("   (from the first day of a run the search for San Diego's hour is carried two days further, to day +3, for 2026 and the eighteen alike: in 2026 the rise came on the day after the first day)")
k, e = anchor_at(Y26[0], i(dt.date(2026, 9, 27)), 72); show("from the first day of its run", Y26, k, e); print(f"      anchor found: {dt.datetime(2026, 9, 1) + dt.timedelta(hours=k):%d %b %H:%M}")
for d in (dt.date(2026, 10, 3), dt.date(2026, 10, 4), dt.date(2026, 10, 6)):
    k, e = anchor_at(Y26[0], i(d)); show(f"from {d:%d %b}", Y26, k, e)
# the first day of each of the eighteen runs
first = {}
for y in range(1950, 2026):
    vals = []; day = dt.date(y, 8, 1)
    while day <= dt.date(y, 10, 31):
        m = CO.measure(R.a, day)
        if m is not None and m[0] >= 10: vals.append((day, m[0]))
        day += dt.timedelta(days=1)
    rr = []
    for v in vals:
        if rr and (v[0] - rr[-1][-1][0]).days < 12: rr[-1].append(v)
        else: rr.append([v])
    for r in rr: first[max(r, key=lambda v: v[1])[0]] = r[0][0]
print("   the eighteen, from the list's day (as on the page) and from the first day of each run (as 2026 was)")
tally = {"list": [], "first": []}; sizes_list = []
for ev in H.EV:
    D = ev["D"]; F = first[D]; j = (D - F).days
    cA1, cA2, rowsA = show(f"{D} list's day", ev["Y"], ev["k"], ev["edge"]); tally["list"].append((cA1, cA2)); sizes_list.append([None if r is None else r[0] for r in rowsA])
    k, e = anchor_at(ev["Y"][0], H.hh(-j), 72)
    if k is None: print(f"   {D} first day {F}: no anchor"); tally["first"].append((None, None)); continue
    cB1, cB2, rowsB = show(f"{D} first day ({j} d earlier)", ev["Y"], k, e); tally["first"].append((cB1, cB2))
for tag in ("list", "first"):
    t = tally[tag]
    print(f"   anchored from the {'list' if tag == 'list' else 'first'} day: first way north in order {sum(1 for a, b in t if a == 'north in order')}, second way {sum(1 for a, b in t if b == 'north in order')}, both {sum(1 for a, b in t if a == 'north in order' and b == 'north in order')}")
s26 = [rows26[j][0] for j in range(10)]
for j, nm in ((6, "San Francisco"), (9, "Humboldt Bay")):
    v = [s[j] for s in sizes_list if s[j] is not None]; sh = [s[j] / s[0] for s in sizes_list if s[j] is not None]
    print(f"   {nm}: 2026 by the eighteen's rule {s26[j]:.1f} cm ({s26[j] / s26[0]:.2f} of San Diego's {s26[0]:.1f}); larger among the eighteen: {sum(1 for x in v if x > s26[j])} of {len(v)}; as large a share or larger: {sum(1 for x in sh if x >= s26[j] / s26[0])} of {len(sh)}")
# ---------------- B
print("\nB. MADE-UP RISES in the records of 2026 before the season (hourly heights, ten gauges)")
def raw(sid):
    t0 = dt.datetime(2026, 1, 1); n = 24 * 304; x = np.full(n, np.nan)
    for r in csv.reader(open(f'/home/agent1/trace/data/coops/h{sid}.csv')):
        try: t = dt.datetime.strptime(r[0], '%Y-%m-%d %H:%M'); v = float(r[1])
        except (ValueError, IndexError): continue
        kk = int((t - t0).total_seconds() // 3600)
        if 0 <= kk < n: x[kk] = v * 100
    return x
RAW = [raw(sid) for sid, *_ in ST[:10]]
avg_sizes = [float(np.nanmean([s[j] for s in sizes_list if s[j] is not None])) for j in range(10)]
sz26 = [13.4, 13.7, 11.3, 10.6, 8.6, 8.5, 8.1, 8.7, 8.8, 5.1]
print("   sizes added, the eighteen's mean at each gauge: " + ", ".join(f"{v:.1f}" for v in avg_sizes) + "; and this year's first step: " + ", ".join(f"{v:.1f}" for v in sz26))
hr = lambda m, d: int((dt.datetime(2026, m, d) - dt.datetime(2026, 1, 1)).total_seconds() // 3600) + 12
SETS = (("February to August, three a month", [hr(m, d) for m in (2, 3, 4, 5, 6, 7, 8) for d in (5, 15, 25)]), ("May to August, every fifth day", [hr(5, 12) + 120 * q for q in range(21)]))
def trial(t0, sizes, speed):
    Y = []
    for g in range(10):
        x = RAW[g].copy()
        if sizes is not None:
            arr = t0 + (KM[g] / speed * 24 if speed else 0.0); tt = np.arange(len(x)); x = x + sizes[g] * np.clip((tt - arr) / 24 + 0.5, 0, 1)
        Y.append(W.godin(H.fill_short(x)))
    return kind1(Y, t0)[0], kind2(Y, t0)[0]
for setname, starts in SETS:
    print(f"   trials begun in {setname} ({len(starts)}):")
    for tag, sizes, speed in (("nothing added", None, None), ("the eighteen's mean sizes, all gauges at once", avg_sizes, None), ("the eighteen's mean sizes, north at 440 km/day", avg_sizes, 440.0), ("this year's sizes, north at 440 km/day", sz26, 440.0), ("the eighteen's mean sizes, north at 250 km/day", avg_sizes, 250.0)):
        res = [trial(t0, sizes, speed) for t0 in starts]
        print(f"   {tag:<48} {len(res)} trials: 'north in order' by the first way {sum(1 for a, b in res if a == 'north in order'):2d}, by the second {sum(1 for a, b in res if b == 'north in order'):2d}, by both {sum(1 for a, b in res if a == 'north in order' and b == 'north in order'):2d}; no line at all by the first way {sum(1 for a, b in res if a is None):2d}")
# ---------------- C
print("\nC. A THIRD WAY: correlation with San Diego at every shift from -120 to +120 hours, over the window from 6 days before San Diego's hour to 10 after, averaged over the rises; the best shift is the delay")
SH = np.arange(-120, 121)
def chg(y):
    d = np.full(len(y), np.nan); d[12:-12] = y[24:] - y[:-24]; return d
def rcurve(Y, k, g, f):
    x = f(Y[0]); y = f(Y[g]); w0, w1 = k - 144, k + 240; a = x[w0:w1]; out = np.full(len(SH), np.nan)
    if np.isnan(a).mean() > 0.05: return out
    for n_, L_ in enumerate(SH):
        if w0 + L_ < 0 or w1 + L_ > len(y): continue
        b = y[w0 + L_:w1 + L_]; ok = ~np.isnan(a) & ~np.isnan(b)
        if ok.mean() >= 0.95: out[n_] = np.corrcoef(a[ok], b[ok])[0, 1]
    return out
rng = np.random.default_rng(20261127)
for tag, f in (("levels", lambda y: y), ("change over 24 hours", chg)):
    print(f"   {tag}: delay in hours of the averaged correlation (5th to 95th of 400 redraws of the rises); 2026 anchored by hand on 28 Sep; 2026 anchored from its list day")
    for g in (1, 2, 4, 5, 6, 7, 8, 9, 10):
        C = np.array([rcurve(ev["Y"], ev["k"], g, f) for ev in H.EV if ev["Y"][g] is not None]); C = C[~np.isnan(C).all(axis=1)]
        if len(C) < 5: continue
        best = SH[int(np.nanargmax(np.nanmean(C, axis=0)))]; bs = [SH[int(np.nanargmax(np.nanmean(C[rng.integers(0, len(C), len(C))], axis=0)))] for _ in range(400)]
        if g < 10:
            a26 = SH[int(np.nanargmax(rcurve(Y26, i(dt.date(2026, 9, 28)) + 16, g, f)))]; b26 = SH[int(np.nanargmax(rcurve(Y26, int((t26 - dt.datetime(2026, 9, 1)).total_seconds() // 3600), g, f)))]
        print(f"      {ST[g][1]:<14} {KM[g]:5.0f} km: {len(C):2d} rises, {best:+4d} ({np.percentile(bs, 5):+.0f} to {np.percentile(bs, 95):+.0f})" + (f"; 2026: {a26:+d}; {b26:+d}" if g < 10 else ""))
# ---------------- D
print("\nD. ALL DAYS of August-October 1950-2025: the list's sum at San Francisco on day t + shift against San Diego's on day t; and the daily height less its own 15-day mean")
days = [dt.date(y, 8, 1) + dt.timedelta(days=k) for y in range(1950, 2026) for k in range(92)]
def dev(name, d):
    S = N.S[name]
    if d not in S: return None
    v = [S[d + dt.timedelta(days=k)] for k in range(-7, 8) if (d + dt.timedelta(days=k)) in S]
    return S[d] - float(np.mean(v)) if len(v) >= 12 else None
for name in ("San Francisco", "Crescent City"):
    for tag, fn in (("the list's sum", N.summ), ("height less 15-day mean", dev)):
        out = []
        for Ls in (-4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6):
            p = [(fn("San Diego", d), fn(name, d + dt.timedelta(days=Ls))) for d in days]; p = np.array([q for q in p if q[0] is not None and q[1] is not None])
            out.append(f"{Ls:+d}: {np.corrcoef(p[:, 0], p[:, 1])[0, 1]:.2f}")
        print(f"   {name:<14} {tag:<24} " + "  ".join(out))
# ---------------- E
print("\nE. WHO CHOOSES THE DAYS: the list's rule (10 cm or more, the largest day of each run, August-October 1950-2025) applied at San Francisco")
evs = []
for y in range(1950, 2026):
    vals = []; day = dt.date(y, 8, 1)
    while day <= dt.date(y, 10, 31):
        m = N.summ("San Francisco", day)
        if m is not None and m >= 10: vals.append((day, m))
        day += dt.timedelta(days=1)
    rr = []
    for v in vals:
        if rr and (v[0] - rr[-1][-1][0]).days < 12: rr[-1].append(v)
        else: rr.append([v])
    for r in rr: evs.append(max(r, key=lambda v: v[1]))
same = [(N.summ("San Diego", d), m) for d, m in evs]; same = [(a, b) for a, b in same if a is not None]
bestn = []
for d, m in evs:
    v = [x for x in (N.summ("San Diego", d + dt.timedelta(days=L_)) for L_ in range(-4, 5)) if x is not None]
    if v: bestn.append((max(v), m))
print(f"   {len(evs)} rises at San Francisco; San Diego's sum on the same day as a share of San Francisco's: middle {np.median([a / b for a, b in same]):.2f}; taking San Diego's largest of the nine days round it: middle {np.median([a / b for a, b in bestn]):.2f}")
print(f"   (chosen at San Diego, the eighteen: San Francisco's share on the same day, middle {np.median([N.summ('San Francisco', e[0]) / e[1] for e in R.events if N.summ('San Francisco', e[0]) is not None]):.2f})")
