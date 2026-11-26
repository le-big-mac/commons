"""Referee, second reading: Lemma 12 (rearranging fibre classes) tested literally.

For many multisets A with a set Z of pairwise disjoint fibre classes (nonempty and empty ones, of different depths,
sometimes the root) and many rearrangements A' (same outside the union, each member again a fibre class with the
same total):
 (i)   every class not properly contained in a member of Z has the same vector in A and A';
 (ii)  A' balanced iff A balanced; F(A') = F(A);
 (iii) a in E(A') iff [every class of depth a-1 NOT contained in a member has children of equal totals in A] and
       [every class of depth a-1 contained in a member has children of equal totals in A'].
Two sources of A: (1) the constructions (III), (IV), (V) of section 6.3, which have nonempty fibre classes, and the
others with whole fibres added; (2) a random cut of the tree into disjoint classes, some filled with whole fibres,
some with smaller constructions or random weights.

usage: ref_lemma12.py p q n ntrials seed
"""
import sys, random
import numpy as np
from ref_common import literal_classes, literal_patterns, bits_to_set
from ref_construct import digits, build, first_case


def classes_info(p, q, n, W):
    G, eqT, eqS = literal_classes(p, q, n, W.reshape(1, p ** n, q))
    return [g[0] for g in G], [e[0] for e in eqT]


def root_pattern(p, q, n, W):
    r = literal_patterns(p, q, n, W.reshape(1, p ** n, q))[0]
    return bits_to_set(r["E"][0, 0]), bits_to_set(r["F"][0, 0]), bool(r["bal"][0, 0])


