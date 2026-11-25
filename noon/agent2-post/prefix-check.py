"""Check the files of openings: the classes' sizes add up to every ordered list (so none is missed or counted twice), and the count after 1123
is Goddard's 130.   usage: python -I prefix-check.py > prefix-check.out"""
import itertools, numpy as np
n, k = 4, 6; N = k ** n
digits = np.array(list(itertools.product(range(k), repeat=n))); weights = k ** np.arange(n - 1, -1, -1)
G = np.array([(np.array(cp)[digits[:, list(pp)]] * weights).sum(1) for pp in itertools.permutations(range(n)) for cp in itertools.permutations(range(k))], dtype=np.int32)
name = lambda c: "".join(str(x + 1) for x in digits[c])
for L in (1, 2, 3):
    tot = 0; lines = [list(map(int, l.split())) for l in open(f"openings-4-6-{L}.txt")]
    for t in lines:
        H = G
        for c in t: H = H[H[:, c] == c]
        tot += len(G) // len(H)
    print(f"openings of {L}: {len(lines)} classes; their sizes add to {tot}; all ordered lists of {L} codes: {N ** L}; {'equal' if tot == N ** L else 'NOT EQUAL'}")
    if L == 1: print("  the single openings: " + ", ".join(name(t[0]) for t in lines))
    if L == 2:
        import collections; c = collections.Counter(name(t[0]) for t in lines); print("  pairs by their first code: " + ", ".join(f"{a}: {b}" for a, b in sorted(c.items())))
