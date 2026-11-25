"""Second reader, step 10: 'from one edge' -- the cycle in which each glyph month first has no eclipse, against its model distance.
usage: run10.py CATDIR [CATDIR...]"""
import sys, os, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import cat2, lists2
CATS = sys.argv[1:]
K0 = json.load(open(os.path.join(HERE, 'k0.json')))['K0']
FL, FS, info, _ = lists2.freeth()
LE, _, _ = cat2.load('LE', CATS, verbose=False); SE, _, _ = cat2.load('SE', CATS, verbose=False)
LM = {int(round(cat2.k_of(r['jd']) - 0.5)) - K0 + 1: r for r in LE}
SM = {int(round(cat2.k_of(r['jd']))) - K0: r for r in SE}
def first_gone(n, M):
    return next(j for j in range(0, 123) if 223 * j + n not in M)
def comes_back(n, M):
    j0 = first_gone(n, M); return any(223 * j + n in M for j in range(j0, 123))
rowsL = sorted((info[('L', n)][0], n, first_gone(n, LM)) for n in FL)
print('lunar glyph months: (model distance in units, month, first cycle without a lunar eclipse):', rowsL)
d = np.array([r[0] for r in rowsL]); c = np.array([r[2] for r in rowsL])
print('   straight line: first cycle without an eclipse = %.2f + %.3f * distance; correlation %.4f; any month regains an eclipse later: %s' % (np.polyfit(d, c, 1)[1], np.polyfit(d, c, 1)[0], np.corrcoef(d, c)[0, 1], any(comes_back(n, LM) for n in FL)))
rowsS = sorted((info[('S', n)][0], info[('S', n)][1], n, first_gone(n, SM)) for n in FS)
print('solar glyph months: (distance, node, month, first cycle without a solar eclipse):', rowsS)
for node in 'DA':
    d = np.array([r[0] for r in rowsS if r[1] == node]); c = np.array([r[3] for r in rowsS if r[1] == node])
    print(f'   node {node}: correlation {np.corrcoef(d, c)[0, 1]:.4f}; slope {np.polyfit(d, c, 1)[0]:.3f} cycles a unit')
print('   any solar month regains an eclipse later:', any(comes_back(n, SM) for n in FS))
# the misses: months in which the dial comes to miss a partial/total lunar eclipse, in order
firstU = {}
for j in range(123):
    for n in range(1, 224):
        if n not in FL and 223 * j + n in LM and LM[223 * j + n]['umag'] > 0 and n not in firstU: firstU[n] = j
def dist(n):
    p = (38 * (n - 1) + 17) % 446
    dD = ((p - 66 + 223) % 446) - 223; dA = ((p - 289 + 223) % 446) - 223
    return dD if abs(dD) <= abs(dA) else dA
print('unmarked months by the first cycle in which they hold a partial or total lunar eclipse (cycle, month, model distance), first 12:', sorted((j, n, dist(n)) for n, j in firstU.items())[:12])
