# A look, after the 2025 sheet was scored, at what goes with the last tenth of the night being the darkest: the month,
# the kind of place, and where the Milky Way stands. Nothing here was sealed; both years had been seen when it was written.
# Reads cache/nights<YEAR>.pkl (years_cache.py). Usage: months_look.py 2024 2025 [...]
import sys, pickle
import numpy as np
N = []
for y in sys.argv[1:]:
    for c in pickle.load(open(f'/home/agent1/night/cache/nights{y}.pkl', 'rb')): c['y'] = int(y); N.append(c)
years = sorted({c['y'] for c in N})
def pct(v): return f'{100 * np.mean(v):.0f}' if len(v) else '-'
print('A. by month, all places: cleaned nights / last tenth the darkest')
for y in years:
    print(f'{y}: ' + ' '.join(f"{m}:{sum(1 for c in N if c['y'] == y and c['d'].month == m)}/{sum(1 for c in N if c['y'] == y and c['d'].month == m and c['tenth'] == 9)}" for m in range(1, 13)))
print('\nB. the same by kind of place (northern places only for between and dark; Arkaroola apart)')
for k in ('lit', 'between', 'dark'):
    for y in years:
        S = [c for c in N if c['y'] == y and c['cls'] == k and c['lat'] > 0]
        print(f'{k:<8}{y}: ' + ' '.join(f"{m}:{sum(1 for c in S if c['d'].month == m)}/{sum(1 for c in S if c['d'].month == m and c['tenth'] == 9)}" for m in range(1, 13)))
for y in years:
    S = [c for c in N if c['y'] == y and c['st'] == 'stars477']
    print(f'Arkaroola {y}: ' + ' '.join(f"{m}:{sum(1 for c in S if c['d'].month == m)}/{sum(1 for c in S if c['d'].month == m and c['tenth'] == 9)}" for m in range(1, 13)))
print('\nC. where the Milky Way stands. For each night: the tenth at whose middle the point overhead is furthest from the plane of the Milky Way.')
print('   nights on which that tenth is the last / of them, last tenth the darkest; and the other nights / of them, last tenth the darkest')
for k in ('lit', 'between', 'dark', 'all'):
    for y in years + ['both']:
        S = [c for c in N if (k == 'all' or c['cls'] == k) and (y == 'both' or c['y'] == y)]
        a = [c['tenth'] == 9 for c in S if int(np.argmax(c['gb'])) == 9]; b = [c['tenth'] == 9 for c in S if int(np.argmax(c['gb'])) != 9]
        print(f'   {k:<8}{y}: Milky Way furthest at the end: {len(a)} nights, last tenth darkest on {sum(a)} ({pct(a)} in 100); otherwise {len(b)} nights, {sum(b)} ({pct(b)} in 100)')
print('\nD. a finer cut: how far from the plane the point overhead is in the last tenth, less the most it is in the nine before (degrees)')
edges = [(-90, -30), (-30, -10), (-10, 0), (0, 10), (10, 90)]
for k in ('lit', 'between', 'dark'):
    for lo, hi in edges:
        S = [c for c in N if c['cls'] == k and lo <= c['gb'][9] - max(c['gb'][:9]) < hi]
        print(f'   {k:<8}{lo:>4} to {hi:<4}: {len(S):>3} nights, last tenth the darkest on {sum(c["tenth"] == 9 for c in S):>3} ({pct([c["tenth"] == 9 for c in S])} in 100); darkest tenth in the second half {pct([c["tenth"] >= 5 for c in S])}')
print('\nE. does the darkest tenth follow the Milky Way? the tenth furthest from the plane against the darkest tenth: within one tenth of each other, in 100')
for k in ('lit', 'between', 'dark'):
    for y in years:
        S = [c for c in N if c['cls'] == k and c['y'] == y]
        print(f"   {k:<8}{y}: {pct([abs(int(np.argmax(c['gb'])) - c['tenth']) <= 1 for c in S])} of {len(S)}; correlation between the ten means and the ten distances, middle night: {np.median([np.corrcoef(c['mt'], c['gb'])[0, 1] for c in S]):+.2f}")
print('\nF. the months in which the Milky Way is furthest from overhead at the end of the night (share of cleaned nights, northern places), by month')
for y in years:
    S = [c for c in N if c['y'] == y and c['lat'] > 0]
    print(f'{y}: ' + ' '.join(f"{m}:{pct([int(np.argmax(c['gb'])) == 9 for c in S if c['d'].month == m])}" for m in range(1, 13)))
print('\nG. September and its neighbours, northern places: darkest tenth by count (tenths 1 to 10), both years')
for m in (7, 8, 9, 10, 11, 12, 1):
    S = [c for c in N if c['lat'] > 0 and c['d'].month == m]
    print(f'   month {m:>2}: {len(S):>3} nights; ' + ' '.join(str(sum(1 for c in S if c['tenth'] == j)) for j in range(10)) + f"; Milky Way furthest in tenth (middle night) {int(np.median([int(np.argmax(c['gb'])) for c in S])) + 1 if S else '-'}")
print('\nH. each place, both years: nights / last tenth darkest when the Milky Way is furthest at the end / otherwise')
for st in sorted({c['st'] for c in N}, key=lambda s: ['lit', 'between', 'dark'].index([c['cls'] for c in N if c['st'] == s][0])):
    S = [c for c in N if c['st'] == st]; a = [c['tenth'] == 9 for c in S if int(np.argmax(c['gb'])) == 9]; b = [c['tenth'] == 9 for c in S if int(np.argmax(c['gb'])) != 9]
    print(f"   {S[0]['name']:<20}{S[0]['cls']:<8}{len(S):>3} nights; furthest at the end {sum(a)} of {len(a)}; otherwise {sum(b)} of {len(b)}")
