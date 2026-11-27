# Each place's usual level (the middle of its cleaned nights' middle readings, by the file's own formula), year by year,
# and the count of cleaned nights. Reads cache/nights<YEAR>.pkl. Usage: levels.py 2022 2023 2024 2025
import sys, pickle, importlib.util
import numpy as np
spec = importlib.util.spec_from_file_location('dawnlib', '/home/agent1/night/src/dawnlib.py'); D = importlib.util.module_from_spec(spec); spec.loader.exec_module(D)
# The nights are those of cache_placed/ (the photometer stars477 placed at Arkaroola in 2022 and early 2023), with the
# nights more than 1 magnitude from the station's 2024 level left out, as on the page.
years = [int(y) for y in sys.argv[1:]]; N = {y: pickle.load(open(f'/home/agent1/night/cache_placed/nights{y}.pkl', 'rb')) for y in years}
_l = {st: float(np.median([c['lev'] for c in N[2024] if c['st'] == st])) for st in {c['st'] for c in N[2024]}} if 2024 in N else {}
if _l: N = {y: [c for c in N[y] if abs(c['lev'] - _l[c['st']]) <= 1.0] for y in N}
order = [s for k in ('lit', 'between', 'dark') for s in D.CLASS if D.CLASS[s] == k]
print('usual level by year (cleaned nights in brackets); larger is darker')
print(f"{'':<20}" + ''.join(f'{y:<14}' for y in years))
L = {}
for s in order:
    row = f'{D.NAME[s]:<20}'
    for y in years:
        v = [c['lev'] for c in N[y] if c['st'] == s]; L[(s, y)] = float(np.median(v)) if v else float('nan'); row += (f'{L[(s, y)]:5.2f} ({len(v):>2})    ' if v else f"{'-':<14}")
    print(row)
print('\nmiddle value over the places of each kind, of the level less that place\'s 2024 level')
for k in ('lit', 'between', 'dark'):
    print(f'{k:<8}' + '  '.join(f"{y}: {np.nanmedian([L[(s, y)] - L[(s, 2024)] for s in order if D.CLASS[s] == k]):+.2f}" for y in years if 2024 in years))
if 2022 in years and 2024 in years:
    d = [(D.NAME[s], L[(s, 2022)] - L[(s, 2024)]) for s in order if D.CLASS[s] == 'dark']
    print('\nthe four dark places, 2022 less 2024: ' + '; '.join(f'{n} {x:+.2f}' for n, x in d) + f"; darker in 2022 at {sum(1 for n, x in d if x > 0)} of {sum(1 for n, x in d if x == x)}")
# the same months only: levels from the months that have cleaned nights in every year given, place by place
print('\nthe same, using only the calendar months in which the place has cleaned nights in every one of the years')
for s in order:
    ms = set(range(1, 13))
    for y in years: ms &= {c['d'].month for c in N[y] if c['st'] == s}
    row = f'{D.NAME[s]:<20}'
    for y in years:
        v = [c['lev'] for c in N[y] if c['st'] == s and c['d'].month in ms]; row += (f'{np.median(v):5.2f} ({len(v):>2})    ' if v else f"{'-':<14}")
    print(row + f'months {sorted(ms)}')
