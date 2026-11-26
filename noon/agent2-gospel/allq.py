"""HAKMEM's ".155" is a share of all fractions, with even denominators too.  The same count as the first sheet's G8, over every
denominator q up to 10^6 (a fraction p/q behaves as the odd part of q does), each q weighted by its number of fractions.
usage: python -I allq.py > allq.out      (numpy; one thread; under a minute)"""
import math, sys
import numpy as np

N = 10 ** 6

if __name__ == '__main__':
    spf = np.zeros(N + 1, dtype=np.int32)
    for i in range(2, int(N ** 0.5) + 1):
        if spf[i] == 0:
            idx = np.arange(i * i, N + 1, i); idx = idx[spf[idx] == 0]; spf[idx] = i
    z = np.nonzero(spf == 0)[0]; spf[z] = z; spf = spf.tolist()

    def factor(m):
        out = []
        while m > 1:
            l = spf[m]; e = 0
            while m % l == 0: m //= l; e += 1
            out.append((l, e))
        return out
    ordmemo = {}
    def ord_prime(r):
        o = ordmemo.get(r)
        if o is None:
            o = r - 1
            for s, _ in factor(r - 1):
                while o % s == 0 and pow(2, o // s, r) == 1: o //= s
            ordmemo[r] = o
        return o
    def val(o, l):
        k = 0
        while o % l == 0: o //= l; k += 1
        return k
    def bounded(f):                      # f: the odd part's factors; below 10^6 the only prime with a defect, 1093, cannot occur squared with anything else
        for l, e in f:
            if e < 2: continue
            if all(r == l or val(ord_prime(r), l) < e - 1 for r, _ in f): return True
        return False

    marks = (10 ** 4, 10 ** 5, 10 ** 6); out = {}; w_all = w_sq = w_b = 0; n_all = n_sq = n_b = 0
    for q in range(1, N + 1):
        f = factor(q); phi = q
        for l, e in f: phi = phi // l * (l - 1)
        fo = [(l, e) for l, e in f if l != 2]; sq = any(e >= 2 for l, e in fo); b = sq and bounded(fo)
        w_all += phi; n_all += 1
        if sq: w_sq += phi; n_sq += 1
        if b: w_b += phi; n_b += 1
        if q in marks: out[q] = (n_all, n_sq, n_b, w_all, w_sq, w_b)
    for q in marks:
        na, ns, nb, wa, ws, wb = out[q]
        print(f"every denominator up to {q}: its odd part holds a square for {ns / na:.4f}, and the path is bounded for {nb / na:.4f}; weighted by the number of fractions: {ws / wa:.4f} and {wb / wa:.4f}")
    print(f"HAKMEM's product: 1 - prod over odd primes below 10^6 of (1 - 1/(P(P+1))) = {1 - math.prod(1 - 1 / (p * (p + 1)) for p in range(3, N, 2) if spf[p] == p):.5f}")
