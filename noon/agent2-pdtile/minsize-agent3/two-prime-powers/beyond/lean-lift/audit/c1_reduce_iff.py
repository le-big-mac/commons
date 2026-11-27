# Part 3(a): `sum_reduce` and `cyclotomic_dvd_reduce_iff`, read literally, on every multiset w' on Z_{N r} up to a size.
#   sum_reduce:                 sum_x reduce(w')(x) = sum_y w'(y)
#   cyclotomic_dvd_reduce_iff:  for every d | N:  Phi_d | mask(reduce w')  <->  Phi_d | mask(w')
# (neither assumes r odd; r = 2 is included.)  Slow path: count vectors and long division over Z, nothing else.
# Fast path (larger cases): remainders by table (checked against long division in c0_selftest.py).
import sys, time
sys.path.insert(0, '/home/agent3/lean/lift-audit')
from core import *
t0 = time.time()
print("SLOW PATH (count vectors, long division)")
slow = [(1,2,8),(1,3,7),(1,5,5),(2,2,7),(2,3,6),(3,2,6),(3,3,5),(4,2,5),(4,3,4),(6,2,4),(6,3,4),(5,2,5),(5,3,4),(9,2,4),(8,3,3),(12,3,3),(10,3,3),(6,5,3)]
tot = 0
for (N, r, S) in slow:
    M = N * r; n = 0; ndiv = 0
    for s in range(0, S + 1):
        for t in multisets(M, s):
            w = counts_of(t, M)
            red = reduce_mod(w, N)
            assert len(red) == N and sum(red) == sum(w) == s, ("sum_reduce fails", N, r, t)
            for d in divisors(N):
                a = divides(d, red); b = divides(d, w)
                assert a == b, ("cyclotomic_dvd_reduce_iff fails", N, r, t, d, a, b)
                ndiv += a
            n += 1
    tot += n
    print(f"  N={N:2d} r={r} M={M:2d}: all {n} multisets of size 0..{S}: both statements hold  ({ndiv} cases of divisibility among them)")
print(f"  slow path total {tot} multisets, {time.time()-t0:.0f} s")
print("FAST PATH (tables)")
fast = [(1,2,12),(2,2,10),(3,2,9),(6,2,7),(6,3,6),(9,2,6),(4,3,7),(12,2,5),(12,3,5),(10,3,5),(6,5,5),(15,2,5),(18,3,4),(15,3,4),(8,7,4),(9,3,6),(4,5,6),(10,5,4),(12,5,4),(30,2,4)]
tot = 0
for (N, r, S) in fast:
    M = N * r; n = 0; ndiv = 0
    TM = {d: rem_table(M, d) for d in divisors(N)}
    TN = {d: rem_table(N, d) for d in divisors(N)}
    for s in range(0, S + 1):
        for idx in multiset_chunks(M, s):
            k = idx.shape[0]; red = idx % N          # the reduced multiset, element by element
            for d in divisors(N):
                r1 = np.zeros((k, TM[d].shape[1]), dtype=np.int32); r2 = np.zeros_like(r1)
                for i in range(s):
                    r1 += TM[d][idx[:, i]]; r2 += TN[d][red[:, i]]
                a = ~r2.any(axis=1); b = ~r1.any(axis=1)
                assert (a == b).all(), ("cyclotomic_dvd_reduce_iff fails", N, r, d)
                ndiv += int(a.sum())
            n += k
    tot += n
    print(f"  N={N:2d} r={r} M={M:2d}: all {n} multisets of size 0..{S}: iff holds for every d | N  ({ndiv} cases of divisibility)")
print(f"  fast path total {tot} multisets; whole run {time.time()-t0:.0f} s")
