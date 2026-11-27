# Referee's second look, two small checks.  Exact integers / fractions.  Imports nothing of the author's.
from fractions import Fraction as Fr
from cyc import cyclo
# 1. Phi_(2e)(x) = Phi_e(-x) for odd e > 1 (the reflection at level 1 for every odd e is the substitution x -> -x)
bad = [e for e in range(3, 200, 2) if cyclo(2 * e) != [c * (-1) ** i for i, c in enumerate(cyclo(e))]]
print("Phi_(2e)(x) = Phi_e(-x) for every odd e from 3 to 199:", not bad, "; and Phi_2(x) = -Phi_1(-x):",
      cyclo(2) == [-c * (-1) ** i for i, c in enumerate(cyclo(1))])
# 2. the least of 1 - 2 p_m - 2 W_m(no 3) over 5 <= m <= 200, to more places
def primes_upto(n):
    return [p for p in range(2, n + 1) if all(p % r for r in range(2, int(p ** 0.5) + 1))]
def A(t):
    r = 1
    for p in primes_upto(t + 1):
        if p >= 5:
            r *= 1 + t // (p - 1)
    return r
def W(m):
    s, t = Fr(0), 2
    while t <= m - 1:
        s += Fr(A(t) - A(t - 2), 2 ** t)
        t += 2
    return s
def p(r):
    x = Fr(1)
    for _ in range(r):
        x = (1 - x) / 2
    return x
least = min((1 - 2 * p(m) - 2 * W(m), m) for m in range(5, 201))
v = least[0]
print("least over 5 <= m <= 200 at m =", least[1], ": floor to 14 places =", int(v * 10 ** 14), "/ 10^14")
