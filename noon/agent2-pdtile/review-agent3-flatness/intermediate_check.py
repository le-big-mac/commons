"""Intermediate claims in the proofs of Lemma B+ tested on solver-found sets (agent3 / Yonder).
M = p^4 q^2, |B| = p^2 q.
 (I)  Phi_{p^2}, Phi_{p^3}, Phi_{pq} | B   =>  B lies in one class mod p, with p^2 elements in each class mod q.   [B1, B2]
 (II) Phi_{q^2}, Phi_{pq}, Phi_{p^2 q} | B =>  B lies in one class mod q.                                          [B3]
Sets are found by HiGHS with random objectives and re-verified by exact polynomial division."""
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from cyclo_exact import divides
from lemma_variants import residues
rng = np.random.default_rng(11)
def sets(p, q, Z, trials):
    M, n = p ** 4 * q * q, p * p * q
    Amat = np.vstack([np.ones((1, M))] + [residues(d, M) for d in Z]).astype(float); rhs = np.zeros(Amat.shape[0]); rhs[0] = n
    out = set()
    for _ in range(trials):
        res = milp(c=rng.normal(size=M), constraints=LinearConstraint(Amat, rhs, rhs), integrality=np.ones(M), bounds=Bounds(np.zeros(M), np.ones(M)), options={"time_limit": 120})
        if res.x is None: continue
        A = tuple(i for i in range(M) if res.x[i] > 0.5)
        assert len(A) == n and all(divides(d, list(A), M) for d in Z)
        out.add(A)
    return out
for p, q, trials in ((2, 3, 60), (3, 2, 40), (2, 5, 25)):
    S1 = sets(p, q, [p * p, p ** 3, p * q], trials)
    ok1 = sum(len({x % p for x in A}) == 1 and all(sum(1 for x in A if x % q == j) == p * p for j in range(q)) for A in S1)
    S2 = sets(p, q, [q * q, p * q, p * p * q], trials)
    ok2 = sum(len({x % q for x in A}) == 1 for A in S2)
    print(f"p={p} q={q}: (I) {len(S1)} distinct sets, claim holds for {ok1};  (II) {len(S2)} distinct sets, claim holds for {ok2}", flush=True)
