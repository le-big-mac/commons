# attained.py seed budget_seconds -- multisets of an even number m of elements, 14 <= m <= 24, on which the bound of
# Lemma L (first part) is attained at a chosen level d = p^i d'':  f groups at level i of the p-tree that are full with one
# element in each subclass (all p elements of a group with the same residue modulo n''), and q groups that hold two equal
# elements; m = p f + 2 q, e = (p-1) f + q, and the number of signings bad at d must be exactly 2^(m - e).
# For each: that count; the fraction of good signings (all 2^m signings, exact division) against 0.039; the
# contraction with (1), (2), (3) and Corollary L.
import sys, math, random, time
from fractions import Fraction
import numpy as np
from rlib import factor, divisors, mu, nprime, vp, contract_all, all_levels_full, lemmaL_e, crt
from rfast import bad_fast

seed = int(sys.argv[1]); budget = float(sys.argv[2])
rng = random.Random(seed)
t0 = time.time()
GROUPS = [9, 27, 45, 81, 135, 25, 75, 225, 63, 189, 125, 375]
viol = {"count": 0, "F": 0, "C1": 0, "C2": 0, "C3": 0, "D": 0}
rows = {}
total = 0
while time.time() - t0 < budget:
    n = rng.choice(GROUPS)
    p = rng.choice([q for q in factor(n) if q in (3, 5)])
    a = vp(n, p)
    pa = p ** a
    n2 = n // pa
    i = rng.randint(1, a)
    ngroups = p ** (i - 1)
    opts = [(f, q) for f in range(1, ngroups + 1) for q in range(0, ngroups - f + 1) if 14 <= p * f + 2 * q <= 24 and (p * f + 2 * q) % 2 == 0]
    if not opts:
        continue
    f, q = rng.choice(opts)
    m = p * f + 2 * q
    d2 = rng.choice(divisors(n2))
    d = p ** i * d2
    cls = rng.sample(range(ngroups), f + q)
    B = []
    for c in cls[:f]:
        w = rng.randrange(n2)
        for e in range(p):
            u = c + e * p ** (i - 1) + p ** i * rng.randrange(pa // p ** i)
            B.append(crt(u, pa, w, n2))
    for c in cls[f:]:
        u = c + rng.randrange(p) * p ** (i - 1) + p ** i * rng.randrange(pa // p ** i)
        x = crt(u, pa, rng.randrange(n2), n2)
        B += [x, x]
    assert len(B) == m
    full = 1 << m
    e = lemmaL_e(B, p, i)
    assert e == (p - 1) * f + q
    anybad = np.zeros(full, dtype=bool)
    nb = {}
    for dd in divisors(n):
        v = bad_fast(B, dd)
        nb[dd] = int(v.sum())
        anybad |= v
    total += 1
    if nb[d] << e != full:
        viol["count"] += 1
        print("COUNT DIFFERS", n, B, d, nb[d], e)
    frac = Fraction(full - int(anybad.sum()), full)
    if not frac > Fraction(39, 1000):
        viol["F"] += 1
        print("VIOLATION F", n, B, frac)
    Bf, nf, steps = contract_all(B, n, "deep")
    if not all_levels_full(Bf, nf):
        viol["C2"] += 1
    if nprime(m) % nf:
        viol["C3"] += 1
    if steps:
        anyf = np.zeros(full, dtype=bool)
        nbf = {}
        for dd in divisors(nf):
            v = bad_fast(Bf, dd)
            nbf[dd] = int(v.sum())
            anyf |= v
        if (~anyf & anybad).any():
            viol["C1"] += 1
            print("VIOLATION C1", n, B, Bf, nf)
    else:
        nbf = nb
    for dd, k in nbf.items():
        if dd > 1 and k << mu(dd) > full:
            viol["D"] += 1
            print("VIOLATION D", n, B, Bf, nf, dd, k)
    r = rows.setdefault((n, p), {"cnt": 0, "minfrac": Fraction(2), "nf_eq_n": 0, "levels": set()})
    r["cnt"] += 1
    r["minfrac"] = min(r["minfrac"], frac)
    r["nf_eq_n"] += nf == n
    r["levels"].add(d)
print("seed %d: %d multisets of 14..24 elements (even) built so that Lemma L is attained at one level" % (seed, total))
for (n, p), r in sorted(rows.items()):
    print("  Z_%-4d p = %d: %4d multisets (%d with n_flat = n), levels d used %s; least good fraction %.4f" % (n, p, r["cnt"], r["nf_eq_n"], sorted(r["levels"]), float(r["minfrac"])))
print("violations:", viol, "  seconds %.0f" % (time.time() - t0))
