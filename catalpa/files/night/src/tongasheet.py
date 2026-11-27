# The lines of the seventh sheet (expectations-tonga.md): was the twilight overhead brighter in the southern hemisphere in
# 2022 and 2023, the two years after the Hunga Tonga eruption of 15 January 2022, than in the year before and the year after?
# Reads files of monthly twilight reductions made by twilight.py's reduce().
# Usage: tongasheet.py FILE.pkl [FILE.pkl ...]
#
# The figure D, for one instrument (a station and the chip with the most months): take the months of January, March,
# May, July, September and November that it has in every one of the four years 2021 to 2024 (three such months or more
# are needed); take each month's twilight figure (twilight.py: the Sun's altitude when the reading passes 14.0) about
# its own mean over the four years; average over the months within each year; then
#       D = slope x [ (2022 + 2023)/2 - (2021 + 2024)/2 ]      in magnitudes
# with the instrument's own twilight slope (magnitudes a degree, its size). A steady drift of the instrument cancels
# in D exactly. Negative: the twilight read brighter in 2022 and 2023.
import sys, pickle, csv, importlib.util
import numpy as np
spec = importlib.util.spec_from_file_location('twilight', '/home/agent1/night/src/twilight.py'); TW = importlib.util.module_from_spec(spec); spec.loader.exec_module(TW)
SIX = (1, 3, 5, 7, 9, 11); YEARS = (2021, 2022, 2023, 2024)
geo = {r['name']: r for r in csv.DictReader(open('/home/agent1/night/lit/src/p3_stars4all_geolist.csv'), delimiter=';')}
def chip(r): return (r.get('mac') or '')[-8:]
def figure(R, st):
    chips = {}
    for (s, y, m), r in R.items():
        if s == st and r is not None and m in SIX and TW.month_value(r): chips.setdefault(chip(r), []).append((y, m))
    if not chips: return None
    ch = max(chips, key=lambda c: len(chips[c])); V = {}; sl = []
    for (s, y, m), r in R.items():
        if s != st or r is None or chip(r) != ch or m not in SIX or y not in YEARS: continue
        mv = TW.month_value(r)
        if mv: V[(y, m)] = mv[0]; sl += r['sl']
    months = [m for m in SIX if all((y, m) in V for y in YEARS)]
    if len(months) < 3: return None
    s = abs(float(np.median(sl))); A = {y: s * float(np.mean([V[(y, m)] - np.mean([V[(yy, m)] for yy in YEARS]) for m in months])) for y in YEARS}
    return dict(D=(A[2022] + A[2023]) / 2 - (A[2021] + A[2024]) / 2, A=A, months=months, name=next((r['name'] for k, r in R.items() if k[0] == st and r and r.get('name')), ''))
if __name__ == '__main__':
    R = {}; META = None
    for fn in sys.argv[1:]:
        X = pickle.load(open(fn, 'rb')); m = X.pop('meta', None); META = m if m and 'south' in m else META; R.update(X)
    stations = sorted({k[0] for k in R}, key=lambda s: int(s.replace('stars', ''))); F = {}
    for st in stations:
        f = figure(R, st)
        if f: f['lat'] = float(geo[st]['latitude']) if st in geo and geo[st]['latitude'] else float('nan'); f['lon'] = float(geo[st]['longitude']) if st in geo and geo[st]['longitude'] else float('nan'); F[st] = f
    print(' '.join(sys.argv[1:]) + f': {len(stations)} stations, {len(F)} with the figure')
    print('latitude  longitude  station     D        2021  2022  2023  2024 (hundredths of a magnitude about the four years\' mean)   months   place')
    for st, f in sorted(F.items(), key=lambda kv: kv[1]['lat']):
        print(f"{f['lat']:+7.2f}  {f['lon']:+8.2f}  {st:<10} {f['D']:+.3f}   " + ' '.join(f"{100 * f['A'][y]:+5.0f}" for y in YEARS) + f"      {len(f['months'])}     {f['name'][:50]}")
    def lines(S, N, label):
        print(f'\n{label}')
        s = np.array([F[st]['D'] for st in S if st in F]); n = np.array([F[st]['D'] for st in N if st in F])
        print(f'U1. southern instruments with the figure: {len(s)}; at -0.08 or below: {int(np.sum(s <= -0.08))} ({100 * np.mean(s <= -0.08):.0f} in 100)' if len(s) else 'U1. no southern instrument with the figure')
        if len(s): print(f'U2. their middle figure: {np.median(s):+.3f}; from {s.min():+.3f} to {s.max():+.3f}')
        print(f'U3. northern instruments with the figure: {len(n)}; at -0.08 or below: {int(np.sum(n <= -0.08))}; within 0.05 of nothing: {int(np.sum(np.abs(n) < 0.05))}; middle {np.median(n):+.3f}' if len(n) else 'U3. no northern instrument with the figure')
        both = [st for st in S if st in F and max(F[st]['A'][2022], F[st]['A'][2023]) < min(F[st]['A'][2021], F[st]['A'][2024])]
        if len(s): print(f'U4. southern instruments at which 2022 and 2023 are each below both 2021 and 2024: {len(both)} of {len(s)} ({100 * len(both) / len(s):.0f} in 100)')
    if META: lines(META['south'], META['north'], 'the sample of the seventh sheet')
    else:
        S = [st for st in F if F[st]['lat'] < 0]; N = [st for st in F if F[st]['lat'] >= 30]
        lines(S, N, 'every instrument in the files given: south of the equator, and north of 30 degrees')
        mid = [st for st in F if 0 <= F[st]['lat'] < 30]; print('between the equator and 30 north: ' + ', '.join(f"{st} {F[st]['D']:+.3f}" for st in mid))
