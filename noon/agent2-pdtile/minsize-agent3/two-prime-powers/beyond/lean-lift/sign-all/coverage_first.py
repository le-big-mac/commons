# coverage_first.py -- the least odd n covered by none of Theorems 2, 3, 6, 7.
# Monotonicity (result file, section 5): if n' has the primes p'_1 < .. < p'_k with exponents e_1..e_k and n has the
# first k odd primes 3, 5, 7, .. with the same exponents in the same order, then "n covered" implies "n' covered"
# (lam(p, a) decreases and single(p, a) does not decrease when p grows; Theorems 2, 3 depend on the exponents only;
# the digit recursion is monotone in the same way).  So the least uncovered n has an initial segment of the odd primes
# as its support, and it is enough to enumerate exponent vectors (e_1..e_k), all e_j >= 1, with n below a bound.
# usage: python coverage_first.py LOG10BOUND
import sys, math
from fractions import Fraction
from sympy import primerange
from coverage2 import Gamma, cdigit, lam, single

def greedy(trees):
    """Gamma along the order of increasing primes (a lower bound for Gamma)."""
    G = single(*trees[0]); L = trees[0][1] + 1
    for (p, a) in trees[1:]:
        cand = min(single(p, a) * G, Fraction(3, 4) * G - L * lam(p, a))
        if a == 1: cand = max(cand, min(G / 2, G - Fraction(L, 2 ** (p - 1))))
        if cand <= 0: return cand
        G = cand; L *= a + 1
    return G

def lamf(p, a):
    w = 2.0 ** (1 - p)
    return w * (1 - w ** a) / (1 - w)
def singlef(p, a):
    return 0.5 if (a == 1 or p >= 5) else 0.625 - lamf(3, a)
def greedy_float(trees):
    """the same in floating point; only a value above 1e-9 is trusted (rounding errors are below 1e-13), anything
    else is recomputed with exact fractions."""
    G = singlef(*trees[0]); L = trees[0][1] + 1
    for (p, a) in trees[1:]:
        cand = min(singlef(p, a) * G, 0.75 * G - L * lamf(p, a))
        if a == 1: cand = max(cand, min(G / 2, G - L * 2.0 ** (1 - p)))
        if cand <= 1e-9: return -1.0
        G = cand; L *= a + 1
    return G

stats = {"examined": 0, "thm23": 0, "greedy": 0, "full": 0, "digit": 0, "uncovered": 0, "undetermined": 0}
def covered(primes, exps):
    k = len(exps)
    stats["examined"] += 1
    if k <= 2 or (k == 3 and sorted(exps)[:2] == [1, 1]):
        stats["thm23"] += 1; return True
    items = list(zip(primes[:k], exps))
    for qi in [None] + list(range(k)):
        trees = tuple(t for j, t in enumerate(items) if j != qi)
        if greedy_float(trees) > 1e-9 or greedy(trees) > 0:
            stats["greedy"] += 1; return True
    if k <= 9:
        for qi in [None] + list(range(k)):
            trees = tuple(t for j, t in enumerate(items) if j != qi)
            if Gamma(trees) > 0:
                stats["full"] += 1; return True
        for qi in [None] + list(range(k)):
            trees = tuple(t for j, t in enumerate(items) if j != qi)
            if cdigit(tuple(p for p, a in trees), tuple(a for p, a in trees)) > 0:
                stats["digit"] += 1; return True
        stats["uncovered"] += 1
        return False
    stats["undetermined"] += 1
    return None

def main():
    bound = float(sys.argv[1]) * math.log(10)
    primes = list(primerange(3, 200))
    best = [None]; undet = []
    def rec(i, exps, logn):
        if exps:
            c = covered(primes, exps)
            if c is False:
                if best[0] is None or logn < best[0][0]: best[0] = (logn, list(exps))
            elif c is None:
                undet.append(list(exps))
        lp = math.log(primes[i])
        a = 1
        while logn + a * lp < (best[0][0] if best[0] else bound):
            exps.append(a)
            rec(i + 1, exps, logn + a * lp)
            exps.pop()
            a += 1
    rec(0, [], 0.0)
    print("exponent vectors on initial segments of the odd primes examined: %s" % stats)
    if undet: print("undetermined (more than 9 primes and the greedy order failed): %d, e.g. %s" % (len(undet), undet[:3]))
    if best[0] is None:
        print("every such n below 10^%s is covered" % sys.argv[1])
    else:
        e = best[0][1]; n = 1
        for p, a in zip(primes, e): n *= p ** a
        print("least odd n covered by nothing: %d = %s (about %.3e)" % (n, " * ".join("%d^%d" % (p, a) for p, a in zip(primes, e)), float(n)))

if __name__ == "__main__":
    main()
