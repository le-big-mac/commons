"""Referee: explicit sets of Lemma 1 and Lemma 2 (exact), and D+ by floating-point LP.

Part 1 (exact): for every E, zero sets of T_E x Z_q and T_E x {0}; for every admissible (E, F) the set B of
        Lemma 2: size and the order of every pairwise difference. Negative control: B built with the digit
        convention reversed (position l-1 instead of n-l).
Part 2 (LP, float): D+(Z) for every pattern (E, F); check (U1), (U2), Lemma 2's bound.
Part 3 (LP + census from ref_brute.py): end-to-end check of the theorem on every subset containing 0.
"""
import sys, math, itertools, os
import numpy as np
from scipy.optimize import linprog
from refcommon import *


def subsets(items):
    items = list(items)
    for r in range(len(items) + 1):
        for c in itertools.combinations(items, r):
            yield frozenset(c)


def T_E(E, p, n):
    E = sorted(E)
    out = []
    for digs in itertools.product(range(p), repeat=len(E)):
        out.append(sum(d * p ** (l - 1) for d, l in zip(digs, E)))
    return out


def build_B(E, F, p, n, q, reversed_digits=False):
    """Lemma 2's set, built from the text. Returns list of (u, w), and a = max(E \\ F)."""
    a = max(E - F)
    t = min(p, q)
    choices = []            # per digit position i = 0..n-1
    for i in range(n):
        l = (i + 1) if reversed_digits else (n - i)
        if l == a:
            choices.append(list(range(t)))
        elif l > a:
            choices.append(list(range(p)) if (l not in E and l not in F) else [0])
        else:
            choices.append(list(range(p)) if (l not in E) else [0])
    pos_a = (a - 1) if reversed_digits else (n - a)
    B = []
    for digs in itertools.product(*choices):
        u = sum(d * p ** i for i, d in enumerate(digs))
        B.append((u, digs[pos_a] % q))
    return B, a


def part1(p, n, q):
    M = p ** n * q
    fwd, inv = crt_table(p, n, q)
    res = dict(E_patterns=0, U1_ok=0, U2_ok=0, U1_exact=0, U2_exact=0, L2_patterns=0, L2_ok=0, L2_pairs=0,
               L2_rev_bad=0, L2_nohyp_patterns=0, L2_nohyp_validclique=0)
    for E in subsets(range(1, n + 1)):
        res["E_patterns"] += 1
        T = T_E(E, p, n)
        assert len(set(T)) == p ** len(E) and all(0 <= u < p ** n for u in T)
        A1 = [inv[(u, w)] for u in T for w in range(q)]
        A2 = [inv[(u, 0)] for u in T]
        E1, F1 = EF_from_zero_set(zero_set_exact(M, A1), p, n, q)
        E2, F2 = EF_from_zero_set(zero_set_exact(M, A2), p, n, q)
        if E1 >= E and F1 == frozenset(range(0, n + 1)) and len(set(A1)) == p ** len(E) * q:
            res["U1_ok"] += 1
        if E1 == E:
            res["U1_exact"] += 1
        if E2 >= E and F2 >= E and len(set(A2)) == p ** len(E):
            res["U2_ok"] += 1
        if E2 == E and F2 == E:
            res["U2_exact"] += 1
        for F in subsets(range(0, n + 1)):
            if not (E - F):
                continue
            a = max(E - F)
            hyp = not any((l in F and l not in E) for l in range(a + 1, n + 1))
            Z = set(p ** l for l in E) | set(p ** l * q for l in F)
            for rev in (False, True):
                B, a_ = build_B(E, F, p, n, q, reversed_digits=rev)
                xs = [inv[b] for b in B]
                distinct = len(set(xs)) == len(xs)
                bad = 0
                for i1 in range(len(xs)):
                    for i2 in range(i1 + 1, len(xs)):
                        dlt = (xs[i1] - xs[i2]) % M
                        order = M // math.gcd(dlt, M)
                        if order in Z:
                            bad += 1
                if not rev:
                    if 0 in F and hyp:
                        res["L2_patterns"] += 1
                        res["L2_pairs"] += len(xs) * (len(xs) - 1) // 2
                        if distinct and bad == 0 and len(xs) == min(p, q) * p ** (n - len(E)):
                            res["L2_ok"] += 1
                    else:
                        # the difference argument does not use 0 in F nor the side hypothesis; only the count does
                        res["L2_nohyp_patterns"] += 1
                        if distinct and bad == 0:
                            res["L2_nohyp_validclique"] += 1
                else:
                    if 0 in F and hyp and (bad > 0 or not distinct):
                        res["L2_rev_bad"] += 1
    return res


