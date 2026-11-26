"""The formula as the note states it (README.md, "In short" and sections 2 and 3), written from the note's
words, and its comparison with Lean's own values (lean-values.txt, printed by AuditEval.lean).

E, F here are sets of levels in 1..n; `bal` says whether Phi_q | A (the note's "0 in F").
"""
import sys
from collections import Counter


def note_value(p, q, n, bal, E, F):
    """returns (kind, a0, kprime, x, value)"""
    e = len(E)
    if not bal:
        # "When Phi_q does not divide A the smallest multiset with pattern (E, F) has p^e elements if F is a
        #  subset of E and p^e(p^k + q) elements otherwise", k = number of levels a >= 1 in F and not in E
        k = len([a for a in F if a not in E])
        if all(a in E for a in F):
            return (0, 0, 0, 0, p ** e)
        return (0, 0, 0, 0, p ** e * (p ** k + q))
    levels = list(range(1, n + 1))
    if all(a in F for a in levels):
        # "If F is all of 0..n the minimum is q p^e"
        return (1, 0, 0, 0, q * p ** e)
    # "Let a0 be the first level in 1..n that is not in F, and k' the number of levels of F\E deeper than a0."
    a0 = min(a for a in levels if a not in F)
    deeper = sorted(a for a in F if a not in E and a > a0)
    kp = len(deeper)
    # "x = 0 if one of these holds and x = 1 if none does"
    c1 = (kp == 0)                                           # (1) k' = 0
    c2 = any(a in E for a in range(1, a0))                   # (2) some level shallower than a0 (one of 1..a0-1) is in E
    c3 = (a0 in E) and p >= 3                                # (3) a0 in E and p >= 3
    # (4) a0 in E, p = 2, and strictly between a0 and the first level of F\E deeper than a0 there is a level
    #     in E and not in F
    c4 = False
    if (a0 in E) and p == 2 and deeper:
        first = deeper[0]
        c4 = any((b in E) and (b not in F) for b in range(a0 + 1, first))
    x = 0 if (c1 or c2 or c3 or c4) else 1
    return (2, a0, kp, x, q * p ** e * (p ** kp + x))


def levels_of(mask, n):
    return frozenset(l for l in range(1, n + 1) if (mask >> (l - 1)) & 1)


def read_lean(path):
    """dict (p,q,n,bal,emask,fmask) -> (kind,a0,kprime,x,value,ok)"""
    d = {}
    for ln in open(path):
        t = ln.split()
        if len(t) != 12 or not all(s.isdigit() for s in t):
            raise SystemExit("unexpected line in Lean output: " + ln)
        p, q, n, bal, em, fm, kind, a0, kp, x, val, ok = map(int, t)
        key = (p, q, n, bal, em, fm)
        assert key not in d
        d[key] = (kind, a0, kp, x, val, ok)
    return d


if __name__ == '__main__':
    lean = read_lean(sys.argv[1] if len(sys.argv) > 1 else 'lean-values.txt')
    kinds = Counter()
    bad = []
    notok = 0
    clause_census = Counter()
    for (p, q, n, bal, em, fm), (kind, a0, kp, x, val, ok) in lean.items():
        E, F = levels_of(em, n), levels_of(fm, n)
        mine = note_value(p, q, n, bool(bal), E, F)
        kinds[kind] += 1
        if ok != 1:
            notok += 1
        if mine != (kind, a0, kp, x, val):
            bad.append(((p, q, n, bal, sorted(E), sorted(F)), mine, (kind, a0, kp, x, val)))
        if kind == 2:
            clause_census[(p == 2, x)] += 1
    triples = sorted(set(k[:3] for k in lean))
    print(f"rows read from Lean: {len(lean)}  (triples (p,q,n): {len(triples)}; n from "
          f"{min(t[2] for t in triples)} to {max(t[2] for t in triples)})")
    print(f"by theorem: unbalanced {kinds[0]}, balanced-all {kinds[1]}, balanced with a0 {kinds[2]}, none {kinds[3]}")
    print(f"rows where Lean decides the hypotheses of the theorem used are NOT all true "
          f"(or a0 is not the unique number that satisfies them): {notok}")
    print(f"rows where the note's formula (my reading of its words) and Lean's value differ in kind, a0, k', x or value: {len(bad)}")
    for b in bad[:40]:
        print("   ", b)
    print("kind-2 rows by (p == 2, x):", dict(sorted(clause_census.items())))
