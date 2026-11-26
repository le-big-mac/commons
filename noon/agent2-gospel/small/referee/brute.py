# brute.py -- a second, independent reckoning for small m: every coset sum for odd m <= N by
# numpy's exp and math.fsum (correctly rounded summation), compared with the C program's records.
import sys, math, numpy as np

LIM = 1e-2
def run(N):
    recs = {}; zero_m = 0; nonzero_m = 0; mixed = 0; least = (9e9, 0, 0, 0)
    counts = [0, 0]
    for m in range(3, N + 1, 2):
        ang = 2 * np.pi * np.arange(m) / m
        c = np.cos(ang); s = np.sin(ang)
        seen = bytearray(m); z = 0; tot = 0
        selfm = None
        for a in range(1, (m - 1) // 2 + 1):
            if seen[a] or math.gcd(a, m) != 1: continue
            xs = []; x = a
            while True:
                xs.append(x); seen[x] = 1; seen[m - x] = 1
                x = 2 * x % m
                if x == a: break
            if selfm is None: selfm = (m - 1) in xs if a == 1 else None
            re = math.fsum(c[xs].tolist()); im = math.fsum(s[xs].tolist()); ab = math.hypot(re, im)
            tot += 1
            if ab < 1e-8: z += 1
            else:
                if ab < least[0]: least = (ab, m, a, len(xs))
                if ab < LIM: recs[(m, a)] = (ab, len(xs), int((m - a) in xs))
        if z == 0: nonzero_m += 1
        elif z == tot: zero_m += 1
        else: mixed += 1
    return recs, zero_m, nonzero_m, mixed, least

if __name__ == '__main__':
    N = int(sys.argv[1]); fn = sys.argv[2]
    if len(sys.argv) > 3: LIM = float(sys.argv[3])
    recs, zm, nzm, mixed, least = run(N)
    crec = {}
    for l in open(fn):
        if l.startswith('#'): continue
        r = l.split(); crec[(int(r[3]), int(r[4]))] = (float(r[0]), int(r[5]), int(r[6]))
    print('brute force, odd m <= %d: zero m %d, non-zero m %d, mixed %d, least non-zero %r' % (N, zm, nzm, mixed, least))
    print('records kept: brute %d, C program %d, same keys: %s' % (len(recs), len(crec), set(recs) == set(crec)))
    worst = 0; bad = 0
    for k in recs:
        if k in crec:
            worst = max(worst, abs(recs[k][0] - crec[k][0]))
            if recs[k][1:] != crec[k][1:]: bad += 1
    print('largest difference in |S| over the common records: %.3e ; records whose n or self flag differ: %d' % (worst, bad))
