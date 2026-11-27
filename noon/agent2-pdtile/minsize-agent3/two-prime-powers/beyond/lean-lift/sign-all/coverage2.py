# coverage2.py -- which odd n are covered once Theorem 7 (tree boxes) is added to the earlier theorems.
# Earlier: Theorem 2 (n = p^a q^b), Theorem 3 (n = p r q^b), Theorem 6 (n = m q^b or n = m with c(m) > 0; the digit
# recursion of sign-general-result.md section 4, re-implemented here from its text).
# New: n = m q^b or n = m with Gamma(m) > 0, where for the tree box of m (one coordinate Z_{p^a} per prime power of m)
#   lam(p, a)  = w + w^2 + .. + w^a,  w = 2^(1-p)                                   (Lemma T)
#   single(p,a)= 1/2 if a = 1 or p >= 5;  5/8 - lam(3, a) if p = 3, a >= 2          (Lemma S)
#   Gamma(one tree) = single;  Gamma(S) = max over the tree T = (p, a) of S taken last, with G' = Gamma(S - T) > 0 and
#   L' = number of levels of S - T = prod (a_l + 1):
#        min( single(p, a) * G' , 3/4 * G' - L' * lam(p, a) )                       (Lemma 3T)
#        and, if a = 1, also  min( G'/2 , G' - L' * 2^(1-p) )                       (Lemma 3 of the earlier result)
# usage: python coverage2.py N          -- all odd n < N
#        python coverage2.py first      -- the least odd n covered by nothing, by a search over exponent vectors
import sys
from fractions import Fraction
from functools import lru_cache
from itertools import product
from sympy import factorint, primerange

def lam(p, a):
    w = Fraction(1, 2 ** (p - 1))
    return sum(w ** l for l in range(1, a + 1))

def single(p, a):
    if a == 1 or p >= 5: return Fraction(1, 2)
    return Fraction(5, 8) - lam(3, a)

@lru_cache(None)
def Gamma(trees):
    """trees: sorted tuple of (p, a)."""
    if len(trees) == 0: return Fraction(1)
    if len(trees) == 1: return single(*trees[0])
    best = Fraction(-1)
    for idx, (p, a) in enumerate(trees):
        rest = trees[:idx] + trees[idx + 1:]
        G = Gamma(rest)
        if G <= 0: continue
        L = 1
        for (_, b) in rest: L *= b + 1
        cand = min(single(p, a) * G, Fraction(3, 4) * G - L * lam(p, a))
        if a == 1:
            cand = max(cand, min(G / 2, G - Fraction(L, 2 ** (p - 1))))
        best = max(best, cand)
    return best

@lru_cache(None)
def cdigit(state_primes, state):
    """the digit recursion c(m) of the earlier result, tree levels."""
    if sum(state) == 0: return Fraction(1)
    best = Fraction(-1)
    for i, p in enumerate(state_primes):
        if state[i] == 0: continue
        prev = tuple(a - (1 if j == i else 0) for j, a in enumerate(state))
        cp = cdigit(state_primes, prev)
        if cp <= 0: continue
        L = 1
        for j, a in enumerate(prev):
            if j != i: L *= 1 + a
        best = max(best, min(cp / 2, cp - Fraction(L, 2 ** (p - 1))))
    return best

def covered_f(f):
    """f: dict prime -> exponent (odd primes).  Returns (list of earlier reasons, list of new reasons)."""
    old = []; new = []
    if len(f) <= 2: old.append("Thm2")
    if len(f) == 3 and sorted(f.values())[:2] == [1, 1]: old.append("Thm3")
    for q in [None] + sorted(f):
        fm = {p: a for p, a in f.items() if p != q}
        if not fm: continue
        ps = tuple(sorted(fm))
        if cdigit(ps, tuple(fm[p] for p in ps)) > 0: old.append("Thm6 q=%s" % q)
        G = Gamma(tuple(sorted(fm.items())))
        if G > 0: new.append("Thm7 q=%s Gamma=%s" % (q, G))
    return old, new

def val(f):
    n = 1
    for p, a in f.items(): n *= p ** a
    return n

if __name__ == "__main__":
    if sys.argv[1] == "first":
        # the least uncovered n: search over exponent vectors on the first primes, n below a bound that is raised until
        # an uncovered n is found; then every n below it is covered (all odd n below the bound were enumerated by shape).
        import math
        bound_log = float(sys.argv[2]) if len(sys.argv) > 2 else 60.0     # natural log of the bound
        primes = list(primerange(3, 60))
        best = [None]
        cnt = [0]
        def rec(i, f, logn):
            # f uses primes[0..i-1]; to enumerate all n below the bound up to the smallest representative of the shape
            # we only take exponent vectors on an initial segment of the primes?  No: coverage depends on which primes,
            # so all supports are enumerated.
            if f:
                cnt[0] += 1
                o, nw = covered_f(f)
                if not o and not nw:
                    if best[0] is None or logn < best[0][0]:
                        best[0] = (logn, dict(f))
            for j in range(i, len(primes)):
                p = primes[j]
                lp = math.log(p)
                a = 1
                while logn + a * lp < (best[0][0] if best[0] else bound_log):
                    f[p] = a
                    rec(j + 1, f, logn + a * lp)
                    a += 1
                if p in f: del f[p]
                if logn + lp >= (best[0][0] if best[0] else bound_log): break
        rec(0, {}, 0.0)
        print("exponent vectors examined: %d (primes up to %d, n < e^%.1f or below the least uncovered found)" % (cnt[0], primes[-1], bound_log))
        if best[0] is None:
            print("no uncovered n below e^%.1f = %.3e" % (bound_log, math.exp(bound_log)))
        else:
            f = best[0][1]
            print("least odd n covered by nothing: %d = %s  (about %.3e)" % (val(f), " * ".join("%d^%d" % (p, a) for p, a in sorted(f.items())), float(val(f))))
    else:
        N = int(sys.argv[1])
        unc = []; newly = []
        for n in range(3, N, 2):
            f = factorint(n)
            o, nw = covered_f(f)
            if not o and not nw: unc.append(n)
            elif not o: newly.append(n)
        print("odd n < %d: covered by nothing: %s" % (N, unc[:10]))
        print("odd n < %d: covered by Theorem 7 and by none of Theorems 2, 3, 6: %d; first: %s" % (N, len(newly), newly[:10]))
        for n in (118125, 165375, 3**3 * 5**3 * 7**3, 3**4 * 5**4 * 7**4, 3**7 * 5**2 * 7**2, 3**13 * 5**23 * 7):
            f = factorint(n)
            o, nw = covered_f(f)
            print(n, dict(f), "earlier:", o[:2], "new:", nw)
