"""S1's corner formula against the definition, for every up-set of the divisors of p^n q^m, 0 <= n, m <= 6 (p = 2, q = 3; only exponents matter).
Definition: corners = maximal elements of the complement L (by brute force over all pairs of exponents).
Formula (S1): minimal elements N_j = p^{a_j} q^{b_j}, a_1 < ... < a_k; a_{k+1} = n + 1, b_0 = m + 1;
              c_i = p^{a_{i+1} - 1} q^{b_i - 1} for i = 0..k, kept unless (i = 0 and a_1 = 0) or (i = k and b_k = 0); k = 0: C = {M}.
Also checked: the b_j strictly decrease; the kept c_i are pairwise incomparable; the rectangles R_i partition L; and the step of the
induction in Theorem S: the corners of D' = D restricted to the divisors of M' = p^{a_k - 1} q^m are the corners of D other than c_k."""
import itertools
from construct import upsets_staircase
tot = 0; deg = dict(a1_zero=0, bk_zero=0, k0=0, n0=0, m0=0, ind=0)
for n in range(0, 7):
    for m in range(0, 7):
        allts = upsets_staircase(2, n, 3, m) + [tuple([m + 1] * (n + 1))] if False else upsets_staircase(2, n, 3, m)
        for ts in allts:                                  # D = {(u, v): v >= ts[u]}
            inD = lambda u, v: v >= ts[u]
            L = [(u, v) for u in range(n + 1) for v in range(m + 1) if not inD(u, v)]
            assert (0, 0) in L
            brute = sorted(c for c in L if not any(d != c and d[0] >= c[0] and d[1] >= c[1] for d in L))
            Dl = [(u, v) for u in range(n + 1) for v in range(m + 1) if inD(u, v)]
            mins = sorted(d for d in Dl if not any(e != d and e[0] <= d[0] and e[1] <= d[1] for e in Dl))
            k = len(mins); a = [0] + [x for x, _ in mins] + [n + 1]; b = [m + 1] + [y for _, y in mins]
            assert all(a[j] < a[j + 1] for j in range(1, k)) and all(b[j] > b[j + 1] for j in range(1, k))
            keep = [i for i in range(k + 1) if not (k >= 1 and i == 0 and a[1] == 0) and not (k >= 1 and i == k and b[k] == 0)]
            formula = sorted((a[i + 1] - 1, b[i] - 1) for i in keep)
            assert formula == brute, (n, m, ts, formula, brute)
            # rectangles partition L
            cells = []
            for i in range(k + 1):
                cells += [(u, v) for u in range(a[i], a[i + 1]) for v in range(0, b[i])]
            assert sorted(cells) == sorted(L) and len(cells) == len(set(cells))
            assert all(not (c[0] <= d[0] and c[1] <= d[1]) for c in formula for d in formula if c != d)
            tot += 1
            if k == 0: deg['k0'] += 1
            if k >= 1 and a[1] == 0: deg['a1_zero'] += 1
            if k >= 1 and b[k] == 0: deg['bk_zero'] += 1
            if n == 0: deg['n0'] += 1
            if m == 0: deg['m0'] += 1
            # induction step
            if k >= 1 and a[k] >= 1:
                n2 = a[k] - 1
                L2 = [(u, v) for (u, v) in L if u <= n2]
                brute2 = sorted(c for c in L2 if not any(d != c and d[0] >= c[0] and d[1] >= c[1] for d in L2))
                ck = (n, b[k] - 1)
                assert brute2 == sorted(c for c in brute if c != ck), (n, m, ts)
                assert (ck in brute) == (b[k] >= 1)
                deg['ind'] += 1
print(f'{tot} up-sets (0 <= n, m <= 6): S1\'s formula gives exactly the maximal elements of the complement in all; the rectangles partition L in all;')
print(f'degenerate cases met: k = 0: {deg["k0"]}; a_1 = 0: {deg["a1_zero"]}; b_k = 0: {deg["bk_zero"]}; n = 0: {deg["n0"]}; m = 0: {deg["m0"]};')
print(f'induction step of Theorem S (corners of D\' in Z_M\' = corners of D other than c_k): checked in {deg["ind"]} cases with a_k >= 1')
