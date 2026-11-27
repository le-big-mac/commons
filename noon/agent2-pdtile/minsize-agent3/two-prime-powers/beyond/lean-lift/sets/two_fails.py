"""For the prime 2 the statement of the proposition fails with j = 2: on Z_2 the multiset with 0 four times and 1 twice
(multiplicities at most 4, not all 4; no cyclotomic divisor) has no lift to a SET on Z_8 without a new divisor.  Exhaustive."""
import itertools
from sympy import Poly, cyclotomic_poly, symbols, ZZ
X = symbols('X')
def pat(els, M):
    A = Poly(sum(X**e for e in els), X, domain=ZZ)
    return tuple(d for d in range(1, M + 1) if M % d == 0 and A.rem(Poly(cyclotomic_poly(d, X), X, domain=ZZ)).is_zero)
base = Poly(4 + 2 * X, X, domain=ZZ)
print('on Z_2, mask 4 + 2X: divisible by Phi_1:', base.rem(Poly(cyclotomic_poly(1, X), X, domain=ZZ)).is_zero, ' by Phi_2:', base.rem(Poly(cyclotomic_poly(2, X), X, domain=ZZ)).is_zero)
for pair in itertools.combinations([1, 3, 5, 7], 2):
    S = [0, 2, 4, 6] + list(pair); print('  set', S, 'on Z_8: cyclotomic divisors', pat(S, 8))
