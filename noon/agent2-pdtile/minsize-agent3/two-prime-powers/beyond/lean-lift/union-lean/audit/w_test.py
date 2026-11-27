# Audit of Corollary U (card_exists_badAt_le), by brute force, exact integer arithmetic, every signing.
# Literally as Lean has it: exponents e_k any natural numbers; P = sum of sg(eps_k) X^(e_k) in Z[X];
# BadAt e eps d  <=>  the cyclotomic polynomial Phi_d divides P in Z[X] (Phi_d is monic: exact long division,
# remainder 0).  Left: #{eps | exists d | 2^k n', BadAt};  right: #{eps | exists d | n', BadAt}.  Claim: left <= 2*right.
# Polynomials are lists of Python integers, lowest degree first.
import sys, random, itertools
from fractions import Fraction
import numpy as np

def divmod_monic(a, b):
    """quotient and remainder of a by the monic b, in Z[X]"""
    assert b[-1] == 1
    a = list(a)
    db = len(b) - 1
    q = [0] * max(0, len(a) - db)
    for i in range(len(a) - 1, db - 1, -1):
        c = a[i]
        if c:
            q[i - db] = c
            for t in range(db + 1):
                a[i - db + t] -= c * b[t]
    return q, a[:db] + [0] * max(0, db - len(a))

_phi = {}
def cyclotomic(d):
    """Phi_d = (X^d - 1) / product of Phi_t over t | d, t < d (exact divisions)"""
    if d in _phi:
        return _phi[d]
    f = [-1] + [0] * (d - 1) + [1]
    for t in range(1, d):
        if d % t == 0:
            f, r = divmod_monic(f, cyclotomic(t))
            assert not any(r)
    _phi[d] = f
    return f

def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]

def badAt_literal(e, eps, d):
    """Phi_d | sum of +-X^(e_k), by one long division of the whole polynomial"""
    P = [0] * (max(e) + 1 if e else 1)
    for ek, s in zip(e, eps):
        P[ek] += 1 if s else -1
    _, r = divmod_monic(P, cyclotomic(d))
    return not any(r)

_rem = {}
def rem_monomial(a, d):
    """the remainder of X^a by Phi_d (long division of the monomial), as a tuple of length deg Phi_d"""
    key = (a, d)
    if key not in _rem:
        _, r = divmod_monic([0] * a + [1], cyclotomic(d))
        _rem[key] = tuple(r)
    return _rem[key]

_signs = {}
def signs(m):
    # rows: every signing, as +-1; row index i has sign of element k = +1 iff bit k of i is set
    if m not in _signs:
        S = np.ones((2 ** m, m), dtype=np.int64)
        for k in range(m):
            S[:, k] = np.where((np.arange(2 ** m) >> k) & 1, 1, -1)
        _signs[m] = S
    return _signs[m]

def badvec(e, d):
    """for every signing: is it bad at d?  (the remainder of P is the signed sum of the remainders of the monomials)"""
    m = len(e)
    if m == 0:
        return np.ones(1, dtype=bool)          # P = 0 is divisible by everything
    R = np.array([rem_monomial(a, d) for a in e], dtype=np.int64)    # m x deg
    return ~((signs(m) @ R).any(axis=1))

def two_counts(e, k, n1):
    m = len(e)
    left = np.zeros(2 ** m, dtype=bool)
    right = np.zeros(2 ** m, dtype=bool)
    for d in divisors(n1):
        right |= badvec(e, d)
    left |= right
    for d in divisors(2 ** k * n1):
        if n1 % d:
            left |= badvec(e, d)
    return int(left.sum()), int(right.sum())

