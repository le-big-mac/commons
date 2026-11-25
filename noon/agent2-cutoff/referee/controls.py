"""Referee's controls, from rows.pkl made by blind.py. usage: python -I controls.py rows.pkl"""
import sys, pickle, math, random
from collections import Counter, defaultdict
from datetime import date

rows = pickle.load(open(sys.argv[1], "rb"))  # (id, group, cat, utc, et, version, updated)
G = ["astro-ph", "hep-th", "hep-ph", "gr-qc", "quant-ph", "maths", "cs.CL"]
PHYS = G[:5]
sod = lambda d: d.hour * 3600 + d.minute * 60 + d.second
R = [(i, g, c, u, e, sod(e) - 14 * 3600, e.weekday(), e.date()) for i, g, c, u, e, v, up in rows]
W = [r for r in R if r[6] < 5]
by = {g: [r for r in W if r[1] == g] for g in G}
cnt = lambda rs, lo, hi: sum(1 for r in rs if lo <= r[5] < hi)

print("== 0. Edge of the sample: weekday papers by Eastern date outside 1 Jan - 30 Jun")
print("   Eastern date 2024-12-31:", Counter(r[1] for r in W if r[7] == date(2024, 12, 31)))
print("   distinct Eastern weekdays with papers, all groups:", len(set(r[7] for r in W)), " of which in 2025:", len(set(r[7] for r in W if r[7].year == 2025)))

print("\n== 1. Ten-minute spans from 11:00 to 15:00 Eastern, weekdays (| marks 14:00)")
for g in G:
    b = [cnt(by[g], k * 600, k * 600 + 600) for k in range(-18, 6)]
    print(f"   {g:9s}", " ".join(f"{x:4d}" for x in b[:18]), "|", " ".join(f"{x:4d}" for x in b[18:]))
print("   yardsticks for 13:50-13:59: /13:00-13:09 (sealed) | /13:40-13:49 | /mean of 13:00-13:49 | /mean of 12:00-12:59 | /mean of 09:00-12:59 | /busiest other ten-minute span 08:00-13:49 | line fitted to 12:00-13:49 and carried forward (count expected, ratio, z)")
for g in G:
    b = {k: cnt(by[g], k * 600, k * 600 + 600) for k in range(-36, 0)}
    last = b[-1]
    m1349 = sum(b[k] for k in range(-6, -1)) / 5
    m12 = sum(b[k] for k in range(-12, -6)) / 6
    m9 = sum(b[k] for k in range(-30, -6)) / 24
    mx = max(b[k] for k in range(-36, -1))
    xs = list(range(-12, -1)); ys = [b[k] for k in xs]
    n = len(xs); mxx = sum(xs) / n; myy = sum(ys) / n
    sl = sum((x - mxx) * (y - myy) for x, y in zip(xs, ys)) / sum((x - mxx) ** 2 for x in xs)
    pred = myy + sl * (-1 - mxx)
    z = (last - pred) / math.sqrt(max(pred, 1))
    print(f"   {g:9s} {last:4d}: {last / b[-6]:5.2f} | {last / max(1, b[-2]):5.2f} | {last / m1349:5.2f} | {last / m12:5.2f} | {last / m9:5.2f} | {last / mx:5.2f} (max {mx}) | {pred:6.1f} {last / pred:5.2f} z={z:5.1f}")
print("   maths by category:")
for c in ("math.CO", "math.AP"):
    rs = [r for r in by["maths"] if r[2] == c]
    print(f"     {c}: n {len(rs)}; 13:00-09 {cnt(rs, -3600, -3000)}; 13:50-59 {cnt(rs, -600, 0)}; 14:00-09 {cnt(rs, 0, 600)}; hour before {cnt(rs, -3600, 0)}; hour after {cnt(rs, 0, 3600)}")
print("   per-minute, 13:45 to 14:05, maths and cs.CL and gr-qc:")
for g in ("maths", "cs.CL", "gr-qc"):
    print(f"     {g:6s}", " ".join(str(cnt(by[g], k * 60, k * 60 + 60)) for k in range(-15, 0)), "|", " ".join(str(cnt(by[g], k * 60, k * 60 + 60)) for k in range(0, 6)))

print("\n== 2. after/before at many widths (direction)")
ws = [1, 2, 5, 10, 30, 60, 120, 300, 600, 1200, 1800, 3600, 7200, 10800, 14400, 21600]
print("   width(s)  ", " ".join(f"{w:>7d}" for w in ws))
for g in G:
    print(f"   {g:9s} ", " ".join(f"{cnt(by[g], 0, w) / max(1, cnt(by[g], -w, 0)):7.2f}" for w in ws))
print("   which group has the largest ratio at each width:", [max(G, key=lambda g: cnt(by[g], 0, w) / max(1, cnt(by[g], -w, 0))) for w in ws])

