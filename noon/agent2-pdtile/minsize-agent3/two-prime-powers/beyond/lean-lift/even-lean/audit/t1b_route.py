"""The steps of the plan's route for T (the plan has been read by nobody), on random valued families, all signings:
  F_d := {signings : csum(2^d, r) = 0 for every r < 2^d}
  (a) F_(d+1) is contained in F_d          (b) #{bad at level j+1} = #F_j
  (c) F_(j+1) is contained in {bad at j+1} and in {bad at 0}; F_0 = {bad at 0}
  (d) #{some level j <= K bad} + #F_K <= 2 #{bad at 0}
Word-for-word definitions (no fast code)."""
import random

random.seed(12)
GROUPS = {'Z': 0, 'Z/2': 2, 'Z/3': 3, 'Z/4': 4, 'Z/6': 6}
VALS = {'Z': [-2, -1, 0, 1, 2], 'Z/2': [0, 1], 'Z/3': [0, 1, 2], 'Z/4': [0, 1, 2, 3], 'Z/6': [0, 1, 2, 3, 4, 5]}


def csum(pos, val, eps, M, r, N):
    s = sum(eps[k] * val[k] for k in range(len(pos)) if pos[k] % M == r)
    return s % N if N else s


def bad(pos, val, eps, j, N):
    if j == 0:
        s = sum(eps[k] * val[k] for k in range(len(pos)))
        return (s % N if N else s) == 0
    jj = j - 1
    return all(csum(pos, val, eps, 2 ** (jj + 1), r, N) == csum(pos, val, eps, 2 ** (jj + 1), r + 2 ** jj, N)
               for r in range(2 ** jj))


def inF(pos, val, eps, d, N):
    return all(csum(pos, val, eps, 2 ** d, r, N) == 0 for r in range(2 ** d))


fam = 0
fail = {'a': 0, 'b': 0, 'c': 0, 'd': 0}
for trial in range(2500):
    g = random.choice(list(GROUPS))
    N = GROUPS[g]
    m = random.randint(0, 7)
    top = random.choice([2, 4, 8, 16])
    pos = [random.randrange(0, top) for _ in range(m)]
    val = [random.choice(VALS[g]) for _ in range(m)]
    K = 5
    sig = [[1 if (t >> k) & 1 else -1 for k in range(m)] for t in range(1 << m)]
    B = [[bad(pos, val, e, j, N) for e in sig] for j in range(K + 1)]
    F = [[inF(pos, val, e, d, N) for e in sig] for d in range(K + 1)]
    fam += 1
    for d in range(K):
        if any(F[d + 1][s] and not F[d][s] for s in range(len(sig))):
            fail['a'] += 1
        if sum(B[d + 1]) != sum(F[d]):
            fail['b'] += 1
        if any(F[d + 1][s] and not (B[d + 1][s] and B[0][s]) for s in range(len(sig))):
            fail['c'] += 1
    if F[0] != B[0]:
        fail['c'] += 1
    for KK in range(K + 1):
        q = sum(1 for s in range(len(sig)) if any(B[j][s] for j in range(KK + 1)))
        if q + sum(F[KK]) > 2 * sum(B[0]):
            fail['d'] += 1
print(f"plan's route for T on {fam} random valued families (values in Z, Z/2, Z/3, Z/4, Z/6, 0 allowed; up to 7 "
      f"elements; levels up to 5): failures of (a), (b), (c), (d): {fail}")