def selftest(rng):
    # 1. cyclotomic polynomials against sympy's
    try:
        import sympy
        X = sympy.Symbol('X')
        for d in range(1, 130):
            c = sympy.Poly(sympy.cyclotomic_poly(d, X), X).all_coeffs()[::-1]
            assert [int(x) for x in c] == cyclotomic(d), d
        print("selftest: Phi_d for d = 1..129 equal sympy's")
    except ImportError:
        print("selftest: sympy not there; Phi_d only from the product formula")
    # 2. the vector form against one long division of the whole signed mask
    n = 0
    for _ in range(600):
        N = rng.choice((1, 2, 3, 4, 6, 8, 9, 12, 15, 20, 24, 40))
        m = rng.randint(0, 6)
        e = tuple(rng.randrange(rng.choice((N, 3 * N, 200))) for _ in range(m))
        for d in divisors(N):
            v = badvec(e, d)
            for i in range(2 ** m):
                eps = tuple(bool((i >> t) & 1) for t in range(m))
                assert badAt_literal(e, eps, d) == bool(v[i]), (e, eps, d)
                n += 1
    print(f"selftest: the vector form of BadAt = long division of the whole signed mask on {n} (family, signing, d) triples")
    # 3. known cases
    assert two_counts((0, 1), 0, 1) == (2, 2)          # X^a - X^b at 1 only
    assert two_counts((0, 1), 1, 1) == (4, 2)          # 1 + X = Phi_2
    assert two_counts((0, 1, 2), 0, 3) == (2, 2)       # +-(1 + X + X^2) = +-Phi_3; an odd number of signs has no zero sum
    assert two_counts((), 3, 5) == (1, 1)
    assert two_counts((7,), 3, 5) == (0, 0)
    print("selftest: five known cases")

class Tally:
    def __init__(self):
        self.fam = 0; self.fail = 0; self.eq2 = 0; self.right0 = 0; self.left_pos_right0 = 0
        self.maxratio = Fraction(0); self.signings = 0; self.f32 = 0; self.f1 = 0; self.first = {}
        self.redmis = 0
    def add(self, e, k, n1, check_reduction=False):
        L, R = two_counts(e, k, n1)
        self.fam += 1; self.signings += 2 ** len(e)
        if L > 2 * R:
            self.fail += 1; self.first.setdefault('FAILS', (e, k, n1, L, R))
        if R == 0:
            self.right0 += 1
            if L > 0:
                self.left_pos_right0 += 1
        else:
            self.maxratio = max(self.maxratio, Fraction(L, R))
            if L == 2 * R:
                self.eq2 += 1; self.first.setdefault('factor 2 attained', (e, k, n1, L, R))
        if 2 * L > 3 * R:
            self.f32 += 1; self.first.setdefault('variant 3/2 fails', (e, k, n1, L, R))
        if L > R:
            self.f1 += 1
        if check_reduction:
            # the same two numbers from the exponents reduced modulo n (left) and modulo n' (right)
            n = 2 ** k * n1
            L2, _ = two_counts(tuple(a % n for a in e), k, n1)
            _, R2 = two_counts(tuple(a % n1 for a in e), 0, n1)
            if (L2, R2) != (L, R):
                self.redmis += 1; self.first.setdefault('REDUCTION MISMATCH', (e, k, n1, (L, R), (L2, R2)))
        return L, R
    def line(self):
        return (f"families {self.fam}, signings {self.signings}, fails {self.fail}, right = 0: {self.right0} "
                f"(of them left > 0: {self.left_pos_right0}), largest left/right {self.maxratio}, left = 2*right > 0: {self.eq2}, "
                f"left > right: {self.f1}, [false variant 2*left <= 3*right fails {self.f32}]")

def exhaustive(cases):
    """every multiset of m elements of 0..n-1 (n = 2^k n'), every signing"""
    tot = Tally()
    for n1, k, mmax in cases:
        n = 2 ** k * n1
        for m in range(0, mmax + 1):
            t = Tally()
            for e in itertools.combinations_with_replacement(range(n), m):
                L, R = t.add(e, k, n1)
                tot.fam += 1; tot.signings += 2 ** m
                if L > 2 * R:
                    tot.fail += 1
                if R and L == 2 * R:
                    tot.eq2 += 1
            print(f"n' = {n1}, k = {k}, n = {n}, m = {m}: {t.line()}")
            for kk, v in t.first.items():
                if kk in ('FAILS',):
                    print("   ", kk, v)
            sys.stdout.flush()
    print(f"TOTAL exhaustive: families {tot.fam}, signings {tot.signings}, fails {tot.fail}, left = 2*right > 0: {tot.eq2}")

