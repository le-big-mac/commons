# usage: python3 -I small_check.py NMAX
# My own check (reads no download): for odd n and every multiset B of m residues (m = 3, 4),
# count the signings whose signed sum vanishes at some n-th root of unity (floating point, tolerance 1e-9),
# and compare with the hand derivation: m = 4 -> exactly the 6 signings with sign-sum 0; m = 3 -> a subset of {+++, ---}.
import sys, cmath, itertools
nmax = int(sys.argv[1])
for m in (3, 4):
    worst = 0; ok = True; cases = 0
    for n in range(1, nmax + 1, 2):
        roots = [cmath.exp(2j * cmath.pi * k / n) for k in range(n)]
        for B in itertools.combinations_with_replacement(range(n), m):
            if B[0] != 0:
                continue  # translation does not change the bad set
            cases += 1
            bad = []
            for eps in itertools.product((1, -1), repeat=m):
                if any(abs(sum(e * roots[(k * b) % n] for e, b in zip(eps, B))) < 1e-9 for k in range(n)):
                    bad.append(eps)
            worst = max(worst, len(bad))
            if m == 4 and sorted(bad) != sorted(e for e in itertools.product((1, -1), repeat=4) if sum(e) == 0):
                ok = False; print("m=4 mismatch", n, B, len(bad))
            if m == 3 and not set(bad) <= {(1, 1, 1), (-1, -1, -1)}:
                ok = False; print("m=3 mismatch", n, B, bad)
    print("m =", m, "odd n up to", nmax, "multisets (first element 0):", cases, "largest bad count:", worst, "of", 2 ** m, "| agrees with hand derivation:", ok)
