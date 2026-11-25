"""Do authors time their arXiv submissions to the daily cutoff?   usage: python -I cutoff.py records.csv results.json"""
import sys, csv, json
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import numpy as np
NY = ZoneInfo("America/New_York")
GROUP = lambda c: "astro-ph" if c.startswith("astro-ph.") else c if c in ("hep-th", "hep-ph", "gr-qc", "quant-ph", "cs.CL") else "maths" if c in ("math.CO", "math.AP") else None
ORDER = ["astro-ph", "hep-th", "hep-ph", "gr-qc", "quant-ph", "maths", "cs.CL"]
recs = []
for r in csv.DictReader(open(sys.argv[1])):
    g = GROUP(r["primary"])
    if g is None: continue
    u = datetime.strptime(r["published"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    if not (datetime(2025, 1, 1, tzinfo=timezone.utc) <= u < datetime(2025, 7, 1, tzinfo=timezone.utc)): continue
    e = u.astimezone(NY); recs.append((g, u, e, (e.hour - 14) * 3600 + e.minute * 60 + e.second, e.weekday()))
print(f"{len(recs)} papers with a first version from 1 January to 30 June 2025 (API's clock) and a primary category in the seven groups")
out = {}; W = [r for r in recs if r[4] < 5]
print("\n1. Papers on Mondays to Fridays (Eastern time), and the ten minutes either side of 14:00 Eastern")
print("   group       papers   13:00-13:09   13:50-13:59   14:00-14:09   ratio after/before   first 60 s   before / an hour earlier   share of all in 14:00-14:09 (a level day: 0.69%)")
for g in ORDER:
    s = np.array([r[3] for r in W if r[0] == g]); n = len(s); a = int(((s >= 0) & (s < 600)).sum()); b = int(((s >= -600) & (s < 0)).sum()); e = int(((s >= -3600) & (s < -3000)).sum()); f = int(((s >= 0) & (s < 60)).sum())
    out[g] = dict(n=n, after=a, before=b, early=e, first60=f, ratio=a / b if b else None, rush=b / e if e else None)
    print(f"   {g:10s} {n:6d}   {e:6d}        {b:6d}        {a:6d}        {a / b if b else float('nan'):8.2f}           {f:6d}        {b / e if e else float('nan'):8.2f}                 {100 * a / n:.2f}%")
big = max(ORDER, key=lambda g: out[g]["ratio"] or 0); print(f"   largest ratio: {big}")
print("\n2. astro-ph, the first ten minutes after the cutoff, minute by minute: " + ", ".join(str(int(((np.array([r[3] for r in W if r[0] == 'astro-ph']) >= 60 * k) & (np.array([r[3] for r in W if r[0] == 'astro-ph']) < 60 * k + 60)).sum())) for k in range(10)))
sa = np.array([r[3] for r in W if r[0] == "astro-ph"]); print("   and the first minute by tens of seconds: " + ", ".join(str(int(((sa >= 10 * k) & (sa < 10 * k + 10)).sum())) for k in range(6)) + f"; in the very first second: {int((sa == 0).sum())}; in the first five: {int(((sa >= 0) & (sa < 5)).sum())}")
print("\n3. astro-ph, the busiest minute of the day by the API's clock (UTC)")
for name, months in (("January and February", (1, 2)), ("April, May and June", (4, 5, 6)), ("March", (3,))):
    mins = {}
    for g, u, e, s, wd in recs:
        if g == "astro-ph" and u.month in months: mins[(u.hour, u.minute)] = mins.get((u.hour, u.minute), 0) + 1
    top = sorted(mins.items(), key=lambda kv: -kv[1])[:3]; print(f"   {name}: " + "; ".join(f"{h:02d}:{m:02d} ({c} papers)" for (h, m), c in top))
    out["busiest_" + name.split()[0]] = [f"{h:02d}:{m:02d}" for (h, m), c in top]
print("\n4. Day by day: astro-ph papers in 14:00-14:09 Eastern, by day of the week (number of such days in the half-year; papers; a day)")
import collections
days = collections.defaultdict(set); cnt = collections.Counter()
for g, u, e, s, wd in recs:
    if g == "astro-ph": days[wd].add(e.date()); cnt[wd] += (0 <= s < 600)
for wd, nm in enumerate(("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")): print(f"   {nm:9s} {len(days[wd]):3d} days; {cnt[wd]:4d} papers; {cnt[wd] / max(1, len(days[wd])):.1f} a day")
out["records"] = len(recs); json.dump(out, open(sys.argv[2], "w"), indent=1)
