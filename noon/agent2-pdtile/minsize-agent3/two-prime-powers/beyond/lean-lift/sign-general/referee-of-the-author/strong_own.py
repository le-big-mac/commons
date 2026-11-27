"""Referee's recomputation of section 5.2 of sign-general-result.md (Proposition S and the two examples).
Exact integers only; no factoring library.  Written from the text.

Part 1: the construction for arbitrary sides, checked by listing every point of small boxes.
Part 2: a small complete instance (sides 2, 3, 5 and r = 11, a multiset of 242 elements on Z_330), with every
        signing 'all +' and 'one sign turned' divided by cyclotomic polynomials (exact long division).
Part 3: the arithmetic for the primes 3..29 (PI, Q, e, weights, counts, N, r, n, factorisations, primality).
Part 4: the cube sums of the signing with the two elements over x = 0 turned.
"""
from fractions import Fraction as Fr
from itertools import product, combinations
from math import prod, isqrt, gcd

def weights(ps, m, a, b):
    """weights by zero set, as in the text; a, b the two special indices (the text: the first and the last)."""
    PI = prod(ps); qs = [p - 1 for p in ps]
    e = sum(PI // p for p in ps) - PI
    w = {}
    for i in range(len(ps)):
        if i not in (a, b):
            w[frozenset([i])] = m * qs[i] * (PI // ps[i])
    w[frozenset([a])] = m * qs[a] * (PI // ps[a] - e)
    w[frozenset([b])] = m * qs[b] * (PI // ps[b] - e)
    w[frozenset([a, b])] = m * qs[a] * qs[b] * e
    w[frozenset(range(len(ps)))] = 2
    return PI, qs, e, w

# ---------------- Part 1: enumeration on small boxes ----------------
def part1():
    print('Part 1. Counts by listing every point of small boxes (sides need not be prime here):')
    for ps in [(2, 3, 5), (2, 3, 6), (3, 3, 3), (2, 4, 5, 7), (3, 3, 5, 7), (2, 3, 7, 43), (3, 4, 4, 4), (2, 5, 5, 5),
               (3, 3, 4, 13), (2, 3, 11, 13, 17)]:
        for m in (1, 2, 3):
            k = len(ps); a, b = 0, k - 1
            PI, qs, e, w = weights(ps, m, a, b)
            Q = prod(qs)
            if e < 0 or min(w.values()) < 0:
                print(f'   sides {ps} m={m}: e = {e}, least weight {min(w.values())}: construction not available (skipped)')
                continue
            cnt = [[0] * p for p in ps]; total = 0
            for x in product(*[range(p) for p in ps]):
                Z = frozenset(i for i in range(k) if x[i] == 0)
                wx = w.get(Z, 0)
                if wx:
                    total += wx
                    for i in range(k):
                        cnt[i][x[i]] += wx
            ok = total == 2 + m * Q * PI
            for i in range(k):
                u = m * Q * PI // ps[i]
                assert (m * Q * PI) % ps[i] == 0
                ok = ok and cnt[i][0] == u + 2 and all(c == u for c in cnt[i][1:])
            print(f'   sides {ps} m={m}: e = {e}, weights >= 0, total = 2 + mQPI: {total == 2 + m*Q*PI}, '
                  f'class 0 has u_i + 2 and every other class u_i for every i: {ok}')
            assert ok

# ---------------- exact polynomial tools ----------------
def cyclotomic(n):
    """Phi_n as a list of integer coefficients (lowest first), by dividing X^n - 1 by Phi_d, d | n, d < n."""
    cache = cyclotomic.cache
    if n in cache: return cache[n]
    num = [-1] + [0] * (n - 1) + [1]
    for d in range(1, n):
        if n % d == 0:
            num, rem = polydivmod(num, cyclotomic(d))
            assert not any(rem)
    cache[n] = num
    return num
cyclotomic.cache = {}

def polydivmod(a, b):
    """a, b integer lists lowest first, b monic.  Exact long division."""
    a = list(a); db = len(b) - 1
    assert b[-1] == 1
    q = [0] * max(len(a) - db, 1)
    for i in range(len(a) - 1, db - 1, -1):
        c = a[i]
        if c:
            q[i - db] = c
            for j in range(db + 1):
                a[i - db + j] -= c * b[j]
    return q, a[:db] if db > 0 else []

def divisible(coeffs, n, d):
    """coeffs: dict exponent -> integer on Z_n; is the polynomial divisible by Phi_d (d | n)?  Fold to Z_d first."""
    f = [0] * d
    for x, c in coeffs.items():
        f[x % d] += c
    _, rem = polydivmod(f, cyclotomic(d))
    return not any(rem)

def crt(res, mods):
    x = 0; M = prod(mods)
    for r_, m_ in zip(res, mods):
        Mi = M // m_
        x += r_ * Mi * pow(Mi, -1, m_)
    return x % M

# ---------------- Part 2: a small complete instance ----------------
def part2():
    print('Part 2. A complete small instance of Proposition S, every element listed, exact division:')
    for ps, m in [((2, 3, 5), 1), ((2, 3, 5), 3), ((3, 3, 5, 7), 1)]:
        k = len(ps); PI, qs, e, w = weights(ps, m, 0, k - 1); Q = prod(qs)
        N = 2 + m * Q * PI
        # an odd prime r dividing N and prime to PI
        r = next(d for d in range(3, N + 1, 2) if N % d == 0 and gcd(d, PI) == 1 and all(d % t for t in range(3, isqrt(d) + 1, 2)))
        pairwise = all(gcd(ps[i], ps[j]) == 1 for i in range(k) for j in range(i))
        # elements: equal points of G consecutive, t-th element gets t mod r
        elems = []; t = 0
        for x in product(*[range(p) for p in ps]):
            Z = frozenset(i for i in range(k) if x[i] == 0)
            for _ in range(w.get(Z, 0)):
                elems.append((x, t % r)); t += 1
        assert t == N
        maxw = max(w.values())
        if not pairwise:
            # G is not cyclic: check the statement on the class counts only
            okplus = all(sum(1 for (_, c) in elems if c == v) == N // r for v in range(r))
            okturn = True
            for (x, c) in elems:
                good_i = False
                for i in range(k):
                    if x[i] != 0: continue
                    cl = [0] * ps[i]
                    for (y, _) in elems: cl[y[i]] += 1
                    cl[0] -= 2
                    if len(set(cl)) == 1: good_i = True
                okturn = okturn and good_i
            print(f'   sides {ps} m={m}: N = {N}, r = {r} (box not cyclic; class counts only): classes modulo r equal: {okplus}; '
                  f'every single turn equalises the classes of some side i with x_i = 0: {okturn}')
            assert okplus and okturn
            continue
        n = PI * r
        zn = [crt(list(x) + [c], list(ps) + [r]) for (x, c) in elems]
        mult = {}
        for z in zn: mult[z] = mult.get(z, 0) + 1
        divs = [d for d in range(1, n + 1) if n % d == 0]
        plus = dict(mult)
        dplus = [d for d in divs if divisible(plus, n, d)]
        # every single turn: by distinct point of Z_n (turning one copy of z)
        all_bad = True; bad_at = {}
        for z in mult:
            s = dict(mult); s[z] -= 2
            ds = [d for d in divs if divisible(s, n, d)]
            if not ds: all_bad = False
            want = [p for p in ps if z % p == 0]
            assert not ds or any(d in want for d in ds), (z, ds, want)
            for d in ds: bad_at[d] = bad_at.get(d, 0) + mult[z]
        isset = max(mult.values()) == 1
        print(f'   sides {ps} m={m}: N = {N}, r = {r}, n = {n}, largest weight on G {maxw}, a set on Z_n: {isset} (r >= max w: {r >= maxw})')
        print(f'      all +: divisible by Phi_d for d in {dplus}')
        print(f'      every signing with one sign turned has a cyclotomic divisor: {all_bad}; elements by divisor d: {dict(sorted(bad_at.items()))}')
        assert r in dplus and all_bad
        # two turns: is some signing with two signs turned good?  (small case only)
        pts = sorted(mult); found = None
        zero_pt = crt([0] * k + [0], list(ps) + [r])
        for z1, z2 in combinations(pts, 2):
            s = dict(mult); s[z1] -= 2; s[z2] -= 2
            if not any(divisible(s, n, d) for d in divs):
                found = (z1, z2); break
        print(f'      some signing with two signs turned is good: {found is not None} {found}')

# ---------------- Part 3: the arithmetic for 3..29 ----------------
def is_prime_trial(n):
    if n < 2: return False
    if n % 2 == 0: return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0: return False
        d += 2
    return True

def is_prime_mr(n):
    """Miller-Rabin with the first twelve primes as bases: a proof of primality for n < 3.3 * 10^24."""
    if n < 2: return False
    small = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    for p in small:
        if n % p == 0: return n == p
    d = n - 1; s = 0
    while d % 2 == 0: d //= 2; s += 1
    for a in small:
        x = pow(a, d, n)
        if x in (1, n - 1): continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1: break
        else:
            return False
    return True

def part3():
    print('Part 3. The primes 3, ..., 29:')
    ps = [3, 5, 7, 11, 13, 17, 19, 23, 29]
    # the first odd primes whose reciprocals add up to more than 1
    s = Fr(0); odd_primes = [p for p in range(3, 60, 2) if is_prime_trial(p)]
    for p in odd_primes:
        s += Fr(1, p)
        print(f'      sum of 1/p over odd primes up to {p}: {float(s):.6f} {"> 1" if s > 1 else "< 1" if s < 1 else "= 1"}')
        if s > 1:
            first = p; break
    assert first == 29 and odd_primes[:9] == ps
    PI, qs, e, _ = weights(ps, 1, 0, 8); Q = prod(qs)
    print(f'   PI = {PI} (text 3234846615: {PI == 3234846615}); Q = {Q} (text 1021870080: {Q == 1021870080}); '
          f'e = {e} (text 108169298: {e == 108169298})')
    print(f'   PI/29 - e = {PI // 29 - e}, PI/3 - e = {PI // 3 - e} (both must be >= 0)')
    for m in (1, 2, 3):
        PI, qs, e, w = weights(ps, m, 0, 8)
        assert min(w.values()) >= 0
        N = 2 + m * Q * PI
        # counts by class, from the weights and the numbers of points (not from the formula u_i of the text)
        tot = 0; ok = True
        cnt0 = [0] * 9; cntv = [0] * 9          # x_i = 0; x_i = one fixed v != 0
        for Z, wz in w.items():
            npts = prod(qs[j] for j in range(9) if j not in Z)
            tot += wz * npts
            for i in range(9):
                if i in Z: cnt0[i] += wz * npts
                else:
                    assert npts % qs[i] == 0
                    cntv[i] += wz * (npts // qs[i])
        for i in range(9):
            u = m * Q * PI // ps[i]
            ok = ok and cnt0[i] == u + 2 and cntv[i] == u and ps[i] * u + 2 == N
        maxw = max(w.values()); argmax = sorted(ps[i] for i in max(w, key=w.get))
        print(f'   m = {m}: total = {tot} = 2 + mQPI: {tot == N}; counts u_i + 2 and u_i for all nine primes: {ok}; '
              f'largest weight {maxw} at zero set {argmax}; all weights >= 0: {min(w.values()) >= 0}')
        assert ok and tot == N
        if m == 1:
            fac = [2, 103, 70943447, 226188161]
            print(f'      text: N = 3305592969257779202: {N == 3305592969257779202}; 2*103*70943447*226188161 = N: {prod(fac) == N}; '
                  f'primes (trial division): {[is_prime_trial(f) for f in fac]}')
            r = 103; n = PI * r
            print(f'      r = 103 divides N: {N % r == 0}; r does not divide PI: {PI % r != 0}; n = PI*103 = {n} '
                  f'(text 333189201345: {n == 333189201345}); largest weight {maxw} (text 6057480688: {maxw == 6057480688}) > r: multiset')
            print(f'      3*5*7*11*13*17*19*23*29*103 = {3*5*7*11*13*17*19*23*29*103}')
            # largest multiplicity on Z_n itself: a block of w consecutive t has ceil(w/r) or floor(w/r) of each residue
            print(f'      largest multiplicity of a point of Z_n: between {maxw // r} and {-(-maxw // r)}')
        if m == 3:
            fac = [2, 641, 7735396963941761]
            r = fac[2]; n = PI * r
            print(f'      text: N = 9916778907773337602: {N == 9916778907773337602}; 2*641*7735396963941761 = N: {prod(fac) == N}; '
                  f'641 prime: {is_prime_trial(641)}; 7735396963941761 prime (Miller-Rabin, 12 bases, a proof below 3.3e24): {is_prime_mr(r)}')
            print(f'      r >= largest weight {maxw} (text 18172442064: {maxw == 18172442064}): {r >= maxw}; r does not divide PI: {PI % r != 0}; '
                  f'n = PI*r = {n} (text 25022822684488282627989015: {n == 25022822684488282627989015}); N <= n: {N <= n}')
            return r

def part3b(r):
    print('   7735396963941761 prime by trial division up to its square root (odd d): ', end='', flush=True)
    n = r; d = 3; lim = isqrt(n); ok = True
    # wheel over odd numbers, in blocks
    while d <= lim:
        if n % d == 0: ok = False; break
        d += 2
    print(ok)

# ---------------- Part 4: cube sums ----------------
def cube_sum_formula(ps, w, P, turned_at_zero):
    """cube at level P with corners 0 and 1; fold = weights by zero set, with the value at x = 0 lowered by 2 * turned."""
    k = len(ps); qs = [p - 1 for p in ps]; full = frozenset(range(k))
    tot = 0
    for Z, wz in w.items():
        if Z == full:
            tot += wz - 2 * turned_at_zero       # the point 0: every factor [x_i = 0] - [x_i = 1] is 1
        else:
            tot += wz * (-1) ** len(P - Z) * prod(qs[j] for j in range(k) if j not in P and j not in Z)
    return tot

def cube_sum_brute(ps, w, P, turned_at_zero):
    k = len(ps); full = frozenset(range(k)); tot = 0
    for x in product(*[range(p) for p in ps]):
        Z = frozenset(i for i in range(k) if x[i] == 0)
        val = w.get(Z, 0)
        if Z == full: val -= 2 * turned_at_zero
        if not val: continue
        f = 1
        for i in P:
            f *= (1 if x[i] == 0 else 0) - (1 if x[i] == 1 else 0)
        tot += val * f
    return tot

def part4(rbig):
    print('Part 4. Cube sums (corners 0 and 1) of the fold to Z_PI:')
    # the formula against brute force on small boxes
    agree = True
    for ps in [(2, 3, 5), (3, 3, 5, 7), (2, 4, 5, 7)]:
        k = len(ps); PI, qs, e, w = weights(ps, 1, 0, k - 1)
        for rr in range(k + 1):
            for P in combinations(range(k), rr):
                P = frozenset(P)
                for turned in (0, 1, 2):
                    agree = agree and cube_sum_formula(ps, w, P, turned) == cube_sum_brute(ps, w, P, turned)
    print(f'   formula against listing every point on three small boxes, all levels, 0/1/2 turns at the origin: {agree}')
    assert agree
    ps = [3, 5, 7, 11, 13, 17, 19, 23, 29]
    for m, r in [(3, rbig), (1, 103)]:
        PI, qs, e, w = weights(ps, m, 0, 8)
        for turned, name in [(0, 'all +'), (1, 'one element over 0 turned'), (2, 'both elements over 0 turned')]:
            zero = []; zero_mod = []
            for rr in range(10):
                for P in combinations(range(9), rr):
                    cs = cube_sum_formula(ps, w, frozenset(P), turned)
                    if cs == 0: zero.append([ps[i] for i in P])
                    if cs % r == 0: zero_mod.append([ps[i] for i in P])
            print(f'   m = {m}, r = {r}, {name}: of 512 cube sums, equal to 0: {len(zero)}; = 0 mod r: {len(zero_mod)} '
                  f'{zero_mod if len(zero_mod) <= 10 else ""}')

if __name__ == '__main__':
    part1()
    part2()
    r = part3()
    part4(r)
    part3b(r)
