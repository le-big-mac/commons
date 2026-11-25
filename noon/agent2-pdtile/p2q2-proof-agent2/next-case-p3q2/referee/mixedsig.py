"""Referee: EXHAUSTIVE check of Lemma M on all 'line unions' of size p^2 q in Z_{p^3 q^2}, by a route different from the
author's mixedlemmas.py: the set A = (X + P) u (Y + Q), X in Z_M/P = Z_{p^2 q^2}, Y in Z_M/Q = Z_{p^3 q}, is never listed.
Instead all X and all Y of the sizes allowed by M0 are listed separately and reduced to 'signatures'
   X: (zero bits at the orders (l, 2), l = 0, 1, 2;  the counts of X modulo G = p^2 q = M/(pq))
   Y: (zero bits at the orders (3, m), m = 0, 1;     the counts of Y modulo G)
and the zero set of A is assembled from a pair of signatures:
   (3, 2) always;  (3, m) from Y;  (l, 2) from X;  (l, m), l <= 2, m <= 1  from the counts  p N^X + q N^Y  modulo p^l q^m.
The cosets lie in different cosets of K iff the supports of the two count vectors modulo G are disjoint.
(The assembly rule is the 'dictionary' of Lemma M; it is validated separately in dictcheck.py by direct computation on
subsets of Z_M.)
usage: mixedsig.py p q"""
import sys, itertools, os
import numpy as np
from collections import Counter, defaultdict

p, q = int(sys.argv[1]), int(sys.argv[2]); a, b = 3, 2
M = p**a * q**b; MX = M // p; MY = M // q; G = M // (p * q)
ORDS = [(l, m) for l in range(a + 1) for m in range(b + 1) if (l, m) != (0, 0)]
val = lambda o: p**o[0] * q**o[1]


