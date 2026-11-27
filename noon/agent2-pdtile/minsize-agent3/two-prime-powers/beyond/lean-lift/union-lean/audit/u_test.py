# Audit of statement U (card_exists_exists_levelBad_le), by brute force, exact integer arithmetic, every signing.
# csum and levelBad are written word for word after Pnq/EvenTwice.lean:
#   csum pos val eps M r = sum over k of (sg(eps k) . val k if pos k % M = r else 0)
#   levelBad .. 0     : sum over k of sg(eps k) . val k = 0
#   levelBad .. (j+1) : for all r < 2^j, csum (2^(j+1)) r = csum (2^(j+1)) (r + 2^j)
# U: #{eps | exists c, exists j <= K, levelBad pos (val c) eps j} <= 2 * #{eps | exists c, levelBad pos (val c) eps 0}
# A group is a tuple of moduli, 0 standing for Z: (0,) = Z, (2,) = Z/2, (0,0) = Z^2, ...
import sys, random, itertools
from fractions import Fraction

def sg(b):
    return 1 if b else -1

def natmod(x, M):          # Lean: x % 0 = x
    return x if M == 0 else x % M

def gzero(G):
    return tuple(0 for _ in G)

def gred(G, v):
    return tuple((x % q) if q else x for x, q in zip(v, G))

def gadd(G, a, b):
    return gred(G, tuple(x + y for x, y in zip(a, b)))

def gsmul(G, z, a):
    return gred(G, tuple(z * x for x in a))

def csum(G, pos, val, eps, M, r):
    s = gzero(G)
    for k in range(len(pos)):
        s = gadd(G, s, gsmul(G, sg(eps[k]), val[k]) if natmod(pos[k], M) == r else gzero(G))
    return s

def levelBad(G, pos, val, eps, j):
    if j == 0:
        s = gzero(G)
        for k in range(len(pos)):
            s = gadd(G, s, gsmul(G, sg(eps[k]), val[k]))
        return s == gzero(G)
    jj = j - 1
    M = 2 ** (jj + 1)
    for r in range(2 ** jj):
        if csum(G, pos, val, eps, M, r) != csum(G, pos, val, eps, M, r + 2 ** jj):
            return False
    return True

def levelBad_fast(G, pos, val, eps, j):
    # the same thing with the class sums collected once per level
    z = gzero(G)
    if j == 0:
        s = z
        for k in range(len(pos)):
            s = gadd(G, s, gsmul(G, sg(eps[k]), val[k]))
        return s == z
    jj = j - 1
    M = 2 ** (jj + 1)
    d = {}
    for k in range(len(pos)):
        r = pos[k] % M
        d[r] = gadd(G, d.get(r, z), gsmul(G, sg(eps[k]), val[k]))
    H = 2 ** jj
    for r, s in d.items():
        r0 = r if r < H else r - H
        if d.get(r0, z) != d.get(r0 + H, z):
            return False
    return True

def masks(G, pos, vals, Kmax, slow=False):
    """for each signing, for each system c, the set of bad levels 0..Kmax as a bit mask"""
    m = len(pos)
    out = []
    lb = levelBad if slow else levelBad_fast
    for eps in itertools.product((False, True), repeat=m):
        row = []
        for val in vals:
            b = 0
            for j in range(Kmax + 1):
                if lb(G, pos, val, eps, j):
                    b |= 1 << j
            row.append(b)
        out.append(row)
    return out

def counts(ms, K):
    """the two cardinalities of U, and those of the false variants, from the masks"""
    low = (1 << (K + 1)) - 1
    left = sum(1 for row in ms if any(b & low for b in row))
    right = sum(1 for row in ms if any(b & 1 for b in row))
    left_all = sum(1 for row in ms if all(b & low for b in row))
    right_all = sum(1 for row in ms if all(b & 1 for b in row))
    return left, right, left_all, right_all

GROUPS = {'Z': (0,), 'Z/2': (2,), 'Z/3': (3,), 'Z/4': (4,), 'Z^2': (0, 0), 'Z/2xZ/4': (2, 4)}

def rand_val(G, rng, style):
    v = []
    for q in G:
        if q:
            v.append(rng.randrange(q))
        else:
            v.append(rng.choice((-1, 1)) if style == 1 else rng.randint(-2, 2) if style == 0 else rng.choice((0, 0, 1, -1, 2)))
    return tuple(v)

