# contract_rand.py seed budget_seconds mlo mhi n1 n2 ... -- random and structured multisets on larger groups, all 2^m signings,
# exact division (rfast.py).  For each multiset B on Z_n:
#  A. Lemma L, first part, on B itself, for every d | n, d > 1 and every prime p | d.
#  B. Lemma 1(b): "bad at d" equals "flat on every group at level v_p(d) of the p-tree" (slices modulo Phi_{d''}), for
#     every d | n and every p | d (only for m <= 12).
#  C. contraction in four orders (deepest first, shallowest first, two random): (1) good for B_flat => good for B,
#     (2) every level of every tree of B_flat has a full group, (3) n_flat | n'_m.
#  D. Corollary L for B_flat: #bad at d <= 2^(m - mu(d)) for every d | n_flat, d > 1.
#  E. union bound for B_flat;  F. the stated bounds for B.
# Kinds: "random"; "full" (a full group at every level of every tree, the other elements random, copied or near);
# "partfull" (full for some primes/levels only, digits inserted elsewhere); "cluster" (few points, repeated);
# "coset" (union of cosets with noise).
import sys, math, random, time
from fractions import Fraction
import numpy as np
from rlib import factor, divisors, mu, nprime, vp, groups, has_full_group, contractible, contract, contract_all, \
    all_levels_full, lemmaL_e, crt
from rfast import ptable, bad_fast, all_signed_sums

seed = int(sys.argv[1]); budget = float(sys.argv[2]); mlo = int(sys.argv[3]); mhi = int(sys.argv[4])
NS = [int(a) for a in sys.argv[5:]]
rng = random.Random(seed)
t0 = time.time()


def A_formula(t):
    r = 1
    for p in range(3, t + 2, 2):
        if all(p % q for q in range(3, int(p ** 0.5) + 1, 2)):
            r *= 1 + t // (p - 1)
    return r


WUP = sum(Fraction(A_formula(t) - A_formula(t - 2), 2 ** t) for t in range(2, 401, 2)) + Fraction(1, 10 ** 9)
SIX = {2: Fraction(1, 2), 4: Fraction(3, 8), 6: Fraction(3, 16), 8: Fraction(9, 128), 10: Fraction(11, 256), 12: Fraction(23, 1024)}