def order_sums(M):
    """R[d][e] = sum over x of order d of cos(2 pi x / e), an integer (Ramanujan sum)."""
    divs = divisors(M)
    R = {}
    for d in divs:
        xs = [x for x in range(M) if M // math.gcd(x, M) == d]
        for e in divs:
            v = sum(math.cos(2 * math.pi * x * (M // e) / M) for x in xs)
            assert abs(v - round(v)) < 1e-7
            R[(d, e)] = int(round(v))
        R[(d, "phi")] = len(xs)
    return divs, R


def dplus(Z, divs, R):
    Z = sorted(Z)
    if not Z:
        return 1.0
    c = [-R[(d, "phi")] for d in Z]
    A_ub = [[-R[(d, e)] for d in Z] for e in divs]
    b_ub = [1.0] * len(divs)
    r = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=[(0, None)] * len(Z), method="highs")
    assert r.status == 0, r.message
    return 1.0 - r.fun


def part2(p, n, q, cache):
    M = p ** n * q
    divs, R = order_sums(M)
    tol = 1e-6
    res = dict(patterns=0, U1_viol=0, U2_app=0, U2_viol=0, U2_tight=0, L2_app=0, L2_viol=0, L2_tight=0,
               L2_nohyp=0, L2_nohyp_boundfails=0, U1_tight=0)
    for E in subsets(range(1, n + 1)):
        for F in subsets(range(0, n + 1)):
            Z = set(p ** l for l in E) | set(p ** l * q for l in F)
            D = dplus(Z, divs, R)
            cache[(E, F)] = D
            e = len(E)
            res["patterns"] += 1
            if D > p ** e * q + tol:
                res["U1_viol"] += 1
            if abs(D - p ** e * q) < tol:
                res["U1_tight"] += 1
            if 0 not in F and F <= E:
                res["U2_app"] += 1
                if D > p ** e + tol:
                    res["U2_viol"] += 1
                if abs(D - p ** e) < tol:
                    res["U2_tight"] += 1
            if 0 in F and (E - F):
                a = max(E - F)
                hyp = not any((l in F and l not in E) for l in range(a + 1, n + 1))
                bnd = p ** e * q / min(p, q)
                if hyp:
                    res["L2_app"] += 1
                    if D > bnd + tol:
                        res["L2_viol"] += 1
                    if abs(D - bnd) < tol:
                        res["L2_tight"] += 1
                else:
                    res["L2_nohyp"] += 1
                    if D > bnd + tol:
                        res["L2_nohyp_boundfails"] += 1
    return res


def part3(p, n, q, cache):
    fn = f"census_{p}_{n}_{q}.npy"
    if not os.path.exists(fn):
        return None
    cen = np.load(fn)
    tol = 1e-6
    res = dict(sets=0, I1_viol=0, pd_sets=0, pd_patterns=set(), concl_fail=0, pd_caseA=0, pd_caseB=0,
               T1T2_sets=0, T1T2_not_pd=0)
    for Eb, Fb, size, cnt in cen.tolist():
        E = frozenset(l for l in range(1, n + 1) if (Eb >> l) & 1)
        F = frozenset(l for l in range(0, n + 1) if (Fb >> l) & 1)
        D = cache[(E, F)]
        res["sets"] += cnt
        if D > size + tol:
            res["I1_viol"] += cnt
        e = len(E)
        t1t2 = (size == p ** e * (q if 0 in F else 1)) and ((0 not in F) or E <= F)
        if t1t2:
            res["T1T2_sets"] += cnt
        if abs(D - size) < tol:
            res["pd_sets"] += cnt
            res["pd_patterns"].add((tuple(sorted(E)), tuple(sorted(F))))
            if 0 not in F:
                ok = (F <= E) and size == p ** e
                res["pd_caseA"] += cnt
            else:
                ok = (E <= F) and size == p ** e * q
                res["pd_caseB"] += cnt
            if not ok:
                res["concl_fail"] += cnt
        elif t1t2:
            res["T1T2_not_pd"] += cnt
    res["pd_patterns"] = len(res["pd_patterns"])
    return res


if __name__ == "__main__":
    cases = [tuple(int(v) for v in s.split(",")) for s in sys.argv[1:]]
    for (p, n, q) in cases:
        M = p ** n * q
        cache = {}
        print(f"p={p} n={n} q={q} M={M}")
        print("  exact sets:", part1(p, n, q), flush=True)
        print("  LP bounds :", part2(p, n, q, cache), flush=True)
        r3 = part3(p, n, q, cache)
        if r3 is not None:
            print("  end-to-end:", r3, flush=True)
