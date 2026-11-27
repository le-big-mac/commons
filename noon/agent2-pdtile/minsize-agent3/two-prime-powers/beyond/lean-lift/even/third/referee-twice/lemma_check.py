"""Referee's checks of the steps that Corollaries 2 and 3 of theorem-twice.md take from even-result-2.md, section 1.

A. The translation used in Corollary 3 (Lemma S3 for p = 2) and in Corollary 2, signing by signing, by two routes:
     route 1: "3-bad at 2^j e''" / "bad at 2^j e" from the remainder modulo Phi_d (cyc_check.py);
     route 2: "level j bad" of Theorem T, by the literal routine of t_check.py, for the valued family with
              position b mod 2^k and value (X^b mod Phi_e'') in (Z/3)^phi(e'')  [resp. in Z^phi(e)].
B. Lemma L3 (a), (b), (c) as stated, on multisets built to have live levels (also several live levels of one
   prime, and two primes): step-down, level bound, the union in (c), and the SUM of the shares at the live e' > 1
   against sum 2^(-mu(e'*)) and against W(no 3).
C. A few least shares recomputed by route 2.
"""
import itertools, math, random, sys, time
from fractions import Fraction
import numpy as np
import cyc_check as cc
import t_check as tc

def int_table(d, N):
    return np.rint(cc.pow_table(d, N)).astype(np.int64)

def level_flags_literal(k, fam, mods):
    """list over all signings (first sign +) of the tuple (level 0 bad, ..., level k bad), literal definition"""
    m = len(fam)
    zero = tuple(0 for _ in mods)
    out = []
    for rest in itertools.product((1, -1), repeat=m - 1):
        signs = (1,) + rest
        def sigma(idx):
            s = zero
            for i in idx:
                s = tc.vadd(s, tc.vscale(signs[i], fam[i][1], mods), mods)
            return s
        fl = [sigma(range(m)) == zero]
        for j in range(1, k + 1):
            classes = {}
            for i, (u, v) in enumerate(fam):
                classes.setdefault(u % (1 << (j - 1)), []).append(i)
            ok = True
            for res, idx in classes.items():
                h = [i for i in idx if fam[i][0] % (1 << j) == res]
                h2 = [i for i in idx if fam[i][0] % (1 << j) != res]
                if sigma(h) != sigma(h2):
                    ok = False
            fl.append(ok)
        out.append(tuple(fl))
    return out

