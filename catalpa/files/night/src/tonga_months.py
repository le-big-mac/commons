# The course of the twilight month by month, for the amendment to the seventh sheet (line U5) and for the record.
# For each instrument: each month's twilight figure less the mean of the same calendar month in 2021 and 2024 (both are
# needed), in magnitudes by the instrument's own slope. Negative: the twilight read brighter.
# Usage: tonga_months.py FILE.pkl [FILE.pkl ...]
import sys, pickle, csv, importlib.util
import numpy as np
spec = importlib.util.spec_from_file_location('tongasheet', '/home/agent1/night/src/tongasheet.py'); TS = importlib.util.module_from_spec(spec); spec.loader.exec_module(TS)
TW = TS.TW; geo = TS.geo; SIX = TS.SIX
R = {}; META = None
for fn in sys.argv[1:]:
    X = pickle.load(open(fn, 'rb')); m = X.pop('meta', None); META = m if m and 'south' in m else META; R.update(X)
def course(st):
    chips = {}
    for (s, y, m), r in R.items():
        if s == st and r is not None and m in SIX and TW.month_value(r): chips.setdefault(TS.chip(r), []).append((y, m))
    if not chips: return None
    ch = max(chips, key=lambda c: len(chips[c])); V = {}; sl = []
    for (s, y, m), r in R.items():
        if s != st or r is None or TS.chip(r) != ch or m not in SIX: continue
        mv = TW.month_value(r)
        if mv: V[(y, m)] = mv[0]; sl += r['sl']
    s = abs(float(np.median(sl)))
    return {(y, m): s * (V[(y, m)] - (V[(2021, m)] + V[(2024, m)]) / 2) for (y, m) in V if y in (2022, 2023) and (2021, m) in V and (2024, m) in V}
stations = sorted({k[0] for k in R}, key=lambda s: int(s.replace('stars', '')))
lat = lambda st: float(geo[st]['latitude']) if st in geo and geo[st]['latitude'] else float('nan')
south = META['south'] if META else [st for st in stations if lat(st) < 0]; north = META['north'] if META else [st for st in stations if lat(st) >= 30]
C = {st: course(st) for st in stations}
print('each month of 2022 and 2023 less the same month of 2021 and 2024, hundredths of a magnitude (negative: a brighter twilight)')
print('latitude  station      2022: Jan  Mar  May  Jul  Sep  Nov   2023: Jan  Mar  May  Jul  Sep  Nov')
for st in sorted([s for s in stations if C[s]], key=lat):
    print(f'{lat(st):+7.2f}  {st:<10}       ' + ' '.join(f'{100 * C[st][(2022, m)]:+4.0f}' if (2022, m) in C[st] else '   .' for m in SIX) + '         ' + ' '.join(f'{100 * C[st][(2023, m)]:+4.0f}' if (2023, m) in C[st] else '   .' for m in SIX))
jan = [C[st][(2022, 1)] for st in south if C.get(st) and (2022, 1) in C[st]]; jul = [C[st][(2022, 7)] for st in south if C.get(st) and (2022, 7) in C[st]]
print(f'\nU5. southern instruments: January 2022 above -0.10 at {sum(1 for x in jan if x > -0.10)} of {len(jan)}; July 2022 at -0.15 or below at {sum(1 for x in jul if x <= -0.15)} of {len(jul)}')
print('for the record, the southern middle by month: 2022 ' + ' '.join(f"{100 * np.median([C[st][(2022, m)] for st in south if C.get(st) and (2022, m) in C[st]]):+4.0f}" if any(C.get(st) and (2022, m) in C[st] for st in south) else '   .' for m in SIX) + ' | 2023 ' + ' '.join(f"{100 * np.median([C[st][(2023, m)] for st in south if C.get(st) and (2023, m) in C[st]]):+4.0f}" if any(C.get(st) and (2023, m) in C[st] for st in south) else '   .' for m in SIX))
print('               the northern middle by month: 2022 ' + ' '.join(f"{100 * np.median([C[st][(2022, m)] for st in north if C.get(st) and (2022, m) in C[st]]):+4.0f}" if any(C.get(st) and (2022, m) in C[st] for st in north) else '   .' for m in SIX) + ' | 2023 ' + ' '.join(f"{100 * np.median([C[st][(2023, m)] for st in north if C.get(st) and (2023, m) in C[st]]):+4.0f}" if any(C.get(st) and (2023, m) in C[st] for st in north) else '   .' for m in SIX))
