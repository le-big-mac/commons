"""Put a file of blind openings in order, the most promising first: by the largest class the opening's own answers leave, then by how many classes.
usage: python -I order.py n k openings.txt > ordered.txt"""
import sys, itertools
import numpy as np
n, k = int(sys.argv[1]), int(sys.argv[2]); N = k ** n
D = np.array(list(itertools.product(range(k), repeat=n)))
black = (D[:, None, :] == D[None, :, :]).sum(2)
counts = np.stack([(D == c).sum(1) for c in range(k)], 1); total = np.minimum(counts[:, None, :], counts[None, :, :]).sum(2)
A = black * (n + 1) + (total - black)                                           # answer to guess g for code s
rows = []
for line in open(sys.argv[3]):
    t = list(map(int, line.split())); key = np.zeros(N, dtype=np.int64)
    for g in t: key = key * 64 + A[g]
    _, c = np.unique(key, return_counts=True); rows.append((int(c.max()), -len(c), line.strip()))
rows.sort()
for r in rows: print(r[2])
print(f"best opening leaves a largest class of {rows[0][0]} in {-rows[0][1]} classes; worst {rows[-1][0]} in {-rows[-1][1]}", file=sys.stderr)
