"""Weak-tiling bound D^w against the pd bound D+ for every zero pattern of several cyclic groups (agent3 / Yonder).
After Noon's observation (20 Nov, 08:50 UTC) that the bounds (S) and (C) do not need the complement to be positive definite.
  D+(Z) = M / min{ sum f : f(0) = 1, f >= 0, fhat >= 0, fhat = 0 at characters whose order is neither 1 nor in Z }
  D^w(Z): the same without fhat >= 0.
f may be taken constant on elements of equal order (average over the units), so there is one variable per divisor of M.
The sum over elements of order e of a character of order d is the Ramanujan sum c_e(M/d) = mu(e/g) phi(e) / phi(e/g), g = gcd(e, M/d)."""
import sys, itertools, math
from fractions import Fraction
import numpy as np
from scipy.optimize import linprog
def divisors(n): return [d for d in range(1, n + 1) if n % d == 0]
def phi(n): return sum(1 for k in range(1, n + 1) if math.gcd(k, n) == 1)
def mu(n):
    r = 1; p = 2
    while p * p <= n:
        if n % p == 0:
            n //= p
            if n % p == 0: return 0
            r = -r
        p += 1
    return -r if n > 1 else r
def setup(M):
    D = divisors(M); c = {(d, e): mu(e // math.gcd(e, M // d)) * phi(e) // phi(e // math.gcd(e, M // d)) for d in D for e in D}
    def bound(Z, pd):
        var = D[1:]; obj = [phi(e) for e in var]; A_ub, b_ub, A_eq, b_eq = [], [], [], []
        for d in D[1:]:
            row = [c[(d, e)] for e in var]                       # fhat(d) = 1 + row . f
            if d in Z:
                if pd: A_ub.append([-x for x in row]); b_ub.append(1.0)
            else: A_eq.append(row); b_eq.append(-1.0)
        r = linprog(obj, A_ub=A_ub or None, b_ub=b_ub or None, A_eq=A_eq or None, b_eq=b_eq or None, bounds=[(0, None)] * len(var), method="highs")
        assert r.status == 0, (M, Z, r.message); return M / (1 + r.fun)
    return D, bound
if __name__ == "__main__":
    D, bound = setup(30); Z = {2, 3, 5, 30}
    print(f"M = 30, Z = {sorted(Z)}: D+ = {bound(Z, True):.6f}, D^w = {bound(Z, False):.6f}   (Noon reports 120/19 = {120 / 19:.6f} against 15/2)")
    for M in [int(a) for a in sys.argv[1:]] or [6, 10, 12, 15, 18, 20, 24, 28, 40, 45, 48, 54, 56, 75, 80, 88, 96, 135, 162, 189, 250, 30, 72]:
        D, bound = setup(M); divs = D[1:]; ndiff = 0; worst = 0.0; ex = None; npat = 0
        for m in range(0, len(divs) + 1):
            for Zt in itertools.combinations(divs, m):
                Z = set(Zt); dw, dp = bound(Z, False), bound(Z, True); npat += 1
                assert dw >= dp * (1 - 1e-9)                       # dropping fhat >= 0 can only lower the minimum of sum f, so D^w >= D+
                if dw - dp > 1e-7 * dp:
                    ndiff += 1
                    if dw - dp > worst: worst, ex = dw - dp, (sorted(Z), dw, dp)
        print(f"M = {M:3d}: {npat:5d} patterns; D^w differs from D+ in {ndiff}" + (f"   largest gap at Z = {ex[0]}: D^w = {ex[1]:.4f}, D+ = {ex[2]:.4f}" if ex else ""), flush=True)
