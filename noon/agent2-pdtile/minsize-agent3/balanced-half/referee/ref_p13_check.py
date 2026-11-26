"""Referee, second reading: Proposition 13 from the states of ref_dp13 (least depth of a nonempty fibre class for
every top-level state (vector, E, F) with total <= B).

usage: ref_p13_check.py p q n B states.bin [brute_dump.npy brute_B bal|all]

For every pattern (E, F), 0 in F, F not everything, k' >= 1, with q p^(e+k') <= B:
   (*) the balanced state of total q p^(e+k') with exact pattern (E+, F) exists and its least fibre depth is < g1
   against x = 0.
Also, for the sentence after the proof ("the size condition cannot be dropped, and (E+, F) cannot be replaced by
(E, F) with 'some multiset'"): for every pattern with x = 1 the least total <= B at which a balanced multiset with
exact pattern (E+, F), resp. (E, F), has a nonempty fibre class of depth < g1.
"""
import sys
import numpy as np
from ref_common import rule, bits_to_set


def main():
    p, q, n, B = (int(x) for x in sys.argv[1:5])
    rec = np.fromfile(sys.argv[5], dtype=np.int32).reshape(-1, q + 4).astype(np.int64)
    rec = rec[rec[:, 0] == n]
    g = rec[:, 1:1 + q]
    bal = (g == g[:, :1]).all(axis=1)
    tot = g.sum(axis=1)
    state = {}
    for row, b, t in zip(rec, bal, tot):
        if b and t > 0:
            state[(int(t), int(row[1 + q]), int(row[2 + q]))] = int(row[3 + q])
    full = (1 << n) - 1
    npat = nin = nbad = 0
    nx0 = nx1 = 0
    drop_Eplus = []
    drop_E = []
    for e_ in range(full + 1):
        for f_ in range(full + 1):
            E = bits_to_set(e_)
            F = bits_to_set(f_) | {0}
            val, x, a0, kp = rule(p, q, n, E, F)
            if x is None or kp == 0:
                continue
            npat += 1
            Gp = sorted(a for a in range(a0 + 1, n + 1) if a in F and a not in E)
            g1 = Gp[0]
            size = q * p ** (len(E) + kp)
            ep = sum(1 << (a - 1) for a in (E | set(Gp)))
            if size <= B:
                nin += 1
                v = state.get((size, ep, f_))
                star = v is not None and v < g1
                if v is None:
                    nbad += 1
                    print(f"   NOT SEEN: (E+, F) = ({sorted(E | set(Gp))}, {sorted(F)}) at its least size {size}")
                elif star != (x == 0):
                    nbad += 1
                    print(f"   PROPOSITION 13 FAILS: E={sorted(E)} F={sorted(F)} x={x} g1={g1} least fibre depth {v}")
                nx0 += x == 0
                nx1 += x == 1
            if x == 1:
                t1 = [t for (t, e2, f2), v in state.items() if e2 == ep and f2 == f_ and v < g1]
                t2 = [t for (t, e2, f2), v in state.items() if e2 == e_ and f2 == f_ and v < g1]
                drop_Eplus.append((sorted(E), sorted(F), size, min(t1) if t1 else None))
                drop_E.append((sorted(E), sorted(F), val, min(t2) if t2 else None))
    print(f"=== Proposition 13 by recursion: p={p} q={q} n={n}, balanced states with total <= {B}: {len(state)} ===")
    print(f"  patterns with k' >= 1: {npat}; with q p^(e+k') <= {B}: {nin} (x=0: {nx0}, x=1: {nx1}); disagreements {nbad}")
    f1 = [d for d in drop_Eplus if d[3] is not None]
    f2 = [d for d in drop_E if d[3] is not None]
    print(f"  x = 1 patterns: {len(drop_Eplus)}; some multiset with exact pattern (E+, F) and a nonempty fibre class of depth "
          f"< g1 exists within the run for {len(f1)} of them (always at a total above q p^(e+k'): "
          f"{all(d[3] > d[2] for d in f1)}); with exact pattern (E, F): for {len(f2)} of them")
    if f1:
        d = min(f1, key=lambda d: (d[3], d[0], d[1]))
        print(f"    smallest such example for (E+, F): E={d[0]} F={d[1]}: q p^(e+k') = {d[2]}, fibre class appears at total {d[3]}")
    for d in f1:
        if d[0] == [2] and d[1] == [0, 3]:
            print(f"    E=[2] F=[0,3]: least total with pattern (E+, F) and a fibre class of depth < g1: {d[3]}")
    for d in f2:
        if d[0] == [2] and d[1] == [0, 3]:
            print(f"    E=[2] F=[0,3]: least total with pattern (E, F) and a fibre class of depth < g1: {d[3]} (least size of the pattern {d[2]})")
    if len(sys.argv) > 6:
        dump = np.load(sys.argv[6])
        bB = int(sys.argv[7])
        mode = sys.argv[8]
        bs = {tuple(int(v) for v in row[:-1]): int(row[-1]) for row in dump}
        ds = {}
        for row, b, t in zip(rec, bal, tot):
            if 1 <= t <= bB and (mode == "all" or b):
                ds[tuple(int(v) for v in row[1:3 + q])] = int(row[3 + q])
        if mode == "bal":
            bs = {k: v for k, v in bs.items() if len(set(k[:q])) == 1}
        diff = sum(1 for k in bs if k in ds and ds[k] != bs[k])
        print(f"  against the literal brute force ({mode}, totals 1..{bB}): brute states {len(bs)}, recursion states {len(ds)}, "
              f"only in brute {len(set(bs) - set(ds))}, only in recursion {len(set(ds) - set(bs))}, least fibre depth differs for {diff}")


if __name__ == "__main__":
    main()
