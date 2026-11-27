"""Tests of the lemmas of even-result.md, exact arithmetic (lib.py).  usage: tests1.py sets|recursion|pairs|m34|closed"""
import sys, itertools, random
import numpy as np
from lib import *

def v2n(x, n):
    """2-adic valuation of x as a residue modulo n = 2^k n', capped at k (x = 0 mod 2^k gives k)"""
    k, _ = two_part(n); x %= 2 ** k
    if x == 0: return k
    v = 0
    while x % 2 == 0: x //= 2; v += 1
    return v

def t_sets():
    """Lemma S: (1) 2X^x good; (2) 3X^a +- X^b good; (3) O = {a,b} exceptional, c another element:
    X^a + X^b + 2X^c good if u >= v, X^a - X^b - 2X^c good if u < v (u = v2(a-c), v = v2(a-b))."""
    tot = 0
    for n in range(2, 62, 2):
        k, _ = two_part(n)
        for a in [0]:
            for b in range(1, n):
                if (a - b) % 2 ** k == 0: continue          # not an exceptional pair
                for s in (1, -1):
                    c = np.zeros(n, dtype=np.int64); c[a] = 3; c[b] = s; assert is_good(c, n); tot += 1
                    c = np.zeros(n, dtype=np.int64); c[b] = 3; c[a] = s; assert is_good(c, n); tot += 1
                for cc in range(n):
                    if cc in (a, b): continue
                    u, v = v2n(a - cc, n), v2n(a - b, n)
                    m = np.zeros(n, dtype=np.int64)
                    if u >= v: m[a] = 1; m[b] = 1; m[cc] = 2
                    else:      m[a] = 1; m[b] = -1; m[cc] = -2
                    assert is_good(m, n), (n, a, b, cc); tot += 1
                    # and the other choice does fail somewhere in the complementary case, as the proof says it may:
        m = np.zeros(n, dtype=np.int64); m[0] = 2; assert is_good(m, n)
    print('Lemma S: constructions good in all', tot, 'cases, even n <= 60')
    # brute force: multisets (with multiplicities) on small even n: has a good signing iff not an exceptional pair
    cnt = 0
    for n, M in ((2, 9), (4, 7), (6, 6), (8, 5), (10, 5), (12, 5)):
        for m in range(1, M + 1):
            for rest in itertools.combinations_with_replacement(range(n), m - 1):
                els = [0] + list(rest)
                _, g = good_signings(n, els)
                assert g.any() != exceptional_pair(n, els), (n, els); cnt += 1
    print('Conjecture E by brute force on', cnt, 'multisets containing 0 (n = 2..12): holds')

