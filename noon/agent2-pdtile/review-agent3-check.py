"""Independent sanity check of agent2's two necessary conditions: every set that properly tiles Z_M (and so
pd-tiles) must satisfy (a) #Fourier zeros >= |A|-1 and (b) |A-A| <= M - M/|A| + 1. My own tiling test."""
import itertools, cmath, sys
def tiles(A, M):
    n = len(A)
    if M % n: return False
    A = sorted(A); m = M // n
    # backtracking: choose translates covering 0..M-1 exactly once
    def rec(covered, first):
        if covered == (1 << M) - 1: return True
        x = next(i for i in range(M) if not covered >> i & 1)          # smallest uncovered must be covered by a translate
        for a in A:
            t = (x - a) % M; mask = 0; ok = True
            for b in A:
                bit = 1 << ((b + t) % M)
                if covered & bit or mask & bit: ok = False; break
                mask |= bit
            if ok and rec(covered | mask, 0): return True
        return False
    return rec(0, 0)
for M in (12, 16, 18, 20, 24):
    tot = bad = 0; tight_a = tight_b = 0
    for n in range(2, M):
        if M % n: continue
        for rest in itertools.combinations(range(1, M), n - 1):
            A = (0,) + rest
            if not tiles(A, M): continue
            tot += 1
            z = sum(1 for k in range(1, M) if abs(sum(cmath.exp(2j * cmath.pi * k * a / M) for a in A)) < 1e-9)
            d = len({(x - y) % M for x in A for y in A})
            if z < n - 1 or d > M - M / n + 1 + 1e-9: bad += 1; print("VIOLATION", M, A, z, d)
            tight_a += (z == n - 1); tight_b += (abs(d - (M - M / n + 1)) < 1e-9)
    print(f"M={M}: {tot} tiling sets containing 0; violations of either condition: {bad}; (a) tight for {tight_a}, (b) tight for {tight_b}")
