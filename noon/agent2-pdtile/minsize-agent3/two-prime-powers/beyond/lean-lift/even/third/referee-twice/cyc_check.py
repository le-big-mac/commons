"""Referee's exact test of Corollaries 2 and 3 of theorem-twice.md (and of what they take from even-result-2.md).

Everything is computed from remainders modulo cyclotomic polynomials with integer coefficients:
  bad at d    : the remainder of S(X) = sum eps_b X^b modulo Phi_d is 0
  3-bad at d  : every coefficient of that remainder is divisible by 3        (d | n_3, n = 3^a n_3)
  good        : bad at no d | n;   3-good : 3-bad at no d | n_3.
By the symmetry eps -> -eps only the signings with sign + on the first element are gone through
(shares are the same).  Multisets are taken with 0 as first element (translation multiplies S by a unit).

Checked for every multiset:
  (2)   for every e'' | n'' : #(3-bad at 2^j e'' for some j <= k) <= 2 #(3-bad at e'')
  (2s)  the same with  - #(3-bad at 2^j e'' for every j <= k)  on the right (referee's sharper form)
  (C2)  for every odd e | n : #(bad at 2^j e for some j <= k) <= 2 #(bad at e), and the sharper form
  (M)   every 3-good signing is good                                   (Lemma M)
  (E)   m >= 3: there is a good signing; least share of good and of 3-good signings for each m
  (bd)  share of 3-good signings >= 1/2 (m = 3), 1/4 (m = 4), p_(m-1) - 0.2383 (m >= 5)
"""
import itertools, math, random, sys, time
from fractions import Fraction
import numpy as np

def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]

_cyc = {}
def cyclo(n):
    """coefficients of Phi_n, lowest first, by exact division of X^n - 1"""
    if n in _cyc:
        return _cyc[n]
    num = [-1] + [0] * (n - 1) + [1]
    for d in divisors(n):
        if d < n:
            den = cyclo(d)
            q = [0] * (len(num) - len(den) + 1)
            num = num[:]
            for i in range(len(q) - 1, -1, -1):
                c = num[i + len(den) - 1]            # den is monic
                q[i] = c
                if c:
                    for t, dc in enumerate(den):
                        num[i + t] -= c * dc
            assert not any(num), (n, d)
            num = q
    _cyc[n] = num
    return num

def pow_table(d, N):
    """row b = coefficients of X^b modulo Phi_d, b = 0..N-1 (exact integers)"""
    phi = cyclo(d)
    deg = len(phi) - 1
    r = [1] + [0] * (deg - 1)
    rows = []
    for b in range(N):
        rows.append(r)
        top = r[-1]
        r = [0] + r[:-1]
        if top:
            r = [r[i] - top * phi[i] for i in range(deg)]
    A = np.array(rows, dtype=np.int64)
    assert np.abs(A).max() < 1 << 20
    # independent check of the table: evaluate at a complex primitive d-th root
    zeta = np.exp(2j * np.pi / d)
    val = A @ (zeta ** np.arange(deg))
    assert np.allclose(val, zeta ** np.arange(N), atol=1e-7), d
    # and Phi_d(zeta) = 0, degree = Euler phi
    assert abs(sum(c * zeta ** i for i, c in enumerate(phi))) < 1e-7
    assert deg == sum(1 for t in range(1, d + 1) if math.gcd(t, d) == 1)
    return A.astype(np.float64)

_sg = {}
def half_signs(m):
    if m not in _sg:
        _sg[m] = np.array([(1,) + s for s in itertools.product((1, -1), repeat=m - 1)], dtype=np.float64)
    return _sg[m]

class Ctx:
    def __init__(self, N):
        self.N = N
        self.k = 0
        while N % (2 ** (self.k + 1)) == 0:
            self.k += 1
        self.a = 0
        while N % (3 ** (self.a + 1)) == 0:
            self.a += 1
        self.n3 = N // 3 ** self.a
        self.nodd = N // 2 ** self.k                 # n'
        self.n2 = self.n3 // 2 ** self.k             # n'' , prime to 6
        self.tab = {d: pow_table(d, N) for d in divisors(N)}

    def flags(self, B):
        """B: (F, m) integer array.  Returns dicts d -> boolean (F, S): bad at d (all d | N), 3-bad at d (d | n_3)."""
        Sg = half_signs(B.shape[1])
        bad, bad3 = {}, {}
        for d, T in self.tab.items():
            R = np.rint(np.matmul(Sg[None], T[B])).astype(np.int64)
            bad[d] = (R == 0).all(axis=2)
            if self.n3 % d == 0:
                bad3[d] = (R % 3 == 0).all(axis=2)
        return bad, bad3

W2 = 0.2383
def p_r(r):
    return Fraction(1, 3) + Fraction(2, 3) * Fraction(-1, 2) ** r
