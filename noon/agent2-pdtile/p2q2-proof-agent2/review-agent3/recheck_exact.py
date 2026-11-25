"""Independent exact re-check of Noon's certificates for 'weak tiles of Z_{p^2 q^2} are tiles' (agent3 / Yonder).
Written from the statement in p2q2-agent2.md (sections 1, 3, 5) WITHOUT using check_p2q2.py or spotcheck_p2q2.py.
For a list of prime pairs p < q, in exact rational arithmetic, for every one of the 192 patterns with p or q a zero:
  - the pattern list in the file is complete and without repetition, for each regime;
  - cat a: the pattern satisfies (T2) and has no orphan;
  - every other category: the dual y uses only rows of LP(Z) (the normalisation row and the orders NOT in Z), and all nine reduced costs are >= 0;
  - cat b: y0 > M/k;   cat H: y0 = M/k = pq, Ep = {1}, |Eq| = 1, (2,2) in F, (1,2) not in F;
  - cat RP/RQ/N: gamma* >= 0, gamma*_{22} = 1, Lambda_{lm}(gamma*) = 0 for every order not in Z, sigma(gamma*) = y0;
    RP: gamma*_{0j} = 0;  RQ: gamma*_{i0} = 0;  N: Ep = Eq = {1} and y0 = (p^2(q-1) + q^2(p-1))/(pq-1), and M/y0 is not an integer.
Also (independent of the certificates) the optimum of LP(Z) is computed with HiGHS and compared with y0 (must be >= y0; equal for R, N, H)."""
import json, sys, itertools
from fractions import Fraction as Fr
import sympy as sp
P, Q = sp.symbols("p q")
CERT = json.load(open("/srv/commons/agent2-pdtile/p2q2-proof-agent2/certificates_p2q2.json"))
CLS = [(i, j) for i in range(3) for j in range(3)]; ORD = [(l, m) for l in range(3) for m in range(3)]
def cc(n, l, i): return [[n * n - n, n - 1, 1], [-n, n - 1, 1], [0, -1, 1]][l][i]
_cache = {}
def val(expr, p, q):
    if expr not in _cache: _cache[expr] = sp.lambdify((P, Q), sp.sympify(expr, locals={"p": P, "q": Q}), modules=[{"ImmutableDenseMatrix": None}, "sympy"])
    v = sp.Rational(_cache[expr](sp.Integer(p), sp.Integer(q))); return Fr(int(v.p), int(v.q))
def all_patterns():
    out = []
    for Ep in ((), (1,), (2,), (1, 2)):
        for Eq in ((), (1,), (2,), (1, 2)):
            if 1 not in Ep and 1 not in Eq: continue
            for r in range(5):
                for F in itertools.combinations([(1, 1), (1, 2), (2, 1), (2, 2)], r): out.append((Ep, Eq, F))
    return out
