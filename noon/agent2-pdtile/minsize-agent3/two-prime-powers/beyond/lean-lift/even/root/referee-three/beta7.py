"""A check of the engine against Theorem Q's value beta(7) = 7/32, which none of the exhaustive runs reaches (largest on
Z_15: 13/64): seven elements on Z_105 with classes (5,1,1) modulo 3, (3,1,1,1,1) modulo 5 and all different modulo 7."""
import itertools
from fractions import Fraction as Fr
from extra import share_bad, share_at
import tests as TS
best = Fr(0); arg = None; n = 105; cnt = 0
r7 = list(range(7))
for r5 in set(itertools.permutations([0, 0, 0, 1, 2, 3, 4])):
    for r3 in set(itertools.permutations([0, 0, 0, 0, 0, 1, 2])):
        els = [next(b for b in range(n) if b % 7 == r7[i] and b % 5 == r5[i] and b % 3 == r3[i]) for i in range(7)]
        ms = {}
        for b in els: ms[b] = ms.get(b, 0) + 1
        P = TS.check(n, ms); cnt += 1
        if P > best: best = P; arg = sorted(els)
print(f"{cnt} multisets of 7 elements on Z_105 of that shape: largest share {best} at {arg}; Psi(7) = {TS.Psi(7)}")
print("shares at 3, 5, 7 there:", share_at(n, {b: 1 for b in arg}, 3), share_at(n, {b: 1 for b in arg}, 5), share_at(n, {b: 1 for b in arg}, 7))
TS.report("beta7 FINAL")
