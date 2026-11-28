# Second look: recounts for the three disputed sentences and for the new (d).  Exact counts by grid.py / tree.py.
import sys, math, random
from fractions import Fraction as F
from math import comb
from decimal import Decimal as D, getcontext
import grid, tree
def q(r): return F(comb(r, r // 2), 1 << r)
print("(b) family: h copies of 0 with 1, 3, 9, 11, 12 on Z_15; share of signings bad ONLY at composite d (here d = 15)")
for h in list(range(0, 17)) + [21, 22, 51, 52, 101, 102]:
    items = {0: h, 1: 1, 3: 1, 9: 1, 11: 1, 12: 1} if h else {1: 1, 3: 1, 9: 1, 11: 1, 12: 1}
    m, tot, pp, X, b1, live, same, comp = grid.counts(15, items)
    sh = F(comp, 1 << m); want = q(h) / 16 if h % 2 == 1 else F(0)
    assert sh == want, (h, sh, want)
    if h <= 8 or h in (21, 22, 101): print(f"   h = {h}, m = {m}: {sh}" + (f" = (1/16) q({h}); sqrt(m) x share = {float(sh) * math.sqrt(m):.4f}" if h % 2 else " (none)"))
print("   equal to (1/16) q(h) for every odd h and to 0 for every even h in 0..16, 21, 22, 51, 52, 101, 102")
m, tot, pp, X, b1, live, same, comp = grid.counts(15, {0: 5, 1: 1, 2: 1, 3: 1, 7: 1, 9: 1, 11: 1})
print(f"   the other multiset, five copies of 0 with 1, 2, 3, 7, 9, 11 (m = {m}): bad only at 15: {F(comp, 1 << m)}")
m, tot, pp, X, b1, live, same, comp = grid.counts(15, {0: 6, 1: 1, 3: 1, 9: 1, 11: 1, 12: 1})
print(f"   the family at h = 6 (m = {m}): bad only at 15: {F(comp, 1 << m)}")
it = {0: 2}
for b in (45, 63, 90, 105, 126, 135, 180, 189, 210, 225, 252, 270): it[b] = 1
m, tot, pp, X, b1, live, same, comp = grid.counts(315, it)
print(f"   Z_315, m = {m} (two copies of 0 and the nonzero multiples of 105, 63, 45): bad only at composite d: {F(comp, 1 << m)} ; sqrt(m) x = {comp / 2**m * math.sqrt(m):.4f}")
m, tot, pp, X, b1, live, same, comp = grid.counts(15, {0: 1, 1: 1, 3: 1, 9: 1, 11: 1, 12: 1})
print(f"   Z_15, m = 6: {F(comp, 1 << m)}")
# (a) all slices zero at x != 1 need not be bad at 1: {0, 5, 10} on Z_15 with equal signs
m, tot, pp, X, b1, live, same, comp = grid.counts(15, {0: 1, 5: 1, 10: 1})
print(f"(a) {{0, 5, 10}} on Z_15: bad share {F(tot, 8)}, bad at 1: {F(b1, 8)} (the two bad signings have equal signs, sum +-3, mask zero at the cube roots of unity)")
# (d): the numbers
getcontext().prec = 30
kap = (D(2) / D("3.14159265358979323846264338327950288")).sqrt()
def isprime(x): return x > 1 and all(x % t for t in range(2, int(x ** 0.5) + 1))
def a_p(p):
    tau = D(p).sqrt() * D(2) ** (1 - p); return tau / (1 - D("0.8165") * D(p).sqrt() * D(2) ** (2 - p))
def c(r): return D(comb(r, r // 2)) / D(2 ** r) if r % 2 == 0 else D(0)
exc = []; mxodd = D(0); mxev8 = D(0); dec = True; prev = None
for p in range(5, 400):
    if not isprime(p): continue
    a = a_p(p)
    if prev is not None and a >= prev: dec = False
    prev = a
    mxodd = max(mxodd, a / D(p).sqrt())
    for r in range(p + 1, 3000, 2):
        v = c(r) + a / D(r).sqrt()
        if v >= D("0.375"): exc.append((p, r, float(v)))
        if r >= 8: mxev8 = max(mxev8, v)
print(f"(d) primes 5 <= p < 400: a_p decreasing: {dec}; max a_p/sqrt(p) = {mxodd:.5f} (< 0.09); max over even r >= max(p+1, 8), r < 3000, of c(r) + a_p/sqrt(r) = {mxev8:.5f} (< 0.338; 35/128 + a_5/sqrt(8) = {c(8) + a_p(5) / D(8).sqrt():.5f});")
print(f"    pairs (p, even r >= p) with c(r) + a_p/sqrt(r) >= 3/8: {exc}; c(r) values r = 1..8: {[str(F(comb(r, r // 2), 1 << r)) if r % 2 == 0 else '0' for r in range(1, 9)]}")
# e_5(6) = 0: every multiset of six elements on Z_25 (containing 0, by translation) and a sample on Z_125, Z_625
import itertools
n0 = 0; bad = 0
for rest in itertools.combinations_with_replacement(range(25), 5):
    items = {0: 1}
    for b in rest: items[b] = items.get(b, 0) + 1
    mm, f0, x = tree.analyse(5, 2, items); n0 += 1; bad += x != 0
rng = random.Random(5); n1 = 0
for v in (3, 4):
    for _ in range(20000):
        base = [rng.randrange(5 ** v) for _ in range(6)]
        if rng.random() < 0.7:   # make a full group likely: five elements c + t 5^i (+ multiples of 5^(i+1))
            i = rng.randrange(v); cc = rng.randrange(5 ** i)
            base = [(cc + t * 5 ** i + 5 ** (i + 1) * rng.randrange(5 ** (v - i - 1))) % 5 ** v for t in range(5)] + [rng.choice([cc, rng.randrange(5 ** v)])]
        items = {}
        for b in base: items[b] = items.get(b, 0) + 1
        mm, f0, x = tree.analyse(5, v, items); n1 += 1; bad += x != 0
print(f"    e_5(6) = 0: P(X_5) = 0 for all {n0} multisets of six elements containing 0 on Z_25 and for {n1} multisets of six on Z_125, Z_625 (most with a full group): exceptions {bad}")
print(f"(7) 9553/8192 x kappa = {D(9553) / D(8192) * kap:.8f}; 597/512 x kappa = {D(597) / D(512) * kap:.8f}; 78764625/67108864 x kappa = {D(78764625) / D(67108864) * kap:.8f}; 19221/16384 x kappa = {D(19221) / D(16384) * kap:.8f}; 7 kappa/6 = {7 * kap / 6:.8f}; 3 kappa/2 = {3 * kap / 2:.6f}; kappa/2 = {kap / 2:.6f}")
