"""Remaining README numbers and a few last controls. usage: python -I verify.py rows.pkl README.md expectations.md records.csv"""
import sys, pickle, re, statistics, csv
from collections import Counter, defaultdict
from datetime import date

rows = pickle.load(open(sys.argv[1], "rb"))
G = ["astro-ph", "hep-th", "hep-ph", "gr-qc", "quant-ph", "maths", "cs.CL"]
sod = lambda d: d.hour * 3600 + d.minute * 60 + d.second
R = [(i, g, c, u, e, sod(e) - 14 * 3600, e.weekday(), e.date(), v, up) for i, g, c, u, e, v, up in rows]
W = [r for r in R if r[6] < 5]
by = {g: [r for r in W if r[1] == g] for g in G}
cnt = lambda rs, lo, hi: sum(1 for r in rs if lo <= r[5] < hi)
A = by["astro-ph"]
print("astro minute by minute:", [cnt(A, 60 * k, 60 * k + 60) for k in range(10)], " tens of seconds:", [cnt(A, 10 * k, 10 * k + 10) for k in range(6)])
print("astro by month ratio:", [round(cnt([r for r in A if r[4].month == m], 0, 600) / cnt([r for r in A if r[4].month == m], -600, 0), 1) for m in range(1, 7)])
print("astro by weekday ratio:", [round(cnt([r for r in A if r[6] == d], 0, 600) / cnt([r for r in A if r[6] == d], -600, 0), 1) for d in range(5)])
dd = Counter(r[7] for r in A if 0 <= r[5] < 600); days = sorted(set(r[7] for r in A))
print("astro median a day after:", statistics.median([dd[d] for d in days]), "days", len(days))
print("hour from 14:00 share:", {g: round(100 * cnt(by[g], 0, 3600) / len(by[g]), 1) for g in G})
print("astro weekend papers 14:00-14:09:", sum(1 for r in R if r[1] == 'astro-ph' and r[6] >= 5 and 0 <= r[5] < 600))
print("latest version after the half-year:", sum(1 for r in R if r[9] and r[9] > "2025-06-30T23:59:59Z"), "of", len(R))
print("version-1 papers:", sum(1 for r in R if r[8] == 1), "; of them with updated == published:", sum(1 for r in R if r[8] == 1 and r[9] == r[3].strftime('%Y-%m-%dT%H:%M:%SZ')))
print("papers with version > 1 whose updated == published:", sum(1 for r in R if r[8] > 1 and r[9] == r[3].strftime('%Y-%m-%dT%H:%M:%SZ')), "of", sum(1 for r in R if r[8] > 1))
C = by["cs.CL"]; cd = Counter(r[7] for r in C if -600 <= r[5] < 0); cdays = sorted(set(r[7] for r in C))
v = sorted(cd[d] for d in cdays); print("cs.CL before: median", statistics.median(v), "days", len(v), "without top five", sum(v[:-5]), "by month", [cnt([r for r in C if r[4].month == m], -600, 0) for m in range(1, 7)])
print("cs.CL last minute", cnt(C, -60, 0), "first minute", cnt(C, 0, 60))
print("days (all groups) with a paper at exactly 14:00:00:", len(set(r[7] for r in W if r[5] == 0)), "; papers at 14:00:00 a day: mean", round(cnt(W, 0, 1) / 129, 1), "max", max(Counter(r[7] for r in W if r[5] == 0).values()))
print("physics first minute 14:00:", sum(cnt(by[g], 0, 60) for g in G[:5]))
print("maths before vs hour earlier, Jan-Mar and Apr-Jun:", [(cnt([r for r in by['maths'] if r[4].month in ms], -600, 0), cnt([r for r in by['maths'] if r[4].month in ms], -3600, -3000)) for ms in ((1, 2, 3), (4, 5, 6))])
print("maths ten-minute spans, mean 12:00-13:49:", round(cnt(by['maths'], -7200, -600) / 11, 1), " mean 14:10-14:59:", round(cnt(by['maths'], 600, 3600) / 5, 1))
# identifier month on the last weekday of each month
for d in (date(2025, 1, 31), date(2025, 2, 28), date(2025, 3, 31), date(2025, 4, 30), date(2025, 5, 30)):
    rs = [r for r in W if r[7] == d]
    nxt = lambda r: r[0].split(".")[0] != d.strftime("%y%m")
    b = [r for r in rs if r[5] < 0]; a = [r for r in rs if r[5] >= 0]
    print(f"  {d}: stamped before 14:00: {len(b)} papers, {sum(map(nxt, b))} with another month's identifier; from 14:00:00: {len(a)} papers, {sum(map(nxt, a))} with another month's identifier; stamped 14:00:00-14:00:59: {sum(1 for r in a if r[5] < 60)}, next month's id {sum(1 for r in a if r[5] < 60 and nxt(r))}; 13:50-13:59: {sum(1 for r in b if r[5] >= -600)}, next month's id {sum(1 for r in b if r[5] >= -600 and nxt(r))}")
# pasted lines
norm = lambda s: re.sub(r"\s+", " ", s)
readme = norm(open(sys.argv[2]).read()); exp = open(sys.argv[3]).read()
for k in ("T5", "T6", "T7", "T8"):
    m = re.search(rf"^{k}\. (.*?)\s+odds 0\.\d+\s*$", exp, re.M | re.S)
    line = norm(m.group(1)); print(k, "sealed words found in README:", ('"' + line + '"') in readme)
print("marks on the sheet:", re.findall(r"^(T\d)\. \(([a-z ]+)", exp, re.M))
# records.csv against my table
mine = {r[0]: (r[3].strftime('%Y-%m-%dT%H:%M:%SZ'), r[2]) for r in R}
theirs = {}
for r in csv.DictReader(open(sys.argv[4])):
    theirs[r["id"]] = (r["published"], r["primary"])
same = sum(1 for k, v in mine.items() if theirs.get(k) == v)
print("records.csv lines:", len(theirs), "; my kept papers found there with the same stamp and category:", same, "of", len(mine))
