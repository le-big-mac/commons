"""Find a list of L blind guesses whose answers tell every code apart, by climbing: change one guess at a time for the better.
usage: python -I static.py n k L seed      Prints the list, or says that it did not find one (which shows nothing)."""
import sys, itertools
import numpy as np
n, k, L, seed = map(int, sys.argv[1:5]); N = k ** n; rng = np.random.default_rng(seed)
D = np.array(list(itertools.product(range(k), repeat=n)))
black = (D[:, None, :] == D[None, :, :]).sum(2); counts = np.stack([(D == c).sum(1) for c in range(k)], 1)
A = (black * (n + 1) + np.minimum(counts[:, None, :], counts[None, :, :]).sum(2) - black).astype(np.int64)
name = lambda c: "".join(str(x + 1) for x in D[c])
def classes(lst):
    key = np.zeros(N, dtype=np.int64)
    for g in lst: key = key * 32 + A[g]
    return len(np.unique(key))
for restart in range(200):
    lst = list(rng.integers(0, N, L)); best = classes(lst)
    for sweep in range(60):
        if best == N: break
        j = int(rng.integers(0, L)); rest = np.zeros(N, dtype=np.int64)
        for i, g in enumerate(lst):
            if i != j: rest = rest * 32 + A[g]
        _, rid = np.unique(rest, return_inverse=True)
        score = np.array([len(np.unique(rid * 32 + A[g])) for g in range(N)]); top = np.nonzero(score == score.max())[0]
        if score.max() >= best: lst[j] = int(rng.choice(top)); best = int(score.max())
    if best == N:
        print(f"{n} pegs, {k} colours: {L} blind guesses that tell all {N} codes apart (restart {restart}): " + " ".join(name(g) for g in lst)); print("L " + " ".join(map(str, lst))); sys.exit(0)
print(f"{n} pegs, {k} colours: no list of {L} found in 200 restarts (this shows nothing)"); sys.exit(1)
