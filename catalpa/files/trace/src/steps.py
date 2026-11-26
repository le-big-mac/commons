# The reverse of the hurricane sum: find every lasting step at San Diego first, then ask what storm was about.
# A step: a day D (1 August to 15 November, 1980-2025) on which the daily sea level (rule L) on days D+1..D+5 stands
# 9 cm or more above days D-10..D-4, and still 7 cm or more above on days D+9..D+13. Neighbouring days are one step;
# the step's day is the day of its largest rise. Then, from the best tracks: every storm at hurricane strength
# within 600 km of Baja California's ocean-side line, north of 20 N, within 6 days before or after the step's day.
# The thresholds were chosen after seeing 1997 (11.4, 9.8), 2015 (13.1, 9.4) and 2026 (13.3): this is a look, not a test.
# Run: ~/ipd/.venv/bin/python -I src/steps.py > steps.out
import sys, io, contextlib, importlib.util, datetime as dt
import numpy as np
def load(name):
    spec = importlib.util.spec_from_file_location(name, f'/home/agent1/trace/src/{name}.py'); m = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(m)
    return m
A4 = load('after4'); CO = A4.CO; PS = CO.PS; C = CO.C; T = CO.T
a = {k: v - C.fitday("San Diego", k) for k, v in T.daily["San Diego"].items() if k.year >= 1979}
TR = A4.tracks(1980, 2025)
found = []
for y in range(1980, 2026):
    day = dt.date(y, 8, 1); hits = []
    while day <= dt.date(y, 11, 15):
        m = CO.measure(a, day)
        if m is not None and m[0] >= 9 and m[1] >= 7: hits.append((day, m[0], m[1], m[2]))
        day += dt.timedelta(days=1)
    # cluster neighbouring days
    cl = []
    for h in hits:
        if cl and (h[0] - cl[-1][-1][0]).days <= 3: cl[-1].append(h)
        else: cl.append([h])
    for c in cl: found.append(max(c, key=lambda h: h[1]) + (len(c),))
days_checked = sum(1 for y in range(1980, 2026) for k in range((dt.date(y, 11, 15) - dt.date(y, 8, 1)).days + 1) if CO.measure(a, dt.date(y, 8, 1) + dt.timedelta(days=k)) is not None)
print(f"LASTING STEPS AT SAN DIEGO, 1 August - 15 November, 1980-2025 ({days_checked} days with enough data): {len(found)}")
print("  day of largest rise   rise   two weeks on   base   days in the cluster   hurricanes within 600 km of Baja's ocean side (north of 20 N) within 6 days")
for d, r, af, base, n in found:
    st = []
    for (code, name), pts in TR.items():
        near = [(p[0], PS.near(p[1], p[2])[0], p[3]) for p in pts if p[3] >= 64 and p[1] >= 20.0 and abs((p[0].date() - d).days) <= 6 and PS.near(p[1], p[2])[0] <= 600]
        if near:
            best = min(near, key=lambda q: q[1]); st.append(f"{name.title()} ({best[0].strftime('%d %b')}, {best[1]:.0f} km, {best[2]} kt)")
    print(f"  {d}   {r:+5.1f}   {af:+5.1f}   {base:5.1f}   {n:2d}   " + ("; ".join(st) if st else "none"))
# how often is a hurricane within 600 km (north of 20 N) within 6 days of an arbitrary day in the season?
tot = hit = 0
for y in range(1980, 2026):
    day = dt.date(y, 8, 1)
    while day <= dt.date(y, 11, 15):
        tot += 1
        if any(p[3] >= 64 and p[1] >= 20.0 and abs((p[0].date() - day).days) <= 6 and PS.near(p[1], p[2])[0] <= 600 for pts in TR.values() for p in pts if p[0].year == y): hit += 1
        day += dt.timedelta(days=1)
print(f"\nshare of all days of that season with such a hurricane within 6 days: {hit} of {tot} = {100 * hit / tot:.0f}%")
print("strong El Nino autumns by NOAA's table (the first page's indices.out): 1982, 1997, 2015 (and 2026)")
