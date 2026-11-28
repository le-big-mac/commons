"""Random markings of 3 to 10 marks on some clocks: is the share of good signings ever below the page's figures?
(a quarter for every number of marks from three on; a half for an odd number; exactly-least 1/2, 1/4, 1/2, 5/16,
9/16, 25/64 for three to eight marks).  All signings, exact integers (shares_check.py)."""
import random, sys
from fractions import Fraction
from shares_check import reductions, good_share

floor = {3: Fraction(1, 2), 4: Fraction(1, 4), 5: Fraction(1, 2), 6: Fraction(5, 16), 7: Fraction(9, 16),
         8: Fraction(25, 64), 9: Fraction(1, 2), 10: Fraction(17, 64)}
rng = random.Random(int(sys.argv[1]))
per = int(sys.argv[2])
tried = 0; below = 0
for n in map(int, sys.argv[3:]):
    red = reductions(n)
    least = {}
    for m in range(3, 11):
        for _ in range(per):
            kind = rng.randrange(3)
            if kind == 0:
                marks = [rng.randrange(n) for _ in range(m)]
            elif kind == 1:   # few different hours, repeated
                pool = [rng.randrange(n) for _ in range(rng.randint(2, 4))]
                marks = [rng.choice(pool) for _ in range(m)]
            else:             # one heavy hour and some small ones
                marks = [0] * rng.randint(1, m - 2)
                marks += [rng.randrange(min(n, 6)) for _ in range(m - len(marks))]
            g = good_share(n, marks, red); tried += 1
            if g < floor[m]:
                below += 1; print("BELOW:", n, m, sorted(marks), g, flush=True)
            if m not in least or g < least[m][0]:
                least[m] = (g, sorted(marks))
    print(f"clock {n}: least share met by number of marks: " + "; ".join(f"{m}: {least[m][0]}" for m in sorted(least)), flush=True)
print(f"markings tried {tried}, below the page's figures: {below}")
