"""After the sealed sheet (not sealed): by the model's own geometry with the node points moved by the fitted shift
and drift, cycle by cycle: glyph months still inside the limits, and umbral full moons the dial would miss.
Writes survival.json for the figure. usage: dial_after.py"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np, dial, eym
lunar, solar = dial.glyph_months()
SH0, RATE = 0.75, 0.58            # from dial_score.out: the shift in cycle 0 and its drift per cycle (units)
UMB = np.degrees(np.arcsin(1.0 / dial.INC)) * 446 / 360        # 1.0 deg of latitude in units from the node: 13.9
rows = []
for j in range(0, 141):
    s = SH0 + RATE * j
    lun = sum(abs(dial.model_lat(n, 'full', s)) <= dial.LIM_N for n in lunar)
    sol = sum(-dial.LIM_S <= dial.model_lat(n, 'new', s) <= dial.LIM_N for n in solar)
    umb = [n for n in range(1, 224) if abs(dial.model_lat(n, 'full', s)) < 1.0]
    missed = [n for n in umb if n not in lunar]
    rows.append(dict(cycle=j, years=round(j * 18.03, 1), lunar=int(lun), solar=int(sol), umbral=len(umb), umbral_missed=len(missed), first_missed=missed[:4]))
json.dump(rows, open(os.path.join(HERE, 'survival.json'), 'w'))
print(f'umbral zone: {UMB:.1f} units either side of a node point; shift {SH0} + {RATE} per cycle')
print('cycle (years after 205 BC): lunar glyph months inside the limit; solar inside the limits; umbral full moons, of which on no glyph month')
for r in rows:
    if r['cycle'] <= 20 or r['cycle'] % 5 == 0:
        print(f"  {r['cycle']:3d} ({r['years']:6.0f}): {r['lunar']:2d} of 38; {r['solar']:2d} of 28; {r['umbral']:2d}, {r['umbral_missed']:2d} missed {r['first_missed'] if r['umbral_missed'] and r['cycle'] <= 12 else ''}")
first = {k: next(r['cycle'] for r in rows if r['umbral_missed'] >= k) for k in (1, 3, 5, 10)}
print('first cycle in which the dial misses at least 1, 3, 5, 10 umbral eclipses:', first, '=', {k: round(v * 18.03) for k, v in first.items()}, 'years')