def main():
    p, q, n, ntr, seed = (int(x) for x in sys.argv[1:6])
    rng = random.Random(seed)
    pn = p ** n
    digs = {j: digits(p, j) for j in range(1, n + 1)}
    dig = digs[n]
    u = np.arange(pn)
    levels = list(range(1, n + 1))
    st = dict(trials=0, members=0, root=0, empty=0, nonempty=0, bad_i=0, bad_ii=0, bad_iii=0, E_changed=0, cls=0,
              lev_true=0, lev_false=0, proper_changed=0, balA=0)

    def fibre_fill(A, d, c, nf, T=None):
        """put nf whole fibres into class (d, c): m.Fib(D) with D free on T (levels beyond d) if p^|T| divides nf,
        else at random strings"""
        inZ = (u % p ** d) == c
        A[inZ, :] = 0
        if nf == 0:
            return
        if T is None:
            T = [a for a in range(d + 1, n + 1) if rng.random() < 0.5]
        T = [a for a in T if a > d]
        while T and nf % p ** len(T):
            T.pop(rng.randrange(len(T)))
        if rng.random() < 0.85:
            m = inZ.copy()
            for a in range(d + 1, n + 1):
                if a not in T:
                    m &= dig[a] == (0 if rng.random() < 0.8 else rng.randrange(p))
            A[m, :] = nf // p ** len(T)
        else:
            idx = np.flatnonzero(inZ)
            for _f in range(nf):
                A[rng.choice(idx), :] += 1

    for _ in range(ntr):
        A = np.zeros((pn, q), dtype=np.int64)
        fibre_classes = []                      # known fibre classes of A (d, c)
        if rng.random() < 0.55:
            # (1) a construction of section 6.3
            E = {a for a in levels if rng.random() < 0.5}
            F = {a for a in levels if rng.random() < 0.6} | {0}
            A = build(p, q, n, dig, E, F, first_case(p, n, E, F)).copy()
            if rng.random() < 0.2:
                A[rng.randrange(pn), rng.randrange(q)] += 1          # sometimes unbalanced
        else:
            # (2) a random cut of the tree
            cut = [(0, 0)]
            for _s in range(rng.choice((1, 2, 3, 4))):
                d, c = cut.pop(rng.randrange(len(cut)))
                if d == n:
                    cut.append((d, c))
                    continue
                cut += [(d + 1, c + j * p ** d) for j in range(p)]
            for (d, c) in cut:
                inZ = (u % p ** d) == c
                r = rng.random()
                j = n - d
                if r < 0.45:
                    fibre_fill(A, d, c, rng.choice((0, 1, 2, p, p * p, 2 * p, p ** min(j, 3))))
                elif r < 0.8 and j >= 1:
                    E = {a for a in range(1, j + 1) if rng.random() < 0.5}
                    F = {a for a in range(1, j + 1) if rng.random() < 0.6} | {0}
                    sub = build(p, q, j, digs[j], E, F, first_case(p, j, E, F))
                    A[inZ, :] = sub                      # strings c + p^d u' in increasing u'
                else:
                    for _k in range(rng.choice((1, 2, 3))):
                        A[rng.choice(np.flatnonzero(inZ)), rng.randrange(q)] += 1
        # all fibre classes of A, literally
        leafconst = (A == A[:, :1]).all(axis=1)
        cands = []
        for d in range(0, n + 1):
            for c in range(p ** d):
                inZ = (u % p ** d) == c
                if leafconst[inZ].all():
                    cands.append((d, c, int(A[inZ].sum()) > 0))
        rng.shuffle(cands)
        cands.sort(key=lambda t: (not t[2], rng.random()))           # nonempty ones first
        Z = []
        for (d, c, ne) in cands:
            if rng.random() < (0.25 if ne else 0.9):
                continue
            if all((c % p ** min(d, d2)) != (c2 % p ** min(d, d2)) for (d2, c2) in Z):    # disjoint from those chosen
                Z.append((d, c))
            if len(Z) >= 5:
                break
        if not Z:
            continue
        A2 = A.copy()
        commonT = [a for a in levels if rng.random() < 0.5] if rng.random() < 0.7 else None
        for (d, c) in Z:
            inZ = (u % p ** d) == c
            nf = int(A[inZ, 0].sum())
            st["members"] += 1
            st["root"] += d == 0
            st["empty" if nf == 0 else "nonempty"] += 1
            fibre_fill(A2, d, c, nf, commonT)
            assert int(A2[inZ].sum()) == int(A[inZ].sum()) and bool((A2[inZ] == A2[inZ][:, :1]).all())
        st["trials"] += 1
        GA, eqTA = classes_info(p, q, n, A)
        GB, eqTB = classes_info(p, q, n, A2)

        def contained(d, c):
            return any(d2 <= d and (c % p ** d2) == c2 for (d2, c2) in Z)

        def properly(d, c):
            return any(d2 < d and (c % p ** d2) == c2 for (d2, c2) in Z)

        for d in range(0, n + 1):
            for c in range(p ** d):
                same = bool((GA[d][c] == GB[d][c]).all())
                if not properly(d, c):
                    st["cls"] += 1
                    st["bad_i"] += not same
                else:
                    st["proper_changed"] += not same
        EA, FA, balA = root_pattern(p, q, n, A)
        EB, FB, balB = root_pattern(p, q, n, A2)
        st["balA"] += balA
        st["bad_ii"] += (balA != balB or FA != FB)
        for a in levels:
            cond = True
            for c in range(p ** (a - 1)):
                cond = cond and bool(eqTB[a - 1][c] if contained(a - 1, c) else eqTA[a - 1][c])
            st["bad_iii"] += cond != (a in EB)
            st["lev_true" if a in EB else "lev_false"] += 1
        st["E_changed"] += EA != EB
    print(f"Lemma 12: p={p} q={q} n={n}: {st['trials']} pairs (A, A') ({st['balA']} with A balanced), {st['members']} members of Z "
          f"({st['nonempty']} nonempty, {st['empty']} empty, {st['root']} equal to the root); (i) on {st['cls']} classes not properly inside a member: "
          f"violations {st['bad_i']} (classes properly inside a member whose vector did change: {st['proper_changed']}); (ii) violations {st['bad_ii']}; "
          f"(iii) violations {st['bad_iii']} over {st['lev_true'] + st['lev_false']} levels ({st['lev_true']} in E(A'), {st['lev_false']} not); "
          f"E(A') differs from E(A) in {st['E_changed']} pairs", flush=True)


if __name__ == "__main__":
    main()
