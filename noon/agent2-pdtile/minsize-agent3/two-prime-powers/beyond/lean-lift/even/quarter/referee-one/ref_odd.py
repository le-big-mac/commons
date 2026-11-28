"""Referee's tests on general odd moduli (sections 6, 7 of result.md), by the definition: a signing is bad at d iff
the remainder of its signed mask modulo Phi_d is 0 (exact integers), all signings.

usage: ref_odd.py examples
       ref_odd.py exhaust N M            every multiset of M elements of Z_N that contains 0
       ref_odd.py chain SEED COUNT MLO MHI N1 N2 ...   random and structured multisets: the chain of section 6, Lemma R,
                                         the weights, tbar, b(m)
       ref_odd.py pp                     prime powers: Lemma V, Theorem P
"""
import sys, random, itertools
from fractions import Fraction as Fr
from math import comb
import numpy as np
from cyc import rem_matrix, divisors, signs, bad_at, three_bad_at, factor, live_levels

# the text's table (section 6); recomputed independently in ref_rec.py
TBAR = {3: Fr(1, 4), 4: Fr(3, 8), 5: Fr(3, 16), 6: Fr(11, 32), 7: Fr(5, 32), 8: Fr(39, 128), 9: Fr(35, 256), 10: Fr(145, 512),
        11: Fr(63, 512), 12: Fr(267, 1024), 13: Fr(231, 2048), 14: Fr(2025, 8192)}
WP = {3: Fr(0), 4: Fr(0), 5: Fr(1, 16), 6: Fr(1, 32), 7: Fr(5, 64), 8: Fr(1, 16), 9: Fr(5, 64), 10: Fr(19, 256), 11: Fr(21, 256),
      12: Fr(165, 2048), 13: Fr(369, 4096), 14: Fr(367, 4096)}
BB = {m: TBAR[m] + WP[m] for m in TBAR}
BETA_EXACT = {3: Fr(1, 4), 4: Fr(3, 8), 5: Fr(1, 4), 6: Fr(11, 32), 7: Fr(7, 32)}        # claimed exact values
assert [BB[m] for m in range(3, 13)] == [Fr(1, 4), Fr(3, 8), Fr(1, 4), Fr(3, 8), Fr(15, 64), Fr(47, 128), Fr(55, 256), Fr(183, 512), Fr(105, 512), Fr(699, 2048)]


