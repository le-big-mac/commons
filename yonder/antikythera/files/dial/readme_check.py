"""My own check of the mended README's numbers against the json and catalogue (after the fact).
usage: readme_check.py CATDIR [CATDIR ...]   (under -I through runpy)"""
import sys, os, re, json, glob, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
import dial, ij2019
T = json.load(open(os.path.join(HERE, 'two_lists.json')))
print('table rows (cycle: lunar F, IJ | partial or total F, IJ | missed F, IJ | solar F, IJ):')
for j in (0, 1, 2, 3, 5, 6, 8, 10, 12, 15, 20, 25, 30, 35, 40, 50, 60, 70, 122):
    f, i = T['F'][j], T['IJ'][j]
    print(f"| {j} ({round(j * 18.03):,}) | {f['A']}, {i['A']} | {f['Aum']}, {i['Aum']} | {f['U']}, {i['U']} | {f['S']}, {i['S']} |")
for name in ('F', 'IJ', 'read'):
    r = T[name]
    up = [(b['cycle'], k, a[k], b[k]) for a, b in zip(r, r[1:]) for k in ('A', 'S') if b[k] > a[k]]
    print(name, 'rises:', up)
    print(name, 'Aum after it first reaches 0 stays 0:', all(x['Aum'] == 0 for x in r[next(x['cycle'] for x in r if x['Aum'] == 0):]),
          '; U equals all partial or total from cycle 55 on:', all(x['U'] == x['umbral'] for x in r[55:]) if name != 'read' else '')
r = T['read']
print('read: A by cycle 0..16:', [x['A'] for x in r[:17]], '; S:', [x['S'] for x in r[:17]])
print('F: A by cycle 0..12:', [x['A'] for x in T['F'][:13]], 'S:', [x['S'] for x in T['F'][:13]], 'U:', [x['U'] for x in T['F'][:13]])
print('F cycles 28..36 A:', [(x['cycle'], x['A']) for x in T['F'][28:37]], 'S:', [(x['cycle'], x['S']) for x in T['F'][30:38]])

# the starts, with N allowed to be 0, 1, 2
pat = re.compile(r'^\s*(\d{5})\s+(-?\d{4})\s+([A-Z][a-z]{2})\s+(\d{2})\s+(\d{2}):(\d{2}):(\d{2})\s+(-?\d+)\s+(-?\d+)\s+(\d+)\s+(\S+)\s+\S+\s+(-?\d+\.\d+)')
def read_cat(prefix, add):
    rows = {}
    for f in sorted(f for d in sys.argv[1:] for f in glob.glob(os.path.join(d, prefix + '*.html'))):
        for line in open(f, encoding='utf-8', errors='replace'):
            m = pat.match(re.sub(r'<[^>]*>', '', line))
            if m: rows[int(m.group(9)) + add] = (m.group(11)[0], float(m.group(12)), f'{int(m.group(2))} {m.group(3)} {m.group(4)}')
    return rows
def year_of(k):
    jd = 1646679.21 + 29.530589 * k
    return 1 - math.floor(-4712 + (jd + 0.5) / 365.25)
LE, SE = read_cat('LE', 27257), read_cat('SE', 27256)
fl, fs = dial.glyph_months()
K = [k for k in range(-1250, 2700) if 1 <= year_of(k) <= 300]
for name, L, S in (('F', sorted(fl), sorted(fs)), ('IJ', ij2019.LUNAR, ij2019.SOLAR)):
    sc = {}
    for k in K:
        sc[k] = (sum(k + n in LE for n in L), sum(k + n in SE for n in S), sum(1 for n in range(1, 224) if k + n in LE and LE[k + n][0] in 'PT' and n not in L),
                 sum(1 for n in range(1, 224) if k + n in SE and SE[k + n][1] > 0 and n not in S))
    a0, s0, u0, n0 = sc[0]
    g3 = [k for k in K if sc[k][0] >= a0 and sc[k][1] >= s0 and sc[k][2] <= u0]
    print(name, 'good on A, S, U:', len(g3), '; their N values:', sorted(sc[k][3] for k in g3))
    for lim in (0, 1, 2):
        g = [k for k in g3 if sc[k][3] <= lim]
        print(f'   N <= {lim}: {len(g)}:', [(k, year_of(k), sc[k]) for k in g])
    print('   perfect (all lunar and all solar):', sum(sc[k][0] == len(L) and sc[k][1] == len(S) for k in K), '; of the good ones:', sum(sc[k][0] == len(L) and sc[k][1] == len(S) for k in g3))
# dates of the first eclipses of cycles 64 and 70, for the AD years
for j in (31, 34, 55, 64, 70):
    b = 223 * j
    print('cycle', j, 'first lunar eclipse:', next(LE[n][2] for n in range(b + 1, b + 224) if n in LE), '; first solar:', next(SE[n][2] for n in range(b + 1, b + 224) if n in SE))
