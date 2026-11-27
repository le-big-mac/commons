"""The two final statements, literally, with ExceptionalPair computed from ITS definition.

For n and a multiset w : Z_n -> N (every multiset of the given sizes, no reduction by translation):
  good splitting: u, v with u + v = w and no Phi_d, d | n, dividing maskW u - maskW v = sum_x (u_x - v_x) X^x
                  (exponents x = 0..n-1; divisibility by exact long division)
  ExceptionalPair w: there are a, b in Z_n with w = single(a) + single(b) (as functions) and the additive order of
                  a - b in Z_n is even; the order is found by adding a - b to itself until 0 comes (not by a formula)
Checked: for every nonempty w:  (a good splitting exists)  <=>  not ExceptionalPair w.
(exists_signs_all is "<=" for nonempty w, not_exists_signs_of_exceptionalPair is "=>".)
Also printed: what the conjecture's words say ("two elements a, b with 2^k not dividing a - b") against the definition.

usage: t5_final.py NMIN NMAX SIZEMAX
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import time
from itertools import combinations_with_replacement, product
from ecore import cyclo, divisors, pdivmod


def add_order(x, n):
    """the least t >= 1 with t * x = 0 in Z_n"""
    t = 1
    y = x % n
    while y != 0:
        y = (y + x) % n
        t += 1
    return t


def exceptional_by_definition(w, n):
    for a in range(n):
        for b in range(n):
            s = [0] * n
            s[a] += 1
            s[b] += 1
            if s == w and add_order((a - b) % n, n) % 2 == 0:
                return True
    return False


def exceptional_by_words(w, n):
    """two elements a, b (counted with multiplicity) with 2^k not dividing a - b, 2^k the power of 2 in n"""
    els = [x for x in range(n) for _ in range(w[x])]
    if len(els) != 2:
        return False
    k2 = 1
    while n % (2 * k2) == 0:
        k2 *= 2
    return (els[0] - els[1]) % k2 != 0


def has_good_splitting(w, n, cyc):
    supp = [x for x in range(n) if w[x]]
    for us in product(*[range(w[x] + 1) for x in supp]):
        mask = [0] * n
        for x, u in zip(supp, us):
            mask[x] = u - (w[x] - u)
        good = True
        for c in cyc:
            _, r = pdivmod(mask, c)
            if not any(r):
                good = False
                break
        if good:
            return True
    return False


def main():
    nmin, nmax, smax = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    t0 = time.time()
    for n in range(nmin, nmax + 1):
        cyc = [list(cyclo(d)) for d in divisors(n)]
        tot = exc = good = mismatch = words_mismatch = 0
        exc_double = 0
        for size in range(0, smax + 1):
            for els in combinations_with_replacement(range(n), size):
                w = [0] * n
                for x in els:
                    w[x] += 1
                e = exceptional_by_definition(w, n)
                g = has_good_splitting(w, n, cyc)
                ew = exceptional_by_words(w, n)
                if size == 0:
                    # the empty multiset: not exceptional, and no good splitting (the mask is 0): hw is needed
                    assert not e and not g
                    continue
                tot += 1
                exc += e
                good += g
                if g == e:
                    mismatch += 1
                    print("   MISMATCH", n, els, "exceptional", e, "good splitting", g)
                if e != ew:
                    words_mismatch += 1
                    print("   WORDS DIFFER", n, els, e, ew)
                if size == 2 and els[0] == els[1]:
                    assert not e and g
                    exc_double += 1
            if time.time() - t0 > 270:
                print(f"   (stopped by the clock at n = {n}, size {size})")
                return
        print(f"n={n}: nonempty multisets of size <= {smax}: {tot}; exceptional pairs (definition) {exc}; with a good "
              f"splitting {good}; mismatches of 'good splitting iff not exceptional' {mismatch}; definition against "
              f"'two elements with 2^k not dividing a - b': {words_mismatch} differences; the {exc_double} doubled "
              f"marks are not exceptional and have a good splitting ({time.time() - t0:.0f} s)")
        sys.stdout.flush()


main()
