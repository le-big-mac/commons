"""Referee's own tools (nothing imported from the author's scripts).

exact_pattern_division(p, q, n, w): the pattern (E, F) of the multiset with weights w[0..M-1] on Z_M, M = p^n q,
    by exact integer long division of A(X) = sum w[x] X^x by Phi_d(X) (Python integers).
tree_pattern(p, q, n, w): the pattern by the three translations of section 1 of the note
    (equal totals / equal shapes among the children of every class; balanced root).
cyclo(d): Phi_d by the product formula over the divisors of d with the Moebius function, exact division.
remainder_matrix(d, M): column x = coefficients of X^x mod Phi_d (exact long division of each monomial).
"""
import itertools


def poly_divmod(num, den):
    """exact division of integer polynomials (lists, lowest degree first); den monic. returns (quotient, remainder)"""
    num = list(num)
    dd = len(den) - 1
    assert den[-1] == 1
    if len(num) - 1 < dd:
        return [0], num
    quo = [0] * (len(num) - dd)
    for k in range(len(num) - 1, dd - 1, -1):
        c = num[k]
        if c:
            quo[k - dd] = c
            for t in range(dd + 1):
                num[k - dd + t] -= c * den[t]
    return quo, num[:dd] if dd > 0 else [0]


def poly_mul(a, b):
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                out[i + j] += x * y
    return out


def mobius(m):
    res = 1
    f = 2
    while f * f <= m:
        if m % f == 0:
            m //= f
            if m % f == 0:
                return 0
            res = -res
        f += 1
    if m > 1:
        res = -res
    return res


_cy = {}


def cyclo(d):
    """Phi_d = prod_{e | d} (X^e - 1)^{mu(d/e)}"""
    if d in _cy:
        return _cy[d]
    num, den = [1], [1]
    for e in range(1, d + 1):
        if d % e == 0:
            mu = mobius(d // e)
            f = [-1] + [0] * (e - 1) + [1]
            if mu == 1:
                num = poly_mul(num, f)
            elif mu == -1:
                den = poly_mul(den, f)
    quo, rem = poly_divmod(num, den)
    assert not any(rem)
    while len(quo) > 1 and quo[-1] == 0:
        quo.pop()
    _cy[d] = quo
    return quo


def divides(d, w):
    quo, rem = poly_divmod(list(w), cyclo(d))
    return not any(rem)


def exact_pattern_division(p, q, n, w):
    E = tuple(a for a in range(1, n + 1) if divides(p ** a, w))
    F = tuple(a for a in range(0, n + 1) if divides(p ** a * q, w))
    return E, F


def class_vectors(p, q, n, w, d):
    """dict: class c mod p^d -> list of q counts by residue mod q"""
    pd = p ** d
    g = {c: [0] * q for c in range(pd)}
    for x, wt in enumerate(w):
        if wt:
            g[x % pd][x % q] += wt
    return g


def tree_pattern(p, q, n, w):
    """section 1 of the note, literally"""
    E, F = [], []
    g0 = class_vectors(p, q, n, w, 0)[0]
    if len(set(g0)) == 1:
        F.append(0)
    for a in range(1, n + 1):
        par = p ** (a - 1)
        g = class_vectors(p, q, n, w, a)
        eq_tot = True
        eq_shape = True
        for c in range(par):
            kids = [g[c + i * par] for i in range(p)]
            tots = [sum(v) for v in kids]
            if len(set(tots)) != 1:
                eq_tot = False
            for v in kids[1:]:
                diff = [v[j] - kids[0][j] for j in range(q)]
                if len(set(diff)) != 1:
                    eq_shape = False
        if eq_tot:
            E.append(a)
        if eq_shape:
            F.append(a)
    return tuple(E), tuple(F)


def remainder_matrix(d, M):
    """rows = coefficients (deg Phi_d of them), columns x = 0..M-1: X^x mod Phi_d, each by exact long division"""
    phi = cyclo(d)
    deg = len(phi) - 1
    cols = []
    for x in range(M):
        mono = [0] * x + [1]
        _, rem = poly_divmod(mono, phi)
        rem = list(rem) + [0] * (deg - len(rem))
        cols.append(rem[:deg])
    return [[cols[x][r] for x in range(M)] for r in range(deg)]


def parse_witness(s, M):
    w = [0] * M
    for tok in s.split():
        if '^' in tok:
            a, b = tok.split('^')
            w[int(a)] += int(b)
        else:
            w[int(tok)] += 1
    return w


def all_patterns(n):
    lv = list(range(1, n + 1))
    for ke in range(n + 1):
        for E in itertools.combinations(lv, ke):
            for kf in range(n + 2):
                for F in itertools.combinations(range(0, n + 1), kf):
                    yield E, F


# ---- the note's formulas, written from the note's words (sections 2 and 3) ----
def thm_value(p, q, E, F):
    """section 2: 0 not in F"""
    assert 0 not in F
    e = len(E)
    k = len([a for a in F if a >= 1 and a not in E])
    return p ** e if k == 0 else p ** e * (p ** k + q)


def rule_value(p, q, n, E, F):
    """section 3: 0 in F.  returns (value, x or None)"""
    assert 0 in F
    e = len(E)
    if set(F) == set(range(0, n + 1)):
        return q * p ** e, None
    a0 = min(a for a in range(1, n + 1) if a not in F)
    deeper = sorted(a for a in F if a > a0 and a not in E)     # levels of F\E deeper than a0
    k1 = len(deeper)
    if k1 == 0:
        x = 0                                                   # clause (1)
    elif any(a in E for a in range(1, a0)):
        x = 0                                                   # clause (2): a level above (shallower than) a0 in E
    elif a0 in E and p >= 3:
        x = 0                                                   # clause (3)
    elif a0 in E and p == 2 and any(a in E and a not in F for a in range(a0 + 1, deeper[0])):
        x = 0                                                   # clause (4)
    else:
        x = 1
    return q * p ** e * (p ** k1 + x), x
