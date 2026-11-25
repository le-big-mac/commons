"""Referee: Lemma D on pairs of tiles.  A1, A2 tiles of Z_{M'} (so weak tiles with (T1); 'no orphan' is checked on each),
of the same size.  Is there a common weak complement (f >= 0, f(0) = 1, 1_{A1} * f = 1_{A2} * f = 1)?  Linear feasibility,
scipy/HiGHS in floating point.  Lemma D: if yes, then S_{A1} = S_{A2}.
usage: lemmaD.py p a q b npairs [seed]"""
import sys, random, itertools
import numpy as np
from scipy.optimize import linprog
from lemmatests import Grp
p, a, q, b, n = (int(v) for v in sys.argv[1:6]); random.seed(int(sys.argv[6]) if len(sys.argv) > 6 else 1)
G = Grp(p, a, q, b); M = G.M
PP = [(l, 0) for l in range(1, a + 1)] + [(0, m) for m in range(1, b + 1)]
def tile_with_S(S):
    """a random tile whose prime-power zeros are S: a random complement of the digit set of the other prime powers"""
    B = G.digit([s for s in PP if s not in S]); A = G.random_complement(B)
    if A is None: return None
    u = random.choice([t for t in range(1, M) if t % p and t % q]); sh = random.randrange(M)
    return sorted({(u * x + sh) % M for x in A})
def common(A1, A2):
    rows = []; rhs = []
    for A in (A1, A2):
        for v in range(M):
            r = np.zeros(M)
            for x in A: r[(v - x) % M] += 1
            rows.append(r); rhs.append(1.0)
    r = np.zeros(M); r[0] = 1; rows.append(r); rhs.append(1.0)
    res = linprog(np.zeros(M), A_eq=np.array(rows), b_eq=np.array(rhs), bounds=[(0, None)] * M, method='highs')
    return res.status == 0
stat = {'same S, common complement': 0, 'same S, none': 0, 'different S, none': 0, 'DIFFERENT S WITH A COMMON COMPLEMENT (Lemma D fails)': 0, 'hypotheses not met': 0}
subsets = [frozenset(c) for r in range(len(PP) + 1) for c in itertools.combinations(PP, r)]
done = 0
while done < n:
    S1 = random.choice(subsets)
    same = [S for S in subsets if sum(1 for s in S if s[1] == 0) == sum(1 for s in S1 if s[1] == 0) and len(S) == len(S1)]
    S2 = random.choice(same) if random.random() < 0.8 else S1
    A1 = tile_with_S(S1); A2 = tile_with_S(S2)
    if A1 is None or A2 is None: continue
    Z1 = G.zeros(A1); Z2 = G.zeros(A2); P1 = G.pattern(Z1); P2 = G.pattern(Z2)
    T1 = frozenset(o for o in Z1 if o[0] == 0 or o[1] == 0); T2 = frozenset(o for o in Z2 if o[0] == 0 or o[1] == 0)
    if not (len(A1) == P1[2] and len(A2) == P2[2] and not P1[4] and not P2[4] and T1 == S1 and T2 == S2): stat['hypotheses not met'] += 1; continue
    done += 1; c = common(A1, A2)
    if T1 == T2: stat['same S, common complement' if c else 'same S, none'] += 1
    else: stat['DIFFERENT S WITH A COMMON COMPLEMENT (Lemma D fails)' if c else 'different S, none'] += 1
print(f"Z_{M} = Z_({p}^{a} {q}^{b}): {n} pairs of tiles of equal size: {stat}")
