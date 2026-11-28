"""The count for a general odd modulus (result.md, sections 5 and 6): refined level counts R_q(m), the table of
b(m) = tbar(m) + W'(m), and tests of the whole chain by exact arithmetic and all signings.

usage: combine.py table M          R_q(m), W_m(no 3), W'(m), b(m) for 3 <= m <= M (xi from the recursion, as in rec3.py)
       combine.py level            the pattern formula for "3-bad at q^j" against the definition (Z_5, Z_25, Z_7, Z_49)
       combine.py chain SEED COUNT random and structured multisets on Z_15, 45, 75, 105, 135, 225, 315: the chain of
                                   section 5 signing by signing, and the three bounds
"""
import sys, itertools, random
from fractions import Fraction as F
from math import comb, gcd
from functools import lru_cache
import numpy as np


def c(r):
    return F(comb(r, r // 2), 2 ** r)


def pr(v, r):
    if (r + v) % 2 or abs(v) > r:
        return F(0)
    return F(comb(r, (r + v) // 2), 2 ** r)


def recursion(M):                                    # the bounding recursion of section 3 (third copy; see rec3.py)
    xi = {0: F(0)}
    for m in range(1, M + 1):
        best = F(0)
        for r2 in range(0, m // 3 + 1):
            for r1 in range(max(r2, 1), (m - r2) // 2 + 1):
                r0 = m - r1 - r2
                rs = (r0, r1, r2)
                A = 2 * sum(pr(v, r0) * pr(v, r1) * pr(v, r2) for v in range(1, r2 + 1))
                gs = [(c(r) if r % 2 == 0 else 0) + xi[r] for r in rs]
                S = gs[0] * gs[1] * gs[2]
                if all(r % 2 == 0 for r in rs):
                    S = min(S, S - c(r0) * c(r1) * c(r2))
                if r2 == 0 and r0 % 2 and r1 % 2 and r0 <= 7:
                    S = min(S, xi[r0] * xi[r1] / 2)
                best = max(best, A + S)
        xi[m] = best
    return xi


# ---------- refined level count modulo 3
@lru_cache(maxsize=None)
def pmod3(r, w):
    """P(sum of r signs is congruent to w modulo 3)"""
    return sum(pr(v, r) for v in range(-r, r + 1) if (v - w) % 3 == 0)


def partitions(s, parts, largest=None):
    """partitions of s into at most `parts` positive parts, as tuples"""
    if largest is None:
        largest = s
    if s == 0:
        yield ()
        return
    if parts == 0:
        return
    for k in range(min(s, largest), 0, -1):
        for rest in partitions(s - k, parts - 1, k):
            yield (k,) + rest


def group_share(sizes, q):
    """share of signings of a group with subclass sizes `sizes` (the other q - len(sizes) subclasses empty) for which
    the q sums are congruent to one another modulo 3"""
    tot = F(0)
    for w in range(3):
        if len(sizes) < q and w != 0:
            continue
        p = F(1)
        for k in sizes:
            p *= pmod3(k, w)
        tot += p
    return tot


@lru_cache(maxsize=None)
def best_group(s, q, full):
    best = F(0); arg = None
    for part in partitions(s, q):
        if full and len(part) < q:
            continue
        v = group_share(part, q)
        if v > best:
            best = v; arg = part
    return best, arg


@lru_cache(maxsize=None)
def R(q, m):
    """largest share of signings 3-bad at q^j over all size patterns of m elements at a level j of the q-tree with at
    least one full group; also the pattern"""
    best = F(0); arg = None
    for gs in partitions(m, m):                      # sizes of the occupied groups
        for i in set(gs):
            if i < q:
                continue
            v, a = best_group(i, q, True); pat = [a]
            rest = list(gs); rest.remove(i)
            for s in rest:
                v2, a2 = best_group(s, q, False)
                v *= v2; pat.append(a2)
            if v > best:
                best = v; arg = tuple(pat)
    return best, arg


def primes_from(lo, hi):
    return [p for p in range(lo, hi + 1) if all(p % d for d in range(2, int(p ** 0.5) + 1))]


def estars(m):
    """all e* > 1 with prime factors >= 5 and mu(e*) = max v_q (q - 1) <= m - 1, as dicts q -> v"""
    ps = [q for q in primes_from(5, m) if q - 1 <= m - 1]
    out = []
    for vs in itertools.product(*[range(0, (m - 1) // (q - 1) + 1) for q in ps]):
        if any(vs):
            out.append({q: v for q, v in zip(ps, vs) if v})
    return out


def W(m, refined):
    tot = F(0)
    for e in estars(m):
        mu = max(v * (q - 1) for q, v in e.items())
        w = F(1, 2 ** mu)
        if refined and len(e) == 1 and list(e.values()) == [1]:
            q = list(e)[0]
            w = min(w, R(q, m)[0])
        tot += w
    return tot


def table(M):
    xi = recursion(M)
    print("R_q(m): largest share 3-bad at a live level of q, with a pattern (full group first)")
    for m in range(5, min(M, 14) + 1):
        for q in (5, 7, 11, 13):
            if q <= m:
                v, a = R(q, m)
                print(f"  m = {m:2d}  q = {q:2d}  R = {str(v):>10s}  2^(1-q) = {F(1, 2 ** (q - 1))}  pattern {a}")
    print("m, tbar(m) = [m even] c_m + xi(m), W_m(no 3), W'(m) (prime e* refined), b = tbar + W', b <= 3/8, crude tbar + W <= 3/8")
    allok = True
    for m in range(3, M + 1):
        t = (c(m) if m % 2 == 0 else 0) + xi[m]
        if m <= 26:
            w0 = W(m, False); w1 = W(m, True if m <= 14 else False)
        else:
            w0 = w1 = None                             # use W(no 3) < 0.118569 (even-result-2.md, Lemma L3 (c))
        if w0 is not None:
            b = t + w1; ok = b <= F(3, 8); allok &= ok
            print(f"  m = {m:2d}  tbar = {str(t):>16s}  W = {str(w0):>10s}  W' = {str(w1):>10s}  b = {str(b):>18s} = {float(b):.6f}  {ok}   crude: {t + w0 <= F(3, 8)}")
        else:
            ok = t + F(118569, 10 ** 6) <= F(3, 8); allok &= ok
            if m % 20 == 0 or m <= 30:
                print(f"  m = {m:3d}  tbar = {float(t):.6f}  tbar + 0.118569 = {float(t) + 0.118569:.6f}  {ok}")
    print(f"b(m) <= 3/8 for every 3 <= m <= {M}: {allok}")


# ---------- exact arithmetic with cyclotomic polynomials
def polymul(a, b):
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                out[i + j] += x * y
    return out


def polydiv_exact(a, b):
    a = a[:]; q = [0] * (len(a) - len(b) + 1)
    for i in range(len(a) - len(b), -1, -1):
        x = a[i + len(b) - 1]
        assert x % b[-1] == 0
        x //= b[-1]; q[i] = x
        for j, y in enumerate(b):
            a[i + j] -= x * y
    assert not any(a)
    return q


@lru_cache(maxsize=None)
def cyclo(d):
    p = [-1] + [0] * (d - 1) + [1]
    for e in range(1, d):
        if d % e == 0:
            p = polydiv_exact(p, list(cyclo(e)))
    return tuple(p)


@lru_cache(maxsize=None)
def redmat(n, d):
    """integer matrix (phi(d) x n): column k = X^k modulo Phi_d"""
    phi = list(cyclo(d)); deg = len(phi) - 1
    cols = []
    cur = [1] + [0] * (deg - 1) if deg > 0 else []
    for k in range(n):
        cols.append(cur[:])
        nxt = [0] + cur                              # multiply by X
        top = nxt[deg]
        nxt = nxt[:deg]
        if top:
            for j in range(deg):
                nxt[j] -= top * phi[j]
        cur = nxt
    return np.array(cols, dtype=np.int64).T


def signs_matrix(m):
    return np.array(list(itertools.product((1, -1), repeat=m)), dtype=np.int64)


def remainders(n, B, d, E):
    """rows: signings; the remainder of the signed mask modulo Phi_d (exact integers)"""
    Rm = redmat(n, d)
    return E @ Rm[:, B].T                            # (2^m, phi(d))


def live_levels(B, q, vq):
    out = []
    for j in range(1, vq + 1):
        groups = {}
        for b in B:
            groups.setdefault(b % q ** (j - 1), set()).add(b % q ** j)
        if any(len(s) == q for s in groups.values()):
            out.append(j)
    return out


def pattern(B, q, j):
    groups = {}
    for b in B:
        groups.setdefault(b % q ** (j - 1), {}).setdefault(b % q ** j, 0)
        groups[b % q ** (j - 1)][b % q ** j] += 1
    return [tuple(sorted(g.values(), reverse=True)) for g in groups.values()]


def level_test():
    total = 0; live_cases = 0
    for (n, q, ms, mode) in [(5, 5, (5, 6, 7, 8, 9, 10), 'all'), (25, 5, (5, 6, 7, 8, 9, 10), 'random'),
                             (7, 7, (7, 8, 9, 10), 'all'), (49, 7, (7, 8, 9, 10), 'random')]:
        vq = 1 if n == q else 2
        rnd = random.Random(n)
        for m in ms:
            E = signs_matrix(m)
            if mode == 'all':
                Bs = [list(t) for t in itertools.combinations_with_replacement(range(n), m)]
            else:
                Bs = []
                for _ in range(150):
                    style = rnd.randint(0, 2)
                    if style == 0:
                        B = [rnd.randrange(n) for _ in range(m)]
                    elif style == 1:                    # a full group at level 2 and a heavy subclass
                        base = rnd.randrange(q); B = [base + q * t for t in range(q)]
                        B += [rnd.choice(B[:q]) for _ in range(m - q)]
                    else:                               # a full group at level 1, elements repeated
                        B = [t + q * rnd.randrange(q) for t in range(q)]
                        B += [rnd.choice(B[:q]) if rnd.random() < .7 else rnd.randrange(n) for _ in range(m - q)]
                    Bs.append(B)
            worst = F(0)
            for B in Bs:
                for j in range(1, vq + 1):
                    V = remainders(n, B, q ** j, E)
                    bad3 = int((~np.any(V % 3 != 0, axis=1)).sum())
                    pat = pattern(B, q, j)
                    formula = F(1)
                    for gsz in pat:
                        formula *= group_share(gsz, q)
                    assert F(bad3, 2 ** m) == formula, ("pattern formula fails", n, B, j)
                    total += 1
                    if j in live_levels(B, q, vq):
                        live_cases += 1
                        assert formula <= R(q, m)[0], ("R fails", n, B, j)
                        worst = max(worst, formula)
            print(f"Z_{n}, m = {m}: {len(Bs)} multisets ({mode}); largest share 3-bad at a live level: {worst}; R_{q}({m}) = {R(q, m)[0]}", flush=True)
    print(f"pattern formula = definition in {total} cases (multiset, level); {live_cases} with the level live, each <= R_q(m); no failure")


MS = [5, 6, 6, 7, 8, 8, 9, 10, 10]


def chain_test(seed, count):
    rnd = random.Random(seed)
    xi = recursion(12)
    stats = {}
    done = 0
    moduli = [15, 45, 75, 105, 135, 225, 315]
    for trial in range(count):
        n = rnd.choice(moduli)
        m = rnd.choice(MS)
        a3 = 0
        while n % 3 ** (a3 + 1) == 0:
            a3 += 1
        n2 = n // 3 ** a3
        style = rnd.randint(0, 3)
        if style == 0:
            B = [rnd.randrange(n) for _ in range(m)]
        else:
            # residues modulo 3^a from a heavy / paired pattern, residues modulo n'' covering a full group of 5 or 7
            if style == 1:
                r3 = [0] * (m - 4) + [1, 1, 2, 2] if m % 2 == 0 else [0] * (m - 2) + [1, 2]
            elif style == 2:
                r3 = ([0, 0, 1, 1, 2, 2] + [3 % 3 ** a3, 3 % 3 ** a3, 6 % 3 ** a3, 6 % 3 ** a3] + [0] * m)[:m]
            else:
                r3 = [rnd.randrange(3 ** a3) for _ in range(m)]
            q = rnd.choice([p for p in (5, 7) if n2 % p == 0])
            r2 = [t * (n2 // q) % n2 for t in range(q)] if rnd.random() < .5 else list(range(q))
            r2 = (r2 + [rnd.choice(r2) if rnd.random() < .8 else rnd.randrange(n2) for _ in range(m)])[:m]
            rnd.shuffle(r2)
            B = [next(x for x in range(n) if x % 3 ** a3 == u % 3 ** a3 and x % n2 == v) for u, v in zip(r3, r2)]
        E = signs_matrix(m); tot = 2 ** m
        divs = [d for d in range(1, n + 1) if n % d == 0]
        badat = {d: ~np.any(remainders(n, B, d, E) != 0, axis=1) for d in divs}
        bad = np.zeros(tot, dtype=bool)
        for d in divs:
            bad |= badat[d]
        bad3pow = np.zeros(tot, dtype=bool)
        for i in range(a3 + 1):
            bad3pow |= badat[3 ** i]
        # live e' > 1 dividing n'' = n2
        primes = [p for p in (5, 7) if n2 % p == 0]
        vq = {}
        for p in primes:
            v = 0
            while n2 % p ** (v + 1) == 0:
                v += 1
            vq[p] = v
        live = {p: live_levels(B, p, vq[p]) for p in primes}
        liveE = []
        for choice in itertools.product(*[[0] + live[p] for p in primes]):
            if any(choice):
                e = 1; es = 1
                for p, j in zip(primes, choice):
                    e *= p ** j
                    es *= p ** (sum(1 for l in live[p] if l <= j))
                liveE.append((e, es, choice))
        threebad_live = np.zeros(tot, dtype=bool)
        wsum = F(0)
        for e, es, choice in liveE:
            tb = ~np.any(remainders(n, B, e, E) % 3 != 0, axis=1)
            threebad_live |= tb
            # the weight of e*
            fac = {}
            x = es
            for p in primes:
                while x % p == 0:
                    fac[p] = fac.get(p, 0) + 1; x //= p
            mu = max(v * (p - 1) for p, v in fac.items())
            w = F(1, 2 ** mu)
            assert mu <= m - 1
            if len(fac) == 1 and list(fac.values()) == [1]:
                w = min(w, R(list(fac)[0], m)[0])
            assert F(int(tb.sum()), tot) <= w, ("level weight fails", n, B, e)
            wsum += w
        # the chain: bad => bad at a power of 3, or 3-bad at a live e' > 1
        assert not np.any(bad & ~bad3pow & ~threebad_live), ("chain fails", n, B)
        t = (c(m) if m % 2 == 0 else 0) + xi[m]
        s_bad = F(int(bad.sum()), tot); s_3 = F(int(bad3pow.sum()), tot); s_rest = F(int((bad & ~bad3pow).sum()), tot)
        assert s_3 <= t, ("tbar fails", n, B)
        assert s_rest <= wsum <= W(m, True), ("W' fails", n, B)
        assert s_bad <= t + W(m, True) <= F(3, 8), ("b fails", n, B)
        if m == 7:                                       # section 6: no signing is 3-bad at a live 5^j 7^k
            assert s_bad <= F(7, 32), ("beta(7) fails", n, B)
            for e, es, choice in liveE:
                if es == 35:
                    assert not np.any(~np.any(remainders(n, B, e, E) % 3 != 0, axis=1)), ("35 at m = 7", n, B)
        key = m
        st = stats.setdefault(key, [0, F(0), F(0), F(0), None])
        st[0] += 1; st[2] = max(st[2], s_3); st[3] = max(st[3], s_rest)
        if s_bad > st[1]:
            st[1] = s_bad; st[4] = (n, sorted(B))
        done += 1
    print(f"seed {seed}: {done} multisets on Z_15, 45, 75, 105, 135, 225, 315, all signings; chain and bounds hold in every case")
    for m in sorted(stats):
        st = stats[m]
        t = (c(m) if m % 2 == 0 else 0) + xi[m]
        print(f"  m = {m:2d}: {st[0]:4d} multisets; largest bad share {st[1]} = {float(st[1]):.4f} (b(m) = {t + W(m, True)}) at {st[4]}; "
              f"largest share bad at a power of 3: {st[2]} (tbar = {t}); largest share bad elsewhere only: {st[3]} (W' = {W(m, True)})")


def primepower_test():
    """prime powers q^a, q = 5, 7 (section 7): characteristic 0, by the definition"""
    for (n, q, ms, mode) in [(5, 5, range(5, 12), 'all'), (25, 5, range(5, 11), 'random'), (125, 5, (9, 10), 'random'),
                             (7, 7, range(7, 11), 'all'), (49, 7, range(7, 11), 'random')]:
        vq = {5: 1, 25: 2, 125: 3, 7: 1, 49: 2}[n]
        rnd = random.Random(1000 + n)
        for m in ms:
            E = signs_matrix(m); tot = 2 ** m
            if mode == 'all':
                Bs = [list(t) for t in itertools.combinations_with_replacement(range(n), m)]
            else:
                Bs = []
                for _ in range(300):
                    style = rnd.randint(0, 3)
                    if style == 0:
                        B = [rnd.randrange(n) for _ in range(m)]
                    elif style == 1:                    # a full group at level 2 inside one class, heavy subclass
                        base = rnd.randrange(q); B = [base + q * t for t in range(q)]
                        B += [rnd.choice(B[:q]) for _ in range(m - q)]
                    elif style == 2:                    # full at level 1, one class full again at level 2 (two live levels)
                        B = [t for t in range(1, q)] + [q * t for t in range(q)]
                        B = (B + [rnd.choice(B) for _ in range(m)])[:m] if m >= 2 * q - 1 else [t + q * rnd.randrange(q) for t in range(q)] + [rnd.randrange(n) for _ in range(m - q)]
                    else:
                        B = [t + q * rnd.randrange(q) for t in range(q)]
                        B += [rnd.choice(B[:q]) for _ in range(m - q)]
                    Bs.append(B)
            L = (m - 1) // (q - 1)
            lev = F(c(m - q + 1), 2 ** (q - 2))          # 2^(2-q) c_(m-q+1)
            if m % 2:
                bound = lev + sum(F(1, 2 ** (l * (q - 1))) for l in range(2, L + 1))
            else:
                bound = c(m) + sum(F(1, 2 ** (l * (q - 1))) for l in range(1, L + 1))
            worst = F(0); worstlev = F(0); ex = None
            for B in Bs:
                bad = ~np.any(remainders(n, B, 1, E) != 0, axis=1)
                for j in range(1, vq + 1):
                    bj = ~np.any(remainders(n, B, q ** j, E) != 0, axis=1)
                    if m % 2:
                        assert F(int(bj.sum()), tot) <= lev, ("single level fails", n, B, j)
                    worstlev = max(worstlev, F(int(bj.sum()), tot))
                    bad |= bj
                sh = F(int(bad.sum()), tot)
                assert sh <= bound, ("prime power bound fails", n, B)
                assert sh <= F(3, 8) or m < 3
                if sh > worst:
                    worst = sh; ex = B
            print(f"Z_{n}, m = {m:2d}: {len(Bs):5d} multisets ({mode}); largest bad share {worst} (bound {bound}"
                  f"{'; 2^(2-q) c_(m-q+1) = ' + str(lev) if m % 2 else '; c_m = ' + str(c(m))}); largest share at one level q^j, j >= 1: {worstlev}; e.g. {sorted(ex)}", flush=True)
    print("no failure")


def exhaust(n, m):
    """every multiset of m elements of Z_n that contains 0 (the events are invariant under translation), all signings"""
    xi = recursion(m)
    t = (c(m) if m % 2 == 0 else 0) + xi[m]; b = t + W(m, True)
    E = signs_matrix(m); tot = 2 ** m
    divs = [d for d in range(1, n + 1) if n % d == 0]
    mats = [redmat(n, d) for d in divs]
    best = 0; ex = None; count = 0
    for rest in itertools.combinations_with_replacement(range(n), m - 1):
        B = [0] + list(rest)
        bad = np.zeros(tot, dtype=bool)
        for Rm in mats:
            bad |= ~np.any((E @ Rm[:, B].T) != 0, axis=1)
        k = int(bad.sum()); count += 1
        if k > best:
            best = k; ex = B
    assert F(best, tot) <= b
    print(f"Z_{n}, m = {m}: {count} multisets with 0, all signings: largest bad share {F(best, tot)} at {ex};  b(m) = {b}", flush=True)


def set_partitions(k, blocks_exact=None, blocks_max=None):
    """restricted growth strings of length k"""
    def rec(prefix, mx):
        if len(prefix) == k:
            nb = mx + 1
            if (blocks_exact is None or nb == blocks_exact) and (blocks_max is None or nb <= blocks_max):
                yield tuple(prefix)
            return
        lim = mx + 1
        if blocks_max is not None:
            lim = min(lim, blocks_max - 1)
        if blocks_exact is not None:
            lim = min(lim, blocks_exact - 1)
        for v in range(0, lim + 1):
            yield from rec(prefix + [v], max(mx, v))
    yield from rec([0], 0)


def search8():
    """eight elements on Z_105 with every level live: residues modulo 7 of pattern (2, 1^6) (elements 0, 1 the pair),
    every partition into five classes modulo 5, every partition into at most three classes modulo 3; all signings.
    (The events do not change when the classes modulo a prime are permuted.)"""
    n = 105; m = 8
    E = signs_matrix(m)[: 2 ** (m - 1)]                   # first sign +
    divs = [d for d in range(1, n + 1) if n % d == 0]
    mats = [redmat(n, d) for d in divs]
    crt = {(x % 3, x % 5, x % 7): x for x in range(n)}
    r7 = [0, 0, 1, 2, 3, 4, 5, 6]
    P5 = list(set_partitions(m, blocks_exact=5)); P3 = list(set_partitions(m, blocks_max=3))
    best = 0; ex = None; count = 0; hist = {}
    for p5 in P5:
        for p3 in P3:
            B = [crt[(p3[i], p5[i], r7[i])] for i in range(m)]
            bad = np.zeros(2 ** (m - 1), dtype=bool)
            for Rm in mats:
                bad |= ~np.any((E @ Rm[:, B].T) != 0, axis=1)
            k = int(bad.sum()); count += 1
            hist[k] = hist.get(k, 0) + 1
            if k > best:
                best = k; ex = B
    top = sorted(hist.items(), reverse=True)[:4]
    print(f"Z_105, eight elements, 5 and 7 live: {count} multisets ({len(P5)} partitions modulo 5 x {len(P3)} modulo 3), all signings: "
          f"largest bad share {F(best, 2 ** (m - 1))} at {sorted(ex)}; the largest counts (out of 128): {top}")


def example(n, B):
    m = len(B); E = signs_matrix(m); tot = 2 ** m
    divs = [d for d in range(1, n + 1) if n % d == 0]
    badat = {d: ~np.any(remainders(n, B, d, E) != 0, axis=1) for d in divs}
    bad = np.zeros(tot, dtype=bool); bad3 = np.zeros(tot, dtype=bool)
    for d in divs:
        bad |= badat[d]
        if 3 ** round(np.log(d) / np.log(3)) == d:
            bad3 |= badat[d]
    where = {d: F(int(badat[d].sum()), tot) for d in divs if badat[d].any()}
    print(f"  Z_{n}, m = {m}, B = {B}: bad share {F(int(bad.sum()), tot)}; bad at a power of 3: {F(int(bad3.sum()), tot)}; "
          f"bad at 1: {F(int(badat[1].sum()), tot)}; share bad at d, by d: " + ", ".join(f"{d}: {v}" for d, v in where.items()))


def examples():
    print("the examples cited in result.md, all signings, by division by the cyclotomic polynomials:")
    for m in (3, 5, 7, 9, 11, 13):
        example(3, [0] * (m - 2) + [1, 2])
    example(3, [0, 0, 1, 1, 2, 2]); example(3, [0, 0, 0, 0, 1, 1, 2, 2])
    example(9, [0, 0, 1, 1, 2, 2, 3, 3, 6, 6]); example(9, [0, 0, 0, 0, 3, 3, 6, 6, 1, 1, 2, 2])
    example(15, [6, 8, 9, 10, 12]); example(105, [0, 3, 9, 12, 32, 36, 97])
    example(45, [0, 1, 1, 3, 12, 20, 24, 27, 29, 33]); example(225, [1, 29, 51, 63, 75, 100, 128, 129, 162, 177])
    example(15, [3, 6, 9, 12, 5, 10])                    # six elements: 11/32 in a second way (bad at 15, not at 3)


if __name__ == '__main__':
    if sys.argv[1] == 'examples':
        examples()
    elif sys.argv[1] == 'exhaust':
        exhaust(int(sys.argv[2]), int(sys.argv[3]))
    elif sys.argv[1] == 'search8':
        search8()
    elif sys.argv[1] == 'primepower':
        primepower_test()
    elif sys.argv[1] == 'table':
        table(int(sys.argv[2]))
    elif sys.argv[1] == 'level':
        level_test()
    else:
        if len(sys.argv) > 4:                            # optional: the sizes m to draw from (at most 12)
            MS[:] = [int(x) for x in sys.argv[4:]]
        chain_test(int(sys.argv[2]), int(sys.argv[3]))
