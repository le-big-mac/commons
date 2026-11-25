"""Second reader, step 7: how the number of 'as good' starts depends on the definition. usage: run7.py IJPAPER CATDIR [CATDIR...]"""
import sys, os, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import cat2, lists2
PAPER, CATS = sys.argv[1], sys.argv[2:]
K0 = json.load(open(os.path.join(HERE, 'k0.json')))['K0']
FL, FS, info, _ = lists2.freeth()
t5 = lists2.ij_table5(PAPER); IL = [r[0] for r in t5 if r[1] == 'Y']; IS = [r[0] for r in t5 if r[3] == 'Y']
LE, _, _ = cat2.load('LE', CATS, verbose=False); SE, _, _ = cat2.load('SE', CATS, verbose=False)
LM = {int(round(cat2.k_of(r['jd']) - 0.5)) - K0 + 1: r for r in LE}
SM = {int(round(cat2.k_of(r['jd']))) - K0: r for r in SE}
def year(k):
    jd = cat2.mean_phase_jde(K0 + 0.5 + k); y = int(np.floor((jd - 1721057.5) / 365.25))
    while cat2.jd_from_date(y + 1, 1, 1, False) <= jd: y += 1
    while cat2.jd_from_date(y, 1, 1, False) > jd: y -= 1
    return y
Ks = [k for k in range(-1300, 2800) if -299 <= year(k) <= 0]
for name, L, S in (('Freeth', FL, FS), ('IJ', IL, IS)):
    sc = {}
    for k in Ks:
        A = sum(k + n in LM for n in L); Sn = sum(k + n in SM for n in S)
        U = sum(1 for n in range(1, 224) if k + n in LM and LM[k + n]['umag'] > 0 and n not in L)
        N = sum(1 for n in range(1, 224) if k + n in SM and SM[k + n]['gamma'] > 0 and n not in S)
        Sth = sum(1 for n in range(1, 224) if k + n in SM and SM[k + n]['gamma'] < 0 and n not in S)
        sc[k] = (A, Sn, U, N, Sth)
    a0, s0, u0, n0, _ = sc[0]
    right = lambda k: sc[k][3] < sc[k][4]            # more southern than northern eclipses left unmarked
    print(f'{name}: 205 BC = {sc[0]}')
    for lab, cond in (('A >= a0, S >= s0, U <= u0 (the README)', lambda k: sc[k][0] >= a0 and sc[k][1] >= s0 and sc[k][2] <= u0),
                      ('A + S >= a0 + s0, U <= u0', lambda k: sc[k][0] + sc[k][1] >= a0 + s0 and sc[k][2] <= u0),
                      ('A + S >= a0 + s0 (U not asked)', lambda k: sc[k][0] + sc[k][1] >= a0 + s0),
                      ('A + S >= a0 + s0 - 1, U <= u0', lambda k: sc[k][0] + sc[k][1] >= a0 + s0 - 1 and sc[k][2] <= u0),
                      ('A + S >= a0 + s0 - 2, U <= 1', lambda k: sc[k][0] + sc[k][1] >= a0 + s0 - 2 and sc[k][2] <= 1)):
        g = [k for k in Ks if cond(k)]; r = [k for k in g if right(k)]
        print(f'   {lab}: {len(g)} starts, {len(r)} the right way round; years BC of the right-way ones: {[1 - year(k) for k in r]}')
        if lab.startswith('A + S >= a0 + s0, U'):
            print('      detail:', [(1 - year(k), k % 223, sc[k][:4]) for k in r])
