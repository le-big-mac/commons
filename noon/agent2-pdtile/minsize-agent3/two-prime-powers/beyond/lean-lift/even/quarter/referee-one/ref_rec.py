"""Referee's own recomputation of the numbers in result.md sections 3, 4, 6 (written from the text's definitions).

usage: ref_rec.py M [M2]
  - xi(m) for m <= M by the recursion of section 3 (rules (a), (b), (c)), exact rationals
  - checks C1 .. C5
  - R_q(m) by a search of my own over size patterns; W_m(no 3) two ways; W'(m); b(m); b(m) <= 3/8
  - with M2: the hypothesis of Proposition 3 for xi* on M < m <= M2 (a look at Proposition T)
"""
import sys
from fractions import Fraction as Fr
from math import comb
from itertools import product

M = int(sys.argv[1])
M2 = int(sys.argv[2]) if len(sys.argv) > 2 else M
TOP = max(M, M2)

# numerators of pi(v; r) = P(sum of r signs = v):  N[r][v] = C(r, (r+v)/2), v from -r to r
N = []
for r in range(TOP + 1):
    N.append({v: comb(r, (r + v) // 2) for v in range(-r, r + 1, 2)})


def cc(r):                      # c_r = max_v pi(v; r)
    return Fr(max(N[r].values()), 2 ** r)


C = [cc(r) for r in range(TOP + 1)]
assert all(C[r] == Fr(comb(r, r // 2), 2 ** r) for r in range(TOP + 1))


def A_num(r0, r1, r2):          # 2^(r0+r1+r2) * sum over v != 0 of pi(v;r0) pi(v;r1) pi(v;r2)
    n0, n1, n2 = N[r0], N[r1], N[r2]
    t = 0
    for v, x in n2.items():
        if v != 0 and v in n1 and v in n0:
            t += x * n1[v] * n0[v]
    return t


xi = [Fr(0), Fr(0)]             # xi(0) = xi(1) = 0


def g(r, X):
    return (C[r] if r % 2 == 0 else Fr(0)) + X[r]


def bound_for(m, X):
    """max over triples r0 >= r1 >= r2 >= 0, r1 >= 1, sum m, of A + (least applicable rule), rules computed with X"""
    best = Fr(0); arg = None
    for r2 in range(0, m + 1):
        for r1 in range(max(1, r2), m + 1):
            r0 = m - r1 - r2
            if r0 < r1:
                break
            A = Fr(A_num(r0, r1, r2), 2 ** m)
            rules = [g(r0, X) * g(r1, X) * g(r2, X)]
            if r0 % 2 == 0 and r1 % 2 == 0 and r2 % 2 == 0:
                rules.append((C[r0] + X[r0]) * (C[r1] + X[r1]) * (C[r2] + X[r2]) - C[r0] * C[r1] * C[r2])
            if r2 == 0 and r0 % 2 == 1 and r1 % 2 == 1 and r0 <= 7:
                rules.append(X[r0] * X[r1] / 2)
            val = A + min(rules)
            if val > best:
                best = val; arg = (r0, r1, r2)
    return best, arg


args = {}
for m in range(2, M + 1):
    b, a = bound_for(m, xi)
    xi.append(b); args[m] = a

print("xi(m), m = 2 ..", min(M, 30))
for m in range(2, min(M, 30) + 1):
    print(f"  {m:3d}  {xi[m]}  at {args[m]}")

# ---- C1 .. C5
c1 = all(xi[m] == C[m - 2] / 2 for m in range(3, M + 1, 2))
print("C1 xi(m) = c_(m-2)/2 for all odd 3 <= m <= M:", c1)
ev = list(range(2, M + 1, 2))
mx = max(ev, key=lambda m: xi[m])
print("C2 largest xi over even m:", xi[mx], "at m =", mx, "; <= 309/8192:", all(xi[m] <= Fr(309, 8192) for m in ev),
      "; < 5/128:", all(xi[m] < Fr(5, 128) for m in ev))
print("   xi(2,4,6,8,10,12) =", [str(xi[m]) for m in (2, 4, 6, 8, 10, 12) if m <= M])
rt = max(ev, key=lambda m: xi[m] / C[m])
print("C3 xi(m) <= c_m/2 for all even m <= M:", all(xi[m] <= C[m] / 2 for m in ev), "; largest ratio", float(xi[rt] / C[rt]), "at", rt)
half_c = {m: Fr(comb(m, m // 2), 2 ** (m + 1)) for m in range(2, 1001, 2)}
first = min(m for m in half_c if half_c[m] <= Fr(5, 128))
print("C4 least even m with c_m/2 <= 5/128:", first, "; holds for all even m in [that, 1000]:",
      all(half_c[m] <= Fr(5, 128) for m in half_c if m >= first), "(c_m decreases over even m: ratio (m+1)/(m+2))")
if M >= 60:
    worst = None
    for r1 in range(2, 61, 2):
        for r2 in range(0, r1 + 1, 2):
            if r1 + r2 > 60:
                continue
            psi = C[r1 + r2] - 2 * C[r1] * C[r2] + Fr(3, 2) * g(r1, xi) * g(r2, xi)
            if worst is None or psi > worst[0]:
                worst = (psi, r1, r2)
    print("C5 largest Psi:", worst[0], "at", worst[1:], "; <= 1/4:", worst[0] <= Fr(1, 4))
    tail = Fr(comb(62, 31), 2 ** 62) + Fr(3, 2) * Fr(5, 128) * (Fr(1, 2) + 1 + Fr(5, 128))
    print("   tail of Psi (r1 + r2 >= 62):", float(tail), "< 0.1912:", tail < Fr(1912, 10000))

# (P1), (P2) as used in Proposition T
print("P1 xi(r) <= c_(r-1)/2 <= 1/4 odd r >= 3:", all(xi[r] <= C[r - 1] / 2 <= Fr(1, 4) for r in range(3, M + 1, 2)))
print("P2 xi(r) <= min(5/128, c_r/2) even r >= 2:", all(xi[r] <= min(Fr(5, 128), C[r] / 2) for r in ev),
      "; g(r) < 1:", all(g(r, xi) < 1 for r in ev))

# ---- t-bar
tbar = [None] * (M + 1)
for m in range(3, M + 1):
    tbar[m] = (C[m] if m % 2 == 0 else 0) + xi[m]
print("tbar(m) <= 3/8 for 3 <= m <= M:", all(tbar[m] <= Fr(3, 8) for m in range(3, M + 1)))
if M >= 27:
    w = Fr(118569, 10 ** 6)
    mm = max(range(27, M + 1), key=lambda m: tbar[m])
    print("tbar(m) + 0.118569 <= 3/8 for 27 <= m <= M:", all(tbar[m] + w <= Fr(3, 8) for m in range(27, M + 1)),
          "; largest", float(tbar[mm] + w), "at m =", mm)
    print("odd 27 <= m <= M: tbar + 0.118569 <= 1/4:", all(tbar[m] + w <= Fr(1, 4) for m in range(27, M + 1, 2)),
          "; even 28 <= m <= M: <= 47/128:", all(tbar[m] + w <= Fr(47, 128) for m in range(28, M + 1, 2)))
    print("tail m > 240: 1.5*c_242 =", float(Fr(3, 2) * Fr(comb(242, 121), 2 ** 242)), " c_239/2 =", float(Fr(comb(239, 119), 2 ** 240)))


# ---- R_q(m): my own search.  p3[k][w] = P(sum of k signs = w mod 3)
def p3(k, w):
    return Fr(sum(x for v, x in N[k].items() if (v - w) % 3 == 0), 2 ** k)


def parts(s, kmax, cap):        # partitions of s into at most kmax positive parts, each <= cap
    if s == 0:
        yield []
        return
    if kmax == 0:
        return
    for k in range(min(s, cap), 0, -1):
        for rest in parts(s - k, kmax - 1, k):
            yield [k] + rest


def gshare(sizes, q):           # q subclasses, sizes padded with zeros; the q sums are congruent modulo 3
    full = sizes + [0] * (q - len(sizes))
    tot = Fr(0)
    for w in range(3):
        p = Fr(1)
        for k in full:
            p *= p3(k, w)
        tot += p
    return tot


def Rq(q, mmax):
    any_g = [Fr(1)] + [Fr(0)] * mmax; full_g = [Fr(0)] * (mmax + 1); fullarg = [None] * (mmax + 1)
    for s in range(1, mmax + 1):
        for pt in parts(s, q, s):
            v = gshare(pt, q)
            if v > any_g[s]:
                any_g[s] = v
            if len(pt) == q and v > full_g[s]:
                full_g[s] = v; fullarg[s] = tuple(pt)
    # best product over any collection of groups with n elements in all
    best_any = [Fr(1)] + [Fr(0)] * mmax
    for n in range(1, mmax + 1):
        best_any[n] = max(any_g[s] * best_any[n - s] for s in range(1, n + 1))
    out = {}
    for m in range(q, mmax + 1):
        cand = [(full_g[s] * best_any[m - s], fullarg[s], m - s) for s in range(q, m + 1)]
        out[m] = max(cand, key=lambda t: t[0])
    return out


def primes(lo, hi):
    return [p for p in range(lo, hi + 1) if all(p % d for d in range(2, p)) and p > 1]


RMAX = min(M, 20)
Rtab = {q: Rq(q, RMAX) for q in primes(5, RMAX)}
print("R_q(m) (value, full group, elements outside it):")
for m in range(5, min(RMAX, 14) + 1):
    print("  m =", m, "; ".join(f"q={q}: {Rtab[q][m][0]} {Rtab[q][m][1]}+{Rtab[q][m][2]}" for q in Rtab if q <= m))
print("R_q(m) <= 2^(1-q) in every case computed:", all(Rtab[q][m][0] <= Fr(1, 2 ** (q - 1)) for q in Rtab for m in Rtab[q]))
print("R_q(m) equals the pattern (m-q+1, 1, ..., 1) for all q <= m <=", RMAX, ":",
      all(Rtab[q][m][0] == gshare([m - q + 1] + [1] * (q - 1), q) for q in Rtab for m in Rtab[q]))


# ---- W_m(no 3): (1) by listing the e*, (2) by the product formula for the number of e* with mu <= t
def W_list(m):
    ps = primes(5, m)
    tot = Fr(0); cnt = 0
    for vs in product(*[range(0, (m - 1) // (q - 1) + 1) for q in ps]):
        mu = max([v * (q - 1) for v, q in zip(vs, ps)] + [0])
        if mu > 0:
            assert mu <= m - 1
            tot += Fr(1, 2 ** mu); cnt += 1
    return tot, cnt


def Acount(t):
    a = 1
    for p in primes(5, t + 1):
        a *= 1 + t // (p - 1)
    return a


def W_formula(m):
    return sum(Fr(Acount(t) - Acount(t - 1), 2 ** t) for t in range(1, m))


print("m, tbar, W_m(no 3), W'(m), b(m), b <= 3/8, crude <= 3/8")
okall = True
for m in range(3, min(M, 26) + 1):
    w1, cnt = W_list(m); w2 = W_formula(m)
    assert w1 == w2, (m, w1, w2)
    wp = w1
    if m <= 14:
        for q in primes(5, m):
            wp -= Fr(1, 2 ** (q - 1)) - Rtab[q][m][0]
    b = tbar[m] + wp
    okall &= b <= Fr(3, 8)
    print(f"  {m:2d}  {str(tbar[m]):>16s}  {str(w1):>16s} ({cnt} e*)  {str(wp):>12s}  {str(b):>18s} = {float(b):.6f}  {b <= Fr(3, 8)}  {tbar[m] + w1 <= Fr(3, 8)}")
print("b(m) <= 3/8 for 3 <= m <= 26:", okall)
print("W_m(no 3) < 0.118569 for m <= 60:", all(W_formula(m) < Fr(118569, 10 ** 6) for m in range(3, 61)), float(W_formula(60)))

# ---- a look at Proposition T
if M2 > M:
    X = xi[:]
    ok = True; worst_even = Fr(0); worst_odd = Fr(0)
    for m in range(M + 1, M2 + 1):
        target = C[m - 2] / 2 if m % 2 else C[m] / 2
        X.append(target)
    for m in range(M + 1, M2 + 1):
        b, a = bound_for(m, X)
        ok &= b <= X[m]
        if m % 2:
            worst_odd = max(worst_odd, b / X[m])
        else:
            worst_even = max(worst_even, b / X[m])
    print(f"Proposition T, a look: for {M} < m <= {M2}, max(A + S) <= xi*(m): {ok}; largest ratio even {float(worst_even):.4f}, odd {float(worst_odd):.6f}")
