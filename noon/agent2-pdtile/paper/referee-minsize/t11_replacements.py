"""Checks of two statements that the referee's report proposes as replacement text.
(a) Host level h in cases (III), (IV), (V): S and each fibre multiset meet the same classes of depth h-1,
    namely those whose digits are 0 outside E, and in each of them every child has q p^(|E n (h,n]| + k') elements.
(b) Shape part, level a in H: in the class of depth a-1 with digit 1 at the levels of H before a and 0 elsewhere,
    the child with digit 0 has beta = p^h e_0 and the child with digit 1 has beta = (p^h - t) e_0 + t e_1, t >= 1,
    h = |T2 n (a,n]|; and the S-vectors of these two children do not differ by a constant, in every mode."""
import itertools
import numpy as np
from lib import class_vectors, children, is_constant, subsets
from t6_constructions import digit, D, shape_part, balanced

def sub(s):
    s = sorted(s)
    for r in range(len(s) + 1):
        for c in itertools.combinations(s, r):
            yield set(c)

ta = fa = 0
for (p, q, nmax) in [(2, 3, 5), (3, 2, 4), (2, 5, 4), (5, 2, 3), (3, 5, 3)]:
    for n in range(2, nmax + 1):
        full = set(range(1, n + 1))
        for E in sub(full):
            for F in sub(full):
                if F == full: continue
                a0 = min(full - F); G = {a for a in F - E if a > a0}; kp = len(G)
                A, case = balanced(p, q, n, E, F)
                if case not in ("III", "IV", "V"): continue
                if case == "III":
                    h = min(E)
                elif case == "IV":
                    h = a0
                else:
                    h = min(a for a in E - F if a0 < a < min(G))
                want = q * p ** (len({a for a in E if a > h}) + kp)
                vprev = class_vectors(A, p, n, h - 1); vch = class_vectors(A, p, n, h)
                ok = True
                for c in range(p ** (h - 1)):
                    zero_outside_E = all(digit(c, a, p) == 0 for a in range(1, h) if a not in E)
                    tots = [int(vch[k].sum()) for k in children(c, p, h - 1)]
                    if zero_outside_E:
                        ok = ok and all(t == want for t in tots)
                    else:
                        ok = ok and vprev[c].sum() == 0
                ta += 1; fa += (not ok)
print(f"(a) host-level statement: patterns in cases (III), (IV), (V): {ta}, failures {fa}")

tb = fb = 0
for (p, q, nmax) in [(2, 3, 4), (3, 2, 4), (2, 5, 4), (5, 2, 3), (3, 5, 3)]:
    for n in range(1, nmax + 1):
        for a0 in range(1, n + 1):
            for T2 in sub(range(a0 + 1, n + 1)):
                for H in sub(T2):
                    Dstar = D({a0} | T2, p, n)
                    def tau(u): return 1 if (H and all(digit(u, a, p) != 0 for a in H)) else 0
                    for a in sorted(H):
                        c = sum(p ** (l - 1) for l in H if l < a)      # digit 1 at the levels of H before a, 0 elsewhere
                        hh = len({l for l in T2 if l > a})
                        betas = []
                        for j in (0, 1):
                            cc = c + j * p ** (a - 1)
                            us = [u for u in Dstar if u % p ** a == cc]
                            betas.append((sum(1 for u in us if tau(u) == 0), sum(1 for u in us if tau(u) == 1)))
                        t = betas[1][1]
                        ok = betas[0] == (p ** hh, 0) and t >= 1 and betas[1] == (p ** hh - t, t)
                        for mode in "UQW":
                            S = shape_part(p, q, n, a0, set(), T2, H, mode)
                            v = class_vectors(S, p, n, a)
                            ok = ok and not is_constant(v[c] - v[c + p ** (a - 1)])
                        tb += 1; fb += (not ok)
print(f"(b) level of H: (parameters, level) pairs: {tb}, failures {fb}")
