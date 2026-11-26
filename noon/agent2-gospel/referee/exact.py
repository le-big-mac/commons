"""Exact check, whole numbers only: is  P(x) = sum over the doubling cycle of x^(2^k mod m)
divisible by the m-th cyclotomic polynomial?  (P(zeta_m) = 0 iff Phi_m | P.)
Then compare three lists for odd m in 3..3000: exact, floating (brute.py), rule (rule.py).

Output: exact.out
"""
import sys
import numpy as np
sys.path.insert(0, '/home/agent2/gospel/referee')
import brute, rule


def cyclotomic(m, spf):
    f = rule.factor(m, spf)
    primes = list(f)
    num, den = [], []
    for mask in range(1 << len(primes)):
        d = 1
        bits = 0
        for i, p in enumerate(primes):
            if mask >> i & 1:
                d *= p
                bits += 1
        (num if bits % 2 == 0 else den).append(m // d)
    poly = [1]
    for k in num:                       # multiply by x^k - 1
        new = [0] * (len(poly) + k)
        for i, c in enumerate(poly):
            new[i + k] += c
            new[i] -= c
        poly = new
    for k in den:                       # exact division by x^k - 1
        n = len(poly) - k
        q = [0] * n
        work = poly[:]
        for i in range(len(work) - 1, k - 1, -1):
            c = work[i]
            q[i - k] = c
            work[i] -= c
            work[i - k] += c
        assert all(v == 0 for v in work[:k]), 'division not exact'
        poly = q
    return poly


def exact_zero(m, spf):
    phi = cyclotomic(m, spf)
    deg = len(phi) - 1
    assert phi[-1] == 1
    Phi = np.array(phi, dtype=np.int64)
    P = np.zeros(m, dtype=np.int64)
    a = 1
    while True:
        P[a] += 1
        a = (2 * a) % m
        if a == 1:
            break
    for i in range(m - 1, deg - 1, -1):
        c = int(P[i])
        if c:
            assert abs(c) < 2 ** 40
            P[i - deg:i + 1] -= c * Phi
    return not P.any(), deg


if __name__ == '__main__':
    out = open('/home/agent2/gospel/referee/exact.out', 'w')
    spf = rule.sieve_spf(3001)
    rule_B, d, w = rule.make_rule_B(3001, spf)
    ex, fl, ra, rb = [], [], [], []
    degbad = 0
    for m in range(3, 3001, 2):
        z, deg = exact_zero(m, spf)
        f = rule.factor(m, spf)
        ph = 1
        for p, e in f.items():
            ph *= (p - 1) * p ** (e - 1)
        if deg != ph:
            degbad += 1
        if z:
            ex.append(m)
        if brute.cycle_sum(1, m)[2] < brute.TOL:
            fl.append(m)
        if rule.rule_A(m, spf):
            ra.append(m)
        if rule_B(m):
            rb.append(m)
    print('odd m 3..3000: cyclotomic degree != phi(m):', degbad, file=out)
    print('exact zero:', len(ex), ' floating zero:', len(fl), ' rule A:', len(ra), ' rule B:', len(rb), file=out)
    print('exact == floating:', ex == fl, file=out)
    print('exact == rule A:', ex == ra, file=out)
    print('exact == rule B:', ex == rb, file=out)
    print('symmetric differences:', sorted(set(ex) ^ set(fl)), sorted(set(ex) ^ set(ra)), sorted(set(ex) ^ set(rb)), file=out)
    # exercise 30's claim and HAKMEM's, on the same range
    def powerful_nonwief(m):
        f = rule.factor(m, spf)
        return all(e >= 2 for e in f.values()) and all(w[p] == 1 for p in f)
    def hakmem(m):
        f = rule.factor(m, spf)
        return any(e >= (3 if w[p] > 1 else 2) for p, e in f.items())
    S = set(ex)
    if_fail = [m for m in range(3, 3001, 2) if powerful_nonwief(m) and m not in S]
    onlyif_fail = [m for m in range(3, 3001, 2) if m in S and not powerful_nonwief(m)]
    print("exercise 30, odd q 3..3000: 'if' fails at", if_fail, file=out)
    print("exercise 30: 'only if' fails at %d values, first twenty %s" % (len(onlyif_fail), onlyif_fail[:20]), file=out)
    h_if = [m for m in range(3, 3001, 2) if hakmem(m) and m not in S]
    h_only = [m for m in range(3, 3001, 2) if m in S and not hakmem(m)]
    print("HAKMEM, odd q 3..3000: has-odd-prime-squared yet unbounded: %d values, first twenty %s" % (len(h_if), h_if[:20]), file=out)
    print("HAKMEM: bounded yet no odd prime squared:", h_only, file=out)
    out.close()
    print(open('/home/agent2/gospel/referee/exact.out').read())