class Tally:
    def __init__(self):
        self.fam = 0; self.chk = 0; self.fail = 0; self.eq2 = 0; self.right0 = 0; self.nontriv = 0
        self.beyondT = 0; self.maxratio = Fraction(0); self.signings = 0
        self.f32 = 0; self.fRall = 0; self.fLall = {}; self.fBoth = 0
        self.first = {}
    def add(self, G, pos, vals, ms, Kmax, per_system_right):
        self.fam += 1
        self.signings += len(ms)
        for K in range(Kmax + 1):
            L, R, La, Ra = counts(ms, K)
            self.chk += 1
            if L > 2 * R:
                self.fail += 1
                self.first.setdefault('U FAILS', (G, pos, vals, K, L, R))
            if R == 0:
                self.right0 += 1
            else:
                self.maxratio = max(self.maxratio, Fraction(L, R))
                if L == 2 * R:
                    self.eq2 += 1
                    self.first.setdefault('factor 2 attained', (G, pos, vals, K, L, R))
            if L > R:
                self.nontriv += 1
            if L > 0 and 2 * R < L + 0 and False:
                pass
            if len(vals) >= 2 and 2 * R < 2 * sum(per_system_right) and L > R:
                self.beyondT += 1
            if 2 * L > 3 * R:
                self.f32 += 1
                self.first.setdefault('variant 3/2 fails', (G, pos, vals, K, L, R))
            if L > 2 * Ra:
                self.fRall += 1
                self.first.setdefault('variant "all c" on the right fails', (G, pos, vals, K, L, Ra))
            if La > 2 * R:
                self.fLall[len(vals)] = self.fLall.get(len(vals), 0) + 1
                self.first.setdefault('variant "all c" on the left fails', (G, pos, vals, K, La, R))
            if La > 2 * Ra:
                self.fBoth += 1
                self.first.setdefault('variant "all c" on both sides fails', (G, pos, vals, K, La, Ra))
    def report(self, title):
        print(title)
        print(f"  families {self.fam}, signings {self.signings}, checks (family, K) {self.chk}")
        print(f"  U fails: {self.fail}")
        print(f"  right side 0: {self.right0}; left > right (some level >= 1 adds a signing): {self.nontriv}")
        print(f"  largest left/right: {self.maxratio}; left = 2*right > 0: {self.eq2}")
        print(f"  checks with >= 2 systems, left > right, and 2*right below the sum over c of 2*right_c: {self.beyondT}")
        print(f"  false variants: 2*left <= 3*right fails {self.f32}; 'all c' on the right only fails {self.fRall}; "
              f"'all c' on the left only fails by number of systems {dict(sorted(self.fLall.items()))}; "
              f"'all c' on both sides fails {self.fBoth}")
        for kname, v in self.first.items():
            print(f"  first case, {kname}: group {v[0]}, pos {v[1]}, values {v[2]}, K {v[3]}, counts {v[4]} and {v[5]}")
        sys.stdout.flush()

def per_right(ms, nsys):
    return [sum(1 for row in ms if row[c] & 1) for c in range(nsys)]

def selftest(rng):
    # the fast levelBad against the word-for-word one
    n = 0
    for _ in range(400):
        gname = rng.choice(list(GROUPS)); G = GROUPS[gname]
        m = rng.randint(0, 5)
        pos = tuple(rng.randrange(rng.choice((2, 4, 8, 16, 1000))) for _ in range(m))
        vals = tuple(tuple(rand_val(G, rng, rng.randrange(3)) for _ in range(m)) for _ in range(rng.randint(0, 3)))
        Kmax = 5
        a = masks(G, pos, vals, Kmax, slow=True)
        b = masks(G, pos, vals, Kmax, slow=False)
        assert a == b, (G, pos, vals)
        n += len(a) * len(vals) * (Kmax + 1)
    print(f"selftest: fast levelBad = word-for-word levelBad on {n} (signing, system, level) triples")

def exhaustive():
    # every family: m elements, positions in 0..3, two systems of values in Z/2 or Z/3 (m <= 3), levels up to 4
    for gname, mmax in (('Z/2', 4), ('Z/3', 3)):
        G = GROUPS[gname]; q = G[0]
        t = Tally()
        for m in range(0, mmax + 1):
            for pos in itertools.product(range(4), repeat=m):
                allv = list(itertools.product(range(q), repeat=m))
                for i, v1 in enumerate(allv):
                    for v2 in allv[i:]:
                        vals = (tuple((x,) for x in v1), tuple((x,) for x in v2))
                        ms = masks(G, pos, vals, 4)
                        t.add(gname, pos, vals, ms, 4, per_right(ms, 2))
        t.report(f"EXHAUSTIVE {gname}: m = 0..{mmax}, positions in 0..3, two systems (unordered pairs), K = 0..4")

