# The page's wording of the answer against Theorem 1 of the paper, on every pattern for many (p, q, n):
# first case: the page's single value must be the theorem's; second case: the theorem's value must be one of
# the page's two, and the x = 0 one when k' = 0. Also counts how often each clause that names p decides x.
from itertools import combinations
from rules import page_rule, theorem1
tot = c1 = c2 = bad = two = 0
full_F = 0
for p in (2, 3, 5, 7):
    for q in (2, 3, 5, 7):
        if p == q: continue
        for n in range(0, 7):
            M = p**n * q
            ds = [p**a for a in range(1, n + 1)] + [q] + [p**a * q for a in range(1, n + 1)]
            for r in range(len(ds) + 1):
                for c in combinations(ds, r):
                    pat = frozenset(c); tot += 1
                    allowed = page_rule(M, p, n, q, pat); thm = theorem1(M, p, n, q, pat)
                    if q not in pat:
                        c1 += 1
                        if allowed != {thm}: bad += 1
                    else:
                        c2 += 1
                        if thm not in allowed: bad += 1
                        if len(allowed) == 2: two += 1
                        if all(p**a * q in pat for a in range(1, n + 1)): full_F += 1
print(f"patterns {tot} over 12 pairs (p,q) from 2,3,5,7 and n = 0..6: first case {c1}, second case {c2}; page differs from Theorem 1: {bad};"
      f" second-case patterns where the page leaves two values open: {two};"
      f" second-case patterns with balance at every p^a q (the page's 'smallest power' does not exist): {full_F}")
