"""Referee: (A1)-(A5) of section 1 checked on all integers up to N for several (p, q, u)."""
from ref_common import set_tables
N = 600
bad = 0
cases = 0
for (p, q) in ((2, 3), (3, 2), (2, 5), (5, 2), (3, 5), (5, 3), (2, 7), (7, 2), (3, 7), (7, 3), (5, 7), (2, 11), (11, 2)):
    inS, inSp, inQ = set_tables(p, q, 4, N)
    for u in range(0, 5):
        if p ** u * q > N // 2:
            continue
        cases += 1
        S = [x for x in range(N + 1) if inS[u][x]]; Sp = [x for x in range(N + 1) if inSp[u][x]]; Q = [x for x in range(N + 1) if inQ[u][x]]
        qz0 = list(range(0, N + 1, q)); qz1 = qz0[1:]
        if u >= 1:   # (A1)
            for x in range(N // p + 1):
                bad += inS[u - 1][x] and not inS[u][p * x]
                bad += inSp[u - 1][x] and not inSp[u][p * x]
                bad += inQ[u - 1][x] and not inQ[u][p * x]
        def sub(A, B, C):
            return sum(1 for a in A for b in B if a + b <= N and not C[a + b])
        bad += sub(S, S, inS[u]) + sub(S, qz0, inS[u]) + sub(Sp, S, inSp[u]) + sub(Sp, qz0, inSp[u]) + sub(S, qz1, inSp[u])   # (A2)
        bad += sub(Q, S, inSp[u]) + sub(Q, qz1, inSp[u])                                                                    # (A3)
        for x in S:                                                                                                       # (A4)
            if x % q == 0:
                bad += not (inQ[u][x] or inSp[u][x])
                bad += x < q * p ** u
        for x in Sp:                                                                                                      # (A5)
            if x % q == 0:
                bad += x < q * p ** u + q
print(f"(A1)-(A5): {cases} triples (p, q, u), integers up to {N}: violations {bad}")
