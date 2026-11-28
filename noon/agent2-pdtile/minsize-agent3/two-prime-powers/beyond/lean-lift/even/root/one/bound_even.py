"""Even m: the bound B_E(m) of result.md (Theorem 6), floating point.

  B_E(m) = c_m + sum over the d* with at least two primes of LC(m, N(d*)) + sum over the prime powers p^j of PPE(m, p, j)
  LC(m, N) = 2^-(N-2) gamma(m, N)                                              (Lemma C; any integer N >= 3)
  Fb(m, p, k, g) = 2^-(k+p-3) max over 0 <= s <= m - ceil(m/(pk)) of c_(m-s) min(g, 2 c_(ceil(s/2) - 2(k+p-4)))   (Lemmas E, E', F)
  PPE(m, p, j) = max( max over k = G, ..., G+q-1 of min(LC(m, k+p-1), Fb(m, p, k, g_k)),  LC(m, G+q+p-1) ),
       G = 1 + (j-1)(p-1), q = max(2, p-2), g_k = 2^-(p-2), except g_1 = 17/64 for p^j = 3;
       for p >= 11 simply PPE(m, p, j) = LC(m, N(p^j)).
  The d* with N(d*) > 61 are bounded together by sqrt(2/(pi m)) * tail (Lemma B), as in bound.py.

usage: bound_even.py M0        the largest sqrt(m) B_E(m) over even m in several ranges up to M0, and the bound for m > M0
"""
import sys, math
import numpy as np
sys.path.insert(0, '/home/agent3/lean/lift-check/even/root/one')
from bound import cnt_table, tail_beyond, odd_primes, NTOP

class Even:
    def __init__(self, M0):
        self.M0 = M0
        self.cnt = cnt_table(NTOP); self.tail = tail_beyond(NTOP)
        self.OFF = OFF = 2 * NTOP + 8
        c = np.ones(M0 + OFF + 1); c[1 + OFF] = 0.5
        for r in range(2, M0 + 1):
            c[r + OFF] = c[r - 1 + OFF] if r % 2 == 0 else c[r - 1 + OFF] * r / (r + 1)
        self.c = c
        self.pp = []                                   # prime powers (p, j, N*) with N* <= NTOP
        npp = {}
        for p in odd_primes(NTOP):
            j = 1
            while j * (p - 1) + 1 <= NTOP:
                N = j * (p - 1) + 1; self.pp.append((p, j, N)); npp[N] = npp.get(N, 0) + 1; j += 1
        self.cnt_comp = {N: self.cnt[N] - npp.get(N, 0) for N in self.cnt}
        assert all(v >= 0 for v in self.cnt_comp.values())
        self.s2pi = math.sqrt(2 / math.pi)
    def cc(self, x):
        return self.c[np.maximum(x, -self.OFF) + self.OFF]
    def gamma(self, m, N):
        r = np.arange(1, (m - 1) // 2 + 1)
        return float(np.max(2 * self.cc(r) * self.cc(np.maximum(m - 2 * r, r) - 2 * (N - 3))))
    def LC(self, m, N):
        if N > m: return 0.0
        key = (m, N)
        if key not in self._lc: self._lc[key] = 2.0 ** -(N - 2) * self.gamma(m, N)
        return self._lc[key]
    def Fb(self, m, p, k, g):
        N = k + p - 1
        if N > m: return 0.0
        s = np.arange(0, m - (-(-m // (p * k))) + 1)
        v = self.cc(m - s) * np.minimum(g, 2 * self.cc((s + 1) // 2 - 2 * (N - 3)))
        return 2.0 ** -(N - 2) * float(np.max(v))
    def PPE(self, m, p, j):
        G = 1 + (j - 1) * (p - 1)
        if p >= 11: return self.LC(m, G + p - 1)
        q = max(2, p - 2); best = self.LC(m, G + q + p - 1)
        for k in range(G, G + q):
            g = 17 / 64 if (p, j, k) == (3, 1, 1) else 2.0 ** -(p - 2)
            best = max(best, min(self.LC(m, k + p - 1), self.Fb(m, p, k, g)))
        return best
    def BE(self, m, parts=False):
        assert m % 2 == 0 and m <= self.M0
        self._lc = {}
        lvl0 = float(self.c[m + self.OFF])
        comp = sum(self.cnt_comp[N] * self.LC(m, N) for N in self.cnt_comp if N <= m and self.cnt_comp[N])
        pp = sum(self.PPE(m, p, j) for (p, j, N) in self.pp if N <= m)
        tl = self.s2pi / math.sqrt(m) * self.tail if m > NTOP else 0.0
        return (lvl0, comp, pp, tl) if parts else lvl0 + comp + pp + tl

def main():
    M0 = int(sys.argv[1]); E = Even(M0); rows = []
    for m in range(2, M0 + 1, 2):
        a, b, c_, d = E.BE(m, parts=True); t = a + b + c_ + d
        rows.append((m, t, t * math.sqrt(m)))
        if m <= 120 or m % 200 == 0:
            print(f"m = {m:5d}  level 0 {a:.6f}  composite {b:.6f}  prime powers {c_:.6f}  B_E(m) = {t:.6f}  sqrt(m) B_E(m) = {t * math.sqrt(m):.5f}")
    for lo in (2, 22, 28, 48, 62, 112, 300, 1000):
        v, m = max((v, m) for m, t, v in rows if m >= lo)
        print(f"largest sqrt(m) B_E(m) over even m in [{lo}, {M0}]: {v:.6f} at m = {m}")
    # m > M0: the d* = 3 and 9 refined, every other d* as in bound.py (NA = 21)
    NA = 21; s2pi = E.s2pi; cnt = E.cnt
    f1 = math.sqrt(M0 / (M0 - 2 * NA + 2))
    f2 = 0.75 * math.sqrt(M0 / (7 * M0 / 9 - 2 * NA + 6)); f3 = 2 * s2pi * 3 / math.sqrt(M0 / 9 - 2 * NA + 6)
    assert f2 <= f1 and f3 <= f1
    h = math.sqrt(8 / 7)
    def far(p, k, N):      # the part s > m/8 of Fb, times sqrt(m) 2^(N-2) / sqrt(2/pi)
        return 2 * math.sqrt(2 * p * k / math.pi) / math.sqrt(M0 / 16 - 2 * (N - 3))
    t3 = max(0.5 * max(17 / 64 * h, far(3, 1, 3)), 0.25 * max(0.5 * h, far(3, 2, 4)), 0.125 * f1)
    t9 = max(0.125 * max(0.5 * h, far(3, 3, 5)), 0.0625 * max(0.5 * h, far(3, 4, 6)), 2.0 ** -5 * f1)
    sA = sum(cnt[N] * 2.0 ** -(N - 2) for N in cnt if N <= NA) - 0.5 - 0.125
    sB = sum(cnt[N] * math.sqrt(N) * 2.0 ** -(N - 2) for N in cnt if N > NA)
    print(f"m > {M0}: far parts {far(3, 1, 3):.4f} {far(3, 2, 4):.4f} {far(3, 3, 5):.4f} {far(3, 4, 6):.4f};  the terms of 3 and 9 (times sqrt(m)/sqrt(2/pi)): {t3:.6f}, {t9:.6f}")
    print(f"for every even m > {M0}: sqrt(m) beta(m) <= {s2pi * (1 + t3 + t9 + f1 * sA + sB + E.tail):.6f}")

if __name__ == '__main__':
    main()
