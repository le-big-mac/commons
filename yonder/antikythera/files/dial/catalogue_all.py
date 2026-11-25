"""The dial against NASA's catalogue of eclipses for every cycle from 205 BC to today (sealed: expectations-catalogue.md).
Months come from the catalogue's own lunation number: a lunar eclipse is in dial month number + 27257, a solar
eclipse in month number + 27256 (luna_check.out: true of all 357 eclipses of the 76 years where the JPL tables give the month).
usage: catalogue_all.py CATDIR [CATDIR ...]      (run under -I through runpy)"""
import sys, os, re, json, glob
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
import dial
pat = re.compile(r'^\s*(\d{5})\s+(-?\d{4})\s+([A-Z][a-z]{2})\s+(\d{2})\s+(\d{2}):(\d{2}):(\d{2})\s+(-?\d+)\s+(-?\d+)\s+(\d+)\s+(\S+)\s+\S+\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)(?:\s+(-?\d+\.\d+))?')


def read_cat(prefix, add):
    rows = {}
    files = sorted(f for d in sys.argv[1:] for f in glob.glob(os.path.join(d, prefix + '*.html')))
    for f in files:
        for line in open(f, encoding='utf-8', errors='replace'):
            m = pat.match(re.sub(r'<[^>]*>', '', line))
            if not m: continue
            n = int(m.group(9)) + add
            assert n not in rows, (f, n)                 # one eclipse of a kind to a month
            rows[n] = dict(cat=int(m.group(1)), date=f'{int(m.group(2))} {m.group(3)} {m.group(4)}', kind=m.group(11)[0], gamma=float(m.group(12)),
                           umag=float(m.group(14)) if (prefix == 'LE' and m.group(14)) else None)
    cats = sorted(r['cat'] for r in rows.values())
    assert cats == list(range(cats[0], cats[-1] + 1)), 'a gap in the catalogue numbers'
    return rows, len(files)


lunar, solar = dial.glyph_months()
LE, nl = read_cat('LE', 27257); SE, ns = read_cat('SE', 27256)
assert set(r['kind'] for r in LE.values()) <= set('NPT') and set(r['kind'] for r in SE.values()) <= set('PATH')
print(f'{nl} lunar pages, {len(LE)} lunar eclipses, {LE[min(LE)]["date"]} to {LE[max(LE)]["date"]}; {ns} solar pages, {len(SE)} solar eclipses, {SE[min(SE)]["date"]} to {SE[max(SE)]["date"]}')
rows = []
for j in range(0, 123):
    b = 223 * j
    le = {n - b: LE[n] for n in range(b + 1, b + 224) if n in LE}; se = {n - b: SE[n] for n in range(b + 1, b + 224) if n in SE}
    um = [n for n in le if le[n]['kind'] in 'PT']
    rows.append(dict(cycle=j, years=round(j * 18.03, 1), A=sum(n in le for n in lunar), Aum=sum(n in le and le[n]['kind'] in 'PT' for n in lunar),
                     lunar_all=len(le), umbral=len(um), U=sum(n not in lunar for n in um), U_months=sorted(n for n in um if n not in lunar),
                     S=sum(n in se for n in solar), solar_all=len(se), solar_on_glyph=sum(n in solar for n in se),
                     A_none=sorted(n for n in lunar if n not in le), S_none=sorted(n for n in solar if n not in se)))
json.dump(rows, open(os.path.join(HERE, 'catalogue_all.json'), 'w'))
print('cycle (years after 205 BC): A = lunar glyph months with a lunar eclipse of any kind (with a partial or total one) | partial or total lunar eclipses, of which U in months without a lunar glyph | S = solar glyph months with a solar eclipse | solar eclipses in the cycle')
for r in rows:
    if r['cycle'] <= 24 or r['cycle'] % 4 == 0 or r['cycle'] == 122:
        print(f"  {r['cycle']:3d} ({r['years']:6.0f}): A {r['A']:2d} of 38 ({r['Aum']:2d}) | {r['umbral']:2d}, U {r['U']:2d} {r['U_months'] if 0 < r['U'] <= 4 else ''} | S {r['S']:2d} of 28 | {r['solar_all']}")
first = lambda cond: next((r['cycle'] for r in rows if cond(r)), None)
print()
f1 = first(lambda r: r['A'] <= 19); f2 = first(lambda r: r['A'] == 0); stays = all(r['A'] == 0 for r in rows if f2 is not None and r['cycle'] >= f2)
f3 = first(lambda r: r['S'] <= 14); f4 = first(lambda r: r['U'] >= 3); f5 = first(lambda r: r['A'] < 30)
res = [('E1', 0.70, 30 <= f1 <= 36, f'first cycle with A <= 19: {f1} (sealed: 30 to 36)'),
       ('E2', 0.65, 63 <= f2 <= 69 and stays, f'first cycle with A = 0: {f2}; A stays 0 after: {stays} (sealed: 63 to 69, and stays)'),
       ('E3', 0.60, 32 <= f3 <= 39, f'first cycle with S <= 14: {f3} (sealed: 32 to 39)'),
       ('E4', 0.60, 8 <= f4 <= 13, f'first cycle with U >= 3: {f4} (sealed: 8 to 13)'),
       ('E5', 0.65, 13 <= f5 <= 18, f'first cycle with A < 30: {f5} (sealed: 13 to 18)')]
for name, p, ok, what in res: print(f'{name}  {int(p * 100)}%  {"held  " if ok else "FAILED"}  {what}')
print(f'{sum(ok for _, _, ok, _ in res)} of 5 held; Brier {sum((p - ok) ** 2 for _, p, ok, _ in res) / 5:.4f} (always saying 50%: 0.2500)')
print()
print('first cycle with S = 0:', first(lambda r: r['S'] == 0), '; later cycles with S > 0:', [r['cycle'] for r in rows if r['S'] > 0 and r['cycle'] > (first(lambda r: r['S'] == 0) or 999)])
print('first cycle with U >= 1, 3, 5, 10:', [first(lambda r, k=k: r['U'] >= k) for k in (1, 3, 5, 10)])
print('first cycle with no partial or total lunar eclipse in a glyph month:', first(lambda r: r['Aum'] == 0))
print('A is non-increasing:', all(a['A'] >= b['A'] for a, b in zip(rows, rows[1:])), '; S is non-increasing:', all(a['S'] >= b['S'] for a, b in zip(rows, rows[1:])))
print('cycles where A or S goes up:', [(b['cycle'], a['A'], b['A'], a['S'], b['S']) for a, b in zip(rows, rows[1:]) if b['A'] > a['A'] or b['S'] > a['S']])
