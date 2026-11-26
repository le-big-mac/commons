"""Lemmas 5, 6, 7, 8 and 10 of the PDF (divisibility; S_u; S+_u or Q_u; S+_u; balanced class) on every class
that dp.c found: all (E(N), F(N), balanced?, |N|) for classes with j levels below them and |N| <= B.

Each lemma speaks of a pair (E, F) CONTAINED in the pattern of N, so for every class type every
sub-pair E <= E(N), F <= F(N) is tried.  "N has a witness at level g" is, by the paper's definition,
"g is not in E(N)".
usage: t4_lemmas.py file [file ...]      (files dpout/dp-p-q-n-B*.txt)
"""
import sys, re, itertools
from lib import in_S, in_Sp, in_Q


def subs(s):
    s = sorted(s)
    for r in range(len(s) + 1):
        for c in itertools.combinations(s, r):
            yield frozenset(c)


def main():
    grand = {}
    for fn in sys.argv[1:]:
        m = re.search(r"dp-(\d+)-(\d+)-(\d+)-B(\d+)", fn)
        p, q, n, B = map(int, m.groups())
        st = dict(L5=0, L5bal=0, L6=0, L7=0, L8=0, L10=0,
                  L5_fail=0, L6_fail=0, L7_fail=0, L8_fail=0, L10_fail=0,
                  L6_balanced_would_fail=0, L7_Q_not_Sp=0, L7_nowitness_would_fail=0,
                  L8_extra_hyp_fails_and_not_Sp=0, L8_extra_hyp_fails=0, L10_equalshapes_would_fail=0,
                  L7_balanced_would_fail=0)
        ex8 = None
        memo = {}

        def mem(kind, x, u):
            k = (kind, x, u)
            if k not in memo:
                memo[k] = {"S": in_S, "Sp": in_Sp, "Q": in_Q}[kind](x, p, q, u)
            return memo[k]
        types = 0
        for line in open(fn):
            t = list(map(int, line.split()))
            j = t[0]
            EN = frozenset(l for l in range(1, j + 1) if t[1] >> (l - 1) & 1)
            FN = frozenset(l for l in range(1, j + 1) if t[2] >> (l - 1) & 1)
            bal = bool(t[3])
            for tot in t[4:]:
                if tot == 0:
                    continue          # the empty class; every lemma below assumes or implies nonempty, except Lemma 5 (trivial)
                types += 1
                for E in subs(EN):
                    # Lemma 5
                    st["L5"] += 1
                    if tot % p ** len(E):
                        st["L5_fail"] += 1
                    if bal:
                        st["L5bal"] += 1
                        if tot % (q * p ** len(E)):
                            st["L5_fail"] += 1
                    for F in subs(FN):
                        u = len(E | F)
                        wit = [g for g in F if g not in EN]
                        if not bal:
                            st["L6"] += 1
                            if not mem("S", tot, u):
                                st["L6_fail"] += 1
                            if wit:
                                st["L7"] += 1
                                isSp = mem("Sp", tot, u)
                                isQ = mem("Q", tot, u)
                                if not (isSp or isQ):
                                    st["L7_fail"] += 1
                                if isQ and not isSp:
                                    st["L7_Q_not_Sp"] += 1
                                good_g = [g for g in wit if not any(l < g for l in E - F)]
                                if good_g:
                                    st["L8"] += 1
                                    if not isSp:
                                        st["L8_fail"] += 1
                                else:
                                    st["L8_extra_hyp_fails"] += 1
                                    if not isSp:
                                        st["L8_extra_hyp_fails_and_not_Sp"] += 1
                                        cand = (j, sorted(EN), sorted(FN), sorted(E), sorted(F), tot)
                                        if ex8 is None or (cand[0], cand[5]) < (ex8[0], ex8[5]):
                                            ex8 = cand
                            else:
                                if F and not (mem("Sp", tot, u) or mem("Q", tot, u)):
                                    st["L7_nowitness_would_fail"] += 1
                        else:
                            if not mem("S", tot, u):
                                st["L6_balanced_would_fail"] += 1
                            if wit and not (mem("Sp", tot, u) or mem("Q", tot, u)):
                                st["L7_balanced_would_fail"] += 1
                            if j >= 1 and 1 not in FN:
                                st["L10"] += 1
                                if tot < q * p ** u:
                                    st["L10_fail"] += 1
                            elif j >= 1 and tot < q * p ** u:
                                st["L10_equalshapes_would_fail"] += 1
        print(f"p={p} q={q} classes with j<={n} levels below, |N|<={B}: {types} nonempty class types (E(N),F(N),balanced,|N|)")
        print("   instances (class type x sub-pair): " + ", ".join(f"{k}={st[k]}" for k in ("L5", "L5bal", "L6", "L7", "L8", "L10")))
        print("   FAILURES: " + ", ".join(f"{k}={st[k]}" for k in ("L5_fail", "L6_fail", "L7_fail", "L8_fail", "L10_fail")))
        print("   hypotheses exercised: " + ", ".join(f"{k}={st[k]}" for k in st if "would" in k or "not_Sp" in k or "extra" in k))
        if ex8:
            print("   smallest case with Lemma 7's hypotheses, Lemma 8's extra hypothesis false for every witness level, and |N| not in S+_u:"
                  f" j={ex8[0]} E(N)={ex8[1]} F(N)={ex8[2]} pair E={ex8[3]} F={ex8[4]} |N|={ex8[5]}")
        for k, v in st.items():
            grand[k] = grand.get(k, 0) + v
    print("TOTAL over files: " + ", ".join(f"{k}={v}" for k, v in grand.items()))


main()
