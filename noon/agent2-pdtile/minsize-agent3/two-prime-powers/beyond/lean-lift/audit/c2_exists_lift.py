# Part 3(b): `exists_lift`, read literally:
#   for every w on Z_N with some w(x) != 0 there is w' on Z_{N r} with reduce(w') = w and
#   for all d: d | N r -> not d | N -> not (Phi_d | mask(w')).
# Method 1 (literal, exhaustive): run over EVERY multiset w' on Z_{N r} of size <= S, keep those with no new divisor,
#   collect their reductions; then every nonempty w on Z_N of size <= S must have been collected.
# Method 2 (larger sizes): for every nonempty w, run through its lifts (all w' with reduce(w') = w: each element x goes
#   to one of x, x+N, ..., x+(r-1)N) until one with no new divisor is found; if none, w is a counterexample.
# r = 2 is run too (the statement excludes it): it is reported whether a lift exists there.
import sys, time, itertools
from math import comb
sys.path.insert(0, '/home/agent3/lean/lift-audit')
from core import *
t0 = time.time()

def method1(N, r, S):
    M = N * r
    new = [d for d in divisors(M) if N % d != 0]
    T = {d: rem_table(M, d) for d in new}
    missing = []; nw = 0
    for s in range(1, S + 1):
        got = set()
        for idx in multiset_chunks(M, s):
            k = idx.shape[0]; nw += k
            good = np.ones(k, dtype=bool)
            for d in new:
                rem = np.zeros((k, T[d].shape[1]), dtype=np.int32)
                for i in range(s):
                    rem += T[d][idx[:, i]]
                good &= rem.any(axis=1)          # Phi_d does not divide
            red = np.sort(idx[good] % N, axis=1).astype(np.int64)
            key = np.zeros(red.shape[0], dtype=np.int64)
            for i in range(s):
                key = key * N + red[:, i]
            got.update(np.unique(key).tolist())
        for t in multisets(N, s):
            key = 0
            for x in t:
                key = key * N + x
            if key not in got:
                missing.append(t)
        assert len(got) <= comb(N + s - 1, s)
    return nw, missing, new

def lifts(t, N, r):
    """all multisets w' on Z_{N r} with reduction t (t a nondecreasing tuple on Z_N); lazy, nothing is stored"""
    groups = [(x, len(list(g))) for x, g in itertools.groupby(t)]
    def rec(i):
        if i == len(groups):
            yield ()
            return
        x, c = groups[i]
        for js in itertools.combinations_with_replacement(range(r), c):   # lazy
            head = tuple(x + j * N for j in js)
            for rest in rec(i + 1):
                yield head + rest
    return rec(0)

def method2(N, r, S, smin=1):
    M = N * r
    new = [d for d in divisors(M) if N % d != 0]
    T = {d: rem_table(M, d).tolist() for d in new}
    bad = []; nw = 0; maxtried = 0
    for s in range(smin, S + 1):
        for t in multisets(N, s):
            nw += 1; found = False; tried = 0
            for lt in lifts(t, N, r):
                tried += 1; ok = True
                for d in new:
                    Td = T[d]
                    rem = [sum(col) for col in zip(*[Td[y] for y in lt])]
                    if not any(rem):
                        ok = False; break
                if ok:
                    found = True; break
            maxtried = max(maxtried, tried)
            if not found:
                bad.append(t)
    return nw, bad, new, maxtried

which, scale = sys.argv[1], sys.argv[2]
M1_ODD = [(1,3,9),(2,3,8),(3,3,7),(4,3,6),(6,3,6),(5,3,5),(9,3,5),(12,3,5),(10,3,4),(15,3,4),(18,3,4),
          (1,5,7),(2,5,6),(3,5,5),(4,5,5),(5,5,5),(6,5,5),(10,5,4),(12,5,4),(1,7,6),(2,7,5),(3,7,5),(6,7,4),(7,7,4),(1,11,5),(2,11,4)]
M1_TWO = [(1,2,12),(2,2,10),(3,2,9),(4,2,8),(5,2,7),(6,2,7),(7,2,6),(8,2,6),(9,2,6),(10,2,6),(12,2,5),(15,2,5),(18,2,5),(20,2,4),(30,2,4)]
M2_ODD = [(6,3,9),(12,3,7),(18,3,6),(9,3,8),(10,3,7),(15,3,6),(30,3,4),(36,3,4),(6,5,8),(12,5,6),(20,3,5),(24,3,5),(45,3,3),(8,3,7),
          (16,3,5),(27,3,4),(25,5,4),(49,7,3),(14,7,5),(21,7,4),(1,3,40),(1,5,30),(1,13,8),(2,3,20),(3,3,14)]
M2_TWO = [(1,2,60),(2,2,24),(3,2,16),(4,2,13),(5,2,11),(6,2,10),(7,2,9),(9,2,8),(10,2,8),(12,2,7),(15,2,7),(18,2,6),(21,2,6),
          (30,2,5),(36,2,4),(45,2,4),(60,2,3),(105,2,3)]
if scale == "small":   # trial run, to look at time and memory before the real one
    M1_ODD, M1_TWO, M2_ODD, M2_TWO = [(6,3,4),(1,11,4)], [(6,2,4)], [(6,3,5),(1,13,6),(1,3,20)], [(6,2,5),(1,2,30)]
def line(tag, N, r, S, nw, bad, extra=""):
    print(f"  {tag} N={N:3d} r={r:2d} S={S:2d}: examined {nw}; nonempty w of size <= {S} with no lift: {len(bad)}{extra}" + (f"  e.g. {bad[:3]}" if bad else ""), flush=True)
if which == "m1":
    print("METHOD 1: every w' on Z_{Nr} of size 1..S; reductions of those with no new divisor (examined = number of w')")
    for (N, r, S) in M1_ODD:
        nw, missing, new = method1(N, r, S); line("odd r", N, r, S, nw, missing, f"; new divisors {new}")
    print("  r = 2 (excluded by the statement):")
    for (N, r, S) in M1_TWO:
        nw, missing, new = method1(N, r, S); line("r = 2", N, r, S, nw, missing, f"; new divisors {new}")
if which == "m2":
    print("METHOD 2: every nonempty w on Z_N of size <= S; search among its lifts (examined = number of w)")
    for (N, r, S) in M2_ODD:
        nw, bad, new, mt = method2(N, r, S); line("odd r", N, r, S, nw, bad, f"; most lifts tried for one w: {mt}")
    print("  r = 2 (excluded by the statement):")
    for (N, r, S) in M2_TWO:
        nw, bad, new, mt = method2(N, r, S); line("r = 2", N, r, S, nw, bad, f"; most lifts tried for one w: {mt}")
    for (N, r) in [(1,3),(6,3),(12,5)]:
        M = N * r
        assert all(divides(d, [0] * M) for d in divisors(M))
    print("the empty multiset on Z_N: its only preimage under reduce is empty, mask 0, every Phi_d divides: no lift (hw is needed)")
print(f"run {which} {scale}: {time.time()-t0:.0f} s")
