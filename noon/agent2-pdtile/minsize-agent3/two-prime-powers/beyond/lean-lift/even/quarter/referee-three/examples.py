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

CASES = [
 ('beta(5) example', 15, [0, 1, 2, 3, 9], Fr(1, 4)),
 ('beta(7) example', 105, [0, 1, 2, 3, 39, 75, 90], Fr(7, 32)),
 ('beta(6) on Z_3', 3, [0, 0, 1, 1, 2, 2], Fr(11, 32)),
 ('beta(8) on Z_3', 3, [0, 0, 0, 0, 1, 1, 2, 2], Fr(39, 128)),
 ('m=6 on Z_75', 75, [0, 0, 25, 25, 38, 50], Fr(11, 32)),
 ('m=8 on Z_105', 105, [32, 35, 38, 59, 82, 85, 93, 93], Fr(39, 128)),
 ('m=9 pattern Z_105', 105, [0, 1, 2, 3, 39, 75, 90, 0, 0], Fr(3, 16)),
 ('m=10 on Z_315', 315, [2, 34, 51, 90, 164, 165, 183, 258, 261, 277], Fr(73, 256)),
 ('m=10 on Z_45', 45, [2, 9, 15, 18, 20, 21, 22, 31, 33, 39], Fr(73, 256)),
 ('m=11 pattern Z_1155', 1155, [0, 1, 2, 3, 774, 390, 930, 315, 525, 735, 945], Fr(43, 256)),
 ('m=12 on Z_315', 315, [48, 132, 172, 180, 180, 186, 219, 225, 230, 234, 266, 298], Fr(269, 1024)),
 ('m=12 on Z_1575', 1575, [375, 876, 940, 1088, 1129, 1134, 1146, 1170, 1503, 1520, 1557, 1572], Fr(269, 1024)),
 ('m=13 pattern Z_15015', 15015, [0, 1, 2, 3, 10014, 5010, 9015, 13020, 6300, 14595, 7875, 1155, 8085], Fr(627, 4096)),
 ('(m-2,1,1), m=9, on Z_3', 3, [0] * 7 + [1, 2], Fr(35, 256)),
]
for name, n, B, claimed in CASES:
    s, per = share(n, B)
    print('%-24s n=%-5d m=%-2d bad share %s  claimed %s  %s   bad signings (first sign +) by divisor: %s' % (name, n, len(B), s, claimed, 'EQUAL' if s == claimed else 'DIFFERENT', per), flush=True)
