"""Independent checks of (I3) (F1)-(F3), (I5), (I6) in pure Python (exact integer arithmetic).

 (a) Linear algebra: for M = p0 p1 p2, the kernel of  a |-> a(X) mod Phi_M(X)  on Q^{Z_M} has dimension
     M - phi(M).  V1 + V2 + V3 (functions not depending on one coordinate) is spanned by the indicators of the
     cosets of the three subgroups of prime order.  We check (i) every such indicator reduces to 0 mod Phi_M
     (exact division over Z), (ii) the rank of the family of indicators is M - phi(M) (rank mod a large prime is a
     lower bound for the rank over Q; the upper bound is (i)).  Hence kernel = V1 + V2 + V3: that is (F3).
     Same for (F2) (Phi_{p_x p_y}: kernel = functions whose N_xy is additive) and (F1).
 (b) Random sets: Phi_d | A decided by exact polynomial division, against the coordinate criteria
     (F1) N_x constant, (F2) N_xy additive, (F3) all A_c - A_c' additive.  Random sets almost never have
     Phi_M | A, so the sample is built from unions of cosets of the three prime-order subgroups, with and
     without a few random elements added or removed.
 (c) (I5): X -> X° kills exactly the additive matrices (rank check), (I6) exhaustive for small sizes.
"""
import random, itertools, sys
from math import gcd

def polydivmod(num, den):
    num = num[:]; dd = len(den) - 1
    assert den[-1] == 1
    q = [0]*(max(len(num) - dd, 1))
    for k in range(len(num) - 1, dd - 1, -1):
        c = num[k]
        if c:
            q[k - dd] = c
            for j in range(dd + 1): num[k - dd + j] -= c*den[j]
    return q, num[:dd]

_cyc = {}
def cyclo(n):
    if n in _cyc: return _cyc[n]
    num = [-1] + [0]*(n - 1) + [1]
    for e in range(1, n):
        if n % e == 0:
            num, r = polydivmod(num, cyclo(e)); assert not any(r)
            while len(num) > 1 and num[-1] == 0: num.pop()
    _cyc[n] = num
    return num

def divides(d, a):   # a: list of length M of integers (coefficients of the mask polynomial)
    _, r = polydivmod(list(a), cyclo(d))
    return not any(r)

def rank_mod(rows, P=(1 << 61) - 1):
    rows = [[v % P for v in r] for r in rows]
    rk = 0; ncol = len(rows[0])
    for col in range(ncol):
        piv = next((i for i in range(rk, len(rows)) if rows[i][col]), None)
        if piv is None: continue
        rows[rk], rows[piv] = rows[piv], rows[rk]
        inv = pow(rows[rk][col], P - 2, P)
        rows[rk] = [v*inv % P for v in rows[rk]]
        for i in range(len(rows)):
            if i != rk and rows[i][col]:
                f = rows[i][col]
                rows[i] = [(a - f*b) % P for a, b in zip(rows[i], rows[rk])]
        rk += 1
        if rk == len(rows): break
    return rk

def phi(n): return sum(1 for k in range(1, n + 1) if gcd(k, n) == 1)

