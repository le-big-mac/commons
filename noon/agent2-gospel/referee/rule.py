"""The rule, in two forms, and the shares up to N.

Form A (orders):  odd m > 1 is bounded  iff  ord_m(2) != ord_rad(m)(2).
Form B (primes):  odd m > 1 is bounded  iff  some prime l | m, with l^e || m, has
                  e >= w_l + 1 + max over primes r | m of v_l(ord_r(2)),
                  where w_l = v_l(2^ord_l(2) - 1)  (1 unless l is a Wieferich prime).

Output: rule.out
"""
import sys, math


def sieve_spf(n):
    spf = list(range(n + 1))
    i = 2
    while i * i <= n:
        if spf[i] == i:
            for j in range(i * i, n + 1, i):
                if spf[j] == j:
                    spf[j] = i
        i += 1
    return spf


def factor(n, spf):
    f = {}
    while n > 1:
        p = spf[n]
        while n % p == 0:
            n //= p
            f[p] = f.get(p, 0) + 1
    return f


def order2(m, spf):
    """Multiplicative order of 2 mod odd m > 1, by stripping primes from phi(m)."""
    f = factor(m, spf)
    phi = 1
    for p, e in f.items():
        phi *= (p - 1) * p ** (e - 1)
    n = phi
    for p in factor(phi, spf):
        while n % p == 0 and pow(2, n // p, m) == 1:
            n //= p
    return n


def order2_slow(m):
    k, a = 1, 2 % m
    while a != 1:
        a = (2 * a) % m
        k += 1
    return k


def vp(n, p):
    k = 0
    while n % p == 0:
        n //= p
        k += 1
    return k


def rule_A(m, spf):
    f = factor(m, spf)
    rad = 1
    for p in f:
        rad *= p
    if rad == m:
        return False
    return order2(m, spf) != order2(rad, spf)


def make_rule_B(N, spf):
    d = {}      # ord_r(2) for odd primes r <= N
    w = {}
    for r in range(3, N + 1, 2):
        if spf[r] == r:
            d[r] = order2(r, spf)
            w[r] = vp(pow(2, d[r], r ** 4) - 1, r) if r < 4000 else (2 if pow(2, r - 1, r * r) == 1 else 1)

    def rule_B(m):
        f = factor(m, spf)
        for l, e in f.items():
            if e < 2:
                continue
            mx = 0
            for r in f:
                if r != l:
                    mx = max(mx, vp(d[r], l))
            if e >= w[l] + 1 + mx:
                return True
        return False
    return rule_B, d, w


if __name__ == '__main__':
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 10 ** 6
    outname = sys.argv[2] if len(sys.argv) > 2 else '/home/agent2/gospel/referee/rule.out'
    out = open(outname, 'w')
    spf = sieve_spf(N)
    rule_B, d, w = make_rule_B(N, spf)
    print('Wieferich primes up to', N, ':', [r for r in w if w[r] > 1], file=out)
    # the two forms against each other up to 30000, with a slow order as a check
    bad = 0
    for m in range(3, 30001, 2):
        if rule_A(m, spf) != rule_B(m):
            bad += 1
    print('form A vs form B, odd m to 30000: disagreements', bad, file=out)
    bad = sum(1 for m in range(3, 4001, 2) if order2(m, spf) != order2_slow(m))
    print('fast order vs slow order, odd m to 4000: disagreements', bad, file=out)
    bl = [m for m in range(3, 3001, 2) if rule_B(m)]
    print('rule B, odd m 3..3000: bounded', len(bl), file=out)
    print('rule B list:', bl, file=out)
    # shares
    marks = [10 ** 4, 10 ** 5, 10 ** 6, 10 ** 7]
    marks = [x for x in marks if x <= N]
    cnt = tot = 0
    wcnt = wtot = 0
    sq = sqw = 0
    exc = []
    for m in range(1, N + 1, 2):
        f = factor(m, spf)
        phi = 1
        hassq = False
        for p, e in f.items():
            phi *= (p - 1) * p ** (e - 1)
            if e >= 2:
                hassq = True
        tot += 1
        wtot += phi
        if hassq:
            sq += 1
            sqw += phi
        if m > 1 and rule_B(m):
            cnt += 1
            wcnt += phi
        elif hassq and len(exc) < 40:
            exc.append(m)
        if m + 1 in marks or m in marks:
            print('N=%8d  odd m: %7d  bounded: %6d  share %.5f | weighted by phi: %.5f | '
                  'with an odd prime squared: plain %.5f weighted %.5f'
                  % (m + 1, tot, cnt, cnt / tot, wcnt / wtot, sq / tot, sqw / wtot), file=out)
    print('first forty odd m with a squared prime factor yet unbounded:', exc, file=out)
    print('8/pi^2 complement:', 1 - 8 / math.pi ** 2, file=out)
    out.close()
    print(open(outname).read()[-1500:])
