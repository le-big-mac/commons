# Referee's test of Corollary U (with the term #G) and of the bullets of its proof.
# Written from the statement of the note; imports nothing of the author's.  Exact integers.
#
# usage: coru.py n m [all|zero] [seconds]
#   all  : every multiset of m elements of Z_n
#   zero : every multiset of m elements of Z_n that contains 0 (translation changes none of the counts:
#          the signed mask is multiplied by a unit X^t; compared with "all" on small n)
# For every multiset and every one of the 2^m signings (sign i on element i):
#   badn : Phi_d | S for some d | n            (remainder of S modulo Phi_d, integer coefficients)
#   bado : Phi_e | S' for some e | n'          (S' the signed mask of the reduction modulo n')
#   G    : for some e | n', for every class r modulo 2^k, the signed mask of the elements = r (mod 2^k)
#          has remainder 0 modulo Phi_e
# and, to check the bullets of the proof, for j = 1..k, e | n':
#   lev[j][e] : every class modulo 2^(j-1) is balanced at level j for the values eta_e^b
#               (remainder modulo Phi_e of  sum over one half  -  sum over the other half  is 0)
#   F[d][e]   : every class modulo 2^d has sigma = 0 for the values eta_e^b
import sys, time, itertools
import numpy as np
from cyc import divisors, v2, xpow_mod, phi_divides_ramanujan

def build(n):
    k = v2(n)
    n1 = n >> k
    dn, do = divisors(n), divisors(n1)
    rows_n = {d: np.array(xpow_mod(d, n), dtype=np.int64).reshape(n, -1) for d in dn}
    cols, blocks = [], []          # blocks: (label, start, stop)
    def add(label, mat):
        start = sum(c.shape[1] for c in cols)
        cols.append(mat)
        blocks.append((label, start, start + mat.shape[1]))
    b = np.arange(n)
    for d in dn:                                    # bad on Z_n at d
        add(("A", d), rows_n[d])
    for e in do:                                    # bad on Z_n' at e, computed from B' = B mod n'
        r1 = np.array(xpow_mod(e, n1), dtype=np.int64).reshape(n1, -1)
        add(("O", e), r1[b % n1])
    for j in range(1, k + 1):                       # level j for e, one block per class r modulo 2^(j-1)
        for e in do:
            for r in range(2 ** (j - 1)):
                sgn = np.where(b % 2 ** j == r, 1, np.where(b % 2 ** j == r + 2 ** (j - 1), -1, 0))
                add(("L", j, e, r), rows_n[e] * sgn[:, None])
    for d in range(0, k + 1):                       # F_d for e, one block per class r modulo 2^d
        for e in do:
            for r in range(2 ** d):
                ind = (b % 2 ** d == r).astype(np.int64)
                add(("F", d, e, r), rows_n[e] * ind[:, None])
    T = np.concatenate(cols, axis=1)
    starts = np.array([s for (_, s, _) in blocks])
    idx = {lab: i for i, (lab, _, _) in enumerate(blocks)}
    return k, n1, dn, do, T, starts, idx

