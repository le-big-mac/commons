# Writes the table that the C enumerator reads: for each hour h, X^h mod Phi_d for every divisor d>1 of M.
import sys
from polylib import *
import sympy
M = int(sys.argv[1])
ds = [d for d in divisors(M) if d > 1]
X = sympy.symbols('X')
for d in ds:  # cross-check my Phi_d against sympy's
    assert list(reversed(sympy.Poly(sympy.cyclotomic_poly(d, X), X).all_coeffs())) == list(cyclo(d)), d
rows = []
mx = 0
for h in range(M):
    row = []
    for d in ds:
        phi = len(cyclo(d)) - 1
        _, r = polydivmod([0] * h + [1], list(cyclo(d)))
        r = r + [0] * (phi - len(r))
        row += r
    mx = max(mx, max(abs(x) for x in row))
    rows.append(row)
assert all(len(r) == M - 1 for r in rows)
out = [f"{M} {len(ds)} {mx}"]
out.append(" ".join(f"{d} {len(cyclo(d)) - 1}" for d in ds))
for r in rows:
    out.append(" ".join(map(str, r)))
print("\n".join(out))