def stated_bound(m):
    if m == 3: return Fraction(1, 2)
    if m == 4: return Fraction(1, 4)
    return p_r(m - 1) - Fraction(2383, 10000)

class Tally:
    def __init__(self, ctx, name):
        self.ctx, self.name = ctx, name
        self.n = {}
        self.fail2 = self.fail2s = self.failC2 = self.failC2s = self.failM = self.failE = self.failbd = 0
        self.eq2 = 0; self.tests2 = 0; self.testsC2 = 0; self.eqC2 = 0
        self.min3good = {}; self.mingood = {}
        self.first = None
    def add(self, B):
        ctx = self.ctx
        F, m = B.shape
        S = 1 << (m - 1)
        bad, bad3 = ctx.flags(B)
        self.n[m] = self.n.get(m, 0) + F
        # (2), (2s)
        for e in divisors(ctx.n2):
            some = np.zeros((F, S), dtype=bool); every = np.ones((F, S), dtype=bool)
            for j in range(ctx.k + 1):
                some |= bad3[2 ** j * e]; every &= bad3[2 ** j * e]
            a, z, f = some.sum(axis=1), bad3[e].sum(axis=1), every.sum(axis=1)
            self.tests2 += F
            v = a > 2 * z
            if v.any() and self.first is None:
                self.first = ('(2)', e, B[int(np.argmax(v))].tolist())
            self.fail2 += int(v.sum()); self.fail2s += int((a > 2 * z - f).sum())
            self.eq2 += int(((a == 2 * z) & (z > 0)).sum())
        # (C2)
        for e in divisors(ctx.nodd):
            some = np.zeros((F, S), dtype=bool); every = np.ones((F, S), dtype=bool)
            for j in range(ctx.k + 1):
                some |= bad[2 ** j * e]; every &= bad[2 ** j * e]
            a, z, f = some.sum(axis=1), bad[e].sum(axis=1), every.sum(axis=1)
            self.testsC2 += F
            v = a > 2 * z
            if v.any() and self.first is None:
                self.first = ('(C2)', e, B[int(np.argmax(v))].tolist())
            self.failC2 += int(v.sum()); self.failC2s += int((a > 2 * z - f).sum())
            self.eqC2 += int(((a == 2 * z) & (z > 0)).sum())
        anybad = np.zeros((F, S), dtype=bool)
        for d in bad: anybad |= bad[d]
        any3 = np.zeros((F, S), dtype=bool)
        for d in bad3: any3 |= bad3[d]
        vM = (anybad & ~any3).any(axis=1)                 # good3 and not good
        if vM.any() and self.first is None:
            self.first = ('(M)', None, B[int(np.argmax(vM))].tolist())
        self.failM += int(vM.sum())
        ngood = S - anybad.sum(axis=1); n3good = S - any3.sum(axis=1)
        if m >= 3:
            vE = ngood == 0
            if vE.any() and self.first is None:
                self.first = ('(E)', None, B[int(np.argmax(vE))].tolist())
            self.failE += int(vE.sum())
            bd = stated_bound(m)
            vb = n3good * bd.denominator < bd.numerator * S
            if vb.any() and self.first is None:
                self.first = ('(bd)', None, B[int(np.argmax(vb))].tolist())
            self.failbd += int(vb.sum())
        for store, arr in ((self.min3good, n3good), (self.mingood, ngood)):
            i = int(np.argmin(arr))
            fr = Fraction(int(arr[i]), S)
            if m not in store or fr < store[m][0]:
                store[m] = (fr, B[i].tolist())
    def report(self, extra=''):
        ctx = self.ctx
        print(f"{self.name}: Z_{ctx.N} (k = {ctx.k}, n_3 = {ctx.n3}, n'' = {ctx.n2}); multisets by m: {dict(sorted(self.n.items()))} {extra}")
        print(f"   (2): {self.tests2} tests (multiset, e''), failures {self.fail2}, sharper form failures {self.fail2s}, equality with z > 0 in {self.eq2}")
        print(f"   (C2) characteristic 0: {self.testsC2} tests (multiset, odd e), failures {self.failC2}, sharper {self.failC2s}, equality with z > 0 in {self.eqC2}")
        print(f"   (M) 3-good but not good: {self.failM};  (E) m >= 3 without a good signing: {self.failE};  (bd) 3-good share below the stated bound: {self.failbd}")
        for m in sorted(self.min3good):
            a, b = self.min3good[m], self.mingood[m]
            print(f"   m = {m}: least share 3-good {a[0]} at {a[1]}; least share good {b[0]} at {b[1]}")
        if self.first:
            print("   FIRST FAILURE:", self.first)
        sys.stdout.flush()

