# Referee's exact count on ANY odd modulus for multisets given with multiplicities: every signing is counted
# through the signed sums of the distinct residues (weights = products of binomial coefficients, Python integers),
# and "bad at d" is decided from the definition, for every d | n, by reducing sum_i v_i X^(b_i) modulo Phi_d
# (integer matrix of X^j mod Phi_d).  Tests Corollaries 4 and 5 (and with them Theorems 1, 2 inside a composite
# modulus) on multisets with several primes live, heavy elements, all multiplicities even, few distinct residues.
# usage: grid.py seed count [mode] [seconds]   (stops at the count or at the clock, whichever comes first)
import sys, math, random, itertools, time
T0 = time.time()
import numpy as np
from fractions import Fraction as F
from math import comb

def divisors(n): return [d for d in range(1, n + 1) if n % d == 0]
def pdiv(num, den):
    num = num[:]; q = [0] * (len(num) - len(den) + 1)
    for i in range(len(q) - 1, -1, -1):
        t = num[i + len(den) - 1]; q[i] = t
        for j, dj in enumerate(den): num[i + j] -= t * dj
    assert not any(num)
    return q
_cy = {}
def cyclo(d):
    if d not in _cy:
        num = [-1] + [0] * (d - 1) + [1]
        for e in divisors(d):
            if e < d: num = pdiv(num, cyclo(e))
        _cy[d] = num
    return _cy[d]
_rm = {}
def redmat(d):
    if d not in _rm:
        ph = cyclo(d); k = len(ph) - 1
        cols = []; cur = [1] + [0] * (k - 1)
        for j in range(d):
            cols.append(cur[:])
            t = cur[-1]; cur = [0] + cur[:-1]
            if t:
                for i in range(k): cur[i] -= t * ph[i]
        _rm[d] = np.array(cols, dtype=np.int64).T
    return _rm[d]
def factor(n):
    f = {}; p = 3
    while n > 1:
        while n % p == 0: f[p] = f.get(p, 0) + 1; n //= p
        p += 2
    return f
def load(name):
    T = {}
    try:
        for line in open(name):
            w = line.split(); T[int(w[0])] = int(w[1], 16)
    except FileNotFoundError:
        pass
    return T
ETAB = {3: load("mytable3-1000.txt"), 5: load("mytable5.txt"), 7: load("mytable7.txt")}
def a_p(p):
    tau = math.sqrt(p) * 2.0 ** (1 - p); return tau / (1 - 0.8165 * math.sqrt(p) * 2.0 ** (2 - p))

def counts(n, items):
    """items: dict residue -> multiplicity.  Returns m and exact numbers of signings: bad (any d), bad at 1 or a prime
    power, dict p -> |X_p|, |bad at 1|, dict d -> count."""
    res = sorted(items); mus = [items[b] for b in res]; m = sum(mus)
    axes = [np.arange(-mu, mu + 1, 2, dtype=np.int64) for mu in mus]
    grids = np.meshgrid(*axes, indexing="ij")
    shape = grids[0].shape
    V = np.stack([g.ravel() for g in grids], axis=1)          # (outcomes, k)
    bad = {}
    for d in divisors(n):
        R = redmat(d)                                          # (phi, d)
        cols = R[:, [b % d for b in res]]                      # (phi, k)
        bad[d] = ~((V @ cols.T) != 0).any(axis=1)
    wts = [np.array([comb(mu, i) for i in range(mu + 1)], dtype=object) for mu in mus]
    def weight(mask):
        T = mask.reshape(shape).astype(object)
        for w in reversed(wts): T = T.dot(w)
        return int(T)
    fac = factor(n)
    tot = np.zeros(len(V), dtype=bool)
    for d in bad: tot |= bad[d]
    pp = bad[1].copy(); X = {}; PB = {}
    for p, v in fac.items():
        x = np.zeros(len(V), dtype=bool)
        for i in range(1, v + 1): x |= bad[p ** i]
        pp |= x; X[p] = weight(x & ~bad[1]); PB[p] = x | bad[1]
    # live primes, from the definition
    live = []
    for p, v in fac.items():
        for i in range(1, v + 1):
            cl = {}
            for b in res: cl.setdefault(b % p ** (i - 1), set()).add(b % p ** i)
            if any(len(s) == p for s in cl.values()): live.append(p); break
    same = None
    if len(live) <= 1:
        want = PB[live[0]] if live else bad[1]
        same = bool((want == tot).all())
    return m, weight(tot), weight(pp), X, weight(bad[1]), live, same, weight(tot & ~pp)

