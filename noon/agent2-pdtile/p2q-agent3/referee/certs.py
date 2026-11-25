"""Lemmas 1 and 2 of p2q-agent3.md, re-checked from scratch for a list of prime pairs.

For each (p, q), M = p^2 q:
  * the sets T_p, T_{p^2}, T_q, all A_S (S subset of {p,p^2,q}), the subgroups of order p, q, p^2, pq,
    T_p+T_q: exact zero sets (integer residues mod Phi_d)
  * the difference-avoiding sets of Lemma 2(e),(f): sizes and the orders of ALL pairwise differences
  * exact D+ (vertex enumeration over Q) of U(S), of the six patterns of Lemma 2, of all 32 patterns;
    cross-check with scipy linprog
  * the side claims of the Remarks / Section 4 (D+ >= 2k for which Case-2 patterns; non-closed patterns
    with D+ >= k; how many of the 17 bounds are tight)
"""
import sys
from fractions import Fraction
from itertools import combinations
import numpy as np
import core

pairs = [(2, 3), (3, 2), (2, 5), (5, 2), (3, 5), (5, 3), (2, 7), (7, 2), (3, 7), (7, 3), (5, 7), (7, 5),
         (3, 11), (11, 3), (2, 11), (11, 2), (2, 13), (13, 2), (3, 13), (5, 11), (11, 5), (7, 11), (5, 29),
         (3, 29), (2, 29), (7, 53)]
if len(sys.argv) > 1:
    pairs = [tuple(map(int, a.split(","))) for a in sys.argv[1:]]

