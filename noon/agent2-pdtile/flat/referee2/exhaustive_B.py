"""Solver-free exhaustive search for Lemma B at (p,q) = (2,3), M = 144, |B| = 12.

Phi_4, Phi_8 | B   depend only on n8 = counts of B mod 8;
Phi_9 | B          depends only on n9 = counts of B mod 9;
Phi_6 | B          depends only on n6 = counts of B mod 6.
Each is the exact integer linear condition  sum_c n(c) * (X^c mod Phi_d) = 0.
We list ALL count vectors (compositions of 12) at each of the three levels, keep those that pass
the hypotheses living there, and then ask for a compatible triple: n8 and n6 must induce the same
counts mod 2, n9 and n6 the same counts mod 3.  Any 12-subset (indeed any multiset of 12 residues)
satisfying the hypotheses gives such a triple, so "no compatible triple" proves non-existence.
For the controls (one hypothesis dropped) a compatible triple is turned into an actual subset of
Z_144 by a small backtracking search on the 8 x 9 table of counts mod 72 (cells hold <= 2), and
the set is re-verified by exact long division.

Usage: exhaustive_B.py full | drop4 | drop8 | drop9 | drop6
"""
import sys, time
import numpy as np
from common import residues, phi_divides, zero_set, selftest

M, SIZE = 144, 12


def comps(total, parts, cap):
    if parts == 1:
        if 0 <= total <= cap:
            yield (total,)
        return
    for v in range(min(cap, total) + 1):
        for rest in comps(total - v, parts - 1, cap):
            yield (v,) + rest


