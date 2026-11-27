"""Referee's test of Theorem T of theorem-twice.md, written from the statement.

A valued family: elements with a position in Z_(2^k) and a value in an abelian group V.
V is given by a tuple of moduli, one for each coordinate (0 means Z).
Level 0 bad: signed sum of all values is 0.
Level j bad (1 <= j <= k): every class modulo 2^(j-1) has equal signed sums in its two halves modulo 2^j.
Q = share of signings with some level 0..k bad, z = share with level 0 bad.  Claim: Q <= 2 z.

Two implementations:
  literal(): pure Python, classes built as lists of elements, half-sums compared as the statement says.
  batch():   numpy, all signings of many families at once; cross-checked against literal() on samples.

For every family the program also records (referee's additions, see the report):
  F_d  = the signings for which every class modulo 2^d has signed sum 0   (F_0 = level 0 bad)
  (i)  #(level j bad) == #F_(j-1)
  (ii) #(level j bad and level 0 bad) >= #F_j
  (iii) #(some level bad) <= 2 #(level 0 bad) - #F_k         (sharper than Theorem T)
and two deliberately FALSE statements, to see that the test can see a failure:
  (x)  Q <= 1.5 z
  (y)  Theorem T with "every class balanced" replaced by "some class balanced"
"""
import itertools, random, sys, time
import numpy as np

# ---------------------------------------------------------------- literal reference

def vadd(a, b, mods):
    return tuple(((x + y) % m) if m else (x + y) for x, y, m in zip(a, b, mods))

def vscale(s, a, mods):
    return tuple(((s * x) % m) if m else (s * x) for x, m in zip(a, mods))

def literal(k, fam, mods, some_instead_of_every=False):
    """fam: list of (position, value-tuple).  Returns (nQ, nz, 2^m) by going through all signings."""
    m = len(fam)
    zero = tuple(0 for _ in mods)
    def sigma(idx, signs):
        s = zero
        for i in idx:
            s = vadd(s, vscale(signs[i], fam[i][1], mods), mods)
        return s
    nQ = nz = 0
    for signs in itertools.product((1, -1), repeat=m):
        bad0 = (sigma(range(m), signs) == zero)          # empty family: bad
        anybad = bad0
        for j in range(1, k + 1):
            classes = {}
            for i, (u, v) in enumerate(fam):
                classes.setdefault(u % (1 << (j - 1)), []).append(i)
            flags = []
            for res, idx in classes.items():
                h = [i for i in idx if fam[i][0] % (1 << j) == res]
                h2 = [i for i in idx if fam[i][0] % (1 << j) == res + (1 << (j - 1))]
                assert len(h) + len(h2) == len(idx)
                flags.append(sigma(h, signs) == sigma(h2, signs))
            badj = any(flags) if some_instead_of_every else all(flags)
            anybad = anybad or badj
        nQ += anybad
        nz += bad0
    return nQ, nz, 1 << m

# ---------------------------------------------------------------- numpy batch

_signs = {}
def signs_matrix(m):
    if m not in _signs:
        _signs[m] = np.array(list(itertools.product((1, -1), repeat=m)), dtype=np.float64).reshape(1 << m, m)
    return _signs[m]

