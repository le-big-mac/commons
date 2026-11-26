"""Referee's own model of Section 2 of minsize.tex, written from the paper's definitions.

A multiset on Z_M, M = p^n q, is a numpy integer array A of shape (p^n, q):
A[u, w] = multiplicity of the element (u, w), u in Z_{p^n}, w in Z_q (the layer).
u is written in base p, u = sum_{a=1..n} u_a p^(a-1); u_a is the digit of level a.
A class of depth d is given by c in [0, p^d): all (u, w) with u = c mod p^d.
Its children are the classes of depth d+1 with index c + j p^d, j = 0..p-1.
"""
import itertools
import numpy as np


# ---------- classes, vectors, patterns (Section 2) ----------

def class_vectors(A, p, n, d):
    """g(N) for all classes N of depth d: array of shape (p^d, q)."""
    q = A.shape[1]
    return A.reshape(p ** (n - d), p ** d, q).sum(axis=0)


def children(c, p, d):
    return [c + j * p ** d for j in range(p)]


def is_constant(v):
    return all(x == v[0] for x in v)


def equal_shapes(vs):
    return all(is_constant(v - vs[0]) for v in vs)


def equal_totals(vs):
    return all(int(v.sum()) == int(vs[0].sum()) for v in vs)


def class_pattern(A, p, n, d, c):
    """(E(N), F(N)) for the class N of depth d with index c; own levels l in [1, n-d]."""
    E, F = set(), set()
    for l in range(1, n - d + 1):
        dd = d + l - 1                      # depth of the classes whose children are compared
        gch = class_vectors(A, p, n, dd + 1)
        okE = okF = True
        for cc in range(c, p ** dd, p ** d):  # classes of depth dd contained in N
            vs = [gch[k] for k in children(cc, p, dd)]
            if not equal_totals(vs):
                okE = False
            if not equal_shapes(vs):
                okF = False
        if okE:
            E.add(l)
        if okF:
            F.add(l)
    return frozenset(E), frozenset(F)


def root_pattern(A, p, n):
    q = A.shape[1]
    E, F = class_pattern(A, p, n, 0, 0)
    bal = is_constant(class_vectors(A, p, n, 0)[0])
    return E, F, bal


# ---------- the group Z_M and the mask polynomial (Section 1) ----------

def mask_coeffs(A, p, n):
    """Coefficients a[x], 0 <= x < M, of A(X) = sum_x A(x) X^x, with x <-> (x mod p^n, x mod q)."""
    q = A.shape[1]
    M = p ** n * q
    return [int(A[x % p ** n, x % q]) for x in range(M)]


def poly_divmod_monic(a, b):
    """Exact long division of integer polynomials (lists, low degree first), b monic."""
    a = list(a)
    db = len(b) - 1
    assert b[-1] == 1
    qt = [0] * max(0, len(a) - db)
    for i in range(len(a) - 1, db - 1, -1):
        c = a[i]
        if c:
            qt[i - db] = c
            for k in range(db + 1):
                a[i - db + k] -= c * b[k]
    return qt, a[:db]


_cyc = {}


def cyclotomic(d):
    """Phi_d as an integer list, from X^d - 1 = prod_{c | d} Phi_c."""
    if d in _cyc:
        return _cyc[d]
    num = [-1] + [0] * (d - 1) + [1]
    for c in range(1, d):
        if d % c == 0:
            num, rem = poly_divmod_monic(num, cyclotomic(c))
            assert not any(rem)
    _cyc[d] = num
    return num


def divides_cyclo(a, d):
    """Phi_d | a(X), by exact integer long division."""
    phi = np.array(cyclotomic(d), dtype=object)
    r = np.array(a, dtype=object)
    db = len(phi) - 1
    for i in range(len(r) - 1, db - 1, -1):
        c = r[i]
        if c:
            r[i - db:i + 1] -= c * phi
    return not any(r[:db])


def poly_pattern(A, p, n):
    """(E(A), F(A), balanced) by exact division of the mask polynomial."""
    q = A.shape[1]
    a = mask_coeffs(A, p, n)
    E = frozenset(l for l in range(1, n + 1) if divides_cyclo(a, p ** l))
    F = frozenset(l for l in range(1, n + 1) if divides_cyclo(a, p ** l * q))
    return E, F, divides_cyclo(a, q)


# ---------- Theorem 1 as printed (referee's own reading) ----------

def theorem_value(p, q, n, E, F, balanced):
    E, F = set(E), set(F)
    e = len(E)
    if not balanced:                                    # part (a)
        if F <= E:
            return p ** e
        k = len(F - E)
        return p ** e * (p ** k + q)
    full = set(range(1, n + 1))
    if F == full:                                       # part (b)
        return q * p ** e
    a0 = min(full - F)                                  # part (c)
    G = {a for a in F - E if a > a0}
    kp = len(G)
    c1 = kp == 0
    c2 = any(a < a0 for a in E)
    c3 = (a0 in E) and p >= 3
    c4 = (a0 in E) and p == 2 and kp > 0 and any(a0 < a < min(G) for a in E - F)
    x = 0 if (c1 or c2 or c3 or c4) else 1
    return q * p ** e * (p ** kp + x)


def clauses(p, q, n, E, F):
    """Which clauses of (c) hold (for reporting); None if F = [1,n]."""
    E, F = set(E), set(F)
    full = set(range(1, n + 1))
    if F == full:
        return None
    a0 = min(full - F)
    G = {a for a in F - E if a > a0}
    kp = len(G)
    return (kp == 0, any(a < a0 for a in E), (a0 in E) and p >= 3,
            (a0 in E) and p == 2 and kp > 0 and any(a0 < a < min(G) for a in E - F))


def subsets(n):
    full = list(range(1, n + 1))
    for r in range(n + 1):
        for s in itertools.combinations(full, r):
            yield frozenset(s)


def all_patterns(n):
    for E in subsets(n):
        for F in subsets(n):
            for bal in (False, True):
                yield E, F, bal


# ---------- the three sets of integers (Section 3.1) ----------

def in_S(x, p, q, u):
    """x in S_u = {p^u t + q m : t >= 1, m >= 0}."""
    P = p ** u
    t = 1
    while P * t <= x:
        if (x - P * t) % q == 0:
            return True
        t += 1
    return False


def in_Sp(x, p, q, u):
    """x in S+_u = {p^u t + q m : t >= 1, m >= 1}."""
    P = p ** u
    t = 1
    while P * t + q <= x:
        if (x - P * t) % q == 0:
            return True
        t += 1
    return False


def in_Q(x, p, q, u):
    return x >= 1 and x % (q * p ** u) == 0
