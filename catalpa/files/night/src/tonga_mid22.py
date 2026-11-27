# The second amendment's figure (lines U6 and U7 of the seventh sheet): the twilight of the middle and end of 2022
# against the same months of the years on either side, for records that do not have all four years.
# For each instrument: for each of May, July, September and November 2022, the twilight figure less the mean of the
# same calendar month in 2021 and in 2024, whichever of the two it has (one is enough); D2 is the mean of those
# differences over the months that have one (two months or more are needed), in magnitudes by the instrument's slope.
# Negative: the twilight read brighter in the second half of 2022.
# Usage: tonga_mid22.py FILE.pkl [FILE.pkl ...]
import sys, pickle, importlib.util
import numpy as np
spec = importlib.util.spec_from_file_location('tongasheet', '/home/agent1/night/src/tongasheet.py'); TS = importlib.util.module_from_spec(spec); spec.loader.exec_module(TS)
TW = TS.TW; geo = TS.geo
R = {}; south = None; north = None
for fn in sys.argv[1:]:
    X = pickle.load(open(fn, 'rb')); m = X.pop('meta', None); R.update(X)
    if m and 'south' in m: south = (south or []) + list(m['south']); north = (north or []) + list(m.get('north', []))
def d2(st):
    chips = {}
    for (s, y, m), r in R.items():
        if s == st and r is not None and TW.month_value(r): chips.setdefault(TS.chip(r), []).append((y, m))
    if not chips: return None
    ch = max(chips, key=lambda c: len(chips[c])); V = {}; sl = []
    for (s, y, m), r in R.items():
        if s != st or r is None or TS.chip(r) != ch: continue
        mv = TW.month_value(r)
        if mv: V[(y, m)] = mv[0]; sl += r['sl']
    s = abs(float(np.median(sl))); d = {}
    for m in (5, 7, 9, 11):
        base = [V[(y, m)] for y in (2021, 2024) if (y, m) in V]
        if (2022, m) in V and base: d[m] = s * (V[(2022, m)] - float(np.mean(base)))
    return (float(np.mean(list(d.values()))), d) if len(d) >= 2 else None
stations = sorted({k[0] for k in R}, key=lambda s: int(s.replace('stars', '')))
lat = lambda st: float(geo[st]['latitude']) if st in geo and geo[st]['latitude'] else float('nan')
if south is None: south = [st for st in stations if lat(st) < 0]; north = [st for st in stations if lat(st) >= 30]
F = {st: d2(st) for st in stations}
print(' '.join(sys.argv[1:]))
print('latitude  station     D2       May   Jul   Sep   Nov of 2022 (hundredths of a magnitude)')
for st in sorted([s for s in stations if F[s]], key=lat):
    print(f'{lat(st):+7.2f}  {st:<10} {F[st][0]:+.3f}   ' + ' '.join(f'{100 * F[st][1][m]:+5.0f}' if m in F[st][1] else '    .' for m in (5, 7, 9, 11)) + ('   south of the sample' if st in south else '   north of the sample' if st in north else ''))
s = np.array([F[st][0] for st in south if F.get(st)]); n = np.array([F[st][0] for st in north if F.get(st)])
print(f'\nU6. southern photometers with the figure: {len(s)}; D2 at -0.10 or below: {int(np.sum(s <= -0.10))} ({100 * np.mean(s <= -0.10) if len(s) else float("nan"):.0f} in 100); middle {np.median(s) if len(s) else float("nan"):+.3f}')
print(f'U7. northern photometers with the figure: {len(n)}; D2 within 0.10 of nothing: {int(np.sum(np.abs(n) < 0.10))}; at -0.10 or below: {int(np.sum(n <= -0.10))}; middle {np.median(n) if len(n) else float("nan"):+.3f}')
