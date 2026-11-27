# The lines of the eighth sheet (expectations-between.md), scored. Reads the four sets of reductions already in hand
# (odd months) and the set made by between_fetch.py (even months). An instrument is the chip with the most months at
# its station over both; a month's figure is its twilight altitude less the mean of the same calendar month of 2021
# and 2024 (whichever it has), times the instrument's middle twilight slope: magnitudes, negative = a brighter twilight.
# Comparisons are made on the unrounded figures and include the mark itself ("-0.10 or below", "within 0.08").
import os, sys, pickle, importlib.util
import numpy as np
spec = importlib.util.spec_from_file_location('tongasheet', '/home/agent1/night/src/tongasheet.py'); TS = importlib.util.module_from_spec(spec); spec.loader.exec_module(TS)
TW = TS.TW; geo = TS.geo; B = '/home/agent1/night/'
SOUTH = ['stars456', 'stars221', 'stars29', 'stars634', 'stars215', 'stars220', 'stars315', 'stars722', 'stars391', 'stars251']
NORTH = ['stars246', 'stars347', 'stars47', 'stars602', 'stars489']
NAME = {'stars456': 'Mudgee', 'stars221': 'El Leoncito', 'stars29': 'Bahía Blanca', 'stars634': 'Martinborough', 'stars215': 'Mount Martha', 'stars220': 'Malargüe', 'stars315': 'Coonabarabran', 'stars722': 'Queensland', 'stars391': 'Atacama', 'stars251': 'Réunion'}
R = {}
for fn in ('cache2/twilight16.pkl', 'cache2/twilight_new.pkl', 'cache2/twilight_south.pkl', 'cache2/twilight_south2.pkl', 'cache2/twilight_even.pkl'):
    if not os.path.exists(B + fn): print(f'(no {fn} yet)'); continue
    X = pickle.load(open(B + fn, 'rb')); X.pop('meta', None); R.update(X)
def series(st):
    chips = {}
    for (s, y, m), r in R.items():
        if s == st and r is not None and TW.month_value(r): chips.setdefault(TS.chip(r), []).append((y, m))
    if not chips: return {}
    ch = max(chips, key=lambda c: len(chips[c])); V = {}; sl = []
    for (s, y, m), r in R.items():
        if s != st or r is None or TS.chip(r) != ch: continue
        mv = TW.month_value(r)
        if mv: V[(y, m)] = mv[0]; sl += r['sl']
    s_ = abs(float(np.median(sl))); out = {}
    for (y, m), v in V.items():
        base = [V[(yy, m)] for yy in (2021, 2024) if (yy, m) in V]
        if base: out[(y, m)] = s_ * (v - float(np.mean(base)))
    return out
A = {st: series(st) for st in SOUTH + NORTH}; lat = {st: float(geo[st]['latitude']) for st in SOUTH + NORTH}
def vals(group, k): return [A[st][k] for st in group if k in A[st]]
def mid(group, k): v = vals(group, k); return (float(np.median(v)), len(v)) if v else (None, 0)
def share(group, k): v = vals(group, k); return (sum(1 for x in v if x <= -0.10), len(v))
def verdict(ok, n, need): return 'void (too few)' if n < need else ('held' if ok else 'failed')
ALLM = [(y, m) for y in (2022, 2023) for m in range(1, 13)]
print('the ten southern photometers, every month of 2022 and 2023 (hundredths of a magnitude; negative: a brighter twilight; . no figure)')
for st in sorted(SOUTH, key=lambda s: lat[s]):
    print(f"   {NAME[st]:<14} {lat[st]:+6.1f}  " + ' | '.join(' '.join(f"{100 * A[st][(y, m)]:+4.0f}" if (y, m) in A[st] else '   .' for m in range(1, 13)) for y in (2022, 2023)))