def level(mod, ds):
    """All count vectors on Z_mod summing to 12 (cap 144/mod per cell) whose Phi_d residue is 0
    for every d in ds."""
    V = np.array(list(comps(SIZE, mod, M // mod)), dtype=np.int64)
    total = len(V)
    keep = np.ones(total, dtype=bool)
    for d in ds:
        assert mod % d == 0
        R = np.array(residues(d, mod), dtype=np.int64)
        keep &= ~(V @ R).any(axis=1)
    return total, V[keep]


def build_set(n8, n9, n6):
    """Backtracking: x[r][t] in {0,1,2} on Z_8 x Z_9 with row sums n8, column sums n9, and box
    sums n6 (box of (r,t) is the c in Z_6 with c = r mod 2, c = t mod 3).  Returns a subset of
    Z_144 or None."""
    box_of = {(rho, j): next(c for c in range(6) if c % 2 == rho and c % 3 == j)
              for rho in range(2) for j in range(3)}
    cells = [(r, t) for r in range(8) for t in range(9)]
    row = list(n8); col = list(n9); box = list(n6)
    x = {}
    # remaining capacity trackers (each undecided cell can still take 2)
    row_left = [9] * 8; col_left = [8] * 9; box_left = [12] * 6

    def rec(k):
        if k == len(cells):
            return not any(row) and not any(col) and not any(box)
        r, t = cells[k]
        b = box_of[(r % 2, t % 3)]
        row_left[r] -= 1; col_left[t] -= 1; box_left[b] -= 1
        for v in range(min(2, row[r], col[t], box[b]), -1, -1):
            row[r] -= v; col[t] -= v; box[b] -= v
            if row[r] <= 2 * row_left[r] and col[t] <= 2 * col_left[t] and box[b] <= 2 * box_left[b]:
                x[(r, t)] = v
                if rec(k + 1):
                    return True
            row[r] += v; col[t] += v; box[b] += v
        row_left[r] += 1; col_left[t] += 1; box_left[b] += 1
        return False

    if not rec(0):
        return None
    A = []
    for (r, t), v in x.items():
        if v:
            c = next(c for c in range(72) if c % 8 == r and c % 9 == t)
            A.append(c)
            if v == 2:
                A.append(c + 72)
    return sorted(A)


def run(hyps):
    t0 = time.time()
    tot8, L8 = level(8, [d for d in (4, 8) if d in hyps])
    tot9, L9 = level(9, [d for d in (9,) if d in hyps])
    tot6, L6 = level(6, [d for d in (6,) if d in hyps])
    print(f"  counts mod 8: {tot8} vectors, {len(L8)} satisfy {[d for d in (4, 8) if d in hyps]}")
    print(f"  counts mod 9: {tot9} vectors, {len(L9)} satisfy {[d for d in (9,) if d in hyps]}")
    print(f"  counts mod 6: {tot6} vectors, {len(L6)} satisfy {[d for d in (6,) if d in hyps]}")
    # induced counts mod 2 and mod 3
    m2_from8 = {}
    for v in L8:
        m2_from8.setdefault((int(v[0::2].sum()), int(v[1::2].sum())), []).append(v)
    m3_from9 = {}
    for v in L9:
        m3_from9.setdefault(tuple(int(v[j::3].sum()) for j in range(3)), []).append(v)
    print(f"  possible (N_10(0), N_10(1)) from the mod-8 level: {sorted(m2_from8)}")
    print(f"  possible (N_01(0), N_01(1), N_01(2)) from the mod-9 level: {sorted(m3_from9)}")
    compat = []
    for v in L6:
        m2 = (int(v[0::2].sum()), int(v[1::2].sum()))
        m3 = tuple(int(v[j::3].sum()) for j in range(3))
        if m2 in m2_from8 and m3 in m3_from9:
            compat.append((v, m2, m3))
    if hyps == {4, 8, 9, 6}:
        # what the mod-6 level allows on its own, for the report
        pairs = sorted({((int(v[0::2].sum()), int(v[1::2].sum())),
                         tuple(int(v[j::3].sum()) for j in range(3))) for v in L6})
        ok2 = [pr for pr in pairs if pr[0] in m2_from8]
        ok3 = [pr for pr in pairs if pr[1] in m3_from9]
        print(f"  mod-6 solutions: {len(pairs)} distinct (mod-2 counts, mod-3 counts) pairs;")
        print(f"     with mod-2 counts allowed by the mod-8 level: {ok2}")
        print(f"     with mod-3 counts allowed by the mod-9 level: {len(ok3)} pairs, their mod-2 counts: "
              f"{sorted({pr[0] for pr in ok3})}")
    ntriples = sum(len(m2_from8[m2]) * len(m3_from9[m3]) for _, m2, m3 in compat)
    print(f"  compatible (n8, n9, n6) triples: {ntriples}   [{time.time() - t0:.1f}s]")
    found = None
    tried = 0
    if ntriples:
        for v6, m2, m3 in compat:
            for v8 in m2_from8[m2]:
                for v9 in m3_from9[m3]:
                    tried += 1
                    A = build_set([int(z) for z in v8], [int(z) for z in v9], [int(z) for z in v6])
                    if A is not None:
                        found = A
                        break
                    if tried >= 2000:
                        break
                if found or tried >= 2000:
                    break
            if found or tried >= 2000:
                break
        if found:
            assert len(found) == SIZE and len(set(found)) == SIZE
            ok = all(phi_divides(d, found, M) for d in hyps)
            print(f"  example B = {found}   (triple #{tried})")
            print(f"     exact long-division recheck of {sorted(hyps)}: {'OK' if ok else 'FAILED'};"
                  f" full zero set = {zero_set(found, M)}")
        else:
            print(f"  no set built from the first {tried} compatible triples")
    return ntriples, found


def selftest_levels():
    """Residue test on count vectors agrees with exact division on random sets."""
    rng = np.random.default_rng(11)
    Rs = {d: np.array(residues(d, d), dtype=np.int64) for d in (4, 8, 9, 6)}
    for trial in range(2000):
        if trial % 2:
            A = sorted(rng.choice(144, size=12, replace=False).tolist())
        else:  # structured sets so that positives occur
            g = int(rng.choice([2, 3, 4, 6, 8, 9, 12, 18, 24, 36]))
            base = rng.choice(144 // g, size=max(1, 12 // g), replace=False)
            A = sorted({(int(b) + k * (144 // g)) % 144 for b in base for k in range(g)})
        for d, R in Rs.items():
            n = np.zeros(d, dtype=np.int64)
            for a in A:
                n[a % d] += 1
            assert (not (n @ R).any()) == phi_divides(d, A, M), (d, A)
    print("  level self-test passed")


if __name__ == "__main__":
    selftest()
    mode = sys.argv[1] if len(sys.argv) > 1 else "full"
    full = {4, 8, 9, 6}
    if mode == "full":
        print("Lemma B, (p,q)=(2,3): exhaustive search, hypotheses Phi_4, Phi_8, Phi_9, Phi_6")
        selftest_levels()
        n, _ = run(full)
        print("  RESULT:", "NO 12-subset (or 12-multiset) of Z_144 satisfies all four "
              "(Lemma B confirmed at (2,3))" if n == 0 else "compatible triples exist -- see above")
    else:
        d = int(mode.replace("drop", ""))
        print(f"CONTROL: same search with Phi_{d} dropped, hypotheses {sorted(full - {d})}")
        n, found = run(full - {d})
        print("  RESULT:", "set found" if found else "no set found")
