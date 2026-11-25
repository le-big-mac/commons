"""Referee: tests of the lemmas on actual sets, with the referee's own code (exact arithmetic unless said otherwise).
 (i)   LP model against the definition: for random sets A (tiles and non-tiles) of Z_M, the optimal step function g of
       LP(Z(A)) satisfies 1_A * g = |A| sigma / M exactly (so the rows of the programme are the right ones), and
       D^w(Z(A)) <= |A| with equality for tiles.
 (ii)  Lemma C: pieces with (T1), (T2), no orphan and the same S'  =>  A has (T1), (T2), no orphan and the stated S_A.
 (iii) Lemma E.4 / E.3 through D^w:  A = preimage of A' under Z_M -> Z_M/P:  Z(A) = Z(A') u {(a, m)} and
       [A weak tile <=> A' weak tile];   and for tiles A whose optimal face has x = 1: A -> A/P injective and A/P a weak tile,
       zeros with l < a agree, p^a not a zero.
 (iv)  the lines lemma by brute force in small groups (all subsets of Z_12, Z_18, Z_20, Z_24; all arrays with entries 0..2 on Z_12).
 (v)   the step of M4 for p = 3, q = 2: no X in Z_36 with 2, 4 or 6 elements and Phi_12 | X has a class modulo 2 with one element.
usage: lemmatests.py [seed]"""
import sys, random, itertools, cmath
from fractions import Fraction as Fr
from collections import Counter
import numpy as np
from reflp import solve_lp
random.seed(int(sys.argv[1]) if len(sys.argv) > 1 else 3)


