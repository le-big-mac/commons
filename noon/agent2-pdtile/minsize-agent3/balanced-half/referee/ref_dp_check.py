"""Referee: read the states written by ref_dp (every (vector, E(N), F(N)) of a class with j levels below it and
total <= B) and test Lemmas 2-6 on all of them (every pair contained in the pattern), then at the top level
Theorem A, Proposition 7, Theorem B (lower bound) and whether the least total of each exact balanced pattern is
the claimed value.

usage: ref_dp_check.py p q n B Bfull states.bin [brute_dump.npy brute_smax]
  with a brute dump (from REF_DUMP=... ref_brute.py all p q n smax): the set of top-level states with
  1 <= total <= smax must be the same set as the brute force found from the literal definitions.
"""
import sys
import numpy as np
from ref_common import set_tables, rule, bits_to_set
from ref_lemmas import Tally, test_records


def main():
    p, q, n, B, Bfull = (int(x) for x in sys.argv[1:6])
    rec = np.fromfile(sys.argv[6], dtype=np.int32).reshape(-1, q + 3).astype(np.int64)
    tabs = set_tables(p, q, n + 1, B)
    print(f"=== recursion over the tree: p={p} q={q} n={n}; all states with total <= {B} at levels < {n}; at level {n} "
          f"all states with total <= {Bfull} and all balanced states with total <= {B} ===")
    for j in range(0, n + 1):
        r = rec[rec[:, 0] == j]
        g = r[:, 1:1 + q]
        tot = g.sum(axis=1)
        bal = (g == g[:, :1]).all(axis=1)
        Eb = r[:, 1 + q]
        Fb = r[:, 2 + q]
        keep = tot >= 1
        tally = Tally()
        ex = []
        test_records(p, q, j, tot[keep], bal[keep], Eb[keep], Fb[keep], tabs, tally, ex, tag=f"level{j}")
        print(f" level {j}: {int(keep.sum())} nonempty states ({int((keep & ~bal).sum())} unbalanced, {int((keep & bal).sum())} balanced)")
        tally.report("   ")
        if ex:
            k = ex[0]
            print("   FIRST COUNTEREXAMPLES:", [(t, e, f, [int(v) for v in g[keep][i]], int(Eb[keep][i]), int(Fb[keep][i])) for (_, t, e, f, i) in ex[:5]])
    # top level: theorems
    r = rec[rec[:, 0] == n]
    g = r[:, 1:1 + q]
    tot = g.sum(axis=1)
    bal = (g == g[:, :1]).all(axis=1)
    Eb = r[:, 1 + q]
    Fb = r[:, 2 + q]
    sel = bal & (tot >= 1)
    mins = {}
    nbad = {"A": 0, "P7": 0, "B": 0}
    nchk = 0
    for t, e_, f_ in zip(tot[sel], Eb[sel], Fb[sel]):
        key = (int(e_), int(f_))
        Es = bits_to_set(e_)
        Fs = bits_to_set(f_) | {0}
        val, x, a0, kp = rule(p, q, n, Es, Fs)
        nchk += 1
        if x is None:
            nbad["A"] += t < val
        else:
            nbad["P7"] += t < q * p ** (len(Es) + kp)
            nbad["B"] += t < val
        if key not in mins or t < mins[key]:
            mins[key] = int(t)
    print(f" top level, balanced states checked: {nchk}; below Theorem A bound: {nbad['A']}; below Proposition 7 bound: "
          f"{nbad['P7']}; below Theorem B bound: {nbad['B']}")
    eq = ab = be = notseen = 0
    eqx = {0: 0, 1: 0, None: 0}
    rows = []
    for e_ in range(1 << n):
        for f_ in range(1 << n):
            Es = bits_to_set(e_)
            Fs = bits_to_set(f_) | {0}
            val, x, a0, kp = rule(p, q, n, Es, Fs)
            mn = mins.get((e_, f_))
            if mn is None:
                notseen += 1
                st = "not seen (claimed value above the bound of the run)" if val > B else "NOT SEEN ALTHOUGH CLAIMED VALUE <= B"
            elif mn == val:
                eq += 1
                eqx[x] += 1
                st = "="
            elif mn > val:
                ab += 1
                st = "ABOVE THE CLAIM"
            else:
                be += 1
                st = "BELOW THE CLAIM"
            rows.append(f"   E={sorted(Es)} F={sorted(Fs)}: least total {mn}, claimed {val} (x={x}) {st}")
    print(f" exact balanced patterns: {4 ** n}; least total = claimed value in {eq} (x=0: {eqx[0]}, x=1: {eqx[1]}, "
          f"Theorem A: {eqx[None]}); above the claim {ab}; below the claim {be}; not seen {notseen}")
    for row in rows:
        if not row.endswith("="):
            print(row)
    if len(sys.argv) > 7:
        dump = np.load(sys.argv[7])
        smax = int(sys.argv[8])
        bs = set(tuple(int(v) for v in row) for row in dump)
        ds = set()
        for row, t in zip(r, tot):
            if 1 <= t <= smax:
                ds.add(tuple(int(v) for v in row[1:]))
        print(f" comparison with the literal brute force (totals 1..{smax}): brute states {len(bs)}, recursion states "
              f"{len(ds)}, only in brute {len(bs - ds)}, only in recursion {len(ds - bs)}")


if __name__ == "__main__":
    main()
