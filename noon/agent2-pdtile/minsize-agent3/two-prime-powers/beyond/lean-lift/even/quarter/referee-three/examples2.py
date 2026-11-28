# Referee: the text's examples and record multisets, recounted (all signings, all divisors, polynomial remainders).
import sys
import numpy as np
from fractions import Fraction as Fr
from bf import divisors, cyclo, signs, factor

def rows_for(n, d, residues):
    phi = cyclo(d); deg = len(phi) - 1
    low = np.array(phi[:-1], dtype=np.int64)
    need = sorted(set(r % d for r in residues))
    out = {}
    cur = np.zeros(deg, dtype=np.int64); cur[0] = 1
    k = 0
    for target in need:
        while k < target:
            top = cur[-1]
            cur = np.roll(cur, 1); cur[0] = 0
            if top: cur = cur - top * low
            k += 1
        out[target] = cur.copy()
    return np.array([out[r % d] for r in residues])

def share(n, B):
    m = len(B); S = signs(m)
    bad = np.zeros(S.shape[0], dtype=bool); per = {}
    for d in divisors(n):
        T = rows_for(n, d, B)
        z = ~(S @ T).any(axis=1)
        if z.any(): per[d] = int(z.sum())
        bad |= z
    return Fr(int(bad.sum()), S.shape[0]), per

# the other text's (one/) two multisets that exceed the brief's data, its beta(7) example, its Z_15 example for six
# elements, and the brief's lead-2 remark on Z_35 (seven elements: not a counterexample to Q)
CASES = [
 ('one: m=10 on Z_45', 45, [0, 1, 1, 3, 12, 20, 24, 27, 29, 33], Fr(73, 256)),
 ('one: m=10 on Z_225', 225, [1, 29, 51, 63, 75, 100, 128, 129, 162, 177], Fr(73, 256)),
 ('one: m=12 on Z_135', 135, [0, 0, 1, 1, 2, 29, 33, 54, 57, 57, 87, 108], Fr(269, 1024)),
 ('one: beta(7) on Z_105', 105, [0, 3, 9, 12, 32, 36, 97], Fr(7, 32)),
 ('one: beta(5) on Z_15', 15, [6, 8, 9, 10, 12], Fr(1, 4)),
 ('one: m=6 on Z_15', 15, [3, 6, 9, 12, 5, 10], Fr(11, 32)),
 ('three: m=8 search Z_105', 105, [6, 42, 56, 60, 67, 83, 94, 99], Fr(39, 128)),
 ('three: m=7 search Z_105', 105, [10, 22, 26, 55, 84, 88, 100], Fr(7, 32)),
 ('three: m=10 test5 Z_315', 315, [49, 64, 82, 88, 112, 120, 161, 161, 210, 268], Fr(73, 256)),
 ('three: m=12 on Z_2835', 2835, [405, 405, 656, 810, 972, 1115, 1551, 1657, 1713, 1729, 2634, 2643], Fr(269, 1024)),
 ('three: m=10 on Z_2835', 2835, [94, 312, 547, 896, 1058, 1374, 1540, 1678, 2026, 2140], Fr(73, 256)),
]
for name, n, B, claimed in CASES:
    s, per = share(n, B)
    print('%-26s n=%-5d m=%-2d bad share %s  claimed %s  %s   bad signings (first sign +) by divisor: %s' % (name, n, len(B), s, claimed, 'EQUAL' if s == claimed else 'DIFFERENT', per), flush=True)
