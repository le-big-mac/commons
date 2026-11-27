"""ExceptionalPair: for every n <= NMAX and every pair a, b of Z_n: is the additive order of a - b even (the
definition), and is a - b not divisible by 2^k, 2^k the power of 2 in n (the paper's words)?  The order is computed
by repeated addition; n / gcd(n, (a - b) mod n) (the form of my Lean lemma addOrderOf_eq) is compared as well; and
the good splittings of the pair by long division (X^a + X^b and X^a - X^b against every Phi_d, d | n).
usage: t6_exc.py NMAX
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from math import gcd
from ecore import cyclo, divisors, pdivmod

NMAX = int(sys.argv[1])
tot = diff = diff_formula = diff_good = 0
rows = []
for n in range(1, NMAX + 1):
    k2 = 1
    while n % (2 * k2) == 0:
        k2 *= 2
    cyc = [list(cyclo(d)) for d in divisors(n)]
    ne = 0
    for a in range(n):
        for b in range(n):
            x = (a - b) % n
            t = 1
            y = x
            while y != 0:
                y = (y + x) % n
                t += 1
            even = (t % 2 == 0)
            words = ((a - b) % k2 != 0)
            tot += 1
            ne += even
            diff += (even != words)
            diff_formula += (t != n // gcd(n, x))
            # the splittings of {a, b}: +,+ and +,- (the other two are their negatives)
            plus = [0] * n
            plus[a] += 1
            plus[b] += 1
            minus = [0] * n
            minus[a] += 1
            minus[b] -= 1
            g = any(all(any(pdivmod(m, c)[1]) for c in cyc) for m in (plus, minus))
            diff_good += (g == even)
    rows.append((n, k2, ne))
print(f"n = 1..{NMAX}: pairs (a, b) checked {tot}; 'order of a - b even' differs from '2^k does not divide a - b' in "
      f"{diff} cases; the order differs from n / gcd(n, a - b) in {diff_formula} cases; 'the pair has a good signing' "
      f"differs from 'the order is odd' in {diff_good} cases")
print("(n, 2^k, number of ordered pairs (a, b) with even order):", rows)
print("a = b: the order of 0 is 1 (odd) for every n, so two equal marks are never exceptional; n odd: no exceptional "
      "pair:", all(ne == 0 for (n, k2, ne) in rows if n % 2 == 1), "; n even: the pairs with even order are those with "
      "a - b outside the subgroup of index 2^k:", all(ne == n * n - n * (n // k2) for (n, k2, ne) in rows))
