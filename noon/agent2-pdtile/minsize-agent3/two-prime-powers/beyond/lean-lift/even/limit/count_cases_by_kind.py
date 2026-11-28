"""The cases (multiset, d, x) of test_two_factors.py by kind: class of x occupied (a >= 1) or empty (a = 0, where the
bound of Lemma 1 is c_m).  Same loops as the test, without the signings.  (agent3, 28 November 2026, after the reader
of section 20 asked for the kind of the count.)"""
import itertools
tot = occ = emp = 0
for n, mmax in ((3, 10), (5, 8), (7, 7), (9, 8), (15, 6), (21, 5), (25, 5), (27, 5), (45, 4), (105, 3)):
    for m in range(2, mmax + 1):
        for rest in itertools.combinations_with_replacement(range(n), m - 1):
            xs = (0,) + rest
            for d in range(2, n + 1):
                if n % d: continue
                sizes = [0] * d
                for b in xs: sizes[b % d] += 1
                for a in sizes:
                    if a == m: continue
                    tot += 1
                    if a >= 1: occ += 1
                    else: emp += 1
print(f"cases {tot}: class occupied (a >= 1) in {occ}, empty (a = 0) in {emp}")
