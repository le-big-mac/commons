"""Section 4 (Constructions), built from the paper's words alone.

For every pattern (E, F, balanced or not) with n <= NMAX and the given (p, q):
  build A as Section 4 says, compute its exact pattern from the tree definitions and (option) by
  exact division of the mask polynomial, and its size; compare with the pattern asked for and with
  the formula of Theorem 1.
usage: t6_constructions.py p q nmax [poly]
"""
import sys, itertools
import numpy as np
from lib import root_pattern, poly_pattern, theorem_value, all_patterns, clauses, class_vectors, is_constant


def digit(u, a, p):
    """digit of level a of the string u = sum u_a p^(a-1)"""
    return (u // p ** (a - 1)) % p


def D(T, p, n):
    """strings whose digits are 0 outside T"""
    return [u for u in range(p ** n) if all(digit(u, a, p) == 0 for a in range(1, n + 1) if a not in T)]


def Dmap(T, b, c, p, n):
    """D(T; b -> c): strings with u_b = c and 0 at the other levels outside T"""
    assert b not in T
    return [u for u in range(p ** n) if digit(u, b, p) == c and
            all(digit(u, a, p) == 0 for a in range(1, n + 1) if a not in T and a != b)]


def Fib(Dset, p, q, n, m=1):
    A = np.zeros((p ** n, q), dtype=np.int64)
    for u in Dset:
        A[u, :] += m
    return A


def unbalanced(p, q, n, E, F):
    EmF = E - F
    def tau(u):
        return 1 if (EmF and all(digit(u, a, p) != 0 for a in EmF)) else 0
    A = np.zeros((p ** n, q), dtype=np.int64)
    for u in D(E | F, p, n):
        A[u, tau(u)] += 1
    if not F <= E:
        A = A + Fib(D(E, p, n), p, q, n)
    return A


def shape_part(p, q, n, a0, T1, T2, H, mode):
    assert T1 <= set(range(1, a0)) and H <= T2 and T2 <= set(range(a0 + 1, n + 1)) and mode in "UQW"
    Dstar = D(set(T1) | {a0} | set(T2), p, n)
    def tau(u):
        return 1 if (H and all(digit(u, a, p) != 0 for a in H)) else 0
    one = np.ones(q, dtype=np.int64)
    def delta(x):
        return x - np.roll(x, 1)           # (Delta x)(w) = x(w) - x(w-1)
    def lam(i, x):
        tot = int(x.sum())
        if mode == "U":
            if i == 0:
                return x
            if i == 1:
                return tot * one - x
            return None
        if i == 0:
            return tot * one + delta(x)
        if i == 1:
            return tot * one - delta(x)
        if mode == "Q" and 2 <= i <= p - 1:
            return tot * one
        return None
    S = np.zeros((p ** n, q), dtype=np.int64)
    for u in Dstar:
        e = np.zeros(q, dtype=np.int64)
        e[tau(u)] = 1
        v = lam(digit(u, a0, p), e)
        if v is not None:
            assert (v >= 0).all()
            S[u] += v
    return S


def balanced(p, q, n, E, F, force=None):
    """returns (A, case label).  Cases in the order printed: (I), (III), (IV), (V), (II)."""
    full = set(range(1, n + 1))
    if F == full:
        return Fib(D(E, p, n), p, q, n), "F=[1,n]"
    a0 = min(full - F)
    G = {a for a in F - E if a > a0}
    kp = len(G)
    T20 = {a for a in E | F if a > a0}
    H0 = {a for a in E - F if a > a0}
    mode0 = "Q" if a0 in E else "U"
    Elt = {a for a in E if a < a0}
    between = [a for a in sorted(E - F) if kp >= 1 and a0 < a < min(G)]
    if force is None:
        if kp == 0:
            case = "I"
        elif Elt:
            case = "III"
        elif a0 in E and p >= 3:
            case = "IV"
        elif a0 in E and between:
            case = "V"
        else:
            case = "II"
    else:
        case = force
    if case == "I":
        A = shape_part(p, q, n, a0, Elt, T20, H0, mode0)
    elif case == "III":
        b = min(E)
        A = shape_part(p, q, n, a0, Elt - {b}, T20, H0, mode0)
        for i in range(1, p):
            A = A + Fib(Dmap(E - {b}, b, i, p, n), p, q, n, p ** kp)
    elif case == "IV":
        A = shape_part(p, q, n, a0, Elt, T20, H0, "W")
        for i in range(2, p):
            A = A + Fib(Dmap(E - {a0}, a0, i, p, n), p, q, n, p ** kp)
    elif case == "V":
        b = between[0]
        A = shape_part(p, q, n, a0, Elt, T20 - {b}, H0 - {b}, "Q")
        for i in range(1, p):
            A = A + Fib(Dmap(E - {b}, b, i, p, n), p, q, n, p ** kp)
    else:
        A = shape_part(p, q, n, a0, Elt, T20, H0, mode0) + Fib(D(E, p, n), p, q, n)
    return A, case


def main():
    p, q, nmax = map(int, sys.argv[1:4])
    use_poly = len(sys.argv) > 4
    tot = bad = 0
    bycase = {}
    for n in range(0, nmax + 1):
        nb = 0
        for E, F, bal in all_patterns(n):
            E, F = set(E), set(F)
            if bal:
                A, case = balanced(p, q, n, E, F)
                # "Cases (I), (III), (IV), (V) are clauses (1) to (4), and (II) is reached exactly when x = 1"
                cl = clauses(p, q, n, E, F)
                if cl is not None:
                    first = ["I", "III", "IV", "V"][cl.index(True)] if any(cl) else "II"
                    assert first == case, (E, F, cl, case)
            else:
                A, case = unbalanced(p, q, n, E, F), "unbalanced"
            got = root_pattern(A, p, n)
            ok = got == (frozenset(E), frozenset(F), bal)
            if use_poly:
                gp = poly_pattern(A, p, n)
                if gp != got:
                    print("   TREE AND DIVISION DISAGREE", p, q, n, sorted(E), sorted(F), bal)
                    ok = False
            size = int(A.sum())
            want = theorem_value(p, q, n, E, F, bal)
            ok = ok and size == want
            tot += 1
            c = bycase.setdefault(case, [0, 0])
            c[0] += 1
            if not ok:
                bad += 1
                nb += 1
                c[1] += 1
                print(f"   FAIL p={p} q={q} n={n} E={sorted(E)} F={sorted(F)} balanced={bal} case={case}: "
                      f"got pattern {sorted(got[0])},{sorted(got[1])},{got[2]} size {size}, formula {want}")
        print(f"p={p} q={q} n={n}: {2**(2*n+1)} patterns built, failures {nb}" + (" (pattern by tree and by exact division)" if use_poly else " (pattern by tree)"))
    print(f"p={p} q={q} n<={nmax}: total {tot}, failures {bad}; by case (built, failed): {bycase}")


if __name__ == "__main__":
    main()