def split(n, els, signs):
    """E, D with their signs: multisets on Z_{n/2}"""
    E = [(x // 2, s) for x, s in zip(els, signs) if x % 2 == 0]
    D = [((x - 1) // 2, s) for x, s in zip(els, signs) if x % 2 == 1]
    return E, D

def t_recursion():
    """Lemma R: S good on Z_n (n even, N = n/2, n' odd part)  iff
       (a) for every odd e | n: S_E(X) + X^h S_D(X) and S_E(X) - X^h S_D(X) are not divisible by Phi_e, where
           h = (n'+1)/2 modulo n' and h = 0 modulo 2^(k-1)  [as masks on Z_N], and
       (b) for no even d | N both S_E and S_D are divisible by Phi_d."""
    random.seed(3); cnt = 0; nbad = 0
    for n in (2, 4, 6, 8, 10, 12, 18, 20, 24, 30, 36, 40, 42, 48, 60, 72):
        N = n // 2; k, n1 = two_part(n)
        # h: 2h = 1 mod n', h = 0 mod 2^(k-1)
        h = next(t for t in range(N) if (2 * t - 1) % n1 == 0 and t % 2 ** (k - 1) == 0)
        for _ in range(4000):
            m = random.randint(1, 7)
            if random.random() < 0.5: els = [random.randrange(n) for _ in range(m)]
            else:
                step = random.choice([d for d in divisors(n) if d > 1]); els = [(random.randrange(n // step) * step + random.choice((0, 0, 1))) % n for _ in range(m)]
            sg = [random.choice((1, -1)) for _ in range(m)]
            E, D = split(n, els, sg)
            cE = mask(N, [x for x, _ in E], [s for _, s in E]); cD = mask(N, [x for x, _ in D], [s for _, s in D])
            cDh = np.roll(cD, h)
            bp = set(bad_levels(cE + cDh, N)); bm = set(bad_levels(cE - cDh, N))
            a_ok = not any(e % 2 == 1 for e in bp | bm)
            bE = set(bad_levels(cE, N)); bD = set(bad_levels(cD, N))
            b_ok = not any(d % 2 == 0 for d in bE & bD)
            g = is_good(mask(n, els, sg), n)
            assert g == (a_ok and b_ok), (n, els, sg)
            # finer: the levels themselves
            bl = set(bad_levels(mask(n, els, sg), n))
            pred = set()
            for e in divisors(n1):
                # level e of S <-> S_E(theta) = -eta S_D(theta);  level 2e <-> S_E(theta) = +eta S_D(theta)
                if e in bp: pred.add(e)
                if e in bm: pred.add(2 * e)
            for d in bE & bD:
                if d % 2 == 0: pred.add(2 * d)
            assert bl == pred, (n, els, sg, bl, pred)
            cnt += 1; nbad += (not g)
    print(f'Lemma R: {cnt} random signed multisets on 16 even moduli: the bad levels of S are exactly those predicted ({nbad} of them bad somewhere)')

def t_pairs():
    """Both halves exceptional pairs: E = {x,y}, D = {z,w} on Z_N, v2(x-y), v2(z-w) < k-1... the signing of the proof is good."""
    cnt = 0
    for n in (8, 12, 16, 20, 24, 28, 36, 40, 48, 56, 60, 72, 80, 96):
        N = n // 2; k, n1 = two_part(n); K = 2 ** (k - 1)
        for x, y in itertools.combinations(range(N), 2):
            if (x - y) % K == 0: continue
            if x != 0: continue
            for z, w in itertools.combinations(range(N), 2):
                if (z - w) % K == 0: continue
                vE, vD = v2n(x - y, N), v2n(z - w, N)
                els = [2 * x, 2 * y, 2 * z + 1, 2 * w + 1]
                sg = [1, -1, 1, 1] if vD >= vE else [1, 1, 1, -1]
                assert is_good(mask(n, els, sg), n), (n, els, sg); cnt += 1
                # and the two signings with equal patterns are always bad (at level 1 or 2 of e = 1)
                assert not is_good(mask(n, els, [1, 1, 1, 1]), n) and not is_good(mask(n, els, [1, -1, 1, -1]), n)
    print('two exceptional halves:', cnt, 'four-element sets on 14 moduli: the signing of the proof is good')

def t_m34():
    """Theorem B: m = 3: at most 2 of the 4 signings (first sign +) are bad; m = 4: a signing is good on Z_n iff it is
    good for the residues modulo 2^k on Z_{2^k}."""
    c3 = c4 = 0; worst3 = 0
    for n in list(range(2, 50, 2)) + [54, 60, 72, 84, 90, 96, 120]:
        k, n1 = two_part(n); q = 2 ** k
        for rest in itertools.combinations_with_replacement(range(n), 2):
            els = [0] + list(rest)
            if len(set(els)) < 3: continue
            _, g = good_signings(n, els); nb = int((~g).sum()); worst3 = max(worst3, nb)
            assert nb <= 2; c3 += 1
        lim = 3 if n <= 60 else 2
        it = itertools.combinations_with_replacement(range(n), 3) if n <= 60 else ((random.randrange(n), random.randrange(n), random.randrange(n)) for _ in range(20000))
        for rest in it:
            els = [0] + list(rest)
            sg, g = good_signings(n, els)
            sg2, g2 = good_signings(q, [x % q for x in els])
            assert (g == g2).all(), (n, els); c4 += 1
    print(f'Theorem B: m = 3: {c3} three-element sets containing 0, at most {worst3} of the 4 signings bad;  m = 4: {c4} multisets, good on Z_n iff good modulo 2^k')

def t_closed():
    """B closed under x -> x + N (N = n/2), B = G + {0, N}: with signs equal on the fibres over G_plus and opposite on
    G_minus: S = 2 S_{G+} modulo X^N - 1 and 2 S_{G-} modulo X^N + 1."""
    random.seed(5); cnt = 0
    for n in (4, 8, 12, 16, 20, 24, 36, 40, 48, 60):
        N = n // 2
        for _ in range(1500):
            r = random.randint(2, min(N, 6)); G = random.sample(range(N), r)
            # choose G_minus = one element g such that G - g is not an exceptional pair on Z_N, else two elements
            choice = None
            for g in G:
                rest = [x for x in G if x != g]
                if not exceptional_pair(N, rest) or N % 2 == 1: choice = [g]; break
            if choice is None: choice = G[:2]
            Gp = [x for x in G if x not in choice]
            sgs, good = good_signings(N, Gp)
            assert good.any()
            sp = sgs[np.argmax(good)]
            els = []; sg = []
            for x, s in zip(Gp, sp): els += [x, x + N]; sg += [int(s), int(s)]
            for x in choice: els += [x, x + N]; sg += [1, -1]
            assert is_good(mask(n, els, sg), n), (n, els, sg); cnt += 1
    print('closed under +n/2:', cnt, 'random sets: the signing built from a good signing of G_plus is good')

if __name__ == '__main__':
    {'sets': t_sets, 'recursion': t_recursion, 'pairs': t_pairs, 'm34': t_m34, 'closed': t_closed}[sys.argv[1]]()
