# Statements 3 to 7 (signings bad at d: Phi_d divides sum_k eps_k X^(e_k)), tested by exact counting over all signings.
# Instruments:
#   (i)  reduction modulo Phi_d: X^r mod Phi_d as an integer vector (exact), a signing is bad iff the signed sum of
#        the vectors of its exponents is the zero vector;
#   (ii) plain long division of the mask by Phi_d over the integers (exponents not reduced), remainder zero;
#   (iii) evaluation at exp(2 pi i / d) in floating point (a rough third look).
# Phi_d itself is made by exact division of X^d - 1 by the Phi_c, c | d, c < d.
# usage: python bad.py validate | s3 | s5 | s7
import itertools, random, sys, cmath, time
from math import comb, gcd
import numpy as np

# ---------- cyclotomic polynomials, exact ----------
_phi = {}


def polydivmod(num, den):
    """num, den: lists of ints, lowest degree first; den monic.  Returns (quotient, remainder)."""
    num = list(num)
    n, k = len(num), len(den)
    assert den[-1] == 1
    if n < k:
        return [0], num + [0] * (k - 1 - n)
    q = [0] * (n - k + 1)
    for i in range(n - k, -1, -1):
        c = num[i + k - 1]
        q[i] = c
        if c:
            for j in range(k):
                num[i + j] -= c * den[j]
    return q, num[:k - 1]


def divisors(n):
    return [c for c in range(1, n + 1) if n % c == 0]


def cyclo(d):
    if d not in _phi:
        p = [-1] + [0] * (d - 1) + [1]
        for c in divisors(d):
            if c < d:
                p, r = polydivmod(p, cyclo(c))
                assert not any(r)
        _phi[d] = p
    return _phi[d]


def totient(d):
    return sum(1 for j in range(1, d + 1) if gcd(j, d) == 1)


_T = {}


def redtable(d):
    """T[r] = coefficients of X^r mod Phi_d, r = 0 .. d-1, an integer array d x phi(d)"""
    if d not in _T:
        ph = cyclo(d)
        k = len(ph) - 1
        T = np.zeros((d, k), dtype=np.int64)
        v = [0] * k
        v[0] = 1
        if k == 1 and False:
            pass
        # X^0 mod Phi_d (for d = 1: Phi = X - 1, degree 1, X^0 = 1)
        for r in range(d):
            T[r] = v
            # multiply by X and reduce
            top = v[-1]
            v = [0] + v[:-1]
            if top:
                for j in range(k):
                    v[j] -= top * ph[j]
        # X^d = 1 mod Phi_d
        assert v == [1] + [0] * (k - 1), (d, v)
        _T[d] = T
    return _T[d]


_S = {}


def signs(m):
    """all 2^m signings as rows of +1/-1 (bit j of the row number set: +1)"""
    if m not in _S:
        i = np.arange(1 << m, dtype=np.int64)[:, None]
        j = np.arange(m, dtype=np.int64)[None, :]
        _S[m] = (((i >> j) & 1) * 2 - 1).astype(np.int64)
    return _S[m]


def badvec(e, d):
    """Boolean array over all signings: bad at d (instrument i)."""
    m = len(e)
    if m == 0:
        return np.ones(1, dtype=bool)
    T = redtable(d)
    V = T[np.asarray(e, dtype=np.int64) % d]
    R = signs(m) @ V
    return ~R.any(axis=1)


def badvec_division(e, d):
    """the same by long division over the integers, exponents as given (instrument ii)"""
    m = len(e)
    out = np.zeros(1 << m, dtype=bool)
    ph = cyclo(d)
    S = signs(m) if m else np.zeros((1, 0), dtype=np.int64)
    for i in range(1 << m):
        p = [0] * ((max(e) if m else 0) + 1)
        for k in range(m):
            p[e[k]] += int(S[i, k])
        q, r = polydivmod(p, ph)
        out[i] = not any(r)
    return out


def badvec_float(e, d):
    m = len(e)
    if m == 0:
        return np.ones(1, dtype=bool)
    z = cmath.exp(2j * cmath.pi / d)
    V = np.array([z ** (x % d) for x in e])
    return np.abs(signs(m) @ V) < 1e-9


# ---------- generators of exponents ----------
def prime_factors(n):
    return [p for p in range(2, n + 1) if n % p == 0 and all(p % q for q in range(2, p))]


