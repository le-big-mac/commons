# Referee's own exact tests: bad signings counted from the definition (remainder modulo Phi_d),
# multisets given with multiplicities. Lemmas and theorems of result.md checked in exact arithmetic.
import sys, math, itertools, random, time
from fractions import Fraction as Fr
import numpy as np
import ref_bounds as rb

def factor(n):
    f = {}
    p = 2
    while p * p <= n:
        while n % p == 0:
            f[p] = f.get(p, 0) + 1
            n //= p
        p += 1
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f

def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]

_cyc = {}
def cyclo(d):
    if d in _cyc:
        return _cyc[d]
    num = [-1] + [0] * (d - 1) + [1]
    for e in divisors(d):
        if e < d:
            den = cyclo(e)
            q = [0] * (len(num) - len(den) + 1)
            num = num[:]
            for i in range(len(q) - 1, -1, -1):
                q[i] = num[i + len(den) - 1] // den[-1]
                for j, dj in enumerate(den):
                    num[i + j] -= q[i] * dj
            assert not any(num)
            num = q
    _cyc[d] = num
    return num

_pw = {}
def powers(d):
    """rows j = 0..d-1: coefficients of X^j modulo Phi_d"""
    if d in _pw:
        return _pw[d]
    phi = cyclo(d)
    deg = len(phi) - 1
    cur = [1] + [0] * (deg - 1)
    rows = []
    for j in range(d):
        rows.append(cur)
        top = cur[-1]
        nxt = [0] + cur[:-1]
        if top:
            nxt = [nxt[i] - top * phi[i] for i in range(deg)]
        cur = nxt
    _pw[d] = np.array(rows, dtype=np.int64)
    return _pw[d]

CE = rb.c_exact(700)
def c(x):
    return CE[x] if x > 0 else Fr(1)
CNT = rb.cnt_formula(61)
CALC = rb.Calc(CE, True)
_B = {}
def Bm(m):
    if m not in _B:
        b = rb.B(CALC, m, CNT, True)
        be = None
        if m % 2 == 0:
            be = sum(rb.BE_parts(CALC, m, CNT, True))
        _B[m] = (b, be)
    return _B[m]

ST = {"multisets": 0, "fully live pairs": 0, "composite fully live": 0, "lemmaBC triples": 0, "lemmaC equal": 0,
      "lemmaE pairs": 0, "lemmaE positive": 0, "lemmaE' cases": 0, "lemmaF cases": 0, "lemmaF equal": 0, "failures": 0,
      "even multisets": 0, "thmA3 equal": 0}
MAXR = {}
def ratio(name, val, bound, info):
    if bound == 0:
        if val != 0:
            fail(name + " bound 0", info)
        return
    r = val / bound
    if name not in MAXR or r > MAXR[name][0]:
        MAXR[name] = (r, info)
def fail(what, info):
    ST["failures"] += 1
    print("FAILURE:", what, info, flush=True)

