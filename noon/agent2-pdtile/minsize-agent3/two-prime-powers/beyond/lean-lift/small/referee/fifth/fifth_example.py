"""Fifth look: the second step of the plain page's example, and the numbers of its new sentences (exact; ../reflib.py).
Clock of 9 hours, marks 0, 3, 7 written as (first digit, second digit) = (remainder on division by 3, number of threes).
(1) the second digit, tested group by group; striking it out of the original marks; signs good there are good on 9 hours.
(2) striking both digits: possible in the order second, then first; not in the order first, then second.
(3) the most places a prime can keep with 36 marks: floor(35 / (p - 1)).
(4) a clock with another prime: on 45 hours the 'number of threes' in an hour is not a digit; the digits are those of the
    remainder on division by 9."""
import sys
sys.path.insert(0, '/home/agent3/lean/lift-check/small/referee')
from reflib import good_all, sign_matrix, contract, contractible
B = [0, 3, 7]
print('digits:', [(x % 3, x // 3) for x in B])
groups = {}
for x in B: groups.setdefault(x % 3, []).append(x // 3)
print('(1) second digits by group of the first digit:', groups, '; second place can be struck out:', contractible(B, 3, 2, 2))
Bf = contract(B, 9, 3, 2, 2)
print('    struck out of the original marks:', Bf, 'on the clock of 3 hours')
g9 = good_all(9, B); g3 = good_all(3, Bf)
for row, a, b in zip(sign_matrix(3), g3, g9):
    print('    signs', ''.join('+' if v > 0 else '-' for v in row), ': good on 3 hours', bool(a), '; good on 9 hours', bool(b))
print('    every signing good for', Bf, 'on 3 hours is good for', B, 'on 9 hours:', not (g3 & ~g9).any())
print('(2) after the second digit:', Bf, '-> first place can be struck out:', contractible(Bf, 3, 1, 1), '(clock of 1 hour);',
      'after the first digit:', contract(B, 9, 3, 2, 1), '-> the remaining place can be struck out:', contractible(contract(B, 9, 3, 2, 1), 3, 1, 1))
print('(3) most places kept with 36 marks:', {p: 35 // (p - 1) for p in (3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)})
print('(4) clock of 45 hours, hour 20: remainder on division by 3 is', 20 % 3, ', number of threes in it', 20 // 3,
      '(not a digit); digits of its remainder on division by 9:', ((20 % 9) % 3, (20 % 9) // 3))
