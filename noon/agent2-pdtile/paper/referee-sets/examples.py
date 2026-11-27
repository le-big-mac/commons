"""The example of the three texts, by my own exact tools.
(1) Z_6: every multiset of 5 elements whose pattern is exactly {6}; that each has a repeated element; that they are exactly
    the sums 'pair of opposite elements + triangle' (3 pairs x 2 triangles), and that a pair and a triangle always share
    an element; that nothing smaller has the pattern.
(2) Z_18: {0, 1, 2, 4, 10}: its pattern among the divisors of 18, its reduction modulo 6; the same five numbers on Z_12.
(3) Z_36: {0, 6, 1, 5, 9} (the page's opening example, as the page uses it on 36 hours)."""
import itertools, collections
from cyc import pattern, divisors
ms = []
for k in range(1, 6):
    for c in itertools.combinations_with_replacement(range(6), k):
        mult = dict(collections.Counter(c))
        if pattern(mult, 6) == frozenset({6}):
            ms.append(c)
print('Z_6, multisets with pattern exactly {6}, by size:', dict(collections.Counter(len(c) for c in ms)))
five = [c for c in ms if len(c) == 5]
print('  those of 5 elements:', five)
print('  each has a repeated element:', all(len(set(c)) < 5 for c in five), '; largest multiplicity:', max(max(collections.Counter(c).values()) for c in five))
pairs = [(a, a + 3) for a in range(3)]; tris = [(b, b + 2, b + 4) for b in range(2)]
sums = sorted(tuple(sorted(p + t)) for p in pairs for t in tris)
print('  pair + triangle (3 x 2):', sums, '; the same list:', sums == sorted(five))
print('  a pair and a triangle share exactly one element in every case:', all(len(set(p) & set(t)) == 1 for p in pairs for t in tris))
S = {0: 1, 1: 1, 2: 1, 4: 1, 10: 1}
print('Z_18, {0,1,2,4,10}: pattern among the divisors of 18:', sorted(pattern(S, 18)), '; reduced modulo 6:', sorted(x % 6 for x in S))
print('Z_12, {0,1,2,4,10}: pattern among the divisors of 12:', sorted(pattern(S, 12)))
print('Z_6, {0,1,2,4,4}: pattern:', sorted(pattern({0: 1, 1: 1, 2: 1, 4: 2}, 6)))
T = {0: 1, 6: 1, 1: 1, 5: 1, 9: 1}
print('Z_12, {0,6,1,5,9}: pattern:', sorted(pattern(T, 12)), '; on Z_36:', sorted(pattern(T, 36)))
# the recipe on {0,1,2,4,4}, r = 3: what it gives for each admissible x1 (the text does not say {0,1,2,4,10} is the recipe's)
import random
from prop_test import one_step
for x1 in (0, 1, 2, 4):
    out, case = one_step({0: 1, 1: 1, 2: 1, 4: 2}, 6, 3, 1, random.Random(1), x1=x1)
    print(f'  recipe of the proof on {{0,1,2,4,4}} with x1 = {x1}: {sorted(out)}  pattern on Z_18: {sorted(pattern(out, 18))}')
