"""Full enumeration of subsets of Z_M containing 0, M = p^2 q, with exact zero sets.

For every subset: zero set (exact integer residues mod Phi_d), size.
Checks, per subset:
  F1/F2   Facts 1, 2 (count criteria) against exact divisibility           [given, but cheap to re-check]
  L3a     Lemma 3(a) structural form and the existential form
  L3b     Lemma 3(b) all sentences
  L3c     Lemma 3(c)
  X, Y    the size inequalities used in Case 2
  P1      D+(Z_A) <= |A|, k | |A|            (exact D+ by vertex enumeration over Q)
  THM     every A with D+(Z_A) = |A| has Z_A inside U(P), (T1), (T2)
Output: per-pattern table of the sizes that occur.
Usage: enum_p2q.py p q
"""
import sys
import time
from fractions import Fraction
import numpy as np
import core

p, q = int(sys.argv[1]), int(sys.argv[2])
M = p * p * q
ORD = [p, p * p, q, p * q, p * p * q]          # bit i of pattern <-> ORD[i]
NAME = {p: "p", p * p: "p2", q: "q", p * q: "pq", p * p * q: "p2q"}
t0 = time.time()
nsub = 1 << (M - 1)
idx = np.arange(nsub, dtype=np.int64)
bits = np.zeros((nsub, M), dtype=np.int8)
bits[:, 0] = 1
for b in range(1, M):
    bits[:, b] = (idx >> (b - 1)) & 1
size = bits.sum(axis=1).astype(np.int64)
bits32 = bits.astype(np.int32)

zero = {}
for d in ORD:
    R = core.res(M, d).astype(np.int32)
    zero[d] = ~((bits32 @ R).any(axis=1))
pattern = np.zeros(nsub, dtype=np.int64)
for i, d in enumerate(ORD):
    pattern |= zero[d].astype(np.int64) << i
print(f"M={M} p={p} q={q}: {nsub} subsets containing 0; zero sets computed in {time.time()-t0:.1f}s")

# ---- count arrays -------------------------------------------------------------------------------
# N21[s, u, w] = [x in A], x = u mod p^2, x = w mod q
N21 = np.zeros((nsub, p * p, q), dtype=np.int8)
for x in range(M):
    N21[:, x % (p * p), x % q] = bits[:, x]
N20 = N21.sum(axis=2).astype(np.int16)                 # (nsub, p^2)
N01 = N21.sum(axis=1).astype(np.int16)                 # (nsub, q)
# u = c + i p  ->  [i, c]
box = N21.reshape(nsub, p, p, q).transpose(0, 2, 1, 3).astype(np.int16)   # (nsub, c, i, j)
N11 = box.sum(axis=2)                                   # (nsub, c, j)
N10 = N11.sum(axis=2)                                   # (nsub, c)


def additive(T):
    """T shape (..., I, J): T[i,j] - T[i,0] - T[0,j] + T[0,0] == 0 for all i,j."""
    d = T - T[..., :, :1] - T[..., :1, :] + T[..., :1, :1]
    return ~d.any(axis=(-1, -2))


fail = 0


def check(name, cond, n=None):
    global fail
    ok = bool(np.all(cond))
    cnt = int(np.size(cond)) if n is None else n
    print(f"  [{'ok' if ok else 'FAIL'}] {name}  (cases: {cnt})")
    if not ok:
        fail += 1


# ---- Facts 1 and 2 ------------------------------------------------------------------------------
f1_p = (N10 == N10[:, :1]).all(axis=1)
f1_q = (N01 == N01[:, :1]).all(axis=1)
N20b = N20.reshape(nsub, p, p).transpose(0, 2, 1)       # (nsub, c, i)
f1_p2 = (N20b == N20b[:, :, :1]).all(axis=(1, 2))
f2_pq = additive(N11)
f2_p2q = additive(box).all(axis=1)
print("Facts 1, 2 (count criterion == exact divisibility), every subset:")
check("Fact 1 at p", f1_p == zero[p])
check("Fact 1 at q", f1_q == zero[q])
check("Fact 1 at p^2", f1_p2 == zero[p * p])
check("Fact 2 at pq", f2_pq == zero[p * q])
check("Fact 2 at p^2 q", f2_p2q == zero[p * p * q])

# ---- Lemma 3(a) ---------------------------------------------------------------------------------
print("Lemma 3(a):")
sel = zero[p * q]
T = N11[sel]
a = T.min(axis=(1, 2))
al = T.min(axis=2) - a[:, None]
be = T.min(axis=1) - a[:, None]
check("normal form a+alpha+beta reproduces N11 (Fact 5), all A with Phi_pq | A",
      (T == a[:, None, None] + al[:, :, None] + be[:, None, :]).all(axis=(1, 2)))
x = al.sum(axis=1)
y = be.sum(axis=1)
check("|A| = pq a + q x + p y", size[sel] == p * q * a + q * x + p * y)
check("Phi_p | A  <=>  alpha == 0", (x == 0) == zero[p][sel])
check("Phi_q | A  <=>  beta == 0", (y == 0) == zero[q][sel])
selA = sel & ~zero[p] & ~zero[q]
repA = {p * q * aa + q * xx + p * yy for aa in range(p + 1) for xx in range(1, M) for yy in range(1, M)
        if p * q * aa + q * xx + p * yy <= M}
check("hyp of 3(a) => |A| in {pq a + q x + p y : x,y >= 1}", np.isin(size[selA], sorted(repA)), int(selA.sum()))

