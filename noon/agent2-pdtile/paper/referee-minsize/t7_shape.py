"""Lemma 13 of the PDF (the shape part) and the separate claims of the outline of Proposition 14,
each tested as worded.
usage: t7_shape.py p q nmax seed
"""
import sys, itertools, random
import numpy as np
from lib import class_vectors, class_pattern, root_pattern, is_constant, children, subsets
from t6_constructions import digit, D, Dmap, Fib, shape_part, balanced

p, q, nmax, seed = map(int, sys.argv[1:5])
rng = random.Random(seed)
st = {}
fails = []


def ck(name, ok, info=None):
    c = st.setdefault(name, [0, 0])
    c[0] += 1
    if not ok:
        c[1] += 1
        if len(fails) < 40:
            fails.append((name, info))


def sub(s):
    s = sorted(s)
    for r in range(len(s) + 1):
        for c in itertools.combinations(s, r):
            yield set(c)


def lemma13():
    for n in range(1, nmax + 1):
        for a0 in range(1, n + 1):
            for T1 in sub(range(1, a0)):
                for T2 in sub(range(a0 + 1, n + 1)):
                    for H in sub(T2):
                        for mode in "UQW":
                            info = (n, a0, sorted(T1), sorted(T2), sorted(H), mode)
                            S = shape_part(p, q, n, a0, T1, T2, H, mode)
                            mu = {"U": 1, "Q": p, "W": 2}[mode]
                            ck("L13 size", int(S.sum()) == mu * q * p ** (len(T1) + len(T2)), info)
                            vec = {d: class_vectors(S, p, n, d) for d in range(n + 1)}
                            ck("L13 classes of depth < a0 balanced in S",
                               all(is_constant(vec[d][c]) for d in range(a0) for c in range(p ** d)), info)
                            Dstar = set(D(set(T1) | {a0} | set(T2), p, n))
                            # text before the lemma: a class of depth >= a0 that meets D* with digit 0 or 1 at a0 is unbalanced;
                            # "|beta| is a power of p" (true only for classes that meet D*)
                            for d in range(a0, n + 1):
                                for c in range(p ** d):
                                    meets = sum(1 for u in Dstar if u % p ** d == c)
                                    i = digit(c, a0, p)
                                    if meets:
                                        if i <= 1:
                                            ck("text: class at depth >= a0, digit 0/1, meeting D* is unbalanced", not is_constant(vec[d][c]), info)
                                        elif mode == "Q":
                                            ck("text: mode Q digit >= 2 class is constant |beta| 1", is_constant(vec[d][c]) and vec[d][c][0] == meets, info)
                                        else:
                                            ck("text: modes U, W digit >= 2 class empty", vec[d][c].sum() == 0, info)
                                    ck("text: |beta| is a power of p (as worded, for every class of depth >= a0)",
                                       meets > 0 and p ** round(np.log(meets) / np.log(p)) == meets, None)
                            # S + Phi for sums Phi of m.Fib(D), D arbitrary sets of strings
                            for trial in range(4):
                                Phi = np.zeros_like(S)
                                if trial > 0:
                                    for _ in range(rng.randint(1, 3)):
                                        Dset = rng.sample(range(p ** n), rng.randint(1, p ** n))
                                        Phi = Phi + Fib(Dset, p, q, n, rng.randint(1, 3))
                                E_, F_, bal = root_pattern(S + Phi, p, n)
                                ck("L13 S+Phi balanced, F = [1,a0-1] u (T2 minus H)",
                                   bal and set(F_) == set(range(1, a0)) | (set(T2) - set(H)), info + (trial,))
                            # level by level, in S
                            for a in range(1, n + 1):
                                for c in range(p ** (a - 1)):
                                    kv = [vec[a][k] for k in children(c, p, a - 1)]
                                    meets = any(u % p ** (a - 1) == c for u in Dstar)
                                    if a in T1 or a in (set(T2) - set(H)):
                                        ck("L13 equal vectors at T1 and T2 minus H", all((x == kv[0]).all() for x in kv), info)
                                    elif a in H:
                                        ck("L13 equal totals at H", len({int(x.sum()) for x in kv}) == 1, info)
                                    elif a != a0:
                                        ck("L13 only digit 0 child nonempty outside T1,T2,a0", all(x.sum() == 0 for x in kv[1:]), info)
                                    elif meets:
                                        t = [int(x.sum()) for x in kv]
                                        P = p ** len(T2)
                                        if mode == "U":
                                            want = [P, (q - 1) * P] + [0] * (p - 2)
                                        elif mode == "Q":
                                            want = [q * P] * p
                                        else:
                                            want = [q * P, q * P] + [0] * (p - 2)
                                        ck("L13 totals at a0", t == want, info + (t, want))
                                    else:
                                        ck("L13 class at depth a0-1 not meeting D* is empty", vec[a - 1][c].sum() == 0, info)


