# Reader's second look: the two recursions on the tree of 3, written from the two texts' definitions,
# compared size by size.  xi: first text, section 3 (rules (a), (b), (c)).  E3: third text, section 2.
# Exact fractions.  usage: two_recursions.py M
import sys
from fractions import Fraction as F
from math import comb

M = int(sys.argv[1]) if len(sys.argv) > 1 else 60


def pi(v, r):
    if (r + v) % 2 or abs(v) > r:
        return F(0)
    return F(comb(r, (r + v) // 2), 2 ** r)


def c_max(r):          # first text: c_r = C(r, floor(r/2))/2^r
    return F(comb(r, r // 2), 2 ** r)


def c_zero(r):         # third text: c(r) = P(S_r = 0)
    return pi(0, r)


def A(r0, r1, r2):     # sum over v != 0 of the product of the three point probabilities
    s = F(0)
    for v in range(-min(r0, r1, r2), min(r0, r1, r2) + 1):
        if v:
            s += pi(v, r0) * pi(v, r1) * pi(v, r2)
    return s


xi = {0: F(0), 1: F(0)}


def g(r):
    return F(1) if r == 0 else ((c_max(r) if r % 2 == 0 else F(0)) + xi[r])


for m in range(2, M + 1):
    best = F(0)
    for r2 in range(0, m // 3 + 1):
        for r1 in range(max(r2, 1), (m - r2) // 2 + 1):
            r0 = m - r1 - r2
            if r0 < r1:
                continue
            rules = [g(r0) * g(r1) * g(r2)]
            if r0 % 2 == 0 and r1 % 2 == 0 and r2 % 2 == 0:
                p1 = F(1)
                p2 = F(1)
                for r in (r0, r1, r2):
                    p1 *= c_max(r) + xi[r]
                    p2 *= c_max(r)
                rules.append(p1 - p2)
            if r2 == 0 and r0 % 2 and r1 % 2 and r0 <= 7:
                rules.append(xi[r0] * xi[r1] / 2)
            best = max(best, A(r0, r1, r2) + min(rules))
    xi[m] = best

E3 = {1: F(0), 2: F(0)}
for m in range(3, M + 1):
    best = F(0)
    for r1 in range(1, m // 2 + 1):
        r0 = m - r1
        if r0 in (3, 5) and r1 in (3, 5):
            val = E3[r0] * E3[r1] / 2
        else:
            val = c_zero(r0) * E3[r1] + c_zero(r1) * E3[r0] + E3[r0] * E3[r1]
        best = max(best, val)
    for r2 in range(1, m // 3 + 1):
        for r1 in range(r2, (m - r2) // 2 + 1):
            r0 = m - r1 - r2
            p1 = F(1)
            p2 = F(1)
            for r in (r0, r1, r2):
                p1 *= c_zero(r) + E3[r]
                p2 *= c_zero(r)
            best = max(best, A(r0, r1, r2) + p1 - p2)
    E3[m] = best

print("xi(3..16):", [str(xi[m]) for m in range(3, 17)])
print("E3(3..16):", [str(E3[m]) for m in range(3, 17)])
diff = [m for m in range(3, M + 1) if xi[m] != E3[m]]
print(f"sizes m <= {M} at which the two recursions give different numbers:", diff)
for m in diff[:8]:
    print("  m =", m, " first text", xi[m], " third text", E3[m])
