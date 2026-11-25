"""After the fact (not sealed): the two published lists of the dial's months side by side.
F = Freeth 2014's model as coded (51 cells); IJ = Iversen and Jones 2019, Table 5 (49 cells). They differ in four
entries: lunar 214 (F) against 213 (IJ); solar 207 (F) against 196 (IJ).
Part 1, cycles 0 to 3, from the JPL tables: latitudes at full and new moon against the dial's limits in degrees.
Part 2, all cycles, from NASA's catalogue by its lunation numbers.
Part 3, the glyphs read on the fragments (Iversen and Jones's unbracketed entries) on their own.
usage: two_lists.py DATADIR CATDIR [CATDIR ...]     (run under -I through runpy)"""
import sys, os, re, json, glob
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
import numpy as np, dial, mech, ij2019
DATA, CATS = sys.argv[1], sys.argv[2:]
pat = re.compile(r'^\s*(\d{5})\s+(-?\d{4})\s+([A-Z][a-z]{2})\s+(\d{2})\s+(\d{2}):(\d{2}):(\d{2})\s+(-?\d+)\s+(-?\d+)\s+(\d+)\s+(\S+)\s+\S+\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)(?:\s+(-?\d+\.\d+))?')


def read_cat(prefix, add):
    rows = {}
    for f in sorted(f for d in CATS for f in glob.glob(os.path.join(d, prefix + '*.html'))):
        for line in open(f, encoding='utf-8', errors='replace'):
            m = pat.match(re.sub(r'<[^>]*>', '', line))
            if m: rows[int(m.group(9)) + add] = dict(date=f'{int(m.group(2))} {m.group(3)} {m.group(4)}', kind=m.group(11)[0], gamma=float(m.group(12)))
    return rows


fl, fs = dial.glyph_months()
LISTS = {'F': (sorted(fl), sorted(fs)), 'IJ': (ij2019.LUNAR, ij2019.SOLAR), 'read': (ij2019.LUNAR_ATTESTED, ij2019.SOLAR_ATTESTED)}
moon = mech.read(os.path.join(DATA, 'moon_then.txt')); sun = mech.read(os.path.join(DATA, 'sun_then.txt'))
FM, NM = dial.number(dial.syzygies(moon, sun))
LE, SE = read_cat('LE', 27257), read_cat('SE', 27256)

print('Part 1. From the JPL tables, cycles 0 to 3: lunar months with the full moon within 1.43 deg | solar months with the new moon between -0.51 and +1.43 deg')
for name in ('F', 'IJ', 'read'):
    L, S = LISTS[name]
    for j in range(4):
        b = 223 * j
        lf = [(n, round(FM[b + n], 2)) for n in L if abs(FM[b + n]) > dial.LIM_N]; sf = [(n, round(NM[b + n], 2)) for n in S if not (-dial.LIM_S <= NM[b + n] <= dial.LIM_N)]
        print(f'  {name:4s} cycle {j}: {len(L) - len(lf)} of {len(L)} (outside: {lf}) | {len(S) - len(sf)} of {len(S)} (outside: {sf})')
print('  the four months in dispute, latitude at full moon (213, 214) and at new moon (196, 207), cycles 0 to 3:')
for n, d in ((213, FM), (214, FM), (196, NM), (207, NM)):
    print(f'    {n}:', [round(d[223 * j + n], 2) for j in range(4)])

print('\nPart 2. From the catalogue, every cycle: A = lunar months with a lunar eclipse of any kind (Aum = partial or total); U = partial or total lunar eclipses in months without a lunar glyph; S = solar months with a solar eclipse')
out = {}
for name in ('F', 'IJ', 'read'):
    L, S = LISTS[name]; rows = []
    for j in range(123):
        b = 223 * j
        um = [n for n in range(1, 224) if b + n in LE and LE[b + n]['kind'] in 'PT']
        rows.append(dict(cycle=j, A=sum(b + n in LE for n in L), Aum=sum(n in um for n in L), umbral=len(um), U=sum(n not in L for n in um),
                         S=sum(b + n in SE for n in S), solar_all=sum(b + n in SE for n in range(1, 224)),
                         A_none=[n for n in L if b + n not in LE], S_none=[n for n in S if b + n not in SE]))
    out[name] = rows
    first = lambda cond: next((r['cycle'] for r in rows if cond(r)), None)
    print(f'  {name}: {len(L)} lunar, {len(S)} solar')
    print('    cycle: A (Aum), U, S :', '; '.join(f"{r['cycle']}: {r['A']} ({r['Aum']}), {r['U']}, {r['S']}" for r in rows if r['cycle'] in (0, 1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 25, 30, 35, 40, 50, 60, 70, 122)))
    print(f"    first cycle with A at most half: {first(lambda r: r['A'] <= len(L) // 2)}; A = 0: {first(lambda r: r['A'] == 0)}; Aum = 0: {first(lambda r: r['Aum'] == 0)}; "
          f"S at most half: {first(lambda r: r['S'] <= len(S) // 2)}; S = 0: {first(lambda r: r['S'] == 0)}")
    if name != 'read':
        print(f"    first cycle with A below 37: {first(lambda r: r['A'] < 37)}; below 30: {first(lambda r: r['A'] < 30)}; S below 28: {first(lambda r: r['S'] < 28)}; below 20: {first(lambda r: r['S'] < 20)}; "
              f"U at least 1, 3, 5, 10: {[first(lambda r, k=k: r['U'] >= k) for k in (1, 3, 5, 10)]}; U = all the cycle's partial or total eclipses: {first(lambda r: r['U'] == r['umbral'])}")
        print('    months without an eclipse, cycles 0 to 8: lunar', [r['A_none'] for r in rows[:9]], 'solar', [r['S_none'] for r in rows[:9]])
        b = 0
        left = [(n, SE[n]['kind'], SE[n]['gamma']) for n in range(1, 224) if n in SE and n not in S]
        print(f"    cycle 0: {sum(n in SE for n in range(1, 224))} solar eclipses, {len(left)} in months without a solar glyph, gamma {min(x[2] for x in left):+.2f} to {max(x[2] for x in left):+.2f}")
print('  the four months in dispute in the catalogue, cycles 0 to 5 (N penumbral, P partial, T total; for solar P partial, A annular, T total, H hybrid; - none):')
for n, d in ((213, LE), (214, LE), (196, SE), (207, SE)):
    print(f'    {n}:', ' '.join(f"{d[223 * j + n]['kind']}({d[223 * j + n]['gamma']:+.2f})" if 223 * j + n in d else '-' for j in range(6)))
json.dump(out, open(os.path.join(HERE, 'two_lists.json'), 'w'))
