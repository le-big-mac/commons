# rlib.py -- the referee's own routines, written from the definitions in small/small-multisets.md (sections 1 to 3)
# and in sign-four-result.md (sections 1, 2), not from general3/lib4.py.
#
# A multiset B on Z_n is a list of residues 0..n-1 (repetitions allowed).  A signing is a row of +1/-1.
# "bad at d" is decided by exact division of the signed mask by Phi_d (remainder of sum eps_k X^{b_k} modulo Phi_d,
# whole numbers).
import math
import numpy as np


def factor(n):
    f = {}
    p = 2
    while p * p <= n:
        while n % p == 0:
            f[p] = f.get(p, 0) + 1
            n //= p
        p += 1
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f


def vp(n, p):
    a = 0
    while n % p == 0:
        n //= p
        a += 1
    return a


def divisors(n):
    ds = [1]
    for p, a in factor(n).items():
        ds = [d * p ** j for d in ds for j in range(a + 1)]
    return sorted(ds)


def mu(d):
    """mu(d) = max over the primes p | d of v_p(d)*(p-1); mu(1) = 0.  (Definition, by factoring d.)"""
    return max((a * (p - 1) for p, a in factor(d).items()), default=0)


def nprime(m):
    """n'_m = product over odd primes p <= m of p^floor((m-1)/(p-1))."""
    r = 1
    for p in range(3, m + 1, 2):
        if all(p % q for q in range(3, int(p ** 0.5) + 1, 2)):
            r *= p ** ((m - 1) // (p - 1))
    return r


# ---- integer polynomials: lists of Python ints, index = degree ----

def pdivmod(a, b):
    """a = q*b + r, b monic, deg r < deg b."""
    a = list(a)
    db = len(b) - 1
    assert b[-1] == 1
    q = [0] * max(0, len(a) - db)
    for k in range(len(a) - db - 1, -1, -1):
        c = a[k + db]
        if c:
            q[k] = c
            for j, bj in enumerate(b):
                a[k + j] -= c * bj
    return q, a[:db]


_cyc = {}


def cyclo(d):
    """Phi_d = (X^d - 1) / product of Phi_e over e | d, e < d."""
    if d not in _cyc:
        num = [-1] + [0] * (d - 1) + [1]
        for e in divisors(d):
            if e < d:
                num, r = pdivmod(num, cyclo(e))
                assert not any(r)
        _cyc[d] = num
    return _cyc[d]


_tab = {}


def xtable(n, d):
    """T[x] = coefficients of X^x modulo Phi_d (length phi(d)), x = 0..n-1.  int64."""
    key = (n, d)
    if key not in _tab:
        phi = cyclo(d)
        k = len(phi) - 1
        T = np.zeros((n, k), dtype=np.int64)
        cur = [0] * k
        cur[0] = 1
        for x in range(n):
            T[x] = cur
            top = cur[-1]
            cur = [0] + cur[:-1]
            if top:
                for j in range(k):
                    cur[j] -= top * phi[j]
        _tab[key] = T
    return _tab[key]


_E = {}


def signs(m):
    """all 2^m sign vectors; row r has -1 at position j iff bit j of r is set."""
    if m not in _E:
        r = np.arange(1 << m, dtype=np.int64)[:, None]
        j = np.arange(m, dtype=np.int64)[None, :]
        _E[m] = (1 - 2 * ((r >> j) & 1)).astype(np.int64)
    return _E[m]


def bad_at(B, n, d, E=None):
    """boolean vector over all 2^m signings: Phi_d divides the signed mask (exact)."""
    if E is None:
        E = signs(len(B))
    T = xtable(n, d)
    R = E @ T[np.asarray(B, dtype=np.int64)]
    return ~R.any(axis=1)


def bad_all(B, n):
    E = signs(len(B))
    return {d: bad_at(B, n, d, E) for d in divisors(n)}


def good_vector(B, n):
    bad = np.zeros(1 << len(B), dtype=bool)
    for d, v in bad_all(B, n).items():
        bad |= v
    return ~bad


def divides_direct(B, eps, d):
    """Phi_d | sum eps_k X^{b_k}, by long division of the polynomial itself (no table)."""
    deg = max(B)
    a = [0] * (deg + 1)
    for b, e in zip(B, eps):
        a[b] += int(e)
    phi = cyclo(d)
    if len(a) < len(phi):
        return not any(a)
    q, r = pdivmod(a, phi)
    return not any(r)


# ---- the p-tree (note, section 1) ----

def groups(B, p, i):
    """level i of the p-tree: {class at depth i-1 (residue mod p^(i-1)) : set of occupied subclasses (mod p^i)}.
    Only groups that hold an element appear."""
    g = {}
    for x in B:
        g.setdefault(x % p ** (i - 1), set()).add(x % p ** i)
    return g


def has_full_group(B, p, i):
    return any(len(s) == p for s in groups(B, p, i).values())


def contractible(B, p, t):
    """note, section 2: every group at level t that holds an element of B has a subclass that holds none."""
    return all(len(s) < p for s in groups(B, p, t).values())


def crt(u, M1, w, M2):
    """the y in Z_{M1*M2} with y = u mod M1 and y = w mod M2 (M1, M2 coprime)."""
    if M2 == 1:
        return u % M1
    y = u + M1 * (((w - u) * pow(M1, -1, M2)) % M2)
    return y % (M1 * M2)


def contract(B, n, p, t):
    """delete the digit of index t-1 of x mod p^a from every element; the result is on Z_{n/p}."""
    a = vp(n, p)
    assert 1 <= t <= a
    pa = p ** a
    n2 = n // pa
    out = []
    for x in B:
        u = x % pa
        w = x % n2
        low = u % p ** (t - 1)          # digits of index 0..t-2
        high = u // p ** t              # digits of index t..a-1
        u2 = low + p ** (t - 1) * high
        out.append(crt(u2, pa // p, w, n2))
    return out, n // p


def contract_all(B, n, order="deep", rng=None):
    """contract as long as some level of some tree is contractible.
    order: "deep" (deepest contractible level of the smallest prime first), "shallow", "random"."""
    B = list(B)
    steps = []
    while True:
        cands = [(p, t) for p, a in sorted(factor(n).items()) for t in range(1, a + 1) if contractible(B, p, t)]
        if not cands:
            return B, n, steps
        if order == "deep":
            p0 = cands[0][0]
            p, t = max(c for c in cands if c[0] == p0)
        elif order == "shallow":
            p, t = cands[0]
        else:
            p, t = rng.choice(cands)
        B, n = contract(B, n, p, t)
        steps.append((p, t))


def all_levels_full(B, n):
    return all(has_full_group(B, p, i) for p, a in factor(n).items() for i in range(1, a + 1))


def lemmaL_e(B, p, i):
    """e = sum over occupied groups D at level i of min(k_D, p-1)."""
    return sum(min(len(s), p - 1) for s in groups(B, p, i).values())


def flat_everywhere(B, n, p, i, d2, E=None):
    """right-hand side of Lemma 1(b): for every signing, whether in every group at level i of the p-tree the p
    subclasses have slices that are congruent modulo Phi_{d2}.  Slices are taken in Z[X]/(X^{n''}-1) (exponent
    x mod n'') and reduced modulo Phi_{d2}."""
    if E is None:
        E = signs(len(B))
    a = vp(n, p)
    pa = p ** a
    n2 = n // pa
    assert n2 % d2 == 0 and 1 <= i <= a
    T = xtable(n2, d2)
    idx = {}
    for k, x in enumerate(B):
        u = x % pa
        idx.setdefault(u % p ** (i - 1), {}).setdefault(u % p ** i, []).append(k)
    ok = np.ones(E.shape[0], dtype=bool)
    zero = np.zeros((E.shape[0], T.shape[1]), dtype=np.int64)
    for c, subs in idx.items():
        sl = []
        for e in range(p):
            ks = subs.get(c + p ** (i - 1) * e)
            if ks:
                sl.append(E[:, ks] @ T[[B[k] % n2 for k in ks]])
            else:
                sl.append(zero)
        for s in sl[1:]:
            ok &= ~(s - sl[0]).any(axis=1)
    return ok


# ---- counting good signings from multiplicities (a second method) ----

def good_count_grid(B, n):
    """number of good signings of B, counted through the coefficient vectors: an element of multiplicity c gets
    the coefficient a in {-c, -c+2, .., c} with weight C(c, (c+a)/2).  Exact (Python ints for the total)."""
    mult = {}
    for x in B:
        mult[x] = mult.get(x, 0) + 1
    supp = sorted(mult)
    A = np.zeros((1, 0), dtype=np.int64)
    W = np.ones(1, dtype=np.int64)
    for x in supp:
        c = mult[x]
        vals = np.arange(-c, c + 1, 2, dtype=np.int64)
        wts = np.array([math.comb(c, j) for j in range(c + 1)], dtype=np.int64)
        A = np.concatenate([np.repeat(A, len(vals), axis=0), np.tile(vals, A.shape[0])[:, None]], axis=1)
        W = np.repeat(W, len(vals)) * np.tile(wts, W.shape[0])
    bad = np.zeros(A.shape[0], dtype=bool)
    for d in divisors(n):
        T = xtable(n, d)
        bad |= ~(A @ T[supp]).any(axis=1)
    return int(W[~bad].sum()), int(W.sum())