# ---- Lemma 3(b) ---------------------------------------------------------------------------------
print("Lemma 3(b):")
sel = zero[p * p * q]
Bx = box[sel]                                           # (n, c, i, j)
ac = Bx.min(axis=(2, 3))
alc = Bx.min(axis=3) - ac[:, :, None]                   # (n, c, i)
bec = Bx.min(axis=2) - ac[:, :, None]                   # (n, c, j)
check("normal form on every box", (Bx == ac[:, :, None, None] + alc[:, :, :, None] + bec[:, :, None, :]).all(axis=(1, 2, 3)))
Ac = alc.sum(axis=2)
Bc = bec.sum(axis=2)
check("N10(c) = pq a_c + q A_c + p B_c", (N10[sel] == p * q * ac + q * Ac + p * Bc).all(axis=1))
xb = (p * ac + Ac).sum(axis=1)
yb = Bc.sum(axis=1)
check("|A| = q x + p y", size[sel] == q * xb + p * yb)
check("Phi_p2 | A  <=>  every alpha^c == 0", (Ac.sum(axis=1) == 0) == zero[p * p][sel])
check("every beta^c == 0  =>  Phi_q | A", zero[q][sel][yb == 0], int((yb == 0).sum()))
check("Phi_p2 not| A  =>  x >= 1", xb[~zero[p * p][sel]] >= 1, int((~zero[p * p][sel]).sum()))
check("Phi_q not| A  =>  y >= 1", yb[~zero[q][sel]] >= 1, int((~zero[q][sel]).sum()))
n_conv_fail = int((zero[q][sel] & (yb > 0)).sum())
print(f"  (info) Phi_q | A but some beta^c != 0 (converse of the Phi_q sentence is not claimed): {n_conv_fail} sets")

# ---- Lemma 3(c) ---------------------------------------------------------------------------------
print("Lemma 3(c):")
selc = (size == p * q) & zero[p] & zero[p * p * q]
check("|A| = pq, Phi_p, Phi_p2q | A  =>  Phi_pq | A", zero[p * q][selc], int(selc.sum()))

# ---- Case 2 size inequalities -------------------------------------------------------------------
print("Case 2 size claims (pure set statements, no D+):")
sX = zero[p * q] & ~zero[p] & ~zero[q]
check("(X): n >= p+q", size[sX] >= p + q, int(sX.sum()))
sX2 = sX & zero[p * p]
check("(X), p^2 in Z: n > pq   (n >= pq+p)", size[sX2] >= p * q + p, int(sX2.sum()))
sY = zero[p * p * q] & ~zero[p * p] & ~zero[q]
check("(Y) hyp (p2q in Z, p2,q not): n >= p+q", size[sY] >= p + q, int(sY.sum()))
sY2 = sY & zero[p]
check("(Y), p in Z: n > p*min(p,q)", size[sY2] > p * min(p, q), int(sY2.sum()))
if sY2.any():
    print(f"  (info) min size in (Y) with p in Z: {int(size[sY2].min())}; p(p+q) = {p*(p+q)}")
if sX2.any():
    print(f"  (info) min size in (X) with p^2 in Z: {int(size[sX2].min())}; pq+p = {p*q+p}")

# ---- pattern table, D+, theorem ------------------------------------------------------------------
print("Pattern table: zero set | k | D+ (exact) | #sets | sizes occurring | #sets with |A| = D+")


def U_of(P):
    U = set()
    if p in P:
        U |= {p, p * q}
    if p * p in P:
        U |= {p * p, p * p * q}
    if q in P:
        U |= {q, p * q, p * p * q}
    return U


tot_pd = 0
viol = 0
hist = np.bincount(pattern * 64 + size, minlength=32 * 64).reshape(32, 64)
pd_mask = np.zeros(nsub, dtype=bool)
for pat in range(32):
    Z = [ORD[i] for i in range(5) if pat >> i & 1]
    cnt = int(hist[pat].sum())
    if cnt == 0:
        continue
    dp = core.dplus_exact(M, Z)
    dpf = core.dplus_float(M, Z)
    assert abs(float(dp) - dpf) < 1e-7, (Z, dp, dpf)
    P = set(Z) & {p, p * p, q}
    k = p ** len(P & {p, p * p}) * q ** len(P & {q})
    sizes = [s for s in range(64) if hist[pat][s]]
    inU = set(Z) <= U_of(P)
    t2 = (not (p in Z and q in Z) or p * q in Z) and (not (p * p in Z and q in Z) or p * p * q in Z)
    npd = int(hist[pat][int(dp)]) if dp.denominator == 1 else 0
    tot_pd += npd
    if npd:
        pd_mask |= (pattern == pat) & (size == int(dp))
    bad = []
    if min(sizes) < dp:
        bad.append("SIZE<D+")
    if any(s % k for s in sizes):
        bad.append("k not| n")
    if npd and not (inU and t2 and k == dp):
        bad.append("PD-TILING SET VIOLATING (T1)/(T2)/U(P)")
    viol += len(bad)
    print(f"  {{{','.join(NAME[d] for d in Z)}}} | k={k} | D+={dp} | {cnt} | {sizes} | pd={npd} | inU={inU} T2closed={t2} {' '.join(bad)}")
print(f"pd-tiling sets containing 0 (|A| = D+(Z_A)): {tot_pd}; violations: {viol}")
np.save(f"pdmask_{M}.npy", np.nonzero(pd_mask)[0])
print(f"FAILED CHECKS: {fail}   time {time.time()-t0:.1f}s")
