# Referee's exact count on a prime-power modulus p^v for multisets given with multiplicities, without listing
# signings: for every class (node of the tree of p) the number of signings of its elements with a given sum of
# signs s and a given set ("mask") of deeper levels at which every group inside the class is flat (subclass sums
# equal).  Events F_i (bad at p^i) are taken from their definition by class sums (the slice criterion with the
# root 1; brute.py tests that criterion against division by Phi_d).  Convolutions by Kronecker substitution in
# Python integers: everything is exact.
#   bad at some p^i (i >= 0)  <=>  s = 0 at the root or the root's mask is not empty;  X_p = mask not empty, s != 0.
# Asserted for every multiset: Theorem 1 / Theorem 2 / Corollary 3 bounds, the table bound \hat E_p(m) where I have
# it, and Lemma 2 with the TRUE x_t for every node with at least two occupied subclasses (each node is a multiset).
# usage: tree.py p v seed count mode
import sys, math, random
from fractions import Fraction as F
from math import comb

def conv(a, b, nb):
    A = int.from_bytes(b"".join(x.to_bytes(nb, "little") for x in a), "little")
    B = int.from_bytes(b"".join(x.to_bytes(nb, "little") for x in b), "little")
    n = len(a) + len(b) - 1
    cb = (A * B).to_bytes(nb * (n + 1), "little")
    return [int.from_bytes(cb[i * nb:(i + 1) * nb], "little") for i in range(n)]

def load(name):
    T = {}
    try:
        for line in open(name):
            w = line.split(); T[int(w[0])] = int(w[1], 16)
    except FileNotFoundError:
        pass
    return T
