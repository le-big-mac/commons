"""The half-year of 2025 set beside the figures printed for 2002 to 2005.   Added 26 November 2026, after a reader's report.
usage: python -I then.py records.csv > then.out          (standard library)
The printed figures are shares of ALL submissions to an archive in a window after the deadline (16:00 Eastern then,
14:00 since 2 January 2017), so this counts the same way: every paper of the half-year whose primary category is in
the archive, weekends included, against those stamped in the window after 14:00:00 Eastern on a weekday.
Second part: papers whose identifier is later than their stamp implies. Identifiers are given in order of arrival; a
paper stamped before one day's 14:00 whose identifier is higher than that of a paper stamped after it was numbered
late. Why, the data cannot say: that such papers were held back by the moderators is a guess. The count is a
low one: only the seven groups of the study are looked at, and the sequence starts again each month."""
import csv, sys
from datetime import datetime, timezone, timedelta, time
from zoneinfo import ZoneInfo
ET = ZoneInfo('America/New_York')

PRINTED = [  # archive, window in seconds, share printed, where
    ('astro-ph', 60, 1.5, 'Dietrich 2008, second half of 2002'),
    ('astro-ph', 60, 2.3, 'Dietrich 2008, second half of 2005'),
    ('astro-ph', 300, 2.9, 'Dietrich 2008, second half of 2002'),
    ('astro-ph', 300, 4.6, 'Dietrich 2008, second half of 2005'),
    ('astro-ph', 600, 100 * 1049 / 23165, 'Haque and Ginsparg 2009, 2002 to 2004: 1,049 of 23,165'),
    ('hep-th', 1200, 100 * 309 / 9932, 'Haque and Ginsparg 2009, 2002 to 2004: 309 of 9,932'),
    ('hep-ph', 1200, 100 * 363 / 12281, 'Haque and Ginsparg 2009, 2002 to 2004: 363 of 12,281'),
    ('quant-ph', 300, 6.0, 'Peters 2023: "about 6%" within five minutes'),
]

def archive(p):
    return 'astro-ph' if p.startswith('astro-ph') else p

def batch_day(t):
    """the weekday whose 14:00 closes the list this stamp falls in (holidays ignored)"""
    d = t.date()
    if t.weekday() < 5 and t.time() < time(14, 0): return d
    d += timedelta(days=1)
    while d.weekday() >= 5: d += timedelta(days=1)
    return d

if __name__ == '__main__':
    rows = []
    for r in csv.DictReader(open(sys.argv[1])):
        t = datetime.strptime(r['published'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc).astimezone(ET)
        rows.append((r['id'], t, archive(r['primary'])))
    print(f"{len(rows)} papers")
    after = lambda t: (t.hour - 14) * 3600 + t.minute * 60 + t.second
    print("1. share of all of an archive's papers stamped within a window after 14:00:00 Eastern on a weekday, beside the printed shares")
    for arch, w, share, where in PRINTED:
        v = [t for _, t, a in rows if a == arch]
        n = sum(1 for t in v if t.weekday() < 5 and 0 <= after(t) < w)
        now = 100 * n / len(v)
        print(f"   {arch}, {w} s: {n} of {len(v)} = {now:.1f}% in the first half of 2025; printed: {share:.1f}% ({where}); ratio {now / share:.1f}")
    for arch in ('astro-ph', 'hep-th', 'hep-ph'):
        v = [t for _, t, a in rows if a == arch]
        c = {w: sum(1 for t in v if t.weekday() < 5 and 0 <= after(t) < w) for w in (60, 300, 600, 1200)}
        print(f"   {arch}: of the papers in the first five minutes, {100 * c[60] / c[300]:.0f}% are in the first minute; of those in the first twenty, {100 * c[60] / c[1200]:.0f}%")
    print("   printed for astro-ph: the first minute held 1.5 of 2.9 (52%) in 2002 and 2.3 of 4.6 (50%) in 2005")
    print("2. papers numbered later than their stamp implies")
    groups = {'astro-ph': 'astro-ph', 'hep-th': 'hep-th', 'hep-ph': 'hep-ph', 'gr-qc': 'gr-qc', 'quant-ph': 'quant-ph', 'cs.CL': 'cs.CL', 'math.CO': 'maths', 'math.AP': 'maths'}
    seq = sorted((i, t, groups[a]) for i, t, a in rows if a in groups)
    late = {}; tot = {}; pile = [0, 0]; month = None; top = None
    for i, t, g in seq:
        if i[:4] != month: month, top = i[:4], None          # identifiers start again each month
        b = batch_day(t)
        tot[g] = tot.get(g, 0) + 1
        is_late = top is not None and b < top
        if is_late: late[g] = late.get(g, 0) + 1
        if t.weekday() < 5 and 0 <= after(t) < 60:
            pile[0] += 1; pile[1] += is_late
        if top is None or b > top: top = b
    for g in ('astro-ph', 'hep-th', 'hep-ph', 'gr-qc', 'quant-ph', 'maths', 'cs.CL'):
        print(f"   {g}: {late.get(g, 0)} of {tot[g]} = {100 * late.get(g, 0) / tot[g]:.1f}%")
    print(f"   of the {pile[0]} papers stamped in the first minute after 14:00 on a weekday: {pile[1]}")
