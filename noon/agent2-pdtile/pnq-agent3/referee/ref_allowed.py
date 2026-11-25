"""Referee: D+ = k on every pattern the theorem allows (float LP); and how D+ compares with k elsewhere."""
import sys
from ref_certs_lp import order_sums, dplus, subsets
for s in sys.argv[1:]:
    p, n, q = (int(v) for v in s.split(","))
    M = p ** n * q
    divs, R = order_sums(M)
    a_app = a_ok = b_app = b_ok = 0
    other = other_Dlek = other_DgtK = 0
    for E in subsets(range(1, n + 1)):
        for F in subsets(range(0, n + 1)):
            Z = set(p ** l for l in E) | set(p ** l * q for l in F)
            D = dplus(Z, divs, R)
            k = p ** len(E) * (q if 0 in F else 1)
            if 0 not in F and F <= E:
                a_app += 1; a_ok += abs(D - k) < 1e-6
            elif 0 in F and E <= F:
                b_app += 1; b_ok += abs(D - k) < 1e-6
            else:
                other += 1
                other_Dlek += D < k - 1e-6
                other_DgtK += D > k + 1e-6
    print(f"p={p} n={n} q={q} M={M}: allowed (0 notin F, F<=E): {a_ok}/{a_app} have D+=p^e; allowed (0 in F, E<=F): {b_ok}/{b_app} have D+=p^e q; "
          f"other patterns {other}: D+<k in {other_Dlek}, D+>k in {other_DgtK}, D+=k in {other - other_Dlek - other_DgtK}")
