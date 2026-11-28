# Recursion for the tree of a prime p (exact integers): \hat E_p(m)*2^m, m <= M.  usage: recp.py p M
import sys, math
from math import comb
from fractions import Fraction
def table(p, M):
    binom = [[comb(r, j) for j in range(r + 1)] for r in range(M + 1)]
    c = [binom[r][r // 2] if r % 2 == 0 else 0 for r in range(M + 1)]
    E = [0] * (M + 1); U = c[:]; arg = [None] * (M + 1)
    def parts(m, k, lo):          # partitions of m into k parts, each >= lo, nondecreasing
        if k == 1:
            if m >= lo: yield (m,)
            return
        for a in range(lo, m // k + 1):
            for rest in parts(m - a, k - 1, a): yield (a,) + rest
    for m in range(3, M + 1):
        best = 0; ba = None
        for k in range(2, min(p, m) + 1):
            for rs in parts(m, k, 1):
                pu = 1; pc = 1
                for r in rs: pu *= U[r]; pc *= c[r]
                t = pu - pc
                if p == 3 and k == 2 and rs[0] in (3, 5, 7) and rs[1] in (3, 5, 7): t = E[rs[0]] * E[rs[1]] // 2
                if k == p and all((r - rs[0]) % 2 == 0 for r in rs):
                    g = 0
                    for v in range(2 - rs[0] % 2, rs[0] + 1, 2):
                        q = 1
                        for r in rs: q *= binom[r][(r + v) // 2]
                        g += q
                    t += 2 * g
                if t > best: best = t; ba = rs
        E[m] = best; U[m] = c[m] + best; arg[m] = ba
    return E, U, c, arg
if __name__ == "__main__":
    p = int(sys.argv[1]); M = int(sys.argv[2])
    E, U, c, arg = table(p, M)
    kap = math.sqrt(2 / math.pi)
    print(f"p={p}: E_p(m) for m={p}..{min(M, p + 11)}:", [str(Fraction(E[m], 1 << m)) for m in range(p, min(M, p + 11) + 1)])
    for par in (0, 1):
        ms = [m for m in range(p, M + 1) if m % 2 == par]
        me = max(ms, key=lambda m: E[m] / (1 << m) * math.sqrt(m))
        print(f"  parity {par}: max E_p(m)*sqrt(m) over {p} <= m <= {M}: {E[me] / (1 << me) * math.sqrt(me):.6f} at m={me}, split {arg[me]};"
              f" at m={ms[-1]}: {E[ms[-1]] / (1 << ms[-1]) * math.sqrt(ms[-1]):.6f}, split {arg[ms[-1]]}")
    print(f"  analytic constant of result.md: tau_p = kappa*sqrt(p)*2^(2-p) = {kap * math.sqrt(p) * 2.0 ** (2 - p):.6f}")
