"""Test of the structure statement behind the four-hypothesis form of Lemma A (agent3 / Yonder).
Claim (p != q primes, M = p^4 q^2, |A| = p^2 q):  if Phi_q, Phi_{p^3 q^2}, Phi_{p^2 q^2} divide A(X) then for every j in Z_q the
p^2 elements of A that are = j mod q lie in ONE class mod p and ONE class mod q^2, one in each of the p^2 classes
mod p^3 above that class mod p.
Forward direction (the one the proof uses): sets satisfying the three divisibilities are found by HiGHS with random
linear objectives, re-verified by exact polynomial division, and tested for the structure.
Converse (not needed, a sanity check): random sets built with the structure satisfy the three divisibilities."""
import sys, random, numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from cyclo_exact import divides
from lemma_variants import residues

def has_structure(A, p, q):
    for j in range(q):
        cls = [x for x in A if x % q == j]
        if len(cls) != p * p: return False
        if len({x % p for x in cls}) != 1 or len({x % (q * q) for x in cls}) != 1: return False
        if len({x % p ** 3 for x in cls}) != p * p: return False
    return True

rng = random.Random(7); nprng = np.random.default_rng(7)
for p, q, trials in ((2, 3, 60), (2, 5, 30), (3, 2, 40), (5, 2, 4), (3, 5, 4)):
    M, n = p ** 4 * q * q, p * p * q
    Z = [q, p ** 3 * q * q, p * p * q * q]
    Amat = np.vstack([np.ones((1, M))] + [residues(d, M) for d in Z]).astype(float); rhs = np.zeros(Amat.shape[0]); rhs[0] = n
    found = ok = with_p4 = 0; distinct = set()
    for _ in range(trials):
        res = milp(c=nprng.normal(size=M), constraints=LinearConstraint(Amat, rhs, rhs), integrality=np.ones(M), bounds=Bounds(np.zeros(M), np.ones(M)), options={"time_limit": 120})
        if res.x is None: continue
        A = [i for i in range(M) if res.x[i] > 0.5]
        assert len(A) == n and all(divides(d, A, M) for d in Z)
        found += 1; ok += has_structure(A, p, q); distinct.add(tuple(A)); with_p4 += divides(p ** 4, A, M)
    conv = 0
    for _ in range(200):                                   # converse: build with the structure, test the divisibilities
        A = []
        for j in range(q):
            rho = rng.randrange(p); t = j + q * rng.randrange(q)            # class mod p, class mod q^2
            for r in range(p ** 3):
                if r % p == rho:
                    r4 = r + p ** 3 * rng.randrange(p)                         # any lift to Z_{p^4}
                    A.append(next(x for x in range(r4, M, p ** 4) if x % (q * q) == t))
        A = sorted(A); assert len(set(A)) == n
        conv += all(divides(d, A, M) for d in Z)
    print(f"p={p} q={q} M={M}: solver-found sets with the three divisibilities {found} ({len(distinct)} distinct), with the structure {ok}, "
          f"also divisible by Phi_p^4: {with_p4};  built with the structure 200, satisfying the three divisibilities {conv}", flush=True)
