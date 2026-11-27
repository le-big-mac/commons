"""Referee's enumeration for Lemma 2 of sign-general-result.md and for the case k = 1 of Theorem P.

(c)  for a sign vector s_0, the number of sign vectors s with <s, s_0> = 0 in F is at most 2^(p-1) - 2
     (through <s, s_0> = p - 2j, j = number of places where they differ; that identity itself by enumeration for p <= 9);
(d)  for every subspace K of F_q^p with 0 != K != F_q^p: at most 2^(p-1) sign vectors in K u K-perp.
     Every subspace is listed (reduced row echelon forms) for the pairs (p, q) named below.
k=1  for every nonzero f in F_q^p at least 2^(p-1) sign vectors s make s*f good at both levels (sum != 0, not constant).
usage: lemma2_own.py c | d P Q DIMS | k1
"""
import sys, time
import numpy as np
from itertools import product, combinations
from math import comb

def is_prime(n):
    return n > 1 and all(n % d for d in range(2, int(n ** 0.5) + 1))

def part_c():
    # the identity <s, s0> = p - 2j by enumeration
    for p in (3, 5, 7, 9):
        S = np.array(list(product((1, -1), repeat=p)), dtype=np.int64)
        s0 = S[37 % len(S)]
        assert all(int(s @ s0) == p - 2 * int((s != s0).sum()) for s in S)
    worst = None; n = 0
    for p in range(3, 152, 2):
        # over Q
        J = [j for j in range(p + 1) if p - 2 * j == 0]
        assert not J
        for q in range(3, 400):
            if not is_prime(q) or p % q == 0: continue
            cnt = sum(comb(p, j) for j in range(p + 1) if (p - 2 * j) % q == 0)
            assert cnt <= 2 ** (p - 1) - 2, (p, q, cnt)
            n += 1
            ratio = cnt / (2 ** (p - 1) - 2)
            if worst is None or ratio > worst[0]: worst = (ratio, p, q, cnt)
    print(f'Lemma 2(c): all odd p from 3 to 151, all odd primes q < 400 not dividing p ({n} pairs) and Q: the count is at most 2^(p-1) - 2; '
          f'closest: p = {worst[1]}, q = {worst[2]}: {worst[3]} against {2 ** (worst[1] - 1) - 2}')
    # and what happens when q divides p (outside the hypothesis), for information
    bad = [(p, q) for p in range(3, 60, 2) for q in range(3, 60) if is_prime(q) and p % q == 0
           and sum(comb(p, j) for j in range(p + 1) if (p - 2 * j) % q == 0) > 2 ** (p - 1) - 2]
    print(f'   (for information, q dividing p, p < 60: pairs where the count exceeds 2^(p-1) - 2: {bad})')

def rref_subspaces(p, q, d):
    """all d-dimensional subspaces of F_q^p as reduced row echelon bases (d x p integer arrays)."""
    for piv in combinations(range(p), d):
        free = [(i, c) for i in range(d) for c in range(piv[i] + 1, p) if c not in piv]
        base = np.zeros((d, p), dtype=np.int64)
        for i, c in enumerate(piv): base[i, c] = 1
        for vals in product(range(q), repeat=len(free)):
            Mx = base.copy()
            for (i, c), v in zip(free, vals): Mx[i, c] = v
            yield Mx

def part_d(p, q, dims):
    assert p % 2 == 1 and is_prime(q) and q % 2 == 1 and p % q != 0
    S = np.array(list(product((1, -1), repeat=p)), dtype=np.int64)       # 2^p sign vectors
    Smod = S % q
    codes = {tuple(r) for r in Smod.tolist()}
    t0 = time.time()
    for d in dims:
        coeffs = np.array(list(product(range(q), repeat=d)), dtype=np.int64)    # q^d coefficient vectors
        worst = 0; nsub = 0; nworst = 0
        for B in rref_subspaces(p, q, d):
            nsub += 1
            # sign vectors in K: s is in K iff s equals its projection: in RREF, the coefficients are the entries at the pivots
            piv = [int(np.nonzero(B[i])[0][0]) for i in range(d)]
            inK = ((Smod[:, piv] @ B) % q == Smod).all(axis=1)
            inKp = ((S @ B.T) % q == 0).all(axis=1)
            cnt = int((inK | inKp).sum())
            if cnt > worst: worst = cnt; nworst = 0
            if cnt == worst: nworst += 1
            assert cnt <= 2 ** (p - 1), (p, q, B)
        from math import prod
        gauss = prod(q ** (p - i) - 1 for i in range(d)) // prod(q ** (d - i) - 1 for i in range(d))
        assert nsub == gauss
        print(f'Lemma 2(d): p = {p}, q = {q}, all {nsub} subspaces K of dimension {d} (with K-perp of dimension {p - d}): '
              f'largest number of sign vectors in K u K-perp = {worst} (bound {2 ** (p - 1)}), attained {nworst} times  [{time.time() - t0:.0f} s]', flush=True)

def part_k1():
    for p, q in [(3, 5), (3, 7), (3, 11), (5, 3), (5, 7), (7, 3), (7, 5), (9, 5)]:
        S = np.array(list(product((1, -1), repeat=p)), dtype=np.int64)
        least = 2 ** p; nf = 0
        if q ** p > 400000:
            rng = np.random.default_rng(1); F = rng.integers(0, q, size=(60000, p))
            # and all vectors with entries in {0, 1, q-1}
            F = np.concatenate([F, np.array(list(product((0, 1, q - 1), repeat=p)), dtype=np.int64)])
            note = 'a sample of 60000 and all vectors with entries 0, 1, -1'
        else:
            F = np.array(list(product(range(q), repeat=p)), dtype=np.int64); note = 'every nonzero f'
        F = F[F.any(axis=1)]
        for start in range(0, len(F), 2000):
            Fc = F[start:start + 2000]
            H = Fc[:, None, :] * S[None, :, :]                       # (nf, 2^p, p)
            tot = H.sum(axis=2) % q != 0
            nonconst = ((H - H[:, :, :1]) % q != 0).any(axis=2)
            good = (tot & nonconst).sum(axis=1)
            least = min(least, int(good.min())); nf += len(Fc)
        print(f'k = 1: p = {p}, q = {q}, {note} ({nf}): least number of good sign vectors {least} (bound 2^(p-1) = {2 ** (p - 1)})')
        assert least >= 2 ** (p - 1)

if __name__ == '__main__':
    if sys.argv[1] == 'c': part_c()
    elif sys.argv[1] == 'k1': part_k1()
    else:
        p, q = int(sys.argv[2]), int(sys.argv[3]); dims = [int(x) for x in sys.argv[4].split(',')]
        part_d(p, q, dims)