tot_fail = 0
tight_counts = []
for p, q in pairs:
    M = p * p * q
    O = [p, p * p, q, p * q, p * p * q]
    nm = {p: "p", p * p: "p2", q: "q", p * q: "pq", p * p * q: "p2q"}
    fails = []

    def el(u, w):
        return core.crt_pair(u, w, p * p, q)

    def zs(A):
        A = list(A)
        assert len(set(A)) == len(A)
        return core.zero_set(M, A)

    def U(S):
        out = set()
        if p in S:
            out |= {p, p * q}
        if p * p in S:
            out |= {p * p, p * p * q}
        if q in S:
            out |= {q, p * q, p * p * q}
        return out

    def k(Z):
        return p ** len(set(Z) & {p, p * p}) * q ** len(set(Z) & {q})

    Tp = [el(u, 0) for u in range(p)]
    Tp2 = [el(i * p, 0) for i in range(p)]
    Tq = [el(0, w) for w in range(q)]
    T = {p: Tp, p * p: Tp2, q: Tq}
    # --- Lemma 1 sets
    if not zs(Tp) >= {p, p * q}:
        fails.append("T_p zeros")
    if zs(Tp2) != {p * p, p * p * q}:
        fails.append("T_p2 zeros")
    if zs(Tq) != {q, p * q, p * p * q}:
        fails.append("T_q zeros")
    # T_p2, T_q are the subgroups of order p, q?
    if sorted(Tp2) != [i * (M // p) for i in range(p)]:
        fails.append("T_p2 not the subgroup of order p")
    if sorted(Tq) != [i * (M // q) for i in range(q)]:
        fails.append("T_q not the subgroup of order q")
    exact_dp = {}

    def dp(Z):
        key = frozenset(Z)
        if key not in exact_dp:
            v = core.dplus_exact(M, key)
            f = core.dplus_float(M, key)
            if abs(float(v) - f) > 1e-6:
                fails.append(f"exact/float D+ mismatch {sorted(key)} {v} {f}")
            exact_dp[key] = v
        return exact_dp[key]

    bounds = []    # (name, pattern, bound)
    for r in range(4):
        for S in combinations([p, p * p, q], r):
            AS = [0]
            for s in S:
                AS = [(a + t) % M for a in AS for t in T[s]]
            if len(set(AS)) != k(S):
                fails.append(f"A_S not direct / wrong size S={S}")
            if not zs(AS) >= U(S):
                fails.append(f"A_S zeros S={S}")
            bounds.append((f"L1 S={{{','.join(nm[s] for s in S)}}}", U(S), k(S)))
    # --- Lemma 2 (S)-certificates: subgroups
    for h, name in [(p, "p"), (q, "q"), (p * p, "p2"), (p * q, "pq")]:
        H = [i * (M // h) for i in range(h)]
        want = {d for d in O if (M // h) % d != 0}
        if zs(H) != want:
            fails.append(f"subgroup of order {name}: zeros {sorted(zs(H))} != {sorted(want)}")
    TpTq = [(a + b) % M for a in Tp for b in Tq]
    if len(set(TpTq)) != p * q or zs(TpTq) != {p, q, p * q, p * p * q}:
        fails.append("T_p+T_q")
    Hq = [i * (M // q) for i in range(q)]
    Hp = [i * (M // p) for i in range(p)]
    Hp2 = [i * (M // (p * p)) for i in range(p * p)]
    Hpq = [i * (M // (p * q)) for i in range(p * q)]
    cert = [
        ("L2a via subgroup pq", {p * p, p * q, p * p * q}, Hpq),
        ("L2a via subgroup p2", {p * p, p * q, p * p * q}, Hp2),
        ("L2b via Tp+Tq", {p, p * q, p * p * q}, TpTq),
        ("L2b via subgroup p2", {p, p * q, p * p * q}, Hp2),
        ("L2c via subgroup q", {p * q, p * p * q}, Hq),
        ("L2d via subgroup q", {p * p * q}, Hq),
        ("L2d via subgroup p", {p * p * q}, Hp),
    ]
    for name, Z, A in cert:
        if not zs(A) >= Z:
            fails.append(name + ": zero set does not contain the pattern")
        bounds.append((name, Z, len(A)))
    # --- Lemma 2 (C)-certificates
    t = min(p, q)
    Be = [el(c + i * p, i) for c in range(p) for i in range(t)]
    Bf = [el(c + i * p, c) for c in range(t) for i in range(p)]
    for name, B, Z, claimed in [("L2e", Be, {p, q}, {p * p, p * q, p * p * q}), ("L2f", Bf, {p * p, q, p * q}, {p, p * p * q})]:
        if len(set(B)) != p * t:
            fails.append(name + " size")
        orders = {core.order(x - y, M) for x, y in combinations(B, 2)}
        if orders & Z:
            fails.append(f"{name}: a difference has an order in the pattern: {sorted(orders & Z)}")
        if not orders <= claimed:
            fails.append(f"{name}: difference orders {sorted(orders)} not within the claimed {sorted(claimed)}")
        bounds.append((name, Z, Fraction(M, len(B))))
        if Fraction(M, len(B)) != max(p, q):
            fails.append(name + " bound != max(p,q)")
    # stated values of the six bounds
    stated = [({p * p, p * q, p * p * q}, p * min(p, q)), ({p, p * q, p * p * q}, p * min(p, q)),
              ({p * q, p * p * q}, q), ({p * p * q}, min(p, q)), ({p, q}, max(p, q)), ({p * p, q, p * q}, max(p, q))]
    for Z, b in stated:
        if dp(Z) > b:
            fails.append(f"LEMMA 2 BOUND VIOLATED {sorted(Z)}: D+={dp(Z)} > {b}")
    ntight = 0
    for name, Z, b in bounds:
        d = dp(Z)
        if d > b:
            fails.append(f"BOUND VIOLATED {name}: D+={d} > {b}")
        ntight += (d == b)
    tight_counts.append(ntight)
    # --- all 32 patterns: monotone; Case-2 patterns; non-closed patterns
    allpat = [frozenset(c) for r in range(6) for c in combinations(O, r)]
    for Z in allpat:
        for d in O:
            if d not in Z and dp(Z | {d}) < dp(Z):
                fails.append("monotonicity")
    case2 = [Z for Z in allpat if not Z <= U(Z & {p, p * p, q})]
    big = [Z for Z in case2 if dp(Z) >= 2 * k(Z)]
    small = [Z for Z in case2 if dp(Z) < 2 * k(Z)]
    nonclosed = [Z for Z in allpat if (p in Z and q in Z and p * q not in Z) or (p * p in Z and q in Z and p * p * q not in Z)]
    nc_big = [Z for Z in nonclosed if dp(Z) >= k(Z)]

    def fmt(Z):
        return "{" + ",".join(nm[d] for d in O if d in Z) + "}"

    # the theorem at pattern level: patterns that could carry a pd-tiling set violating T1/T2 by D+ and k alone
    danger = [Z for Z in allpat if dp(Z).denominator == 1 and dp(Z) % k(Z) == 0 and (Z in case2 or Z in nonclosed or dp(Z) != k(Z))]
    print(f"(p,q)=({p},{q}) M={M}: {len(bounds)} bounds, {ntight} tight; #case2={len(case2)}; "
          f"case2 with D+<2k: {[fmt(Z)+'='+str(dp(Z)) for Z in small]}; "
          f"non-closed with D+>=k: {[fmt(Z)+'='+str(dp(Z)) for Z in nc_big]}; "
          f"patterns not excluded by (D+ integer, k | D+) alone: {[fmt(Z)+'='+str(dp(Z)) for Z in danger]}; "
          f"{'OK' if not fails else 'FAILS: ' + '; '.join(fails)}")
    print("     case2 D+: " + ", ".join(f"{fmt(Z)}:{dp(Z)}(k={k(Z)})" for Z in case2))
    print("     Lemma 2 D+ vs bound: " + ", ".join(f"{fmt(Z)}:{dp(Z)}<={b}" for Z, b in stated))
    tot_fail += len(fails)
print("tight counts per pair:", tight_counts)
print("TOTAL FAILS:", tot_fail)