def check_pair(p, q, lp=False):
    assert p < q and q != p * p; regime = "A" if q < p * p else "B"; M = p * p * q * q; bad = []; n = 0
    ents = [e for e in CERT if e["regime"] == regime]; keys = [(tuple(e["Ep"]), tuple(e["Eq"]), tuple(sorted(map(tuple, e["F"])))) for e in ents]
    if sorted(keys) != sorted((a, b, tuple(sorted(c))) for a, b, c in all_patterns()): bad.append("pattern list is not exactly the 192 patterns")
    coef = {(o, c): Fr(cc(p, o[0], c[0]) * cc(q, o[1], c[1])) for o in ORD for c in CLS}
    for e, (Ep, Eq, F) in zip(ents, keys):
        n += 1; Z = {(l, 0) for l in Ep} | {(0, m) for m in Eq} | set(F); k = p ** len(Ep) * q ** len(Eq); rows = [o for o in ORD if o != (0, 0) and o not in Z]; cat = e["cat"]; tag = (Ep, Eq, F, cat)
        t2 = all((l, m) in F for l in Ep for m in Eq); orphan = any(l not in Ep and m not in Eq for (l, m) in F)
        if cat == "a":
            if not t2 or orphan: bad.append((tag, "cat a but not (T2 and no orphan)"))
            continue
        y = {k_: val(v, p, q) for k_, v in e["y"].items()}; y0 = y.pop("norm"); yr = {tuple(map(int, k_.split(","))): v for k_, v in y.items()}
        if any(o not in rows and v != 0 for o, v in yr.items()): bad.append((tag, "dual uses a row that is not in LP(Z)"))
        for c in CLS:
            r = coef[((0, 0), c)] - (y0 if c == (2, 2) else 0) - sum(v * coef[(o, c)] for o, v in yr.items())
            if r < 0: bad.append((tag, f"reduced cost of class {c} is {r}"))
        if cat == "b":
            if not y0 > Fr(M, k): bad.append((tag, f"y0 = {y0} is not > M/k = {Fr(M, k)}"))
        if cat == "H":
            if not (y0 == Fr(M, k) and k == p * q and Ep == (1,) and len(Eq) == 1 and (2, 2) in F and (1, 2) not in F): bad.append((tag, "H conditions"))
        if cat in ("RP", "RQ", "N"):
            g = {c: Fr(0) for c in CLS}
            for k_, v in e["gamma"].items(): g[tuple(map(int, k_.split(",")))] = val(v, p, q)
            if any(v < 0 for v in g.values()): bad.append((tag, "gamma* has a negative entry"))
            if g[(2, 2)] != 1: bad.append((tag, "gamma*_22 != 1"))
            for o in rows:
                if sum(g[c] * coef[(o, c)] for c in CLS) != 0: bad.append((tag, f"Lambda{o}(gamma*) != 0"))
            if sum(g[c] * coef[((0, 0), c)] for c in CLS) != y0: bad.append((tag, "sigma(gamma*) != y0"))
            if cat == "RP" and any(g[(0, j)] != 0 for j in range(3)): bad.append((tag, "gamma* not supported in pZ"))
            if cat == "RQ" and any(g[(i, 0)] != 0 for i in range(3)): bad.append((tag, "gamma* not supported in qZ"))
            if cat == "N":
                f = Fr(p * p * (q - 1) + q * q * (p - 1), p * q - 1)
                if not (Ep == (1,) and Eq == (1,) and y0 == f and (Fr(M) / y0).denominator != 1): bad.append((tag, "N conditions"))
        if cat not in ("a", "b", "RP", "RQ", "H", "N"): bad.append((tag, "unknown category"))
        if lp:
            import numpy as np
            from scipy.optimize import linprog
            A_eq = [[float(coef[(o, c)]) for c in CLS] for o in rows] + [[1.0 if c == (2, 2) else 0.0 for c in CLS]]; b_eq = [0.0] * len(rows) + [1.0]
            res = linprog([float(coef[((0, 0), c)]) for c in CLS], A_eq=A_eq, b_eq=b_eq, bounds=[(0, None)] * 9, method="highs")
            if res.status != 0: bad.append((tag, f"LP status {res.status}"))
            else:
                rel = (res.fun - float(y0)) / float(y0)
                if rel < -1e-9: bad.append((tag, f"LP optimum {res.fun} below y0 {float(y0)}"))
                if cat in ("RP", "RQ", "N", "H") and abs(rel) > 1e-9: bad.append((tag, f"LP optimum {res.fun} != y0 {float(y0)}"))
    return regime, n, bad
if __name__ == "__main__":
    pairs = [tuple(map(int, a.split(","))) for a in sys.argv[1:]]
    tot = 0; nb = 0
    for p, q in pairs:
        regime, n, bad = check_pair(p, q, lp=(q < 2000)); tot += n; nb += len(bad)
        if bad: print(f"({p},{q}) regime {regime}: {len(bad)} FAILURES, first: {bad[:3]}")
    print(f"{len(pairs)} prime pairs, {tot} (pattern, pair) checks, {nb} failures")
