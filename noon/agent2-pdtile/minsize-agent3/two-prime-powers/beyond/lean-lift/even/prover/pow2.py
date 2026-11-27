"""Theorem A (n = 2^k): the recursive construction of the proof, as a program, and its exhaustive test.
sign(els, k): els a list of residues modulo 2^k (a nonempty multiset, not two different elements); returns a list of
signs, by the recursion  S(X) = S_E(X^2) + X S_D(X^2)  exactly as in the proof.  The test checks every output with
lib.is_good (exact) and checks that pairs of different elements have no good signing at all."""
import sys, itertools, random
import numpy as np
from lib import is_good, mask, good_signings

def v2(x, k):
    """2-adic valuation of a nonzero residue modulo 2^k"""
    x %= 2 ** k
    assert x != 0
    v = 0
    while x % 2 == 0: x //= 2; v += 1
    return v

def exceptional(els, k):
    return len(els) == 2 and (els[0] - els[1]) % (2 ** k) != 0

def sign(els, k):
    m = len(els)
    assert m >= 1 and not exceptional(els, k)
    if k == 0:
        return [1] * m
    iE = [i for i, x in enumerate(els) if x % 2 == 0]; iD = [i for i, x in enumerate(els) if x % 2 == 1]
    E = [els[i] // 2 for i in iE]; D = [(els[i] - 1) // 2 for i in iD]
    out = [None] * m
    def put(idx, sg):
        for i, s in zip(idx, sg): out[i] = s
    if not D: put(iE, sign(E, k - 1)); return out
    if not E: put(iD, sign(D, k - 1)); return out
    exE, exD = exceptional(E, k - 1), exceptional(D, k - 1)
    if exE and exD:
        vE, vD = v2(E[0] - E[1], k - 1), v2(D[0] - D[1], k - 1)
        if vD >= vE: put(iE, [1, -1]); put(iD, [1, 1])
        else:        put(iE, [1, 1]);  put(iD, [1, -1])
        return out
    # A = a non-exceptional one, C = the other
    if not exE: iA, A, iC, C = iE, E, iD, D
    else:       iA, A, iC, C = iD, D, iE, E
    if len(C) == 1 and exceptional(A, k - 1):      # cannot happen here (A is not exceptional)
        raise AssertionError
    if len(C) >= 2:
        sA = sign(A, k - 1); sigA = abs(sum(sA))
        sC = [1] * len(C)
        if sigA == len(C): sC[0] = -1              # |C| and |C| - 2 are different absolute values
        put(iA, sA); put(iC, sC); return out
    # |C| = 1
    if len(A) % 2 == 0:
        put(iA, sign(A, k - 1)); put(iC, [1]); return out
    assert len(A) >= 3                             # |A| = 1 would be an exceptional pair
    put(iA, [1] * len(A)); put(iC, [1]); return out

def main():
    random.seed(7)
    # every subset of Z_{2^k}, k <= 4
    for k in range(0, 5):
        n = 2 ** k; cnt = 0; exc = 0
        for bits in range(1, 2 ** n):
            els = [x for x in range(n) if bits >> x & 1]
            if exceptional(els, k):
                exc += 1
                _, g = good_signings(n, els); assert not g.any()
                continue
            sg = sign(els, k); cnt += 1
            assert is_good(mask(n, els, sg), n), (n, els, sg)
        print(f'n={n}: all {2**n-1} nonempty subsets: {cnt} signed by the construction, all good; {exc} pairs, none with a good signing', flush=True)
    # every multiset containing 0 of size <= M
    for k, M in ((1, 10), (2, 8), (3, 6), (4, 5)):
        n = 2 ** k; cnt = 0; exc = 0
        for m in range(1, M + 1):
            for rest in itertools.combinations_with_replacement(range(n), m - 1):
                els = [0] + list(rest)
                if exceptional(els, k):
                    exc += 1
                    _, g = good_signings(n, els); assert not g.any()
                    continue
                sg = sign(els, k); cnt += 1
                assert is_good(mask(n, els, sg), n), (n, els, sg)
        print(f'n={n}: all multisets containing 0 of size <= {M}: {cnt} signed, all good; {exc} exceptional pairs, none good', flush=True)
    # random sets and multisets on Z_32 .. Z_1024
    for k in (5, 6, 7, 8, 10):
        n = 2 ** k; cnt = 0
        for trial in range(1500 if k <= 8 else 300):
            kind = trial % 4
            m = random.randint(1, min(n, 40))
            if kind == 0: els = random.sample(range(n), m)
            elif kind == 1: els = [random.randrange(n) for _ in range(m)]
            elif kind == 2:                                   # closed under x -> x + n/2
                half = random.sample(range(n // 2), max(1, m // 2)); els = half + [x + n // 2 for x in half]
            else:                                             # union of cosets of a subgroup, plus a few
                step = 2 ** random.randint(1, k - 1); els = sorted(set(
                    (c + t * step) % n for c in random.sample(range(step), random.randint(1, min(step, 3))) for t in range(n // step)))
                if len(els) > 64: els = els[:64]
            if exceptional(els, k): continue
            sg = sign(els, k); cnt += 1
            assert is_good(mask(n, els, sg), n), (n, els, sg)
        print(f'n={n}: {cnt} random sets, multisets, sets closed under +n/2, unions of cosets: all signed, all good', flush=True)

if __name__ == '__main__':
    main()
