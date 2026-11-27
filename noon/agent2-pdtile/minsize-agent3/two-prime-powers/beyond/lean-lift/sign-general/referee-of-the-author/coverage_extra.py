"""Referee: on which parts of the result does "every odd n below 118125" rest?  Uses coverage_own."""
from coverage_own import factor, thm2, thm3, thm6_ways, one_repeated, thmP_sorted

LIM = 118125
tot = 0; only23 = []; ab = 0; further = []; rec_only = []
for n in range(1, LIM, 2):
    f = factor(n); tot += 1
    t2, t3 = thm2(f), thm3(f); ways = thm6_ways(n, f)
    assert t2 or t3 or ways, n
    if not ways: only23.append(n)
    if t2 or t3: continue
    if one_repeated(f): ab += 1; continue
    further.append(n)
    if all(k == "P'" for _, k in ways): rec_only.append(n)
print(f'odd n < {LIM}: {tot}, all covered (asserted)')
print(f'covered by Theorems 2, 3 of the earlier result and not by Theorem 6: {only23}')
print(f'not in Theorems 2, 3, covered by Theorem 6 (a) or (b) (at most one repeated prime): {ab}')
print(f'not in Theorems 2, 3 and with two or more repeated primes (the "further cases"): {len(further)}; first {further[:8]}')
print(f'   of these, covered only through the recursion (Theorem P\' with tree levels; Theorem P applies for no choice of q): {len(rec_only)}; first {rec_only[:8]}')
# first n not covered when parts are left out
def first_uncovered(use_further, use_rec):
    for n in range(1, 400000, 2):
        f = factor(n)
        if thm2(f) or thm3(f) or one_repeated(f): continue
        ways = thm6_ways(n, f)
        if use_further and ways and (use_rec or any(k == 'P' for _, k in ways)): continue
        return n
print('first odd n not covered with Theorems 2, 3 and Theorem 6 (a), (b) only:', first_uncovered(False, False))
print('first odd n not covered when Theorem P on digit boxes with repeated digits is added, without the recursion:', first_uncovered(True, False))
print('first odd n not covered with everything:', first_uncovered(True, True))
