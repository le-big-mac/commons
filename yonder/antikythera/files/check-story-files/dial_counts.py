"""Recount what the story says about the eclipse dial from the note's two_lists.json (read only)."""
import json
d = json.load(open('/srv/commons/antikythera-agent3/dial/two_lists.json'))
SAROS_Y = 6585.3211 / 365.25          # years in a cycle (Julian years)
START = -204 + (31 + 28 + 31 + 30 + 12) / 365.0   # 12 May 205 BC as an astronomical year number (205 BC = -204)
def ad(cycle):
    y = START + cycle * SAROS_Y        # astronomical year; for y >= 1 the same as AD
    return y
for name in ('F', 'IJ'):
    rows = d[name]
    print('==', name, 'cycles', len(rows))
    r0 = rows[0]
    print(' cycle 0: A', r0['A'], 'Aum', r0['Aum'], 'S', r0['S'], 'U', r0['U'], 'umbral', r0['umbral'], 'solar_all', r0['solar_all'])
    for c in (5, 6, 8, 31, 34, 55, 63, 64, 69, 70):
        r = rows[c]
        print(f"  cycle {c:3d} ({c*SAROS_Y:7.1f} y on, year {ad(c):8.2f}): A {r['A']:2d} Aum {r['Aum']:2d} S {r['S']:2d} U {r['U']:2d} umbral {r['umbral']}")
    fa = next(r['cycle'] for r in rows if r['A'] <= 19)
    fz = next(r['cycle'] for r in rows if r['A'] == 0)
    fs = next(r['cycle'] for r in rows if r['S'] <= 14)
    sz = next(r['cycle'] for r in rows if r['S'] == 0)
    um0 = next(r['cycle'] for r in rows if r['Aum'] == 0)
    u3 = next(r['cycle'] for r in rows if r['U'] >= 3)
    u1 = next(r['cycle'] for r in rows if r['U'] >= 1)
    uall = next(r['cycle'] for r in rows if r['U'] == r['umbral'])
    print(' first cycle A<=19:', fa, round(fa*SAROS_Y, 1), 'y, year', round(ad(fa), 1), ' A there', rows[fa]['A'])
    print(' first cycle A==0 :', fz, round(fz*SAROS_Y, 1), 'y, year', round(ad(fz), 1))
    print(' first cycle S<=14:', fs, round(fs*SAROS_Y, 1), 'y, year', round(ad(fs), 1), ' S there', rows[fs]['S'])
    print(' first cycle S==0 :', sz, round(sz*SAROS_Y, 1), 'y, year', round(ad(sz), 1))
    print(' first cycle Aum==0:', um0, round(um0*SAROS_Y, 1), 'y, year', round(ad(um0), 1))
    print(' first cycle U>=1:', u1, round(u1*SAROS_Y, 1), '; U>=3:', u3, round(u3*SAROS_Y, 1), '; U == all umbral:', uall, round(uall*SAROS_Y, 1), 'year', round(ad(uall), 1))
    print(' stays zero after: A', all(r['A'] == 0 for r in rows[fz:]), ' S', all(r['S'] == 0 for r in rows[sz:]), ' Aum', all(r['Aum'] == 0 for r in rows[um0:]))
    print(' A never rises:', all(rows[i+1]['A'] <= rows[i]['A'] for i in range(len(rows)-1)), ' S never rises:', all(rows[i+1]['S'] <= rows[i]['S'] for i in range(len(rows)-1)))
    # month by month: once a month is in the none-list, is it there in every later cycle?
    for key in ('A_none', 'S_none'):
        back = []
        for i in range(len(rows) - 1):
            lost = set(rows[i][key])
            for j in range(i + 1, len(rows)):
                ret = lost - set(rows[j][key])
                if ret: back.append((i, j, sorted(ret))); break
        print(' ', key, 'months that get an eclipse back after losing it:', back[:6] if back else 'none')
    # order in which lunar months are lost
    seen = []; 
    for r in rows:
        for m in r['A_none']:
            if m not in seen: seen.append(m)
    print(' lunar months in order of loss:', seen[:8])
    seen = []
    for r in rows:
        for m in r['S_none']:
            if m not in seen: seen.append(m)
    print(' solar months in order of loss:', seen[:6])
    # 100 years on
    for c in range(0, 8): print('   cycle', c, round(c*SAROS_Y), 'y: A', rows[c]['A'], 'S', rows[c]['S'], 'Aum', rows[c]['Aum'], 'U', rows[c]['U'])
