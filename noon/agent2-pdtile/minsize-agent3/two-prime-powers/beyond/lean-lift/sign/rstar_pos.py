"""(R**) exploration: for every family F of nonempty subsets of [r], over all signings, the best achievable value of
   min over grid points of f(z^D)   (f = 1 + sum eta_B z^B),  and of  min_D f(z^D) / prod_{i in D}(1 - 1/q_i).
Is positivity on the whole grid always achievable?  What margin?    usage: rstar_pos.py q1 .. qr"""
import sys, itertools
from fractions import Fraction as Fr
q = [int(t) for t in sys.argv[1:]]; r = len(q)
subsets = list(range(1, 1 << r))
def val(B, D):
    v = Fr(1)
    for i in range(r):
        if (B >> i & 1) and (D >> i & 1): v *= Fr(-1, q[i])
    return v
C = {B: [val(B, D) for D in range(1 << r)] for B in subsets}
ref = []
for D in range(1 << r):
    v = Fr(1)
    for i in range(r):
        if D >> i & 1: v *= (1 - Fr(1, q[i]))
    ref.append(v)
worst_abs = None; worst_rel = None; nopos = 0; nfam = 0
for F in range(1 << len(subsets)):
    fam = [subsets[b] for b in range(len(subsets)) if F >> b & 1]; nfam += 1
    best_abs = None; best_rel = None
    for signs in itertools.product((1, -1), repeat=len(fam)):
        vals = [1 + sum(s * C[B][D] for s, B in zip(signs, fam)) for D in range(1 << r)]
        ma = min(vals); mr = min(v / rf for v, rf in zip(vals, ref))
        if best_abs is None or ma > best_abs: best_abs = ma
        if best_rel is None or mr > best_rel: best_rel = mr
    if best_abs <= 0: nopos += 1
    if worst_abs is None or best_abs < worst_abs[0]: worst_abs = (best_abs, fam)
    if worst_rel is None or best_rel < worst_rel[0]: worst_rel = (best_rel, fam)
print(f'q = {q}: families {nfam}; families where NO signing is positive on the whole grid: {nopos}; '
      f'least best min f: {worst_abs}; least best min f/prod(1-1/q_i): {worst_rel}')
