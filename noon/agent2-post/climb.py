"""Lists of L blind guesses that leave many classes (not necessarily all apart), by the same climbing as static.py; prints the best few as openings.
usage: python -I climb.py n k L seed tries > openings"""
import sys, itertools
import numpy as np
n, k, L, seed, tries = map(int, sys.argv[1:6]); N = k ** n; rng = np.random.default_rng(seed)
D = np.array(list(itertools.product(range(k), repeat=n)))
black = (D[:, None, :] == D[None, :, :]).sum(2); counts = np.stack([(D == c).sum(1) for c in range(k)], 1)
A = (black * (n + 1) + np.minimum(counts[:, None, :], counts[None, :, :]).sum(2) - black).astype(np.int64)
def classes(lst):
    key = np.zeros(N, dtype=np.int64)
    for g in lst: key = key * 32 + A[g]
    _, c = np.unique(key, return_counts=True); return len(c), int(c.max())
found = {}
for restart in range(tries):
    lst = list(rng.integers(0, N, L)); best = classes(lst)[0]
    for sweep in range(40):
        j = int(rng.integers(0, L)); rest = np.zeros(N, dtype=np.int64)
        for i, g in enumerate(lst):
            if i != j: rest = rest * 32 + A[g]
        _, rid = np.unique(rest, return_inverse=True)
        score = np.array([len(np.unique(rid * 32 + A[g])) for g in range(N)]); top = np.nonzero(score == score.max())[0]
        if score.max() >= best: lst[j] = int(rng.choice(top)); best = int(score.max())
    found[tuple(sorted(lst))] = classes(lst)
rows = sorted(found.items(), key=lambda kv: (-kv[1][0], kv[1][1]))
print(f"best of {len(rows)} lists: {rows[0][1][0]} classes, largest {rows[0][1][1]}; tenth: {rows[min(9, len(rows) - 1)][1]}", file=sys.stderr)
for lst, _ in rows[:30]:
    for first in range(L): print(" ".join(map(str, (lst[first],) + lst[:first] + lst[first + 1:])))
