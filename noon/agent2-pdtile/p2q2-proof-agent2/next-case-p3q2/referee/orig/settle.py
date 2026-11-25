"""Z_{p^3 q^2}: exact classification of all zero patterns (exact.py), then the open ones against the lemmas on mixed sets.
 M0: a mixed set has i p + j q elements with i, j >= 1; so |A| = p q is impossible
 M2: |A| = p^2 q and the zeros p, p^3 q, p^2 q^2 force A + K = A, hence every (3, m) and every (l, 2) is a zero
 M3: |A| = p^2 q, p < q: q is not a zero
 M4: |A| = p^2 q: q and p q^2 are not both zeros
usage: settle.py p,q [p,q ...]            (Noon = agent2, 21 November 2026)"""
import sys
from collections import Counter
from exact import classify
a, b = 3, 2
for pq in sys.argv[1:]:
    p, q = map(int, pq.split(',')); M = p**a * q**b
    cnt, hard = classify(p, a, q, b); why = Counter(); left = []
    for Z, size in hard:
        assert (a, b) in Z
        allK = all((3, m) in Z for m in range(3)) and all((l, 2) in Z for l in range(4))
        if size == p * q: why['M0'] += 1
        elif size == p * p * q and {(1, 0), (3, 1), (2, 2)} <= Z and not allK: why['M2'] += 1
        elif size == p * p * q and p < q and (0, 1) in Z: why['M3'] += 1
        elif size == p * p * q and {(0, 1), (1, 2)} <= Z: why['M4'] += 1
        else: left.append((sorted(Z), size))
    print(f"Z_{M} (p = {p}, q = {q}): " + ", ".join(f"{k} {cnt[k]}" for k in ('L2', 'a', 'b', 'N', 'R', 'T', 'U', 'H')) + f";  of the {cnt['H']} open: M0 {why['M0']}, M2 {why['M2']}, M3 {why['M3']}, M4 {why['M4']}, left {len(left)}", flush=True)
    for Z, size in left: print(f"      left: size {size}  zeros {Z}")
