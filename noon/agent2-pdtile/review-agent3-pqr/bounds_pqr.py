"""Lemmas 1 and 2 of agent2's pqr-agent2.md against D+ computed by my own linear program, for every pattern of several triples
(agent3 / Yonder).  D+ = M / min{ sum f : f(0) = 1, f >= 0, fhat >= 0, fhat = 0 at characters whose order is not 1 and not in Z };
f may be taken constant on elements of equal order, which leaves 7 variables."""
import itertools, numpy as np
from scipy.optimize import linprog
def setup(pr):
    M = pr[0] * pr[1] * pr[2]; subs = [s for r in range(4) for s in itertools.combinations(range(3), r)]
    val = lambda s: int(np.prod([pr[x] for x in s])) if s else 1
    size = lambda e: int(np.prod([pr[x] - 1 for x in e])) if e else 1
    csum = lambda d, e: int(np.prod([(-1 if x in d else pr[x] - 1) for x in e])) if e else 1
    def dplus(Z):                                         # Z: set of index-subsets (nonempty)
        var = subs[1:]; c = [size(e) for e in var]; A_ub, b_ub, A_eq, b_eq = [], [], [], []
        for d in subs:
            row = [csum(d, e) for e in var]
            if not d or d in Z: A_ub.append([-v for v in row]); b_ub.append(1.0)
            else: A_eq.append(row); b_eq.append(-1.0)
        r = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq or None, b_eq=b_eq or None, bounds=[(0, None)] * len(var), method="highs"); assert r.status == 0
        return M / (1 + r.fun)
    return M, subs[1:], val, dplus
triples = [(2, 3, 5), (2, 3, 7), (2, 5, 7), (3, 5, 7), (2, 3, 11), (2, 7, 11), (3, 5, 11), (5, 7, 11), (2, 3, 13), (7, 11, 13), (2, 3, 101), (2, 97, 101), (89, 97, 101)]
tot = dict(l1=0, l1_att=0, l1_bad=0, l2=0, l2_att=0, l2_bad=0)
for pr in triples:
    M, divs, val, dplus = setup(pr); loc = dict(l1=0, l1_att=0, l1_bad=0, l2=0, l2_att=0, l2_bad=0)
    for m in range(1, 8):
        for Zt in itertools.combinations(divs, m):
            Z = set(Zt); d = dplus(Z)
            for r in (1, 2, 3):
                for U in itertools.combinations(range(3), r):
                    if all(any(x in dd for x in U) for dd in Z):
                        b = val(U); loc["l1"] += 1; loc["l1_att"] += abs(d - b) < 1e-6 * b; loc["l1_bad"] += d > b * (1 + 1e-7)
            for z in range(3):
                x, y = [w for w in range(3) if w != z]
                if (x, y) not in Z and (z,) not in Z and (0, 1, 2) not in Z:
                    b = max(pr[x], pr[y]); loc["l2"] += 1; loc["l2_att"] += abs(d - b) < 1e-6 * b; loc["l2_bad"] += d > b * (1 + 1e-7)
    for k in tot: tot[k] += loc[k]
    print(f"{pr}: Lemma 1 applicable {loc['l1']} times, attained {loc['l1_att']}, violated {loc['l1_bad']};  Lemma 2 applicable {loc['l2']}, attained {loc['l2_att']}, violated {loc['l2_bad']}")
print(f"all {len(triples)} triples, 127 nonempty patterns each: Lemma 1 {tot['l1']} / attained {tot['l1_att']} / violated {tot['l1_bad']};  Lemma 2 {tot['l2']} / attained {tot['l2_att']} / violated {tot['l2_bad']}")
