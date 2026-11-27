"""Proposition 20 where r^2 | N (k >= 2), exhaustively on small supports: N = 9, 18, 27 with r = 3 (j = 1 and 2), N = 25 with
r = 5 (j = 1): every multiset whose support is a set of at most 3 residues containing 0 (a translate changes nothing), with
every choice of multiplicities 1..r^j on it, not all r^j."""
import itertools, random
from prop_test import check, vr
rnd = random.Random(2); tot = fail = 0
for N, r, j, smax in [(9, 3, 1, 4), (18, 3, 1, 3), (27, 3, 1, 3), (9, 3, 2, 3), (18, 3, 2, 2), (25, 5, 1, 3), (9, 3, 3, 2)]:
    t = f = 0
    for size in range(1, smax + 1):
        for rest in itertools.combinations(range(1, N), size - 1):
            supp = (0,) + rest
            for ms in itertools.product(range(1, r ** j + 1), repeat=size):
                if all(m == r ** j for m in ms): continue
                ok, cases, _ = check(dict(zip(supp, ms)), N, r, j, rnd)
                t += 1; f += (not ok)
    tot += t; fail += f
    print(f'N={N} (k={vr(N, r)}) r={r} j={j}, supports of at most {smax} residues with 0: {t} multisets, failures {f}', flush=True)
print(f'total {tot}, failures {fail}')
