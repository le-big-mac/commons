"""Checks made after the sealed lines were scored; none was registered.   usage: python -I after.py records.csv"""
import sys, csv, collections
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import numpy as np
NY = ZoneInfo("America/New_York")
GROUP = lambda c: "astro-ph" if c.startswith("astro-ph.") else c if c in ("hep-th", "hep-ph", "gr-qc", "quant-ph", "cs.CL") else "maths" if c in ("math.CO", "math.AP") else None
ORDER = ["astro-ph", "hep-th", "hep-ph", "gr-qc", "quant-ph", "maths", "cs.CL"]
recs = []; upd_late = 0; nall = 0
for r in csv.DictReader(open(sys.argv[1])):
    g = GROUP(r["primary"])
    if g is None: continue
    u = datetime.strptime(r["published"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    if not (datetime(2025, 1, 1, tzinfo=timezone.utc) <= u < datetime(2025, 7, 1, tzinfo=timezone.utc)): continue
    e = u.astimezone(NY); recs.append((g, u, e, (e.hour - 14) * 3600 + e.minute * 60 + e.second, e.weekday(), r["primary"], r.get("updated", "")))
W = [r for r in recs if r[4] < 5]
def cnt(rows, lo, hi): s = np.array([r[3] for r in rows]); return int(((s >= lo) & (s < hi)).sum())
print("A. Was every paper of the half-year fetched, or only those not revised since? The latest version's date, by half-year, of the papers in the table")
c = collections.Counter(("2025 first half" if r[6][:7] <= "2025-06" else "2025 second half" if r[6][:4] == "2025" else "2026") for r in recs if r[6]); print("   " + "; ".join(f"{k}: {v}" for k, v in sorted(c.items())) + f"   (papers with a latest-version date: {sum(c.values())} of {len(recs)})")
print("B. Other widths of window either side of 14:00 Eastern (papers after / papers before, weekdays)")
for g in ORDER:
    rows = [r for r in W if r[0] == g]; print(f"   {g:10s} " + "; ".join(f"{w // 60:3d} min: {cnt(rows, 0, w):5d} / {cnt(rows, -w, 0):5d} = {cnt(rows, 0, w) / max(1, cnt(rows, -w, 0)):6.2f}" for w in (60, 300, 600, 1800, 3600)))
print("C. astro-ph by category (ten minutes after / before), and by month")
for sub in ("astro-ph.CO", "astro-ph.EP", "astro-ph.GA", "astro-ph.HE", "astro-ph.IM", "astro-ph.SR"):
    rows = [r for r in W if r[5] == sub]; a, b = cnt(rows, 0, 600), cnt(rows, -600, 0); print(f"   {sub}: {len(rows):5d} papers; {a:4d} / {b:3d} = {a / max(1, b):5.1f}; first 60 s: {cnt(rows, 0, 60)}")
for m in range(1, 7):
    rows = [r for r in W if r[0] == "astro-ph" and r[2].month == m]; a, b = cnt(rows, 0, 600), cnt(rows, -600, 0); print(f"   month {m}: {a:4d} / {b:3d} = {a / max(1, b):5.1f}")
print("D. Is it every day or a few days? astro-ph papers in 14:00:00 to 14:09:59, weekday by weekday")
days = collections.Counter(); alld = set()
for r in W:
    if r[0] == "astro-ph":
        alld.add(r[2].date())
        if 0 <= r[3] < 600: days[r[2].date()] += 1
v = np.array([days[d] for d in sorted(alld)]); print(f"   {len(v)} weekdays with any astro-ph paper; papers in the ten minutes: median {np.median(v):.0f} a day, least {v.min()}, most {v.max()}; days with none: {int((v == 0).sum())}; days with ten or more: {int((v >= 10).sum())}")
first = collections.defaultdict(lambda: 99999)
for r in W:
    if r[0] == "astro-ph" and 0 <= r[3] < 600: first[r[2].date()] = min(first[r[2].date()], r[3])
fs = np.array(sorted(first.values())); print(f"   the first astro-ph paper after the cutoff arrives within 1 second on {int((fs <= 1).sum())} of {len(fs)} such days, within 5 seconds on {int((fs <= 5).sum())}, within 60 on {int((fs <= 60).sum())}")
print("E. The seconds around the cutoff, all seven groups together (papers at each second from 13:59:50 to 14:00:15, weekdays)")
s = np.array([r[3] for r in W]); print("   " + " ".join(f"{k:+d}:{int((s == k).sum())}" for k in range(-10, 16)))
print("F. By day of the week, astro-ph: ten minutes after / before")
for wd, nm in enumerate(("Monday", "Tuesday", "Wednesday", "Thursday", "Friday")):
    rows = [r for r in W if r[0] == "astro-ph" and r[4] == wd]; a, b = cnt(rows, 0, 600), cnt(rows, -600, 0); print(f"   {nm:9s} {a:4d} / {b:3d} = {a / max(1, b):5.1f}")
print("G. The other end of the day: papers in the hour before the cutoff against the hour after, and the day's shape (share of weekday papers by Eastern hour)")
for g in ORDER:
    rows = [r for r in W if r[0] == g]; hours = collections.Counter(r[2].hour for r in rows); n = len(rows); print(f"   {g:10s} " + " ".join(f"{100 * hours[h] / n:4.1f}" for h in range(24)))
print("   (hours 0 to 23, Eastern)")
