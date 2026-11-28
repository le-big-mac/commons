"""Where is Lemma E attained?  All multisets with 0 on Z_n, even m <= MMAX: list the fully live d with one prime and
P(bad at d) = max(E1, E2), saying which of E1, E2 it is.  usage: find_e.py N MMAX"""
import sys, math
from fractions import Fraction as Fr
from eng import *
from tests import multisets_with_zero
n = int(sys.argv[1]); mmax = int(sys.argv[2]); seen = 0
for m in range(2, mmax + 1, 2):
    for ms in multisets_with_zero(n, m):
        res = sorted(ms); FL = [f for f in fully_live(n, res) if len(f['fd']) == 1]
        if not FL: continue
        T, w = grid([ms[b] for b in res])
        for f in FL:
            d = f['d']; fl = ~(T @ redmat(n, d)[res]).any(axis=1)
            P = Fr(int(w[fl].sum()) if fl.any() else 0, 2 ** m)
            q = f['q']; kap = f['kap']
            E1 = Fr(3, 4) * Fr(1, 2 ** (kap - 1)) * cstar(m - 2 * kap) if m >= 2 * kap + 2 else Fr(0)
            E2 = Fr(1, 2 ** (kap + q - 3)) * cstar(m - 2 * kap - 2 * q + 6)
            if P > 0 and P == max(E1, E2):
                seen += 1
                if seen <= 12: print(f"equality: n = {n} m = {m} multiset {ms} d = {d} e = {f['e']} kappa = {kap} P = {P} E1 = {E1} E2 = {E2}")
print(f"n = {n}, even m <= {mmax}: equalities in Lemma E: {seen}")
