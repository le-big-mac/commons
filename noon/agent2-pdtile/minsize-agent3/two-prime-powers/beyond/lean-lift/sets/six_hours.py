"""The plain example: on the clock of 6 hours, balance at 6 and at no other divisor needs 5 marks with an hour marked twice;
is there a SET of 5 marks on the clocks of 18 = 6*3 and 30 = 6*5 hours that balances at 6 and at no other divisor of 18 (of 30)?
And on 6 itself and 12 = 6*2, is there one?  Exhaustive over all 5-subsets, exact division."""
import itertools
from sympy import Poly, cyclotomic_poly, symbols, ZZ
X = symbols('X')
def pat(els, M):
    A = Poly(sum(X**e for e in els), X, domain=ZZ)
    return tuple(d for d in range(2, M + 1) if M % d == 0 and A.rem(Poly(cyclotomic_poly(d, X), X, domain=ZZ)).is_zero)
for M in (6, 12, 18, 30):
    found = [c for c in itertools.combinations(range(M), 5) if c[0] == 0 and pat(c, M) == (6,)]
    smaller = [c for k in range(1, 5) for c in itertools.combinations(range(M), k) if c[0] == 0 and pat(c, M) == (6,)]
    print(f'clock of {M} hours: sets of 5 marks (one at hour 0) that balance at 6 and at no other divisor: {len(found)}' + (f', for instance {found[0]}' if found else '') + f'; sets of fewer than 5: {len(smaller)}')
# multisets of 5 on the 6-hour clock
ms = [c for c in itertools.combinations_with_replacement(range(6), 5) if c[0] == 0]
good = []
for c in ms:
    A = Poly(sum(X**e for e in c), X, domain=ZZ)
    if tuple(d for d in (2, 3, 6) if A.rem(Poly(cyclotomic_poly(d, X), X, domain=ZZ)).is_zero) == (6,): good.append(c)
print('clock of 6 hours, 5 marks with repeats allowed (one at hour 0), balance at 6 only:', good)
