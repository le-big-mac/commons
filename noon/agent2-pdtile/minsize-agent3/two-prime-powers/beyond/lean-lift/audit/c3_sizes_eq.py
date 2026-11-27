# Part 3(c): `sizes_eq`, read literally, up to a size bound S.  For P a finite set of naturals with every element dividing N:
#   {s | exists w' on Z_{Nr}: sum w' = s, 0 < s, for all d: d | N r -> d != 1 -> (Phi_d | mask w'  <->  d in P)}
# = {s | exists w  on Z_N   : sum w  = s, 0 < s, for all d: d | N   -> d != 1 -> (Phi_d | mask w   <->  d in P)}
# Both sets are computed for s <= S from a census of ALL multisets of size <= S on both groups, and compared for EVERY P
# that satisfies hP (every subset of the divisors of N, those containing 1 included).
import sys, time, itertools
sys.path.insert(0, '/home/agent3/lean/lift-audit')
from core import *
t0 = time.time()
def subsets(xs):
    for k in range(len(xs) + 1):
        for c in itertools.combinations(xs, k):
            yield frozenset(c)
def sizes(cen, modulus, P, S):
    """the set of the statement, cut at S: cen is the census of Z_modulus"""
    out = set()
    for D, ss in cen.items():
        if all(((d in D) == (d in P)) for d in divisors(modulus) if d != 1):
            out |= {s for s in ss if 0 < s <= S}
    return out
def run(N, r, S, tag):
    M = N * r
    cM, nM = census(M, S); cN, nN = census(N, S)
    nP = 0; bad = []; nonempty = 0; both_empty = 0
    for P in subsets(divisors(N)):
        L = sizes(cM, M, P, S); R = sizes(cN, N, P, S); nP += 1
        if L != R: bad.append((sorted(P), sorted(L), sorted(R)))
        if L: nonempty += 1
        if not L and not R: both_empty += 1
    # what happens if hP is dropped: P containing a divisor of N r that does not divide N
    new = [d for d in divisors(M) if N % d != 0]
    differ = 0; tried = 0
    for P in subsets(divisors(N)):
        for d in new:
            P2 = P | {d}; tried += 1
            if sizes(cM, M, P2, S) != sizes(cN, N, P2, S): differ += 1
    print(f"  {tag} N={N:2d} r={r:2d} S={S:2d}: {nM}+{nN} multisets; {nP} sets P with hP: sets differ for {len(bad)}; "
          f"both nonempty (<=S) for {nonempty}, both empty (<=S) for {both_empty}.  [P with one new divisor added (hP false): differ for {differ} of {tried}]"
          + (f"  FIRST DIFFERENCE {bad[0]}" if bad else ""), flush=True)
    return bad
scale = sys.argv[1]
ODD = [(1,3,20),(2,3,12),(3,3,10),(4,3,9),(5,3,7),(6,3,7),(9,3,6),(10,3,6),(12,3,6),(15,3,5),(18,3,5),(20,3,4),
       (1,5,10),(2,5,8),(3,5,7),(4,5,7),(5,5,6),(6,5,6),(10,5,5),(12,5,4),(1,7,8),(2,7,6),(3,7,6),(6,7,5),(7,7,5),(1,11,6)]
TWO = [(1,2,30),(2,2,16),(3,2,12),(4,2,10),(5,2,9),(6,2,8),(7,2,7),(8,2,7),(9,2,7),(10,2,7),(12,2,6),(15,2,6),(18,2,6),(30,2,4)]
if scale == "small":
    ODD, TWO = [(6,3,5),(1,3,8)], [(6,2,5)]
print("r odd (the statement):")
allbad = []
for (N, r, S) in ODD: allbad += run(N, r, S, "odd r")
print("r = 2 (excluded by the statement):")
for (N, r, S) in TWO: run(N, r, S, "r = 2")
print(f"differences for odd r: {len(allbad)};  run {scale}: {time.time()-t0:.0f} s")
