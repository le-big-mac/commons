"""Recompute, with the referee's engine, the shares of the best multisets that section 5 of result.md reports."""
import math
from fractions import Fraction as Fr
from extra import share_bad
cases = [(27, 16, [(0, 2), (3, 2), (4, 2), (6, 2), (13, 2), (17, 4), (22, 2)], Fr(7539, 32768)),
         (45, 20, [(7, 2), (15, 4), (18, 2), (21, 2), (23, 2), (32, 2), (36, 2), (39, 2), (43, 2)], Fr(108941, 524288)),
         (27, 24, [(0, 8), (3, 4), (5, 2), (6, 4), (7, 2), (9, 2), (18, 2)], Fr(790385, 4194304)),
         (45, 30, [(0, 12), (6, 2), (12, 4), (14, 2), (19, 2), (30, 2), (33, 2), (36, 2), (42, 2)], Fr(2847261, 16777216)),
         (27, 40, [(0, 24), (5, 4), (12, 3), (15, 3), (16, 2), (21, 1), (24, 1), (25, 2)], Fr(39977323845, 274877906944)),
         (225, 20, [(50, 2), (54, 2), (64, 2), (100, 2), (104, 2), (180, 2), (193, 4), (196, 2), (217, 2)], Fr(108685, 524288))]
for n, m, L, claimed in cases:
    ms = dict(L); assert sum(ms.values()) == m
    P = share_bad(n, ms)
    print(f"Z_{n} m = {m}: share {P} = {float(P):.6f}, times sqrt(m) {float(P) * math.sqrt(m):.4f}; the text's value {claimed}: {'agrees' if P == claimed else 'DIFFERS'}")
