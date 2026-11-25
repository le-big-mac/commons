"""Solver-free exhaustive search for Lemma A at (p,q) = (2,3), M = 144, |A| = 12.

Every 12-subset A of Z_144 has a unique chain of count functions
     n3 on Z_3  <-  n36 on Z_36 (cells hold <= 4)  <-  n72 on Z_72 (cells hold <= 2)  <-  A.
Phi_d | A depends only on the count function on Z_{d'} for any d | d' | 144, and is the exact
integer linear condition  sum_c n(c) * (X^c mod Phi_d) = 0.   So we enumerate level by level,
keeping at each level exactly the count functions that satisfy the hypotheses visible there:
     level 3: Phi_3      level 36: Phi_36      level 72: Phi_72      level 144: Phi_16.
Level 36 is done by meet-in-the-middle over the three classes mod 3 (exact vector matching);
levels 72 and 144 by listing every refinement of every survivor.
No Fact from the text is used to prune; a hypothesis can be switched off (control).

Usage: exhaustive_A.py full | drop3 | drop16 | drop72 | drop36  [time budget seconds]
"""
import sys, time, itertools
import numpy as np
from common import residues, phi_divides, zero_set, selftest

M, SIZE = 144, 12
R3 = np.array(residues(3, 3), dtype=np.int64)        # 3 x 2
R36 = np.array(residues(36, 36), dtype=np.int64)     # 36 x 12
R72 = np.array(residues(72, 72), dtype=np.int64)     # 72 x 24
R16 = np.array(residues(16, 144), dtype=np.int64)    # 144 x 8
CELLS36 = [[c for c in range(36) if c % 3 == j] for j in range(3)]


def comps(total, parts, cap):
    """All tuples of length `parts`, entries in [0, cap], summing to `total`."""
    if parts == 1:
        if 0 <= total <= cap:
            yield (total,)
        return
    for v in range(min(cap, total) + 1):
        for rest in comps(total - v, parts - 1, cap):
            yield (v,) + rest


_VCACHE = {}


def class_vectors(n):
    """All ways to put n elements in the 12 cells (mod 36) of one class mod 3, <= 4 per cell."""
    if n not in _VCACHE:
        lst = list(comps(n, 12, 4))
        _VCACHE[n] = np.array(lst, dtype=np.int64).reshape(len(lst), 12)
    return _VCACHE[n]


def stage36(n3, use36):
    """Yield every n36 (length-36 int array) refining n3, cap 4, [with Phi_36-residue zero]."""
    V = [class_vectors(n3[j]) for j in range(3)]
    if not use36:
        for i0 in range(len(V[0])):
            for i1 in range(len(V[1])):
                for i2 in range(len(V[2])):
                    n36 = np.zeros(36, dtype=np.int64)
                    n36[CELLS36[0]] = V[0][i0]; n36[CELLS36[1]] = V[1][i1]; n36[CELLS36[2]] = V[2][i2]
                    yield n36
        return
    W = [V[j] @ R36[CELLS36[j]] for j in range(3)]           # m_j x 12 exact residues
    order = sorted(range(3), key=lambda j: len(V[j]))          # a, b = two smallest; c = lookup side
    a, b, c = order
    table = {}
    for i, w in enumerate(W[c]):
        table.setdefault((-w).tobytes(), []).append(i)
    rnd = np.random.default_rng(12345).integers(1, 2 ** 20, size=12, dtype=np.int64)
    hc = np.unique((-W[c]) @ rnd)
    for ia in range(len(V[a])):
        S = W[a][ia] + W[b]                                    # m_b x 12
        cand = np.nonzero(np.isin(S @ rnd, hc))[0]             # hash prefilter (no false negatives)
        for ib in cand:
            for ic in table.get(S[ib].tobytes(), ()):          # exact match
                n36 = np.zeros(36, dtype=np.int64)
                n36[CELLS36[a]] = V[a][ia]; n36[CELLS36[b]] = V[b][ib]; n36[CELLS36[c]] = V[c][ic]
                assert not (n36 @ R36).any()
                yield n36


