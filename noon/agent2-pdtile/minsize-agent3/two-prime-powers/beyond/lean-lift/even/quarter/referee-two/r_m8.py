#!/usr/bin/env python3
"""Referee: the remark of section 5 on eight elements: for every d divisible by 7 the signings bad at d are among
the same two.  Tested on multisets of 8 elements whose residues modulo 7 have the pattern (2,1,1,1,1,1,1) (the only
pattern with a 7-full cell and no lone element), other coordinates random or shaped; all signings, from the definition.
Also counts the families of COMP (m <= 16 and m <= 30) from r_tables_46.out for comparison with the text's test list."""
import random, re
import numpy as np
import r_brute as RB

rnd = random.Random(8)
tot = 0; worst = 0; nonzero = 0
for n in (21, 63, 105, 147, 315, 735):
    E = RB.signs(8); divs7 = [d for d in RB.divisors(n) if d % 7 == 0]
    for it in range(400):
        res7 = list(range(7)) + [rnd.randrange(7)]
        co = n // 7 if n % 49 else n // 49
        style = rnd.randrange(3)
        B = []
        for r in res7:
            # an element with residue r modulo 7 and a random or shaped rest
            while True:
                x = rnd.randrange(n) if style == 0 else (rnd.choice([0, 1, 2, 3, 5, 6, 10, 15]) * (n // 3 if style == 1 else 1) + 7 * rnd.randrange(3)) % n
                x = (x - (x % 7) + r) % n if n % 7 == 0 else x
                if x % 7 == r:
                    break
            B.append(x)
        u = np.zeros(256, dtype=bool)
        for d in divs7:
            u |= RB.zero_rows(E, RB.V(d)[[b % d for b in B]])
        c = int(u.sum()); tot += 1; worst = max(worst, c); nonzero += c > 0
print("eight elements, pattern (2,1,1,1,1,1,1) modulo 7, moduli 21, 63, 105, 147, 315, 735: %d multisets; largest number of signings bad at some d divisible by 7: %d (claim: at most 2); multisets with some: %d" % (tot, worst, nonzero))
s16 = s30 = 0
for line in open("r_tables_46.out"):
    mm = re.match(r'(\d+) \|.*\((\d+)\)', line)
    if mm:
        m, k = int(mm.group(1)), int(mm.group(2))
        if m <= 16: s16 += k
        if m <= 30: s30 += k
print("families (j_p) with at least two primes and a nonzero term: %d for m <= 16, %d for m <= 30 (text: 474 and 37,018)" % (s16, s30))

# built cases: six single residues modulo 7 in one class modulo 3, the pair in the two other classes modulo 3
import itertools
built = 0; worst2 = 0; exact2 = 0
for n in (21, 63, 105, 315, 735):
    E = RB.signs(8); divs7 = [d for d in RB.divisors(n) if d % 7 == 0]
    for it in range(150):
        B = []
        s0 = rnd.randrange(3)
        for r in range(1, 7):
            B.append(next(x for x in iter(lambda: rnd.randrange(n), None) if x % 7 == r and x % 3 == s0))
        for s in ((s0 + 1) % 3, (s0 + 2) % 3):
            B.append(next(x for x in iter(lambda: rnd.randrange(n), None) if x % 7 == 0 and x % 3 == s))
        u = np.zeros(256, dtype=bool)
        for d in divs7:
            u |= RB.zero_rows(E, RB.V(d)[[b % d for b in B]])
        c = int(u.sum()); built += 1; worst2 = max(worst2, c); exact2 += c == 2
        if c:
            # the bad ones must be: six singles one sign, the pair the opposite sign
            rows = E[u]
            assert all(len(set(row[:6])) == 1 and row[6] == row[7] == -row[0] for row in rows), B
print("built cases (six singles in one class modulo 3, the pair in the two others) on Z_21, 63, 105, 315, 735: %d multisets; largest number of signings bad at some d divisible by 7: %d; exactly 2 in %d; the bad ones always 'six singles v, pair -v'" % (built, worst2, exact2))
