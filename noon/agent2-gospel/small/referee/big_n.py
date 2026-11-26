# big_n.py -- the program's rounding error where the round is longest: the records of small-2e6.txt
# with the largest n, recomputed with mpmath at 30 digits.
import sys
from multiprocessing import Pool
from mpmath import mp, mpf, cos, sin, pi, sqrt, nstr
def one(r):
    mp.dps = 30
    ab, re, im = float(r[0]), float(r[1]), float(r[2]); m, a, n = int(r[3]), int(r[4]), int(r[5])
    x = a; sr = mpf(0); si = mpf(0); k = 0; tp = 2 * pi / m
    while True:
        t = tp * x; sr += cos(t); si += sin(t); x = 2 * x % m; k += 1
        if x == a: break
    assert k == n
    return 'm=%d a=%d n=%d program |S|=%.17e mpmath |S|=%s diff re %s diff im %s ; n*4e-16 = %.2e' % (m, a, n, ab, nstr(sqrt(sr*sr+si*si), 20), nstr(mpf(re) - sr, 3), nstr(mpf(im) - si, 3), n * 4e-16)
if __name__ == '__main__':
    rows = [l.split() for l in open(sys.argv[1]) if not l.startswith('#')]
    rows.sort(key=lambda r: -int(r[5]))
    with Pool(3) as p:
        for s in p.imap(one, rows[:3]): print(s, flush=True)
