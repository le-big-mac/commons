"""Reader's own LB, U3 and U for every pattern of Z_{p^2 q^2}, written from the words of the note (sections 1 and 2) and from
Theorem 1 of minsize.pdf as printed, not from lowerbound.py / algebra.py / algebra2.py.

LB(D)  = least multiple of p^a q^b that is >= r1, r2, c   (section 1)
U3(D)  = least cost by atoms, convolution, sum, reduce-and-lift on Z_M   (section 2, first three moves)
U(D)   = least cost with dilation and stacking as well, the set of sizes kept for every pattern of every proper quotient group
         up to CAP times the group's order (the note: CAP = 2)
usage: bounds_own.py [CAP]      prints comparisons with status.json; writes reader/own-bounds-CAP.json"""
import sys, json, math, itertools

# ---------- Theorem 1 of minsize.pdf, as printed -------------------------------------------------------------------------
def theorem1(p, q, n, E, F, balanced):
    """least size of a (nonempty) multiset on Z_{p^n q} with E(A) = E, F(A) = F (subsets of [1, n]) and Phi_q | A iff balanced"""
    E, F = set(E), set(F); e = len(E)
    assert E <= set(range(1, n + 1)) and F <= set(range(1, n + 1))
    if not balanced:                                                    # (a)
        if F <= E: return p ** e
        return p ** e * (p ** len(F - E) + q)
    if F == set(range(1, n + 1)):                                       # (b)
        return q * p ** e
    a0 = min(a for a in range(1, n + 1) if a not in F)                  # (c)
    G = {a for a in F - E if a > a0}; k1 = len(G)
    c1 = (k1 == 0)
    c2 = any(a in E for a in range(1, a0))
    c3 = (a0 in E and p >= 3)
    c4 = (k1 >= 1 and a0 in E and p == 2 and any(a0 < b < min(G) for b in E - F))
    x = 0 if (c1 or c2 or c3 or c4) else 1
    return q * p ** e * (p ** k1 + x)

PAIRS = [(u, v) for u in range(3) for v in range(3) if (u, v) != (0, 0)]

