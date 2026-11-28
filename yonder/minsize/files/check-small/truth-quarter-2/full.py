"""One mark on every hour of the clock of n hours: the number of bad falls of the coins (all 2^n choices of signs),
by the definition (a balance at some divisor of n, 1 included), with exact integers.
Compared with the bounds of the page: at most 3 in 8 bad on a clock with an odd number of hours, at most 6 in 8 on
any clock, both for three or more marks.  The printed table the search used lists these counts up to n = 51;
this run goes as far as N (default 18) only."""
import sys
from fractions import Fraction
from check import divisors, red_rows

N = int(sys.argv[1]) if len(sys.argv) > 1 else 18
for n in range(1, N + 1):
    divs = divisors(n)
    rows = {d: red_rows(n, d) for d in divs}
    bad = 0
    for bits in range(2 ** (n - 1)):                 # first sign +; the count is doubled below
        s = [1] + [1 if (bits >> i) & 1 else -1 for i in range(n - 1)]
        for d in divs:
            r = rows[d]
            k = len(r[0])
            if all(sum(s[h] * r[h][c] for h in range(n)) == 0 for c in range(k)):
                bad += 1
                break
    bad *= 2
    share = Fraction(bad, 2 ** n)
    if n >= 3:
        bound = Fraction(3, 8) if n % 2 else Fraction(3, 4)
        verdict = "within" if share <= bound else "OUTSIDE"
        print(f"n = {n:2d}: bad falls {bad:6d} of {2 ** n:6d} = {str(share):>9s}; bound {bound}: {verdict}")
    else:
        print(f"n = {n:2d}: bad falls {bad:6d} of {2 ** n:6d} = {str(share):>9s}; fewer than three marks, the statement does not speak of it")
