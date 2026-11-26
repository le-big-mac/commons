"""The referee's reason for the model's low counts, recomputed with a program of my own and carried to two million.
The model takes the mean square of a real coset sum of n terms to be n.  The true mean square over the cosets of one m is
    (n / k) * sum over d dividing m, with m/d squarefree, of d * mu(m/d) / ord_d(2),      k = phi(m)/n cosets
(the sum over the cosets of |S|^2 is the sum over h in <2> of Ramanujan's sum c_m(h - 1); for a prime m it is n(m - n)/(m - 1)).
Putting that in place of n, for the m with at least CUT cosets, gives another H.  No cosines here but in the control.
usage: python -I hvar.py 2000000 > hvar.out"""
import sys, math
from math import gcd

def lcm(a, b): return a // gcd(a, b) * b

if __name__ == '__main__':
    N = int(sys.argv[1])
    spf = list(range(N + 1))
    for i in range(2, int(N ** 0.5) + 1):
        if spf[i] == i:
            for j in range(i * i, N + 1, i):
                if spf[j] == j: spf[j] = i
    ordp = {}
    def order_prime(p):
        o = p - 1; r = p - 1
        while r > 1:
            f = spf[r]
            while r % f == 0: r //= f
            while o % f == 0 and pow(2, o // f, p) == 1: o //= f
        return o
    def order_pp(p, e):
        key = (p, e)
        if key not in ordp:
            if e == 0: ordp[key] = 1
            elif e == 1: ordp[key] = order_prime(p)
            else:
                o = order_pp(p, e - 1); ordp[key] = o if pow(2, o, p ** e) == 1 else o * p
        return ordp[key]
    cuts = (1, 2, 4, 8, 16, 32, 10 ** 9); marks = [m for m in (1500, 20000, 60000, 200000, 2000000) if m <= N]
    H0 = 0.0; H = {c: 0.0 for c in cuts}; nreal = 0; nopen = 0; out = []; ctl = []
    for m in range(3, N + 1, 2):
        f = []; r = m
        while r > 1:
            p = spf[r]; e = 0
            while r % p == 0: r //= p; e += 1
            f.append((p, e))
        n = 1; nrad = 1; phi = 1
        for p, e in f: n = lcm(n, order_pp(p, e)); nrad = lcm(nrad, order_pp(p, 1)); phi *= (p - 1) * p ** (e - 1)
        if n == nrad:                                      # the rounds do not close
            nopen += 1
            if n % 2 == 0 and pow(2, n // 2, m) == m - 1:  # -1 is a power of 2: every coset is its own negative
                k = phi // n; tot = 0.0
                for mask in range(1 << len(f)):
                    d = 1; o = 1; sign = 1
                    for i, (p, e) in enumerate(f):
                        ee = e - 1 if mask >> i & 1 else e
                        if mask >> i & 1: sign = -sign
                        d *= p ** ee; o = lcm(o, order_pp(p, ee))
                    tot += sign * d / o
                v = n * tot / k                            # the true mean square of one coset's sum
                nreal += k; w0 = k * 2 / math.sqrt(2 * math.pi * n); H0 += w0
                w1 = k * 2 / math.sqrt(2 * math.pi * v) if v > 0 else 0.0
                for c in cuts: H[c] += w1 if k >= c else w0
                if m < 400 and len(ctl) < 40: ctl.append((m, n, k, v))
        if m + 1 in marks or m in marks or m + 2 > N:
            mk = m if m in marks else m + 1
            if mk in marks and not any(o[0] == mk for o in out): out.append((mk, nopen, nreal, H0, dict(H)))
    # control: the formula for the mean square against cosines, for the first forty real m
    worst = 0.0
    for m, n, k, v in ctl:
        seen = set(); sq = 0.0
        for a in range(1, m):
            if gcd(a, m) != 1 or a in seen: continue
            x = a; s = 0.0
            while x not in seen: seen.add(x); s += math.cos(2 * math.pi * x / m); x = x * 2 % m
            sq += s * s
        worst = max(worst, abs(sq / k - v))
    print('control: for the first %d odd m with real cosets (%d to %d) the mean square of the coset sums, by cosines, differs from the formula by at most %.1e' % (len(ctl), ctl[0][0], ctl[-1][0], worst))
    for mk, no, nr, h0, h in out:
        print('odd m up to %d: %d whose rounds do not close; %d real cosets; H with n for the mean square: %.4f' % (mk, no, nr, h0))
        print('   H with the true mean square for m of at least CUT cosets: ' + '; '.join('CUT %s: %.1f (%+.2f%%)' % (c if c < 10 ** 9 else 'none', h[c], 100 * (h[c] / h0 - 1)) for c in cuts))
