"""Appendix of proof.md: the pattern by the tree conditions equals the pattern by exact division of the mask polynomial
by the cyclotomic polynomials (pat.py: tree_pattern against exact_pattern_division), on random multisets."""
import sys, random
sys.path.insert(0, "/home/agent3/minsize/prove")
from pat import exact_pattern_division, tree_pattern
from test_tree import rnd_tree, leaves_to_weights, rnd_cosets
rng = random.Random(7)
tot = bad = 0; seen = set()
for (p, q, n, reps) in [(2, 3, 2, 3000), (3, 2, 2, 3000), (2, 3, 3, 3000), (3, 2, 3, 1500), (2, 5, 3, 1500), (5, 2, 2, 1000), (2, 3, 4, 1500),
                        (3, 5, 2, 1000), (2, 7, 3, 800), (3, 2, 4, 400), (2, 3, 5, 400), (7, 3, 2, 300)]:
    for r in range(reps):
        w = leaves_to_weights(p, q, n, rnd_tree(p, q, n, rng, 0)) if r % 2 else rnd_cosets(p, q, n, rng)
        a = tree_pattern(p, q, n, w); b = exact_pattern_division(p, q, n, w)
        tot += 1; seen.add((p, q, n, a))
        if a != b:
            bad += 1
            if bad < 5: print('DIFFER', p, q, n, a, b)
print(f'{tot} random multisets in 12 groups, {len(seen)} distinct (group, pattern) pairs: tree pattern differs from division pattern in {bad}')
