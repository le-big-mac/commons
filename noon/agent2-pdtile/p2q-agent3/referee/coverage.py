"""Which leaf of the proof in Section 3 of p2q-agent3.md handles each of the 32 patterns Z, and does the
containment / bound used in that leaf actually hold?  Exact D+ for prime pairs in every regime
(p<q<p^2, q>p^2, q<p, p=2, q=2)."""
from itertools import combinations
import core

names = ["p", "p2", "q", "pq", "p2q"]
subsets = [frozenset(c) for r in range(6) for c in combinations(names, r)]


def U(P):
    out = set()
    if "p" in P:
        out |= {"p", "pq"}
    if "p2" in P:
        out |= {"p2", "p2q"}
    if "q" in P:
        out |= {"q", "pq", "p2q"}
    return out


def closed(Z):
    return (not ({"p", "q"} <= Z) or "pq" in Z) and (not ({"p2", "q"} <= Z) or "p2q" in Z)


def leaf(Z):
    """returns (case, T2-leaf or Case-2 leaf, superset used for the D+ bound or None)"""
    P = Z & {"p", "p2", "q"}
    if Z <= U(P):
        if "q" not in P or P == {"q"}:
            assert closed(Z)
            return ("Case1", "T2 nothing to check", None)
        if P == {"p", "p2", "q"}:
            return ("Case1", "A = Z_M (so Z = O)", None)
        if P == {"p", "q"}:
            if "p2q" in Z:
                return ("Case1", "Lemma 3(c) => pq in Z", None)
            if "pq" not in Z:
                assert Z == {"p", "q"}
                return ("Case1", "Lemma 2(e): Z = {p,q}", frozenset({"p", "q"}))
            assert closed(Z)
            return ("Case1", "T2 holds (pq in Z)", None)
        if P == {"p2", "q"}:
            if "p2q" not in Z:
                assert Z <= {"p2", "q", "pq"}
                return ("Case1", "Lemma 2(f): Z in {p2,q,pq}", frozenset({"p2", "q", "pq"}))
            assert closed(Z)
            return ("Case1", "T2 holds (p2q in Z)", None)
        raise AssertionError("uncovered Case 1 pattern")
    # Case 2
    assert ("pq" in Z and "p" not in Z and "q" not in Z) or ("p2q" in Z and "p2" not in Z and "q" not in Z)
    assert "q" not in Z
    if "pq" in Z and "p" not in Z and "q" not in Z:
        if "p2" not in Z:
            assert Z <= {"pq", "p2q"}
            return ("Case2", "X, p2 not in Z: Lemma 2(c)", frozenset({"pq", "p2q"}))
        assert Z <= {"p2", "pq", "p2q"}
        return ("Case2", "X, p2 in Z: Lemma 2(a)", frozenset({"p2", "pq", "p2q"}))
    assert "p2q" in Z and "p2" not in Z and "q" not in Z and ("pq" not in Z or "p" in Z)
    if "p" not in Z:
        assert Z == {"p2q"}
        return ("Case2", "Y, p not in Z: Lemma 2(d)", frozenset({"p2q"}))
    assert Z <= {"p", "pq", "p2q"}
    return ("Case2", "Y, p in Z: Lemma 2(b)", frozenset({"p", "pq", "p2q"}))


tab = {}
for Z in subsets:
    tab.setdefault(leaf(Z)[:2], []).append(Z)
print("leaf -> patterns")
for k in sorted(tab):
    print(f"  {k[0]} / {k[1]}: {len(tab[k])}: " + " ".join("{" + ",".join(n for n in names if n in Z) + "}" for Z in tab[k]))
print("total patterns covered:", sum(len(v) for v in tab.values()))
# every non-closed Case-1 pattern must land in a leaf that excludes it or forces closure
for Z in subsets:
    c, l, sup = leaf(Z)
    if c == "Case1" and not closed(Z):
        assert l.startswith("Lemma") or l.startswith("A = Z_M"), (Z, l)

pairs = [(2, 3), (3, 2), (2, 5), (5, 2), (3, 5), (5, 3), (2, 7), (7, 2), (3, 7), (7, 3), (2, 11), (5, 7), (7, 5), (3, 11), (11, 3), (2, 13)]
bad = 0
for p, q in pairs:
    M = p * p * q
    val = {"p": p, "p2": p * p, "q": q, "pq": p * q, "p2q": p * p * q}
    cache = {}

    def D(Z):
        if Z not in cache:
            cache[Z] = core.dplus_exact(M, [val[n] for n in Z])
        return cache[Z]

    def k(Z):
        return p ** len(Z & {"p", "p2"}) * q ** len(Z & {"q"})

    for Z in subsets:
        c, l, sup = leaf(Z)
        P = Z & {"p", "p2", "q"}
        if c == "Case1":
            ok = D(Z) <= D(frozenset(U(P))) <= k(Z)                   # the (T1) chain
            if l.startswith("Lemma 2"):
                ok = ok and D(Z) <= D(sup) <= max(p, q) < p * q == k(Z)
        else:
            ok = D(Z) <= D(sup)
            if "2(c)" in l:
                ok = ok and D(sup) <= q < p + q
            if "2(a)" in l:
                ok = ok and D(sup) <= p * min(p, q) <= p * q < p * q + p and k(Z) == p
            if "2(d)" in l:
                ok = ok and D(sup) <= min(p, q) < p + q
            if "2(b)" in l:
                ok = ok and D(sup) <= p * min(p, q) and (min(p, q) < q if p < q else min(p, q) < p)
        if not ok:
            bad += 1
            print("  VIOLATION", (p, q), sorted(Z), l)
print(f"numeric check of every leaf's D+ bound for {len(pairs)} prime pairs x 32 patterns: violations = {bad}")
