"""Which programmes of the published Z_108 HiGHS run emit 'transformNewIntegerFeasibleSolution tmpSolver.run()', and what does HiGHS return there?
(the script is run from its source with one textual patch in memory: file-descriptor capture around each solve01 call)"""
import sys, os, io, tempfile, contextlib
from loadscripts import T2, _exec
src = open(T2).read()
s1 = "st, xs = solve01(Am, rhs, None if control else wit); nmilp += 1"; assert src.count(s1) == 1
src = src.replace(s1, "st, xs = CAP(lambda: solve01(Am, rhs, None if control else wit), (i, j, k, sorted(val(o) for o in Z))); nmilp += 1")
import ctypes
LIBC = ctypes.CDLL(None)
HITS = []
def CAP(fn, tag):
    sys.stdout.flush(); sys.stderr.flush()
    with tempfile.TemporaryFile(mode="w+b", dir="/tmp/rev_t2") as tf:
        o1, o2 = os.dup(1), os.dup(2); os.dup2(tf.fileno(), 1); os.dup2(tf.fileno(), 2)
        try: r = fn()
        finally:
            LIBC.fflush(None)
            os.dup2(o1, 1); os.dup2(o2, 2); os.close(o1); os.close(o2)
        tf.seek(0); txt = tf.read().decode(errors="replace")
    if "Highs" in txt: HITS.append((tag, r[0], txt.strip()))
    return r
buf = io.StringIO()
with contextlib.redirect_stdout(buf): ns = _exec(src, [2, 2, 3, 3], "t2search_cap", {"CAP": CAP})
print(buf.getvalue().strip().split("\n")[-2])
for tag, st, txt in HITS: print("HiGHS message in programme (i, j, k, pattern) =", tag, " returned status:", st, "(2 = infeasible) ;", txt.count("tmpSolver.run()"), "message(s)")
# re-solve those programmes with CP-SAT (script's own solve01 in --cpsat mode is not available in this namespace; use integer model directly)
from ortools.sat.python import cp_model
import numpy as np
from common import residues
M = 108
for tag, st, txt in HITS:
    i, j, k, Zv = tag; m = cp_model.CpModel(); x = [m.NewBoolVar(f"x{t}") for t in range(M)]; m.Add(sum(x) == k)
    for d in Zv:
        for row in residues(d, M): m.Add(sum(int(c) * x[t] for t, c in enumerate(row) if c) == 0)
    X = np.arange(M); N = lambda u, v: ((X % 2 ** i == u % 2 ** i) & (X % 3 ** j == v % 3 ** j)).astype(int)
    w = N(0, 0) - N(2 ** (i - 1), 0) - N(0, 3 ** (j - 1)) + N(2 ** (i - 1), 3 ** (j - 1))
    m.Add(sum(int(c) * x[t] for t, c in enumerate(w) if c) >= 1)
    sv = cp_model.CpSolver(); sv.parameters.num_workers = 3; sv.parameters.max_time_in_seconds = 120
    print("   CP-SAT on the same programme:", sv.StatusName(sv.Solve(m)))