def LB(S, p, q):
    """S: a set of exponent pairs (u, v), meaning Phi_{p^u q^v} divides"""
    S = set(S)
    a = len(S & {(1, 0), (2, 0)}); b = len(S & {(0, 1), (0, 2)})
    # r1: cut down to the divisors of p^2 q; the prime with the power is p
    r1 = theorem1(p, q, 2, {u for u in (1, 2) if (u, 0) in S}, {u for u in (1, 2) if (u, 1) in S}, (0, 1) in S)
    # r2: cut down to the divisors of p q^2; the prime with the power is q
    r2 = theorem1(q, p, 2, {v for v in (1, 2) if (0, v) in S}, {v for v in (1, 2) if (1, v) in S}, (1, 0) in S)
    # c: corner sum of the largest up-set inside S
    up = {(u, v) for (u, v) in S if all((x, y) in S for x in range(u, 3) for y in range(v, 3))}
    low = [(u, v) for u in range(3) for v in range(3) if (u, v) not in up]
    corners = [(u, v) for (u, v) in low if not any((x, y) != (u, v) and x >= u and y >= v for (x, y) in low)]
    c = sum(p ** (2 - u) * q ** (2 - v) for u, v in corners)
    g = p ** a * q ** b
    m = max(r1, r2, c)
    return ((m + g - 1) // g) * g, (r1, r2, c, g)

# ---------- the calculus ---------------------------------------------------------------------------------------------------
def divisors(n): return [d for d in range(1, n + 1) if n % d == 0]

def atoms(N):
    """cosets of cZ_N1 for c | N1 | N, lifted to Z_N: pattern {d | N1, d > 1, d does not divide c}, N1/c elements"""
    for N1 in divisors(N):
        for c in divisors(N1):
            yield frozenset(d for d in divisors(N1) if d > 1 and c % d), N1 // c

def three_moves(M):
    """least cost on Z_M by atoms, convolution, sum, reduce-and-lift"""
    cost = {}
    def put(P, s):
        if s < cost.get(P, math.inf): cost[P] = s; return True
        return False
    for P, s in atoms(M): put(P, s)
    cut = [frozenset(d for d in divisors(N) if d > 1) for N in divisors(M)]
    again = True
    while again:
        again = False
        for P in list(cost):
            for lm in cut:
                again |= put(P & lm, cost[P])
        ps = list(cost)
        for i, P1 in enumerate(ps):
            for P2 in ps[i:]:
                again |= put(P1 | P2, cost[P1] * cost[P2])
                again |= put(P1 & P2, cost[P1] + cost[P2])
    return cost

def from_quotients(N, sizes, cap):
    """dilation and stacking into Z_N from the proper quotient groups Z_K, K = N / c, c > 1.
    sizes[K]: dict pattern -> bitmask of sizes.  Yields (pattern, size)."""
    for c in divisors(N):
        if c == 1: continue
        K = N // c
        def up(T): return frozenset(d for d in divisors(N) if c % d and (d // math.gcd(d, c)) in T)
        base = frozenset(d for d in divisors(c) if d > 1)
        allw = 0
        for T, bits in sizes[K].items():
            allw |= bits
            w = 1
            while (1 << w) <= bits:
                if bits >> w & 1: yield up(T), w                         # dilation: c B, same size
                w += 1
        w = 1
        while (1 << w) <= allw:
            if allw >> w & 1:
                fam = [T for T, bits in sizes[K].items() if bits >> w & 1]
                reach = set(fam); layer = set(fam)
                for _ in range(c - 1):                                   # intersections of at most c patterns
                    layer = {I & T for I in layer for T in fam} - reach
                    if not layer: break
                    reach |= layer
                for T in reach: yield base | up(T), c * w                # stacking: c classes, each with w elements
            w += 1

def size_sets(N, sizes, cap):
    """every (pattern, size <= cap * N) reached on Z_N: dict pattern -> bitmask of sizes"""
    lim = cap * N; full = (1 << (lim + 1)) - 1
    S = {}
    def put(P, bits):
        bits &= full
        old = S.get(P, 0)
        if bits | old != old: S[P] = old | bits; return True
        return False
    for P, s in atoms(N): put(P, 1 << s)
    for N1 in divisors(N):
        if N1 < N:
            for P, bits in sizes[N1].items(): put(P, bits)               # a multiset on Z_N1 lifted to Z_N
    for P, s in from_quotients(N, sizes, cap):
        if s <= lim: put(P, 1 << s)
    cut = [frozenset(d for d in divisors(N1) if d > 1) for N1 in divisors(N)]
    again = True
    while again:
        again = False
        for P in list(S):
            for lm in cut: again |= put(P & lm, S[P])
        ps = list(S)
        for i, P1 in enumerate(ps):
            b1 = S[P1]; l1 = [s for s in range(1, lim + 1) if b1 >> s & 1]
            for P2 in ps[i:]:
                b2 = S[P2]
                add = 0; mul = 0
                for s in l1: add |= b2 << s
                l2 = [s for s in range(1, lim // l1[0] + 1) if b2 >> s & 1]
                for s in l1:
                    for t in l2:
                        if s * t > lim: break
                        mul |= 1 << (s * t)
                again |= put(P1 & P2, add)
                again |= put(P1 | P2, mul)
    return S

def five_moves(M, cap=2):
    sizes = {}
    for N in divisors(M):
        if N < M: sizes[N] = size_sets(N, sizes, cap)
    cost = {}
    def put(P, s):
        if s < cost.get(P, math.inf): cost[P] = s; return True
        return False
    for P, s in atoms(M): put(P, s)
    for N1 in divisors(M):
        if N1 < M:
            for P, bits in sizes[N1].items(): put(P, (bits & -bits).bit_length() - 1)
    for P, s in from_quotients(M, sizes, cap): put(P, s)
    cut = [frozenset(d for d in divisors(N) if d > 1) for N in divisors(M)]
    again = True
    while again:
        again = False
        for P in list(cost):
            for lm in cut: again |= put(P & lm, cost[P])
        ps = list(cost)
        for i, P1 in enumerate(ps):
            for P2 in ps[i:]:
                again |= put(P1 | P2, cost[P1] * cost[P2])
                again |= put(P1 & P2, cost[P1] + cost[P2])
    return cost, sizes

def pairs_of(D, p, q):
    out = set()
    for d in D:
        u = v = 0
        while d % p == 0: d //= p; u += 1
        while d % q == 0: d //= q; v += 1
        assert d == 1
        out.add((u, v))
    return out

if __name__ == '__main__':
    cap = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    st = json.load(open('/home/agent3/pq2/rule/status.json'))
    out = {}
    for M, p, q in ((36, 2, 3), (100, 2, 5), (225, 3, 5)):
        u3 = three_moves(M); u5, sizes = five_moves(M, cap)
        divs = [d for d in divisors(M) if d > 1]
        assert len(u3) == 256 and len(u5) == 256
        dLB = dU3 = dU = 0; below = []
        for r in st[str(M)]['rows']:
            D = frozenset(r['D']); lb, parts = LB(pairs_of(D, p, q), p, q)
            if lb != r['LB']: dLB += 1; print('  LB differs', M, sorted(D), lb, r['LB'], parts)
            if u3[D] != r['U3']: dU3 += 1; print('  U3 differs', M, sorted(D), u3[D], r['U3'])
            if u5[D] != r['U']: dU += 1; print('  U differs', M, sorted(D), u5[D], r['U'])
            if u5[D] < u3[D]: below.append((r['S'], u3[D], u5[D]))
            out[f'{M}|{",".join(map(str, sorted(D)))}'] = dict(LB=lb, parts=parts, U3=u3[D], U=u5[D])
        print(f'Z_{M} (cap {cap}): my LB differs from status.json in {dLB} of 256; my U3 in {dU3}; my U in {dU}')
        print(f'   U < U3 for {len(below)}: {below}')
    json.dump(out, open(f'/home/agent3/pq2/rule/reader/own-bounds-{cap}.json', 'w'))
