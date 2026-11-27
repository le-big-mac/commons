# strong_cyclic.py -- a multiset (and, with r large enough, a set) on a cyclic group Z_n, n odd, for which
# "all signs +" and every signing with exactly one sign turned are divisible by some Phi_d.
# Exact integer arithmetic only.
#
# Construction.  p_1..p_9 = 3,5,7,11,13,17,19,23,29 (sum of 1/p_i > 1), PI = their product, G = prod Z_{p_i},
# q_i = p_i - 1, Q = prod q_i.  A point x of G has a "zero set" Z(x) = {i : x_i = 0}.  The multiplicity w(x)
# depends only on Z(x):
#     Z = {i}, i = 2..8 :  m q_i PI/p_i
#     Z = {1}           :  m q_1 (PI/p_1 - e)
#     Z = {9}           :  m q_9 (PI/p_9 - e)
#     Z = {1,9}         :  m q_1 q_9 e            where e = sum_i PI/p_i - PI  (> 0)
#     Z = {1..9} (x=0)  :  2
#     otherwise         :  0
# Then (checked below from the formulas, and the formulas are checked by enumeration on small boxes):
#   for every i the number of elements with x_i = 0 is  u_i + 2  and with x_i = v (v != 0) is u_i = m Q PI / p_i.
# N = 2 + m Q PI.  r = an odd prime factor of N (r does not divide PI because N = 2 mod p_i).  n = PI * r.
# The N elements are listed with equal points of G consecutive and the t-th gets the coordinate t mod r in Z_r.
import sys, itertools
from math import prod, gcd
from sympy import factorint, isprime

