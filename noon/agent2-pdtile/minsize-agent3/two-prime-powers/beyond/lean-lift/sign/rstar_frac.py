"""(R**): fraction of good signings per family; candidate universal rules.   usage: rstar_frac.py q1 .. qr"""
import sys, itertools
from fractions import Fraction as Fr
q = [int(t) for t in sys.argv[1:]]; r = len(q)
subsets = list(range(1, 1 << r))
def coef(B, D):
    v = 1
    for i in range(r):
        if D >> i & 1: v *= (-1 if B >> i & 1 else q[i])
    return v
C = {B: [coef(B, D) for D in range(1 << r)] for B in [0] + subsets}
pc = lambda v: bin(v).count('1')
minfrac = (2, None); rules = {'all +': 0, '(-1)^(|B|+1)': 0, '(-1)^|B|': 0, 'all -': 0}
nfam = 0; hist = {}
for F in range(1 << len(subsets)):
    fam = [subsets[b] for b in range(len(subsets)) if F >> b & 1]; nfam += 1; N = len(fam)
    good = 0
    for signs in itertools.product((1, -1), repeat=N):
        if all(C[0][D] + sum(s * C[B][D] for s, B in zip(signs, fam)) != 0 for D in range(1 << r)): good += 1
    fr = Fr(good, 2 ** N)
    if fr < minfrac[0]: minfrac = (fr, fam)
    for name, rule in (('all +', lambda B: 1), ('(-1)^(|B|+1)', lambda B: -(-1) ** pc(B)), ('(-1)^|B|', lambda B: (-1) ** pc(B)), ('all -', lambda B: -1)):
        if all(C[0][D] + sum(rule(B) * C[B][D] for B in fam) != 0 for D in range(1 << r)): rules[name] += 1
print(f'q = {q}: families {nfam}; least fraction of good signings {minfrac}; families where a fixed rule works: {rules}')