def batch(k, U, Vv, mods, some_instead_of_every=False):
    """U: (F, m) positions; Vv: (F, m, dim) values.  Returns dict of integer arrays of length F."""
    F, m = U.shape
    P = 1 << k
    dim = Vv.shape[2]
    S = 1 << m
    W = np.zeros((F, m, P, dim), dtype=np.float64)
    fi, ii = np.indices((F, m))
    W[fi, ii, U] = Vv
    PS = np.rint(np.matmul(signs_matrix(m)[None], W.reshape(F, m, P * dim))).astype(np.int64).reshape(F, S, P, dim)
    def iszero(A):               # A: (..., dim) -> boolean (...)
        ok = np.ones(A.shape[:-1], dtype=bool)
        for c, mod in enumerate(mods):
            ok &= ((A[..., c] % mod) == 0) if mod else (A[..., c] == 0)
        return ok
    def classsums(d):            # (F, S, 2^d, dim): signed sum of each residue class modulo 2^d
        return PS.reshape(F, S, P >> d, 1 << d, dim).sum(axis=2)
    Fd = [iszero(classsums(d)).all(axis=2) for d in range(k + 1)]       # (F, S)
    E = [Fd[0]]
    for j in range(1, k + 1):
        C = classsums(j)
        half = 1 << (j - 1)
        bal = iszero(C[:, :, :half] - C[:, :, half:])                  # (F, S, 2^(j-1)): class by class
        if some_instead_of_every:
            # only occupied classes count
            occ = np.zeros((F, half), dtype=bool)
            for f in range(F):
                occ[f, U[f] % half] = True
            E.append((bal & occ[:, None, :]).any(axis=2))
        else:
            E.append(bal.all(axis=2))
    anybad = np.zeros((F, S), dtype=bool)
    for e in E:
        anybad |= e
    out = {'nQ': anybad.sum(axis=1), 'nz': E[0].sum(axis=1), 'nFk': Fd[k].sum(axis=1)}
    out['i_ok'] = np.ones(F, dtype=bool)
    out['ii_ok'] = np.ones(F, dtype=bool)
    for j in range(1, k + 1):
        out['i_ok'] &= (E[j].sum(axis=1) == Fd[j - 1].sum(axis=1))
        out['ii_ok'] &= ((E[j] & E[0]).sum(axis=1) >= Fd[j].sum(axis=1))
    return out

# ---------------------------------------------------------------- driver

class Tally:
    def __init__(self, name):
        self.name = name
        self.n = 0; self.failT = 0; self.failSharp = 0; self.fail_i = 0; self.fail_ii = 0
        self.fail15 = 0; self.eq = 0; self.zpos = 0; self.maxratio = (0, 1); self.firstfail = None
        self.sharp_eq = 0
    def add(self, k, U, Vv, mods, r):
        nQ, nz, nFk = r['nQ'], r['nz'], r['nFk']
        self.n += len(nQ)
        bad = nQ > 2 * nz
        if bad.any() and self.firstfail is None:
            f = int(np.argmax(bad))
            self.firstfail = (k, U[f].tolist(), Vv[f].tolist(), int(nQ[f]), int(nz[f]))
        self.failT += int(bad.sum())
        self.failSharp += int((nQ > 2 * nz - nFk).sum())
        self.sharp_eq += int((nQ == 2 * nz - nFk).sum())
        self.fail_i += int((~r['i_ok']).sum())
        self.fail_ii += int((~r['ii_ok']).sum())
        self.fail15 += int((2 * nQ > 3 * nz).sum())
        pos = nz > 0
        self.zpos += int(pos.sum())
        self.eq += int(((nQ == 2 * nz) & pos).sum())
        if pos.any():
            ratio = nQ[pos] / nz[pos]
            a = int(np.argmax(ratio))
            q, zz = int(nQ[pos][a]), int(nz[pos][a])
            if q * self.maxratio[1] > self.maxratio[0] * zz:
                self.maxratio = (q, zz)
    def line(self):
        q, zz = self.maxratio
        return (f"{self.name}: families {self.n}; Q>2z: {self.failT}; Q>2z-P(F_k): {self.failSharp} "
                f"(equal: {self.sharp_eq}); (i) fails: {self.fail_i}; (ii) fails: {self.fail_ii}; "
                f"z>0 in {self.zpos}, Q=2z>0 in {self.eq}, largest Q/z = {q}/{zz}; "
                f"[false statement Q<=1.5z fails in {self.fail15}]"
                + (f"; FIRST FAILURE OF T: {self.firstfail}" if self.firstfail else ""))

