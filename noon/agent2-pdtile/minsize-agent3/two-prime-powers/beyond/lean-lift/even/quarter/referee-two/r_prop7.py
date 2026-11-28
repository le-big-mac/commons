#!/usr/bin/env python3
"""Referee's test of Proposition 7 of result.md on random trees of one prime, exact counts by a recursion over the
tree (all signings are counted, none enumerated).  For every tree: for every live level i, of rank j, the share of
"bad at p^i and not at 1" against (1) prod e(D_k), (2) sum_k delta(D_k) prod_{l != k} e(D_l) for the actual groups,
(3) last_p(j, m), (4) nonlast_p(j, m) when every class at depth i has at least two elements; the share of "bad at
some p^i, i >= 1, not at 1" against PP_p(m) and against the exact U_p(m) where the text has it.

usage: r_prop7.py p mlo mhi count seed
"""
import sys, random
from math import comb
from fractions import Fraction as F
import r_tables as RT


def gen(r, a, p, rnd, style):
    if a == 0:
        return r
    if r == 1 or rnd.random() < 0.15:
        return [gen(r, a - 1, p, rnd, style)]
    k = rnd.randint(2, p) if rnd.random() < 0.3 else p
    k = min(k, r)
    if style == 0:
        cuts = sorted(rnd.sample(range(1, r), k - 1)); parts = [b - a_ for a_, b in zip([0] + cuts, cuts + [r])]
    elif style == 1:                      # one heavy class, the others small
        parts = [1] * k; parts[0] = r - (k - 1)
    else:                                  # even sizes where possible
        parts = [2] * k
        if 2 * k > r:
            parts = [1] * k; parts[0] = r - (k - 1)
        else:
            left = r - 2 * k
            while left >= 2:
                parts[rnd.randrange(k)] += 2; left -= 2
            parts[0] += left
    return [gen(x, a - 1, p, rnd, rnd.choice([style, rnd.randrange(3)])) for x in parts]


def size(node):
    return node if isinstance(node, int) else sum(size(ch) for ch in node)


def dist(node, a, p):
    """{(s, L): count}; bit i-1 of L: every group at relative level i of the subtree is flat"""
    if a == 0:
        r = node
        return {(s, 0): comb(r, (r + s) // 2) for s in range(-r, r + 1, 2)}
    kids = [dist(ch, a - 1, p) for ch in node]
    k = len(kids)
    cur = {(0, (1 << (a - 1)) - 1, None): 1}
    for d in kids:
        new = {}
        for (s, mk, cv), cnt in cur.items():
            for (s2, L2), c2 in d.items():
                ncv = s2 if cv is None else (cv if cv == s2 else 'N')
                kk = (s + s2, mk & L2, ncv)
                new[kk] = new.get(kk, 0) + cnt * c2
        cur = new
    res = {}
    for (s, mk, cv), cnt in cur.items():
        flat = cv != 'N' and (k == p or cv == 0)
        kk = (s, (mk << 1) | (1 if flat else 0))
        res[kk] = res.get(kk, 0) + cnt
    return res


def groups_at(node, a, level, out):
    """groups at absolute level `level` below this node (which is `level - 1` steps above the group's class)"""
    if level == 1:
        out.append([size(ch) for ch in node])
    else:
        for ch in node:
            groups_at(ch, a - 1, level - 1, out)


def last_nonlast(p, m):
    kmax = m // 2
    last, non = [], []
    j = 1
    while 1 + (j - 1) * (p - 1) <= kmax:
        G = 1 + (j - 1) * (p - 1)
        last.append(min(max(RT.Emax(p, k, m, True, 1) for k in range(G, kmax + 1)), max(RT.Vmax(p, k, m, 1) for k in range(G, kmax + 1))))
        non.append(min(max(RT.Emax(p, k, m, True, 2) for k in range(G, kmax + 1)), max(RT.Vmax(p, k, m, 2) for k in range(G, kmax + 1))))
        j += 1
    return last, non


def main():
    p, mlo, mhi, count, seed = (int(x) for x in sys.argv[1:6])
    rnd = random.Random(seed)
    for m in range(mlo, mhi + 1):
        a = min((m - 1) // (p - 1), 6)
        last, non = last_nonlast(p, m)
        pp = RT.PP(p, m)
        uex = F(RT.U_TEXT[p][m]) if (p in RT.U_TEXT and m in RT.U_TEXT[p]) else None
        nf = 0; best = F(0); nlev = 0; eq_last = 0; nbig = 0
        for it in range(count):
            t = gen(m, a, p, rnd, rnd.randrange(3))
            d = dist(t, a, p)
            assert sum(d.values()) == 2 ** m
            live = []
            for i in range(1, a + 1):
                gs = []; groups_at(t, a, i, gs)
                if any(len(g) == p for g in gs):
                    live.append(i)
                    j = len(live)
                    sh = F(sum(c for (s, L), c in d.items() if s != 0 and (L >> (i - 1)) & 1), 2 ** m)
                    nlev += 1
                    e = [RT.ef_df(p, sum(g), 1)[0] if len(g) == p else RT.enf(sum(g)) for g in gs]
                    dl = [RT.ef_df(p, sum(g), 1)[1] if len(g) == p else F(0) for g in gs]
                    pr = F(1)
                    for x in e:
                        pr *= x
                    sm = F(0)
                    for k_ in range(len(gs)):
                        t_ = dl[k_]
                        for l_ in range(len(gs)):
                            if l_ != k_:
                                t_ *= e[l_]
                        sm += t_
                    bad = False
                    if len(gs) < 1 + (j - 1) * (p - 1): bad = True
                    if sh > pr or sh > sm: bad = True
                    lastj = last[j - 1] if j <= len(last) else F(0)   # more groups than m elements allow: the bound is 0
                    nonj = non[j - 1] if j <= len(non) else F(0)
                    if sh > lastj: bad = True
                    if sh == lastj and sh > 0: eq_last += 1
                    if all(x >= 2 for g in gs for x in g):
                        nbig += 1
                        if sh > nonj: bad = True
                    if bad:
                        nf += 1
                        if nf <= 3: print("  FAILURE level", m, t, i, j, sh, pr, sm)
            u = F(sum(c for (s, L), c in d.items() if s != 0 and L), 2 ** m)
            best = max(best, u)
            if u > pp or (uex is not None and u > uex):
                nf += 1
                if nf <= 3: print("  FAILURE U", m, t, u, pp, uex)
        print("p=%d m=%d depth<=%d trees=%d live levels tested=%d (classes all >= 2: %d; equal to last: %d)  largest U-share met=%s = %.5f  PP=%.5f  exact U=%s  failures=%d" % (
            p, m, a, count, nlev, nbig, eq_last, best, float(best), float(pp), uex, nf), flush=True)


if __name__ == '__main__':
    main()
