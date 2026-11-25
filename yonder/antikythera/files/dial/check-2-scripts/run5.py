"""Second reader, step 5: starts near December 178 BC under the standard numbering; one-month offsets around 205 BC.
usage: run5.py IJPAPER CATDIR [CATDIR...]"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import cat2, lists2
PAPER, CATS = sys.argv[1], sys.argv[2:]
K0 = json.load(open(os.path.join(HERE, 'k0.json')))['K0']
FL, FS, info, _ = lists2.freeth()
t5 = lists2.ij_table5(PAPER); IL = [r[0] for r in t5 if r[1] == 'Y']; IS = [r[0] for r in t5 if r[3] == 'Y']
LE, _, _ = cat2.load('LE', CATS, verbose=False); SE, _, _ = cat2.load('SE', CATS, verbose=False)
LM = {int(round(cat2.k_of(r['jd']) - 0.5)) - K0 + 1: r for r in LE}
SM = {int(round(cat2.k_of(r['jd']))) - K0: r for r in SE}
def score(k, L, S):
    return (sum(k + n in LM for n in L), sum(k + n in SM for n in S), sum(1 for n in range(1, 224) if k + n in LM and LM[k + n]['umag'] > 0 and n not in L),
            sum(1 for n in range(1, 224) if k + n in SM and SM[k + n]['gamma'] > 0 and n not in S))
print('starts near December 178 BC (the solar eclipse of -177 Dec 22 is the new moon of month 342 in the 205 BC count):')
for k in range(338, 345):
    print(f'   k {k}: the eclipse of 22 Dec 178 BC is then the new moon of month {342 - k}; Freeth (A, S, U, N) {score(k, FL, FS)}; IJ {score(k, IL, IS)}')
print('offsets of a few months around 205 BC (Freeth):', {k: score(k, FL, FS) for k in range(-7, 8)})
print('offsets of a few months around 205 BC (IJ):', {k: score(k, IL, IS) for k in range(-7, 8)})
# lunar eclipses in months 213 and 214 over cycles -5..7, and solar in 196, 207
for n in (213, 214, 125):
    print(f'month {n} lunar, cycles -5..7:', [(j, LM[223*j+n]['typ'], LM[223*j+n]['pmag']) if 223*j+n in LM else (j, None) for j in range(-5, 8)])
for n in (196, 207, 149, 2):
    print(f'month {n} solar, cycles -5..7:', [(j, SM[223*j+n]['typ'], SM[223*j+n]['gamma']) if 223*j+n in SM else (j, None) for j in range(-5, 8)])
