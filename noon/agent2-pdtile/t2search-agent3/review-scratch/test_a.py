"""(a) the scripts' own transform matrix and pattern programmes.
 1. Tm of t2search.py and t1search.py against an independent computation (FFT of each class indicator at EVERY frequency of each order).
 2. sumf_range in floating point against sumf_range in rational arithmetic on ALL 2^|ORD| patterns (not only the ones the search visits).
 3. For Z_36: on all 13749 orbit representatives with certified verdicts (res36.pkl from test_g.py):
      'the script's pattern programme for the exact zero set allows the size'  <=>  'weak tile'   (both arithmetic modes),
      and the scripts' exact_complement functions return a complement exactly for the weak tiles."""
import sys, itertools, pickle, time, math
from fractions import Fraction
import numpy as np
from common import *
import wt
from loadscripts import t2_defs, t1_defs
t0 = time.time()
for (p, a, q, b) in [(2, 2, 3, 2), (2, 3, 3, 2), (2, 2, 3, 3), (2, 4, 3, 2), (2, 3, 5, 2)]:
    M = p ** a * q ** b
    nf = t2_defs(p, a, q, b); nx = t2_defs(p, a, q, b, "--exact"); n1 = t1_defs(p, a, q, b)
    divs, cls, Tm = wt.class_data(M)
    G = nf["G"]; ORD = nf["ORD"]
    # 1. transform matrix, class sizes, class of 0
    for o in ORD:
        d = p ** o[0] * q ** o[1]
        mine = [Tm[d][divs.index(p ** g[0] * q ** g[1])] for g in G]
        assert [int(v) for v in nf["Tm"][o]] == mine == [int(v) for v in nx["Tm"][o]] == list(n1["Tm"][o]), (M, o)
    assert [int(v) for v in nf["size"]] == [len(cls[p ** g[0] * q ** g[1]]) for g in G] == list(n1["size"])
    assert nf["cls"][0] == (a, b) and all(math.gcd(x, M) == p ** nf["cls"][x][0] * q ** nf["cls"][x][1] for x in range(1, M)) and math.gcd(0, M) == M
    assert n1["unit0"] == [int(g == (a, b)) for g in G]
    # 2. all patterns: float vs exact
    npat = ninf = nunb = 0; maxdiff = 0.0; mism = 0; allow_mism = 0
    if len(ORD) <= 11:
        for r in range(len(ORD) + 1):
            for Z in itertools.combinations(ORD, r):
                Z = frozenset(Z); npat += 1
                rf = nf["sumf_range"](Z); rx = nx["sumf_range"](Z)
                if (rf is None) != (rx is None): mism += 1; print("FEASIBILITY MISMATCH", M, sorted(Z), rf, rx); continue
                if rf is None: ninf += 1; continue
                lo, hi = rx
                if (hi is None) != (rf[1] == np.inf): mism += 1; print("UNBOUNDED MISMATCH", M, sorted(Z), rf, rx); continue
                nunb += hi is None
                maxdiff = max(maxdiff, abs(rf[0] - float(lo)), 0 if hi is None else abs(rf[1] - float(hi)))
                # sizes allowed: the scripts' two tests (range(2, M) in t2search; range(1, M + 1) in t1search)
                kf = [k for k in range(1, M + 1) if rf[0] - 1e-7 <= M / k <= rf[1] + 1e-7]
                kx = [k for k in range(1, M + 1) if lo * k <= M and (hi is None or M <= hi * k)]
                allow_mism += kf != kx
                assert kx == n1["sizes_allowed"](Z)
        print(f"Z_{M}: Tm, class sizes, classes agree with the independent computation;  all {npat} patterns: {ninf} infeasible, {nunb} with sum f unbounded; "
              f"float/exact status mismatches: {mism};  largest |float - exact| endpoint difference: {maxdiff:.2e};  patterns whose allowed size list differs between float (tol 1e-7) and exact: {allow_mism}   [{time.time() - t0:.0f} s]", flush=True)
    else:
        print(f"Z_{M}: Tm, class sizes, classes agree with the independent computation (pattern comparison skipped here: {2 ** len(ORD)} patterns)", flush=True)
    # 3. Z_36: script's pattern verdict against certified verdicts
    if M == 36:
        res = pickle.load(open("/tmp/rev_t2/res36.pkl", "rb")); o_of = {p ** o[0] * q ** o[1]: o for o in ORD}
        bad_f = bad_x = bad_c2 = bad_c1 = 0; nyes = 0
        for mask, k, verdict, ff, Z, cl in res:
            A = [x for x in range(M) if mask >> x & 1]; Zp = frozenset(o_of[d] for d in Z); yes = verdict == "yes"; nyes += yes
            rf = nf["sumf_range"](Zp); rx = nx["sumf_range"](Zp)
            af = rf is not None and rf[0] - 1e-7 <= M / k <= rf[1] + 1e-7
            ax = rx is not None and rx[0] * k <= M and (rx[1] is None or M <= rx[1] * k)
            bad_f += af != yes; bad_x += ax != yes
            f2, ZA2 = nf["exact_complement"](A); assert {p ** o[0] * q ** o[1] for o in ZA2} == set(Z)
            bad_c2 += (f2 is not None) != yes
            f1, ZA1 = n1["exact_complement"](A)
            bad_c1 += (f1 is not None) != yes
        print(f"Z_36, {len(res)} orbit representatives ({nyes} certified weak tiles): script pattern verdict differs from the certified verdict in {bad_f} (float) / {bad_x} (exact) cases; "
              f"t2search.exact_complement wrong in {bad_c2} cases, t1search.exact_complement wrong in {bad_c1} cases   [{time.time() - t0:.0f} s]", flush=True)
