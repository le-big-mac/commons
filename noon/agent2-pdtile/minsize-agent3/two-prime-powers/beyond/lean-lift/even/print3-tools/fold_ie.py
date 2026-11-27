# usage: python3 -I fold_ie.py B144926.txt N [N ...]
# Second way to get F(n) (the number of sign vectors of length n whose folding modulo the odd part n' is a singular
# circulant of order n'): inclusion-exclusion over sets T of divisors of n'.  N(T) = weighted number of folded vectors
# divisible by G_T = prod_{d in T} Phi_d, counted by running over the lowest n' - deg(G_T) coefficients (the rest is forced,
# G_T being monic with constant term +-1), or by a closed form when T is {1}, {p} or {1,p} with p prime.
import sys, math, itertools
import numpy as np
LIMIT = 20_000_000

def polymul(a, b):
    r = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            r[i + j] += x * y
    return r

def polydiv(a, b):
    a = a[:]; q = [0] * (len(a) - len(b) + 1)
    for i in range(len(a) - len(b), -1, -1):
        q[i] = a[i + len(b) - 1] // b[-1]
        for j, bj in enumerate(b):
            a[i + j] -= q[i] * bj
    assert all(x == 0 for x in a)
    return q

def cyclo(d):
    p = [-1] + [0] * (d - 1) + [1]
    for e in range(1, d):
        if d % e == 0:
            p = polydiv(p, cyclo(e))
    return p

def is_prime(m):
    return m > 1 and all(m % t for t in range(2, m))

def N_of(T, n, m, q):
    T = tuple(sorted(T))
    if T == (1,):
        return math.comb(n, n // 2)
    if len(T) == 1 and is_prime(T[0]):
        p = T[0]; return sum(math.comb(n // p, k) ** p for k in range(n // p + 1))
    if len(T) == 2 and T[0] == 1 and is_prime(T[1]):
        p = T[1]; return math.comb(n // p, n // (2 * p)) ** p
    G = [1]
    for d in T:
        G = polymul(G, cyclo(d))
    D = len(G) - 1
    f = m - D
    assert abs(G[0]) == 1 and G[-1] == 1 and f >= 0
    base = q + 1
    total = base ** f
    if total > LIMIT:
        raise RuntimeError("too many: T=%s" % (T,))
    w = np.array([math.comb(q, t) for t in range(q + 1)], dtype=np.int64)
    count = 0
    chunk = 1_000_000
    for start in range(0, total, chunk):
        idx = np.arange(start, min(total, start + chunk), dtype=np.int64)
        x = idx.copy()
        digs = []
        for j in range(f):
            digs.append(x % base); x //= base
        wt = np.ones(len(idx), dtype=np.int64)
        g = []
        for i in range(f):
            ci = 2 * digs[i] - q
            wt *= w[digs[i]]
            acc = ci.copy()
            for j in range(1, min(i, D) + 1):
                acc -= G[j] * g[i - j]
            g.append(acc * G[0])            # G[0] = +-1, so dividing is multiplying
        ok = np.ones(len(idx), dtype=bool)
        for i in range(f, m):
            ci = np.zeros(len(idx), dtype=np.int64)
            for j in range(0, D + 1):
                if 0 <= i - j < f:
                    ci += G[j] * g[i - j]
            good = (np.abs(ci) <= q) & ((ci - q) % 2 == 0)
            ok &= good
            t = np.where(good, (ci + q) // 2, 0)
            wt *= w[t]
        count += int(wt[ok].sum())
    return count

a = {}
for line in open(sys.argv[1], encoding="ascii", errors="replace"):
    parts = line.split()
    if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
        a[int(parts[0])] = int(parts[1])
for n in [int(s) for s in sys.argv[2:]]:
    k = 0; m = n
    while m % 2 == 0: m //= 2; k += 1
    q = 2 ** k
    divs = [d for d in range(1, m + 1) if m % d == 0]
    F = 0
    for r in range(1, len(divs) + 1):
        for T in itertools.combinations(divs, r):
            F += (-1) ** (r + 1) * N_of(T, n, m, q)
    print("n=%d n'=%d  a(n) listed=%d  F(n) by inclusion-exclusion=%d  2F(n)=%d  a(n)<=2F(n): %s" % (n, m, a.get(n, -1), F, 2 * F, a.get(n, -1) <= 2 * F))
