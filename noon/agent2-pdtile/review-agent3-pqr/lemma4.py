"""Lemma 4 and Lemma 5 of agent2's pqr-agent2.md, step by step, on every subset of Z_30 containing 0 that has Phi_30 (agent3 / Yonder).
Input: t1sets.txt (mask, pattern) from census30.c.  Exact rational arithmetic."""
from fractions import Fraction as Fr
import itertools
PR = (2, 3, 5); PAIRS = ((0, 1), (0, 2), (1, 2))
def dc(X):                                             # double centring, exact
    r, c = len(X), len(X[0]); rs = [Fr(sum(row), c) for row in X]; cs = [Fr(sum(X[i][j] for i in range(r)), r) for j in range(c)]; m = Fr(sum(map(sum, X)), r * c)
    return [[X[i][j] - rs[i] - cs[j] + m for j in range(c)] for i in range(r)]
def lines_only(X):                                     # union of full rows, or union of full columns
    return all(len(set(row)) == 1 for row in X) or all(len({X[i][j] for i in range(len(X))}) == 1 for j in range(len(X[0])))
n_sets = 0; stat = dict(a_fail=0, a_cases=0, b_cases_pair=0, b_cases_empty=0, b_fail=0, T_nonzero=0, L5_cases=0, L5_fail=0, V2_cases=0, V2_fail=0, T_int_fail=0)
for line in open("t1sets.txt"):
    mask, pat = map(int, line.split()); n_sets += 1
    a = {(r % 2, r % 3, r % 5): 1 for r in range(30) if mask >> r & 1}; n = len(a)
    E = {x for x in range(3) if pat >> x & 1}; P = {PAIRS[q] for q in range(3) if pat >> (3 + q) & 1}
    for z in range(3):
        x, y = [w for w in range(3) if w != z]
        def cell(i, j, c):
            t = [0, 0, 0]; t[x], t[y], t[z] = i, j, c; return a.get(tuple(t), 0)
        slices = [[[cell(i, j, c) for j in range(PR[y])] for i in range(PR[x])] for c in range(PR[z])]
        Ts = [dc(S) for S in slices]; stat["a_cases"] += 1
        if any(T != Ts[0] for T in Ts): stat["a_fail"] += 1; continue
        T = Ts[0]; N = [[sum(S[i][j] for S in slices) for j in range(PR[y])] for i in range(PR[x])]
        if dc(N) != [[PR[z] * v for v in row] for row in T]: stat["a_fail"] += 1
        zero = all(v == 0 for row in T for v in row); stat["T_nonzero"] += not zero
        pair_in = (x, y) in P; empty = any(not any(map(any, S)) for S in slices)
        stat.setdefault('empty_cases', 0); stat['empty_cases'] += empty
        stat.setdefault('U_fail', 0); stat['U_fail'] += (empty and not pair_in)
        if pair_in or empty:
            stat["b_cases_pair"] += pair_in; stat["b_cases_empty"] += (empty and not pair_in)
            if not zero or not all(lines_only(S) for S in slices): stat["b_fail"] += 1
        if n == PR[x] * PR[y] and x in E and y in E:
            stat["L5_cases"] += 1
            if any(v.denominator != 1 for row in T for v in row): stat["T_int_fail"] += 1
            if not pair_in: stat["L5_fail"] += 1
        # V2 with z as the sliced coordinate: z in E and {x,y} in P and t = 1  =>  x in E or y in E
        if z in E and pair_in:
            stat["V2_cases"] += 1
            if x not in E and y not in E: stat["V2_fail"] += 1
print(f"{n_sets} sets with Phi_30 (all subsets of Z_30 containing 0)")
print(f"Lemma 4(a): {stat['a_cases']} (set, direction) cases; slices' double-centred parts unequal, or (N_xy)° != p_z T: {stat['a_fail']};   cases with T != 0: {stat['T_nonzero']}")
print(f"Lemma 4(b): hypothesis met in {stat['b_cases_pair']} cases through the pair and {stat['b_cases_empty']} more through an empty slice; T != 0 or a slice not a union of full lines: {stat['b_fail']}")
print(f"Lemma 5: {stat['L5_cases']} cases with n = p_x p_y and both primes in E; T not integral: {stat['T_int_fail']}; pair missing: {stat['L5_fail']}")
print(f"The stronger statement V2 (z in E, {{x,y}} in P, Phi_30  =>  x in E or y in E): {stat['V2_cases']} cases, violations {stat['V2_fail']}")
print(f"Fact U (Phi_30 and an empty slice along z  =>  {{x,y}} in P): {stat['empty_cases']} cases with an empty slice, violations {stat['U_fail']}")
