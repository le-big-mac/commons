"""Fourth look: the example of the plain page, by exact arithmetic (../reflib.py).
Clock of 9 hours, marks 0, 3, 7.  Remainders on division by 3; the quotients as marks on the clock of 3 hours; every
choice of signs on both clocks (first mark plus; the opposite choices behave the same)."""
import sys
sys.path.insert(0, '/home/agent3/lean/lift-check/small/referee')
from reflib import good_all, sign_matrix, bad_levels, contract, contractible
B = [0, 3, 7]
print('marks', B, 'remainders on division by 3:', [x % 3 for x in B], '; quotients:', [x // 3 for x in B])
print('first place can be struck out (some remainder does not occur):', contractible(B, 3, 2, 1), '; the note\'s map gives', contract(B, 9, 3, 2, 1), 'on the clock of 3 hours')
Bf = contract(B, 9, 3, 2, 1)
g9 = good_all(9, B); g3 = good_all(3, Bf)
for row, a, b in zip(sign_matrix(3), g3, g9):
    s = ''.join('+' if v > 0 else '-' for v in row)
    print(f'signs {s}: on 3 hours balances at {bad_levels(3, Bf, [int(v) for v in row]) or "no divisor"} -> good {bool(a)}; '
          f'on 9 hours balances at {bad_levels(9, B, [int(v) for v in row]) or "no divisor"} -> good {bool(b)}')