def gen_exps(N, m, rng):
    """m exponents, random or structured with respect to the modulus N; some lifted above N"""
    mode = rng.randrange(7)
    divs = [c for c in divisors(N) if c > 1]
    if mode == 0 or not divs:
        e = [rng.randrange(N) for _ in range(m)]
    elif mode == 1:
        pool = [rng.randrange(N) for _ in range(rng.randint(1, 3))]
        e = [rng.choice(pool) for _ in range(m)]
    elif mode == 2:
        c = rng.choice(divs)
        s = rng.randrange(N)
        e = [(s + rng.randrange(c) * (N // c)) % N for _ in range(m)]
    elif mode == 3:
        c1, c2 = rng.choice(divs), rng.choice(divs)
        e = [(rng.randrange(c1) * (N // c1) + rng.randrange(c2) * (N // c2)) % N for _ in range(m)]
    elif mode == 4:
        e = []
        while len(e) < m:
            p = rng.choice(prime_factors(N))
            s = rng.randrange(N)
            e += [(s + j * (N // p)) % N for j in range(p)]
        e = e[:m]
    elif mode == 5:
        c = rng.choice(divs)
        h = rng.randint(0, m)
        e = [0] * h + [N // c] * (m - h)
    else:
        # a few classes with odd sizes
        c = rng.choice(divs)
        e = []
        j = 0
        while len(e) < m:
            sz = rng.choice([1, 1, 3, 5])
            e += [(j * (N // c)) % N] * sz
            j += 1
        e = e[:m]
    if rng.random() < 0.3:
        e = [x + N * rng.randrange(3) for x in e]
    rng.shuffle(e)
    return e


# ---------- runs ----------
def run_validate():
    rng = random.Random(1)
    # known cyclotomic polynomials
    assert cyclo(1) == [-1, 1] and cyclo(2) == [1, 1] and cyclo(3) == [1, 1, 1] and cyclo(4) == [1, 0, 1]
    assert cyclo(6) == [1, -1, 1] and cyclo(12) == [1, 0, -1, 0, 1] and cyclo(9) == [1, 0, 0, 1, 0, 0, 1]
    assert cyclo(15) == [1, -1, 0, 1, -1, 1, 0, -1, 1]
    assert min(cyclo(105)) == -2 and len(cyclo(105)) == 49
    for d in range(1, 400):
        ph = cyclo(d)
        assert len(ph) - 1 == totient(d) and ph[-1] == 1
        # value at 1: p for a power of the prime p, 0 for d = 1, else 1
        v1 = sum(ph)
        pf = prime_factors(d)
        assert v1 == (0 if d == 1 else (pf[0] if len(pf) == 1 else 1)), d
        # roots: Phi_d(exp(2 pi i/d)) = 0 numerically
        z = cmath.exp(2j * cmath.pi / d)
        assert abs(sum(c * z ** k for k, c in enumerate(ph))) < 1e-6, d
    print("Phi_d for d < 400: degrees, values at 1, the root exp(2 pi i/d), and the known cases agree")
    n = 0
    nbad = 0
    t0 = time.time()
    while time.time() - t0 < 60:
        d = rng.randint(1, 60)
        m = rng.randint(0, 8)
        e = gen_exps(d * rng.choice([1, 1, 2, 3]), m, rng)
        a = badvec(e, d)
        b = badvec_division(e, d)
        c = badvec_float(e, d)
        assert (a == b).all() and (a == c).all(), (e, d)
        n += 1
        nbad += int(a.sum())
    print("three instruments agree on %d (e, d) with d <= 60, m <= 8 (in all %d bad signings among them)" % (n, nbad))


def s3_search(budget):
    """statement 3 (and 4): one divisor d."""
    rng = random.Random(3)
    M = 12
    best = {}      # (m) -> (count, e, d)
    bestd = {}     # (m, d) -> count
    viol4 = 0
    n = 0

    def see(e, d):
        nonlocal n, viol4
        m = len(e)
        c = int(badvec(e, d).sum())
        n += 1
        if c > comb(m, m // 2):
            print("VIOLATION of statement 3", e, d, c)
            sys.exit(1)
        if d == 1 and m % 2 == 1 and c:
            print("VIOLATION of statement 4", e, c)
            viol4 += 1
            sys.exit(1)
        if c > best.get(m, (-1,))[0]:
            best[m] = (c, list(e), d)
        if c > bestd.get((m, d), -1):
            bestd[(m, d)] = c

    # exhaustive: all multisets of residues modulo d, for small d and m
    nex = 0
    exh = []
    for d in range(1, 13):
        mm = 0
        for m in range(0, M + 1):
            if comb(d + m - 1, m) > 13000:
                break
            mm = m
            for e in itertools.combinations_with_replacement(range(d), m):
                see(e, d)
                nex += 1
        exh.append((d, mm))
    print("exhaustive (all multisets of residues modulo d with m elements), d: largest m =", exh, "; %d cases" % nex)
    # structured and random, d up to 60
    t0 = time.time()
    while time.time() - t0 < budget:
        d = rng.randint(1, 60)
        m = rng.randint(0, M)
        see(gen_exps(d, m, rng), d)
    for d in range(1, 61):
        for m in range(0, M + 1):
            see([5] * m, d)                                     # all exponents equal
            see([0] * (m - 1) + [d // 2] * (1 if m else 0), d)
            for p in prime_factors(d):
                # sizes (m-2, 1, 1), (m-p+1, 1, .., 1) on the classes j d/p
                if m >= p:
                    see([0] * (m - p + 1) + [j * (d // p) for j in range(1, p)], d)
    print("in all %d (e, d); statement 4: no signing bad at 1 for odd m in any of them" % n)
    print()
    print(" m  C(m,m//2)  largest count bad at one d   ratio  equality   case (e, d)")
    for m in range(M + 1):
        c, e, d = best[m]
        print("%2d %9d %12d %20.4f  %-8s  %s, d = %d" % (m, comb(m, m // 2), c, c / comb(m, m // 2),
                                                     "yes" if c == comb(m, m // 2) else "no", e, d))
    print()
    print("odd m: largest count by d (only d with a nonzero count for some odd m):")
    for d in range(1, 61):
        row = [bestd.get((m, d), 0) for m in range(1, M + 1, 2)]
        if any(row):
            print("  d = %2d: m = 1,3,..,11: %s" % (d, row))
    zero_d = [d for d in range(1, 61) if not any(bestd.get((m, d), 0) for m in range(1, M + 1, 2))]
    print("  d with no bad signing found for any odd m:", zero_d)


def union_count(e, N, cache=None):
    """number of signings bad at some divisor of N; also the per-divisor Boolean arrays"""
    acc = None
    per = {}
    for d in divisors(N):
        b = badvec(e, d)
        per[d] = b
        acc = b.copy() if acc is None else (acc | b)
    return int(acc.sum()), per


def s5_search(budget):
    """statements 5 and 6: divisors of 2^k."""
    rng = random.Random(5)
    M = 12
    best = {}
    bestk = {}
    n = 0
    eq = {}

    def see(e, k):
        nonlocal n
        m = len(e)
        c, per = union_count(e, 2 ** k)
        n += 1
        rhs = 2 * comb(m, m // 2)
        if c > rhs:
            print("VIOLATION of statement 5", e, k, c, rhs)
            sys.exit(1)
        if m % 2 == 1 and c:
            print("VIOLATION of statement 6", e, k, c)
            sys.exit(1)
        if c > best.get(m, (-1,))[0]:
            best[m] = (c, list(e), k)
        if c > bestk.get((m, k), -1):
            bestk[(m, k)] = c
        if c == rhs:
            eq.setdefault(m, (list(e), k))

    nex = 0
    exh = []
    for k in range(0, 5):
        N = 2 ** k
        mm = 0
        for m in range(0, M + 1):
            if comb(N + m - 1, m) > 20000:
                break
            mm = m
            for e in itertools.combinations_with_replacement(range(N), m):
                see(e, k)
                nex += 1
        exh.append((k, mm))
    print("exhaustive (all multisets of residues modulo 2^k with m elements), k: largest m =", exh, "; %d cases" % nex)
    for k in range(0, 7):
        for m in range(0, M + 1):
            see([0] * (m - 1) + [1] * (1 if m else 0), k)      # classes of sizes m-1 and 1 modulo 2
            see([0] * m, k)
            see(list(range(m)), k)
    t0 = time.time()
    while time.time() - t0 < budget:
        k = rng.randint(0, 6)
        m = rng.randint(0, M)
        see(gen_exps(2 ** k, m, rng), k)
    print("in all %d (e, k), k <= 6; statement 6: no signing bad at a divisor of 2^k for odd m in any of them" % n)
    print()
    print(" m  2 C(m,m//2)  2^m  largest count  ratio  equality  case (e, k)")
    for m in range(M + 1):
        c, e, k = best[m]
        rhs = 2 * comb(m, m // 2)
        print("%2d %9d %6d %9d %10.4f  %-8s  %s, k = %d" % (m, rhs, 2 ** m, c, c / rhs, "yes" if c == rhs else "no", e, k))
    print()
    print("largest count by k (rows k = 0..6; columns m = 0, 2, .., 12):")
    for k in range(0, 7):
        print("  k = %d: %s" % (k, [bestk.get((m, k), 0) for m in range(0, M + 1, 2)]))


def s7_search(budget):
    """statement 7: divisors of 2^k n', n' odd; also the proved 'twice' (count(2^k n') <= 2 count(n'))."""
    rng = random.Random(7)
    M = 12
    best = {}       # m -> (ratio, count, rhs, e, k, n')
    bestn = {}      # n' -> (ratio, count, rhs, e, k, m)
    bestsum = {}    # m -> largest count(n') / (d(n') C) (union over the divisors of n' against the sum bound), n' > 1
    twice = {}      # parity of m -> largest count(2^k n') / count(n')
    n = 0
    eq = []

    def see(e, k, n1):
        nonlocal n
        m = len(e)
        N = 2 ** k * n1
        c, per = union_count(e, N)
        n += 1
        dn = len(divisors(n1))
        rhs = 2 * dn * comb(m, m // 2)
        if c > rhs:
            print("VIOLATION of statement 7", e, k, n1, c, rhs)
            sys.exit(1)
        acc = np.zeros_like(per[1])
        for d in divisors(n1):
            acc |= per[d]
        c1 = int(acc.sum())
        if c > 2 * c1:
            print("VIOLATION of card_exists_badAt_le", e, k, n1, c, c1)
            sys.exit(1)
        r = c / rhs
        if r > best.get(m, (-1,))[0]:
            best[m] = (r, c, rhs, list(e), k, n1)
        if m >= 1 and r > bestn.get(n1, (-1,))[0]:
            bestn[n1] = (r, c, rhs, list(e), k, m)
        if c == rhs:
            eq.append((list(e), k, n1))
        if c1:
            key = m % 2
            if c / c1 > twice.get(key, (0,))[0]:
                twice[key] = (c / c1, c, c1, list(e), k, n1)
        if n1 > 1:
            r1 = c1 / (dn * comb(m, m // 2))
            if r1 > bestsum.get(m, (-1,))[0]:
                bestsum[m] = (r1, c1, dn * comb(m, m // 2), list(e), n1)

    odd = list(range(1, 46, 2))
    # exhaustive for small moduli
    nex = 0
    exh = []
    for N in range(1, 13):
        k = 0
        n1 = N
        while n1 % 2 == 0:
            n1 //= 2
            k += 1
        mm = 0
        for m in range(0, 9):
            if comb(N + m - 1, m) > 7000:
                break
            mm = m
            for e in itertools.combinations_with_replacement(range(N), m):
                see(e, k, n1)
                nex += 1
        exh.append((N, mm))
    print("exhaustive (all multisets of residues modulo N = 2^k n' with m elements), N: largest m =", exh,
          "; %d cases" % nex)
    for n1 in odd:
        for k in range(0, 4):
            N = 2 ** k * n1
            for m in range(0, M + 1):
                see([0] * (m - 1) + [N // 2 if k else 0] * (1 if m else 0), k, n1)
                see([0] * m, k, n1)
    t0 = time.time()
    while time.time() - t0 < budget:
        n1 = rng.choice(odd)
        k = rng.randint(0, 3)
        m = rng.randint(0, M)
        see(gen_exps(2 ** k * n1, m, rng), k, n1)
    print("in all %d (e, k, n'), k <= 3, n' odd <= 45, m <= %d" % (n, M))
    print()
    print(" m  largest ratio count / (2 d(n') C(m,m//2))   count   bound  case (e, k, n')")
    for m in range(M + 1):
        r, c, rhs, e, k, n1 = best[m]
        print("%2d %10.4f %30d %7d  %s, k = %d, n' = %d" % (m, r, c, rhs, e, k, n1))
    print()
    print("by n' (m >= 1): largest ratio, count, bound, case")
    for n1 in odd:
        r, c, rhs, e, k, m = bestn[n1]
        print("  n' = %2d (d(n') = %d): %.4f  %d / %d   m = %d, k = %d, e = %s" % (
            n1, len(divisors(n1)), r, c, rhs, m, k, e))
    print()
    print("equality in statement 7 found in %d cases; with n' > 1: %d; first few: %s" % (
        len(eq), sum(1 for x in eq if x[2] > 1), eq[:4]))
    print()
    print("the proved 'twice': largest count(2^k n') / count(n') where count(n') > 0:")
    for key in sorted(twice):
        r, c, c1, e, k, n1 = twice[key]
        print("  m %s: %.4f (%d / %d), e = %s, k = %d, n' = %d" % ("even" if key == 0 else "odd", r, c, c1, e, k, n1))
    print()
    print("n' > 1: largest count(some divisor of n') / (d(n') C(m,m//2)), the step that sums over the divisors of n':")
    for m in range(M + 1):
        if m in bestsum:
            r1, c1, b1, e, n1 = bestsum[m]
            print("  m = %2d: %.4f (%d / %d), e = %s, n' = %d" % (m, r1, c1, b1, e, n1))


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "validate":
        run_validate()
    elif mode == "s3":
        s3_search(float(sys.argv[2]) if len(sys.argv) > 2 else 60)
    elif mode == "s5":
        s5_search(float(sys.argv[2]) if len(sys.argv) > 2 else 60)
    elif mode == "s7":
        s7_search(float(sys.argv[2]) if len(sys.argv) > 2 else 90)
