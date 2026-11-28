"""Second look: Lemma 1 for EVERY multiset of m elements containing 0 on Z_n, every divisor d > 1 and every residue x
modulo d with fewer than m elements in its class:  #(signings bad at d) <= c_a c_(m-a) 2^m  (an integer:
C(a, a//2) * C(m-a, (m-a)//2)), now with exact counts.
The first run (t_lemma1_all.py) decided "bad at d" by |S(exp(2 pi i/d))| < 1e-9 in floating point.  Here:
 - a signing with S(zeta_d) = 0 has a computed value below 1e-13 (at most 7 terms), so it is among those below 1e-9;
 - every signing found below 1e-9 is CONFIRMED in integers: sum of the signed columns X^b mod Phi_d (lib.red) is 0;
   a signing below 1e-9 that is not confirmed is reported and not counted;
 - the number of computed values between 1e-9 and 1e-6 is reported (a clean gap means the threshold was not at issue);
 - the bound is compared in integers.
Also counts how many of the cases have a >= 1 (the class of x is occupied).
usage: t_lemma1_all_exact.py SECONDS"""
import sys, math, itertools, time
import numpy as np
sys.path.insert(0, '/home/agent3/lean/lift-check/even/limit/referee')
from lib import red
def blocks(n, m, size=150000):
    buf = []
    for rest in itertools.combinations_with_replacement(range(n), m - 1):
        buf.append((0,) + rest)
        if len(buf) == size: yield np.array(buf, dtype=np.int64); buf = []
    if buf: yield np.array(buf, dtype=np.int64)
if __name__ == '__main__':
    secs = float(sys.argv[1]); t0 = time.time(); total = 0; total_occ = 0; fails = 0; unconfirmed = 0; band = 0; confirmed = 0
    for n, m in ((15, 7), (27, 6), (45, 5), (63, 4), (75, 4), (105, 4), (135, 4), (165, 3), (315, 3), (63, 5), (105, 5)):
        if time.time() - t0 > secs: print(f"n = {n} m = {m}: not started (time)"); continue
        divs = [d for d in range(3, n + 1) if n % d == 0]
        Ei = np.array([(1,) + e for e in itertools.product((1, -1), repeat=m - 1)], dtype=np.int64).T     # m x 2^(m-1); first sign +, count twice
        E = Ei.astype(np.float64)
        BIG = np.iinfo(np.int64).max
        bnd = np.array([math.comb(a, a // 2) * math.comb(m - a, (m - a) // 2) for a in range(m)] + [BIG], dtype=np.int64)
        cases = 0; occ = 0; eq = 0; nms = 0; complete = True; worst = 0.0
        for X in blocks(n, m):
            if time.time() - t0 > secs: complete = False; break
            nms += len(X)
            for d in divs:
                Xd = X % d
                z = np.exp(2j * np.pi * np.arange(d) / d)
                av = np.abs(z[Xd] @ E)
                zero = av < 1e-9
                band += int(((av >= 1e-9) & (av < 1e-6)).sum())
                rows, cols = np.nonzero(zero)
                if len(rows):
                    R = red(d); acc = np.zeros((R.shape[0], len(rows)), dtype=np.int64)
                    for j in range(m): acc += R[:, Xd[rows, j]] * Ei[j, cols]
                    notzero = np.any(acc != 0, axis=0)
                    confirmed += int((~notzero).sum())
                    if notzero.any():
                        unconfirmed += int(notzero.sum()); zero[rows[notzero], cols[notzero]] = False
                        print("below 1e-9 but NOT zero in integers:", n, d, X[rows[notzero][0]], flush=True)
                cnt = 2 * zero.sum(axis=1).astype(np.int64)                 # exact number of signings bad at d
                for x in range(d):
                    a = (Xd == x).sum(axis=1)
                    lim = bnd[a]; live = a < m
                    cases += int(live.sum()); occ += int((live & (a >= 1)).sum())
                    f = live & (cnt > lim)
                    if f.any(): fails += int(f.sum()); print("LEMMA 1 FAILS:", n, d, x, X[f][0], flush=True)
                    eq += int((live & (cnt == lim) & (cnt > 0)).sum())
                    worst = max(worst, float(np.max(np.where(live, cnt / np.where(live, lim, 1), 0))))
        total += cases; total_occ += occ
        print(f"n = {n:3d} m = {m}: {nms} multisets{'' if complete else ' (NOT all: time)'}, {cases} cases (multiset, d, x), of them {occ} with a >= 1; largest count/bound {worst:.4f}, equal to the bound (count > 0) in {eq}", flush=True)
    print(f"{total} cases in all, of them {total_occ} with a >= 1 (an occupied class) and {total - total_occ} with a = 0; failures {fails}")
    print(f"signings (first sign +) found below 1e-9: confirmed zero in integers {confirmed}, not confirmed {unconfirmed}; computed values between 1e-9 and 1e-6: {band}")
