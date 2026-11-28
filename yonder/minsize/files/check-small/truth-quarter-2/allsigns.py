"""The six markings with the least shares, once more, with every one of the 2^m choices of signs written out
(no use of the fact that turning all signs over changes nothing).  Exact integers; balance by the remainder
modulo the cyclotomic polynomial (check.py)."""
import itertools
from fractions import Fraction
from check import divisors, balances

ex = [(12, [0, 1, 2]), (2, [0, 0, 0, 1]), (30, [0, 1, 2, 3, 9]), (6, [0, 0, 1, 2, 2, 4]),
      (210, [0, 3, 9, 12, 32, 141, 202]), (6, [0, 0, 0, 0, 1, 2, 2, 4])]
for n, hs in ex:
    m = len(hs)
    good = 0
    for s in itertools.product((1, -1), repeat=m):
        if not any(balances(n, d, hs, list(s)) for d in divisors(n)):
            good += 1
    print(f"clock {n:3d}, marks {hs}: good ways {good} of {2 ** m} = {Fraction(good, 2 ** m)}")