def run_exhaustive(name, k, values, mods, mmax, budget_s, crosscheck=40, seed=1):
    """All multisets of at most mmax elements of {positions} x {values}."""
    rng = random.Random(seed)
    types = [(u, v) for u in range(1 << k) for v in values]
    tal = Tally(name)
    t0 = time.time()
    done_m = 0
    xc = 0
    for m in range(0, mmax + 1):
        if m == 0:
            # the empty family, by the literal routine only
            nQ, nz, tot = literal(k, [], mods)
            assert (nQ, nz, tot) == (1, 1, 1)
            done_m = 0
            continue
        chunk = max(1, min(4000, (1 << 21) // ((1 << m) * (1 << k) * len(mods))))
        it = itertools.combinations_with_replacement(range(len(types)), m)
        while True:
            block = list(itertools.islice(it, chunk))
            if not block:
                break
            idx = np.array(block, dtype=np.int64)
            U = np.array([t[0] for t in types], dtype=np.int64)[idx]
            Vv = np.array([t[1] for t in types], dtype=np.int64)[idx]
            r = batch(k, U, Vv, mods)
            tal.add(k, U, Vv, mods, r)
            # cross-check a few families of this block against the literal routine
            if m <= 7:
                for f in rng.sample(range(len(block)), min(2, len(block))):
                    if xc < crosscheck * (m + 1):
                        fam = [types[t] for t in block[f]]
                        assert literal(k, fam, mods)[:2] == (int(r['nQ'][f]), int(r['nz'][f])), fam
                        xc += 1
            if time.time() - t0 > budget_s:
                print(f"{name}: STOPPED by time budget inside m = {m}; complete up to m = {done_m}", flush=True)
                print(tal.line() + f"; literal cross-checks {xc}", flush=True)
                return tal
        done_m = m
    print(tal.line() + f"; complete for m <= {done_m}; literal cross-checks {xc}; {time.time()-t0:.0f} s", flush=True)
    return tal

def run_random(name, k, values, mods, mlo, mhi, count, seed, structured=True, some=False):
    rng = random.Random(seed)
    tal = Tally(name)
    t0 = time.time()
    P = 1 << k
    xc = 0
    for m in range(mlo, mhi + 1):
        fams = []
        for _ in range(count):
            mode = rng.randrange(5) if structured else 0
            fam = []
            if mode == 0:        # free
                fam = [(rng.randrange(P), rng.choice(values)) for _ in range(m)]
            elif mode == 1:      # few positions
                pos = [rng.randrange(P) for _ in range(rng.randint(1, 3))]
                fam = [(rng.choice(pos), rng.choice(values)) for _ in range(m)]
            elif mode == 2:      # pairs v, +-v at positions that differ by a power of 2
                while len(fam) < m:
                    u = rng.randrange(P); v = rng.choice(values)
                    fam.append((u, v))
                    if len(fam) < m:
                        w = v if rng.random() < .5 else tuple(-x for x in v)
                        fam.append(((u + (1 << rng.randrange(k))) % P if k else u, w))
            elif mode == 3:      # distinct positions when possible, one value up to sign
                v = rng.choice(values)
                pos = rng.sample(range(P), min(m, P))
                fam = [(pos[i % len(pos)], v if rng.random() < .5 else tuple(-x for x in v)) for i in range(m)]
            else:                # all in one class modulo a power of 2
                d = rng.randint(0, k); base = rng.randrange(P)
                fam = [((base + (rng.randrange(P) << d)) % P, rng.choice(values)) for _ in range(m)]
            fams.append(fam)
        U = np.array([[e[0] for e in fam] for fam in fams], dtype=np.int64)
        Vv = np.array([[e[1] for e in fam] for fam in fams], dtype=np.int64)
        chunk = max(1, (1 << 21) // ((1 << m) * P * len(mods)))
        for a in range(0, count, chunk):
            r = batch(k, U[a:a + chunk], Vv[a:a + chunk], mods, some_instead_of_every=some)
            tal.add(k, U[a:a + chunk], Vv[a:a + chunk], mods, r)
            if m <= 8 and xc < 60:
                f = 0
                assert literal(k, fams[a + f], mods, some_instead_of_every=some)[:2] == (int(r['nQ'][f]), int(r['nz'][f]))
                xc += 1
    print(tal.line() + f"; m = {mlo}..{mhi}, {count} each; literal cross-checks {xc}; {time.time()-t0:.0f} s", flush=True)
    return tal

def vals(mods, rng_list):
    return [tuple(v) for v in rng_list]

if __name__ == '__main__':
    what = sys.argv[1]
    B = float(sys.argv[2]) if len(sys.argv) > 2 else 60.0
    Z3 = [(1,), (2,)]
    Z5 = [(1,), (2,), (3,), (4,)]
    Z5h = [(1,), (2,)]
    Z9 = [(i,) for i in range(1, 9)]
    Z9h = [(1,), (2,), (3,), (4,)]
    Z33 = [(a, b) for a in range(3) for b in range(3) if (a, b) != (0, 0)]
    Z33h = [(1, 0), (0, 1), (1, 1), (1, 2)]
    Zs = [(1,), (-1,), (2,), (-2,), (3,)]
    Zh = [(1,), (2,), (3,)]
    ZZ = [(1, 0), (0, 1), (1, 1), (1, -1), (-1, 0), (0, -1), (2, 1)]
    ZZh = [(1, 0), (0, 1), (1, 1), (1, -1)]
    if what == 'exh-a':      # every value of the group (pairs v, -v included), all positions
        run_exhaustive('Z_2 x Z/3 all values', 1, Z3, (3,), 12, B)
        run_exhaustive('Z_4 x Z/3 all values', 2, Z3, (3,), 9, B)
        run_exhaustive('Z_8 x Z/3 all values', 3, Z3, (3,), 7, B)
        run_exhaustive('Z_2 x Z/5 all values', 1, Z5, (5,), 9, B)
        run_exhaustive('Z_4 x Z/5 all values', 2, Z5, (5,), 6, B)
        run_exhaustive('Z_8 x Z/5 all values', 3, Z5, (5,), 5, B)
    elif what == 'exh-b':
        run_exhaustive('Z_2 x Z/9 all values', 1, Z9, (9,), 7, B)
        run_exhaustive('Z_4 x Z/9 all values', 2, Z9, (9,), 5, B)
        run_exhaustive('Z_8 x Z/9 all values', 3, Z9, (9,), 4, B)
        run_exhaustive('Z_2 x (Z/3)^2 all values', 1, Z33, (3, 3), 7, B)
        run_exhaustive('Z_4 x (Z/3)^2 all values', 2, Z33, (3, 3), 5, B)
        run_exhaustive('Z_8 x (Z/3)^2 all values', 3, Z33, (3, 3), 4, B)
    elif what == 'exh-c':
        run_exhaustive('Z_2 x Z, values 1,-1,2,-2,3', 1, Zs, (0,), 8, B)
        run_exhaustive('Z_4 x Z, values 1,-1,2,-2,3', 2, Zs, (0,), 6, B)
        run_exhaustive('Z_8 x Z, values 1,-1,2,-2,3', 3, Zs, (0,), 5, B)
        run_exhaustive('Z_2 x Z^2, 7 values', 1, ZZ, (0, 0), 7, B)
        run_exhaustive('Z_4 x Z^2, 7 values', 2, ZZ, (0, 0), 5, B)
        run_exhaustive('Z_8 x Z^2, 7 values', 3, ZZ, (0, 0), 4, B)
    elif what == 'exh-d':    # values up to sign only (negating a value is renaming a sign): more elements
        run_exhaustive('Z_8 x Z/3, value 1 only', 3, [(1,)], (3,), 11, B)
        run_exhaustive('Z_4 x Z/3, value 1 only', 2, [(1,)], (3,), 14, B)
        run_exhaustive('Z_8 x Z/5, values 1,2', 3, Z5h, (5,), 7, B)
        run_exhaustive('Z_8 x Z/9, values 1,2,3,4', 3, Z9h, (9,), 5, B)
    elif what == 'exh-e':
        run_exhaustive('Z_8 x (Z/3)^2, 4 values up to sign', 3, Z33h, (3, 3), 5, B)
        run_exhaustive('Z_8 x Z, values 1,2,3', 3, Zh, (0,), 6, B)
        run_exhaustive('Z_8 x Z^2, 4 values up to sign', 3, ZZh, (0, 0), 5, B)
        run_exhaustive('Z_16 x Z/3, value 1 only', 4, [(1,)], (3,), 7, B)
        run_exhaustive('Z_16 x Z, value 1 only', 4, [(1,)], (0,), 7, B)
    elif what == 'hyp':      # hypotheses of Theorem T broken
        run_exhaustive('BROKEN Z_2 x Z/2 (2-torsion)', 1, [(1,)], (2,), 12, B)
        run_exhaustive('BROKEN Z_4 x Z/2', 2, [(1,)], (2,), 10, B)
        run_exhaustive('BROKEN Z_8 x Z/2', 3, [(1,)], (2,), 9, B)
        run_exhaustive('BROKEN Z_4 x Z/4 values 1,2,3', 2, [(1,), (2,), (3,)], (4,), 7, B)
        run_exhaustive('BROKEN Z_8 x Z/4 values 1,2,3', 3, [(1,), (2,), (3,)], (4,), 5, B)
        run_exhaustive('BROKEN Z_4 x Z/6 values 1..5', 2, [(i,) for i in range(1, 6)], (6,), 6, B)
        run_exhaustive('BROKEN Z_8 x Z/6 values 1..5', 3, [(i,) for i in range(1, 6)], (6,), 4, B)
        run_exhaustive('BROKEN Z_4 x Z/3 with the value 0', 2, [(0,), (1,), (2,)], (3,), 8, B)
        run_exhaustive('BROKEN Z_8 x Z/3 with the value 0', 3, [(0,), (1,), (2,)], (3,), 6, B)
        run_exhaustive('BROKEN Z_8 x Z with the value 0', 3, [(0,), (1,), (2,)], (0,), 6, B)
        run_exhaustive('BROKEN Z_8 x Z/2 x Z/2 with the value 0', 3, [(0, 0), (1, 0), (0, 1), (1, 1)], (2, 2), 5, B)
        run_exhaustive('BROKEN Z_8 x Z/4 x Z/6 mixed', 3, [(0, 3), (2, 0), (1, 1), (2, 3), (3, 2)], (4, 6), 5, B)
    elif what == 'rand':
        for k in (3, 4, 5):
            run_random(f'random Z_{1<<k} x Z/3', k, Z3, (3,), 2, 12, 400, 11 + k)
            run_random(f'random Z_{1<<k} x Z/5', k, Z5, (5,), 2, 12, 400, 21 + k)
            run_random(f'random Z_{1<<k} x Z/9', k, Z9, (9,), 2, 12, 400, 31 + k)
            run_random(f'random Z_{1<<k} x (Z/3)^2', k, Z33, (3, 3), 2, 12, 300, 41 + k)
            run_random(f'random Z_{1<<k} x Z', k, Zs, (0,), 2, 12, 400, 51 + k)
            run_random(f'random Z_{1<<k} x Z^2', k, ZZ, (0, 0), 2, 12, 300, 61 + k)
            run_random(f'random BROKEN Z_{1<<k} x Z/2', k, [(1,)], (2,), 2, 12, 300, 71 + k)
            run_random(f'random BROKEN Z_{1<<k} x Z/4', k, [(1,), (2,), (3,)], (4,), 2, 12, 300, 81 + k)
            run_random(f'random BROKEN Z_{1<<k} x Z/6', k, [(i,) for i in range(1, 6)], (6,), 2, 12, 300, 91 + k)
            run_random(f'random BROKEN Z_{1<<k} x Z with 0', k, [(0,), (1,), (-1,), (2,)], (0,), 2, 12, 300, 101 + k)
    elif what == 'false':    # a false variant: "some class balanced" in place of "every class balanced"
        for k in (2, 3):
            run_random(f'FALSE VARIANT (some class) Z_{1<<k} x Z/3', k, Z3, (3,), 2, 8, 300, 5 + k, some=True)
            run_random(f'FALSE VARIANT (some class) Z_{1<<k} x Z', k, Zs, (0,), 2, 8, 300, 7 + k, some=True)