class Grp:
    def __init__(s, p, a, q, b):
        s.p, s.a, s.q, s.b = p, a, q, b; s.M = p**a * q**b
        s.cls = [(i, j) for i in range(a + 1) for j in range(b + 1)]; s.ords = [o for o in s.cls if o != (0, 0)]
        def csum(pp, n, l, i):
            sub = lambda t: (pp ** (n - t) if l <= t else 0)
            return sub(i) - (sub(i + 1) if i < n else 0)
        s.C = {(o, c): csum(p, a, o[0], c[0]) * csum(q, b, o[1], c[1]) for o in s.cls for c in s.cls}
        s.size = [s.C[((0, 0), c)] for c in s.cls]
        def v(x, r, cap):
            if x == 0: return cap
            e = 0
            while x % r == 0: x //= r; e += 1
            return e
        s.clsof = [(v(x % p**a, p, a), v(x % q**b, q, b)) for x in range(s.M)]
        s.val = lambda o: p**o[0] * q**o[1]
    def zeros(s, A):
        """exact zero set of a set or multiset A (list of residues), by cuboid sums of counts"""
        out = set(); p, q = s.p, s.q
        for o in s.ords:
            l, m = o; d = s.val(o); N = [0] * d
            for x in A: N[x % d] += 1
            if l and m: z = all(N[c] - N[(c + d // p) % d] - N[(c + d // q) % d] + N[(c + d // p + d // q) % d] == 0 for c in range(d))
            elif l: z = all(N[c] == N[(c + d // p) % d] for c in range(d))
            else: z = all(N[c] == N[(c + d // q) % d] for c in range(d))
            if z: out.add(o)
        return frozenset(out)
    def zeros_fft(s, A):
        ind = np.zeros(s.M); ind[list(A)] = 1; F = np.fft.fft(ind)
        return frozenset(o for o in s.ords if abs(F[s.M // s.val(o)]) < 1e-8)
    def lp(s, Z, extra=None, obj=None):
        rows = [[1 if c == (s.a, s.b) else 0 for c in s.cls]] + [[s.C[(o, c)] for c in s.cls] for o in s.ords if o not in Z]
        rhs = [1] + [0] * (len(rows) - 1)
        if extra:
            for r, v in extra: rows.append(r); rhs.append(v)
        return solve_lp(rows, rhs, s.size if obj is None else obj)
    def Dw(s, Z):
        st, v, x, y = s.lp(Z); assert st == 'optimal'
        return Fr(s.M) / v, v, x
    def pattern(s, Z):
        a, b, p, q = s.a, s.b, s.p, s.q
        Ep = [l for l in range(1, a + 1) if (l, 0) in Z]; Eq = [m for m in range(1, b + 1) if (0, m) in Z]
        k = p ** len(Ep) * q ** len(Eq)
        t2 = all((l, m) in Z for l in Ep for m in Eq)
        orphan = any(l >= 1 and m >= 1 and l not in Ep and m not in Eq for (l, m) in Z)
        return Ep, Eq, k, t2, orphan
    def digit(s, S):
        """digit set of a set S of prime powers (given as orders (l, 0) / (0, m))"""
        T = [0]
        for (l, m) in S:
            if l: g = s.p ** (l - 1) * s.q ** s.b; n = s.p
            else: g = s.q ** (m - 1) * s.p ** s.a; n = s.q
            T = [(t + c * g) % s.M for t in T for c in range(n)]
        return sorted(T)
    def random_complement(s, B):
        """a random set A with A + B = Z_M (greedy with restarts)"""
        M = s.M
        for _ in range(50):
            cov = [False] * M; A = []
            ok = True
            while True:
                x = next((i for i in range(M) if not cov[i]), None)
                if x is None: break
                cand = [(x - bb) % M for bb in B if not any(cov[((x - bb) + c) % M] for c in B)]
                if not cand: ok = False; break
                t = random.choice(cand)
                for c in B: cov[(t + c) % M] = True
                A.append(t)
            if ok: return sorted(A)
        return None
    def random_tile(s):
        PP = [(l, 0) for l in range(1, s.a + 1)] + [(0, m) for m in range(1, s.b + 1)]
        while True:
            S = random.sample(PP, random.randint(0, len(PP)))
            B = s.digit(S); A = s.random_complement(B)
            if A is None: continue
            T = A if random.random() < 0.7 else B
            u = random.choice([t for t in range(1, s.M) if t % s.p and t % s.q]); sh = random.randrange(s.M)
            return sorted({(u * x + sh) % s.M for x in T})


def test_i(p, a, q, b, n):
    G = Grp(p, a, q, b); M = G.M; bad = 0; nt = nw = 0; fftbad = 0
    for t in range(n):
        if t % 2 == 0: A = G.random_tile(); tile = True
        else: A = sorted(random.sample(range(M), random.randint(1, min(M - 1, 14)))); tile = False
        Z = G.zeros(A)
        if Z != G.zeros_fft(A): fftbad += 1
        D, v, x = G.Dw(Z)
        g = [x[G.cls.index(G.clsof[z])] for z in range(M)]
        conv = [sum(g[(z - y) % M] for y in A) for z in range(M)]
        const = Fr(len(A)) * v / M
        if any(c != const for c in conv) or const < 1 or D > len(A): bad += 1
        if tile:
            nt += 1
            if D != len(A): bad += 1
        elif D == len(A):
            nw += 1; Ep, Eq, k, t2, orphan = G.pattern(Z)
            if not (k == len(A) and t2): bad += 1; print("    *** WEAK TILE WITHOUT (T1), (T2):", A)
    print(f"(i)   Z_{M} = Z_({p}^{a} {q}^{b}): {n} sets ({nt} tiles); 1_A * g constant = |A| sigma/M, D^w <= |A|, = |A| for tiles: failures {bad}; cuboid zero test != FFT zero test: {fftbad}; random sets that are weak tiles: {nw} (all with (T1), (T2) unless reported)")


def test_ii(p, a, q, b, n, swap=False):
    """Lemma C with the prime p (pieces modulo p).  swap: use the roles of the primes exchanged (pieces modulo q)."""
    G = Grp(p, a, q, b); M = G.M
    r = q if swap else p                                              # the prime of the pieces
    Gs = Grp(p, a, q, b - 1) if swap else Grp(p, a - 1, q, b)         # Z_{M/r}
    PPs = [(l, 0) for l in range(1, Gs.a + 1)] + [(0, m) for m in range(1, Gs.b + 1)]
    bad = 0; done = 0; skipped = 0
    while done < n:
        S = random.sample(PPs, random.randint(0, len(PPs))); B = Gs.digit(S)
        pieces = []
        for c in range(r):
            T = Gs.random_complement(B)
            if T is None: break
            u = random.choice([t for t in range(1, Gs.M) if t % p and t % q]); sh = random.randrange(Gs.M)
            pieces.append(sorted({(u * x + sh) % Gs.M for x in T}))
        if len(pieces) < r: continue
        # hypotheses of Lemma C on the pieces
        Zs = [Gs.zeros(T) for T in pieces]; pats = [Gs.pattern(Zc) for Zc in Zs]
        Ss = [frozenset(o for o in Zc if o[0] == 0 or o[1] == 0) for Zc in Zs]
        if not all(len(T) == pt[2] and pt[3] and not pt[4] for T, pt in zip(pieces, pats)) or len(set(Ss)) != 1: skipped += 1; continue
        A = sorted(c + r * y for c in range(r) for y in pieces[c])
        Z = G.zeros(A); Ep, Eq, k, t2, orphan = G.pattern(Z)
        SA = frozenset(o for o in Z if o[0] == 0 or o[1] == 0)
        if swap: want = {(0, 1)} | {(0, m + 1) for (l, m) in Ss[0] if l == 0} | {(l, 0) for (l, m) in Ss[0] if m == 0}
        else: want = {(1, 0)} | {(l + 1, 0) for (l, m) in Ss[0] if m == 0} | {(0, m) for (l, m) in Ss[0] if l == 0}
        done += 1
        if not (len(A) == k and t2 and not orphan and SA == frozenset(want)): bad += 1; print("    LEMMA C FAILS", A)
    print(f"(ii)  Z_{M} = Z_({p}^{a} {q}^{b}), pieces modulo {r}: {n} sets built from pieces with (T1), (T2), no orphan, same S' ({skipped} draws skipped: hypotheses not met); Lemma C fails: {bad}")


def test_iii(p, a, q, b, n):
    G = Grp(p, a, q, b); M = G.M; Gs = Grp(p, a - 1, q, b); Ms = Gs.M; P = [t * Ms for t in range(p)]
    bad = 0; nweak = 0
    for t in range(n):                                               # E.4
        if t % 2 == 0: As = Gs.random_tile()
        else: As = sorted(random.sample(range(Ms), random.randint(1, 10)))
        A = sorted((x + g) % M for x in As for g in P)
        Z = G.zeros(A); Zs = Gs.zeros(As)
        if Z != frozenset(Zs | {(a, m) for m in range(b + 1)}): bad += 1; print("    E.4 zero sets differ", As)
        w = G.Dw(Z)[0] == len(A); ws = Gs.Dw(Zs)[0] == len(As); nweak += w
        if w != ws: bad += 1; print("    E.4: weak tile status differs", As, w, ws)
    print(f"(iii) Z_{M} = Z_({p}^{a} {q}^{b}), P of order {p}: E.4 on {n} unions of cosets of P ({nweak} weak tiles): failures {bad}")
    bad = 0; nx1 = 0; tried = 0
    cP = (a - 1, b); unit = [1 if c == cP else 0 for c in G.cls]
    while tried < n:                                                 # E.3
        A = G.random_tile(); Z = G.zeros(A); tried += 1
        D, v, x = G.Dw(Z)
        st, val, xx, _ = G.lp(Z, extra=[(G.size, v)], obj=[-u for u in unit])
        xmax = -val
        if xmax > 1: bad += 1; print("    E.1 fails: x > 1 on the optimal face", A)
        if xmax != 1: continue
        nx1 += 1
        img = sorted({x_ % Ms for x_ in A}); Zs = Gs.zeros(img)
        okinj = len(img) == len(A)
        okweak = Gs.Dw(Zs)[0] == len(img)
        okz = frozenset(o for o in Z if o[0] < a) == Zs
        Ep, Eq, k, t2, orphan = Gs.pattern(Zs)
        oktop = (a, 0) not in Z if (k == len(img) and t2) else True
        if not (okinj and okweak and okz and oktop): bad += 1; print("    E.3 FAILS", A, okinj, okweak, okz, oktop)
    print(f"      E.3 on {tried} random tiles, {nx1} with an optimal step complement equal to 1 on P: failures {bad}")


def test_iv():
    for M, p, q in [(12, 2, 3), (12, 3, 2), (18, 3, 2), (18, 2, 3), (20, 2, 5), (20, 5, 2), (24, 2, 3), (24, 3, 2)]:
        # here p, q are just the two primes; P, Q the subgroups of order p, q; all subsets of Z_M
        if M == 24 and p == 3: continue
        w = cmath.exp(2j * cmath.pi / M); pw = np.array([w ** x for x in range(M)])
        G = M // (p * q); nz = bad = 0
        allx = np.arange(1 << M, dtype=np.int64) if M <= 20 else None
        chunk = 1 << 20
        for start in range(0, 1 << M, chunk):
            xs = np.arange(start, min(start + chunk, 1 << M), dtype=np.int64)
            bits = ((xs[:, None] >> np.arange(M)) & 1).astype(np.int8)
            val = bits @ pw
            idx = np.nonzero(np.abs(val) < 1e-9)[0]
            for t in idx:
                A = bits[t]; nz += 1
                for c in range(G):
                    arr = np.array([[A[(c + u * (M // p) + v * (M // q)) % M] for v in range(q)] for u in range(p)])   # rows: u (P-direction), columns: v
                    rows_const = all(len(set(arr[u])) == 1 for u in range(p))      # each row constant  -> union of cosets of Q
                    cols_const = all(len(set(arr[:, v])) == 1 for v in range(q))   # each column constant -> union of cosets of P
                    if not (rows_const or cols_const): bad += 1
        print(f"(iv)  Z_{M} (p = {p}, q = {q}): all {1 << M:,} subsets; with Phi_{M} | A: {nz:,}; some coset of K not a union of cosets of P or of Q: {bad}")
    # integer form on Z_12 = Z_4 x Z_3, d = 12: arrays with entries 0..2
    M, p, q = 12, 2, 3; w = cmath.exp(2j * cmath.pi / M); pw = np.array([w ** x for x in range(M)]); nz = bad = 0
    for N in itertools.product(range(3), repeat=M):
        if abs(np.dot(N, pw)) > 1e-9: continue
        nz += 1
        for c in range(M // (p * q)):
            arr = np.array([[N[(c + u * (M // p) + v * (M // q)) % M] for v in range(q)] for u in range(p)])
            u0 = int(np.argmin(arr[:, 0])); al = arr[:, 0] - arr[u0, 0]; be = arr[u0, :]
            if not ((al >= 0).all() and (be >= 0).all() and (arr == al[:, None] + be[None, :]).all()): bad += 1
    print(f"      Z_12, all {3**12:,} arrays with entries 0, 1, 2 and Phi_12 | N: {nz:,}; not of the form alpha_u + beta_v with alpha, beta >= 0: {bad}")


def test_v():
    w = cmath.exp(2j * cmath.pi / 12); res = Counter()
    for n in (2, 4, 6):
        for X in itertools.combinations(range(36), n):
            if abs(sum(w ** x for x in X)) > 1e-9: continue
            e = sum(1 for x in X if x % 2 == 0); res[(n, 'Phi_12 | X')] += 1
            if e == 1 or n - e == 1: res[(n, 'a class modulo 2 with exactly one element')] += 1
    print(f"(v)   subsets of Z_36 with Phi_12 | X: sizes 2, 4, 6: {res[(2, 'Phi_12 | X')]:,}, {res[(4, 'Phi_12 | X')]:,}, {res[(6, 'Phi_12 | X')]:,}; with a class modulo 2 holding exactly one element: "
          f"{res[(2, 'a class modulo 2 with exactly one element')]}, {res[(4, 'a class modulo 2 with exactly one element')]}, {res[(6, 'a class modulo 2 with exactly one element')]}")


if __name__ == '__main__':
    which = sys.argv[2].split(',') if len(sys.argv) > 2 else ['i', 'ii', 'iii', 'iv', 'v']
    if 'i' in which:
        for (p, a, q, b) in [(2, 3, 3, 2), (3, 3, 2, 2), (2, 3, 5, 2), (2, 2, 3, 2)]: test_i(p, a, q, b, 300)
    if 'ii' in which:
        for (p, a, q, b) in [(2, 3, 3, 2), (3, 3, 2, 2), (2, 3, 5, 2)]:
            test_ii(p, a, q, b, 300); test_ii(p, a, q, b, 300, swap=True)
    if 'iii' in which:
        for (p, a, q, b) in [(2, 3, 3, 2), (3, 3, 2, 2), (3, 2, 2, 3), (2, 2, 3, 3), (2, 3, 5, 2)]: test_iii(p, a, q, b, 300)
    if 'v' in which: test_v()
    if 'iv' in which: test_iv()
