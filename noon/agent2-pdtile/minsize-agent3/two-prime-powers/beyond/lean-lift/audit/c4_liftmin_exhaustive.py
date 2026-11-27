# Part 3(d), exhaustive: the three theorems of Pnq/LiftMin.lean against a census of ALL multisets of size <= S on Z_{p^n q r}.
# For each instance (Es, Fs, a0 satisfying the hypotheses) the least s in the set of the Lean statement is found from the
# census and compared with the value Lean gives by #eval (A7_rule_eval.out).  If the value is above S, only "no member of
# size <= S" is checked (lower bound up to S); those are left to the integer-programming run (c5).
import sys, time
sys.path.insert(0, '/home/agent3/lean/lift-audit')
from core import *
from liftmin_conditions import *
t0 = time.time()
val = lean_values()
scale = sys.argv[1]
#        p  q  n  r   S  fix_zero
CASES = [(3, 2, 0, 3,  6, False), (2, 3, 0, 3,  7, False), (2, 3, 0, 5,  6, False), (2, 5, 0, 3,  7, False), (3, 2, 0, 5, 6, False),
         (5, 2, 0, 3,  6, False), (2, 5, 0, 5,  6, False), (2, 7, 0, 3,  7, True), (3, 5, 0, 3, 6, False), (5, 3, 0, 5, 5, True),
         (2, 3, 1, 3,  7, False), (3, 2, 1, 3,  7, False), (2, 3, 1, 5,  6, False), (3, 2, 1, 5,  6, False), (2, 3, 1, 7, 6, True),
         (3, 2, 1, 7,  6, True),  (2, 5, 1, 3,  8, True),  (5, 2, 1, 3,  8, True),  (2, 5, 1, 5,  6, True),  (3, 5, 1, 3, 6, True),
         (5, 3, 1, 3,  6, True),  (3, 2, 2, 3,  6, True),  (2, 3, 2, 5,  5, True),  (2, 5, 2, 3, 5, True),
         (2, 3, 3, 3,  5, True),  (2, 3, 2, 3,  8, True)]
if scale == "small":
    CASES = [(2, 3, 1, 3, 6, False), (2, 3, 2, 3, 5, True)]
cache = {}
allbad = 0; full = 0; partial = 0
for (p, q, n, r, S, fz) in CASES:
    N = p ** n * q; M = N * r
    key = (M, S, fz)
    if key not in cache:
        cache[key] = census(M, S, fix_zero=fz)
        if fz:   # the translation shortcut, checked against the plain census at a smaller size in the same group
            S0 = min(S, 4)
            a, _ = census(M, S0, fix_zero=False); b, _ = census(M, S0, fix_zero=True)
            assert a == b, "fix_zero census differs"
    cen, nms = cache[key]
    insts = instances(p, q, n, r, val)
    bad = []; nfull = 0; npart = 0; kinds = {"U": 0, "A": 0, "B": 0}
    for (label, member, v) in insts:
        sizes = sorted({s for D, ss in cen.items() for s in ss if member(D, s)})
        least = sizes[0] if sizes else None
        kinds[label[0]] += 1
        if v <= S:
            nfull += 1
            if least != v: bad.append((label, "Lean value", v, "least found", least))
        else:
            npart += 1
            if least is not None: bad.append((label, "Lean value", v, "but a member of size", least))
    allbad += len(bad); full += nfull; partial += npart
    print(f"  p={p} q={q} n={n} r={r}  Z_{M:<3d} (N={N:2d})  S={S}{' (0 fixed)' if fz else ''}: {nms} multisets; instances U/A/B = {kinds['U']}/{kinds['A']}/{kinds['B']}; "
          f"least size = Lean value in {nfull} (value <= S); no member of size <= S in {npart} (value > S); DISAGREEMENTS {len(bad)}"
          + (f"  FIRST {bad[0]}" if bad else ""), flush=True)
print(f"total: {full} instances confirmed exactly, {partial} only bounded below by S+1, {allbad} disagreements;  run {scale}: {time.time()-t0:.0f} s")
