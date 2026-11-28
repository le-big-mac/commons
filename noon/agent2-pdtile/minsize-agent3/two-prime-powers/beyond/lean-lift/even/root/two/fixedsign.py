# The remark on lead 3 in section 5 of result.md: for the primes 3, 5, 7 (n = 105) and the decoration U = all nonzero
# multiples of n/q (q = 3, 5, 7), all with sign +, Q(zeta_d) = |U| - (sum of the primes of d), for every d | 105.
def polydiv(num, den):
    num = num[:]; q = [0] * (len(num) - len(den) + 1)
    for i in range(len(num) - len(den), -1, -1):
        q[i] = num[i + len(den) - 1]
        for j, dj in enumerate(den): num[i + j] -= q[i] * dj
    return q, num[:len(den) - 1]
PHI = {}
def phi(d):
    if d not in PHI:
        num = [-1] + [0] * (d - 1) + [1]
        for e in range(1, d):
            if d % e == 0:
                num, rem = polydiv(num, phi(e)); assert not any(rem)
        PHI[d] = num
    return PHI[d]
n = 105; U = [j * (n // q) for q in (3, 5, 7) for j in range(1, q)]
Q = [0] * n
for b in U: Q[b] += 1
vals = {}
for d in [d for d in range(1, n + 1) if n % d == 0]:
    _, rem = polydiv(Q, phi(d))
    assert not any(rem[1:]), d
    primes = sum(q for q in (3, 5, 7) if d % q == 0)
    assert rem[0] == len(U) - primes, (d, rem[0])
    vals[d] = rem[0]
print("U =", sorted(U), " |U| =", len(U)); print("Q(zeta_d) for d | 105:", vals, "; distinct values:", len(set(vals.values())))
