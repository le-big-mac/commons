# coverage.py -- which odd n are covered by Theorem 2 (n = p^a q^b), Theorem 3 (n = p r q^b) and the new
# Theorem 6 / 6' (n = m q^b, with the bound c(m) > 0 computed by the recursion below).
# c(state): state = number of digits used of each prime of m; adding a digit of the prime p to a state `prev`:
#     c = min( c(prev)/2 , c(prev) - L * 2^(1-p) ),  L = number of levels of prev without a digit of p
#       = prod over primes r != p of (1 + digits of r in prev)            [levels: at most one digit per prime]
# and c(state) = the best over the prime added last.  c(empty) = 1.  Full-box version (Theorem P): L = 2^(#digits of prev).
import sys
from fractions import Fraction
from functools import lru_cache
from sympy import factorint
def cbound(fm, full=False):
    primes = sorted(fm)
    @lru_cache(None)
    def c(state):
        if sum(state) == 0: return Fraction(1)
        best = Fraction(-1)
        for i, p in enumerate(primes):
            if state[i] == 0: continue
            prev = tuple(a - (1 if j == i else 0) for j, a in enumerate(state))
            cp = c(prev)
            if cp <= 0: continue
            if full: L = 2 ** sum(prev)
            else:
                L = 1
                for j, a in enumerate(prev):
                    if j != i: L *= 1 + a
            best = max(best, min(cp / 2, cp - Fraction(L, 2 ** (p - 1))))
        return best
    return c(tuple(fm[p] for p in primes))
def covered(n):
    f = factorint(n)
    how = []
    if len(f) <= 2: how.append("Thm2")
    if len(f) == 3 and sorted(f.values())[:2] == [1, 1]: how.append("Thm3")
    for q in [None] + sorted(f):
        fm = {p: a for p, a in f.items() if p != q}
        if not fm: continue
        if cbound(fm, full=True) > 0: how.append("P(full box) q=%s" % q)
        elif cbound(fm) > 0: how.append("P'(tree levels) q=%s" % q)
    return how
if __name__ == "__main__":
    N = int(sys.argv[1])
    unc = []; newly = []
    for n in range(3, N, 2):
        h = covered(n)
        if not h: unc.append(n)
        elif not any(x.startswith("Thm") for x in h): newly.append(n)
    print("odd n < %d: not covered by Theorems 2, 3: %d of them are covered by the new theorem; first: %s" % (N, len(newly), newly[:12]))
    print("odd n < %d covered by nothing: %d; first: %s" % (N, len(unc), [(n, dict(factorint(n))) for n in unc[:8]]))
    for n in (1155, 1365, 1575, 3465, 5005, 11025, 7875, 15015, 3**3 * 5**3 * 7**3, 3*5*7*11*13*17*19*23*29):
        print(n, dict(factorint(n)), covered(n)[:3])
