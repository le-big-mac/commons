"""Second look: where is Lemma E attained, and is E1 (case (b)) ever attained?
All multisets containing 0 on Z_n with even m in the given range; for every fully live d with one prime and bad
signings: the case ((a): some full cell with odd classes; (b): every class of every cell even), and whether
P = E2, P = E1, P = max(E1, E2); also the largest P/E1 in case (b).
usage: scan_e.py N MMAX"""
import sys, math
from fractions import Fraction as Fr
from eng import *
from tests import multisets_with_zero
n = int(sys.argv[1]); mmax = int(sys.argv[2])
cnt = dict(a=0, b=0, a_eqE2=0, a_eqmax=0, b_eqE1=0, b_eqmax=0, other=0); best = (Fr(0), None)
for m in range(2, mmax + 1, 2):
    for ms in multisets_with_zero(n, m):
        res = sorted(ms); FL = [f for f in fully_live(n, res) if len(f['fd']) == 1]
        if not FL: continue
        T, w = grid([ms[b] for b in res])
        for f in FL:
            d = f['d']; fl = ~(T @ redmat(n, d)[res]).any(axis=1)
            if not fl.any(): continue
            P = Fr(int(w[fl].sum()), 2 ** m)
            q = f['q']; kap = f['kap']; d0 = f['d0']
            E1 = Fr(3, 4) * Fr(1, 2 ** (kap - 1)) * cstar(m - 2 * kap) if m >= 2 * kap + 2 else Fr(0)
            E2 = Fr(1, 2 ** (kap + q - 3)) * cstar(m - 2 * kap - 2 * q + 6)
            # sizes of the classes of every cell (class of b: (b mod d0, ((b - b mod d0)/d0) mod q))
            sizes = {}
            for b in res:
                c_ = b % d0; key = (c_, ((b - c_) // d0) % q); sizes[key] = sizes.get(key, 0) + ms[b]
            alleven = all(v % 2 == 0 for v in sizes.values())
            if alleven:
                cnt['b'] += 1
                if P == E1: cnt['b_eqE1'] += 1
                if P == max(E1, E2): cnt['b_eqmax'] += 1
                if E1 > 0 and P / E1 > best[0]: best = (P / E1, (m, dict(ms), d))
                if P > E1: cnt['other'] += 1          # would contradict the proof of case (b)
            else:
                cnt['a'] += 1
                if P == E2: cnt['a_eqE2'] += 1
                if P == max(E1, E2): cnt['a_eqmax'] += 1
                if P > E2: cnt['other'] += 1          # would contradict the proof of case (a)
print(f"Z_{n}, even m <= {mmax}: divisors with one prime and bad signings: case (a) {cnt['a']} (P = E2 in {cnt['a_eqE2']}, P = max(E1, E2) in {cnt['a_eqmax']}); "
      f"case (b) {cnt['b']} (P = E1 in {cnt['b_eqE1']}, P = max(E1, E2) in {cnt['b_eqmax']}); against the case bounds: {cnt['other']}; largest P/E1 in case (b): {float(best[0]):.4f} at {best[1]}")