def part_a(p):
    M = p[0]*p[1]*p[2]
    coords = [(e % p[0], e % p[1], e % p[2]) for e in range(M)]
    # (F3)
    gens = []
    for w in range(3):
        o = [v for v in range(3) if v != w]
        for u in range(p[o[0]]):
            for v in range(p[o[1]]):
                g = [1 if (coords[e][o[0]] == u and coords[e][o[1]] == v) else 0 for e in range(M)]
                assert divides(M, g)
                gens.append(g)
    r3 = rank_mod(gens)
    ok3 = (r3 == M - phi(M))
    # (F2) for each pair: kernel of reduction mod Phi_{p_x p_y} has dim M - phi(p_x p_y); it should be
    # {a : N_xy additive} = (functions with N_xy = 0) + (pull-backs of additive matrices).
    ok2 = True
    for x, y in ((0, 1), (0, 2), (1, 2)):
        z = 3 - x - y; d = p[x]*p[y]
        gens = []
        # pull-backs of functions of i alone and of j alone (put on the fibre point with z-coordinate 0 is not a pull-back;
        # use instead: delta at (i,j,0) patterns):  basis of {a : N_xy additive}:
        #   e_(i,j,c) - e_(i,j,0) for c != 0 (N_xy = 0), and sum_j e_(i,j,0), sum_i e_(i,j,0) (N_xy = indicator of a row / column)
        idx = {coords[e]: e for e in range(M)}
        def key(i, j, c):
            t = [0, 0, 0]; t[x] = i; t[y] = j; t[z] = c
            return idx[tuple(t)]
        for i in range(p[x]):
            for j in range(p[y]):
                for c in range(1, p[z]):
                    g = [0]*M; g[key(i, j, c)] = 1; g[key(i, j, 0)] = -1; gens.append(g)
        for i in range(p[x]):
            g = [0]*M
            for j in range(p[y]): g[key(i, j, 0)] = 1
            gens.append(g)
        for j in range(p[y]):
            g = [0]*M
            for i in range(p[x]): g[key(i, j, 0)] = 1
            gens.append(g)
        assert all(divides(d, g) for g in gens)
        ok2 &= (rank_mod(gens) == M - phi(d))
    # (F1)
    ok1 = True
    for x in range(3):
        gens = []
        byx = {}
        for e in range(M): byx.setdefault(coords[e][x], []).append(e)
        for i in range(p[x]):
            for e in byx[i][1:]:
                g = [0]*M; g[e] = 1; g[byx[i][0]] = -1; gens.append(g)       # N_x = 0
        g = [0]*M
        for i in range(p[x]): g[byx[i][0]] = 1                                # N_x = constant 1
        gens.append(g)
        assert all(divides(p[x], g) for g in gens)
        ok1 &= (rank_mod(gens) == M - phi(p[x]))
    return ok1, ok2, ok3

def criteria(p, a):
    """pattern by the coordinate criteria of the note, as literally stated."""
    M = p[0]*p[1]*p[2]
    coords = [(e % p[0], e % p[1], e % p[2]) for e in range(M)]
    out = {}
    for x in range(3):
        N = [0]*p[x]
        for e in range(M): N[coords[e][x]] += a[e]
        out[p[x]] = all(v == N[0] for v in N)
    def additive(Mx):
        return all(Mx[i][j] - Mx[i][0] - Mx[0][j] + Mx[0][0] == 0 for i in range(len(Mx)) for j in range(len(Mx[0])))
    for x, y in ((0, 1), (0, 2), (1, 2)):
        N = [[0]*p[y] for _ in range(p[x])]
        for e in range(M): N[coords[e][x]][coords[e][y]] += a[e]
        out[p[x]*p[y]] = additive(N)
    # (F3) in its slice form, slicing along EACH coordinate z (they must all agree)
    res = []
    for z in range(3):
        x, y = [w for w in range(3) if w != z]
        sl = [[[0]*p[y] for _ in range(p[x])] for _ in range(p[z])]
        for e in range(M): sl[coords[e][z]][coords[e][x]][coords[e][y]] = a[e]
        ok = all(additive([[sl[c][i][j] - sl[c2][i][j] for j in range(p[y])] for i in range(p[x])])
                 for c in range(p[z]) for c2 in range(p[z]))
        res.append(ok)
    assert res[0] == res[1] == res[2], "slice criterion depends on the slicing coordinate?!"
    out[M] = res[0]
    return out