def outline():
    for n in range(1, nmax + 1):
        full = set(range(1, n + 1))
        for E in sub(full):
            for F in sub(full):
                if F == full:
                    continue
                a0 = min(full - F)
                G = {a for a in F - E if a > a0}
                kp = len(G)
                e = len(E)
                A, case = balanced(p, q, n, E, F)
                info = (n, sorted(E), sorted(F), case)
                T20 = {a for a in E | F if a > a0}
                H0 = {a for a in E - F if a > a0}
                Elt = {a for a in E if a < a0}
                mode0 = "Q" if a0 in E else "U"
                between = [a for a in sorted(E - F) if kp >= 1 and a0 < a < min(G)]
                if case == "I":
                    S = shape_part(p, q, n, a0, Elt, T20, H0, mode0); host = None; T2 = T20; Hs = H0
                    ck("outline size S (I) = q p^e", int(S.sum()) == q * p ** e, info)
                elif case == "II":
                    S = shape_part(p, q, n, a0, Elt, T20, H0, mode0); host = None; T2 = T20; Hs = H0
                    ck("outline size S (II) = q p^(e+k')", int(S.sum()) == q * p ** (e + kp), info)
                elif case == "III":
                    host = min(E); T2 = T20; Hs = H0
                    S = shape_part(p, q, n, a0, Elt - {host}, T20, H0, mode0)
                    ck("outline size S (III) = q p^(e-1+k')", int(S.sum()) == q * p ** (e - 1 + kp), info)
                elif case == "IV":
                    host = a0; T2 = T20; Hs = H0
                    S = shape_part(p, q, n, a0, Elt, T20, H0, "W")
                    ck("outline size S (IV) = 2 q p^(e-1+k')", int(S.sum()) == 2 * q * p ** (e - 1 + kp), info)
                else:
                    host = between[0]; T2 = T20 - {host}; Hs = H0 - {host}
                    S = shape_part(p, q, n, a0, Elt, T2, Hs, "Q")
                    ck("outline size S (V) = q p^(e-1+k')", int(S.sum()) == q * p ** (e - 1 + kp), info)
                ck("outline: T2 minus H = F n (a0,n] in every case", T2 - Hs == {a for a in F if a > a0}, info)
                Phi = A - S
                vA = {d: class_vectors(A, p, n, d) for d in range(n + 1)}
                vS = {d: class_vectors(S, p, n, d) for d in range(n + 1)}
                vP = {d: class_vectors(Phi, p, n, d) for d in range(n + 1)}
                if host is not None:
                    # "the fibre multisets fill the remaining p-1 (in (IV): p-2) children at the host level with
                    #  q p^(e-1+k') elements each, so the totals at the host level are equal"
                    lit = True
                    eq = True
                    nclasses = 0
                    for c in range(p ** (host - 1)):
                        if vA[host - 1][c].sum() == 0:
                            continue
                        nclasses += 1
                        t = [int(vA[host][k].sum()) for k in children(c, p, host - 1)]
                        if len(set(t)) != 1:
                            eq = False
                        if any(x != q * p ** (e - 1 + kp) for x in t):
                            lit = False
                    ck(f"outline ({case}): totals at the host level equal", eq, info)
                    ck(f"outline ({case}): each child at the host level has q p^(e-1+k') elements (literal)", lit, info + (nclasses,))
                    ck(f"outline ({case}): each Phi_i has q p^(e-1+k') elements in all",
                       int(Phi.sum()) == (p - 2 if case == "IV" else p - 1) * q * p ** (e - 1 + kp), info)
                    # "A class at or below the host level contains either only elements of S or only fibres of one Phi_i"
                    ok = True
                    for d in range(host, n + 1):
                        for c in range(p ** d):
                            if vS[d][c].sum() > 0 and vP[d][c].sum() > 0:
                                ok = False
                    ck(f"outline ({case}): classes of depth >= host hold only S or only fibres", ok, info)
                # level by level
                for a in range(1, n + 1):
                    zero_class = vA[a - 1][0]
                    kv = [vA[a][k] for k in children(0, p, a - 1)]
                    if (a not in E and a not in F) or (a not in E and a < a0):
                        ck("outline: outside E u F, or not in E before a0: class with earlier digits 0 nonempty with one nonempty child",
                           zero_class.sum() > 0 and sum(1 for x in kv if x.sum() > 0) == 1, info + (a,))
                    if a == a0 and a0 not in E:
                        t = [int(x.sum()) for x in kv]
                        c_ = len({b for b in E if b > a0})
                        if case in ("I", "III"):
                            want = [p ** len(T2), (q - 1) * p ** len(T2)] + [0] * (p - 2)
                        else:
                            want = [p ** c_ * (p ** kp + q), p ** c_ * (q - 1) * p ** kp] + [0] * (p - 2)
                        ck(f"outline: totals at a0 not in E, case {case}", t == want, info + (t, want))
                        ck("outline: totals at a0 unequal", len(set(t)) > 1, info)
                    if a in G:
                        if case == "II":
                            ks = [vS[a][k] for k in children(0, p, a - 1)]
                            kp_ = [vP[a][k] for k in children(0, p, a - 1)]
                            ck("outline (II) at G: equal S-vectors, fibres all in digit-0 child",
                               all((x == ks[0]).all() for x in ks) and kp_[0].sum() > 0 and all(x.sum() == 0 for x in kp_[1:]), info + (a,))
                        elif case in ("III", "IV", "V"):
                            dg = {"III": 1, "IV": 2, "V": 1}[case]
                            c = dg * p ** (host - 1)      # digit dg at the host level and 0 elsewhere
                            ks = vS[a - 1][c]
                            kv2 = [vA[a][k] for k in children(c, p, a - 1)]
                            ck(f"outline ({case}) at G: fibre-only class nonempty with all elements in one child",
                               ks.sum() == 0 and vA[a - 1][c].sum() > 0 and sum(1 for x in kv2 if x.sum() > 0) == 1, info + (a,))


lemma13()
outline()
print(f"p={p} q={q} n<={nmax}")
for k in sorted(st):
    print(f"   {k:110s} tested {st[k][0]:8d}  failed {st[k][1]}")
for f in fails[:12]:
    print("   FAIL", f)
