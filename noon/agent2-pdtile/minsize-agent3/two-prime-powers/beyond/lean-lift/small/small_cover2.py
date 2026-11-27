"""Sharper reduction (generalised contraction): a level of the p-tree at which every group that holds elements has an empty
subclass can be deleted, and a good signing of the contracted multiset is a good signing of the original.  After all such
contractions every remaining level of the p-tree has a group all of whose p subclasses hold elements; each such level adds at
least p - 1 to the number of classes that hold elements, so the p-tree has depth at most floor((m-1)/(p-1)).  Hence a
multiset of m elements lives, after reduction, on Z_n with n dividing
        n'_m = product over odd primes p <= m of p^floor((m-1)/(p-1)).
If n'_m is covered by the theorems already proved, the statement on signs holds for every multiset of at most m elements on
every Z_n with n odd.     usage: small_cover2.py MAXM"""
import sys
sys.setrecursionlimit(100000)
sys.path.insert(0, '/home/agent3/lean/lift-check/general2')
from coverage2 import covered_f
from sympy import primerange
M = int(sys.argv[1]); first_uncovered = None
for m in range(1, M + 1):
    f = {p: (m - 1) // (p - 1) for p in primerange(3, m + 1)}
    f = {p: a for p, a in f.items() if a > 0}
    n = 1
    for p, a in f.items(): n *= p ** a
    if not f:
        print(f'm={m}: n\'_m = 1'); continue
    old, new = covered_f(f)
    shape = ' * '.join(f'{p}^{a}' if a > 1 else f'{p}' for p, a in sorted(f.items()))
    ok = bool(old or new)
    if not ok and first_uncovered is None: first_uncovered = m
    print(f'm={m}: n\'_m = {shape} (about {float(n):.3g}): ' + ('covered by ' + '; '.join((old + new)[:2])[:150] if ok else 'NOT covered by the theorems proved so far'), flush=True)
print('first m whose shape is not covered:', first_uncovered)