ETAB = {3: load("mytable3-1000.txt"), 5: load("mytable5.txt"), 7: load("mytable7.txt")}
def cc(r): return F(comb(r, r // 2), 1 << r) if r % 2 == 0 else F(0)
def pS(r, v): return F(comb(r, (r + v) // 2), 1 << r) if (r - v) % 2 == 0 and abs(v) <= r else F(0)

stats = dict(nodes=0, eq=0, worst=F(0))
def node(p, v, depth, items, nb):
    """items: dict residue -> multiplicity, all in one class modulo p^depth.
    returns (r, dist, x) : dist = dict mask -> list over s (index s + r); x = P(X_p(this class as a multiset))."""
    r = sum(items.values())
    if depth == v:
        (res, mu), = items.items()
        return r, {0: [comb(mu, i // 2) if i % 2 == 0 else 0 for i in range(2 * mu + 1)]}, F(0)
    kids = {}
    for res, mu in items.items(): kids.setdefault((res // p ** depth) % p, {})[res] = mu
    ch = [node(p, v, depth + 1, it, nb) for it in kids.values()]
    k = len(ch)
    below = 0
    for i in range(depth + 2, v + 1): below |= 1 << i
    bit = 1 << (depth + 1)
    # all signings: sums add, masks intersect
    acc = {below: [1]}
    for (rt, dt, xt) in ch:
        new = {}
        for ma, la in acc.items():
            for mc, lc in dt.items():
                pr = conv(la, lc, nb); key = ma & mc
                if key in new: new[key] = [x + y for x, y in zip(new[key], pr)]
                else: new[key] = pr
        acc = new
    # the signings with all p subclass sums equal (an empty subclass has sum 0)
    rmin = min(rt for rt, _, _ in ch)
    vals = range(-rmin, rmin + 1) if k == p else [0]
    dia = {below: {val: 1 for val in vals}}
    for (rt, dt, xt) in ch:
        new = {}
        for ma, da in dia.items():
            for mc, lc in dt.items():
                key = ma & mc; tgt = new.setdefault(key, {})
                for val, w in da.items():
                    t = w * lc[val + rt]
                    if t: tgt[val] = tgt.get(val, 0) + t
        dia = new
    out = {m_: l[:] for m_, l in acc.items()}
    for mk, da in dia.items():
        for val, w in da.items():
            if not w: continue
            s = k * val if k == p else 0
            out[mk][s + r] -= w
            out.setdefault(mk | bit, [0] * (2 * r + 1))[s + r] += w
    for l in out.values(): assert min(l) >= 0
    assert sum(sum(l) for l in out.values()) == 1 << r
    x = F(sum(sum(l) - l[r] for m_, l in out.items() if m_), 1 << r)
    if k >= 2:
        # Lemma 2 for this class as a multiset, with the true x_t of its subclasses
        pu = F(1); pc = F(1)
        for (rt, dt, xt) in ch: pu *= cc(rt) + xt; pc *= cc(rt)
        bound = pu - pc
        if k == p:
            g = F(0)
            for val in range(-rmin, rmin + 1):
                if val:
                    t = F(1)
                    for (rt, _, _) in ch: t *= pS(rt, val)
                    g += t
            bound += g
        if p == 3 and k == 2 and all(rt in (3, 5, 7) for rt, _, _ in ch):
            bound = ch[0][2] * ch[1][2] / 2
        stats["nodes"] += 1
        assert x <= bound, ("LEMMA 2 FAILS", p, v, depth, items, x, bound)
        if x == bound: stats["eq"] += 1
    return r, out, x

def analyse(p, v, items):
    m = sum(items.values()); nb = (m + 16) // 8 + 1
    r, dist, x = node(p, v, 0, items, nb)
    f0 = F(sum(l[r] for l in dist.values()), 1 << r)
    assert f0 == cc(m)
    return m, f0, x

def a_p(p):
    return F(str(round(math.sqrt(p) * 2.0 ** (1 - p) / (1 - 0.8165 * math.sqrt(p) * 2.0 ** (2 - p)) * (1 - 1e-9), 12)))

def le_over_sqrt(share, num, m):       # share <= num/sqrt(m), exactly (num rational)
    return share * share * m <= num * num

def check(p, v, items, rec):
    m, f0, x = analyse(p, v, items)
    tot = f0 + x; rt = math.sqrt(m); ok = True
    if p == 3:
        lim = F("0.9487") if m % 2 == 0 else F("0.4331")
        if m > 1000 and m % 2 == 0: lim = F("0.9379")
        if m > 200 and m % 2 == 1: lim = F("0.40")
        ok &= le_over_sqrt(tot, lim, m)
        if m in ETAB[3]:
            ok &= x <= F(ETAB[3][m], 1 << m)
            rec["tab"] = max(rec["tab"], (x / F(ETAB[3][m], 1 << m)) if ETAB[3][m] else F(0)); rec["ntab"] += 1
            if m % 2 == 1 and m >= 5: ok &= tot <= pS(m - 2, 1) / 2
        rec["rat"] = max(rec["rat"], float(tot) * rt / float(lim))
    else:
        ok &= le_over_sqrt(x, a_p(p), m) and le_over_sqrt(tot, F("0.979") if m % 2 == 0 else F("0.182"), m)
        if m in ETAB.get(p, {}):
            ok &= x <= F(ETAB[p][m], 1 << m); rec["ntab"] += 1
            if ETAB[p][m]: rec["tab"] = max(rec["tab"], x / F(ETAB[p][m], 1 << m))
        rec["rat"] = max(rec["rat"], float(x) * rt / float(a_p(p)))
        rec["tau"] = max(rec["tau"], float(x) * rt / (math.sqrt(p) * 2.0 ** (1 - p)))
    ok &= le_over_sqrt(tot, F(1), m)
    par = m % 2
    if float(tot) * rt > rec["best"][par][0]: rec["best"][par] = (float(tot) * rt, m, dict(sorted(items.items())))
    if float(x) * rt > rec["bestx"][par][0]: rec["bestx"][par] = (float(x) * rt, m, dict(sorted(items.items())))
    rec["n"] += 1; rec["big"] += m > 1000; rec["nx"] += x > 0; rec["mmax"] = max(rec["mmax"], m)
    if not ok:
        rec["fail"] += 1; print("FAILURE:", p, v, items, m, tot, x, flush=True)

def rand_items(p, v, rng, mode):
    n = p ** v
    def mult(kind):
        if kind == "one": return 1
        if kind == "two": return 2
        if kind == "even": return 2 * rng.randint(1, 4)
        if kind == "small": return rng.randint(1, 4)
        return rng.randint(1, 12)
    items = {}
    shape = rng.choice(["rand", "heavy", "even", "deep", "full", "twoheavy", "pairs"])
    if shape == "rand":
        for _ in range(rng.randint(2, 9)): items[rng.randrange(n)] = mult(rng.choice(["one", "two", "small", "any"]))
    elif shape == "heavy":
        for _ in range(rng.randint(1, 8)): items[rng.randrange(n)] = mult(rng.choice(["one", "two", "small"]))
        items[0] = rng.choice([8, 15, 30, 31, 60, 101, 200])
    elif shape == "even":
        for _ in range(rng.randint(2, 9)): items[rng.randrange(n)] = mult("even")
    elif shape == "deep":
        for _ in range(rng.randint(3, 10)):
            i = rng.randrange(v); items[(rng.randrange(1, p) * p ** i + rng.choice([0, 0, n // p * rng.randrange(p)])) % n] = mult(rng.choice(["one", "two", "small"]))
        items[0] = rng.choice([1, 2, 4, 10, 20, 50])
    elif shape == "full":
        i = rng.randrange(v); base = rng.randrange(p ** i); kind = rng.choice(["one", "two", "small", "even"])
        for t in range(p): items[(base + t * p ** i + p ** (i + 1) * rng.randrange(p ** (v - i - 1))) % n] = mult(kind)
        if rng.random() < 0.6: items[base % n] = items.get(base % n, 0) + rng.choice([2, 5, 10, 20, 40, 81])
        for _ in range(rng.randint(0, 4)): items[rng.randrange(n)] = mult(rng.choice(["one", "two"]))
    elif shape == "twoheavy":
        items[0] = rng.randint(5, 40); items[rng.randrange(1, n)] = rng.randint(5, 40)
        for _ in range(rng.randint(0, 6)): items[rng.randrange(n)] = mult(rng.choice(["one", "two"]))
    else:
        for i in range(v):
            for t in range(1, p):
                if rng.random() < 0.8: items[t * p ** i] = 2
        items[0] = 2 * rng.randint(0, 40)
    items = {b: mu for b, mu in items.items() if mu > 0}
    if mode == "big" and items:
        b = rng.choice(list(items)); items[b] += rng.choice([1000, 1001, 1500, 2001, 3000])
    return items

if __name__ == "__main__":
    p = int(sys.argv[1]); v = int(sys.argv[2]); seed = int(sys.argv[3]); count = int(sys.argv[4]); mode = sys.argv[5] if len(sys.argv) > 5 else "mid"
    rng = random.Random(seed)
    rec = dict(n=0, big=0, nx=0, fail=0, tab=F(0), ntab=0, rat=0.0, tau=0.0, mmax=0, best=[(0, 0, None), (0, 0, None)], bestx=[(0, 0, None), (0, 0, None)])
    for _ in range(count):
        items = rand_items(p, v, rng, mode)
        if items: check(p, v, items, rec)
    print(f"p = {p}, modulus {p**v}, seed {seed}, mode {mode}: {rec['n']} multisets (largest m = {rec['mmax']}; {rec['big']} with m > 1000; X_p nonempty in {rec['nx']}); "
          f"{rec['ntab']} compared with my table (largest true/table = {float(rec['tab']):.4f}); largest ratio to the claimed bound = {rec['rat']:.4f}"
          + (f"; largest X_p sqrt(m)/tau_p = {rec['tau']:.4f}" if p > 3 else "")
          + f"; Lemma 2 with true x_t at {stats['nodes']} nodes (equality at {stats['eq']}); FAILURES: {rec['fail']}")
    for par in (0, 1):
        print(f"   m {'even' if par == 0 else 'odd'}: largest sqrt(m) x (share bad at a power of p) = {rec['best'][par][0]:.6f} at m = {rec['best'][par][1]}: {rec['best'][par][2]};"
              f" largest sqrt(m) x P(X_p) = {rec['bestx'][par][0]:.6f} at m = {rec['bestx'][par][1]}: {rec['bestx'][par][2]}")