def part_A(N, count, mmax, seed):
    ctx = cc.Ctx(N)
    rng = random.Random(seed)
    k = ctx.k
    tabs = {e: int_table(e, N) for e in cc.divisors(ctx.nodd)}
    n_cmp3 = n_cmp0 = bad_cmp = 0
    for _ in range(count):
        m = rng.randint(2, mmax)
        style = rng.randrange(3)
        if style == 0:
            B = [0] + [rng.randrange(N) for _ in range(m - 1)]
        elif style == 1:
            B = [0] + [rng.choice([0, N // 2, N // 4, 3 * N // 4, ctx.nodd, 2 * ctx.nodd % N]) for _ in range(m - 1)]
        else:
            base = [rng.randrange(N) for _ in range(3)]
            B = [0] + [rng.choice(base) for _ in range(m - 1)]
        Barr = np.array([B], dtype=np.int64)
        bad, bad3 = ctx.flags(Barr)
        for e in cc.divisors(ctx.nodd):
            phi = tabs[e].shape[1]
            # characteristic 0, V = Z^phi(e)
            fam = [(b % (1 << k), tuple(int(x) for x in tabs[e][b])) for b in B]
            lit = level_flags_literal(k, fam, (0,) * phi)
            for j in range(k + 1):
                r1 = bad[2 ** j * e][0]
                r2 = np.array([f[j] for f in lit])
                n_cmp0 += len(r2)
                bad_cmp += int((r1 != r2).sum())
            if ctx.n2 % e == 0:      # e'' prime to 6: V = (Z/3)^phi
                lit = level_flags_literal(k, fam, (3,) * phi)
                for j in range(k + 1):
                    r1 = bad3[2 ** j * e][0]
                    r2 = np.array([f[j] for f in lit])
                    n_cmp3 += len(r2)
                    bad_cmp += int((r1 != r2).sum())
    print(f"A. Z_{N}: {count} multisets of 2..{mmax} elements; comparisons (signing, level, e): modulo 3: {n_cmp3}, "
          f"characteristic 0: {n_cmp0}; disagreements: {bad_cmp}", flush=True)

# ---------------------------------------------------------------- part B

def factor(n):
    f = {}
    q = 2
    while n > 1:
        while n % q == 0:
            f[q] = f.get(q, 0) + 1; n //= q
        q += 1
    return f

def tree(B, q, imax):
    """for i = 1..imax: (live?, sum over occupied groups D at level i of min(k_D, q-1))"""
    res = {}
    for i in range(1, imax + 1):
        groups = {}
        for b in set(B):
            groups.setdefault(b % q ** (i - 1), set()).add(b % q ** i)
        live = any(len(s) == q for s in groups.values())
        res[i] = (live, sum(min(len(s), q - 1) for s in groups.values()))
    return res

def gen_live(N, rng, m):
    ctx_f = factor(N)
    odd_primes = [q for q in ctx_f if q >= 5]
    B = [0]
    tries = 0
    while len(B) < m and tries < 50:
        tries += 1
        if odd_primes and rng.random() < .8:
            q = rng.choice(odd_primes)
            i = rng.randint(1, ctx_f[q])
            if len(B) + q - 1 > m:
                continue
            x = rng.choice(B)
            for t in range(1, q):
                B.append((x + t * q ** (i - 1) + q ** i * rng.randrange(N // q ** i)) % N)
        else:
            B.append(rng.choice(B) if rng.random() < .5 else rng.randrange(N))
    while len(B) < m:
        B.append(rng.choice(B) if rng.random() < .5 else rng.randrange(N))
    return B[:m]

W_NO3 = 0.118564698205556

def part_B(N, count, mlo, mhi, seed):
    ctx = cc.Ctx(N)
    assert ctx.a == 0
    rng = random.Random(seed)
    fN = factor(N)
    k = ctx.k
    n_a = n_a_applied = fail_a = n_b = fail_b = fail_b2 = n_c = fail_c = fail_csum = fail_cW = 0
    n_live_e = 0; max_sum = Fraction(0); tight_b = 0; max_live_levels = 0; two_primes_live = 0
    for _ in range(count):
        m = rng.randint(mlo, mhi)
        B = gen_live(N, rng, m)
        S = 1 << (m - 1)
        bad, bad3 = ctx.flags(np.array([B], dtype=np.int64))
        bad3 = {d: v[0] for d, v in bad3.items()}
        trees = {q: tree(B, q, fN[q]) for q in fN}
        livelv = {q: [i for i in range(1, fN[q] + 1) if trees[q][i][0]] for q in fN}
        max_live_levels = max(max_live_levels, max((len(livelv[q]) for q in fN if q >= 5), default=0))
        if sum(1 for q in fN if q >= 5 and livelv[q]) >= 2:
            two_primes_live += 1
        # (a), (b): every d | n_3, every prime q = 2 or q >= 5 of d
        for d in cc.divisors(N):
            for q, i in factor(d).items():
                live, ssum = trees[q][i]
                n_b += 1
                cnt = int(bad3[d].sum())
                if Fraction(cnt, S) > Fraction(1, 2 ** ssum):
                    fail_b += 1
                if Fraction(cnt, S) == Fraction(1, 2 ** ssum):
                    tight_b += 1
                if live:
                    l = livelv[q].index(i) + 1
                    if Fraction(cnt, S) > Fraction(1, 2 ** (l * (q - 1))):
                        fail_b2 += 1
                else:
                    n_a += 1
                    n_a_applied += cnt
                    if (bad3[d] & ~bad3[d // q]).any():
                        fail_a += 1
        # (c)
        def is_live(e):
            return e > 1 and all(trees[q][i][0] for q, i in factor(e).items())
        def mu_star(e):
            return max((livelv[q].index(i) + 1) * (q - 1) for q, i in factor(e).items())
        live_es = [e for e in cc.divisors(ctx.n2) if is_live(e)]
        n_live_e += len(live_es)
        for j in range(k + 1):
            c = 2 ** j
            second = np.zeros(S, dtype=bool)
            for e in live_es:
                second |= bad3[c * e]
            for e in cc.divisors(ctx.n2):
                n_c += 1
                if (bad3[c * e] & ~bad3[c] & ~second).any():
                    fail_c += 1
            tot = sum(Fraction(int(bad3[c * e].sum()), S) for e in live_es)
            bound = sum(Fraction(1, 2 ** mu_star(e)) for e in live_es)
            max_sum = max(max_sum, tot)
            if tot > bound:
                fail_csum += 1
            if float(bound) > W_NO3:
                fail_cW += 1
    print(f"B. Z_{N}: {count} multisets of {mlo}..{mhi} elements built with live levels "
          f"(live e' > 1 in all: {n_live_e}; most live levels of one prime: {max_live_levels}; two primes live in {two_primes_live} multisets)")
    print(f"   (a) step-down: {n_a} cases (d, q) with level not live, {n_a_applied} signings 3-bad at d in them; failures {fail_a}")
    print(f"   (b) level bound: {n_b} cases (d, q); share > 2^(-sum min(k_D, q-1)): {fail_b} (equal in {tight_b}); share > 2^(-l(q-1)) at the l-th live level: {fail_b2}")
    print(f"   (c) union: {n_c} cases (c, e''); failures {fail_c}; sum of the shares at the live e' > 1 above sum 2^(-mu(e'*)): {fail_csum}; "
          f"sum 2^(-mu(e'*)) above W(no 3): {fail_cW}; largest sum of shares seen: {max_sum} = {float(max_sum):.5f}", flush=True)

def part_C():
    for N, B in ((20, [0, 0, 0, 1]), (20, [0, 1, 2, 4, 13]), (20, [0, 0, 1, 2, 4, 13]), (20, [0, 0, 0, 1, 2, 4, 13]),
                 (20, [0, 0, 0, 0, 1, 2, 4, 13]), (80, [0, 37, 13, 56, 42, 42, 4]), (28, [0, 1, 2, 4, 5, 13, 17]),
                 (120, [0, 36, 41, 51, 27, 111, 43, 39])):
        ctx = cc.Ctx(N)
        k = ctx.k
        m = len(B)
        anybad = None
        for e in cc.divisors(ctx.n2):
            T = int_table(e, N)
            fam = [(b % (1 << k), tuple(int(x) for x in T[b])) for b in B]
            lit = level_flags_literal(k, fam, (3,) * T.shape[1])
            a = np.array([any(f) for f in lit])
            anybad = a if anybad is None else (anybad | a)
        share2 = Fraction(int((~anybad).sum()), len(anybad))
        bad, bad3 = ctx.flags(np.array([B], dtype=np.int64))
        any3 = np.zeros(1 << (m - 1), dtype=bool)
        for d in bad3: any3 |= bad3[d][0]
        share1 = Fraction(int((~any3).sum()), 1 << (m - 1))
        print(f"C. Z_{N}, {B}: share of 3-good signings by remainders {share1}, by levels over e'' | {ctx.n2}: {share2}"
              + ("" if share1 == share2 else "  DISAGREE"), flush=True)

if __name__ == '__main__':
    what = sys.argv[1]
    if what == 'A':
        for N, cnt, mm in ((20, 150, 7), (40, 120, 7), (100, 60, 6), (140, 50, 6), (56, 80, 7), (60, 80, 7), (120, 50, 6), (36, 80, 7)):
            part_A(N, cnt, mm, 100 + N)
    elif what == 'B':
        for N, cnt, lo, hi in ((20, 400, 5, 11), (100, 400, 5, 12), (140, 400, 5, 12), (200, 300, 5, 12), (700, 150, 5, 12), (175, 300, 5, 12), (56, 300, 7, 11), (1100, 60, 5, 12)):
            part_B(N, cnt, lo, hi, 200 + N)
    elif what == 'C':
        part_C()