def exhaustive2():
    # every family: values from a small set, positions in 0..3, two or three systems (unordered), levels up to 3
    for gname, pool, mmax, nsys in (('Z', [(-1,), (0,), (1,)], 3, 2), ('Z/4', [(0,), (1,), (2,), (3,)], 3, 2),
                                    ('Z^2', [(a, b) for a in (-1, 0, 1) for b in (-1, 0, 1)], 2, 2),
                                    ('Z', [(-1,), (0,), (1,), (2,)], 2, 3), ('Z/3', [(0,), (1,), (2,)], 2, 4)):
        G = GROUPS[gname]
        t = Tally()
        for m in range(0, mmax + 1):
            allv = list(itertools.product(pool, repeat=m))
            for pos in itertools.product(range(4), repeat=m):
                for vals in itertools.combinations_with_replacement(allv, nsys):
                    ms = masks(G, pos, vals, 3)
                    t.add(gname, pos, vals, ms, 3, per_right(ms, nsys))
        t.report(f"EXHAUSTIVE {gname}, values from {pool}: m = 0..{mmax}, positions in 0..3, {nsys} systems (unordered), K = 0..3")

def randomrun(seed, N):
    rng = random.Random(seed)
    selftest(rng)
    tall = {}
    for it in range(N):
        gname = rng.choice(list(GROUPS)); G = GROUPS[gname]
        nsys = rng.choice((0, 1, 2, 2, 2, 3, 3, 4))
        m = rng.randint(0, 8)
        prange = rng.choice((1, 2, 4, 4, 8, 8, 16, 10 ** 6))
        pos = tuple(rng.randrange(prange) for _ in range(m))
        style = rng.randrange(3)
        vals = []
        for c in range(nsys):
            kind = rng.randrange(4)
            if kind == 0 or not vals:
                v = tuple(rand_val(G, rng, style) for _ in range(m))
            elif kind == 1:      # a system close to an earlier one (so that the level-0 events overlap)
                w = list(rng.choice(vals))
                if m:
                    i = rng.randrange(m); w[i] = rand_val(G, rng, style)
                v = tuple(w)
            elif kind == 2:      # a multiple of an earlier one
                z = rng.choice((-1, 2, 3)); v = tuple(gsmul(G, z, x) for x in rng.choice(vals))
            else:                # an earlier one with one value negated
                w = list(rng.choice(vals))
                if m:
                    i = rng.randrange(m); w[i] = gsmul(G, -1, w[i])
                v = tuple(w)
            vals.append(v)
        vals = tuple(vals)
        Kmax = rng.choice((3, 5, 7))
        ms = masks(G, pos, vals, Kmax)
        key = (gname, nsys)
        for kk in (key, ('all', 'all'), (gname, 'all'), ('all', nsys)):
            tall.setdefault(kk, Tally()).add(gname, pos, vals, ms, Kmax, per_right(ms, nsys))
    tall[('all', 'all')].report(f"RANDOM seed {seed}, {N} families: m = 0..8, 0..4 systems, positions below 1, 2, 4, 8, 16 or 10^6, K up to 3, 5 or 7")
    for g in GROUPS:
        t = tall.get((g, 'all'))
        if t:
            print(f"  group {g}: families {t.fam}, checks {t.chk}, U fails {t.fail}, left = 2*right > 0: {t.eq2}, largest ratio {t.maxratio}")
    for c in range(5):
        t = tall.get(('all', c))
        if t:
            print(f"  {c} systems: families {t.fam}, checks {t.chk}, U fails {t.fail}, left = 2*right > 0: {t.eq2}, largest ratio {t.maxratio}, "
                  f"'all c' on the left fails {sum(t.fLall.values())}, 'all c' on the right fails {t.fRall}")

def positions_per_system(seed, N):
    # a statement that is NOT U: each system with its own positions.  Is "at most twice" then false?
    rng = random.Random(seed)
    bad = 0; first = None; chk = 0
    for it in range(N):
        gname = rng.choice(list(GROUPS)); G = GROUPS[gname]
        m = rng.randint(1, 6)
        nsys = 2
        poss = [tuple(rng.randrange(4) for _ in range(m)) for _ in range(nsys)]
        vals = [tuple(rand_val(G, rng, 1) for _ in range(m)) for _ in range(nsys)]
        Kmax = 3
        mss = [masks(G, poss[c], (vals[c],), Kmax) for c in range(nsys)]
        for K in range(Kmax + 1):
            low = (1 << (K + 1)) - 1
            L = sum(1 for i in range(2 ** m) if any(mss[c][i][0] & low for c in range(nsys)))
            R = sum(1 for i in range(2 ** m) if any(mss[c][i][0] & 1 for c in range(nsys)))
            chk += 1
            if L > 2 * R:
                bad += 1
                if first is None:
                    first = (gname, poss, vals, K, L, R)
    print(f"NOT U (each system its own positions), seed {seed}: checks {chk}, 'at most twice' fails {bad}; first: {first}")

if __name__ == '__main__':
    what = sys.argv[1]
    if what == 'exh':
        exhaustive()
    elif what == 'exh2':
        exhaustive2()
    elif what == 'rand':
        randomrun(int(sys.argv[2]), int(sys.argv[3]))
    elif what == 'ownpos':
        positions_per_system(int(sys.argv[2]), int(sys.argv[3]))
