# Check, for every 3-element multiset of residues mod n, how many of the three
# one-minus signings (-,+,+), (+,-,+), (+,+,-) vanish at some n-th root of unity.
# Claim to test: at most one of them fails. Floating point, tolerance 1e-9.
import cmath, itertools, sys
worst = 0
for n in range(1, 61):
    z = [cmath.exp(2j * cmath.pi * k / n) for k in range(n)]
    for a, b, c in itertools.combinations_with_replacement(range(n), 3):
        fails = 0
        for s in ((-1, 1, 1), (1, -1, 1), (1, 1, -1)):
            if any(abs(s[0] * z[(a * k) % n] + s[1] * z[(b * k) % n] + s[2] * z[(c * k) % n]) < 1e-9 for k in range(n)):
                fails += 1
        if fails > worst:
            worst = fails
            print("n", n, "B", (a, b, c), "failing one-minus signings:", fails)
print("largest number of failing one-minus signings, n <= 60:", worst)