def c(k):
    return Fraction(math.comb(k, k // 2), 2 ** k)


def stated_ok(m, frac):
    if m % 2 == 1:
        return frac > 1 - WUP
    if m <= 12:
        return frac >= SIX[m]
    return frac > Fraction(39, 1000)


def crt_all(res, fac):
    """res: {p: residue mod p^a}; returns the element of Z_n."""
    x, M = 0, 1
    for p, a in fac.items():
        x = crt(x, M, res[p], p ** a)
        M *= p ** a
    return x


def full_residues(p, a, m, levels=None):
    """m residues modulo p^a with a full group at every level in `levels` (default all)."""
    pa = p ** a
    s = rng.randrange(pa)
    out = [s]
    for i in (levels if levels is not None else range(1, a + 1)):
        base = s % p ** (i - 1)
        dig = (s // p ** (i - 1)) % p
        for e in range(p):
            if e != dig:
                out.append((base + e * p ** (i - 1) + p ** i * rng.randrange(pa // p ** i)) % pa)
    assert len(out) <= m
    while len(out) < m:
        r = rng.random()
        if r < 0.4:
            out.append(rng.randrange(pa))
        elif r < 0.75:
            out.append(rng.choice(out))
        else:
            out.append((rng.choice(out) + p ** rng.randrange(a) * rng.randrange(p)) % pa)
    return out


def gen(n, m, kind):
    fac = factor(n)
    if kind == "random":
        return [rng.randrange(n) for _ in range(m)]
    if kind == "cluster":
        pool = [rng.randrange(n) for _ in range(rng.randint(1, max(1, m // 2)))]
        return [rng.choice(pool) for _ in range(m)]
    if kind == "coset":
        g = rng.choice([d for d in divisors(n) if 1 < d <= m] or [1])
        B = []
        while len(B) + g <= m:
            a0 = rng.randrange(n)
            B += [(a0 + j * (n // g)) % n for j in range(g)]
        while len(B) < m:
            B.append(rng.choice(B) if B and rng.random() < 0.5 else rng.randrange(n))
        return B
    if kind in ("full", "partfull"):
        cols = {}
        for p, a in fac.items():
            if kind == "full":
                lv = None
            else:
                lv = [i for i in range(1, a + 1) if rng.random() < 0.5]
                while 1 + len(lv) * (p - 1) > m:
                    lv.pop()
            col = full_residues(p, a, m, lv)
            if rng.random() < 0.7:
                rng.shuffle(col)
            cols[p] = col
        return [crt_all({p: cols[p][k] for p in fac}, fac) for k in range(m)]
    raise ValueError(kind)


def flat_fast(B, n, p, i, d2, E):
    a = vp(n, p)
    pa = p ** a
    n2 = n // pa
    P = ptable(d2).astype(np.int64)
    idx = {}
    for k, x in enumerate(B):
        u = x % pa
        idx.setdefault(u % p ** (i - 1), {}).setdefault(u % p ** i, []).append(k)
    ok = np.ones(E.shape[0], dtype=bool)
    zero = np.zeros((E.shape[0], P.shape[1]), dtype=np.int64)
    for cl, subs in idx.items():
        sl = []
        for e in range(p):
            ks = subs.get(cl + p ** (i - 1) * e)
            sl.append(E[:, ks] @ P[[(B[k] % n2) % d2 for k in ks]] if ks else zero)
        for s in sl[1:]:
            ok &= ~(s - sl[0]).any(axis=1)
    return ok


_E = {}


def signsE(m):
    if m not in _E:
        r = np.arange(1 << m, dtype=np.int64)[:, None]
        _E[m] = 1 - 2 * ((r >> np.arange(m, dtype=np.int64)[None, :]) & 1)
    return _E[m]


viol = {"A": 0, "B": 0, "C1": 0, "C2": 0, "C3": 0, "D": 0, "E": 0, "F": 0}
stats = {}
kinds = ["random", "full", "full", "full", "partfull", "partfull", "cluster", "coset"]
total = 0
while time.time() - t0 < budget:
    n = rng.choice(NS)
    fac = factor(n)
    need = max(1 + a * (p - 1) for p, a in fac.items())
    kind = rng.choice(kinds)
    lo = max(mlo, need) if kind == "full" else mlo
    if lo > mhi:
        kind = "partfull"
        lo = mlo
    m = rng.randint(lo, mhi)
    B = gen(n, m, kind)
    full = 1 << m
    total += 1
    st = stats.setdefault((n, kind), {"cnt": 0, "contr": 0, "nflat_eq_n": 0, "attA": 0, "attD": 0, "chkA": 0, "chkB": 0, "chkD": 0,
                                      "minfrac": Fraction(2), "maxratio": Fraction(0), "ends": 0, "allfullB": 0, "liveD": 0})
    st["cnt"] += 1
    divs = divisors(n)
    bad = {d: bad_fast(B, d) for d in divs}
    anybad = np.zeros(full, dtype=bool)
    for v in bad.values():
        anybad |= v
    E = signsE(m) if m <= 12 else None
    for d in divs:
        if d == 1:
            continue
        nb = int(bad[d].sum())
        for p, i in factor(d).items():
            e = lemmaL_e(B, p, i)
            st["chkA"] += 1
            if nb << e > full:
                viol["A"] += 1
                print("VIOLATION A", n, B, d, p, nb, e)
            if nb << e == full:
                st["attA"] += 1
            if E is not None:
                st["chkB"] += 1
                if (flat_fast(B, n, p, i, d // p ** i, E) != bad[d]).any():
                    viol["B"] += 1
                    print("VIOLATION B", n, B, d, p)
    if all_levels_full(B, n):
        st["allfullB"] += 1
    seen = set()
    for order in ("deep", "shallow", "random", "random"):
        Bf, nf, steps = contract_all(B, n, order, rng)
        key = (tuple(Bf), nf)
        if key in seen:
            continue
        seen.add(key)
        if order == "deep":
            if steps:
                st["contr"] += 1
            if nf == n:
                st["nflat_eq_n"] += 1
        if not all_levels_full(Bf, nf):
            viol["C2"] += 1
            print("VIOLATION C2", n, B, Bf, nf)
        if nprime(m) % nf:
            viol["C3"] += 1
            print("VIOLATION C3", n, B, Bf, nf)
        badf = {d: bad_fast(Bf, d) for d in divisors(nf)} if steps else bad
        anyf = np.zeros(full, dtype=bool)
        for v in badf.values():
            anyf |= v
        if (~anyf & anybad).any():
            viol["C1"] += 1
            print("VIOLATION C1", n, B, Bf, nf)
        bound = c(m) if m % 2 == 0 else Fraction(0)
        for d, v in badf.items():
            if d == 1:
                continue
            nb = int(v.sum())
            st["chkD"] += 1
            md = mu(d)
            st["liveD"] += nb > 0
            if nb << md > full:
                viol["D"] += 1
                print("VIOLATION D", n, B, Bf, nf, d, nb)
            if nb << md == full:
                st["attD"] += 1
            bound += Fraction(1, 2 ** md)
        nbadf = int(anyf.sum())
        if Fraction(nbadf, full) > bound:
            viol["E"] += 1
            print("VIOLATION E", n, B, Bf, nf, nbadf, bound)
        if bound > 0:
            st["maxratio"] = max(st["maxratio"], Fraction(nbadf, full) / bound)
    st["ends"] += len(seen)
    frac = Fraction(full - int(anybad.sum()), full)
    if not stated_ok(m, frac):
        viol["F"] += 1
        print("VIOLATION F", n, B, frac)
    st["minfrac"] = min(st["minfrac"], frac)

print("seed %d, %d..%d elements, groups %s: %d multisets" % (seed, mlo, mhi, NS, total))
tot = {}
for (n, kind), st in sorted(stats.items()):
    print("  Z_%-5d %-8s %4d multisets, %4d contracted, %4d with n_flat = n, %4d with every level full; distinct ends %d; A: %d checks (attained %d); B: %d checks; D: %d checks (attained %d); least good fraction %.4f; largest bad/bound %.3f"
          % (n, kind, st["cnt"], st["contr"], st["nflat_eq_n"], st["allfullB"], st["ends"], st["chkA"], st["attA"], st["chkB"], st["chkD"], st["attD"], float(st["minfrac"]), float(st["maxratio"])))
    for k in ("cnt", "contr", "nflat_eq_n", "allfullB", "ends", "chkA", "attA", "chkB", "chkD", "attD", "liveD"):
        tot[k] = tot.get(k, 0) + st[k]
print("totals:", tot)
print("(liveD: pairs (contracted multiset, level d > 1) with at least one signing bad at d, among the chkD pairs)")
print("least good fraction overall: %.4f" % float(min(st["minfrac"] for st in stats.values())))
print("violations:", viol, "  seconds %.0f" % (time.time() - t0))
