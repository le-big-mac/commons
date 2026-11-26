"""Checks made on 26 November 2026, after a reader with the web set this study against the papers.
usage: python -I changes.py results.json > changes.out      (standard library only)
1. The correlation of openings with unemployment in levels and in twelve-month changes, by period: is the -0.97 of
   2010 to 2019 anything more than two smooth trends through one expansion?
2. How far the openings rate stood above a curve fitted to 2010-2019, year by year.
3. Small facts the page states: when the survey's series begins, the missing month, unemployment in late 2025."""
import sys, json, math
sys.dont_write_bytecode = True

def corr(a, b):
    p = [(x, y) for x, y in zip(a, b) if x is not None and y is not None]
    n = len(p); ma = sum(x for x, _ in p) / n; mb = sum(y for _, y in p) / n
    sa = sum((x - ma) ** 2 for x, _ in p); sb = sum((y - mb) ** 2 for _, y in p)
    return sum((x - ma) * (y - mb) for x, y in p) / math.sqrt(sa * sb), n

if __name__ == '__main__':
    d = json.load(open(sys.argv[1]))
    clean = lambda v: [None if (x is None or x != x) else x for x in v]          # a missing month is None or not-a-number in the file
    m, J, U = d['months'], clean(d['jo']), clean(d['ur'])
    yr = [int(s[:4]) for s in m]
    both = [i for i in range(len(m)) if J[i] is not None and U[i] is not None]
    print(f"months in the file: {len(m)}, {m[0]} to {m[-1]}; the openings rate begins {m[next(i for i in range(len(m)) if J[i] is not None)]};"
          f" months with both series: {len(both)}; months since the openings rate begins with no unemployment rate: {[m[i] for i in range(len(m)) if J[i] is not None and U[i] is None]}")
    print("1. openings rate against unemployment rate: correlation in levels, in twelve-month changes, in one-month changes")
    for lo, hi in ((2001, 2009), (2010, 2019), (2001, 2019), (2021, 2026)):
        ix = [i for i in both if lo <= yr[i] <= hi]
        r, n = corr([J[i] for i in ix], [U[i] for i in ix])
        i12 = [i for i in ix if i >= 12 and J[i - 12] is not None and U[i - 12] is not None and yr[i - 12] >= lo]
        r12, n12 = corr([J[i] - J[i - 12] for i in i12], [U[i] - U[i - 12] for i in i12])
        i1 = [i for i in ix if i >= 1 and J[i - 1] is not None and U[i - 1] is not None and yr[i - 1] >= lo]
        r1, n1 = corr([J[i] - J[i - 1] for i in i1], [U[i] - U[i - 1] for i in i1])
        print(f"   {lo}-{hi}: levels {r:+.2f} ({n} months); twelve-month changes {r12:+.2f} ({n12}); one-month changes {r1:+.2f} ({n1})")
    ix = [i for i in both if 2010 <= yr[i] <= 2019]
    x = [math.log(U[i]) for i in ix]; y = [math.log(J[i]) for i in ix]
    mx = sum(x) / len(x); my = sum(y) / len(y)
    b = sum((a - mx) * (c - my) for a, c in zip(x, y)) / sum((a - mx) ** 2 for a in x); a0 = my - b * mx
    print(f"2. a straight line through the logarithms of 2010-2019: ln(openings rate) = {a0:.2f} {b:+.2f} ln(unemployment rate). Openings rate above that line, in points, by year:")
    print("   " + "  ".join(f"{Y}: {sum(J[i] - math.exp(a0 + b * math.log(U[i])) for i in both if yr[i] == Y) / sum(1 for i in both if yr[i] == Y):+.1f}" for Y in range(2017, 2027)))
    line = lambda i: math.exp(a0 + b * math.log(U[i]))
    print("   by quarter of 2024: " + "  ".join(f"Q{q}: {sum(J[i] - line(i) for i in both if yr[i] == 2024 and (int(m[i][5:]) - 1) // 3 + 1 == q) / sum(1 for i in both if yr[i] == 2024 and (int(m[i][5:]) - 1) // 3 + 1 == q):+.2f}" for q in (1, 2, 3, 4)))
    print(f"   the line's own misses in its last three years (2017 to 2019) are -0.2, +0.1 and -0.2, so +0.1 to +0.2 is within its scatter")
    lo = [i for i in both if 3.5 <= U[i] <= 3.9]
    a = [J[i] for i in lo if 2010 <= yr[i] <= 2019]; c = [J[i] for i in lo if 2022 <= yr[i] <= 2023]
    print(f"   at the same unemployment, 3.5% to 3.9%: openings rate {min(a)} to {max(a)} in 2010-2019 ({len(a)} months, {min(m[i] for i in lo if 2010 <= yr[i] <= 2019)} on); {min(c)} to {max(c)} in 2022-2023 ({len(c)} months)."
          f" Months since 2021 with unemployment below 3.5%: {[m[i] for i in both if yr[i] >= 2021 and U[i] < 3.5]}")
    band = lambda years: [J[i] for i in both if yr[i] in years and 3.4 <= U[i] <= 4.5]
    for name, years in (("2017-2019", (2017, 2018, 2019)), ("2021-2023", (2021, 2022, 2023)), ("2024", (2024,)), ("2025-2026", (2025, 2026))):
        v = band(years); print(f"   openings rate at unemployment of 3.4% to 4.5%, {name}: {sum(v) / len(v):.2f}% ({len(v)} months)")
    print("   a straight line in logarithms cannot turn upright, so it cannot test whether one steep curve holds both sets of months")
    late = [(m[i], U[i]) for i in range(len(m)) if m[i] >= '2025-06']
    print("3. unemployment rate, June 2025 on: " + ", ".join(f"{a} {b}" for a, b in late))
