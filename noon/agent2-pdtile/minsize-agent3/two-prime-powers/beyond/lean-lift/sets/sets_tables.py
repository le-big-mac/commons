"""For the groups of the second note: Z_36 = Z_{12*3}, Z_100 = Z_{20*5}, Z_225 = Z_{45*5} = Z_{75*3}.  For each pattern of the
smaller group, a least multiset with multiplicities <= r (found by the solver with that cap, checked by exact division) is lifted
along r to a SET on the larger group by the recipe of the proposition; its pattern there is computed by exact division and
compared.  So for these patterns the least size of a set on the larger group is the least size of a multiset.
usage: sets_tables.py TLIMIT"""
import sys, json, importlib.util
from sympy import Poly, cyclotomic_poly, symbols, ZZ
sys.argv_saved = sys.argv; tl = float(sys.argv[1])
def load(name, path, argv):
    sys.argv = argv; spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec)
    return spec, m
import least_mult_lib as L, spread_lib as S
X = symbols('X')
O = '/srv/commons/agent2-pdtile/minsize-agent3/out/'
for (p, q, n, r) in [(2, 3, 2, 3), (2, 5, 2, 5), (3, 5, 2, 5), (5, 3, 2, 3)]:
    N = p ** n * q; done = sets = already = fail = und = 0
    for line in open(O + f'n{n}-p{p}-q{q}-multi-cpsat.jsonl'):
        if not line.startswith('{'): continue
        o = json.loads(line)
        if o.get('min') is None: continue
        E, F, s = o['E'], o['F'], o['min']
        ok, x = L.feasible(p, q, n, E, F, s, r, tl)
        if not ok: und += 1; continue
        assert L.exact(p, q, n, x) == (sorted(E), sorted(F)) and sum(x) == s
        mult = {i: w for i, w in enumerate(x) if w}
        if max(mult.values()) == 1: already += 1
        P = S.pattern(mult, N)
        lifted = S.step(mult, N, r, 1)
        good = (max(lifted.values()) == 1 and sum(lifted.values()) == s and S.pattern(lifted, N * r) == P)
        done += 1; sets += good; fail += (not good)
    print(f'Z_{N} -> Z_{N * r} along {r}: {done} patterns with a least multiset of multiplicities <= {r} ({already} of them sets already); lifted to a set of the same size with exactly the same pattern on Z_{N * r}: {sets}; failed: {fail}; not found by the solver in {tl:.0f} s: {und}', flush=True)
