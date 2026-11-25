"""Blind openings up to the game's symmetry (any reordering of the pegs, any renaming of the colours): one ordered list of L codes from each class.
usage: python -I prefix.py n k L > openings-n-k-L.txt        Codes are numbers base k, first peg most significant, as lag.c reads them."""
import sys, itertools
import numpy as np
n, k, L = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]); N = k ** n
digits = np.array(list(itertools.product(range(k), repeat=n)))                 # code number -> its pegs
weights = k ** np.arange(n - 1, -1, -1)
perms = []
for pp in itertools.permutations(range(n)):
    for cp in itertools.permutations(range(k)):
        perms.append((np.array(cp)[digits[:, list(pp)]] * weights).sum(1))    # where each code goes
G = np.array(perms, dtype=np.int32)                                            # |G| rows, N columns
def extend(prefix, H, left):
    if left == 0: print(" ".join(map(str, prefix))); return 1
    reps = np.nonzero(H.min(axis=0) == np.arange(N))[0]                        # least member of each orbit of H on the codes
    return sum(extend(prefix + [int(c)], H[H[:, c] == c], left - 1) for c in reps)
count = extend([], G, L)
print(f"{count} openings of {L} for {n} pegs and {k} colours; the symmetry group has {len(G)} members", file=sys.stderr)