SPLIT2 = {n: [(x, n - x) for x in range(n + 1) if x <= 2 and n - x <= 2] for n in range(1, 5)}
SPLIT1 = {n: [(x, n - x) for x in range(n + 1) if x <= 1 and n - x <= 1] for n in range(1, 3)}


def refinements(n, half, split):
    """All refinements of count vector n on Z_half to Z_{2*half}: cell c -> cells c, c + half.
    Returns int array (ncombo, 2*half)."""
    cells = [c for c in range(half) if n[c]]
    opts = [np.array(split[int(n[c])], dtype=np.int64) for c in cells]
    ncombo = 1
    for o in opts:
        ncombo *= len(o)
    out = np.zeros((ncombo, 2 * half), dtype=np.int64)
    idx = np.arange(ncombo)
    stride = 1
    for c, o in zip(cells, opts):
        digit = (idx // stride) % len(o)
        out[:, c] = o[digit, 0]
        out[:, c + half] = o[digit, 1]
        stride *= len(o)
    return out


def stage72(n36, use72):
    cand = refinements(n36, 36, SPLIT2)
    if use72:
        cand = cand[~(cand @ R72).any(axis=1)]
    return cand


def stage144(n72, use16):
    cand = refinements(n72, 72, SPLIT1)          # 0/1 indicator vectors on Z_144
    if use16:
        cand = cand[~(cand @ R16).any(axis=1)]
    return cand


def steps123_structure(n72):
    """Does n72 have the form claimed at the end of Step 3 of the proof?
    For each j in Z_3 there is rho_j in Z_2 with N_{3,1}(r, j) = 1 if r = rho_j mod 2 else 0."""
    N31 = np.zeros((8, 3), dtype=np.int64)
    for c in range(72):
        N31[c % 8, c % 3] += n72[c]
    for j in range(3):
        col = N31[:, j]
        if not (list(col) == [1, 0] * 4 or list(col) == [0, 1] * 4):
            return False
    return True


def run(hyps, budget, stop_at_first):
    t0 = time.time()
    use3, use36, use72, use16 = (3 in hyps), (36 in hyps), (72 in hyps), (16 in hyps)
    lvl3 = [n3 for n3 in comps(SIZE, 3, 48)
            if (not use3) or not (np.array(n3, dtype=np.int64) @ R3).any()]
    # most balanced first (only matters for early exit in the controls)
    lvl3.sort(key=lambda n3: (max(n3) - min(n3), n3))
    print(f"  level 3 : {len(lvl3)} count vectors survive" + (f": {lvl3}" if len(lvl3) < 5 else ""))
    s36 = s72 = s144 = 0
    cand72 = cand144 = 0
    struct_ok = struct_bad = 0
    found = []
    complete = True
    for n3 in lvl3:
        for n36 in stage36(n3, use36):
            s36 += 1
            r72 = refinements(n36, 36, SPLIT2)
            cand72 += len(r72)
            if use72:
                r72 = r72[~(r72 @ R72).any(axis=1)]
            for n72 in r72:
                s72 += 1
                if use3 and use36 and use72:
                    if steps123_structure(n72):
                        struct_ok += 1
                    else:
                        struct_bad += 1
                r144 = refinements(n72, 72, SPLIT1)
                cand144 += len(r144)
                if use16:
                    r144 = r144[~(r144 @ R16).any(axis=1)]
                s144 += len(r144)
                for ind in r144[:1] if stop_at_first else r144[:3]:
                    found.append([int(a) for a in np.nonzero(ind)[0]])
                if stop_at_first and found:
                    break
            if (stop_at_first and found) or time.time() - t0 > budget:
                break
        if stop_at_first and found:
            complete = False
            break
        if time.time() - t0 > budget:
            complete = False
            print("  ** time budget hit, search NOT complete **")
            break
    dt = time.time() - t0
    print(f"  level 36: {s36} count vectors survive")
    print(f"  level 72: {cand72} refinements listed, {s72} survive")
    if use3 and use36 and use72:
        print(f"            of these, {struct_ok} have the Step-3 form (N_31(r,j) = 1 iff r = rho_j mod 2), "
              f"{struct_bad} do not")
    print(f"  level 144: {cand144} sets listed, {s144} survive all hypotheses {sorted(hyps)}")
    print(f"  search {'COMPLETE (exhaustive)' if complete else 'stopped early'}; {dt:.1f}s")
    for A in found[:1]:
        ok = all(phi_divides(d, A, M) for d in hyps)
        print(f"  example A = {A}")
        print(f"     exact long-division recheck of {sorted(hyps)}: {'OK' if ok else 'FAILED'};"
              f" full zero set = {zero_set(A, M)}")
    return s36, s72, s144, complete


def pipeline_selftest():
    """The enumeration must contain known solutions and arbitrary sets' refinement chains."""
    rng = np.random.default_rng(7)
    for _ in range(300):
        A = sorted(rng.choice(144, size=12, replace=False).tolist())
        n72 = np.zeros(72, dtype=np.int64); n36 = np.zeros(36, dtype=np.int64)
        ind = np.zeros(144, dtype=np.int64)
        for a in A:
            n72[a % 72] += 1; n36[a % 36] += 1; ind[a] = 1
        r72 = refinements(n36, 36, SPLIT2)
        assert (r72 == n72).all(axis=1).sum() == 1
        assert len(np.unique(r72, axis=0)) == len(r72)
        r144 = refinements(n72, 72, SPLIT1)
        assert (r144 == ind).all(axis=1).sum() == 1
        # residue arrays agree with exact division on random sets
        for d, R, vec in ((36, R36, n36), (72, R72, n72), (16, R16, ind)):
            assert (not (vec @ R).any()) == phi_divides(d, A, M)
    # a set found by my CP-SAT model for {3,72,36} (Phi_16 dropped) must be produced by the chain
    A = [75, 76, 83, 93, 94, 101, 111, 112, 119, 129, 130, 137]
    assert all(phi_divides(d, A, M) for d in (3, 36, 72))
    n36 = np.zeros(36, dtype=np.int64); n72 = np.zeros(72, dtype=np.int64)
    for a in A:
        n36[a % 36] += 1; n72[a % 72] += 1
    n3 = tuple(int(sum(n36[c] for c in CELLS36[j])) for j in range(3))
    assert any((x == n36).all() for x in stage36(n3, True))
    assert (stage72(n36, True) == n72).all(axis=1).sum() == 1
    print("  pipeline self-test passed")


if __name__ == "__main__":
    selftest()
    mode = sys.argv[1] if len(sys.argv) > 1 else "full"
    budget = float(sys.argv[2]) if len(sys.argv) > 2 else 500.0
    full = {3, 16, 72, 36}
    if mode == "full":
        print("Lemma A, (p,q)=(2,3): exhaustive search, hypotheses Phi_3, Phi_16, Phi_72, Phi_36")
        pipeline_selftest()
        s36, s72, s144, complete = run(full, budget, stop_at_first=False)
        assert complete
        print("  RESULT:", "NO 12-subset of Z_144 satisfies all four (Lemma A confirmed at (2,3))"
              if s144 == 0 else f"{s144} SETS FOUND -- Lemma A REFUTED")
    else:
        d = int(mode.replace("drop", ""))
        hyps = full - {d}
        print(f"CONTROL: same search with Phi_{d} dropped, hypotheses {sorted(hyps)}")
        s36, s72, s144, complete = run(hyps, budget, stop_at_first=(d != 16))
        print("  RESULT:", "set(s) found" if s144 else "no set found")