print("\n== 3. first-minute share by category; first five seconds; exact second")
for c in sorted(set(r[2] for r in W)):
    rs = [r for r in W if r[2] == c]
    a, b = cnt(rs, 0, 600), cnt(rs, -600, 0)
    f = cnt(rs, 0, 60)
    p = f / len(rs)
    print(f"   {c:12s} n {len(rs):5d} first minute {f:4d} = {100 * p:5.1f}% (+-{100 * math.sqrt(p * (1 - p) / len(rs)):.1f}); ratio10 {a}/{b} = {a / max(1, b):5.2f}; last minute {cnt(rs, -60, 0)}; before/13:00-09 {b}/{cnt(rs, -3600, -3000)}")
for g in G:
    f = cnt(by[g], 0, 60)
    print(f"   {g:9s} first minute {f} ({100 * f / len(by[g]):.2f}% of weekday papers; {100 * f / sum(1 for r in R if r[1] == g):.2f}% of all papers); first 5 s {cnt(by[g], 0, 5)} ({100 * cnt(by[g], 0, 5) / max(1, f):.0f}%); at :00 {cnt(by[g], 0, 1)}; days with a paper at 14:00:00: {len(set(r[7] for r in by[g] if r[5] == 0))}; mean minute 14:01-14:59: {cnt(by[g], 60, 3600) / 59:.1f}; mean minute 14:10-14:59 {cnt(by[g], 600, 3600) / 50:.1f}")
# bootstrap by day: share difference hep-ph - astro-ph, hep-th - astro-ph, in first minute
random.seed(1)
days = sorted(set(r[7] for r in W))
def per_day(g):
    n = Counter(r[7] for r in by[g]); f = Counter(r[7] for r in by[g] if 0 <= r[5] < 60)
    return n, f
pd = {g: per_day(g) for g in G}
def share(g, ds): return sum(pd[g][1][d] for d in ds) / sum(pd[g][0][d] for d in ds)
for a_, b_ in (("hep-ph", "astro-ph"), ("hep-th", "astro-ph"), ("hep-th", "hep-ph"), ("gr-qc", "quant-ph")):
    diffs = []
    for _ in range(4000):
        ds = [random.choice(days) for _ in days]
        diffs.append(share(a_, ds) - share(b_, ds))
    diffs.sort()
    print(f"   first-minute share {a_} minus {b_}: {100 * (share(a_, days) - share(b_, days)):.2f} points; day-bootstrap 95% [{100 * diffs[100]:.2f}, {100 * diffs[3899]:.2f}]; share of resamples <= 0: {sum(d <= 0 for d in diffs) / 4000:.3f}")

print("\n== 4. Machinery? seconds, other hours, weekends, days")
allsec = Counter(r[4].second for r in W if not (-120 <= r[5] < 120))
print("   second-of-minute, weekday papers away from 13:58-14:02: second 00:", allsec[0], " mean of others:", round(sum(v for k, v in allsec.items() if k) / 59, 1), " min/max:", min(allsec.values()), max(allsec.values()))
print("   papers stamped exactly hh:00:00 Eastern, weekdays, all groups, by hour:", " ".join(f"{h}:{sum(1 for r in W if r[5] == (h - 14) * 3600)}" for h in range(24)))
print("   stamped hh:00:00..04 by hour, physics five:", " ".join(f"{h}:{sum(1 for r in W if r[1] in PHYS and 0 <= r[5] - (h - 14) * 3600 < 5)}" for h in range(24)))
WE = [r for r in R if r[6] >= 5]
print("   weekends: papers", len(WE), "; in 14:00:00-14:00:59:", cnt(WE, 0, 60), "; at 14:00:00:", cnt(WE, 0, 1), "; in 13:59:", cnt(WE, -60, 0), "; mean per minute 13:00-14:59:", round(cnt(WE, -3600, 3600) / 120, 2))
print("   weekend first-minute papers:", [(r[0], r[1], r[4].strftime('%a %m-%d %H:%M:%S')) for r in WE if 0 <= r[5] < 60])
print("   seconds 14:00:00..14:00:09 by group:")
for g in G:
    print(f"     {g:9s}", " ".join(str(cnt(by[g], k, k + 1)) for k in range(10)), "  13:59:50..59:", " ".join(str(cnt(by[g], k, k + 1)) for k in range(-10, 0)))
