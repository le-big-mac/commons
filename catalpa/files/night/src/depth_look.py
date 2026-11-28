# After the ninth sheet was scored: its Brier score, and one reading of the profile that can be set against what is
# in print. If the haze left the directly lit sky overhead as it was and made the light that has been scattered more
# than once brighter by one fixed factor E, then the brightening at a depth d is 1 + f(d) (E - 1), where f(d) is the
# share of the ordinary zenith light at that depth that has been scattered more than once. E is taken from the level
# stretch at 9 to 11 degrees, where f is taken to be 1; f at the other depths follows. A reading, not a measurement.
import pickle, importlib.util, io, contextlib
import numpy as np
B = '/home/agent1/night/'
spec = importlib.util.spec_from_file_location('depth', B + 'src/depth.py'); DP = importlib.util.module_from_spec(spec); spec.loader.exec_module(DP)
with contextlib.redirect_stdout(io.StringIO()): depths, PS, mid, nm = DP.tables(B + 'cache2/depth.pkl')
odds = dict(X1=.85, X2=.65, X3=.60, X4=.25, X5=.65, X6=.70, X7=.60, X8=.55, X9=.75, X10=.70); verd = {}
for line in open(B + 'depth.out', encoding='utf-8'):
    if line[:1] == 'X' and '.' in line[:4]: verd[line.split('.')[0]] = line.rstrip().rsplit(': ', 1)[-1]
print('the ninth sheet: ' + ', '.join(f'{k} {verd[k]}' for k in odds))
sc = [k for k in odds if verd[k] in ('held', 'failed')]
print(f"lines scored: {len(sc)}; held {sum(1 for k in sc if verd[k] == 'held')}; my odds expected {sum(odds[k] if verd[k] == 'held' or True else 0 for k in sc):.1f} to hold; Brier score {np.mean([(odds[k] - (verd[k] == 'held')) ** 2 for k in sc]):.3f} (0.250 for odds of one in two)")
print('\nthe middle of the southern places by depth: magnitudes, the factor by which the twilight was brighter, places')
for d in depths: print(f'   {d:4g}°   {mid[d][0]:+.3f}   x{10 ** (-0.4 * mid[d][0]):.2f}   {mid[d][1]}')
E = float(np.mean([10 ** (-0.4 * mid[d][0]) for d in (9.0, 10.0, 11.0)]))
print(f'\nthe level stretch (9, 10 and 11 degrees): the factor E = {E:.2f}, which is {-2.5 * np.log10(E):+.2f} magnitude')
print('the share f of the ordinary zenith light that would have to be light scattered more than once, if E applies to that light alone:')
for d in (3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0): print(f'   {d:g}°   {(10 ** (-0.4 * mid[d][0]) - 1) / (E - 1):.2f}')
print('the same from each place that gives all of 4 to 10 degrees (E from its own 9 and 10 degrees): the range of f across places')
rows = []
for st in DP.SOUTH:
    if any(PS[(st, d)] is None for d in (4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0)): continue
    e = np.mean([10 ** (-0.4 * PS[(st, d)]) for d in (9.0, 10.0)]); rows.append([(10 ** (-0.4 * PS[(st, d)]) - 1) / (e - 1) for d in (4.0, 5.0, 6.0, 7.0, 8.0)] + [e])
rows = np.array(rows)
for i, d in enumerate((4.0, 5.0, 6.0, 7.0, 8.0)): print(f'   {d:g}°   from {rows[:, i].min():.2f} to {rows[:, i].max():.2f}, middle {np.median(rows[:, i]):.2f}   ({len(rows)} places)')
print(f'   E at those places: from {rows[:, 5].min():.2f} to {rows[:, 5].max():.2f}, middle {np.median(rows[:, 5]):.2f}')
print('\nthe height of the Earth\'s shadow straight overhead, by geometry alone (no bending of the light, no screening by the lower air): ' + ', '.join(f'{d:g}°: {6371 * (1 / np.cos(np.radians(d)) - 1):.0f} km' for d in (3, 4, 5, 6, 7, 8, 9, 10)))