def part_b(p, trials, rng):
    M = p[0]*p[1]*p[2]
    divs = [p[0], p[1], p[2], p[0]*p[1], p[0]*p[2], p[1]*p[2], M]
    stats = {d: [0, 0] for d in divs}   # [#sets with Phi_d | A, #disagreements]
    for tr in range(trials):
        mode = tr % 4
        a = [0]*M
        if mode == 0:
            for e in range(M): a[e] = rng.randint(0, 1)
        else:
            # union of random cosets of the prime-order subgroups (and of the subgroups of order p_x p_y)
            for _ in range(rng.randint(1, 5)):
                w = rng.randrange(6)
                step = [M//p[0], M//p[1], M//p[2], p[0], p[1], p[2]][w]
                s = rng.randrange(M)
                for k in range(M//step): a[(s + k*step) % M] = 1
            if mode == 2:
                for _ in range(rng.randint(1, 2)): a[rng.randrange(M)] ^= 1
            if mode == 3 and rng.random() < 0.5:
                a = [1 - v for v in a]
        if not any(a): continue
        cr = criteria(p, a)
        for d in divs:
            ex = divides(d, a)
            stats[d][0] += ex
            if ex != cr[d]: stats[d][1] += 1
    return stats

def part_c():
    import fractions
    Fr = fractions.Fraction
    out = []
    for (m, n) in [(2, 3), (2, 5), (3, 5), (2, 7), (3, 7), (5, 7)]:
        # matrix of the double-centring map on Q^{m x n}; its kernel should be the additive matrices (dim m+n-1)
        rows = []
        for i0 in range(m):
            for j0 in range(n):
                # image of the elementary matrix E_{i0 j0}, scaled by m n to stay in integers
                img = []
                for i in range(m):
                    for j in range(n):
                        v = m*n*(i == i0 and j == j0) - m*(i == i0) - n*(j == j0) + 1
                        img.append(v)
                rows.append(img)
        rk = rank_mod(rows)
        # additive matrices are killed:
        ok = True
        for i0 in range(m):
            img = [sum(rows[i0*n + j][k] for j in range(n)) for k in range(m*n)]; ok &= not any(img)
        for j0 in range(n):
            img = [sum(rows[i*n + j0][k] for i in range(m)) for k in range(m*n)]; ok &= not any(img)
        out.append(((m, n), rk == m*n - (m + n - 1), ok))
    # (I6) exhaustive
    i6 = []
    for (m, n) in [(2, 2), (2, 3), (3, 2), (2, 5), (3, 3), (3, 5), (5, 3), (2, 7), (3, 7), (4, 5)]:
        cnt = bad = 0
        for bits in range(1 << (m*n)):
            X = [[bits >> (i*n + j) & 1 for j in range(n)] for i in range(m)]
            if all(X[i][j] - X[i][0] - X[0][j] + X[0][0] == 0 for i in range(m) for j in range(n)):
                cnt += 1
                rowsok = all(X[i][j] == X[i][0] for i in range(m) for j in range(n))
                colsok = all(X[i][j] == X[0][j] for i in range(m) for j in range(n))
                if not (rowsok or colsok): bad += 1
        i6.append(((m, n), cnt, bad, cnt == (1 << m) + (1 << n) - 2))
    return out, i6

if __name__ == "__main__":
    rng = random.Random(20261120)
    for p in [(2, 3, 5), (2, 3, 7), (2, 5, 7), (3, 5, 7), (2, 3, 11), (3, 5, 11), (5, 7, 11)]:
        print("kernel/rank check (F1),(F2),(F3) for", p, "->", part_a(p))
    for p, trials in [((2, 3, 5), 20000), ((2, 3, 7), 20000), ((3, 5, 7), 6000), ((2, 5, 11), 4000), ((5, 7, 11), 1500)]:
        st = part_b(p, trials, rng)
        print("random sets", p, "trials", trials, {d: tuple(v) for d, v in st.items()}, " (per divisor: #sets with Phi_d | A, #disagreements)")
    c5, c6 = part_c()
    print("(I5) kernel of double centring = additive matrices:", c5)
    print("(I6) exhaustive (size, #additive 0/1 matrices, #not a union of full rows/columns, count == 2^m+2^n-2):", c6)
