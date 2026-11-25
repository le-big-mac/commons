r"""For the solver test of Lemma 4: in how many of the problems does a set meeting the PREMISE exist at all?
(agent3 / Yonder.)  Premise: Phi_q | A, |A| = p^|E| q, Phi_{p^l} | A for l in E, Phi_{p^b q} | A (b not in E), some a in E, a < b.
If no set meets the premise, 'no counterexample' says nothing.  Any set found is verified exactly, and its E is checked
to be exactly E (forced by |A| = p^|E| q).   usage: milp_premise.py p n q"""
import sys, itertools, numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
sys.path.insert(0, "/home/agent3/review2")
from lemma_variants import residues
from cyclo_exact import divides
p, n, q = (int(x) for x in sys.argv[1:4]); M = p ** n * q
levels = range(1, n + 1); tot = feas = 0; inF = 0
for E in itertools.chain.from_iterable(itertools.combinations(levels, r) for r in range(1, n + 1)):
    e = len(E)
    for b in levels:
        if b in E or not any(a < b for a in E) or p ** e * q > M: continue
        eqs = [residues(q, M), np.ones((1, M))] + [residues(p ** l, M) for l in E] + [residues(p ** b * q, M)]
        A_ = np.vstack(eqs).astype(float); rhs = np.zeros(A_.shape[0]); rhs[len(eqs[0])] = p ** e * q
        r = milp(c=np.random.default_rng(1).normal(size=M), constraints=LinearConstraint(A_, rhs, rhs), integrality=np.ones(M), bounds=Bounds(np.zeros(M), np.ones(M)), options={"time_limit": 60})
        tot += 1
        if r.status == 0:
            S = [i for i in range(M) if r.x[i] > 0.5]
            assert len(S) == p ** e * q and divides(q, S, M) and divides(p ** b * q, S, M) and {l for l in levels if divides(p ** l, S, M)} == set(E)
            feas += 1; inF += all(divides(p ** a * q, S, M) for a in E if a < b)
print(f"p={p} n={n} q={q} M={M}: (E, b) cases {tot}; a set meeting the premise exists in {feas}; in each such set found, the conclusion holds: {inF}")
