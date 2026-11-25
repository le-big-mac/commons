"""Which code paths of exactlp.lp do the test families and the scripts' real pattern programmes exercise?  (instrumented copy in memory)"""
import sys, random, itertools
sys.dont_write_bytecode = True
src = open("/home/agent3/t2search/exactlp.py").read().split('if __name__ == "__main__":')[0]
a1 = "            if s is not None: _pivot(T, basis, i, s)"; assert src.count(a1) == 1
src = src.replace(a1, "            COUNT['art_basic_after_phase1'] += 1\n            if s is not None:\n                COUNT['driven_out'] += 1; COUNT['driven_out_negative_pivot'] += T[i][s] < 0; _pivot(T, basis, i, s)")
a2 = "    T2 = [T[i][:n] + [T[i][n + m]] for i in keep]"; assert src.count(a2) == 1
src = src.replace(a2, "    COUNT['redundant_rows_dropped'] += m - len(keep); COUNT['calls_with_redundancy'] += m > len(keep)\n" + a2)
a3 = "        _pivot(T, basis, best[1], s)"; assert src.count(a3) == 1
src = src.replace(a3, "        COUNT['pivots'] += 1; COUNT['degenerate_pivots'] += best[0] == 0\n" + a3)
import collections
ns = {"COUNT": collections.Counter()}; exec(compile(src, "exactlp_instrumented", "exec"), ns); lp = ns["lp"]; COUNT = ns["COUNT"]
import test_e
rnd = random.Random(20261120)
for kind, ntr in [("degenerate", 2500), ("redundant", 2500), ("fractional", 1500), ("scriptlike", 2500)]:
    COUNT.clear(); st = collections.Counter()
    for _ in range(ntr):
        A, b, c = test_e.gen(kind, rnd); r = lp(A, b, c); st[r[0]] += 1
        assert r[0] == test_e.lp(A, b, c)[0]
    print(f"{kind:11s}: {dict(st)}  paths: {dict(COUNT)}")
# the scripts' real programmes, M = 72 and 108: every pattern, both objectives
from loadscripts import t2_defs
for (p, a, q, b) in [(2, 3, 3, 2), (2, 2, 3, 3)]:
    nx = t2_defs(p, a, q, b, "--exact"); ORD = nx["ORD"]; G = nx["G"]; gi = nx["gi"]; Tm = nx["Tm"]; size = [int(v) for v in nx["size"]]
    COUNT.clear(); st = collections.Counter()
    for r in range(len(ORD) + 1):
        for Z in itertools.combinations(ORD, r):
            rows = [[int(g == (a, b)) for g in G]] + [[int(v) for v in Tm[o]] for o in ORD if o not in Z]; rhs = [1] + [0] * (len(rows) - 1)
            for sg in (1, -1): st[lp(rows, rhs, [sg * v for v in size])[0]] += 1
    print(f"real pattern programmes Z_{p**a*q**b}: {dict(st)}  paths: {dict(COUNT)}")