def main():
    n, m = int(sys.argv[1]), int(sys.argv[2])
    mode = sys.argv[3] if len(sys.argv) > 3 else "zero"
    limit = float(sys.argv[4]) if len(sys.argv) > 4 else 240.0
    t0 = time.time()
    k, n1, dn, do, T, starts, idx = build(n)
    S = 1 << m
    sg = np.array([[-1 if (s >> i) & 1 else 1 for i in range(m)] for s in range(S)], dtype=np.int64)
    sidx = np.arange(S)
    A_cols = [idx[("A", d)] for d in dn]
    O_cols = [idx[("O", e)] for e in do]
    L_cols = {(j, e): [idx[("L", j, e, r)] for r in range(2 ** (j - 1))] for j in range(1, k + 1) for e in do}
    F_cols = {(d, e): [idx[("F", d, e, r)] for r in range(2 ** d)] for d in range(k + 1) for e in do}
    A_of = {d: idx[("A", d)] for d in dn}
    if mode == "all":
        gen = itertools.combinations_with_replacement(range(n), m)
    else:
        gen = ((0,) + c for c in itertools.combinations_with_replacement(range(n), m - 1)) if m >= 1 else iter([()])
    cnt = 0
    fail_main = fail_32 = fail_2G = fail_Gstar = fail_minus1 = 0
    eq_main = eq_two = 0
    slice_mis = lev0_mis = union_mis = bset_mis = bcount_mis = c_mis = a_mis = 0
    nobad_odd = nobad_odd_but_bad_n = 0
    tot_badn = tot_bado = tot_G = 0
    maxratio = (0, 1)
    ex32 = ex2G = exGstar = None
    ram_checked = ram_mis = 0
    cut = False
    for B in gen:
        if cnt % 2000 == 0 and time.time() - t0 > limit:
            cut = True
            break
        cnt += 1
        Bl = list(B)
        R = sg @ T[Bl] if m else np.zeros((1, T.shape[1]), dtype=np.int64)
        Z = np.add.reduceat((R != 0).astype(np.int32), starts, axis=1) == 0      # Z[s, block]: block is 0
        badn = Z[:, A_cols].any(axis=1)
        bado = Z[:, O_cols].any(axis=1)
        # F_d^(e), G_d
        Fde = {de: Z[:, c].all(axis=1) for de, c in F_cols.items()}
        Gd = [np.logical_or.reduce([Fde[(d, e)] for e in do]) for d in range(k + 1)]
        G = Gd[k]
        # the variant "for every class some e" (deliberately not the note's G)
        Gstar = np.logical_and.reduce([np.logical_or.reduce([Z[:, idx[("F", k, e, r)]] for e in do])
                                       for r in range(2 ** k)])
        # levels
        Lje = {je: Z[:, c].all(axis=1) for je, c in L_cols.items()}
        Bj = [bado] + [np.logical_or.reduce([Lje[(j, e)] for e in do]) for j in range(1, k + 1)]
        # bullet 1: bad at e on Z_n iff bad at e for B' ; G_0 = B_0
        for e in do:
            if (Z[:, A_of[e]] != Z[:, idx[("O", e)]]).any():
                lev0_mis += 1
        if (Gd[0] != Bj[0]).any():
            lev0_mis += 1
        # bullet 2: Phi_(2^j e) | S iff level j is bad for e
        for j in range(1, k + 1):
            for e in do:
                if (Z[:, A_of[2 ** j * e]] != Lje[(j, e)]).any():
                    slice_mis += 1
        if (np.logical_or.reduce(Bj) != badn).any():
            union_mis += 1
        # Theorem U's steps in this setting
        pos = [x % 2 ** k for x in Bl]
        for j in range(1, k + 1):
            mask = 0
            for i, u in enumerate(pos):
                if u % 2 ** j >= 2 ** (j - 1):
                    mask |= 1 << i
            if (Bj[j] != Gd[j - 1][sidx ^ mask]).any():
                bset_mis += 1
            if Bj[j].sum() != Gd[j - 1].sum():
                bcount_mis += 1
            if (Gd[j] & ~(Bj[j] & Bj[0])).any():
                c_mis += 1
            if (Gd[j] & ~Gd[j - 1]).any():
                a_mis += 1
        nb, no, g, gs = int(badn.sum()), int(bado.sum()), int(G.sum()), int(Gstar.sum())
        tot_badn += nb; tot_bado += no; tot_G += g
        if nb > 2 * no - g:
            fail_main += 1
        if nb == 2 * no - g:
            eq_main += 1
        if no > 0 and nb == 2 * no:
            eq_two += 1
        if no == 0:
            nobad_odd += 1
            if nb > 0:
                nobad_odd_but_bad_n += 1
        else:
            if nb * maxratio[1] > maxratio[0] * no:
                maxratio = (nb, no)
        if 2 * nb > 3 * no:
            fail_32 += 1
            if ex32 is None: ex32 = (B, nb, no, g)
        if nb > 2 * no - 2 * g:
            fail_2G += 1
            if ex2G is None: ex2G = (B, nb, no, g)
        if nb > 2 * no - gs:
            fail_Gstar += 1
            if exGstar is None: exGstar = (B, nb, no, g, gs)
        if nb > 2 * no - g - 1:
            fail_minus1 += 1
        # second criterion (Ramanujan sums) on a sample of multisets: every d | n, every signing
        if cnt % 997 == 1 and m <= 6:
            for s in range(S):
                v = [0] * n
                for i, x in enumerate(Bl):
                    v[x] += int(sg[s, i])
                for d in dn:
                    ram_checked += 1
                    if phi_divides_ramanujan(v, d) != bool(Z[s, A_of[d]]):
                        ram_mis += 1
    from math import gcd
    g_ = gcd(maxratio[0], maxratio[1]) or 1
    print(f"n={n} (2^{k}*{n1}) m={m} mode={mode} multisets={cnt}{' CUT OFF BY TIME' if cut else ''} signings each={S}")
    print(f"  Corollary U  #bad_n <= 2*#bad_odd - #G : failures {fail_main}; equality in {eq_main}; "
          f"#bad_n = 2*#bad_odd > 0 in {eq_two}; largest #bad_n/#bad_odd = {maxratio[0]//g_}/{maxratio[1]//g_}")
    print(f"  totals over the multisets: bad_n {tot_badn}, bad_odd {tot_bado}, G {tot_G}; "
          f"multisets with no bad signing on the odd part {nobad_odd}, of these with a bad signing on Z_n {nobad_odd_but_bad_n}")
    print(f"  bullets: level 0 / G_0=B_0 mismatches {lev0_mis}; slice criterion (both directions) mismatches {slice_mis}; "
          f"union of levels != bad_n {union_mis}")
    print(f"  steps in this setting: (a') {a_mis}, (b') as sets {bset_mis}, as counts {bcount_mis}, (c') {c_mis} mismatches")
    print(f"  false variants (should fail somewhere): factor 3/2 fails in {fail_32} {ex32}; "
          f"-2#G fails in {fail_2G} {ex2G}; G with 'every class, some e' fails in {fail_Gstar} {exGstar}; "
          f"-#G-1 fails in {fail_minus1}")
    print(f"  Ramanujan-sum criterion against remainders: {ram_checked} (signing, d) pairs, mismatches {ram_mis}")
    print(f"  time {time.time()-t0:.1f}s")

main()