def analyse(n, mult, lemmas=True):
    res = sorted(mult)
    h = [mult[b] for b in res]
    m = sum(h)
    grids = [np.arange(-hb, hb + 1, 2, dtype=np.int64) for hb in h]
    T = np.stack(np.meshgrid(*grids, indexing="ij"), axis=-1).reshape(-1, len(res))
    big = m > 60
    W = np.array([1], dtype=object if big else np.int64)
    for hb in h:
        w = np.array([math.comb(hb, i) for i in range(hb + 1)], dtype=object if big else np.int64)
        W = np.multiply.outer(W, w).reshape(-1)
    tot = 2 ** m
    def cnt(mask):
        return int(W[mask].sum()) if mask.any() else 0
    divs = divisors(n)
    bad = {}
    for d in divs:
        P = powers(d)
        Md = P[[b % d for b in res]]          # r x phi
        V = T @ Md
        bad[d] = ~V.any(axis=1)
    badall = np.zeros(len(T), dtype=bool)
    for d in divs:
        badall |= bad[d]
    share = Fr(cnt(badall), tot)
    info = (n, tuple(sorted(mult.items())))
    ST["multisets"] += 1
    # --- the theorem itself
    par = "odd" if m % 2 else "even"
    ratio("share*sqrt(m), m %s" % par, math.sqrt(m) * float(share), 1.0, info)
    ratio("share*sqrt(m)/claimed constant (1 odd, 1.56 even)", math.sqrt(m) * float(share), 1.0 if m % 2 else 1.56, info)
    if m % 2 == 1 and not m * share * share < 1:
        fail("Theorem 5 odd: share >= 1/sqrt(m)", info)
    if not m * share * share <= Fr(156, 100) ** 2:
        fail("Theorem 5: share > 1.56/sqrt(m)", info)
    if not m * share * share <= Fr(2893, 1000) ** 2:
        fail("Theorem 1: share > 2.893/sqrt(m)", info)
    if not lemmas:
        return share
    # --- structure
    fn = factor(n)
    live = {}
    for p, a in fn.items():
        live[p] = []
        for i in range(1, a + 1):
            sub = {}
            for b in res:
                sub.setdefault(b % p ** (i - 1), set()).add(b % p ** i)
            if any(len(s) == p for s in sub.values()):
                live[p].append(i)
    fl = []
    for d in divs:
        if d == 1:
            continue
        fd = factor(d)
        g = 1
        for p in fd:
            g *= p
        d0 = d // g
        cells = {}
        for b in res:
            cells.setdefault(b % d0, []).append(b)
        k = len(cells)
        fullcells = {}
        for p in fd:
            fullcells[p] = []
            for cc_, el in cells.items():
                cl = {}
                for b in el:
                    cl[b % (d0 * p)] = cl.get(b % (d0 * p), 0) + mult[b]
                if len(cl) == p:
                    fullcells[p].append(sorted(cl.values()))
        if all(fullcells[p] for p in fd):
            fl.append((d, fd, k, fullcells, cells))
    # T4
    cover = bad[1].copy()
    for (d, fd, k, fullcells, cells) in fl:
        cover |= bad[d]
    if (badall & ~cover).any():
        fail("T4 descent", info)
    union = c(m) if m % 2 == 0 else Fr(0)
    if Fr(cnt(bad[1]), tot) != (c(m) if m % 2 == 0 else 0):
        fail("level 0", info)
    pats = set()
    for (d, fd, k, fullcells, cells) in fl:
        ST["fully live pairs"] += 1
        if len(fd) > 1:
            ST["composite fully live"] += 1
        Pd = Fr(cnt(bad[d]), tot)
        # ranks, T5, T6
        ranks = {}
        for p, a in fd.items():
            if a not in live[p]:
                fail("level v_p(d) not live for a fully live d", (info, d))
            ranks[p] = sum(1 for i in live[p] if i <= a)
        G = max(1 + (ranks[p] - 1) * (p - 1) for p in fd)
        if k < G:
            fail("T5 cells < G", (info, d))
        pat = tuple(sorted(ranks.items()))
        if pat in pats:
            fail("T6 pattern repeated", (info, d))
        pats.add(pat)
        Pmax = max(fd)
        Nstar = G + Pmax - 1
        if Pd > 0 and not (m >= Nstar):
            fail("positive share with N(d*) > m", (info, d))
        lc = CALC.LC(m, Nstar)
        if not Pd <= lc:
            fail("Theorem 2 term (Lemma C with N(d*))", (info, d))
        ratio("P(bad at d) / LC(m,N(d*))", Pd, lc, (info, d))
        if not float(Pd) <= math.sqrt(2 / (math.pi * m)) * math.sqrt(Nstar) * 2.0 ** (-(Nstar - 2)) * (1 + 1e-12):
            fail("Theorem 1 term (Lemma B with N(d*))", (info, d))
        union += lc
        for p in fd:
            N = k + p - 1
            for sizes in fullcells[p]:
                ST["lemmaBC triples"] += 1
                r0, r1 = sizes[0], sizes[1]
                bB = c(-(-m // N)) / 2 ** (N - 2)
                bC1 = c(r1) * c(m - r0 - r1 - 2 * (N - 3)) / 2 ** (N - 3)
                bC2 = CALC.LC(m, N)
                if not Pd <= bB:
                    fail("Lemma B", (info, d, p, sizes))
                if not Pd <= bC1:
                    fail("Lemma C first", (info, d, p, sizes))
                if not bC1 <= bC2:
                    fail("Lemma C second", (info, d, p, sizes))
                if Pd == bC1:
                    ST["lemmaC equal"] += 1
                ratio("Lemma B", Pd, bB, (info, d, p))
                ratio("Lemma C", Pd, bC1, (info, d, p))
        if len(fd) == 1:
            p = Pmax
            N = k + p - 1
            cls = {}
            for b in res:
                cls[b % d] = cls.get(b % d, 0) + mult[b]
            lmax = max(cls.values())
            s = m - lmax
            bF = c(lmax) * c(-(-s // 2) - 2 * (N - 3)) / 2 ** (N - 3)
            ST["lemmaF cases"] += 1
            if not Pd <= bF:
                fail("Lemma F", (info, d))
            if Pd == bF:
                ST["lemmaF equal"] += 1
            ratio("Lemma F", Pd, bF, (info, d))
            if m % 2 == 0:
                Pn = Fr(cnt(bad[d] & ~bad[1]), tot)
                for l in set(cls.values()):
                    ST["lemmaE pairs"] += 1
                    bE = c(l) / 2 ** (k + 2 * p - 5)
                    if not Pn <= bE:
                        fail("Lemma E", (info, d, l))
                    ratio("Lemma E", Pn, bE, (info, d, l))
                    if p == 3 and k == 1:
                        ST["lemmaE' cases"] += 1
                        if not Pn <= Fr(17, 128) * c(l):
                            fail("Lemma E'", (info, d, l))
                        ratio("Lemma E'", Pn, Fr(17, 128) * c(l), (info, d, l))
                if Pn > 0:
                    ST["lemmaE positive"] += 1
                j = ranks[p]
                ppe = CALC.PPE(m, p, j)
                if not Pn <= ppe:
                    fail("PPE term of Theorem 4", (info, d))
                ratio("P(bad at p^i, not at 1) / PPE", Pn, ppe, (info, d))
    if not share <= union:
        fail("union bound of Theorem 2 with the actual fully live d", info)
    b, be = Bm(m)
    if not union <= b:
        fail("actual union above B(m)", info)
    if not share <= b:
        fail("Theorem 2: share > B(m)", info)
    ratio("share / B(m)", share, b, info)
    if m % 2 == 0:
        ST["even multisets"] += 1
        if not share <= be:
            fail("Theorem 4: share > B_E(m)", info)
        ratio("share / B_E(m)", share, be, info)
    # the two results of the first text of last night that Theorem 5 uses
    if n % 3 == 0:
        b3 = np.zeros(len(T), dtype=bool)
        e = 3
        while n % e == 0:
            b3 |= bad[e]
            e *= 3
        if m % 2 == 1 and m >= 3:
            v = Fr(cnt(b3), tot)
            if not v <= c(m - 2) / 2:
                fail("first text Theorem A (odd m, powers of 3)", info)
            if v == c(m - 2) / 2:
                ST["thmA3 equal"] += 1
        if m % 2 == 0:
            v = Fr(cnt(b3 & ~bad[1]), tot)
            if not v <= Fr(309, 8192):
                fail("first text Theorem B (even m, powers of 3, not at 1)", info)
            ratio("first text Theorem B: share / (309/8192)", v, Fr(309, 8192), info)
    return share

def report():
    print("counts:", ST)
    for k_ in sorted(MAXR):
        r, info = MAXR[k_]
        print("  largest ratio  %-55s %.6f  at %s" % (k_, float(r), str(info)[:160]))
    sys.stdout.flush()

def exhaustive(n, m, budget, t0):
    best = Fr(0)
    for comb in itertools.combinations_with_replacement(range(n), m - 1):
        mult = {0: 1}
        for b in comb:
            mult[b] = mult.get(b, 0) + 1
        s = analyse(n, mult)
        if s > best:
            best = s
        if time.time() - t0 > budget:
            print("  (stopped by the time budget inside n = %d, m = %d)" % (n, m))
            return best, False
    return best, True

if __name__ == "__main__":
    mode = sys.argv[1]
    t0 = time.time()
    budget = float(sys.argv[2])
    if mode == "exh":
        jobs = [tuple(int(x) for x in a.split(":")) for a in sys.argv[3:]]
        for n, mlo, mhi in jobs:
            for m in range(mlo, mhi + 1):
                if time.time() - t0 > budget:
                    break
                b, done = exhaustive(n, m, budget, t0)
                print("Z_%d, every multiset of %d elements containing 0: largest bad share %s = %.6f, sqrt(m)*share = %.4f, complete: %s, multisets so far %d, failures %d"
                      % (n, m, b, float(b), math.sqrt(m) * float(b), done, ST["multisets"], ST["failures"]), flush=True)
        report()
    elif mode == "rand":
        seed = int(sys.argv[3])
        rnd = random.Random(seed)
        mods = [int(x) for x in sys.argv[4].split(",")]
        mlo, mhi = int(sys.argv[5]), int(sys.argv[6])
        while time.time() - t0 < budget:
            n = rnd.choice(mods)
            m = rnd.randint(mlo, mhi)
            kind = rnd.randint(0, 5)
            mult = {}
            if kind == 0:      # plain random
                for _ in range(m):
                    b = rnd.randrange(n)
                    mult[b] = mult.get(b, 0) + 1
            elif kind == 1:    # all in pairs
                for _ in range(m // 2):
                    b = rnd.randrange(n)
                    mult[b] = mult.get(b, 0) + 2
            elif kind == 2:    # few residues with multiplicities
                rs = rnd.sample(range(n), rnd.randint(2, 5))
                for _ in range(m):
                    b = rnd.choice(rs)
                    mult[b] = mult.get(b, 0) + 1
            elif kind == 3:    # a heavy element and random others
                mult[0] = m - rnd.randint(2, min(m - 1, 7))
                for _ in range(m - mult[0]):
                    b = rnd.randrange(n)
                    mult[b] = mult.get(b, 0) + 1
            elif kind == 4:    # multiples of n/p^a plus noise: classes of a subgroup chain
                f = factor(n)
                p = rnd.choice(list(f))
                step = n // p ** rnd.randint(1, f[p])
                for _ in range(m):
                    b = (rnd.randrange(n // step) * step + (rnd.randrange(n) if rnd.random() < 0.15 else 0)) % n
                    mult[b] = mult.get(b, 0) + 1
            else:              # pairs and fours on a subgroup
                f = factor(n)
                p = rnd.choice(list(f))
                step = n // p ** rnd.randint(1, f[p])
                left = m
                while left > 0:
                    t = min(left, rnd.choice([2, 2, 4]))
                    b = rnd.randrange(n // step) * step
                    mult[b] = mult.get(b, 0) + t
                    left -= t
            K = 1
            for hb in mult.values():
                K *= hb + 1
            if K > 70000:
                continue
            analyse(n, mult)
        report()
