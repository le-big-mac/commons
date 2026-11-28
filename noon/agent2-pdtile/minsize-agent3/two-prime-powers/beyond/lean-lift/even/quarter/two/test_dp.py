#!/usr/bin/env python3
"""Two tests of the programs behind Theorem A.

(a) COMP(m): the composite sum of lo_union2.py (computed there by a sorting formula) against a plain enumeration of
    all tuples (j_p), for m = 3..MB; the values are read from lo2_exact_46.out.
(b) PP_p(m) by the bound of section 5 (used for m >= 17) against exact values on random trees of class sizes:
    for random p-trees with m elements the exact share of "bad at some p^i, i >= 1, and not at 1" (all signings, by
    the distributions of ptree.py) must be <= PP_p(m).

usage: test_dp.py MB  p MLO MHI COUNT SEED
"""
import sys, random, itertools, os, re
from fractions import Fraction
from math import comb
import lo_union2 as L

HERE = os.path.dirname(os.path.abspath(__file__))


def comp_brute(m, T, gen):
    zero = T.zero
    BF, ranks = {}, {}
    for p in L.primes_upto(m):
        Gmax, bf = gen[p]
        B = L.suffix_max(bf, Gmax, m, zero)
        BF[p] = B
        g = []
        j = 1
        while 1 + (j - 1) * (p - 1) <= Gmax and B[1 + (j - 1) * (p - 1)] > 0:
            g.append(1 + (j - 1) * (p - 1)); j += 1
        ranks[p] = g
    ps = sorted(ranks)
    total = zero
    ntuples = 0
    for tup in itertools.product(*[range(len(ranks[p]) + 1) for p in ps]):
        supp = [(p, j) for p, j in zip(ps, tup) if j > 0]
        if len(supp) < 2:
            continue
        G = max(ranks[p][j - 1] for p, j in supp)
        total += min(BF[p][G] if G < len(BF[p]) else zero for p, j in supp)
        ntuples += 1
    return total, ntuples


def pp_dp(p, m, T, Gmax, intl, intb):
    zero = T.zero
    Ef, Vf = intl
    Eb, Vb = intb
    sE, sV = L.suffix_max(Ef, Gmax, m, zero), L.suffix_max(Vf, Gmax, m, zero)
    bE, bV = L.suffix_max(Eb, Gmax, m, zero), L.suffix_max(Vb, Gmax, m, zero)
    val = zero; acc = zero
    j = 1
    while 1 + (j - 1) * (p - 1) <= Gmax:
        G = 1 + (j - 1) * (p - 1)
        val = max(val, acc + min(sE[G], sV[G]))
        acc += min(bE[G], bV[G])
        j += 1
    return val


def random_tree_dist(rng, p, r, a):
    """distribution {(s, mask): count} of a random tree with r elements and depth a (as in ptree.py)"""
    if a == 0:
        return {(s, 0): comb(r, (r + s) // 2) for s in range(-r, r + 1, 2)}
    # random split into at most p parts
    style = rng.randrange(4)
    if r == 1 or style == 0 and rng.random() < 0.5:
        parts = [r]
    else:
        k = rng.randint(1, min(p, r))
        if style == 1:      # singles and one heavy
            parts = [1] * (k - 1) + [r - (k - 1)]
        elif style == 2:    # as even as possible, in pairs
            parts = []
            left = r
            for i in range(k - 1):
                x = max(1, min(left - (k - 1 - i), 2 * rng.randint(1, max(1, r // (2 * k) + 1))))
                parts.append(x); left -= x
            parts.append(left)
        else:
            cuts = sorted(rng.sample(range(1, r), k - 1)) if k > 1 else []
            parts = [b - a_ for a_, b in zip([0] + cuts, cuts + [r])]
        parts = [x for x in parts if x > 0]
    k = len(parts)
    cur = {(0, (1 << (a - 1)) - 1, None, True): 1}
    for sz in parts:
        d = random_tree_dist(rng, p, sz, a - 1)
        nxt = {}
        for (s, mk, cv, eq), cnt in cur.items():
            for (s2, mk2), cnt2 in d.items():
                if cv is None:
                    ncv, neq = s2, True
                else:
                    ncv, neq = cv, (eq and s2 == cv)
                key = (s + s2, mk & mk2, ncv, neq)
                nxt[key] = nxt.get(key, 0) + cnt * cnt2
        cur = nxt
    res = {}
    for (s, mk, cv, eq), cnt in cur.items():
        flat = eq and (k == p or cv == 0)
        key = (s, (mk << 1) | (1 if flat else 0))
        res[key] = res.get(key, 0) + cnt
    return res


def main():
    MB = int(sys.argv[1])
    p, mlo, mhi, count, seed = (int(x) for x in sys.argv[2:7])
    Rmax = max(MB, mhi)
    T = L.Tab(Rmax, True)
    # (a)
    gen = {}
    T2 = L.Tab(MB, True)      # the tables of the run to 46 are larger; the values at m <= MB are the same
    for q in L.primes_upto(MB):
        Gmax = max(1, (MB - q) // 2 + 1)
        vnf, vf = L.general_tables(q, T2)
        _, bf = L.level_dp(vnf, vf, Gmax, MB, T2.zero)
        gen[q] = (Gmax, bf)
    comp_file = {}
    for line in open(os.path.join(HERE, 'lo2_exact_46.out')):
        f = [x.strip() for x in line.split('|')]
        if len(f) >= 5 and f[0].isdigit():
            comp_file[int(f[0])] = Fraction(f[3])
    nt = 0
    for m in range(3, MB + 1):
        b, k = comp_brute(m, T2, gen)
        assert b == comp_file[m], ("COMP", m, b, comp_file[m])
        nt += k
    print("(a) COMP(m) by enumeration of %d tuples equals the value of lo2_exact_46.out for every m = 3..%d" % (nt, MB))
    # (b)
    rng = random.Random(seed)
    for m in range(mlo, mhi + 1):
        Tm = L.Tab(m, True)
        Gmax = max(1, (m - p) // 2 + 1)
        intl = L.integer_level(p, Tm, False, Gmax)
        intb = L.integer_level(p, Tm, True, Gmax)
        bound = pp_dp(p, m, Tm, Gmax, intl, intb)
        a = (m - 1) // (p - 1)
        worst = Fraction(0)
        for _ in range(count):
            depth = rng.randint(1, a)
            d = random_tree_dist(rng, p, m, depth)
            new = sum(cnt for (s, mk), cnt in d.items() if s != 0 and mk)
            sh = Fraction(new, 2 ** m)
            assert sh <= bound, ("PP", p, m, sh, bound)
            worst = max(worst, sh)
        print("(b) p=%d m=%d: %d random trees, largest exact share %s = %.5f <= PP_p(m) = %.5f" % (
            p, m, count, worst, float(worst), float(bound)), flush=True)


if __name__ == '__main__':
    main()