def randomrun(seed, N, n1s, ks, label, mmax=9):
    rng = random.Random(seed)
    tot = Tally(); per = {}
    for it in range(N):
        n1 = rng.choice(n1s); k = rng.choice(ks); n = 2 ** k * n1
        m = rng.randint(0, mmax)
        style = rng.randrange(4)
        if style == 0:
            e = tuple(rng.randrange(n) for _ in range(m))
        elif style == 1:                     # exponents not reduced: up to 4n, and sometimes far beyond
            e = tuple(rng.randrange(4 * n) + (rng.choice((0, 0, 0, 5 * n)) ) for _ in range(m))
        elif style == 2:                     # few residues, repeated elements
            pool = [rng.randrange(n) for _ in range(rng.randint(1, 3))]
            e = tuple(rng.choice(pool) + n * rng.randrange(2) for _ in range(m))
        else:                                # an arithmetic progression (a coset-like family), shifted
            g = rng.choice(divisors(n)); a = rng.randrange(n)
            e = tuple((a + g * t) % n for t in range(m))
        for T in (tot, per.setdefault((n1, k), Tally())):
            T.add(e, k, n1, check_reduction=(T is tot))
    print(f"RANDOM {label}, seed {seed}: {tot.line()}; reduction mismatches {tot.redmis}")
    for kk, v in tot.first.items():
        print(f"   first case, {kk}: e = {v[0]}, k = {v[1]}, n' = {v[2]}, counts {v[3:]}")
    for key in sorted(per):
        t = per[key]
        print(f"   n' = {key[0]}, k = {key[1]}: families {t.fam}, fails {t.fail}, largest ratio {t.maxratio}, left = 2*right > 0: {t.eq2}")
    sys.stdout.flush()

def wrong_right(seed, N):
    # a statement that is NOT the Corollary: on the right only d = 1 (as if n' were 1) while the left has n = 2^k n'
    rng = random.Random(seed)
    bad = 0; first = None
    for it in range(N):
        n1 = rng.choice((3, 5, 9, 15)); k = rng.choice((0, 1, 2)); n = 2 ** k * n1
        m = rng.randint(1, 7)
        e = tuple(rng.randrange(n) for _ in range(m))
        L, _ = two_counts(e, k, n1)
        _, R = two_counts(e, 0, 1)
        if L > 2 * R:
            bad += 1
            if first is None:
                first = (e, k, n1, L, R)
    print(f"NOT the Corollary (right side with d = 1 only), seed {seed}: families {N}, 'at most twice' fails {bad}; first: {first}")

if __name__ == '__main__':
    what = sys.argv[1]
    rng = random.Random(12345)
    selftest(rng)
    if what == 'exh':
        exhaustive([(1, 0, 8), (1, 1, 8), (1, 2, 8), (1, 3, 6), (1, 4, 4),
                    (3, 0, 8), (3, 1, 7), (3, 2, 5), (3, 3, 4),
                    (5, 0, 7), (5, 1, 6), (5, 2, 4), (5, 3, 3),
                    (7, 0, 6), (7, 1, 5), (7, 2, 4),
                    (9, 0, 6), (9, 1, 5), (9, 2, 3),
                    (15, 0, 5), (15, 1, 4), (15, 2, 3)])
    elif what == 'rand':
        randomrun(int(sys.argv[2]), int(sys.argv[3]), (1, 3, 5, 7, 9, 15, 21, 25, 27), (0, 1, 2, 3), "n' odd")
    elif what == 'randbig':
        # more elements (up to 11) on small moduli
        randomrun(int(sys.argv[2]), int(sys.argv[3]), (1, 3, 5, 9, 15), (0, 1, 2, 3), "n' odd, up to 11 elements", mmax=11)
    elif what == 'even':
        # n' even: the hypothesis of the Lean statement excludes it
        randomrun(int(sys.argv[2]), int(sys.argv[3]), (2, 4, 6, 8, 10, 12, 18, 20), (0, 1, 2), "n' EVEN (excluded by the hypothesis)", mmax=8)
        exhaustive([(2, 1, 8), (2, 2, 6), (4, 1, 6), (6, 1, 5), (6, 2, 4), (10, 1, 4), (12, 1, 4)])
    elif what == 'wrong':
        wrong_right(int(sys.argv[2]), int(sys.argv[3]))
