"""Referee: brute-force coverage of all ordered pairs of distinct primes below a bound by the pieces of Theorem D.
Pieces taken from the PARAM table of verify3.py (the checker), half-open at the top."""
import sys
from fractions import Fraction as Fr
from sympy import primerange
N = int(sys.argv[1]) if len(sys.argv) > 1 else 200
direct = {(2, 3), (2, 5), (2, 7), (3, 2), (3, 5), (3, 11)}
pieces = {
 'A1a': lambda p, q: p >= 5 and p + 2 <= q and Fr(q) < 2 * p - Fr(5, 2),
 'A1b': lambda p, q: p >= 5 and 2 * p - 1 <= q < p * p - p + 1,
 'A2':  lambda p, q: p >= 3 and p * p - p + 1 <= q < p * p - 1,
 'B1':  lambda p, q: p >= 5 and p * p + 1 <= q < p * p + p,
 'B2':  lambda p, q: p >= 3 and p * p + p + 1 <= q < p**3 - p * p + p - 1,
 'B3':  lambda p, q: p >= 3 and p**3 - p * p + p <= q < p**3 - 1,
 'C3':  lambda p, q: p >= 3 and q >= p**3 + 1,
 'Ap1': lambda p, q: q >= 3 and q + 1 <= p < q * q - q + 1,
 'Ap2': lambda p, q: q >= 3 and q * q - q + 1 <= p < q * q - 1,
 'Cp':  lambda p, q: q >= 2 and p >= q * q + 1,
 'fam2q': lambda p, q: p == 2 and q >= 11,
}
ps = list(primerange(2, N)); un = []; multi = 0; cnt = {}
for p in ps:
    for q in ps:
        if p == q: continue
        where = [n for n, f in pieces.items() if f(p, q)]
        if (p, q) in direct: where.append('direct')
        if not where: un.append((p, q))
        if len(where) > 1: multi += 1; print("in more than one:", (p, q), where)
        for w in where: cnt[w] = cnt.get(w, 0) + 1
print(f"pairs of distinct primes below {N}: {len(ps) * (len(ps) - 1)}; uncovered: {len(un)} {un[:20]}; in more than one piece: {multi}")
print(sorted(cnt.items()))