def patterns_weights(ps, m, wrap):
    """weights g(Z) for the arc construction; ps = list of moduli (pairwise coprime not needed for the counts);
    wrap = (a, b): indices of the two coordinates whose arcs overlap (first and last)"""
    PI = prod(ps); k = len(ps)
    e = sum(PI // p for p in ps) - PI
    assert e >= 0
    a, b = wrap
    assert e <= PI // ps[a] and e <= PI // ps[b]
    g = {}
    for i in range(k):
        if i in (a, b):
            g[frozenset([i])] = m * (ps[i] - 1) * (PI // ps[i] - e)
        else:
            g[frozenset([i])] = m * (ps[i] - 1) * (PI // ps[i])
    g[frozenset([a, b])] = m * (ps[a] - 1) * (ps[b] - 1) * e
    return g

def marginal_formula(ps, g, i):
    """(number of elements with x_i = 0, number with x_i = v for one v != 0), from the pattern weights,
    the origin NOT included"""
    k = len(ps)
    zero = 0; nonzero = 0
    for Z, w in g.items():
        if i in Z:
            zero += w * prod(ps[j] - 1 for j in range(k) if j not in Z)
        else:
            nonzero += w * prod(ps[j] - 1 for j in range(k) if j not in Z and j != i)
    return zero, nonzero

def cube_formula(ps, s, P):
    """cube sum at level P (corners 0 / 1 in the coordinates of P, the rest summed out) of the function
    sum_Z s(Z) 1[zero set = Z]   (s may include the origin pattern)"""
    k = len(ps); tot = 0
    for Z, w in s.items():
        tot += w * (-1) ** len(P - Z) * prod(ps[j] - 1 for j in range(k) if j not in P and j not in Z)
    return tot

def brute_check(ps, g):
    """enumerate the box, build the weight function, compare marginals and cube sums with the formulas"""
    k = len(ps)
    W = {}
    for x in itertools.product(*[range(p) for p in ps]):
        Z = frozenset(i for i in range(k) if x[i] == 0)
        if Z in g: W[x] = g[Z]
    for i in range(k):
        cnt = [0] * ps[i]
        for x, w in W.items(): cnt[x[i]] += w
        z, nz = marginal_formula(ps, g, i)
        assert cnt[0] == z and all(c == nz for c in cnt[1:]), (i, cnt, z, nz)
    for mask in range(1 << k):
        P = frozenset(i for i in range(k) if mask >> i & 1)
        c = 0
        for x, w in W.items():
            if all(x[i] in (0, 1) for i in P):
                c += w * (-1) ** sum(1 for i in P if x[i] == 1)
        assert c == cube_formula(ps, g, P), (P, c)
    return True

# ---- 1. the formulas against enumeration on small boxes (moduli need not be prime for the counts)
for ps, wrap in [([2, 3, 6], (0, 2)), ([2, 3, 5], (0, 2)), ([3, 3, 3], (0, 2)), ([2, 4, 5, 7], (0, 3)), ([3, 3, 5, 7], (0, 3))]:
    PI = prod(ps)
    e = sum(PI // p for p in ps) - PI
    if e < 0 or e > PI // ps[wrap[0]] or e > PI // ps[wrap[1]]:
        print("box", ps, ": arcs do not fit this pattern (e = %d), skipped" % e); continue
    g = patterns_weights(ps, 1, wrap)
    brute_check(ps, g)
    for i in range(len(ps)):
        z, nz = marginal_formula(ps, g, i)
        assert z == nz, (ps, i, z, nz)
    print("box", ps, ": formulas agree with enumeration; all marginals uniform; weights", sorted((sorted(Z), w) for Z, w in g.items()))

# ---- 2. the cyclic example
ps = [3, 5, 7, 11, 13, 17, 19, 23, 29]
k = len(ps); PI = prod(ps); Q = prod(p - 1 for p in ps)
print("\nprimes", ps, " PI =", PI, " Q =", Q)
print("sum 1/p > 1 :", sum(PI // p for p in ps), ">", PI, sum(PI // p for p in ps) > PI)
print("without 29, sum 1/p < 1 :", sum((PI // 29) // p for p in ps[:-1]) < PI // 29)
found = None
for m in range(1, 60):
    g = patterns_weights(ps, m, (0, 8))
    assert all(w > 0 for w in g.values())
    for i in range(k):
        z, nz = marginal_formula(ps, g, i)
        assert z == nz == m * Q * PI // ps[i]
    N = 2 + m * Q * PI
    assert N == 2 + sum(w * prod(ps[j] - 1 for j in range(k) if j not in Z) for Z, w in g.items())
    assert all(N % p == 2 for p in ps)
    maxw = max(g.values())
    f = factorint(N)
    rs = [r for r in f if r > 2]
    big = [r for r in rs if r >= maxw]
    if m <= 3 or big:
        print("m = %d: N = %d = %s ; largest multiplicity %d ; odd prime factors %s ; those >= largest multiplicity: %s"
              % (m, N, f, maxw, rs, big))
    if big and found is None:
        found = (m, g, N, min(big))
        break
m, g, N, r = found
assert isprime(r) and N % r == 0 and gcd(r, PI) == 1 and r >= max(g.values()) and r >= 2
n = PI * r
print("\nCHOSEN: m = %d, N = |B| = %d, r = %d, n = PI*r = %d (odd: %s), N <= n: %s" % (m, N, r, n, n % 2 == 1, N <= n))
print("weights:")
for Z, w in sorted(g.items(), key=lambda t: (len(t[0]), sorted(t[0]))):
    print("   zero set", [ps[i] for i in sorted(Z)], " multiplicity", w, " points", prod(ps[j] - 1 for j in range(k) if j not in Z))
print("for each p_i: #(x = 0 mod p_i) = u_i + 2, #(x = v mod p_i) = u_i, u_i = m Q PI / p_i  -- asserted above")

# ---- 3. a good signing of this B (the weak form for it), by descent modulo r:
# if the fold S_G of S to Z_PI has, for every P, a cube sum at level P not divisible by r, then S(zeta) != 0
# for every n-th root of unity (Lemmas A and B(b) of sign-lemma-result.md).  S_G does not depend on how the
# coordinates in Z_r were given out.  Signings tried: all + except the two copies of the origin (both turned),
# i.e. s(origin) = -2; and a few others.
def cube_all(s, extra=()):
    """cube sums c_P for all P of  sum_Z s(Z) 1[zero set Z]  +  sum of c * delta_x over (x, c) in extra"""
    out = {}
    for mask in range(1 << k):
        P = frozenset(i for i in range(k) if mask >> i & 1)
        c = cube_formula(ps, s, P)
        for x, coef in extra:
            if all(x[i] in (0, 1) for i in P):
                c += coef * (-1) ** sum(1 for i in P if x[i] == 1)
        out[P] = c
    return out
origin = frozenset(range(k))
def report(name, s, extra=()):
    c = cube_all(s, extra)
    z_int = [sorted(ps[i] for i in P) for P, v in c.items() if v == 0]
    z_mod = [sorted(ps[i] for i in P) for P, v in c.items() if v % r == 0]
    print("%s: levels with cube sum 0: %d ; with cube sum = 0 mod r: %d %s" % (name, len(z_int), len(z_mod), z_mod[:6]))
    return len(z_mod) == 0
s0 = dict(g); s0[origin] = 2
report("all +                        ", s0)
s1 = dict(g); s1[origin] = 0
report("one copy of the origin turned", s1)
s2 = dict(g); s2[origin] = -2
ok = report("both copies of origin turned ", s2)
# one copy of the origin and one copy of a point with zero set {p_i}: x = (1,..,1,0,1,..,1) or with 2's
for i in range(k):
    x = tuple(0 if j == i else 1 for j in range(k))
    report("origin copy + point e_%d(ones) " % ps[i], s1, extra=[(x, -2)])
print("\nweak form for this B, two signs turned (both copies of the origin): %s" % ("GOOD (all 512 cube sums nonzero mod r)" if ok else "not shown by this test"))

# ---- 4. the same construction as a MULTISET on a smaller group: m = 1, r = 103
g1 = patterns_weights(ps, 1, (0, 8)); N1 = 2 + Q * PI; r1 = 103
assert N1 % r1 == 0 and isprime(r1) and gcd(r1, PI) == 1
for i in range(k):
    z, nz = marginal_formula(ps, g1, i); assert z == nz == Q * PI // ps[i]
print("\nMULTISET version: m = 1, N = %d elements, r = 103, n = PI*103 = %d; largest multiplicity of a point of Z_PI: %d (so it is a multiset on Z_n)" % (N1, PI * r1, max(g1.values())))
r = r1
t0 = dict(g1); t0[origin] = 2; report("multiset, all +                   ", t0)
t2 = dict(g1); t2[origin] = -2; ok1 = report("multiset, both origin copies turned", t2)
print("weak form for the multiset, two signs turned: %s" % ("GOOD (all 512 cube sums nonzero mod 103)" if ok1 else "not shown by this test"))
