# Referee's own: every multiset (containing 0) of m elements taken from a given set of residues of Z_n
# (e.g. the multiples of n/p for the primes p of n: several primes live at once), all checks of ref_test.analyse.
import sys, math, itertools, time
from fractions import Fraction as Fr
import ref_test as rt
n = int(sys.argv[1]); budget = float(sys.argv[2]); mlo, mhi = int(sys.argv[3]), int(sys.argv[4])
resid = sorted(set(int(x) % n for x in sys.argv[5].split(",")) - {0})
t0 = time.time()
for m in range(mlo, mhi + 1):
    best = (Fr(0), None); cnt = 0; done = True
    for comb in itertools.combinations_with_replacement([0] + resid, m - 1):
        mult = {0: 1}
        for b in comb:
            mult[b] = mult.get(b, 0) + 1
        s = rt.analyse(n, mult)
        cnt += 1
        if s > best[0]:
            best = (s, sorted(mult.items()))
        if time.time() - t0 > budget:
            done = False
            break
    print("Z_%d, residues %s, m = %d: %d multisets (complete: %s), largest share %s = %.6f, sqrt(m)*share %.4f at %s; failures %d"
          % (n, resid, m, cnt, done, best[0], float(best[0]), math.sqrt(m) * float(best[0]), best[1], rt.ST["failures"]), flush=True)
    if not done:
        break
rt.report()
