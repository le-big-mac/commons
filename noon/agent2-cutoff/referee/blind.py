"""Blind rebuild of the table from the arXiv API pages. Regex parsing only (untrusted XML)."""
import sys, re, glob, os, pickle
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from collections import Counter, defaultdict

data = sys.argv[1]
out = sys.argv[2]
ET = ZoneInfo("America/New_York")
ASTRO = {"astro-ph." + s for s in ("CO", "EP", "GA", "HE", "IM", "SR")}
GROUPS = ["astro-ph", "hep-th", "hep-ph", "gr-qc", "quant-ph", "maths", "cs.CL"]


def group(cat):
    if cat in ASTRO:
        return "astro-ph"
    if cat in ("math.CO", "math.AP"):
        return "maths"
    if cat in ("hep-th", "hep-ph", "gr-qc", "quant-ph", "cs.CL"):
        return cat
    return None


entry_re = re.compile(r"<entry>(.*?)</entry>", re.S)
id_re = re.compile(r"<id>\s*http://arxiv\.org/abs/(.+?)v(\d+)\s*</id>")
pub_re = re.compile(r"<published>\s*([^<]+?)\s*</published>")
upd_re = re.compile(r"<updated>\s*([^<]+?)\s*</updated>")
cat_re = re.compile(r"<arxiv:primary_category[^>]*\bterm=\"([^\"]+)\"")

papers = {}  # id -> (published str, cat, version, updated, file)
nentries = 0
perfile = {}
conflicts = 0
for f in sorted(glob.glob(os.path.join(data, "*.xml"))):
    txt = open(f, encoding="utf-8", errors="replace").read()
    n = 0
    for m in entry_re.finditer(txt):
        e = m.group(1)
        i = id_re.search(e)
        p = pub_re.search(e)
        c = cat_re.search(e)
        u = upd_re.search(e)
        if not (i and p and c):
            print("BAD ENTRY in", f, e[:200], file=sys.stderr)
            continue
        n += 1
        key = i.group(1)
        rec = (p.group(1), c.group(1), int(i.group(2)), u.group(1) if u else None, os.path.basename(f))
        if key in papers and papers[key][:2] != rec[:2]:
            conflicts += 1
        papers[key] = rec
    perfile[os.path.basename(f)] = n
    nentries += n

rows = []  # (id, group, cat, utc dt, et dt, version, updated)
for k, (p, c, v, u, f) in papers.items():
    g = group(c)
    dt = datetime.strptime(p, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    if g is None:
        continue
    if not (datetime(2025, 1, 1, tzinfo=timezone.utc) <= dt <= datetime(2025, 6, 30, 23, 59, 59, tzinfo=timezone.utc)):
        continue
    rows.append((k, g, c, dt, dt.astimezone(ET), v, u))

pickle.dump(rows, open(os.path.join(os.path.dirname(out), "rows.pkl"), "wb"))

L = []
P = L.append
P(f"files {len(perfile)}  entries {nentries}  distinct ids {len(papers)}  conflicts {conflicts}")
for f, n in perfile.items():
    P(f"  {f} {n}")
P(f"kept (in window, in groups): {len(rows)}")
P("")
P("1. papers kept: all / weekdays")
tot = Counter(r[1] for r in rows)
wk = [r for r in rows if r[4].weekday() < 5]
wtot = Counter(r[1] for r in wk)
for g in GROUPS:
    P(f"  {g:9s} {tot[g]:6d} {wtot[g]:6d}")
P(f"  {'ALL':9s} {sum(tot.values()):6d} {sum(wtot.values()):6d}")


def sod(d):
    return d.hour * 3600 + d.minute * 60 + d.second


def cnt(g, a, b, src=wk):
    return sum(1 for r in src if r[1] == g and a <= sod(r[4]) < b)


P("")
P("2. weekday counts: 13:00-13:09 | 13:50-13:59 | 14:00-14:09 | 14:00:00-14:00:59 | ratio third/second")
for g in GROUPS:
    a = cnt(g, 13 * 3600, 13 * 3600 + 600)
    b = cnt(g, 13 * 3600 + 3000, 14 * 3600)
    c = cnt(g, 14 * 3600, 14 * 3600 + 600)
    d = cnt(g, 14 * 3600, 14 * 3600 + 60)
    P(f"  {g:9s} {a:5d} {b:5d} {c:5d} {d:5d}  {c / b if b else float('nan'):.3f}")

P("")
P("3. astro-ph busiest UTC minute (all days of week, by UTC month of published)")
for name, months in (("Jan-Feb", (1, 2)), ("Apr-Jun", (4, 5, 6))):
    for label, src in (("all days", rows), ("weekdays(ET)", wk)):
        cm = Counter(r[3].strftime("%H:%M") for r in src if r[1] == "astro-ph" and r[3].month in months)
        P(f"  {name} {label}: top5 {cm.most_common(5)}")

P("")
P("4. astro-ph weekday papers stamped exactly 14:00:00 ET: %d" % cnt("astro-ph", 14 * 3600, 14 * 3600 + 1))
for g in GROUPS:
    P(f"   ({g}: {cnt(g, 14 * 3600, 14 * 3600 + 1)})")

P("")
P("5. weekdays on which 14:00-14:09 holds more / fewer / equal vs 13:50-13:59 (days with any weekday paper in the group; and over all Mon-Fri of the half-year =129)")
for g in GROUPS:
    days = defaultdict(lambda: [0, 0])
    alldays = set()
    for r in wk:
        if r[1] != g:
            continue
        d = r[4].date()
        alldays.add(d)
        s = sod(r[4])
        if 13 * 3600 + 3000 <= s < 14 * 3600:
            days[d][0] += 1
        elif 14 * 3600 <= s < 14 * 3600 + 600:
            days[d][1] += 1
    more = sum(1 for d in alldays if days[d][1] > days[d][0])
    fewer = sum(1 for d in alldays if days[d][1] < days[d][0])
    eq = len(alldays) - more - fewer
    P(f"  {g:9s} more {more:4d} fewer {fewer:4d} equal {eq:4d}  days {len(alldays)}")

open(out, "w").write("\n".join(L) + "\n")
print("\n".join(L))
