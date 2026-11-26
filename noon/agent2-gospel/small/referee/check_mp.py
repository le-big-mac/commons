# check_mp.py -- recompute the smallest sums of small-2e6.txt with mpmath (50 digits) and compare;
# also an exact test that the sum is not nought: evaluate the same sum at an element of order m in a
# prime field F_P, P = 1 mod m (if S were 0 the image would be 0 for every such element).
import sys
from mpmath import mp, mpf, mpc, cos, sin, pi, fabs, sqrt, nstr
mp.dps = 50

def S_mp(m, a):
    x = a % m; sr = mpf(0); si = mpf(0); n = 0
    while True:
        t = 2 * pi * x / m
        sr += cos(t); si += sin(t)
        x = 2 * x % m; n += 1
        if x == a % m: break
    return sr, si, n

def isprime(n):
    if n < 2: return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0: return n == p
    d = n - 1; s = 0
    while d % 2 == 0: d //= 2; s += 1
    for b in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        x = pow(b, d, n)
        if x in (1, n - 1): continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1: break
        else: return False
    return True

def factor(m):
    f = []; p = 3
    while p * p <= m:
        if m % p == 0:
            f.append(p)
            while m % p == 0: m //= p
        p += 2
    if m > 1: f.append(m)
    return f

def modp_nonzero(m, a):
    """True if the sum is non-zero at some element of order m in some F_P (hence S != 0 exactly)."""
    fs = factor(m)
    k = 2; tried = 0
    while tried < 3:
        P = k * m + 1
        if isprime(P):
            tried += 1
            for g0 in range(2, 60):
                g = pow(g0, (P - 1) // m, P)
                if all(pow(g, m // q, P) != 1 for q in fs):   # order exactly m
                    x = a % m; s = 0
                    while True:
                        s += pow(g, x, P); x = 2 * x % m
                        if x == a % m: break
                    if s % P != 0: return True
                    break
        k += 2
    return False

if __name__ == '__main__':
    fn = sys.argv[1]; want = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    rows = [l.split() for l in open(fn) if not l.startswith('#')]
    def show(rows, title):
        print(title)
        print('  m a n self | program |S| | mpmath |S| (50 digits, shown to 25) | program - mpmath | diff re | diff im | exact non-zero mod P')
        for r in rows:
            ab, re, im = float(r[0]), float(r[1]), float(r[2]); m, a, n, self_ = int(r[3]), int(r[4]), int(r[5]), int(r[6])
            sr, si, n2 = S_mp(m, a)
            A = sqrt(sr * sr + si * si)
            assert n2 == n
            print('  %d %d %d %d | %.17e | %s | %s | %s | %s | %s' % (m, a, n, self_, ab, nstr(A, 25), nstr(mpf(ab) - A, 3), nstr(mpf(re) - sr, 3), nstr(mpf(im) - si, 3), modp_nonzero(m, a)))
    show(rows[:want], 'smallest %d overall' % want)
    show([r for r in rows if r[6] == '0'][:want], 'smallest %d not self-negative' % want)
