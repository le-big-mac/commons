"""Z_{p^3 q^2}: exact classification of all zero patterns (exact.py), then the open ones against the lemmas on mixed sets.
 M0: a mixed set has i p + j q elements with i, j >= 1; so |A| = p q is impossible
 M2: |A| = p^2 q and the zeros p, p^3 q, p^2 q^2 force A + K = A (and then A tiles, by Lemma E.4)
 M4: |A| = p^2 q: q and p q^2 are not both zeros
Also counted: the patterns of categories T, U, H that satisfy (T2) (none means: every weak tile has (T1), (T2), no orphan).
usage: settle.py p,q [p,q ...]            (Noon = agent2, 21 November 2026)"""
import sys
from collections import Counter
from exact import classify, CAT
a, b = 3, 2
for pq in sys.argv[1:]:
    p, q = map(int, pq.split(',')); M = p**a * q**b
    cnt, hard = classify(p, a, q, b); why = Counter(); left = []
    for Z, size in hard:
        assert (a, b) in Z
        if size == p * q: why['M0'] += 1
        elif size == p * p * q and {(1, 0), (3, 1), (2, 2)} <= Z: why['M2'] += 1          # then A + K = A, and A tiles by Lemma E.4
        elif size == p * p * q and {(0, 1), (1, 2)} <= Z: why['M4'] += 1
        else: left.append((sorted(Z), size))
    # do the patterns of categories T, U, H all violate (T2)?  (then no weak tile has a pattern outside L2 and a)
    t2 = lambda Z: all((l, m) in Z for l in range(1, a + 1) for m in range(1, b + 1) if (l, 0) in Z and (0, m) in Z)
    tuh_t2 = sum(1 for Z, c in CAT.items() if c in ('T', 'U', 'H') and t2(Z))
    print(f"Z_{M} (p = {p}, q = {q}): " + ", ".join(f"{k} {cnt[k]}" for k in ('L2', 'a', 'b', 'N', 'R', 'T', 'U', 'H')) + f";  of the {cnt['H']} open: M0 {why['M0']}, M2 {why['M2']}, M4 {why['M4']}, left {len(left)};  T, U, H patterns with (T2): {tuh_t2}", flush=True)
    for Z, size in left: print(f"      left: size {size}  zeros {Z}")
