"""The 1954 composite membrane as quoted in arXiv:0809.1320 (Table I: sigma = 3.125, k = 0.4), by this study's exact Bessel matching.
usage: python composite.py > composite.out"""
import sys
sys.path.insert(0, "../drum")
import drum
w = drum.modes(3.125 ** 2, 0.4); half = w[1] / 2; mine = [x / half for x in w]
paper = {(0, 1): 1.0309, (1, 1): 2.0000, (2, 1): 3.0412, (0, 2): 3.1546, (3, 1): 4.0928, (1, 2): 4.2268, (4, 1): 5.1134, (2, 2): 5.3093, (0, 3): 4.9794}
print(f"the composite membrane at a density ratio of 3.125 squared = {3.125 ** 2:.4f} over 0.4 of the radius, with the second mode taken as 2:")
diffs = {}
for (m, n), x in zip(drum.NINE, mine): diffs[(m, n)] = abs(x - paper[(m, n)]); print(f"   ({m},{n}): mine {x:.4f}; the paper's Table I, 'Composite' column {paper[(m, n)]:.4f}; apart by {diffs[(m, n)]:.4f}")
big = max(diffs, key=diffs.get); rest = max(v for k, v in diffs.items() if k != big)
print(f"largest difference {diffs[big]:.4f}, at ({big[0]},{big[1]}); the others are within {rest:.4f}. Largest miss of this disc by this study's measure (lowest mode as base): {100 * drum.miss(3.125 ** 2, 0.4):.2f}%")
