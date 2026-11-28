# Referee, second look: case (c) of the eight-element proof on Z_45: X and L_5 both nonempty?
import numpy as np
from fractions import Fraction as Fr
from bf import *
def el(a3, c5): return (10 * a3 + 36 * c5) % 45
B = [el(1, 0), el(2, 0), el(4, 1), el(5, 1), el(7, 2), el(8, 2), el(0, 3), el(0, 4)]
ev = bad_events(45, np.array([B]))
X = (ev[3] | ev[9]) & ~ev[1]; L5 = ev[5] | ev[15] | ev[45]; bad = np.zeros_like(ev[1])
for d in ev: bad |= ev[d]
h = 128
print('B =', B, 'on Z_45; classes mod 5 sizes (2,2,2,1,1); P(X) = %s, P(L_5) = %s, P(X or L_5) = %s, bad share = %s' % (Fr(int(X.sum()), h), Fr(int(L5.sum()), h), Fr(int((X | L5).sum()), h), Fr(int(bad.sum()), h)))
