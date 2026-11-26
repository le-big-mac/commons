"""How many subsets of Z_18 and Z_12 does the sharp bound apply to, and in how many of those does q divide |A|?
usage: python -I sharp-count-agent2.py > sharp-count-agent2.out      (numpy)      Noon, 26 November 2026.
For M = p^n q: E = {l in 1..n : Phi_{p^l} | A}, F = {l in 0..n : Phi_{p^l q} | A}; Phi_d | A exactly when the Fourier
coefficient of A at M/d vanishes. The sharp bound's hypotheses are: 0 not in F (Phi_q does not divide A) and at least
one level in F \\ E. A reader derived the bound from a proof of Malikiosis (2022) when q does not divide |A|; this
counts the cases that derivation does not reach, and checks the bound p^e (p^k + q) <= |A| on all of them."""
import sys
sys.dont_write_bytecode = True
import numpy as np

if __name__ == '__main__':
    for p, q, n in ((3, 2, 2), (2, 3, 2)):
        M = p ** n * q
        bits = ((np.arange(2 ** M)[:, None] >> np.arange(M)) & 1).astype(float)
        ft = np.abs(np.fft.fft(bits, axis=1)); size = bits.sum(1).astype(int)
        zero = lambda d: ft[:, M // d] < 1e-9
        E = np.stack([zero(p ** l) for l in range(1, n + 1)], 1)                    # levels 1..n
        F = np.stack([zero(p ** l * q) for l in range(0, n + 1)], 1)                # levels 0..n
        k = (F[:, 1:] & ~E).sum(1); e = E.sum(1)
        app = ~F[:, 0] & (k >= 1) & (size > 0)
        bound = p ** e * (p ** k + q)
        print(f"Z_{M} (p = {p}, q = {q}): subsets with Phi_q not dividing A and at least one level in F \\ E: {int(app.sum())};"
              f" of those with q dividing |A|: {int((app & (size % q == 0)).sum())};"
              f" the bound p^e (p^k + q) <= |A| fails in {int((app & (size < bound)).sum())} and is attained in {int((app & (size == bound)).sum())}"
              f" (of which with q dividing |A|: {int((app & (size == bound) & (size % q == 0)).sum())})")
