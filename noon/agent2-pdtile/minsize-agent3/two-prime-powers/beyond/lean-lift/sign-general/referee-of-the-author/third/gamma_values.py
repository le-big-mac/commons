"""Referee, third pass: Gamma(m) for the m used in the instance's end-to-end runs (its section 7) and in mine."""
import sys
_a = sys.argv; sys.argv = [_a[0]]
from coverage3_own import gamma, factor
sys.argv = _a
for m in (135, 225, 675, 189, 4725, 1323, 2025, 25, 27, 175, 63, 441, 1225, 4375, 6125):
    f = factor(m); G = gamma(tuple(sorted(f.items())))
    print(f'Gamma({m} = {f}) = {G}  ->  Theorem 7 {"applies" if G > 0 else "does NOT apply"} with this m')
