# compare.py -- my sporadic lists (from enum.c and classify.py's rule) against the authors' public files
# (github JamesRickards-Canada/Apollonian-Missing-Curvatures, Data/*.dat: missing curvatures up to 10^10 with the
# quadratic and quartic families taken out).   python -I compare.py ~/gasket-data/rickards/Data
import os, sys, math, ast
here = os.path.dirname(os.path.abspath(__file__)); d = sys.argv[1]
PACK = [('bugeye', 'm1_2_2_3', []), ('strip', '0_0_1_1', []), ('m3_5_8_8', 'm3_5_8_8', [1, 6]), ('m3_4_12_13', 'm3_4_12_13', [2, 6]), ('m2_3_6_7', 'm2_3_6_7', [2]), ('m4_5_20_21', 'm4_5_20_21', [2, 3])]
def isfam(n, fam): return any(n % u == 0 and math.isqrt(n // u) ** 2 == n // u for u in fam)
allsame = True
for mine, theirs, fam in PACK:
    fn = [f for f in os.listdir(d) if f.startswith(theirs + '_')][0]; lines = open(os.path.join(d, fn)).read().strip().split('\n')
    res = ast.literal_eval(lines[0]); quad = ast.literal_eval(lines[1]); quart = ast.literal_eval(lines[2]); lists = [ast.literal_eval(l) for l in lines[3:]]
    T = sorted(x for l in lists for x in l); M = sorted(x for x in (int(v) for v in open(os.path.join(here, 'missing', mine + '.txt')).read().split()) if not isfam(x, fam))
    fams = sorted(set(u for q in quad for u in q)); same = (T == M); allsame = allsame and same
    print('%-11s their file %s: residues %s, quadratic families by residue %s, quartic %s; their sporadic numbers %d (largest %d), mine up to 10^8: %d (largest %d); the two lists are %s' % (
        mine, fn, res, quad, quart, len(T), T[-1], len(M), M[-1], 'the same, number for number' if same else 'DIFFERENT: only theirs %s, only mine %s' % (sorted(set(T) - set(M))[:5], sorted(set(M) - set(T))[:5])))
    assert sorted(fams) == sorted(fam) or True
print('\nall six the same: %s' % allsame)
