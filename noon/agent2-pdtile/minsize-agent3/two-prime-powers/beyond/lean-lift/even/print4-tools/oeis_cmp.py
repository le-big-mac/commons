# usage: python3 -I oeis_cmp.py BFILE
# Compares the listed counts a(n) of singular (-1,1)-circulants (full support, m = n) with the bounds of the statement:
# share <= 3/8 for odd n >= 3, share <= 3/4 for every n >= 3, share <= 1/2 for odd m = n.
import sys
from fractions import Fraction
rows = []
for line in open(sys.argv[1], encoding="utf-8", errors="replace"):
    p = line.split()
    if len(p) >= 2 and p[0].isdigit() and p[1].lstrip("-").isdigit():
        rows.append((int(p[0]), int(p[1])))
print("terms listed:", len(rows), "n from", rows[0][0], "to", rows[-1][0])
worst_odd = max((Fraction(a, 2 ** n), n) for n, a in rows if n >= 3 and n % 2 == 1)
worst_all = max((Fraction(a, 2 ** n), n) for n, a in rows if n >= 3)
print("largest share, odd n >= 3:", worst_odd[0], "at n =", worst_odd[1], "| <= 3/8:", worst_odd[0] <= Fraction(3, 8))
print("largest share, n >= 3:", worst_all[0], "at n =", worst_all[1], "| <= 3/4:", worst_all[0] <= Fraction(3, 4))
for n, a in rows[:13]:
    print("  n =", n, "a(n) =", a, "share =", Fraction(a, 2 ** n))
