# Exact check of the example {5,8,9,25,28,31,41} in Z_42
from sympy import symbols, Poly, cyclotomic_poly, divisors, rem, ZZ, factorint
from itertools import product
X = symbols('X')
M = 42
A = [5, 8, 9, 25, 28, 31, 41]
P = Poly(sum(X**a for a in A), X, domain=ZZ)
zeros = []
for d in divisors(M):
    r = rem(P, Poly(cyclotomic_poly(d, X), X, domain=ZZ))
    if r.is_zero:
        zeros.append(d)
print("zeros (all d | 42, including d=1):", zeros)
print("residues mod 7:", sorted(a % 7 for a in A))
print("residues mod 6:", sorted(a % 6 for a in A))
print("residues mod 2:", sorted(a % 2 for a in A), " mod 3:", sorted(a % 3 for a in A))
# tiling with B = 7 Z_42
B = [7 * k for k in range(6)]
sums = sorted((a + b) % M for a in A for b in B)
print("A + 7Z_42 = Z_42 exactly:", sums == list(range(M)))
# prime powers, S_A, T1, T2, digit set complement
def prime_powers(M):
    out = []
    for p, e in factorint(M).items():
        for a in range(1, e + 1):
            out.append((p ** a, p, a))
    return out
PP = prime_powers(M)
def exact(s, d):
    from math import gcd
    return d % s == 0 and gcd(s, d // s) == 1
SA = [s for (s, p, a) in PP if s in zeros]
print("P_M =", [s for s, _, _ in PP], " S_A =", SA)
prod = 1
for (s, p, a) in PP:
    if s in SA: prod *= p
print("T1:", len(A) == prod)
T2 = all((d in zeros) for d in divisors(M) if d > 1 and all((s in SA) for (s, p, a) in PP if exact(s, d)))
print("T2:", T2)
print("zeros d>1 not exactly divisible by any s in S_A:", [d for d in zeros if d > 1 and not any(exact(s, d) for s in SA)])
# digit set complement T_{P_M \ S_A}
def gen(M, s, p, a):
    Mp = M
    while Mp % p == 0: Mp //= p
    return p ** (a - 1) * Mp
S = [(s, p, a) for (s, p, a) in PP if s not in SA]
T = set()
for c in product(*[range(p) for (s, p, a) in S]):
    T.add(sum(ci * gen(M, s, p, a) for ci, (s, p, a) in zip(c, S)) % M)
print("T_{P\\S_A} =", sorted(T))
print("A + T = Z_42:", sorted((a + b) % M for a in A for b in T) == list(range(M)))
# primes of d=6 dividing |A|=7 ?
print("|A| =", len(A))
