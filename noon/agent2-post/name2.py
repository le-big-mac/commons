"""m(j) again, written apart from name.c, in numpy and with no shortcut: every triple of blind questions (one from each class under
renaming and reordering) with every fourth; for each, the codes left unnamed by four rounds of naming, straight from the definition.
usage: python -I name2.py j PART PARTS   (j = 1, 2, 3 or 4; the openings of j-1 codes are split into PARTS, this run takes PART)
Prints the least found in its part and a list of questions that gives it."""
import sys, itertools
import numpy as np
j, part, parts = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]); n, k = 4, 6; N = k ** n
D = np.array(list(itertools.product(range(k), repeat=n)))
black = (D[:, None, :] == D[None, :, :]).sum(2); cnt = np.stack([(D == c).sum(1) for c in range(k)], 1)
A = (black * (n + 1) + np.minimum(cnt[:, None, :], cnt[None, :, :]).sum(2) - black)          # A[g, s]: the answer to g when the code is s
_, A = np.unique(A, return_inverse=True); A = A.reshape(N, N); F = int(A.max()) + 1            # answers numbered 0 .. F-1
name = lambda c: "".join(str(x + 1) for x in D[c]); allg = np.arange(N)
def classes(keys):                                                                             # number the classes of a key
    u, inv = np.unique(keys, return_inverse=True); return inv, len(u)
def least(prefix):
    """the least, over every last question, of the codes left unnamed; and the last question that gives it"""
    ids = [np.zeros(N, dtype=np.int64)]; sizes = [1]
    for g in prefix: i, c = classes(ids[-1] * F + A[g]); ids.append(i); sizes.append(c)       # ids[l]: class under the first l answers
    live = np.ones(N, dtype=bool); live[list(prefix)] = False
    rows = np.repeat(allg, N); cols = np.tile(allg, N)                                         # every (last question, code)
    w = (live[cols] & (rows != cols)).astype(np.int64)                                         # the questions themselves are sent already
    key = ids[-1][cols] * F + A[rows, cols]; C = sizes[-1] * F
    counts = np.bincount(rows * C + key, weights=w, minlength=N * C).reshape(N, sizes[-1], F)  # codes in each last-round state
    u = np.maximum(counts - 1, 0).sum(2); u = np.maximum(u - 1, 0) if len(prefix) else u       # last round names one each; then this level's one
    for l in range(len(prefix) - 1, 0, -1):                                                    # fold up to the first answer's classes
        par = np.zeros(sizes[l + 1], dtype=np.int64); par[ids[l + 1]] = ids[l]                 # each class's parent
        up = np.zeros((N, sizes[l])); np.add.at(up.T, par, u.T); u = np.maximum(up - 1, 0)
    tot = u.sum(1) if len(prefix) else u.sum(1)
    b = int(np.argmin(tot)); return int(tot[b]), b
if j == 1:
    # one question: classes under its answer, one code named in each
    best = min((sum(max(0, c - 1) for c in np.bincount(A[g][np.arange(N) != g])), g) for g in range(N)); print(f"least {best[0]} with {name(best[1])}; 1296 lists tried"); sys.exit()
lines = [list(map(int, l.split())) for l in open(f"openings-4-6-{j - 1}.txt")][part::parts]; best = (10 ** 9, None)
for pre in lines:
    t, g = least(pre)
    if t < best[0]: best = (t, pre + [g])
print(f"least {best[0]} with {' '.join(name(c) for c in best[1])}; {len(lines)} openings of {j - 1}, each with every one of {N} last questions")
