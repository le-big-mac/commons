"""Referee: the lemma tests on arrays of class records (total, balanced, E(N), F(N)), for EVERY pair (E', F')
contained in the pattern.  Written from the statements of Lemmas 2 to 6 in proof-as-sent.md.

A record is a class N with j levels below it.  E(N), F(N) are bitmasks (level l <-> bit l-1).
"N has a witness at level g" <=> some class at N's own level g has children of unequal totals <=> g not in E(N).
"children of N do not all have equal shapes" <=> 1 not in F(N).
"""
import numpy as np
from ref_common import popcount


class Tally:
    def __init__(self):
        self.c = {}

    def add(self, key, n_hyp, n_bad):
        a = self.c.setdefault(key, [0, 0])
        a[0] += int(n_hyp)
        a[1] += int(n_bad)

    def merge(self, other):
        for k, v in other.c.items():
            self.add(k, v[0], v[1])

    def report(self, prefix=""):
        for k in sorted(self.c):
            print(f"{prefix}{k}: hypothesis held in {self.c[k][0]} (class, pair) instances, violated in {self.c[k][1]}")


def test_records(p, q, j, tot, bal, Eb, Fb, tabs, tally, examples, controls=True, tag=""):
    """tot, bal, Eb, Fb: 1-d arrays over classes with j levels below them."""
    inS, inSp, inQ = tabs
    unb = ~bal
    full = (1 << j) - 1
    for e in range(full + 1):
        selE = (Eb & e) == e
        if not selE.any():
            continue
        pe = p ** popcount(e)
        # Lemma 2
        bad = selE & (tot % pe != 0)
        tally.add("L2 p^|E| divides |N|", selE.sum(), bad.sum())
        badb = selE & bal & (tot % (q * pe) != 0)
        tally.add("L2 balanced: q p^|E| divides |N|", (selE & bal).sum(), badb.sum())
        if bad.any() or badb.any():
            examples.append((tag, "L2", e, None, int(np.flatnonzero(bad | badb)[0])))
        for f in range(full + 1):
            sel = selE & ((Fb & f) == f)
            if not sel.any():
                continue
            u = popcount(e | f)
            su = sel & unb
            # Lemma 3
            if su.any():
                bad = su & ~inS[u][tot]
                tally.add("L3 unbalanced => |N| in S_u", su.sum(), bad.sum())
                if bad.any():
                    examples.append((tag, "L3", e, f, int(np.flatnonzero(bad)[0])))
                if controls:
                    # control (should FAIL somewhere): |N| in S_(u+1)
                    if u + 1 < inS.shape[0]:
                        badc = su & ~inS[u + 1][tot]
                        tally.add("CONTROL (false) L3 with S_(u+1)", su.sum(), badc.sum())
                # Lemma 4: witness at some g in F' : g in f, g not in E(N)
                h4 = su & ((f & ~Eb) != 0)
                if h4.any():
                    bad = h4 & ~(inSp[u][tot] | inQ[u][tot])
                    tally.add("L4 witness in F => |N| in S_u+ or Q_u", h4.sum(), bad.sum())
                    if bad.any():
                        examples.append((tag, "L4", e, f, int(np.flatnonzero(bad)[0])))
                    if controls:
                        badc = h4 & ~inSp[u][tot]
                        tally.add("CONTROL (false) L4 with S_u+ only (= L5 without its hypothesis)", h4.sum(), badc.sum())
                    # Lemma 5: witness at g in F' with no level l < g in E' \ F'
                    adm = 0
                    for g in range(1, j + 1):
                        if (f >> (g - 1)) & 1:
                            lower = (1 << (g - 1)) - 1
                            if (e & ~f & lower) == 0:
                                adm |= 1 << (g - 1)
                    h5 = su & ((adm & ~Eb) != 0)
                    if h5.any():
                        bad = h5 & ~inSp[u][tot]
                        tally.add("L5 => |N| in S_u+", h5.sum(), bad.sum())
                        if bad.any():
                            examples.append((tag, "L5", e, f, int(np.flatnonzero(bad)[0])))
            # Lemma 6: balanced, children not all of equal shapes (needs j >= 1)
            if j >= 1:
                h6 = sel & bal & ((Fb & 1) == 0)
                if h6.any():
                    bad = h6 & (tot < q * p ** u)
                    tally.add("L6 balanced, unequal shapes => |N| >= q p^u", h6.sum(), bad.sum())
                    if bad.any():
                        examples.append((tag, "L6", e, f, int(np.flatnonzero(bad)[0])))
                    if controls:
                        badc = h6 & (tot < q * p ** u + 1)
                        tally.add("CONTROL (false) L6 with strict >", h6.sum(), badc.sum())
