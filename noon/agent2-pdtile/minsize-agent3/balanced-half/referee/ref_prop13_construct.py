"""Referee, second reading: both constructions in the proof of Proposition 13, built from its words.

For every pattern (E, F), 0 in F, F not everything, k' >= 1:
 x = 0  => (*):  A = the multiset of Theorem C (case III, IV or V; the first that applies, and also every other of
     these cases whose condition holds); h, i0; Z = the nonempty classes of depth h whose digit of level h is >= i0.
     Checked: each member is a fibre class whose content is p^k'.Fib(prefix, free on E n (h, n], 0 elsewhere beyond h),
     with q p^(k' + |E n (h,n]|) elements; for a in G', every class of depth a-1 not contained in a member has children
     with equal vectors in A; A+ (Fib(D_Z+) inside each member) has q p^(e+k') elements and exact pattern (E+, F);
     Y (digit i0 at level h, 0 elsewhere) is a member, not empty, a fibre class of A+, of depth h < g1.
 (*) => x = 0:  from that A+ and EVERY nonempty fibre class Z of A+ of depth < g1, the multiset A of the proof
     (m.Fib(D_Z) inside Z) has exact pattern (E, F) and q p^(e+k') elements, and m is a positive integer.
 x = 1: nothing to build; counted.

usage: ref_prop13_construct.py p q nmax
"""
import sys, itertools
import numpy as np
from ref_common import rule
from ref_construct import digits, build, first_case, my_pattern


def main():
    p, q, nmax = (int(x) for x in sys.argv[1:4])
    for n in range(2, nmax + 1):
        pn = p ** n
        dig = digits(p, n)
        u = np.arange(pn)
        lv = list(range(1, n + 1))
        st = dict(pat=0, x1=0, fwd=0, fwd_bad=0, members=0, multi=0, rev=0, rev_bad=0)
        bycase = {}
        for Et in itertools.chain.from_iterable(itertools.combinations(lv, r) for r in range(n + 1)):
            for Ft in itertools.chain.from_iterable(itertools.combinations(lv, r) for r in range(n + 1)):
                E = set(Et)
                F = set(Ft) | {0}
                val, x, a0, kp = rule(p, q, n, E, F)
                if x is None or kp == 0:
                    continue
                st["pat"] += 1
                Gp = sorted(a for a in range(a0 + 1, n + 1) if a in F and a not in E)
                g1 = Gp[0]
                Eplus = E | set(Gp)
                if x == 1:
                    st["x1"] += 1
                    continue
                fc = first_case(p, n, E, F)
                for case in ("III", "IV", "V"):
                    A = build(p, q, n, dig, E, F, case)
                    if A is None:
                        continue
                    tag = case + ("" if case == fc else "(alt)")
                    bycase[tag] = bycase.get(tag, 0) + 1
                    if case == "III":
                        h, i0 = min(E), 1
                    elif case == "IV":
                        h, i0 = a0, 2
                    else:
                        h, i0 = min(b for b in range(a0 + 1, g1) if b in E and b not in F), 1
                    ok = h < g1
                    # members: nonempty classes of depth h whose digit of level h is >= i0
                    members = []
                    for c in range(p ** h):
                        if (c // p ** (h - 1)) % p >= i0:
                            inZ = (u % p ** h) == c
                            if A[inZ].sum() > 0:
                                members.append(c)
                    st["members"] += len(members)
                    st["multi"] += len(members) > (p - i0)
                    Aplus = A.copy()
                    inany = np.zeros(pn, dtype=bool)
                    for c in members:
                        inZ = (u % p ** h) == c
                        inany |= inZ
                        D = inZ.copy()
                        Dp = inZ.copy()
                        for a in range(h + 1, n + 1):
                            if a not in E:
                                D &= dig[a] == 0
                            if a not in Eplus:
                                Dp &= dig[a] == 0
                        want = np.zeros((pn, q), dtype=np.int64)
                        want[D, :] = p ** kp
                        nfree = len([a for a in E if a > h])
                        ok = ok and (A[inZ] == want[inZ]).all() and int(A[inZ].sum()) == q * p ** (kp + nfree)
                        Aplus[inZ, :] = 0
                        Aplus[Dp, :] = 1
                        ok = ok and int(Aplus[inZ].sum()) == int(A[inZ].sum())
                    # for a in G': classes of depth a-1 not contained in a member have children with equal vectors in A
                    for a in Gp:
                        for c in range(p ** (a - 1)):
                            if (c % p ** h) in members:
                                continue
                            kids = [A[(u % p ** a) == c + j * p ** (a - 1)].sum(axis=0) for j in range(p)]
                            ok = ok and all((k == kids[0]).all() for k in kids)
                    Ep, Fp = my_pattern(p, q, n, Aplus)
                    ok = ok and int(Aplus.sum()) == q * p ** (len(E) + kp) and Ep == Eplus and Fp == F
                    # Y
                    cY = i0 * p ** (h - 1)
                    inY = (u % p ** h) == cY
                    ok = ok and cY in members and Aplus[inY].sum() > 0 and bool((Aplus[inY] == Aplus[inY][:, :1]).all())
                    st["fwd"] += 1
                    if not ok:
                        st["fwd_bad"] += 1
                        if st["fwd_bad"] <= 3:
                            print("   FORWARD FAILS", p, q, n, sorted(E), sorted(F), tag, "pattern of A+", sorted(Ep), sorted(Fp))
                    # reverse: every nonempty fibre class of A+ of depth < g1
                    leafconst = (Aplus == Aplus[:, :1]).all(axis=1)
                    for d in range(0, g1):
                        for c in range(p ** d):
                            inZ = (u % p ** d) == c
                            if not leafconst[inZ].all() or Aplus[inZ].sum() == 0:
                                continue
                            Zt = int(Aplus[inZ].sum())
                            nfree = len([a for a in E if a > d])
                            m, rem = divmod(Zt, q * p ** nfree)
                            B = Aplus.copy()
                            B[inZ, :] = 0
                            DZ = inZ.copy()
                            for a in range(d + 1, n + 1):
                                if a not in E:
                                    DZ &= dig[a] == 0
                            B[DZ, :] = m
                            EB, FB = my_pattern(p, q, n, B)
                            st["rev"] += 1
                            if not (rem == 0 and m >= 1 and EB == E and FB == F and int(B.sum()) == q * p ** (len(E) + kp)):
                                st["rev_bad"] += 1
                                if st["rev_bad"] <= 3:
                                    print("   REVERSE FAILS", p, q, n, sorted(E), sorted(F), tag, "Z", d, c, "got", sorted(EB), sorted(FB))
        print(f"Proposition 13 constructions: p={p} q={q} n={n}: {st['pat']} patterns with k' >= 1 ({st['x1']} with x = 1); "
              f"x=0 => (*): {st['fwd']} built {bycase}, failures {st['fwd_bad']}; members of Z in all: {st['members']}, "
              f"constructions with more than one member per digit: {st['multi']}; (*) => x=0: {st['rev']} pairs (A+, fibre class), failures {st['rev_bad']}",
              flush=True)


if __name__ == "__main__":
    main()