ph = [r for r in W if r[1] in PHYS]
d15 = Counter(r[7] for r in ph if 3600 <= r[5] < 3660)
print("   the 15:00 first minute (physics five):", sum(d15.values()), "papers; by date:", sorted((str(d), n) for d, n in d15.items()))
d13 = Counter(r[7] for r in ph if -3600 <= r[5] < -3540)
print("   the 13:00 first minute (physics five):", sum(d13.values()), "; in 10-28 March:", sum(n for d, n in d13.items() if date(2025, 3, 10) <= d <= date(2025, 3, 28)))
print("   physics five, first minute of 14:00 by date range: 10-28 March:", sum(1 for r in ph if 0 <= r[5] < 60 and date(2025, 3, 10) <= r[7] <= date(2025, 3, 28)), " weekdays in that range: 15")
# days with little pile
for g in ("astro-ph",):
    a = Counter(r[7] for r in by[g] if 0 <= r[5] < 600); b = Counter(r[7] for r in by[g] if -600 <= r[5] < 0); n = Counter(r[7] for r in by[g])
    odd = [(str(d), d.strftime('%a'), n[d], b[d], a[d]) for d in sorted(n) if a[d] <= b[d]]
    print("   astro-ph weekdays with after <= before (date, day, papers, before, after):", odd)
    first = {}
    for r in by[g]:
        if 0 <= r[5] < 600: first[r[7]] = min(first.get(r[7], 9999), r[5])
    print("   astro-ph days with a paper in the ten minutes after:", len(first), "; first within 1 s:", sum(v <= 1 for v in first.values()), "; exceptions:", [(str(d), v) for d, v in first.items() if v > 1])
    low = sorted((a[d], str(d), d.strftime('%a'), n[d]) for d in n)[:6]
    print("   astro-ph six thinnest days for 14:00-14:09:", low)

print("\n== 5. Identifiers against stamps (is 'published' the clock the arXiv cuts batches on?)")
def idnum(i):
    try:
        a, b = i.split("."); return int(a) * 100000 + int(b)
    except Exception: return None
S = sorted((r for r in R if idnum(r[0]) is not None), key=lambda r: r[3])
print("   papers with new-style ids:", len(S), "of", len(R))
inv = sum(1 for x, y in zip(S, S[1:]) if idnum(y[0]) < idnum(x[0]) and y[3] > x[3])
print("   adjacent pairs (sorted by stamp, different stamps) whose identifiers run backwards:", inv, "of", len(S) - 1)
# per weekday: ids of the papers stamped 13:50-13:59:59 vs 14:00:00-14:09:59
okd = bad = 0; nb = 0
for d in sorted(set(r[7] for r in W)):
    be = [idnum(r[0]) for r in W if r[7] == d and -600 <= r[5] < 0]
    af = [idnum(r[0]) for r in W if r[7] == d and 0 <= r[5] < 600]
    if be and af:
        nb += sum(1 for x in be if x > min(af))
        if max(be) < min(af): okd += 1
        else: bad += 1
print(f"   weekdays on which every paper stamped 13:50-13:59 has a smaller identifier than every paper stamped 14:00-14:09: {okd}; not so: {bad}; 'before' papers numbered above the day's lowest 'after' paper: {nb}")
# within the first minute, same day: is id order the stamp order?
conc = disc = 0
for d in sorted(set(r[7] for r in W)):
    fm = sorted(((r[5], idnum(r[0])) for r in W if r[7] == d and 0 <= r[5] < 60))
    for i in range(len(fm)):
        for j in range(i + 1, len(fm)):
            if fm[i][0] < fm[j][0]:
                if fm[i][1] < fm[j][1]: conc += 1
                else: disc += 1
print(f"   pairs of papers in the first minute of the same day with different seconds: identifier order agrees with stamp order in {conc}, disagrees in {disc}")
# gap in identifier across the boundary vs across other seconds: the month prefix
flip = Counter()
for r in W:
    ym_id = r[0].split(".")[0]; ym_pub = r[4].strftime("%y%m")
    if ym_id != ym_pub: flip[(str(r[7]), "before 14:00" if r[5] < 0 else "after 14:00")] += 1
print("   papers whose identifier's month differs from the Eastern month of the stamp, by date and side of 14:00 (top 14):", sorted(flip.items())[:14], "... total", sum(flip.values()))
# first paper after boundary each day: is it the lowest id among that day's after-14:00 and next morning's papers?
print("\n== 6. cs.CL from the first query alone (stamps before 2025-05-30 UTC) and the rest")
for lab, f in (("to 29 May", lambda r: r[3].strftime('%m%d') < "0530"), ("from 30 May", lambda r: r[3].strftime('%m%d') >= "0530")):
    rs = [r for r in by["cs.CL"] if f(r)]
    print(f"   {lab}: n {len(rs)}; 13:00-09 {cnt(rs, -3600, -3000)}; before {cnt(rs, -600, 0)}; after {cnt(rs, 0, 600)}; ratio {cnt(rs, 0, 600) / max(1, cnt(rs, -600, 0)):.2f}; first minute {cnt(rs, 0, 60)}; last minute {cnt(rs, -60, 0)}")

print("\n== 7. Does the step in cs.CL and maths follow the Eastern clock? Hourly counts by UTC hour 16..20, Jan-Feb and Apr-Jun, weekdays")
for g in ("cs.CL", "maths"):
    for lab, ms in (("Jan-Feb", (1, 2)), ("Apr-Jun", (4, 5, 6))):
        c = Counter(r[3].hour for r in by[g] if r[3].month in ms)
        c10 = Counter((r[3].hour, r[3].minute // 10) for r in by[g] if r[3].month in ms)
        print(f"   {g:6s} {lab}: by UTC hour 15..21:", [c[h] for h in range(15, 22)], "; UTC ten-minute spans 17:30-19:29:", [c10[(h, m)] for h in (17, 18, 19) for m in range(6)][3:15])
