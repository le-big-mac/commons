# Referee's helper (written from the statements; imports nothing of the author's).
# Exact integer arithmetic only: cyclotomic polynomials by exact division, the remainders X^i mod Phi_d,
# and Ramanujan sums (a second, independent criterion for "Phi_d divides S").

def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]

def v2(n):
    k = 0
    while n % 2 == 0:
        n //= 2
        k += 1
    return k

def polydiv_exact(a, b):
    """a / b for integer polynomials (lists, low degree first), b monic; the remainder must be 0."""
    a = a[:]
    q = [0] * (len(a) - len(b) + 1)
    for i in range(len(a) - len(b), -1, -1):
        c = a[i + len(b) - 1]
        q[i] = c
        if c:
            for j, bj in enumerate(b):
                a[i + j] -= c * bj
    assert not any(a), "division not exact"
    return q

_phi = {}
def cyclo(d):
    """Phi_d, low degree first: (X^d - 1) divided by the Phi_e, e | d, e < d."""
    if d not in _phi:
        p = [-1] + [0] * (d - 1) + [1]
        for e in divisors(d):
            if e < d:
                p = polydiv_exact(p, cyclo(e))
        _phi[d] = p
    return _phi[d]

def xpow_mod(d, n):
    """rows i = 0..n-1: the coefficients of X^i mod Phi_d (length deg Phi_d)."""
    f = cyclo(d)
    deg = len(f) - 1
    rows = []
    r = [1] + [0] * (deg - 1) if deg >= 1 else []
    for i in range(n):
        rows.append(r[:])
        # multiply by X and reduce by the monic f
        top = r[-1]
        r = [0] + r[:-1]
        if top:
            for j in range(deg):
                r[j] -= top * f[j]
    return rows

def mobius(n):
    m, p = 1, 2
    while p * p <= n:
        if n % p == 0:
            n //= p
            if n % p == 0:
                return 0
            m = -m
        p += 1
    if n > 1:
        m = -m
    return m

def ramanujan(d, i):
    """c_d(i) = sum over the primitive d-th roots z of z^i = sum_{g | gcd(i, d)} mu(d/g) g."""
    from math import gcd
    g0 = gcd(i % d, d)
    return sum(mobius(d // g) * g for g in divisors(g0))

def phi_divides_ramanujan(coeffs, d):
    """coeffs: integer vector of length N with d | N (a polynomial modulo X^N - 1).
    Phi_d divides it iff its component in the factor Q(zeta_d) of Q[X]/(X^d - 1) is 0,
    i.e. iff the fold c modulo d has sum_i c_i * c_d(i - j) = 0 for every j."""
    c = [0] * d
    for i, a in enumerate(coeffs):
        c[i % d] += a
    ram = [ramanujan(d, t) for t in range(d)]
    for j in range(d):
        if sum(c[i] * ram[(i - j) % d] for i in range(d)) != 0:
            return False
    return True

if __name__ == "__main__":
    # self-test: the two criteria agree on random integer vectors and on multiples of Phi_d
    import random
    random.seed(5)
    n_agree = 0
    for N in (6, 8, 12, 20, 24, 30, 36, 60):
        for d in divisors(N):
            rows = xpow_mod(d, N)
            f = cyclo(d)
            for trial in range(60):
                if trial % 3 == 0:   # a multiple of Phi_d, folded modulo X^N - 1
                    g = [random.randint(-2, 2) for _ in range(N)]
                    v = [0] * N
                    for i, gi in enumerate(g):
                        for j, fj in enumerate(f):
                            v[(i + j) % N] += gi * fj
                else:
                    v = [random.choice((-1, 0, 0, 1)) for _ in range(N)]
                rem = [sum(v[i] * rows[i][t] for i in range(N)) for t in range(len(f) - 1)]
                a = not any(rem)
                b = phi_divides_ramanujan(v, d)
                assert a == b, (N, d, v)
                if trial % 3 == 0:
                    assert a
                n_agree += 1
    print("cyc self-test: remainder criterion == Ramanujan criterion on", n_agree, "vectors; ok")
