"""The values that the skeleton's CheckEven.lean expects (and that Lean printed, A0_checkeven.out), recomputed with
a word-for-word transcription of csum and levelBad (independent of t1_twice.py)."""


def csum(pos, val, eps, M, r, N):
    s = 0
    for k in range(len(pos)):
        if (pos[k] if M == 0 else pos[k] % M) == r:
            s += eps[k] * val[k]
    return s % N if N else s


def level_bad(pos, val, eps, j, N):
    if j == 0:
        s = sum(eps[k] * val[k] for k in range(len(pos)))
        return (s % N if N else s) == 0
    jj = j - 1
    return all(csum(pos, val, eps, 2 ** (jj + 1), r, N) == csum(pos, val, eps, 2 ** (jj + 1), r + 2 ** jj, N)
               for r in range(2 ** jj))


def counts(pos, val, N, K):
    m = len(pos)
    some = 0
    at = [0] * (K + 1)
    for t in range(1 << m):
        eps = [1 if (t >> k) & 1 else -1 for k in range(m)]
        lv = [level_bad(pos, val, eps, j, N) for j in range(K + 1)]
        some += any(lv)
        for j in range(K + 1):
            at[j] += lv[j]
    return some, at


cases = [
    ([0, 1], [1, 1], 0, 1, (4, [2, None])),
    ([0, 1, 2], [1, 1, 1], 0, 2, (0, [0, None, None])),
    ([0, 0, 1], [1, 2, 1], 3, 2, (4, [2, None, None])),
    ([0, 1, 2, 3], [1, 1, 1, 1], 0, 3, (8, [6, 6, 4, 0])),
    ([0, 0, 2, 5], [1, -1, 0, 2], 0, 3, (8, [4, 4, 0, 0])),
    ([3, 3, 1, 5], [1, 1, 2, 2], 3, 3, (12, [6, 6, 6, 4])),
    ([0, 1, 1, 2, 7], [1, 2, 3, 4, 1], 5, 3, (8, [6, 6, 4, 0])),
    ([0, 4, 2, 6, 1], [1, 1, 1, 1, 0], 0, 3, (16, [12, 12, 12, 8])),
    ([0, 0, 0, 1], [1, 1, 1, 1], 3, 2, (12, [6, 6, 0])),
]
ok = True
for pos, val, N, K, (some, at) in cases:
    s, a = counts(pos, val, N, K)
    good = s == some and all(x is None or x == y for x, y in zip(at, a))
    ok &= good
    print(f"pos {pos} val {val} in {'Z' if N == 0 else 'Z/' + str(N)} K={K}: mine ({s}, {a}); CheckEven expects "
          f"({some}, {at}): {'equal' if good else 'DIFFERENT'}")
p1 = [level_bad([0, 1, 2, 3], [1, 1, 1, 1], [1, 1, -1, -1], j, 0) for j in range(4)]
p2 = [level_bad([0, 1, 2, 3], [1, 1, 1, 1], [1, -1, 1, -1], j, 0) for j in range(4)]
ok &= p1 == [True, True, False, False] and p2 == [True, False, True, False]
print("levels 0..3 for the signs + + - -:", p1, "; for + - + -:", p2)
e1 = [sum(1 for t in range(1 << m) if sum(1 if (t >> k) & 1 else -1 for k in range(m)) % 3 == 0) for m in range(8)]
ok &= e1 == [1, 0, 2, 2, 6, 10, 22, 42]
print("E1 counts for m = 0..7:", e1)
print("all values that CheckEven.lean expects are right:", ok)
