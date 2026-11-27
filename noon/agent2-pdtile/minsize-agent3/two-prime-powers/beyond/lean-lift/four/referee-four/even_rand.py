# even_rand.py seed budget_seconds mlist nlist -- the even case where the proof is thinnest: multisets of m elements, m even,
# 14 <= m <= 24, with all three classes modulo 3 occupied, on groups divisible by 3.  All 2^m signings, exact division
# (rfast.py).  For each multiset B:
#  - the fraction of good signings against the stated 0.039;
#  - contraction (deepest first): (1), (2), (3); Corollary L at every d | n_flat; the level d = 3 against 5/32 and
#    against c_{k0} c_{k1}; the union bound of section 4 with 5/32 at d = 3.
# mlist, nlist: comma separated.
import sys, math, random, time
from fractions import Fraction
import numpy as np
from rlib import factor, divisors, mu, nprime, contract_all, all_levels_full, crt
from rfast import bad_fast

seed = int(sys.argv[1]); budget = float(sys.argv[2])
MS = [int(a) for a in sys.argv[3].split(",")]
NS = [int(a) for a in sys.argv[4].split(",")]
rng = random.Random(seed)
t0 = time.time()
if max(MS) >= 20:
    budget = min(budget, 170.0)       # one multiset of 22 or 24 elements can take a minute; the run is stopped at 290 s


