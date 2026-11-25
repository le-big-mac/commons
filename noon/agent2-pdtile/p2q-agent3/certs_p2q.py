"""Z_{p^2 q}: the explicit certificates used in the proof, built and checked for many prime pairs (agent3 / Yonder).
Two kinds of upper bound for D+(Z):
  (S) a set A' whose zero set contains Z            =>  D+(Z) <= |A'|          (Prop. 1(i) of flatness.md + monotonicity)
  (C) a set B no two of whose elements differ by an element with order in Z   =>  D+(Z) <= M/|B|
Each certificate is constructed, its defining property verified directly (exact zero sets; all pairwise differences),
and the resulting bound compared with the exact D+ from agent2's lp.py."""
import sys, itertools
from math import gcd
sys.path.insert(0, "/srv/commons/agent2-pdtile/flat"); sys.path.insert(0, "/home/agent3/review2")
from lp import Setup
from cyclo_exact import divides
def crt(u, w, p, q):                                   # element of Z_M with residues u mod p^2, w mod q
    M = p * p * q
    return next(x for x in range(u, M, p * p) if x % q == w)
def check(p, q):
    M = p * p * q; o = {"p": p, "p2": p * p, "q": q, "pq": p * q, "p2q": M}; S = Setup(M)
    D = lambda Z: S.Dplus([o[z] for z in Z])[0]
    order = lambda x: M // gcd(x, M)
    zeros = lambda A: {z for z in o if divides(o[z], sorted(A), M)}
    mn, mx = min(p, q), max(p, q); res = []
    def S_cert(Z, A, bound):
        A = set(A); assert len(A) == bound and set(Z) <= zeros(A), ("S", Z, p, q)
        assert D(Z) <= bound; res.append((Z, "S", bound, D(Z)))
    def C_cert(Z, B, bound):
        B = sorted(set(B)); bad = {o[z] for z in Z}
        assert not any(order(b - a) in bad for a, b in itertools.combinations(B, 2)), ("C", Z, p, q)
        assert M % len(B) == 0 and M // len(B) == bound and D(Z) <= bound; res.append((Z, "C", bound, D(Z)))
    Hq = [crt(0, w, p, q) for w in range(q)]                        # subgroup of order q
    Hp = [crt(i * p, 0, p, q) for i in range(p)]                    # subgroup of order p
    Hp2 = [crt(u, 0, p, q) for u in range(p * p)]                   # subgroup of order p^2
    Hpq = [crt(i * p, w, p, q) for i in range(p) for w in range(q)] # subgroup of order pq
    Up = [crt(u, 0, p, q) for u in range(p)]                        # one element in each class mod p, one layer
    UpZq = [crt(u, w, p, q) for u in range(p) for w in range(q)]
    # standard tiles: D+(U(S)) <= k(S)
    T = {"p": Up, "p2": Hp, "q": Hq}
    for r in range(1, 4):
        for Sset in itertools.combinations(("p", "p2", "q"), r):
            A = {0}
            for s in Sset: A = {(a + t) % M for a in A for t in T[s]}
            U = [z for z in o if ("p" in Sset and z in ("p", "pq")) or ("p2" in Sset and z in ("p2", "p2q")) or ("q" in Sset and z in ("q", "pq", "p2q"))]
            k = (p if "p" in Sset else 1) * (p if "p2" in Sset else 1) * (q if "q" in Sset else 1)
            assert zeros(A) == set(U), (Sset, zeros(A), U); S_cert(tuple(U), A, k)
    # the bounds of Case 2
    S_cert(("p2", "pq", "p2q"), Hpq, p * q); S_cert(("p2", "pq", "p2q"), Hp2, p * p)
    S_cert(("p", "pq", "p2q"), UpZq, p * q); S_cert(("p", "pq", "p2q"), Hp2, p * p)
    S_cert(("pq", "p2q"), Hq, q); S_cert(("pq", "p2q"), Hp2, p * p)
    S_cert(("p2q",), Hq, q); S_cert(("p2q",), Hp, p)
    # the two clique bounds of Case 1 (non-closed patterns): D+ <= max(p, q) < pq
    t = mn                                                           # number of layers used
    C_cert(("p", "q"), [crt(c + i * p, i, p, q) for i in range(t) for c in range(p)], mx)          # layer i holds c + i p: same layer => difference a unit
    C_cert(("p2", "q", "pq"), [crt(c + i * p, c, p, q) for c in range(t) for i in range(p)], mx)   # layer c holds the class c mod p
    return res
pairs = [(p, q) for p in (2, 3, 5, 7) for q in (2, 3, 5, 7, 11, 13, 29, 53) if p != q]
for p, q in pairs:
    res = check(p, q)
    tight = sum(1 for Z, kind, b, d in res if d == b)
    print(f"p={p} q={q} M={p*p*q}: {len(res)} certificates verified; bound equals D+ in {tight}", flush=True)
