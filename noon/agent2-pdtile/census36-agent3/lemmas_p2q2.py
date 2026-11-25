"""Two lemmas for Z_{p^2 q^2}, tested by integer programming (HiGHS) for several (p, q) (agent3 / Yonder).
Coordinates (u, w) in Z_{p^2} x Z_{q^2};  N(c, t) = #{a in A : u = c mod p, w = t mod q}.
  Lemma X.  |A| = pq, Phi_q | A, Phi_{p q^2} | A   =>   N(c, t) = 1 for all c, t   (hence Phi_p | A and Phi_{pq} | A).
  Lemma Y.  |A| = pq, Phi_q | A, Phi_{p^2 q^2} | A =>   Phi_{p^2 q} | A   (and Phi_{p^2} | A).
Each is asked as: is there a set with the hypotheses and the negated conclusion?  Symmetry (translations, multiplication by units) lets the
violated cell or second difference be fixed.  Controls: the same question with one hypothesis dropped must find a set."""
import sys, itertools, time
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
def model(p, q):
    P2, Q2 = p * p, q * q; n = P2 * Q2; idx = lambda u, w: (u % P2) * Q2 + (w % Q2)
    rows, lo, hi = [], [], []
    def add(coefs, a, b):
        r = np.zeros(n)
        for v, c in coefs: r[v] += c
        rows.append(r); lo.append(a); hi.append(b)
    cells = [(u, w) for u in range(P2) for w in range(Q2)]
    def cnt(f): return [(idx(u, w), 1) for u, w in cells if f(u, w)]
    neg = lambda L: [(v, -c) for v, c in L]
    def additive(boxes):          # boxes[i][j]: list of (var, 1); require all mixed second differences to vanish
        for i in range(1, len(boxes)):
            for j in range(1, len(boxes[0])): add(boxes[i][j] + neg(boxes[0][j]) + neg(boxes[i][0]) + boxes[0][0], 0, 0)
    H = {}
    def Phi_q():
        for t in range(1, q): add(cnt(lambda u, w: w % q == t) + neg(cnt(lambda u, w: w % q == 0)), 0, 0)
    def Phi_p():
        for c in range(1, p): add(cnt(lambda u, w: u % p == c) + neg(cnt(lambda u, w: u % p == 0)), 0, 0)
    def Phi_pq2():
        for t in range(q): additive([[cnt(lambda u, w, c=c, t=t, t2=t2: u % p == c and w == t + q * t2) for t2 in range(q)] for c in range(p)])
    def Phi_p2q2():
        for c in range(p):
            for t in range(q): additive([[cnt(lambda u, w, c=c, t=t, c2=c2, t2=t2: u == c + p * c2 and w == t + q * t2) for t2 in range(q)] for c2 in range(p)])
    def size(k): add([(v, 1) for v in range(n)], k, k)
    N = lambda c, t: cnt(lambda u, w: u % p == c and w % q == t)
    R = lambda c, c2, t: cnt(lambda u, w: u == c + p * c2 and w % q == t)
    def solve():
        r = milp(np.ones(n), constraints=LinearConstraint(np.array(rows), lo, hi), integrality=np.ones(n), bounds=Bounds(0, 1), options={"time_limit": 300})
        return {0: "set found", 2: "infeasible"}.get(r.status, f"status {r.status}")
    return dict(add=add, size=size, Phi_q=Phi_q, Phi_p=Phi_p, Phi_pq2=Phi_pq2, Phi_p2q2=Phi_p2q2, N=N, R=R, neg=neg, solve=solve, rows=rows, lo=lo, hi=hi)
def ask(p, q, lemma, variant, drop=None):
    m = model(p, q)
    if drop != "size": m["size"](p * q)
    if drop != "Phi_q": m["Phi_q"]()
    if lemma == "X":
        if drop != "deep": m["Phi_pq2"]()
        if variant == "zero": m["add"](m["N"](0, 0), 0, 0)                       # N(0,0) = 0
        else: m["add"](m["N"](0, 0), 2, np.inf)                                  # N(0,0) >= 2
    else:
        if drop != "deep": m["Phi_p2q2"]()
        # not Phi_{p^2 q}: in the class c = 0, the array (c2, t) -> R(0; c2, t) has a nonzero mixed second difference at (0,1),(0,1)
        m["add"](m["R"](0, 0, 0) + m["R"](0, 1, 1) + m["neg"](m["R"](0, 0, 1)) + m["neg"](m["R"](0, 1, 0)), 1, np.inf)
    return m["solve"]()
t0 = time.time()
for p, q in [(2, 3), (3, 2), (2, 5), (5, 2), (3, 5), (5, 3), (2, 7), (7, 2)]:
    out = []
    for lemma, variants in (("X", ("zero", "two")), ("Y", ("d",))):
        for v in variants:
            out.append(f"{lemma}/{v}: {ask(p, q, lemma, v)}")
            for d in ("size", "Phi_q", "deep"): out.append(f"[-{d}: {ask(p, q, lemma, v, d)}]")
    print(f"(p, q) = ({p}, {q}), M = {p * p * q * q}: " + " ".join(out) + f"   ({time.time() - t0:.0f} s)", flush=True)