print('   the middle           ' + ' | '.join(' '.join(f"{100 * mid(SOUTH, (y, m))[0]:+4.0f}" if mid(SOUTH, (y, m))[1] >= 3 else '   .' for m in range(1, 13)) for y in (2022, 2023)))
print('   brighter by 0.10 or more ' + ' | '.join(' '.join(f"{share(SOUTH, (y, m))[0]:4d}" if share(SOUTH, (y, m))[1] else '   .' for m in range(1, 13)) for y in (2022, 2023)))
print('   of those with the month  ' + ' | '.join(' '.join(f"{share(SOUTH, (y, m))[1]:4d}" if share(SOUTH, (y, m))[1] else '   .' for m in range(1, 13)) for y in (2022, 2023)))
print()
# V1, V2: June 2022
s, n = share(SOUTH, (2022, 6)); m6, _ = mid(SOUTH, (2022, 6))
print(f"V1. June 2022 brighter by 0.10 or more at 80 in 100 or more of those that have it: {s} of {n}: {verdict(n and s / n >= 0.80, n, 6)}")
print(f"V2. June 2022, the middle between -0.20 and -0.50: {m6 if m6 is None else round(m6, 3)}: {verdict(m6 is not None and -0.50 <= m6 <= -0.20, n, 6)}")
m8, n8 = mid(SOUTH, (2022, 8))
print(f"V3. August 2022, the middle between -0.22 and -0.50: {m8 if m8 is None else round(m8, 3)}: {verdict(m8 is not None and -0.50 <= m8 <= -0.22, n8, 6)}")
print(f"V4. neither June's nor August's middle is brighter than -0.47: {verdict(m6 is not None and m8 is not None and m6 >= -0.47 and m8 >= -0.47, min(n, n8), 6)}")
s4, n4 = share(SOUTH, (2022, 4))
print(f"V5. April 2022, brighter by 0.10 or more at 45 to 90 in 100 of those that have it: {s4} of {n4}: {verdict(n4 and 0.45 <= s4 / n4 <= 0.90, n4, 6)}")
far = [st for st in SOUTH if lat[st] < -25]; s2, n2 = share(far, (2022, 2))
print(f"V6. February 2022, south of 25 degrees south: at most two brighter by 0.10 or more: {s2} of {n2}: {verdict(s2 <= 2, n2, 5)}")
r2 = A['stars251'].get((2022, 2))
print(f"V7. February 2022 on Réunion brighter by 0.20 or more: {r2 if r2 is None else round(r2, 3)}: {'void (no figure)' if r2 is None else ('held' if r2 <= -0.20 else 'failed')}")
s8, n8b = share(SOUTH, (2023, 8)); m10, n10 = mid(SOUTH, (2023, 10)); m12, n12 = mid(SOUTH, (2023, 12))
print(f"V8. August 2023, brighter by 0.10 or more at 20 to 60 in 100 of those that have it: {s8} of {n8b}: {verdict(n8b and 0.20 <= s8 / n8b <= 0.60, n8b, 6)}")
print(f"V9. October and December 2023, the middle within 0.08 of nothing in both: {m10 if m10 is None else round(m10, 3)} and {m12 if m12 is None else round(m12, 3)}: {verdict(m10 is not None and m12 is not None and abs(m10) <= 0.08 and abs(m12) <= 0.08, min(n10, n12), 6)}")
tot = 0; inside = 0
for st in SOUTH:
    a = A[st]
    for (y, m) in ALLM:
        if m % 2 or not ((2022, 2) <= (y, m) <= (2023, 10)): continue
        i = y * 12 + m - 1; p = ((i - 1) // 12, (i - 1) % 12 + 1); q = ((i + 1) // 12, (i + 1) % 12 + 1)
        if (y, m) in a and p in a and q in a: tot += 1; inside += (min(a[p], a[q]) - 0.10 <= a[(y, m)] <= max(a[p], a[q]) + 0.10)
print(f"V10. even months February 2022 to October 2023 that lie between their two neighbours widened by 0.10: {inside} of {tot}" + (f" ({100 * inside / tot:.0f} in 100)" if tot else '') + f": {verdict(tot and inside / tot >= 0.75, tot, 40)}")
w = [(m, mid(NORTH, (2022, m))) for m in (2, 4, 6, 8, 10, 12)]; w = [(m, v) for m, (v, n_) in w if n_ >= 3]
print(f"V11. the five northern photometers, even months of 2022 with three or more figures: {len(w)}; the middle within 0.08 of nothing in {sum(1 for m, v in w if abs(v) <= 0.08)} ({', '.join(f'{m:02d} {v:+.2f}' for m, v in w)}): {verdict(len(w) - sum(1 for m, v in w if abs(v) <= 0.08) <= 1, len(w), 5)}")
print('\nthe five northern photometers, every month of 2022 and 2023')
for st in NORTH:
    print(f"   {st:<14} {lat[st]:+6.1f}  " + ' | '.join(' '.join(f"{100 * A[st][(y, m)]:+4.0f}" if (y, m) in A[st] else '   .' for m in range(1, 13)) for y in (2022, 2023)))
