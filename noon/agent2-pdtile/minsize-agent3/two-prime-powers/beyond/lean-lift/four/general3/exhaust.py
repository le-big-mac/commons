"""Every multiset of at most mmax elements that contains 0, on a small group Z_n; all signings.

(The property "Phi_d divides the signed mask" is invariant under translation of the multiset, so 0 in B is no loss.)
Checks, for each multiset B (m elements) with canonical contraction (B_flat, n_flat):
  (a) good for B_flat  =>  good for B                      (Lemma 2 / Proposition 3 of the note)
  (b) for every d | n_flat, d > 1: fraction of signings with Phi_d | S  <=  2^(-mu(d))       (level bound)
  (c) fraction of bad signings of B_flat <= c_m + sum over d | n_flat, d > 1 of 2^(-mu(d))    (union bound)
  (e) B has a good signing at all (the statement on signs), and the least fraction of good signings.
Also asserted for each: every level of every tree of B_flat has a full group.

usage: exhaust.py n mmax
"""
import sys
from itertools import combinations_with_replacement
from fractions import Fraction as Fr
import numpy as np
from lib4 import divisors, mu, all_signs, bad_table, contract, c_even, all_full


def main():
    n = int(sys.argv[1]); mmax = int(sys.argv[2])
    Es = {m: all_signs(m) for m in range(1, mmax + 1)}
    for m in range(1, mmax + 1):
        E = Es[m]
        tot = E.shape[0]
        cnt = viol_a = viol_b = viol_c = nogood = 0
        full = 0
        least = Fr(1); least_at = None
        tight_c = Fr(0)
        for rest in combinations_with_replacement(range(n), m - 1):
            B = [0] + list(rest)
            Bf, nf = contract(B, n)
            assert all_full(Bf, nf)        # (2) of section 1 of the result file
            tabF = bad_table(Bf, nf, E)
            badF = np.zeros(tot, dtype=bool)
            bound = c_even(m)
            for d, b in tabF.items():
                badF |= b
                if d > 1:
                    bound += Fr(1, 2 ** mu(d))
                    if int(b.sum()) * 2 ** mu(d) > tot:
                        viol_b += 1
            if nf != n:
                badB = np.zeros(tot, dtype=bool)
                for d, b in bad_table(B, n, E).items():
                    badB |= b
                if (badB & ~badF).any():
                    viol_a += 1
            else:
                badB = badF
                full += 1
            fb = Fr(int(badF.sum()), tot)
            if fb > bound:
                viol_c += 1
            if bound > 0:
                tight_c = max(tight_c, fb / bound)
            gB = 1 - Fr(int(badB.sum()), tot)
            if gB == 0:
                nogood += 1
            if gB < least:
                least = gB; least_at = B
            cnt += 1
        print(f"n={n} m={m}: multisets with 0: {cnt} ({full} with n_flat = n); violations (a) {viol_a}, (b) {viol_b}, (c) {viol_c}; "
              f"without a good signing: {nogood}; least fraction of good signings {least} at {least_at}; "
              f"largest bad/bound {float(tight_c):.4f}", flush=True)


main()