def cc(r):
    return Fr(comb(r, r // 2), 2 ** r)


def p3(k, w):
    return Fr(sum(comb(k, j) for j in range(k + 1) if (2 * j - k - w) % 3 == 0), 2 ** k)


def group_formula(sizes):
    """sizes of all q subclasses (zeros included): share of signings with the q sums congruent modulo 3"""
    tot = Fr(0)
    for w in range(3):
        p = Fr(1)
        for k in sizes:
            p *= p3(k, w)
        tot += p
    return tot


def R_pattern(q, m):
    return group_formula([m - q + 1] + [1] * (q - 1))


def level_formula(B, q, j):
    """Lemma R: product over the groups at level j of the q-tree"""
    groups = {}
    for b in B:
        g = groups.setdefault(b % q ** (j - 1), [0] * q)
        g[(b % q ** j) // q ** (j - 1)] += 1
    out = Fr(1)
    for g in groups.values():
        out *= group_formula(g)
    return out


def share(v):
    return Fr(int(v.sum()), len(v))


def analyse(n, B, strict=True):
    """all the statements of section 6 for one multiset; returns shares"""
    m = len(B); E = signs(m); T = 2 ** m
    f = factor(n); a3 = f.get(3, 0); n2 = n // 3 ** a3
    badd = {d: bad_at(n, B, d, E) for d in divisors(n)}
    bad = np.zeros(T, dtype=bool)
    for v in badd.values():
        bad |= v
    bad3 = np.zeros(T, dtype=bool)
    for i in range(a3 + 1):
        bad3 |= badd[3 ** i]
    qs = [q for q in f if q != 3]
    live = {q: live_levels(B, q, f[q]) for q in qs}
    # Lemma R at every level of every prime q >= 5 (live or not): exact formula
    for q in qs:
        for j in range(1, f[q] + 1):
            tb = three_bad_at(n, B, q ** j, E)
            assert share(tb) == level_formula(B, q, j), ("Lemma R formula", n, B, q, j)
            if j in live[q]:
                assert share(tb) <= R_pattern(q, m), ("R_q(m)", n, B, q, j)
    # the live e' > 1, their e'*, weights
    union3 = np.zeros(T, dtype=bool); wsum = Fr(0); info = []
    for choice in itertools.product(*[[0] + live[q] for q in qs]):
        if not any(choice):
            continue
        e = 1; star = {}
        for q, j in zip(qs, choice):
            if j:
                e *= q ** j
                star[q] = sum(1 for l in live[q] if l <= j)
        mu = max(l * (q - 1) for q, l in star.items())
        assert mu <= m - 1, ("cut-off", n, B, e)
        w = Fr(1, 2 ** mu)
        if m <= 14 and len(star) == 1 and list(star.values()) == [1]:
            w = min(w, R_pattern(list(star)[0], m))
        tb = three_bad_at(n, B, e, E)
        assert share(tb) <= w, ("weight", n, B, e, share(tb), w)
        union3 |= tb; wsum += w
        info.append((e, star, share(tb)))
        if m == 7 and set(star) == {5, 7}:
            assert not tb.any(), ("seven elements, 3-bad at a live 5^j 7^k", n, B, e)
    # the chain: bad => bad at a power of 3, or 3-bad at a live e' > 1
    assert not np.any(bad & ~bad3 & ~union3), ("chain", n, B)
    # every bad signing is bad at 3^i e' with e' live or 1 (the step-down in characteristic 0)
    cover = bad3.copy()
    for choice in itertools.product(*[[0] + live[q] for q in qs]):
        e = 1
        for q, j in zip(qs, choice):
            e *= q ** j
        for i in range(a3 + 1):
            cover |= badd[3 ** i * e]
    assert not np.any(bad & ~cover), ("step-down", n, B)
    s_bad, s_3, s_rest = share(bad), share(bad3), share(bad & ~bad3)
    if m in TBAR:
        assert s_3 <= TBAR[m], ("tbar", n, B, s_3)
        assert wsum <= WP[m] or not strict, ("sum of weights above W'", n, B, wsum)
        assert s_rest <= WP[m], ("W'", n, B, s_rest)
        assert s_bad <= BB[m] <= Fr(3, 8), ("b(m)", n, B, s_bad)
    if m in BETA_EXACT:
        assert s_bad <= BETA_EXACT[m], ("claimed exact beta", n, B, s_bad)
    if m % 2 and m >= 5:
        assert s_bad <= Fr(1, 4), ("odd m", n, B, s_bad)
    if m % 2 == 0 and m >= 8:
        assert s_bad <= Fr(47, 128), ("even m >= 8", n, B, s_bad)
    assert s_bad <= Fr(3, 8) or m < 3, ("Conjecture Q", n, B, s_bad)
    return s_bad, s_3, s_rest, {d: share(v) for d, v in badd.items() if v.any()}


def examples():
    cases = [(3, [0] * (m - 2) + [1, 2], cc(m - 2) / 2) for m in (3, 5, 7, 9, 11, 13, 15)]
    cases += [(3, [0, 0, 1, 1, 2, 2], Fr(11, 32)), (3, [0] * 4 + [1, 1, 2, 2], Fr(39, 128)),
              (9, [0, 0, 1, 1, 2, 2, 3, 3, 6, 6], Fr(145, 512)), (9, [0, 0, 0, 0, 3, 3, 6, 6, 1, 1, 2, 2], Fr(267, 1024)),
              (15, [6, 8, 9, 10, 12], Fr(1, 4)), (105, [0, 3, 9, 12, 32, 36, 97], Fr(7, 32)),
              (45, [0, 1, 1, 3, 12, 20, 24, 27, 29, 33], Fr(73, 256)), (225, [1, 29, 51, 63, 75, 100, 128, 129, 162, 177], Fr(73, 256)),
              (15, [3, 6, 9, 12, 5, 10], Fr(11, 32)), (135, [0, 0, 1, 1, 2, 29, 33, 54, 57, 57, 87, 108], Fr(269, 1024))]
    for n, B, claim in cases:
        s_bad, s_3, s_rest, where = analyse(n, B)
        print(f"Z_{n} m={len(B)} {B}: bad {s_bad} (text: {claim}; equal: {s_bad == claim}); at a power of 3: {s_3}; by d: " +
              ", ".join(f"{d}: {v}" for d, v in where.items()))
    # prime powers q >= 5: the pattern (m-q+1, 1, ..., 1)
    for q in (5, 7, 11):
        for m in range(q, min(2 * q + 3, 15), 2):
            B = [0] * (m - q + 1) + list(range(1, q))
            s = share(bad_at(q, B, q) | bad_at(q, B, 1))
            print(f"Z_{q} m={m} pattern (m-q+1,1,..,1): bad {s}; 2^(2-q) c_(m-q+1) = {cc(m - q + 1) / 2 ** (q - 2)}; equal: {s == cc(m - q + 1) / 2 ** (q - 2)}")


def exhaust(n, m):
    """DFS over nondecreasing b_1 = 0 <= b_2 <= ... <= b_m; first sign +; remainders modulo all Phi_d side by side"""
    divs = divisors(n)
    big = np.hstack([rem_matrix(n, d) for d in divs]).astype(np.int16)        # (n, n)
    cuts = np.cumsum([0] + [rem_matrix(n, d).shape[1] for d in divs])
    blocks = [(int(cuts[i]), int(cuts[i + 1])) for i in range(len(divs))]
    best = 0; ex = None; count = 0; hist = {}
    cap = BB.get(m)
    claim = BETA_EXACT.get(m)

    def rec(k, lo, arr, B):
        nonlocal best, ex, count
        if k == m:
            bad = np.zeros(arr.shape[0], dtype=bool)
            for s, e in blocks:
                bad |= ~arr[:, s:e].any(axis=1)
            c = int(bad.sum()); count += 1
            hist[c] = hist.get(c, 0) + 1
            if c > best:
                best = c; ex = B[:]
            return
        for b in range(lo, n):
            v = big[b]
            B.append(b)
            rec(k + 1, b, np.concatenate((arr + v, arr - v)), B)
            B.pop()

    rec(1, 0, big[0][None, :].copy(), [0])
    sh = Fr(best, 2 ** (m - 1))
    ok = (cap is None or sh <= cap) and (claim is None or sh <= claim) and (m < 3 or sh <= Fr(3, 8))
    top = sorted(hist.items(), reverse=True)[:3]
    print(f"Z_{n}, m = {m}: {count} multisets with 0, all signings: largest bad share {sh} at {ex}; b(m) = {cap}; claimed exact beta = {claim}; within every claim: {ok}; largest counts of {2 ** (m - 1)}: {top}", flush=True)
    assert ok


def crt_elem(n, res):
    """the element of Z_n with the given residues {modulus: residue}"""
    for x in range(n):
        if all(x % md == r % md for md, r in res.items()):
            return x
    raise ValueError


def structured(rnd, n, m):
    f = factor(n); a3 = f.get(3, 0); P3 = 3 ** a3
    style = rnd.randint(0, 5)
    if style == 0:
        return [rnd.randrange(n) for _ in range(m)]
    # residues modulo 3^a
    k = rnd.randint(0, 4)
    if a3 == 0:
        r3 = [0] * m
    elif k == 0:
        r3 = ([0] * (m - 2) + [1, 2]) if m % 2 else ([0] * (m - 4) + [1, 1, 2, 2])
    elif k == 1:
        base = [0, 0, 1, 1, 2, 2, 3, 3, 6, 6, 4, 4, 5, 5]
        r3 = [x % P3 for x in base[:m]] + [0] * max(0, m - len(base))
    elif k == 2:
        r3 = [rnd.randrange(P3) for _ in range(m)]
    elif k == 3:
        pool = [rnd.randrange(P3) for _ in range(3)]; r3 = [rnd.choice(pool) for _ in range(m)]
    else:
        pool = [rnd.randrange(P3) for _ in range(m // 2 + 1)]; r3 = (pool + pool)[:m]
    rnd.shuffle(r3)
    res = [{P3: r} if a3 else {} for r in r3]
    for q in f:
        if q == 3:
            continue
        Q = q ** f[q]
        if q <= m and rnd.random() < 0.8:
            lvl = rnd.randint(1, f[q])                      # a full group at this level, then heavy or spread
            base = rnd.randrange(q ** (lvl - 1))
            full = [(base + t * q ** (lvl - 1)) % Q for t in range(q)]
            mode = rnd.randint(0, 2)
            if mode == 0:
                rq = full + [full[0]] * (m - q)
            elif mode == 1:
                rq = full + [rnd.choice(full) for _ in range(m - q)]
            else:
                rq = full + [rnd.randrange(Q) for _ in range(m - q)]
            if f[q] >= 2 and m >= 2 * q - 1 and rnd.random() < 0.5:     # a second live level
                rq = [t for t in range(q)] + [q * t for t in range(1, q)] + [rnd.choice([0, 1, q]) for _ in range(m - 2 * q + 1)]
            rnd.shuffle(rq)
        else:
            pool = [rnd.randrange(Q) for _ in range(rnd.randint(1, 3))]; rq = [rnd.choice(pool) for _ in range(m)]
        for i in range(m):
            res[i][Q] = rq[i]
    return [crt_elem(n, r) for r in res]


def chain(seed, count, mlo, mhi, moduli):
    rnd = random.Random(seed); best = {}; nsign = 0; nlive = 0
    for _ in range(count):
        n = rnd.choice(moduli); m = rnd.randint(mlo, mhi)
        B = structured(rnd, n, m)
        s_bad, s_3, s_rest, where = analyse(n, B, strict=True)
        nsign += 2 ** m
        if any(live_levels(B, q, v) for q, v in factor(n).items() if q != 3):
            nlive += 1
        if s_bad > best.get(m, (Fr(-1),))[0]:
            best[m] = (s_bad, n, sorted(B), s_3, s_rest)
    print(f"seed {seed}: {count} multisets ({nlive} with a live level of a prime >= 5) on {moduli}, {mlo}..{mhi} elements, {nsign} signings: chain, step-down, Lemma R, weights, tbar, W', b(m), claimed exact values: no failure")
    for m in sorted(best):
        s, n, B, s3, sr = best[m]
        print(f"  m = {m}: largest bad share {s} = {float(s):.4f} (b = {BB.get(m)}) on Z_{n} {B}; there: at a power of 3 {s3}, elsewhere only {sr}")


def pp():
    rnd = random.Random(5)
    for n, q, a, ms, mode in [(5, 5, 1, range(3, 14), 'all'), (7, 7, 1, range(3, 12), 'all'), (25, 5, 2, range(5, 13), 'rand'),
                              (125, 5, 3, range(5, 13), 'rand'), (49, 7, 2, range(7, 14), 'rand'), (11, 11, 1, range(11, 14), 'rand'),
                              (121, 11, 2, range(11, 14), 'rand')]:
        for m in ms:
            E = signs(m)
            if mode == 'all':
                Bs = [[0] + list(t) for t in itertools.combinations_with_replacement(range(n), m - 1)]
            else:
                Bs = []
                for _ in range(250):
                    st = rnd.randint(0, 4)
                    if st == 0:
                        B = [rnd.randrange(n) for _ in range(m)]
                    elif st == 1:
                        lvl = rnd.randint(1, a); full = [t * q ** (lvl - 1) for t in range(q)]
                        B = full + [full[0]] * (m - q)
                    elif st == 2:
                        lvl = rnd.randint(1, a); full = [t * q ** (lvl - 1) for t in range(q)]
                        B = full + [rnd.choice(full) for _ in range(m - q)]
                    elif st == 3 and a >= 2 and m >= 2 * q - 1:
                        B = list(range(q)) + [q * t for t in range(1, q)] + [rnd.choice([0, 1, q]) for _ in range(m - 2 * q + 1)]
                    else:
                        full = [t + q * rnd.randrange(n // q) for t in range(q)]; B = full + [rnd.choice(full) for _ in range(m - q)]
                    Bs.append([b % n for b in B][:m])
            L = (m - 1) // (q - 1)
            lev = cc(m - q + 1) / 2 ** (q - 2) if m >= q else Fr(0)
            tail = sum(Fr(1, 2 ** (l * (q - 1))) for l in range(2, L + 1))
            if m % 2:
                bound = lev + tail
            else:
                bound = cc(m) + (R_pattern(q, m) if m >= q else 0) + tail
            worst = Fr(0); worstlev = Fr(0)
            for B in Bs:
                bad = bad_at(n, B, 1, E)
                for j in range(1, a + 1):
                    bj = bad_at(n, B, q ** j, E)
                    if m % 2:
                        assert share(bj) <= lev, ("Lemma V", n, B, j)
                    worstlev = max(worstlev, share(bj))
                    bad = bad | bj
                s = share(bad)
                assert s <= bound, ("Theorem P", n, B, s, bound)
                assert m < 3 or s <= Fr(3, 8)
                worst = max(worst, s)
            ex = ""
            if m % 2 and q <= m <= 2 * q - 3 and mode == 'all':
                ex = f"; exact value claimed: equal {worst == lev}"
            print(f"Z_{n} m={m}: {len(Bs)} multisets ({mode}); largest bad share {worst}; bound of Theorem P {bound}; largest single level {worstlev}{ex}", flush=True)
    print("Lemma V and Theorem P: no failure")


if __name__ == '__main__':
    if sys.argv[1] == 'examples':
        examples()
    elif sys.argv[1] == 'exhaust':
        exhaust(int(sys.argv[2]), int(sys.argv[3]))
    elif sys.argv[1] == 'chain':
        chain(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), [int(x) for x in sys.argv[6:]])
    elif sys.argv[1] == 'pp':
        pp()