def zero_tests(counts, o):
    """counts: (rows, d) integer array of counts modulo d = p^l q^m; returns boolean vector: Phi_d divides the set"""
    l, m = o; d = val(o); idx = np.arange(d)
    if l and m:
        t = counts - counts[:, (idx + d // p) % d] - counts[:, (idx + d // q) % d] + counts[:, (idx + d // p + d // q) % d]
    elif l:
        t = counts - counts[:, (idx + d // p) % d]
    else:
        t = counts - counts[:, (idx + d // q) % d]
    return (t == 0).all(1)


def fold(counts, d):
    """counts modulo D (rows, D) -> counts modulo d, d | D"""
    D = counts.shape[1]
    return counts.reshape(counts.shape[0], D // d, d).sum(1)


def signatures(mod, size, orders, chunk=400000):
    """all subsets of Z_mod of the given size -> dict (bits tuple, counts mod G tuple) -> multiplicity"""
    out = Counter(); it = itertools.combinations(range(mod), size); total = 0
    base = max(mod // G, 1) + 1
    weights = (base ** np.arange(G, dtype=object)).astype(object)
    assert base ** G * 8 < 2**63, "signature does not fit in 63 bits"
    weights = np.array([base**t for t in range(G)], dtype=np.int64)
    while True:
        flat = np.fromiter(itertools.chain.from_iterable(itertools.islice(it, chunk)), dtype=np.int64)
        if flat.size == 0: break
        sets = flat.reshape(-1, size); n = sets.shape[0]; total += n
        ind = np.zeros((n, mod), dtype=np.int16); ind[np.arange(n)[:, None], sets] = 1
        cnt = fold(ind, G)
        bits = np.zeros(n, dtype=np.int64)
        for t, o in enumerate(orders):
            bits |= zero_tests(fold(ind, val(o)), o).astype(np.int64) << t
        key = cnt.astype(np.int64) @ weights + bits * (base ** G)
        u, c = np.unique(key, return_counts=True)
        for k, m_ in zip(u.tolist(), c.tolist()): out[k] += m_
    # decode
    sig = []
    for k, m_ in out.items():
        bits = k // (base ** G); r = k % (base ** G); cv = []
        for _ in range(G): cv.append(r % base); r //= base
        sig.append((bits, cv, m_))
    return sig, total


def main():
    n = p * p * q
    splits = [(i, (n - i * p) // q) for i in range(1, n // p + 1) if (n - i * p) % q == 0 and (n - i * p) // q >= 1]
    print(f"Z_{M} (p = {p}, q = {q}); X in Z_{MX}, Y in Z_{MY}, K-cosets = classes modulo {G}; size p^2 q = {n}; splits (i, j) = {splits}", flush=True)
    assert all(j % p == 0 and i == q * (p - j // p) for i, j in splits), "M0's description of the splits fails"
    Xo = [(l, 2) for l in range(3)]; Yo = [(3, m) for m in range(2)]
    low = [(l, m) for l in range(3) for m in range(2) if (l, m) != (0, 0)]
    hist = Counter(); histK = Counter(); nsets = 0
    for i, j in splits:
        sx, tx = signatures(MX, i, Xo); sy, ty = signatures(MY, j, Yo)
        print(f"  split ({i}, {j}): {tx:,} sets X -> {len(sx):,} signatures; {ty:,} sets Y -> {len(sy):,} signatures", flush=True)
        YS = np.array([s[1] for s in sy], dtype=np.int64); YB = np.array([s[0] for s in sy], dtype=np.int64); YM = np.array([s[2] for s in sy], dtype=np.int64)
        Ysupp = YS > 0; YK = ((YS == 0) | (YS == p)).all(1)
        for xb, xc, xm in sx:
            xc = np.array(xc, dtype=np.int64)
            ok = ~(Ysupp & (xc > 0)).any(1)
            if not ok.any(): continue
            ys = YS[ok]; yb = YB[ok]; ym = YM[ok]; yk = YK[ok]
            cntA = p * xc + q * ys
            code = np.zeros(len(ys), dtype=np.int64)
            for t, o in enumerate(ORDS):
                if o == (3, 2): z = np.ones(len(ys), bool)
                elif o[0] == 3: z = (yb >> Yo.index(o) & 1).astype(bool)
                elif o[1] == 2: z = np.full(len(ys), bool(xb >> Xo.index(o) & 1))
                else: z = zero_tests(fold(cntA, val(o)), o)
                code |= z.astype(np.int64) << t
            xk = bool(((xc == 0) | (xc == q)).all())
            for c_, m_, k_ in zip(code.tolist(), ym.tolist(), yk.tolist()):
                hist[c_] += xm * m_; nsets += xm * m_
                if xk and k_: histK[c_] += xm * m_
    print(f"  total number of unions of i cosets of P and j cosets of Q in different cosets of K, size {n}: {nsets:,};  distinct zero sets: {len(hist)}")
    dec = lambda c_: frozenset(o for t, o in enumerate(ORDS) if c_ >> t & 1)
    H = {dec(c_): m_ for c_, m_ in hist.items()}; HK = {dec(c_): m_ for c_, m_ in histK.items()}
    # Lemma M
    m2 = sum(m_ for Z, m_ in H.items() if {(1, 0), (3, 1), (2, 2)} <= Z); m2K = sum(m_ for Z, m_ in HK.items() if {(1, 0), (3, 1), (2, 2)} <= Z)
    m3 = sum(m_ for Z, m_ in H.items() if (0, 1) in Z)
    m4 = sum(m_ for Z, m_ in H.items() if {(0, 1), (1, 2)} <= Z)
    print(f"  M2: sets with the zeros p, p^3 q, p^2 q^2: {m2:,}; of these invariant under K: {m2K:,}   -> {'OK' if m2 == m2K else 'LEMMA M2 FAILS'}")
    print(f"  M3: sets with the zero q: {m3:,}" + (f"   -> {'OK' if m3 == 0 else 'LEMMA M3 FAILS'}" if p < q else "   (p > q: M3 says nothing)"))
    print(f"  M4: sets with the zeros q and p q^2: {m4:,}   -> {'OK' if m4 == 0 else 'LEMMA M4 FAILS'}")
    # the H patterns of the author's classification
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'orig'))
    import exact
    cnt, hard = exact.classify(p, a, q, b)
    hs = [Z for Z, s in hard if s == n]
    hit = [(sorted(Z), H[Z]) for Z in hs if Z in H]
    print(f"  the {len(hs)} patterns of category H with size {n}: realised by a line union of that size: {len(hit)}  {hit}")
    other = Counter(exact.CAT[Z] for Z in H)
    print(f"  categories (exact.py) of the {len(H)} zero sets realised: {dict(other)}")
    # is any of these sets a weak tile?  A is a weak tile iff |A| = D^w(Z(A)).  (needs D^w for each realised pattern)
    import pickle
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"mixedsig_{p}_{q}.pkl"), 'wb') as fh:
        pickle.dump({'hist': H, 'histK': HK, 'n': n}, fh)


if __name__ == '__main__':
    main()
