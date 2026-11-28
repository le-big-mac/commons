"""Exact tests of the lemmas of result.md, one by one.
(P)  Lemma P: for every way of writing M <= MMAX as a sum of K parts r_i >= 1, prod c_(r_i) <= 2^(1-K) c*_(M-2K+2); and
     h(K) = 2^(1-K) c*_(M-2K+2) does not increase with K.  Also c_a c_b <= c_2 c_(a+b-2) for a, b <= 300 (c_0 = 1).
(C)  Lemma C: one cell on Z_(pq) (p < q primes), random occupied subclasses of Z_p x Z_q covering every row and every
     column, random multiplicities.  For EVERY choice of the pair of columns (t1, t2) the product of c over the pieces
     of the proof bounds P(bad at pq); for the proof's choice the number of pieces is at least q; the pieces hold
     all elements.
(C2) Lemma C, last sentence: a cell of exactly q elements that is p-full and q-full is never bad at pq (all such cells
     for (3,5) and (3,7), a sample for (5,7)).
(H)  Theorem H: random decorations D beside a heavy element at 0.  V = the integers v with Q + v divisible by some
     Phi_d.  Checks: every such v comes from d = 1 or from a d fully live for D + {0}; and for those d the share of
     signings of D with an integer v_d is at most 2^(1 - kappa(d)).  Prints the largest E|V| met.
usage: test_lemmas.py SEED CASES_C CASES_H MMAX"""
import sys, random, math, itertools
from fractions import Fraction
import numpy as np
from lib import *
def cstar(r): return c(r) if r >= 1 else Fraction(1, 2)
def partitions(M, K, lo=1):
    if K == 1:
        if M >= lo: yield (M,)
        return
    for r in range(lo, M // K + 1):
        for rest in partitions(M - r, K - 1, r): yield (r,) + rest
def test_P(mmax):
    cnt = 0
    for a in range(1, 301):
        for b in range(a, 301):
            assert c(a) * c(b) <= c(2) * c(a + b - 2); cnt += 1
    cnt2 = 0; eq = 0
    for M in range(1, mmax + 1):
        for K in range(1, M + 1):
            h = Fraction(1, 2 ** (K - 1)) * cstar(M - 2 * K + 2)
            if K < M: assert Fraction(1, 2 ** K) * cstar(M - 2 * K) <= h
            for part in partitions(M, K):
                pr = Fraction(1)
                for r in part: pr *= c(r)
                assert pr <= h, (part, pr, h); cnt2 += 1; eq += pr == h
    print(f"(P) c_a c_b <= c_2 c_(a+b-2): {cnt} pairs a <= b <= 300, no violation;  Lemma P: {cnt2} partitions of M <= {mmax}, no violation, equality in {eq}")
def pieces_of(r, p, q, t1, t2):
    """r[s][t] = number of elements in subclass (s, t).  The pieces of the proof of Lemma C for the pair (t1, t2)."""
    out = []
    def group(sizes):                               # sizes[s], s in Z_p: one column, or the pair of columns row by row
        occ = [x for x in sizes if x > 0]
        if len(occ) == 1: return [occ[0]]
        if len(occ) <= p - 1: return occ
        return list(sizes[:p - 2]) + [sizes[p - 2] + sizes[p - 1]]
    for t in range(q):
        if t not in (t1, t2): out += group([r[s][t] for s in range(p)])
    out += group([r[s][t1] + r[s][t2] for s in range(p)])
    return out
def test_C(rng, cases):
    done = 0; tight = 0; pos = 0; minpieces = {}
    for _ in range(cases):
        p, q = rng.choice([(3, 5), (3, 5), (3, 7), (5, 7), (3, 11)]); n = p * q
        occ = set()
        kind = rng.randrange(4)
        if kind == 0:
            for s in range(p): occ.add((s, rng.randrange(q)))
            for t in range(q):
                if not any(o[1] == t for o in occ): occ.add((rng.randrange(p), t))
        elif kind == 1:
            s0 = rng.randrange(p); t0 = rng.randrange(q); occ = {(s0, t) for t in range(q)} | {(s, t0) for s in range(p)}
        elif kind == 2:
            for t in range(q): occ.add((rng.randrange(p), t))
            for s in range(p):
                if not any(o[0] == s for o in occ): occ.add((s, rng.randrange(q)))
            for _ in range(rng.randrange(0, 4)): occ.add((rng.randrange(p), rng.randrange(q)))
        else:
            s0 = rng.randrange(p); occ = {(s0, t) for t in range(q)}
            for s in range(p):
                if s != s0 and rng.random() < 0.7: occ |= {(s, t) for t in range(q) if rng.random() < 0.5}
            for s in range(p):
                if not any(o[0] == s for o in occ): occ.add((s, rng.randrange(q)))
        occ = sorted(occ)
        if len(occ) > 13: continue
        mult = rng.choice(((2,), (2, 2, 4), (1,), (1, 2), (1, 2, 3)))
        r = [[0] * q for _ in range(p)]
        for (s, t) in occ: r[s][t] = rng.choice(mult)
        if rng.random() < 0.4: s, t = rng.choice(occ); r[s][t] = rng.randrange(3, 10)
        items = [(next(x for x in range(n) if x % p == s and x % q == t), r[s][t]) for (s, t) in occ]
        if math.prod(a + 1 for _, a in items) > 300_000: continue
        S, W, m = grid(items); P = Fraction(int(W[bad_mask(n, items, S)].sum()), 2 ** m)
        # the proof's choice of the pair
        cols = [[s for s in range(p) if r[s][t]] for t in range(q)]
        multi = [t for t in range(q) if len(cols[t]) >= 2]
        if multi:
            t0 = multi[0]; t1, t2 = [t for t in range(q) if t != t0][:2]
        else:
            t1 = 0; t2 = next(t for t in range(q) if cols[t] != cols[0])
        pc = pieces_of(r, p, q, t1, t2)
        assert len(pc) >= q, (r, pc); assert sum(pc) == m
        minpieces[(p, q)] = min(minpieces.get((p, q), 99), len(pc))
        for a in range(q):
            for b in range(a + 1, q):
                pcs = pieces_of(r, p, q, a, b); assert sum(pcs) == m
                bound = Fraction(1)
                for x in pcs: bound *= c(x)
                assert P <= bound, (p, q, r, a, b, P, bound)
                if (a, b) == (min(t1, t2), max(t1, t2)) and P == bound: tight += 1
        done += 1; pos += P > 0
    print(f"(C) cells full for two primes tested: {done}; P(bad at pq) > 0 in {pos}; no violation for any pair of columns; equality with the proof's pieces in {tight}; least number of pieces met {minpieces}")
def test_C2(rng):
    """exactly q elements, one in each column, every row occupied: never bad at pq (Lemma C, last sentence)."""
    out = []
    for (p, q, sample) in ((3, 5, None), (3, 7, None), (5, 7, 3000)):
        n = p * q; cnt = 0; pos = 0
        rows_iter = itertools.product(range(p), repeat=q) if sample is None else (tuple(rng.randrange(p) for _ in range(q)) for _ in range(sample))
        for rows in rows_iter:
            if len(set(rows)) < p: continue
            items = [(next(x for x in range(n) if x % p == rows[t] and x % q == t), 1) for t in range(q)]
            S, W, m = grid(items); pos += bool(bad_mask(n, items, S).any()); cnt += 1
        out.append(f"({p}, {q}): {cnt} cells, bad at pq in {pos}")
    print("(C2) cells of exactly q elements full for both primes: " + "; ".join(out))
def test_H(rng, cases):
    done = 0; fl = 0; maxE = Fraction(0); exE = None; maxr = Fraction(0)
    for _ in range(cases):
        n = rng.choice([3, 9, 27, 81, 15, 45, 75, 105, 21, 63, 315, 35, 5, 25])
        f = factor(n); items = {}
        for _ in range(rng.randrange(1, 9)):
            if rng.random() < 0.7:
                p = rng.choice(list(f)); b = (n // p ** rng.randrange(1, f[p] + 1)) * rng.randrange(1, p) % n
            else: b = rng.randrange(1, n)
            items[b] = items.get(b, 0) + rng.choice((1, 1, 2, 2, 3, 4))
        items = sorted(items.items())
        if math.prod(a + 1 for _, a in items) > 200_000: continue
        S, W, r = grid(items); G = S.shape[1]; tot = 2 ** r; elems = [0] + [b for b, _ in items]
        vals = {}
        for d in divisors(n):
            V = red(d)[:, [b % d for b, _ in items]] @ S
            isint = ~np.any(V[1:] != 0, axis=0) if V.shape[0] > 1 else np.ones(G, dtype=bool)
            vals[d] = (isint, -V[0])
        live = [1] + [d for d in divisors(n) if d > 1 and fully_live(d, elems) is not None]
        BIG = 10 ** 9
        def distinct(ds):
            M = np.full((len(ds), G), BIG, dtype=np.int64)
            for i, d in enumerate(ds): M[i, vals[d][0]] = vals[d][1][vals[d][0]]
            M.sort(axis=0); new = np.ones_like(M, dtype=bool); new[1:] = M[1:] != M[:-1]
            return ((M != BIG) & new).sum(axis=0)
        nall = distinct(divisors(n)); nlive = distinct(live)
        assert (nall == nlive).all(), (n, items)                       # every value comes from 1 or a fully live d
        for d in live[1:]:
            ranks = fully_live(d, elems); k = kappa(ranks); pd = Fraction(int(W[vals[d][0]].sum()), tot)
            assert pd <= Fraction(1, 2 ** (k - 1)), (n, items, d, ranks, pd); fl += 1
            maxr = max(maxr, pd * 2 ** (k - 1))
        E = Fraction(int((W * nall.astype(object)).sum()), tot)
        if E > maxE: maxE = E; exE = (n, items)
        done += 1
    print(f"(H) decorations tested: {done}; fully live divisors met {fl}; no violation; largest P(v_d integer) 2^(kappa-1) = {float(maxr):.4f}; largest E|V| met {maxE} = {float(maxE):.4f} at {exE}")
if __name__ == '__main__':
    seed, cc, ch, mmax = map(int, sys.argv[1:5]); rng = random.Random(seed)
    test_P(mmax); test_C(rng, cc); test_H(rng, ch); test_C2(rng)
