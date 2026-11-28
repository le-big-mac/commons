# What WOULD change if the exception of the recursion for E3 (sizes 3, 5) were extended to size 7 (Remark 3.3).
# Nothing in bounds.py is changed by this program; it recomputes the recursion with the larger exception and lists
# the sizes m <= M at which the value differs, and what the bounds of Theorem 6 (m = 10) and Theorem 7 would be.
import sys
from fractions import Fraction as F
import bounds
from bounds import c, g3

M = int(sys.argv[1]) if len(sys.argv) > 1 else 200
bounds.build3(M)
E_old = dict(bounds.E3)

E = {0: F(0), 1: F(0), 2: F(0)}
for m in range(3, M + 1):
    best = F(-1)
    for r1 in range(1, m // 2 + 1):
        r0 = m - r1
        if r0 in (3, 5, 7) and r1 in (3, 5, 7):
            val = E[r0] * E[r1] / 2
        else:
            val = c(r0) * E[r1] + c(r1) * E[r0] + E[r0] * E[r1]
        best = max(best, val)
    for r2 in range(1, m // 3 + 1):
        for r1 in range(r2, (m - r2) // 2 + 1):
            r0 = m - r1 - r2
            val = g3(r0, r1, r2) + (c(r0) + E[r0]) * (c(r1) + E[r1]) * (c(r2) + E[r2]) - c(r0) * c(r1) * c(r2)
            best = max(best, val)
    E[m] = best

diff = [m for m in range(3, M + 1) if E[m] != E_old[m]]
print('sizes m <= %d at which the recursion with the exception for 3, 5, 7 differs from the one with 3, 5: %s' % (M, diff))
for m in diff[:12]:
    print('  m=%d: %s (now) -> %s (with 7): smaller by %s' % (m, E_old[m], E[m], E_old[m] - E[m]))
assert all(E[m] <= E_old[m] for m in range(3, M + 1))
print('E3(10) with 7: %s;  c(10) + E3(10) = %s' % (E[10], c(10) + E[10]))
print('E3 with 7 for m = 12, 14, 16: %s, %s, %s (now: %s, %s, %s)' % (E[12], E[14], E[16], E_old[12], E_old[14], E_old[16]))
# the bounds for ten elements that contain E3(10): Theorem 6 (two levels of 5 counted) and Remark 6.1 (one level)
bounds.build(12)
p5, p7 = bounds.psi(5, 10), bounds.psi(7, 10)
print('ten elements: Theorem 6 bound now %s, with 7 it would be %s;  Remark 6.1 bound now %s, with 7 it would be %s'
      % (bounds.BB[10], c(10) + E[10] + 2 * p5 + p7, c(10) + E_old[10] + p5 + p7, c(10) + E[10] + p5 + p7))
# Theorem 7 for m >= 12: the largest values are at m = 12, 14, 16, where nothing changes
print('sizes 12 <= m <= 21 at which E3 changes: %s' % [m for m in diff if 12 <= m <= 21])
