"""After the two reductions (strip every prime greater than the number m of elements; contract every tree level at which the
multiset does not branch), a multiset of m elements lives on Z_n with n dividing  n_m = product of p^(m-1) over the odd
primes p <= m.  The statement on signs for n implies it for every divisor of n.  So if n_m is covered by the theorems
already proved (Theorems 2, 3, 6 and 7 of the three results, through coverage2.py's own test), the statement holds for
EVERY multiset of at most m elements on EVERY Z_n with n odd.
usage: small_cover.py MAXM"""
import sys
sys.path.insert(0, '/home/agent3/lean/lift-check/general2')
from coverage2 import covered_f
from sympy import primerange
M = int(sys.argv[1])
for m in range(1, M + 1):
    f = {p: m - 1 for p in primerange(3, m + 1)}
    f = {p: a for p, a in f.items() if a > 0}
    if not f:
        print(f'm={m}: n_m = 1: nothing to prove beyond a total that is not 0'); continue
    old, new = covered_f(f)
    shape = ' * '.join(f'{p}^{a}' for p, a in sorted(f.items()))
    print(f'm={m}: n_m = {shape}: ' + ('COVERED by ' + '; '.join((old + new)[:3]) if (old or new) else 'not covered by the theorems proved so far'), flush=True)
