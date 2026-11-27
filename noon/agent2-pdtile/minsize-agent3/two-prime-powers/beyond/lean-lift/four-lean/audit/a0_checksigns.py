"""The values that CheckSigns.lean expects (in its comments), recomputed here from core.py: mu, live, rank, lhsN1, and the
numbers of bad signings by exact division by Phi_d (not by the criterion of that file)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import core
e5 = [0, 1, 2, 3, 6]; e7 = [0, 1, 2, 3, 6, 9, 18]; e15 = [0, 3, 5, 6, 9, 10, 12]; e6 = [0, 1, 2, 3, 4, 5]; e9 = [0, 0, 1, 1, 2, 2]
print([core.mu(t) for t in [3, 5, 9, 15, 45, 7, 21, 27, 105, 11025]])
print([core.mu(t) for t in [0, 1]])
B = lambda l: str([bool(x) for x in l]).lower()
print(B(core.live(e5, 3, i) for i in [0, 1, 2, 3]))
print([core.rank(e5, 3, i) for i in [0, 1, 2, 3]])
print(B(core.live(e7, 3, i) for i in [1, 2, 3, 4]))
print([core.rank(e7, 3, i) for i in [0, 1, 2, 3, 4]])
print(B(core.live(e15, 3, i) for i in [1, 2]))
print(B(core.live(e15, 5, i) for i in [1, 2]))
print([core.rank(e15, 3, i) for i in [1, 2]])
print([core.rank(e15, 5, i) for i in [1, 2]])
print(B(core.live(e6, 3, i) for i in [1, 2]))
print(B(core.live(e6, 5, i) for i in [1, 2]))
print(B(core.live(e9, 3, i) for i in [1, 2]))
print(B(core.live(e5, 2, i) for i in [1, 2]))
print('[' + ', '.join(str(core.lhsN1(m, [3])) for m in [3, 5, 6, 14]) + ']')
print('[' + ', '.join(str(core.lhsN1(m, [3, 5, 9, 15, 45])) for m in [3, 5, 6, 14]) + ']')
print('[' + ', '.join(str(core.lhsN1(m, [])) for m in [1, 2, 4, 12, 14]) + ']')
print([int(core.bad(e5, d).sum()) for d in [1, 3, 9]])
print([int(core.bad(e7, d).sum()) for d in [1, 3, 9, 27]])
print([int(core.bad(e15, d).sum()) for d in [1, 3, 5, 15]])
print([int(core.bad(e6, d).sum()) for d in [1, 3, 5, 15]])
print([int(core.bad(e9, d).sum()) for d in [1, 3, 9]])
