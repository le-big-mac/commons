"""Score the sealed sheet of the dial follow-up by the letter, and list the glyph months that fail. usage: dial_score.py DATADIR"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
import numpy as np, dial, mech
DATA = sys.argv[1]
lunar, solar = dial.glyph_months()
res = {w: dial.syzygies(mech.read(os.path.join(DATA, f'moon_{w}.txt')), mech.read(os.path.join(DATA, f'sun_{w}.txt'))) for w in ('then', 'now')}
FM, NM = dial.number(res['then'])
T = {j: dial.tally(FM, NM, lunar, solar, j) for j in range(4)}
sh = []
for j in range(4):
    s, r = dial.fit_shift({k - 223 * j: v for k, v in FM.items() if 223 * j < k <= 223 * j + 223}, {k - 223 * j: v for k, v in NM.items() if 223 * j < k <= 223 * j + 223}, range(1, 224))
    sh.append(float(s))
rate = float(np.polyfit(np.arange(4), sh, 1)[0])
ft = res['then']['full'][0]; fn = res['now']['full'][0]
syn = 0.5 * (np.polyfit(np.arange(len(ft)), ft, 1)[0] + np.polyfit(np.arange(len(fn)), fn, 1)[0])
gap = (fn[0] - ft[0]) / syn
FM2, NM2 = dial.number(res['now'], first_full_index=1 + int(round(gap)))
last = max(FM2)
FMr = {(n - 1) % 223 + 1: FM2[n] for n in range(last - 222, last + 1) if n in FM2}
NMr = {(n - 1) % 223 + 1: NM2[n] for n in range(last - 222, last + 1) if n in NM2}
Tn = dial.tally(FMr, NMr, lunar, solar, 0)
d3 = sum(-0.6 <= NM[n] <= 1.5 for n in solar)
rows = dial.survival(sh[0] - 0.5 * rate, rate, lunar, solar)
first30 = next(j for j, lun, sol in rows if lun < 30)
L = [
 ('D1', 0.70, T[0]['lun_ok'] >= 33, f"cycle 0: {T[0]['lun_ok']} of 38 lunar glyph months are true possibilities"),
 ('D2', 0.75, T[0]['umb'] - T[0]['umb_hit'] <= 1, f"cycle 0: {T[0]['umb_hit']} of {T[0]['umb']} umbral full moons on a lunar glyph month"),
 ('D3', 0.65, d3 >= 23, f"cycle 0: {d3} of 28 solar glyph months between -0.6 and +1.5 deg"),
 ('D4', 0.55, abs(sh[0]) <= 2, f"shift in cycle 0: {sh[0]:+.2f} units"),
 ('D5', 0.80, all(abs(T[j]['lun_ok'] - T[0]['lun_ok']) <= 2 for j in (1, 2, 3)), f"cycles 1 to 3: {[T[j]['lun_ok'] for j in (1, 2, 3)]}"),
 ('D6', 0.85, Tn['lun_ok'] == 0 and Tn['sol_ok'] == 0, f"to today: {Tn['lun_ok']} of 38 lunar, {Tn['sol_ok']} of 28 solar"),
 ('D7', 0.70, -0.69 <= rate <= -0.50, f"the shift moves {rate:+.3f} units a cycle (sealed: between -0.50 and -0.69)"),
 ('D8', 0.60, 10 <= first30 <= 22, f"first cycle with fewer than 30 of 38: cycle {first30}"),
]
held = 0; brier = 0.0
for name, odds, ok, what in L:
    ok = bool(ok); held += ok; brier += (odds - ok) ** 2
    print(f'{name}  {int(odds * 100):3d}%  {"held  " if ok else "FAILED"}  {what}')
print(f'\n{held} of {len(L)} held; Brier {brier / len(L):.4f} (always saying 50%: 0.2500)')
print('\nGlyph months that fail in cycle 0 (month: model distance from node point in units, true latitude):')
for n in sorted(lunar):
    if abs(FM[n]) > dial.LIM_N: print(f'  lunar {n}: {lunar[n][0]:+d} at {lunar[n][1]}, latitude {FM[n]:+.2f}')
for n in sorted(solar):
    if not (-dial.LIM_S <= NM[n] <= dial.LIM_N): print(f'  solar {n}: {solar[n][0]:+d} at {solar[n][1]}, latitude {NM[n]:+.2f}')
print('New moons inside the dial\'s limits without a solar glyph in cycle 0:', [(n, round(NM[n], 2)) for n in range(1, 224) if -dial.LIM_S <= NM[n] <= dial.LIM_N and n not in solar])
print('Full moons within 1.43 deg without a lunar glyph in cycle 0:', [(n, round(FM[n], 2)) for n in range(1, 224) if abs(FM[n]) <= dial.LIM_N and n not in lunar])
print('How many solar eclipses of any kind (new moon within 1.5 deg) in cycle 0:', sum(abs(NM[n]) < 1.5 for n in range(1, 224)), '; on a solar glyph month:', sum(abs(NM[n]) < 1.5 and n in solar for n in range(1, 224)))
print('Shifts in cycles 0 to 3 (units):', [round(x, 2) for x in sh], '; best-centred cycle by the straight line:', round(-np.polyfit(np.arange(4), sh, 1)[1] / rate, 2))
half_l = next(j for j, lun, sol in rows if lun <= 19); half_s = next(j for j, lun, sol in rows if sol <= 14)
zero_l = next(j for j, lun, sol in rows if lun == 0); zero_s = next(j for j, lun, sol in rows if sol == 0)
print(f'By the model\'s geometry: lunar glyph months down to half by cycle {half_l} ({half_l * 18.03:.0f} years), to none by cycle {zero_l} ({zero_l * 18.03:.0f} years); solar to half by cycle {half_s} ({half_s * 18.03:.0f} years), to none by cycle {zero_s} ({zero_s * 18.03:.0f} years)')
