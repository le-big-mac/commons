# Availability only: for each gauge file, first and last day and the count of valid days by recent year.
# Prints no sea level values. Run with python3 -I.
import csv, sys, datetime as dt
names = dict(l.split(',')[:2] for l in open('/home/agent1/trace/data/stations.csv').read().splitlines()[2:])
order = "093 084 092 091 030 003 392 302 087 082 316 395 034 317 569 554 545 551 556 592 558 542 540 571".split()
print(f"{'id':>4} {'name':<18} {'first':>10} {'last':>10}  valid days 2015 / 1997 / 2023 / 2025 / 2026 (of days to last)")
for sid in order:
    rows = list(csv.reader(open(f'/home/agent1/trace/data/d{sid}.csv')))
    d = [(dt.date(int(r[0]), int(r[1]), int(r[2])), int(r[3])) for r in rows if len(r) >= 4]
    ok = [x for x in d if x[1] > -30000]
    def n(y): return sum(1 for x in ok if x[0].year == y)
    last = ok[-1][0] if ok else None
    print(f"{sid:>4} {names.get(str(int(sid)),'?'):<18} {str(ok[0][0]):>10} {str(last):>10}  {n(2015):>3} / {n(1997):>3} / {n(2023):>3} / {n(2025):>3} / {n(2026):>3}")
