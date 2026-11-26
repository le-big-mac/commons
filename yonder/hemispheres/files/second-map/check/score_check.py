"""Task A4: score the twelve lines of the sealed sheet from the checker's own numbers only
(out/halves.json: hard-edged halves and totals; out/search2-*.json: hard-edged best centres by the checker's search).
usage: python -I score_check.py CHECK_OUT_DIR"""
import sys, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import chk
od = sys.argv[1]
Hh = json.load(open(f'{od}/halves.json'))
S = {n: json.load(open(f'{od}/search2-{n}.json')) for n in ('g2-2020', 'g1-2000', 'g1-2020')}
L2 = {y: Hh[f'g2-{y}']['L'] for y in (2015, 2020, 2025, 2030)}; L1 = {y: Hh[f'g1-{y}']['L'] for y in (2000, 2010, 2020)}
b20 = S['g2-2020']['best']; b00 = S['g1-2000']['best']
d20 = chk.km(b20['lat'], b20['lon'], 52.37, 12.68)
r20 = S['g2-2020']['regions']; r00 = S['g1-2000']['regions']
lines = [
 ('E1', .75, L2[2020] > 0, f"L = {L2[2020]:+.4f} points, {Hh['g2-2020']['diff_millions']:+.2f} million"),
 ('E2', .65, b20['lat'] > 48.5, f"best {b20['lat']:.2f} N, {b20['lon']:.2f} E; best south of 47.5 N is {100 * (r20['alps_south_of_47p5']['share'] - b20['share']):+.4f} points behind, best between 47.5 and 48.5 {100 * (r20['between_47p5_and_48p5']['share'] - b20['share']):+.4f}"),
 ('E3', .45, d20 < 300, f"{d20:.0f} km; the Palatinate summit (332 km away) is 0.037 points behind (out/search-g2-2020.out)"),
 ('E4', .85, L2[2015] < L2[2020] < L2[2025] < L2[2030], ', '.join(f'{L2[y]:+.4f}' for y in L2)),
 ('E5', .55, L2[2015] > 0, f"L = {L2[2015]:+.4f}"),
 ('E6', .80, 0.9250 <= b20['share'] <= 0.9290, f"{100 * b20['share']:.4f}% (hard edge)"),
 ('E7', .75, L1[2000] < 0, f"L = {L1[2000]:+.4f}"),
 ('E8', .70, b00['lat'] < 47.5, f"best {b00['lat']:.2f} N, {b00['lon']:.2f} E; best north of 48.5 N is {100 * (r00['north_of_48p5']['share'] - b00['share']):+.4f} points behind, best between 47.5 and 48.5 {100 * (r00['between_47p5_and_48p5']['share'] - b00['share']):+.4f}"),
 ('E9', .55, L1[2020] > 0, f"L = {L1[2020]:+.4f}"),
 ('E10', .85, L1[2000] < L1[2010] < L1[2020], ', '.join(f'{L1[y]:+.4f}' for y in L1)),
 ('E11', .85, all(abs(v) < 0.3 for v in list(L1.values()) + list(L2.values())), f"largest |L| {max(abs(v) for v in list(L1.values()) + list(L2.values())):.4f}"),
 ('E12', .85, 7.78e9 <= Hh['g2-2020']['total'] <= 7.90e9, f"{Hh['g2-2020']['total'] / 1e9:.4f}"),
]
b = 0
for k, p, ok, what in lines:
    b += (p - (1 if ok else 0)) ** 2
    print(f"{k:4s} {int(100 * p)}%  {'held' if ok else 'FAILED'}  {what}")
print(f"{sum(1 for l in lines if l[2])} of {len(lines)} held; Brier score {b / len(lines):.4f}")
print('totals against GHS-POP (UN 2022): ' + '; '.join(f"{y}: {100 * (Hh[f'g1-{y}']['total'] / Hh[f'ghs-{y}']['total'] - 1):+.2f}%" for y in (2000, 2010, 2020)))
# if stricter readings of the sheet's rule left lines unscored
def brier(drop): 
    ls = [(p, ok) for k, p, ok, w in lines if k not in drop]; return sum((p - 1) ** 2 for p, ok in ls) / len(ls), len(ls)
for drop, why in ((('E10',), 'the 2010 grid of the older series set aside (3% rule against a higher UN figure)'), (('E7', 'E8'), 'the 2000 grid of the older series set aside (not readable by the sealed popgrid.py)'), (('E7', 'E8', 'E10'), 'both')):
    bb, n = brier(drop); print(f'   Brier over {n} lines with {", ".join(drop)} unscored ({why}): {bb:.4f}')
