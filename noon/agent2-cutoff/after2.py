"""More checks made afterwards, and the per-minute profiles for the figure.   usage: python -I after2.py records.csv profiles.json"""
import sys, csv, json, collections
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import numpy as np
NY = ZoneInfo("America/New_York")
GROUP = lambda c: "astro-ph" if c.startswith("astro-ph.") else c if c in ("hep-th", "hep-ph", "gr-qc", "quant-ph", "cs.CL") else "maths" if c in ("math.CO", "math.AP") else None
ORDER = ["astro-ph", "hep-th", "hep-ph", "gr-qc", "quant-ph", "maths", "cs.CL"]; W = []
for r in csv.DictReader(open(sys.argv[1])):
    g = GROUP(r["primary"])
    if g is None: continue
    u = datetime.strptime(r["published"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    if not (datetime(2025, 1, 1, tzinfo=timezone.utc) <= u < datetime(2025, 7, 1, tzinfo=timezone.utc)): continue
    e = u.astimezone(NY)
    if e.weekday() < 5: W.append((g, (e.hour - 14) * 3600 + e.minute * 60 + e.second, e.date(), e.month))
prof = {}
print("H. The last minute before the cutoff and the first minute after, as shares of each group's weekday papers (a level day: 0.07% a minute)")
for g in ORDER:
    s = np.array([r[1] for r in W if r[0] == g]); n = len(s); lm = int(((s >= -60) & (s < 0)).sum()); fm = int(((s >= 0) & (s < 60)).sum()); l5 = int(((s >= -5) & (s < 0)).sum()); f5 = int(((s >= 0) & (s < 5)).sum()); l2 = int(((s >= -2) & (s < 0)).sum())
    prof[g] = dict(n=n, per_minute=[int(((s >= 60 * k) & (s < 60 * k + 60)).sum()) for k in range(-60, 60)])
    print(f"   {g:10s} last minute {lm:4d} ({100 * lm / n:.2f}%); first minute {fm:5d} ({100 * fm / n:.2f}%); last five seconds {l5:3d}, of them the last two {l2:3d}; first five seconds {f5:4d}")
print("I. Day by day: on how many weekdays were there more papers in the ten minutes after than in the ten before?")
for g in ORDER:
    a = collections.Counter(); b = collections.Counter(); days = set()
    for gg, s, d, m in W:
        if gg == g:
            days.add(d); a[d] += (0 <= s < 600); b[d] += (-600 <= s < 0)
    more = sum(a[d] > b[d] for d in days); less = sum(a[d] < b[d] for d in days); print(f"   {g:10s} more after on {more:3d} days, more before on {less:3d}, equal on {len(days) - more - less:3d} (of {len(days)})")
print("J. The rush before the cutoff, month by month (papers 13:50-13:59 / papers 13:00-13:09)")
for g in ORDER:
    out = []
    for m in range(1, 7):
        s = np.array([r[1] for r in W if r[0] == g and r[3] == m]); out.append(f"{int(((s >= -600) & (s < 0)).sum())}/{int(((s >= -3600) & (s < -3000)).sum())}")
    print(f"   {g:10s} " + "  ".join(out))
print("K. cs.CL: is the rush a few days? Papers in 13:50-13:59 by day")
c = collections.Counter(); days = set()
for g, s, d, m in W:
    if g == "cs.CL": days.add(d); c[d] += (-600 <= s < 0)
v = np.array(sorted(c[d] for d in days)); top = sorted(days, key=lambda d: -c[d])[:5]
print(f"   {len(v)} weekdays; median {np.median(v):.0f} a day; days with none {int((v == 0).sum())}; the five busiest: " + ", ".join(f"{d} ({c[d]})" for d in top) + f"; without those five: {int(v[:-5].sum())} papers")
print("L. Another yardstick for the rush: the ten minutes before the cutoff against the mean of the six ten-minute spans from 12:00 to 12:59")
for g in ORDER:
    s = np.array([r[1] for r in W if r[0] == g]); b = int(((s >= -600) & (s < 0)).sum()); noon = int(((s >= -7200) & (s < -3600)).sum()) / 6; print(f"   {g:10s} {b:4d} against {noon:6.1f}: {b / noon:.2f}")
json.dump(prof, open(sys.argv[2], "w"))
print("M. Is 14:00 the only hour with a pile? Papers in the first minute of each Eastern hour, five physics groups together, weekdays (and the minute before each hour)")
phys = [r for r in W if r[0] in ("astro-ph", "hep-th", "hep-ph", "gr-qc", "quant-ph")]; s = np.array([r[1] for r in phys]) + 14 * 3600
print("   first minute: " + " ".join(f"{h}:{int(((s >= 3600 * h) & (s < 3600 * h + 60)).sum())}" for h in range(24)))
print("   last minute:  " + " ".join(f"{h}:{int(((s >= 3600 * h - 60) & (s < 3600 * h)).sum())}" for h in range(1, 24)))
