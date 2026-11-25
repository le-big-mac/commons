# Supplementary checks:
# (a) Lemma digit for every M <= 210 and every S subset of P_M (exact, via cyclotomic division)
# (b) the fact used in the proof of CM(1): p^a is a zero of A  <=>  every class mod p^(a-1) has p times as many
#     elements of A as each of its subclasses mod p^a   (all subsets of Z_M, M in 8, 9, 12, 16)
# (c) the single-factor claim of Lemma digit's proof: sum_{c<p} e_xi(g_s)^c = 0  <=>  p^a || ord(xi)
import cmath
from itertools import product, combinations
from math import gcd
from sympy import divisors, factorint
from brute import cyc, polyrem_is_zero, prime_powers, exact, gen, digit_multiset, order

bad = 0; tot = 0
for M in range(1, 211):
    divs = divisors(M); PP = prime_powers(M); phis = {d: cyc(d) for d in divs}
    for r in range(len(PP) + 1):
        for S in combinations(PP, r):
            ms = digit_multiset(M, list(S)); T = set(ms)
            pr = 1
            for (s, p, a) in S: pr *= p
            co = [0] * M
            for t in T: co[t] = 1
            z = set(d for d in divs if polyrem_is_zero(co, phis[d]))
            want = set(d for d in divs if any(exact(s, d) for (s, p, a) in S))
            tot += 1
            if len(ms) != len(T) or len(T) != pr or z != want:
                bad += 1; print("digit failure", M, S)
print(f"(a) Lemma digit, M<=210, all S: {tot} cases, failures {bad}")

bad = 0; tot = 0
for M in range(1, 211):
    for (s, p, a) in prime_powers(M):
        g = gen(M, p, a)
        for xi in range(M):
            val = sum(cmath.exp(2j * cmath.pi * xi * g * c / M) for c in range(p))
            tot += 1
            if (abs(val) < 1e-9) != exact(s, order(xi, M)):
                bad += 1
print(f"(c) single factor vanishes iff p^a || ord(xi), M<=210: {tot} cases, failures {bad}")

for M in [8, 9, 12, 16]:
    divs = divisors(M); PP = prime_powers(M); phis = {d: cyc(d) for d in divs}
    bad = 0
    for m in range(1 << M):
        A = [x for x in range(M) if (m >> x) & 1]
        co = [0] * M
        for x in A: co[x] = 1
        for (s, p, a) in PP:
            isz = polyrem_is_zero(co, phis[s])
            lo = s // p
            cl = [0] * lo; ch = [0] * s
            for x in A:
                cl[x % lo] += 1; ch[x % s] += 1
            equi = all(cl[v % lo] == p * ch[v] for v in range(s))
            if isz != equi: bad += 1
    print(f"(b) M={M}: p^a zero <=> equidistribution, failures {bad}")
