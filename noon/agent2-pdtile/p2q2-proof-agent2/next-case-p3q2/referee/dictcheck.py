"""Referee: validate the 'dictionary' of Lemma M (zero set of A = (X + P) u (Y + Q) from data of X and Y) against a direct
computation on subsets of Z_M by FFT (floating point, tolerance 1e-7), a route that does not use cuboid sums.
 (1) p q random: random X, Y of random sizes with disjoint K-supports; compare assembled and direct zero sets.
 (2) for p = 2, q = 3 with --all: list all 1,137,312 unions of 3 cosets of P and 2 cosets of Q directly in Z_72, direct zero
     sets by FFT, and compare the histogram of zero sets with the one mixedsig.py produced from signatures.
usage: dictcheck.py p q [ntrials] [--all]"""
import sys, os, itertools, random, pickle
import numpy as np
from collections import Counter
import mixedsig as ms
p, q, a, b = ms.p, ms.q, 3, 2; M, MX, MY, G = ms.M, ms.MX, ms.MY, ms.G; ORDS = ms.ORDS; val = ms.val
freq = [M // val(o) for o in ORDS]                      # a frequency of order p^l q^m
def direct(ind):                                        # ind: (rows, M) 0/1
    F = np.fft.fft(ind.astype(float), axis=1)[:, freq]
    return np.abs(F) < 1e-7
def assemble(X, Y):
    xi = np.zeros((1, MX), dtype=np.int64); xi[0, X] = 1; yi = np.zeros((1, MY), dtype=np.int64); yi[0, Y] = 1
    cnt = p * ms.fold(xi, G) + q * ms.fold(yi, G); out = []
    for o in ORDS:
        if o == (3, 2): z = True
        elif o[0] == 3: z = bool(ms.zero_tests(ms.fold(yi, val(o)), o)[0])
        elif o[1] == 2: z = bool(ms.zero_tests(ms.fold(xi, val(o)), o)[0])
        else: z = bool(ms.zero_tests(ms.fold(cnt, val(o)), o)[0])
        out.append(z)
    return out
random.seed(11); nt = int(sys.argv[3]) if len(sys.argv) > 3 and sys.argv[3].isdigit() else 20000; bad = 0; done = 0; nz = Counter()
while done < nt:
    # structured random choices, so that many zeros occur: unions of random cosets of random subgroups, plus noise
    def rnd(mod):
        S = set()
        for _ in range(random.randint(1, 3)):
            d = random.choice([d for d in range(1, mod + 1) if mod % d == 0]); x = random.randrange(mod)
            S |= {(x + t * d) % mod for t in range(mod // d)} if mod // d <= 12 else {x}
        if random.random() < 0.3: S |= {random.randrange(mod)}
        return sorted(S)
    X = rnd(MX); Y = rnd(MY)
    if {x % G for x in X} & {y % G for y in Y}: continue
    A = np.zeros((1, M), dtype=np.int64)
    for x in X:
        for t in range(p): A[0, (x + t * MX) % M] += 1
    for y in Y:
        for t in range(q): A[0, (y + t * MY) % M] += 1
    assert A.max() == 1 and A.sum() == p * len(X) + q * len(Y)
    z1 = list(direct(A)[0]); z2 = assemble(X, Y); done += 1; nz[sum(z2)] += 1
    if z1 != z2: bad += 1; print("DICTIONARY MISMATCH", X, Y, z1, z2)
print(f"Z_{M} (p = {p}, q = {q}): {done} random pairs (X, Y) with disjoint K-supports; assembled zero set != direct zero set: {bad};  number of zeros -> cases: {dict(sorted(nz.items()))}")
if '--all' in sys.argv:
    n = p * p * q; i, j = 3, 2; assert (p, q) == (2, 3)
    Pl = [[(x + t * MX) % M for t in range(p)] for x in range(MX)]; Ql = [[(y + t * MY) % M for t in range(q)] for y in range(MY)]
    IP = np.zeros((MX, M), dtype=np.int8); IQ = np.zeros((MY, M), dtype=np.int8)
    for x in range(MX): IP[x, Pl[x]] = 1
    for y in range(MY): IQ[y, Ql[y]] = 1
    hist = Counter(); tot = 0
    Qc = list(itertools.combinations(range(MY), j)); QI = np.array([IQ[list(c)].sum(0) for c in Qc]); QK = [frozenset(y % G for y in c) for c in Qc]
    for cp in itertools.combinations(range(MX), i):
        kp = {x % G for x in cp}; ok = np.array([not (kp & kq) for kq in QK])
        if not ok.any(): continue
        A = QI[ok] + IP[list(cp)].sum(0); assert A.max() == 1
        z = direct(A); code = (z.astype(np.int64) << np.arange(len(ORDS))).sum(1)
        for c_, m_ in zip(*np.unique(code, return_counts=True)): hist[int(c_)] += int(m_)
        tot += len(A)
    dec = lambda c_: frozenset(o for t, o in enumerate(ORDS) if c_ >> t & 1)
    H1 = {dec(c_): m_ for c_, m_ in hist.items()}
    H2 = pickle.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"mixedsig_{p}_{q}.pkl"), 'rb'))['hist']
    print(f"   direct listing in Z_{M}: {tot:,} sets, {len(H1)} zero sets;  histogram identical to the one from signatures: {H1 == H2}")
