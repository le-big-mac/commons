"""Second reader, step 6: cycle-0 solar eclipses sorted by gamma with the two lists' marks; last eclipse of month 213.
usage: run6.py IJPAPER CATDIR [CATDIR...]"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import cat2, lists2
PAPER, CATS = sys.argv[1], sys.argv[2:]
K0 = json.load(open(os.path.join(HERE, 'k0.json')))['K0']
FL, FS, info, _ = lists2.freeth()
t5 = lists2.ij_table5(PAPER); IL = [r[0] for r in t5 if r[1] == 'Y']; IS = [r[0] for r in t5 if r[3] == 'Y']
RS = [r[0] for r in t5 if r[3] == 'Y' and not r[4]]; RSno = [r[0] for r in t5 if r[3] == 'N' and not r[4]]
LE, _, _ = cat2.load('LE', CATS, verbose=False); SE, _, _ = cat2.load('SE', CATS, verbose=False)
LM = {int(round(cat2.k_of(r['jd']) - 0.5)) - K0 + 1: r for r in LE}
SM = {int(round(cat2.k_of(r['jd']))) - K0: r for r in SE}
print('cycle 0 solar eclipses by gamma (month, gamma, type, magnitude | Freeth glyph | IJ glyph | read on fragments: Y yes, N read as none, . lost):')
for n in sorted((n for n in range(1, 224) if n in SM), key=lambda n: -SM[n]['gamma']):
    e = SM[n]
    print(f"   {n:4d} {e['gamma']:+.4f} {e['typ']:3s} {e['mag']:.3f} | {'F' if n in FS else '-'} | {'IJ' if n in IS else '--'} | {'Y' if n in RS else ('N' if n in RSno else '.')}")
for j in range(-5, 0):
    n = 223 * j + 213
    if n in LM: print(f"month 213, cycle {j}: {LM[n]['date']} {LM[n]['typ']} pen {LM[n]['pmag']} gamma {LM[n]['gamma']}")
n = -223 + 125; print('month 125, cycle -1:', LM[n]['date'], LM[n]['typ'], LM[n]['pmag'])
# lunar glyph months of cycle 0: gamma of penumbral ones, and the unmarked penumbral eclipses
print('cycle 0 penumbral eclipses in unmarked months:', [(n, LM[n]['date'], LM[n]['pmag'], LM[n]['gamma']) for n in range(1, 224) if n in LM and LM[n]['umag'] < 0 and n not in FL])
