"""The referee's controls, redone here.   usage: python -I after3.py records.csv"""
import sys, csv, collections
from datetime import datetime, timezone, date
from zoneinfo import ZoneInfo
import numpy as np
NY = ZoneInfo("America/New_York")
GROUP = lambda c: "astro-ph" if c.startswith("astro-ph.") else c if c in ("hep-th", "hep-ph", "gr-qc", "quant-ph", "cs.CL") else "maths" if c in ("math.CO", "math.AP") else None
ORDER = ["astro-ph", "hep-th", "hep-ph", "gr-qc", "quant-ph", "maths", "cs.CL"]; W = []; ALL = []
for r in csv.DictReader(open(sys.argv[1])):
    g = GROUP(r["primary"])
    if g is None: continue
    u = datetime.strptime(r["published"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    if not (datetime(2025, 1, 1, tzinfo=timezone.utc) <= u < datetime(2025, 7, 1, tzinfo=timezone.utc)): continue
    e = u.astimezone(NY); rec = (g, (e.hour - 14) * 3600 + e.minute * 60 + e.second, e.date(), r["primary"], r["id"], u, e); ALL.append(rec)
    if e.weekday() < 5: W.append(rec)
S = {g: np.array([r[1] for r in W if r[0] == g]) for g in ORDER}
def c(g, lo, hi): return int(((S[g] >= lo) & (S[g] < hi)).sum())
print("1. Is the ten minutes before the boundary busier than a usual ten minutes of that morning? Papers in each ten-minute span from 12:00 to 13:59 Eastern")
for g in ORDER:
    spans = [c(g, -7200 + 600 * k, -7200 + 600 * k + 600) for k in range(12)]; x = np.arange(11); fit = np.polyfit(x, spans[:11], 1); pred = float(np.polyval(fit, 11))
    print(f"   {g:10s} " + " ".join(f"{v:3d}" for v in spans) + f"   mean of the first eleven {np.mean(spans[:11]):5.1f}; a straight line through them carried on gives {pred:5.1f}; seen {spans[11]}: {spans[11] / pred:.1f} times, {(spans[11] - pred) / max(pred, 1) ** 0.5:+.1f} standard deviations")
print("   maths by quarter, 13:50-13:59 against 13:00-13:09: " + "; ".join(f"{nm}: {int(sum(1 for r in W if r[0] == 'maths' and r[6].month in ms and -600 <= r[1] < 0))} against {int(sum(1 for r in W if r[0] == 'maths' and r[6].month in ms and -3600 <= r[1] < -3000))}" for nm, ms in (("January to March", (1, 2, 3)), ("April to June", (4, 5, 6)))))
print("2. The direction of after / before at widths the first checks did not try")
for g in ORDER: print(f"   {g:10s} " + "; ".join(f"{lab}: {c(g, 0, w)}/{c(g, -w, 0)} = {c(g, 0, w) / max(1, c(g, -w, 0)):.2f}" for lab, w in (("10 s", 10), ("30 s", 30), ("2 h", 7200), ("3 h", 10800), ("6 h", 21600))))
print("3. The first minute as a share of each group's weekday papers, with an interval from resampling whole days (2,000 times)")
rng = np.random.default_rng(14); days = sorted({r[2] for r in W}); idx = {d: i for i, d in enumerate(days)}
def daytab(sel):
    n = np.zeros(len(days)); f = np.zeros(len(days))
    for r in W:
        if sel(r): n[idx[r[2]]] += 1; f[idx[r[2]]] += (0 <= r[1] < 60)
    return n, f
tabs = {g: daytab(lambda r, g=g: r[0] == g) for g in ORDER}; boot = rng.integers(0, len(days), (2000, len(days)))
share = lambda t, b=None: (t[1].sum() / t[0].sum()) if b is None else t[1][b].sum(axis=1) / t[0][b].sum(axis=1)
for g in ORDER: s = share(tabs[g], boot); print(f"   {g:10s} {100 * share(tabs[g]):5.2f}%   ({100 * np.percentile(s, 2.5):.1f} to {100 * np.percentile(s, 97.5):.1f})")
for a, b in (("hep-th", "astro-ph"), ("hep-ph", "astro-ph"), ("hep-th", "hep-ph")):
    d = share(tabs[a], boot) - share(tabs[b], boot); print(f"   {a} minus {b}: {100 * (share(tabs[a]) - share(tabs[b])):+.1f} points ({100 * np.percentile(d, 2.5):+.1f} to {100 * np.percentile(d, 97.5):+.1f})")
print("   within astro-ph, by category (first-minute share; ten minutes before as a share; ratio at ten minutes):")
for sub in ("astro-ph.CO", "astro-ph.EP", "astro-ph.GA", "astro-ph.HE", "astro-ph.IM", "astro-ph.SR"):
    s = np.array([r[1] for r in W if r[3] == sub]); print(f"      {sub}: {100 * ((s >= 0) & (s < 60)).sum() / len(s):5.1f}%; {100 * ((s >= -600) & (s < 0)).sum() / len(s):4.1f}%; {((s >= 0) & (s < 600)).sum() / max(1, ((s >= -600) & (s < 0)).sum()):.1f}")
print("   ten minutes before and after as shares: " + "; ".join(f"{g}: {100 * c(g, -600, 0) / len(S[g]):.1f}% and {100 * c(g, 0, 600) / len(S[g]):.1f}%" for g in ORDER))
print("4. Maths after the boundary: papers in the average ten minutes of 12:00-13:49 and of 14:10-14:59: " + f"{(c('maths', -7200, -600)) / 11:.1f} and {c('maths', 600, 3600) / 5:.1f}; cs.CL: {c('cs.CL', -7200, -600) / 11:.1f} and {c('cs.CL', 600, 3600) / 5:.1f}")
print("5. Is the stamp the clock the arXiv cuts on? The identifier's month (YYMM) of papers stamped on the last weekday of a month, before and from 14:00:00 Eastern")
bym = collections.defaultdict(list)
for r in W: bym[(r[2].year, r[2].month)].append(r[2])
tot = collections.Counter()
for (y, m), ds in sorted(bym.items()):
    if m == 6 or (y, m) == (2024, 12): continue
    last = max(ds); nxt = f"{(y % 100):02d}{m + 1:02d}"
    for r in W:
        if r[2] == last:
            k = ("from 14:00:00" if r[1] >= 0 else "before"); tot[(k, r[4][:4] == nxt)] += 1
            if 0 <= r[1] < 60: tot[("first minute", r[4][:4] == nxt)] += 1
            if -600 <= r[1] < 0: tot[("ten minutes before", r[4][:4] == nxt)] += 1
for k in ("before", "ten minutes before", "first minute", "from 14:00:00"): print(f"   stamped {k:19s}: {tot[(k, True)]:4d} with the next month's identifier, {tot[(k, False)]:4d} with the month's own")
pairs = good = 0
for d in days:
    rows = sorted([(r[1], r[4]) for r in W if r[2] == d and 0 <= r[1] < 60])
    for i in range(len(rows)):
        for j in range(i + 1, len(rows)):
            if rows[i][0] < rows[j][0]: pairs += 1; good += rows[i][1] < rows[j][1]
print(f"   pairs of papers stamped in the same day's first minute at different seconds: {pairs}; the earlier stamp has the lower identifier in {good}")
print("6. Is the pile the arXiv's machinery?")
sec = np.array([r[6].second for r in W if not (-60 <= r[1] < 60)]); cnt = np.bincount(sec, minlength=60); print(f"   away from the boundary's two minutes, papers stamped at second :00 of any minute: {cnt[0]}; mean of the other 59 seconds: {cnt[1:].mean():.0f}")
s_all = np.array([r[1] for r in W]) + 14 * 3600; print("   papers stamped exactly on the hour, hour by hour (Eastern): " + " ".join(f"{h}:{int((s_all == 3600 * h).sum())}" for h in range(24)))
we = [r for r in ALL if r[6].weekday() >= 5]; print(f"   weekends: {sum(1 for r in we if 0 <= r[1] < 60)} of {len(we)} papers in the minute from 14:00; weekdays: {sum(1 for r in W if 0 <= r[1] < 60)} of {len(W)}")
late = [r for r in W if r[0] in ('astro-ph', 'hep-th', 'hep-ph', 'gr-qc', 'quant-ph') and 3600 <= r[1] < 3660]; mar = [r for r in late if date(2025, 3, 10) <= r[2] <= date(2025, 3, 28)]
print(f"   the five physics groups' papers in the minute from 15:00: {len(late)}, of which on the fifteen weekdays from 10 to 28 March: {len(mar)}")
a = collections.Counter(r[2] for r in W if r[0] == 'astro-ph' and 0 <= r[1] < 600); print("   weekdays with fewer than three astro-ph papers in the ten minutes after: " + ", ".join(f"{d} ({a[d]})" for d in days if a[d] < 3 and any(r[2] == d and r[0] == 'astro-ph' for r in W)))
zero = np.array([sum(1 for r in W if r[2] == d and r[1] == 0) for d in days]); print(f"7. Papers stamped 14:00:00 itself, all seven groups: {zero.sum()} in the half-year, {zero.mean():.1f} a weekday, at most {zero.max()}, on {int((zero > 0).sum())} of {len(days)} weekdays")
print(f"8. cs.CL just after the boundary: {c('cs.CL', 0, 60)} and {c('cs.CL', 60, 120)} papers in the first two minutes, against {c('cs.CL', 120, 3600) / 58:.1f} a minute for the rest of the hour; {c('cs.CL', 0, 10)} in the first ten seconds, {c('cs.CL', -10, 0)} in the last ten before")
print(f"9. Weekdays: {len(days)} Eastern dates, the first {days[0]} with {sum(1 for r in W if r[2] == days[0])} papers; first-minute share of ALL of astro-ph's papers, weekends included: {100 * sum(1 for r in ALL if r[0] == 'astro-ph' and 0 <= r[1] < 60 and r[6].weekday() < 5) / sum(1 for r in ALL if r[0] == 'astro-ph'):.1f}%")
print("10. The share of the first minute's papers that come in its first five seconds: " + "; ".join(f"{g}: {100 * c(g, 0, 5) / max(1, c(g, 0, 60)):.0f}%" for g in ORDER[:5]))
