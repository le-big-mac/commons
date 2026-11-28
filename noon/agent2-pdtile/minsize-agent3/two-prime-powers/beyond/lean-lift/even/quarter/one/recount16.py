"""Recount for the revision after the referee's report: the largest X(B) over every multiset of M elements on Z_27
(every shape of depth 3), all signings, with the functions of test3.py (the distribution of the root is not cached).
usage: recount16.py M"""
import sys
from fractions import Fraction as F
import test3
a = 3; m = int(sys.argv[1])
best = -1; ex = None; n = 0
for s in test3.shapes(a, m):
    D = test3.dist.__wrapped__(a, s)
    X = sum(cnt for (v, k), cnt in D.items() if k and v)
    n += 1
    if X > best:
        best = X; ex = s
print(f"Z_27, m = {m}: {n} shapes, all signings: largest X(B) = {F(best, 2 ** m)} at {ex}")
