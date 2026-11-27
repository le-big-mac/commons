# The bound rho_2(B) >= p_(m-1) by brute force over all signings, for every multiset of m elements on Z_(2^k)
# (or, with the word "zero", every multiset that contains 0), and where it is attained.
# usage: run_bound.py K M_FROM M_TO [zero|sets|sets0]
#   sets: only sets (no repeated element); sets0: sets containing 0
import sys, itertools, time
from fractions import Fraction
from ref_lib import p, Fast

K = int(sys.argv[1]); M0 = int(sys.argv[2]); M1 = int(sys.argv[3])
mode = sys.argv[4] if len(sys.argv) > 4 else "all"
n = 1 << K
t0 = time.time()
fails = 0
print(f"Z_{n} (k = {K}), mode {mode}: brute force over all 2^m signings")
for m in range(M0, M1 + 1):
    f = Fast(m)
    bound = p(m - 1)
    bcount = bound * (1 << m)
    assert bcount.denominator == 1
    bcount = int(bcount)
    if mode == "all":
        it = itertools.combinations_with_replacement(range(n), m)
    elif mode == "zero":
        it = ((0,) + t for t in itertools.combinations_with_replacement(range(n), m - 1))
    elif mode == "sets":
        it = itertools.combinations(range(n), m)
    elif mode == "sets0":
        it = ((0,) + t for t in itertools.combinations(range(1, n), m - 1))
    total = 0; eq = 0; least = None; arg = None; below = 0
    for B in it:
        g = f.count_good(B, K)
        total += 1
        if g < bcount:
            below += 1; fails += 1
            print("  BELOW THE BOUND:", B, Fraction(g, 1 << m))
        if g == bcount:
            eq += 1
        if least is None or g < least:
            least = g; arg = B
    if total == 0:
        print(f"m = {m:2d}: no such multiset")
        continue
    print(f"m = {m:2d}: {total:8d} multisets, least rho_2 = {Fraction(least, 1 << m)} "
          f"(p_(m-1) = {bound}), below the bound: {below}, equal to the bound: {eq} "
          f"({'more' if 2 * eq > total else 'not more'} than half), first least at {arg}   [{time.time() - t0:.0f} s]",
          flush=True)
print("failures:", fails)