def c(k):
    return Fraction(math.comb(k, k // 2), 2 ** k)


def crt_all(res, fac):
    x, M = 0, 1
    for p, a in fac.items():
        x = crt(x, M, res[p], p ** a)
        M *= p ** a
    return x


def full_residues(p, a, m):
    pa = p ** a
    s = rng.randrange(pa)
    out = [s]
    for i in range(1, a + 1):
        base = s % p ** (i - 1)
        dig = (s // p ** (i - 1)) % p
        for e in range(p):
            if e != dig:
                out.append((base + e * p ** (i - 1) + p ** i * rng.randrange(pa // p ** i)) % pa)
    style = rng.random()
    while len(out) < m:
        r = rng.random()
        if style < 0.34:                       # balanced: spread over the classes
            out.append(rng.randrange(pa))
        elif style < 0.67:                     # heavy repetition
            out.append(rng.choice(out) if r < 0.85 else rng.randrange(pa))
        else:                                  # near copies
            out.append((rng.choice(out) + p ** rng.randrange(a) * rng.randrange(p)) % pa if r < 0.8 else rng.randrange(pa))
    return out


def gen(n, m, kind):
    fac = factor(n)
    while True:
        if kind == "random":
            B = [rng.randrange(n) for _ in range(m)]
        elif kind == "cluster":
            pool = [rng.randrange(n) for _ in range(rng.randint(3, 7))]
            B = [rng.choice(pool) for _ in range(m)]
        elif kind == "pairs":                  # every element twice or more: many signings bad at d = 1 and elsewhere
            pool = [rng.randrange(n) for _ in range(m // 2)]
            B = pool + pool
        elif kind == "coset":
            g = rng.choice([d for d in divisors(n) if 1 < d <= m])
            B = []
            while len(B) + g <= m:
                a0 = rng.randrange(n)
                B += [(a0 + j * (n // g)) % n for j in range(g)]
            while len(B) < m:
                B.append(rng.choice(B))
        else:                                  # full
            cols = {}
            for p, a in fac.items():
                col = full_residues(p, a, m)
                if rng.random() < 0.7:
                    rng.shuffle(col)
                cols[p] = col
            B = [crt_all({p: cols[p][k] for p in fac}, fac) for k in range(m)]
        if len({x % 3 for x in B}) == 3:
            return B


viol = {"F": 0, "C1": 0, "C2": 0, "C3": 0, "D": 0, "L3": 0, "E": 0}
pairs_total = pairs_live = 0      # pairs (contracted multiset, d > 1), and those with at least one signing bad at d
rows = {}
total = 0
kinds = ["full", "full", "full", "random", "cluster", "pairs", "coset"]
while time.time() - t0 < budget:
    n = rng.choice(NS)
    m = rng.choice(MS)
    fac = factor(n)
    need = max(1 + a * (p - 1) for p, a in fac.items())
    kind = rng.choice(kinds)
    if kind == "full" and need > m:
        kind = "random"
    B = gen(n, m, kind)
    full = 1 << m
    total += 1
    anybad = np.zeros(full, dtype=bool)
    nb = {}
    for d in divisors(n):
        v = bad_fast(B, d)
        nb[d] = int(v.sum())
        anybad |= v
    good = full - int(anybad.sum())
    frac = Fraction(good, full)
    if not frac > Fraction(39, 1000):
        viol["F"] += 1
        print("VIOLATION F", n, B, frac)
    Bf, nf, steps = contract_all(B, n, "deep")
    if not all_levels_full(Bf, nf):
        viol["C2"] += 1
        print("VIOLATION C2", n, B, Bf, nf)
    if nprime(m) % nf:
        viol["C3"] += 1
        print("VIOLATION C3", n, B, Bf, nf)
    if steps:
        anyf = np.zeros(full, dtype=bool)
        nbf = {}
        for d in divisors(nf):
            v = bad_fast(Bf, d)
            nbf[d] = int(v.sum())
            anyf |= v
        if (~anyf & anybad).any():
            viol["C1"] += 1
            print("VIOLATION C1", n, B, Bf, nf)
        badf = int(anyf.sum())
    else:
        nbf = nb
        badf = full - good
    bound = c(m)
    p3 = None
    for d, k in nbf.items():
        if d == 1:
            assert Fraction(k, full) == c(m)
            continue
        pairs_total += 1
        pairs_live += k > 0
        if k << mu(d) > full:
            viol["D"] += 1
            print("VIOLATION D", n, B, Bf, nf, d, k)
        if d == 3:
            ks = sorted((sum(1 for x in Bf if x % 3 == r) for r in range(3)), reverse=True)
            p3 = Fraction(k, full)
            if p3 > Fraction(5, 32) or p3 > c(ks[0]) * c(ks[1]) or ks[2] < 1 or ks[0] < -(-m // 3):
                viol["L3"] += 1
                print("VIOLATION L3", n, B, Bf, nf, k, ks)
            bound += Fraction(5, 32)
        else:
            bound += Fraction(1, 2 ** mu(d))
    if Fraction(badf, full) > bound:
        viol["E"] += 1
        print("VIOLATION E", n, B, Bf, nf, badf, bound)
    r = rows.setdefault((m, kind), {"cnt": 0, "minfrac": Fraction(2), "arg": None, "max3": Fraction(0), "nf_eq_n": 0, "contr": 0, "maxratio": Fraction(0)})
    r["cnt"] += 1
    if frac < r["minfrac"]:
        r["minfrac"] = frac
        r["arg"] = (n, sorted(B))
    if p3 is not None:
        r["max3"] = max(r["max3"], p3)
    r["nf_eq_n"] += nf == n
    r["contr"] += bool(steps)
    r["maxratio"] = max(r["maxratio"], Fraction(badf, full) / bound)

print("seed %d, m in %s, groups %s: %d multisets with all three classes modulo 3 occupied" % (seed, MS, NS, total))
for (m, kind), r in sorted(rows.items()):
    print("  m = %2d %-7s %4d multisets (%d with n_flat = n, %d contracted): least good fraction %.4f; largest fraction bad at d = 3 after contraction %.4f; largest bad/bound %.3f"
          % (m, kind, r["cnt"], r["nf_eq_n"], r["contr"], float(r["minfrac"]), float(r["max3"]), float(r["maxratio"])))
print("pairs (contracted multiset, level d > 1): %d, of them with at least one signing bad at d: %d" % (pairs_total, pairs_live))
worst = min(rows.values(), key=lambda r: r["minfrac"])
print("least good fraction overall: %.5f at %s" % (float(worst["minfrac"]), worst["arg"]))
print("violations:", viol, "  seconds %.0f" % (time.time() - t0))
