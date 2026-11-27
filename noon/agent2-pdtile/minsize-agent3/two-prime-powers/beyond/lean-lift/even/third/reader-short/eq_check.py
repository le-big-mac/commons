#!/usr/bin/env python3
"""The sentence after Theorem T: two elements with different positions and values v, +-v have Q = 2z (= 1).
And {(u, v), (u, v)} (same position, same value): equality in Theorem T', Q = z = P(F_k) = 1/2."""
from tprime_check import analyse, popc

n = 0
for k in (1, 2, 3, 4):
    for N, vals in ((0, (1, 2, 5)), (3, (1, 2)), (5, (1, 2)), (9, (1, 3, 4))):
        for u1 in range(1 << k):
            for u2 in range(1 << k):
                if u1 == u2:
                    continue
                for v in vals:
                    for w in (v, -v):
                        bad, F, _ = analyse([u1, u2], [v, w], k, N)
                        some = 0
                        for b in bad:
                            some |= b
                        assert popc(bad[0]) == 2 and popc(some) == 4, (k, N, u1, u2, v, w)
                        # one sign pattern bad at level 0, the other at the level where they part, and only there
                        part = next(j for j in range(1, k + 1) if u1 % (1 << j) != u2 % (1 << j))
                        assert bad[part] == 15 ^ bad[0]
                        assert all(bad[j] & ~bad[0] == 0 for j in range(1, k + 1) if j != part)
                        n += 1
        for u in range(1 << k):
            for v in vals:
                bad, F, _ = analyse([u, u], [v, v], k, N)
                some = 0
                for b in bad:
                    some |= b
                assert popc(some) == 2 == popc(bad[0]) == popc(F[k])
print("two elements, different positions, values v and +-v: Q = 1 = 2z in all %d cases" % n)