def exhaustive(N, mmax, budget, mmin=1):
    ctx = Ctx(N)
    tal = Tally(ctx, 'exhaustive, 0 in the multiset')
    t0 = time.time()
    done = None
    for m in range(mmin, mmax + 1):
        chunk = max(1, min(20000, (1 << 22) // ((1 << (m - 1)) * max(T.shape[1] for T in ctx.tab.values()))))
        it = itertools.combinations_with_replacement(range(N), m - 1)
        stopped = False
        while True:
            block = list(itertools.islice(it, chunk))
            if not block:
                break
            B = np.zeros((len(block), m), dtype=np.int64)
            if m > 1:
                B[:, 1:] = np.array(block, dtype=np.int64)
            tal.add(B)
            if time.time() - t0 > budget:
                stopped = True
                break
        if stopped:
            tal.report(f"-- STOPPED by the time budget inside m = {m}; complete for m <= {done}")
            return
        done = m
    tal.report(f"-- complete for {mmin} <= m <= {done}; {time.time()-t0:.0f} s")

def structured(N, mlo, mhi, count, seed, budget):
    """random multisets of shapes meant to be hard: few residues modulo 2^k; pairs congruent modulo the odd part;
    full sets of residues modulo a prime q >= 5 (live levels), with the 2-part chosen freely or lopsided;
    everything congruent modulo the odd part; a random half translated by N/2 or N/4."""
    ctx = Ctx(N)
    rng = random.Random(seed)
    tal = Tally(ctx, 'random and structured')
    t0 = time.time()
    P2 = 2 ** ctx.k
    odd = N // P2
    primes = [q for q in (5, 7, 11, 13) if N % q == 0]
    def crt(u, w):       # element of Z_N with residue u mod 2^k and w mod odd
        for x in range(u, N, P2):
            if x % odd == w % odd:
                return x
    for m in range(mlo, mhi + 1):
        rows = []
        for _ in range(count):
            mode = rng.randrange(7)
            if mode == 0:
                b = [rng.randrange(N) for _ in range(m - 1)]
            elif mode == 1:
                us = [rng.randrange(P2) for _ in range(rng.randint(1, 3))]
                b = [crt(rng.choice(us), rng.randrange(odd)) for _ in range(m - 1)]
            elif mode == 2:
                b = []
                while len(b) < m - 1:
                    w = rng.randrange(odd)
                    b.append(crt(rng.randrange(P2), w))
                    if len(b) < m - 1:
                        b.append(crt(rng.randrange(P2), w))
            elif mode == 3 and primes:
                # a full set of residues modulo a prime q >= 5; the residues modulo 2^k free, from two values, or
                # all 0 but one; the rest of the multiset: copies of chosen elements, or random elements
                q = rng.choice(primes)
                style = rng.randrange(3)
                two = [rng.randrange(P2), rng.randrange(P2)]
                b = []
                for t in range(q):
                    u = rng.randrange(P2) if style == 0 else (rng.choice(two) if style == 1 else (0 if t else rng.randrange(P2)))
                    b.append(crt(u, t + q * rng.randrange(odd // q)))
                rng.shuffle(b)
                while len(b) < m - 1:
                    b.append(rng.choice(b) if rng.random() < .6 else rng.randrange(N))
                b = b[:m - 1]
            elif mode == 4:
                w = rng.randrange(odd)
                b = [crt(rng.randrange(P2), w) for _ in range(m - 1)]
            elif mode == 5:
                b = [rng.randrange(N) for _ in range((m - 1 + 1) // 2)]
                b = b + [(x + rng.choice([N // 2, N // 4])) % N for x in b]
                b = b[:m - 1]
            else:
                # lopsided on the 2-part: all but one element in one residue modulo 2^k
                b = [crt(0, rng.randrange(odd)) for _ in range(m - 2)] + [crt(rng.randrange(1, P2) if P2 > 1 else 0, rng.randrange(odd))]
                b = b[:m - 1]
            rows.append([0] + b)
        B = np.array(rows, dtype=np.int64)
        chunk = max(1, (1 << 22) // ((1 << (m - 1)) * max(T.shape[1] for T in ctx.tab.values())))
        for s in range(0, len(rows), chunk):
            tal.add(B[s:s + chunk])
            if time.time() - t0 > budget:
                tal.report(f"-- STOPPED by the time budget inside m = {m}")
                return
    tal.report(f"-- m = {mlo}..{mhi}, {count} each; {time.time()-t0:.0f} s")

if __name__ == '__main__':
    mode = sys.argv[1]
    N = int(sys.argv[2])
    if mode == 'exh':
        exhaustive(N, int(sys.argv[3]), float(sys.argv[4]), mmin=int(sys.argv[5]) if len(sys.argv) > 5 else 1)
    elif mode == 'rand':
        structured(N, int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]), float(sys.argv[7]))
