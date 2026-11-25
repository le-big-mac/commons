"""Referee: choose the prime pairs for the independent recomputation and write one job line per chunk.
(1) every ordered pair of distinct primes below N1 (so every small prime, every piece that has small pairs);
(2) for each band and many values of the fixed prime: the first and last prime of the band (both ends), and primes next to each
    curve F = 0 on which a certificate tree branches (both sides);  (3) C3, Cp: first primes above the lower bound, and far out;
(4) the family p = 2: q = 11 .. and far out;  the six direct pairs."""
import sys, pickle, collections
from fractions import Fraction as Fr
import sympy as sp
from sympy import primerange, nextprime, prevprime, isprime
N1 = int(sys.argv[1]) if len(sys.argv) > 1 else 60
D_ = '/home/agent2/p3q2/referee2/orig/'
direct = {(2, 3), (2, 5), (2, 7), (3, 2), (3, 5), (3, 11)}
pieces = {
 'A1a': lambda p, q: p >= 5 and p + 2 <= q and 2 * q < 4 * p - 5, 'A1b': lambda p, q: p >= 5 and 2 * p - 1 <= q < p * p - p + 1,
 'A2': lambda p, q: p >= 3 and p * p - p + 1 <= q < p * p - 1, 'B1': lambda p, q: p >= 5 and p * p + 1 <= q < p * p + p,
 'B2': lambda p, q: p >= 3 and p * p + p + 1 <= q < p**3 - p * p + p - 1, 'B3': lambda p, q: p >= 3 and p**3 - p * p + p <= q < p**3 - 1,
 'C3': lambda p, q: p >= 3 and q >= p**3 + 1, 'Ap1': lambda p, q: q >= 3 and q + 1 <= p < q * q - q + 1,
 'Ap2': lambda p, q: q >= 3 and q * q - q + 1 <= p < q * q - 1, 'Cp': lambda p, q: q >= 2 and p >= q * q + 1, 'fam2q': lambda p, q: p == 2 and q >= 11}
def where(p, q):
    w = [n for n, f in pieces.items() if f(p, q)] + (['direct'] if (p, q) in direct else [])
    assert len(w) == 1, (p, q, w); return w[0]
jobs = collections.defaultdict(list)
def add(p, q, tag):
    if p != q and isprime(p) and isprime(q) and (p, q) not in jobs[where(p, q)]: jobs[where(p, q)].append((p, q))
ps = list(primerange(2, N1))
for p in ps:
    for q in ps:
        if p != q: add(p, q, 'small')
P, Q = sp.symbols('p q')
BANDS = {'B1': (P, P**2 + 1, P**2 + P, 5), 'B2': (P, P**2 + P + 1, P**3 - P**2 + P - 1, 3), 'B3': (P, P**3 - P**2 + P, P**3 - 1, 3),
         'Ap1': (Q, Q + 1, Q**2 - Q + 1, 3), 'Ap2': (Q, Q**2 - Q + 1, Q**2 - 1, 3), 'A1a': (P, P + 2, 2 * P - sp.Rational(5, 2), 5),
         'A1b': (P, 2 * P - 1, P**2 - P + 1, 5), 'A2': (P, P**2 - P + 1, P**2 - 1, 3)}
def factors(rec, acc):
    if rec['cat'] == 'split': acc.add(rec['factor']); factors(rec['pos'], acc); factors(rec['neg'], acc)
FIXED = [3, 5, 7, 11, 13, 17, 23, 31, 43, 61, 101, 499]
for band, (fixed, lo, up, p0) in BANDS.items():
    res = pickle.load(open(D_ + 'split_' + band + '.pkl', 'rb')); fs = set()
    for r in res.values(): factors(r, fs)
    other = Q if fixed == P else P
    big = band in ('B2', 'B3')
    for f in FIXED:
        if f < p0 or (big and f > 43 and f != 101): continue
        L = int(sp.ceiling(lo.subs(fixed, f))); U = sp.Rational(up.subs(fixed, f))          # L <= other < U
        mk = lambda o: (f, o) if fixed == P else (o, f)
        cand = []
        x = int(nextprime(L - 1)); cand += [x, int(nextprime(x))]                             # the first two primes of the band
        topint = int(sp.ceiling(U)) - 1                                                      # largest integer < U
        y = int(prevprime(topint + 1)); cand += [y, int(prevprime(y))] if y > 2 else [y]     # the last two primes of the band
        cand.append(int(nextprime((L + topint) // 2)))
        for F in fs:                                                                         # primes next to the curves F = 0
            Fe = sp.sympify(F, locals={'p': P, 'q': Q}).subs(fixed, f)
            for rt in sp.Poly(Fe, other).real_roots():
                rv = float(rt)
                if L - 1 <= rv <= float(U) + 1:
                    c = int(sp.floor(rt)); lo_p = int(prevprime(c + 1)) if c >= 2 else 2; cand += [lo_p, int(prevprime(lo_p)) if lo_p > 2 else 2, int(nextprime(c)), int(nextprime(nextprime(c)))]
        for o in cand:
            if o >= 2 and L <= o and o < U and o != f: add(*mk(o), band)
for p in [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 53, 101]:
    add(p, int(nextprime(p**3)), 'C3'); add(p, int(nextprime(nextprime(p**3))), 'C3'); add(p, int(nextprime(10 * p**3)), 'C3')
add(3, 10007, 'C3'); add(3, 1000003, 'C3'); add(5, 1000003, 'C3'); add(101, 10**9 + 7, 'C3')
for q in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 53, 101]:
    add(int(nextprime(q * q)), q, 'Cp'); add(int(nextprime(nextprime(q * q))), q, 'Cp'); add(int(nextprime(10 * q * q)), q, 'Cp')
add(10007, 2, 'Cp'); add(1000003, 2, 'Cp'); add(1000003, 3, 'Cp'); add(10**9 + 7, 101, 'Cp')
for q in [11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 1009, 10007, 1000003, 10**9 + 7]: add(2, q, 'fam')
tot = 0
with open('jobs.txt', 'w') as fh:
    for piece in sorted(jobs):
        L = jobs[piece]; tot += len(L)
        for i in range(0, len(L), 10): fh.write(piece + ' --basis ' + ' '.join(f"{p},{q}" for p, q in L[i:i + 10]) + '\n')
print({k: len(v) for k, v in sorted(jobs.items())}, 'total', tot)
