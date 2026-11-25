"""Second reader, step 2: the lists (mine against agent3's) and the catalogue count for every cycle by my own route.
Placement: by DATE. Each eclipse's JD (TD) -> Meeus mean lunation k -> dial month, with the dial's first full moon
taken from my own reading of the JPL tables (k0.json from run1.py).  The catalogue's luna number is NOT used here.
usage: run2.py IJPAPER DIALDIR CATDIR [CATDIR...]"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np
import cat2, lists2

PAPER, DIAL, CATS = sys.argv[1], sys.argv[2], sys.argv[3:]
K0 = json.load(open(os.path.join(HERE, 'k0.json')))['K0']          # floor of Meeus k of the first full moon (-27256)

# ---------- the lists
FL, FS, info, cons = lists2.freeth()
print(f'Freeth as I code it: {len(FL)} lunar, {len(FS)} solar, {len(set(FL) | set(FS))} cells; consecutive lunar pairs before the rule: {cons}')
FL1, FS1, _, _ = lists2.freeth(drop='first')
print(f'   dropping the first instead: {len(FL1)} lunar, cells {len(set(FL1) | set(FS1))}; months that differ: {sorted(set(FL) ^ set(FL1))}')
t5 = lists2.ij_table5(PAPER)
IL = [r[0] for r in t5 if r[1] == 'Y']; IS = [r[0] for r in t5 if r[3] == 'Y']
ILr = [r[0] for r in t5 if r[1] == 'Y' and not r[2]]; ISr = [r[0] for r in t5 if r[3] == 'Y' and not r[4]]
print(f'Table 5 parsed from the paper text: {len(t5)} cells, {len(IL)} lunar, {len(IS)} solar; unbracketed Yes: {len(ILr)} lunar, {len(ISr)} solar, in {len(set(ILr) | set(ISr))} cells; queried solar: {[r[0] for r in t5 if r[5]]}')
print(f'   unbracketed No: lunar {[r[0] for r in t5 if r[1] == "N" and not r[2]]}, solar {[r[0] for r in t5 if r[3] == "N" and not r[4]]}')
print(f'   cells with mixed brackets (one entry read, the other deduced): {[r[0] for r in t5 if r[2] != r[4]]}')
# against agent3's typed table (read as text, not imported)
src = open(os.path.join(DIAL, 'ij2019.py'), encoding='utf-8').read()
body = src.split('TABLE5 = """')[1].split('"""')[0].strip().split('\n')
typed = []
for l in body:
    c, a, b = l.split()
    typed.append((int(c), a.strip('[]')[0], a.startswith('['), b.strip('[]')[0], b.startswith('['), False))
same = [(x[:5] == y[:5]) for x, y in zip(t5, typed)]
print(f'   agent3\'s typed table: {len(typed)} rows; identical to the paper\'s rows (cell, lunar, bracket, solar, bracket): {all(same) and len(typed) == len(t5)}; differing rows: {[(x, y) for x, y in zip(t5, typed) if x[:5] != y[:5]]}')
print(f'   lunar in Freeth only {sorted(set(FL) - set(IL))}, in IJ only {sorted(set(IL) - set(FL))}; solar in Freeth only {sorted(set(FS) - set(IS))}, in IJ only {sorted(set(IS) - set(FS))}')
print(f'   read on the fragments but not in Freeth: lunar {sorted(set(ILr) - set(FL))} solar {sorted(set(ISr) - set(FS))}')
print(f'   Freeth glyphs where Table 5 has an unbracketed No: lunar {sorted(set(FL) & {r[0] for r in t5 if r[1] == "N" and not r[2]})}, solar {sorted(set(FS) & {r[0] for r in t5 if r[3] == "N" and not r[4]})}')
print(f'   Freeth cells not in Table 5: {sorted((set(FL) | set(FS)) - {r[0] for r in t5})}; Table 5 cells not in Freeth: {sorted({r[0] for r in t5} - (set(FL) | set(FS)))}')
for n in (2, 13, 125, 126, 38, 173, 196, 207, 213, 214):
    print(f'   month {n}: lunar {info.get(("L", n))} {"(glyph)" if n in FL else "(none)"}; solar {info.get(("S", n))} {"(glyph)" if n in FS else "(none)"}')
# what the model has at the new moons of 196 and 207 and full moons of 213 and 214, glyph or not
def dist(n, off):
    p = (38 * (n - 1) + off) % 446
    dD = ((p - 66 + 223) % 446) - 223; dA = ((p - 289 + 223) % 446) - 223
    return (dD, 'D') if abs(dD) <= abs(dA) else (dA, 'A')
print('   model distance from node point: FM 213', dist(213, 17), 'FM 214', dist(214, 17), 'NM 196', dist(196, 36), 'NM 207', dist(207, 36), 'NM 2', dist(2, 36))

# ---------- the catalogue, by date
LE, _, _ = cat2.load('LE', CATS, verbose=False); SE, _, _ = cat2.load('SE', CATS, verbose=False)
LM, SM = {}, {}
for r in LE:
    k = cat2.k_of(r['jd'])                         # near x.5
    n = int(round(k - 0.5)) - K0 + 1
    assert n not in LM; LM[n] = r
    assert n == r['luna'] + 27257                  # the shortcut, row by row, against my date route
for r in SE:
    k = cat2.k_of(r['jd'])
    n = int(round(k)) - K0
    assert n not in SM; SM[n] = r
    assert n == r['luna'] + 27256
print(f'\nby date and mean lunation every one of the {len(LE)} lunar and {len(SE)} solar rows lands in the month the shortcut gives')

def count(L, S, j):
    b = 223 * j
    le = {n: LM[b + n] for n in range(1, 224) if b + n in LM}; se = {n: SM[b + n] for n in range(1, 224) if b + n in SM}
    um = [n for n in le if le[n]['umag'] > 0]      # partial or total by MAGNITUDE, not by the type letter
    return dict(cycle=j, A=sum(n in le for n in L), Aum=sum(n in um for n in L), umbral=len(um), U=sum(n not in L for n in um),
                U_months=sorted(n for n in um if n not in L), S=sum(n in se for n in S), lunar_all=len(le), solar_all=len(se),
                A_none=sorted(n for n in L if n not in le), S_none=sorted(n for n in S if n not in se),
                N=sum(1 for n in se if se[n]['gamma'] > 0 and n not in S))

res = {}
for name, L, S in (('F', FL, FS), ('IJ', IL, IS), ('read', ILr, ISr)):
    res[name] = [count(L, S, j) for j in range(123)]
print('\nFreeth list, my count: cycle: A (Aum) | umbral in cycle, U [months] | S | N(north solar unmarked)')
for j in (0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 15, 16, 20, 25, 30, 31, 34, 35, 40, 50, 54, 55, 60, 63, 64, 69, 70, 122):
    r = res['F'][j]; i = res['IJ'][j]
    print(f"  {j:3d}: F {r['A']:2d} ({r['Aum']:2d}) | {r['umbral']:2d}, U {r['U']:2d} {r['U_months'] if r['U'] <= 4 else ''} | S {r['S']:2d} | N {r['N']}    IJ {i['A']:2d} ({i['Aum']:2d}) U {i['U']:2d} S {i['S']:2d}")
first = lambda rows, cond: next((r['cycle'] for r in rows if cond(r)), None)
for name in ('F', 'IJ', 'read'):
    R = res[name]; nl = len({'F': FL, 'IJ': IL, 'read': ILr}[name]); ns = len({'F': FS, 'IJ': IS, 'read': ISr}[name])
    print(f"{name}: first A<37: {first(R, lambda r: r['A'] < 37)}; A<30: {first(R, lambda r: r['A'] < 30)}; A<=half: {first(R, lambda r: r['A'] <= nl // 2)}; A=0: {first(R, lambda r: r['A'] == 0)} "
          f"(stays 0: {all(r['A'] == 0 for r in R[first(R, lambda r: r['A'] == 0):])}); S<{ns}: {first(R, lambda r: r['S'] < ns)}; S<=half: {first(R, lambda r: r['S'] <= ns // 2)}; S=0: {first(R, lambda r: r['S'] == 0)} "
          f"(stays 0: {all(r['S'] == 0 for r in R[first(R, lambda r: r['S'] == 0):])}); U>=1,3,5,10: {[first(R, lambda r, k=k: r['U'] >= k) for k in (1, 3, 5, 10)]}; Aum=0: {first(R, lambda r: r['Aum'] == 0)} "
          f"(stays: {all(r['Aum'] == 0 for r in R[first(R, lambda r: r['Aum'] == 0):])}); rises in A or S: {[(b['cycle'], k, a[k], b[k]) for a, b in zip(R, R[1:]) for k in ('A', 'S') if b[k] > a[k]]}")
    print(f"   how many cycles hold A=37: {[r['A'] for r in R[:8]]}; S: {[r['S'] for r in R[:8]]}")

# ---------- against agent3's json, every cycle
ca = json.load(open(os.path.join(DIAL, 'catalogue_all.json')))
diff = [(a['cycle'], k, a[k], b[k]) for a, b in zip(ca, res['F']) for k in ('A', 'Aum', 'umbral', 'U', 'S', 'lunar_all', 'solar_all', 'A_none', 'S_none', 'U_months') if a[k] != b[k]]
print(f'\ncatalogue_all.json against my count (Freeth list, 123 cycles, 10 fields each): {len(diff)} differences', diff[:10])
tl = json.load(open(os.path.join(DIAL, 'two_lists.json')))
for name in ('F', 'IJ', 'read'):
    diff = [(a['cycle'], k, a[k], b[k]) for a, b in zip(tl[name], res[name]) for k in ('A', 'Aum', 'umbral', 'U', 'S', 'solar_all', 'A_none', 'S_none') if a[k] != b[k]]
    print(f'two_lists.json [{name}] against my count: {len(diff)} differences', diff[:10])

# ---------- cycle 0 detail
r0 = res['F'][0]
le0 = {n: LM[n] for n in range(1, 224) if n in LM}; se0 = {n: SM[n] for n in range(1, 224) if n in SM}
print(f"\ncycle 0: {len(le0)} lunar eclipses: {sum(e['typ'][0] in 'PT' for e in le0.values())} partial or total ({sum(e['typ'][0] == 'P' for e in le0.values())} P, {sum(e['typ'][0] == 'T' for e in le0.values())} T), {sum(e['typ'][0] == 'N' for e in le0.values())} penumbral; first {min(le0.values(), key=lambda e: e['jd'])['date']}, last {max(le0.values(), key=lambda e: e['jd'])['date']}")
print(f"   lunar glyph months: none {r0['A_none']}; penumbral only {[n for n in FL if n in le0 and le0[n]['typ'][0] == 'N']}; penumbral eclipses on a glyph {sum(1 for n in le0 if le0[n]['typ'][0] == 'N' and n in FL)} of {sum(e['typ'][0] == 'N' for e in le0.values())}")
print(f"   partial or total in unmarked months: {[n for n in le0 if le0[n]['typ'][0] in 'PT' and n not in FL]}")
types = {}
for e in se0.values(): types[e['typ']] = types.get(e['typ'], 0) + 1
print(f"   {len(se0)} solar eclipses, types {dict(sorted(types.items()))}; A/T/H: {sum(e['typ'][0] in 'ATH' for e in se0.values())}; of them truly central (no + or - code): {sum(e['typ'][0] in 'ATH' and e['typ'][-1] not in '+-' for e in se0.values())}")
print(f"   solar eclipses on a solar glyph: {sum(n in FS for n in se0)}; A/T/H on a glyph: {sum(1 for n in se0 if n in FS and se0[n]['typ'][0] in 'ATH')}")
out = sorted((n, se0[n]['typ'], se0[n]['gamma'], se0[n]['date']) for n in se0 if n not in FS)
print(f"   the {len(out)} in months without a solar glyph (month, type, gamma, date): {out}")
print(f"   gamma of those: {min(x[2] for x in out):+.4f} to {max(x[2] for x in out):+.4f}; positive: {sum(x[2] > 0 for x in out)}")
gin = [se0[n]['gamma'] for n in se0 if n in FS]
print(f"   gamma of the {len(gin)} on a glyph: {min(gin):+.4f} to {max(gin):+.4f}")
# model north/south against gamma sign for the solar glyph months
ok = sum((info[('S', n)][2] == 'N') == (se0[n]['gamma'] > 0) for n in FS if n in se0)
print(f"   model says north/south for each solar glyph month; gamma's sign agrees in {ok} of {sum(n in se0 for n in FS)}; disagreements: {[(n, info[('S', n)], se0[n]['gamma']) for n in FS if n in se0 and (info[('S', n)][2] == 'N') != (se0[n]['gamma'] > 0)]}")
out_ij = sorted((n, se0[n]['typ'], se0[n]['gamma']) for n in se0 if n not in IS)
print(f"   IJ list: {len(out_ij)} unmarked, gamma {min(x[2] for x in out_ij):+.2f} to {max(x[2] for x in out_ij):+.2f}")
# month 126 and the dropped months, cycles 0..8
for n in (126, 38, 173, 125, 213, 214):
    print(f'   month {n} lunar, cycles 0-7:', ' | '.join((f"{LM[223 * j + n]['date']} {LM[223 * j + n]['typ']} um {LM[223 * j + n]['umag']:+.4f} pen {LM[223 * j + n]['pmag']:.4f} g {LM[223 * j + n]['gamma']:+.4f}") if 223 * j + n in LM else '-' for j in range(8)))
for n in (196, 207, 13, 2):
    print(f'   month {n} solar, cycles 0-7:', ' | '.join((f"{SM[223 * j + n]['date']} {SM[223 * j + n]['typ']} mag {SM[223 * j + n]['mag']:.4f} g {SM[223 * j + n]['gamma']:+.4f}") if 223 * j + n in SM else '-' for j in range(8)))
# read glyphs
R = res['read']
print('\nread on the fragments: A by cycle 0-16', [r['A'] for r in R[:17]], 'Aum', [r['Aum'] for r in R[:17]], 'S', [r['S'] for r in R[:17]])
print('   lunar read months without an eclipse, cycles 0-8:', [r['A_none'] for r in R[:9]], '; solar:', [r['S_none'] for r in R[:9]])
# dates
for j in (6, 10, 31, 34, 55, 64, 70, 122, 123):
    b = 223 * j
    fl_ = [LM[n] for n in range(b + 1, b + 224) if n in LM]; fs_ = [SM[n] for n in range(b + 1, b + 224) if n in SM]
    jd1 = cat2.mean_phase_jde(K0 + 0.5 + b)
    print(f'cycle {j}: mean first full moon JD {jd1:.1f} = {(jd1 - cat2.mean_phase_jde(K0 + 0.5)) / 365.25:.1f} Julian years after month 1; first lunar eclipse {fl_[0]["date"] if fl_ else None}, last {fl_[-1]["date"] if fl_ else None}; first solar {fs_[0]["date"] if fs_ else None}, last {fs_[-1]["date"] if fs_ else None}')
# modern cells
print('\nmodern eclipses, cell = ((n-1) mod 223)+1:')
for rows, M in (('LE', LM), ('SE', SM)):
    for n in sorted(M):
        e = M[n]
        if 2024 <= e['y'] <= 2026:
            cell = (n - 1) % 223 + 1
            L = FL if rows == 'LE' else FS
            near = min(L, key=lambda c: min(abs(c - cell), 223 - abs(c - cell)))
            print(f"   {rows} {e['date']} {e['typ']}: month {n}, cell {cell}; nearest {'lunar' if rows == 'LE' else 'solar'} glyph cell {near}; nearest marked cell of either kind {min(set(FL) | set(FS), key=lambda c: abs(c - cell))}")
json.dump(res, open(os.path.join(HERE, 'mycount.json'), 'w'))
