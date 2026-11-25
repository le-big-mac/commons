"""Exact zero sets instead of minimal patterns, and an arithmetic test.  (Noon, 21 Nov 2026; exploration, floating point LP.)
For M = p^a q^b: every set Z of orders (the would-be exact zero set of A) that violates (T2) somewhere, every size k that Z
allows (step function f >= 0, f(0)=1, transform zero off Z, sum f = M/k) and that is a multiple of kS(Z).  Tests:
  crude : for some d not in Z:  prod_{e in Z, e/d a prime power or its inverse} |Res(Phi_d, Phi_e)|  >  k^phi(d)
          (A(zeta_d) is a nonzero algebraic integer divisible by every Phi_e(zeta_d), and each conjugate is at most k in size)
  energy: sum over d not in Z, d > 1, of phi(d) * (that product)^(2/phi(d))  >  k (M - k)      (Parseval and AM-GM)
A pair (Z, k) that passes both is 'left'.   usage: norm.py p a q b [--list]"""
import sys, itertools, math, numpy as np
from scipy.optimize import linprog
p, a, q, b = (int(x) for x in sys.argv[1:5]); M = p**a * q**b; X = np.arange(M)
vp = lambda x, r, cap: next(e for e in range(cap, -1, -1) if x % r**e == 0)
cls = [(vp(int(x), p, a), vp(int(x), q, b)) for x in X]
G = [(i, j) for i in range(a + 1) for j in range(b + 1)]; gi = {g: n for n, g in enumerate(G)}
size = np.array([sum(1 for c in cls if c == g) for g in G], float)
ORD = [(l, m) for l in range(a + 1) for m in range(b + 1) if (l, m) != (0, 0)]
val = lambda o: p**o[0] * q**o[1]
phi = lambda o: (p**o[0] - p**(o[0] - 1) if o[0] else 1) * (q**o[1] - q**(o[1] - 1) if o[1] else 1)
Tm = {}
for o in ORD:
    xi = M // val(o); row = np.zeros(len(G)); c = np.cos(2 * np.pi * (X * xi % M) / M)
    for x in X: row[gi[cls[x]]] += c[x]
    Tm[o] = np.round(row)
def sumf_range(Z):
    rows = [np.eye(len(G))[gi[(a, b)]]] + [Tm[o] for o in ORD if o not in Z]; rhs = [1.0] + [0.0] * (len(rows) - 1); out = []
    for sgn in (1, -1):
        r = linprog(sgn * size, A_eq=np.vstack(rows), b_eq=rhs, bounds=[(0, None)] * len(G), method="highs")
        if r.status == 2: return None
        if r.status == 3: out.append(np.inf); continue
        out.append(sgn * r.fun)
    return out
def kS(Z):
    k = 1
    for (l, m) in Z:
        if m == 0: k *= p
        if l == 0: k *= q
    return k
def lognorm(d, Z):
    """log of the product of |Res(Phi_d, Phi_e)| over e in Z comparable with d through one prime"""
    s = 0.0
    for e in Z:
        if e[1] == d[1] and e[0] != d[0]: s += phi(min(d, e, key=val)) * math.log(p)     # e/d a power of p
        if e[0] == d[0] and e[1] != d[1]: s += phi(min(d, e, key=val)) * math.log(q)
    return s
viol = lambda Z: [(i, j) for i in range(1, a + 1) for j in range(1, b + 1) if (i, 0) in Z and (0, j) in Z and (i, j) not in Z]
name = lambda Z: "{" + ",".join(str(val(o)) for o in sorted(Z, key=val)) + "}"
n_pat = n_pairs = n_crude = n_energy = 0; left = []
for r in range(len(ORD) + 1):
    for Zt in itertools.combinations(ORD, r):
        Z = frozenset(Zt)
        if not viol(Z): continue
        rg = sumf_range(Z)
        if rg is None: continue
        n_pat += 1; ks = kS(Z)
        for k in range(ks, M, ks):
            if not (rg[0] - 1e-7 <= M / k <= rg[1] + 1e-7): continue
            n_pairs += 1
            non = [d for d in ORD if d not in Z]
            crude = any(lognorm(d, Z) > phi(d) * math.log(k) + 1e-9 for d in non)
            energy = sum(phi(d) * math.exp(2 * lognorm(d, Z) / phi(d)) for d in non) > k * (M - k) + 1e-6
            n_crude += crude; n_energy += (energy and not crude)
            if not crude and not energy: left.append((k, Z))
print(f"Z_{M}: zero sets violating (T2) and allowing some size: {n_pat};  (zero set, size) pairs with kS | size: {n_pairs};  "
      f"killed by the crude norm test: {n_crude};  by the energy test only: {n_energy};  left: {len(left)}")
if "--list" in sys.argv:
    for k, Z in sorted(left, key=lambda t: (t[0], len(t[1]))): print(f"   left: size {k}  zeros {name(Z)}  (T2) fails at {[val(o) for o in viol(Z)]}")