def rand_items(rng, mode):
    n = rng.choice([15, 21, 35, 45, 63, 75, 105, 135, 147, 175, 225, 315, 525, 945, 1155])
    fac = factor(n); items = {}
    def mult(kind):
        return {"one": 1, "two": 2, "even": 2 * rng.randint(1, 3), "small": rng.randint(1, 3)}[kind]
    if mode == "four":                      # at most four distinct residues, any multiplicities
        k = rng.randint(1, 4)
        base = rng.choice([1, 1, n // 3, n // 3, n // 5 if n % 5 == 0 else 1, 1])
        while len(items) < k:
            b = (rng.randrange(n) * base) % n if rng.random() < 0.7 else rng.randrange(n)
            items[b] = rng.choice([1, 1, 2, 2, 3, 4, 5, 6, 8, 11, 16, 25, 40])
        return n, items
    shape = rng.choice(["groups", "groups", "heavy", "pairs", "rand", "even"])
    if shape in ("groups", "heavy", "pairs"):
        # full groups at chosen levels of several primes (so that several primes are live), with a common element 0
        kind = "two" if shape == "pairs" else rng.choice(["one", "one", "two", "small"])
        for p, v in fac.items():
            if rng.random() < 0.8:
                i = rng.randrange(v) + 1          # level i: the nonzero multiples of n/p^i in the class of 0
                for t in range(1, p):
                    if p <= 7 or rng.random() < 1.0: items[(t * n // p ** i) % n] = mult(kind)
        items[0] = items.get(0, 0) + (rng.choice([1, 2, 6, 10, 15, 20, 30]) if shape != "groups" else mult(kind))
    elif shape == "rand":
        for _ in range(rng.randint(3, 8)): items[rng.randrange(n)] = mult(rng.choice(["one", "two", "small"]))
    else:
        for _ in range(rng.randint(2, 7)): items[rng.randrange(n)] = mult("even")
    if rng.random() < 0.3: items[rng.randrange(n)] = mult("one")
    return n, items

if __name__ == "__main__":
    rng = random.Random(int(sys.argv[1])); count = int(sys.argv[2]); mode = sys.argv[3] if len(sys.argv) > 3 else "mix"
    nd = 0; fails = 0; n5 = 0; n4 = 0; nlive2 = 0; best = {0: (0, None), 1: (0, None)}; bestpp = {0: 0, 1: 0}; bestc = (0, None); best5 = {0: 0, 1: 0}; mmax = 0
    bestsharp = 0
    budget = float(sys.argv[4]) if len(sys.argv) > 4 else 100.0
    while nd < count and time.time() - T0 < budget:
        n, items = rand_items(rng, mode)
        size = 1
        for mu in items.values(): size *= mu + 1
        if size * n > 8000000 or not items: continue
        m, tot, pp, X, b1, live, same, comp = counts(n, items); nd += 1; mmax = max(mmax, m)
        N = 1 << m; rt = math.sqrt(m); par = m % 2; ok = True
        assert b1 == (comb(m, m // 2) if m % 2 == 0 else 0)
        # Corollary 4 (explicit constants) and its sharper form c + sum of table values / a_p
        ok &= F(pp, N) ** 2 * m <= (F("1.18") if par == 0 else F("0.67")) ** 2
        sharp = F(b1, N)
        for p in factor(n):
            if p in ETAB and m in ETAB[p]:
                ok &= X[p] <= ETAB[p][m]; sharp += F(ETAB[p][m], N)
            else:
                sharp += F(str(round(a_p(p) * (1 + 1e-9), 12))) / F(str(round(rt * (1 - 1e-12), 12))) if p >= 5 else F(1)
            if p >= 5: ok &= X[p] / N * rt <= a_p(p)
            if p == 3: ok &= F(b1 + X[3], N) ** 2 * m <= (F("0.9487") if par == 0 else F("0.4331")) ** 2
        ok &= F(pp, N) <= sharp
        if sharp > 0: bestsharp = max(bestsharp, float(F(pp, N) / sharp))
        bestpp[par] = max(bestpp[par], pp / N * rt)
        if tot / N * rt > best[par][0]: best[par] = (tot / N * rt, (n, dict(sorted(items.items()))))
        if comp / N * rt > bestc[0]: bestc = (comp / N * rt, (n, m, dict(sorted(items.items())), str(F(comp, N))))
        # Corollary 5
        if len(live) <= 1:
            n5 += 1
            lim = F("0.979") if (live and live[0] >= 5) else (F("0.9487") if par == 0 else F("0.4331"))
            ok &= same and F(tot, N) ** 2 * m <= lim ** 2
            best5[par] = max(best5[par], tot / N * rt / float(lim))
        else: nlive2 += 1
        if len(items) <= 4:
            n4 += 1; ok &= F(tot, N) ** 2 * m <= (F("0.9487") if par == 0 else F("0.4331")) ** 2
        if not ok: fails += 1; print("FAILURE:", n, items, m, F(tot, N), F(pp, N), X, live, same, flush=True)
    print(f"seed {sys.argv[1]}, mode {mode}: {nd} multisets, sizes up to {mmax}; two or more live primes in {nlive2}; at most one live prime in {n5}; at most four distinct residues in {n4}; FAILURES: {fails}")
    print(f"   largest sqrt(m) x bad share (every d): even {best[0][0]:.4f} at {best[0][1]}, odd {best[1][0]:.4f} at {best[1][1]}")
    print(f"   largest sqrt(m) x (bad at 1 or a prime power): even {bestpp[0]:.4f} (claimed 1.18), odd {bestpp[1]:.4f} (claimed 0.67); largest ratio to c + sum_p table/a_p: {bestsharp:.4f}")
    print(f"   Corollary 5: largest ratio of the bad share to its bound: even {best5[0]:.4f}, odd {best5[1]:.4f}")
    print(f"   largest sqrt(m) x (bad only at composite d): {bestc[0]:.4f} at {bestc[1]}")
