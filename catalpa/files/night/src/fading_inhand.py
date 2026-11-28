# What is in hand before the fifteenth sheet: the fading of the twilight from 3 to 7 degrees (the month's reading at
# 7 degrees less its reading at 3) in the first make, each year less 2021, 2021 to 2024, from the reductions of the
# ninth sheet (cache2/depth.pkl). One unit per place (the chip with the most months). No file is read.
import pickle, importlib.util, io, contextlib
import numpy as np
B = '/home/agent1/night/'
spec = importlib.util.spec_from_file_location('depth', B + 'src/depth.py'); DP = importlib.util.module_from_spec(spec); spec.loader.exec_module(DP)
R = pickle.load(open(B + 'cache2/depth.pkl', 'rb'))
def fading(st, dp=7.0):
    chips = {}
    for (s, y, m), r in R.items():
        if s == st and r is not None and DP.monthfig(r, 6.0) is not None: chips.setdefault((r.get('mac') or '')[-8:], []).append((y, m))
    if not chips: return {}
    ch = max(chips, key=lambda c: len(chips[c])); F = {}
    for (s, y, m), r in R.items():
        if s != st or r is None or (r.get('mac') or '')[-8:] != ch: continue
        a, b = DP.monthfig(r, dp), DP.monthfig(r, 3.0)
        if a is not None and b is not None: F[(y, m)] = a - b
    return F
def diff(F, y, months=range(1, 13)):
    d = [F[(y, m)] - F[(2021, m)] for m in months if (y, m) in F and (2021, m) in F]; return (float(np.mean(d)), len(d)) if len(d) >= 3 else (None, len(d))
f = lambda v: '   .  ' if v[0] is None else f'{v[0]:+.2f}({v[1]:2d})'
for name, sts in (('south', list(DP.SOUTH)), ('north', DP.NORTH)):
    print(f'{name}: the fading from 3 to 7 degrees, each year less 2021, the mean over the months both years have (and how many); negative: brighter at depth than in 2021')
    rows = {}
    for st in sts:
        F = fading(st); rows[st] = [diff(F, y) for y in (2022, 2023, 2024)] + [diff(F, 2024, range(1, 8)), diff(F, 2024, range(8, 13))]
        print(f"   {DP.SOUTH.get(st, st):<14} 2022 {f(rows[st][0])}  2023 {f(rows[st][1])}  2024 {f(rows[st][2])}  2024 Jan-Jul {f(rows[st][3])}  2024 Aug-Dec {f(rows[st][4])}")
    for i, lab in enumerate(('2022', '2023', '2024', '2024 Jan-Jul', '2024 Aug-Dec')):
        v = [rows[st][i][0] for st in sts if rows[st][i][0] is not None]
        print(f'   the middle, {lab}: {np.median(v):+.3f} ({len(v)} places); from {min(v):+.2f} to {max(v):+.2f}; half of them within {np.percentile(v, 25):+.2f} and {np.percentile(v, 75):+.2f}')
print('\nmonth by month, the middle over places of the fading from 3 to 7 degrees less the same month of 2021 (hundredths; the number of places below); odd units left out of the north: stars4, stars426, stars62, stars33')
for name, sts in (('south', list(DP.SOUTH)), ('north', [s for s in DP.NORTH if s not in ('stars4', 'stars426', 'stars62', 'stars33')])):
    FF = {st: fading(st) for st in sts}
    for y in (2022, 2023, 2024):
        v = [[FF[st][(y, m)] - FF[st][(2021, m)] for st in sts if (y, m) in FF[st] and (2021, m) in FF[st]] for m in range(1, 13)]
        print(f"   {name} {y}: " + ' '.join(f'{100 * np.median(x):+4.0f}' if len(x) >= 3 else '   .' for x in v) + '   | places: ' + ' '.join(f'{len(x):2d}' for x in v))
