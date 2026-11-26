# 1. "balance at d" as the page words it (the walk and the weights) against "Phi_d divides sum A(x) X^x".
# 2. Every example on the 12-hour clock.
# 3. The tiling paragraph and its criterion, exhaustively on small clocks, for sets and for markings with repeats.
import random, itertools, math, re, glob
from itertools import combinations, combinations_with_replacement
from mpmath import mp, mpf, mpc, exp, pi
from polylib import *
from rules import read_enum
mp.dps = 60
TOL = mpf(10) ** -40

def walk_balance(marks, M, d):
    """The page's words: count through the hours 0..M-1 moving 1/d of a full turn per hour; a weight for each
    mark where you stand; balance = centre of gravity at the centre. Returns |sum of the weights' positions|."""
    pos = mpc(0)
    here = mpc(1)                       # where you stand at hour 0
    step = exp(2j * pi / d)             # 1/d of a full turn
    cnt = [0] * M
    for h in marks: cnt[h % M] += 1
    for hour in range(M):
        pos += cnt[hour] * here
        here *= step
    return abs(pos)

# ---- 1. equivalence -------------------------------------------------------------------------------
random.seed(20261126)
tested = agree = balanced_cases = 0
smallest_nonzero = None
def test(marks, M):
    global tested, agree, balanced_cases, smallest_nonzero
    for d in divisors(M):
        if d == 1: continue
        ex = balances_exact(marks, M, d)
        w = walk_balance(marks, M, d)
        fl = w < TOL
        tested += 1; agree += (ex == fl); balanced_cases += ex
        if not fl and (smallest_nonzero is None or w < smallest_nonzero): smallest_nonzero = w
# (a) every multiset of at most 5 marks on the 12-hour clock
for s in range(1, 6):
    for marks in combinations_with_replacement(range(12), s): test(marks, 12)
# (b) random markings on other clocks, including clocks not of the form p^n q, biased to produce balances
for M in [6, 8, 9, 10, 12, 18, 20, 24, 30, 36, 54]:
    for _ in range(400):
        marks = []
        for _ in range(random.randint(1, 4)):      # unions of regular polygons and stray marks
            d = random.choice([x for x in divisors(M) if x > 1]); start = random.randrange(M)
            if random.random() < 0.75: marks += [(start + j * (M // d)) % M for j in range(d)]
            else: marks += [start]
        test(marks, M)
print(f"1. balance by the walk (|sum| < 1e-40 at 60 digits) against exact division by Phi_d: {tested} (marking, d) pairs, "
      f"agree {agree}, disagree {tested - agree}; balanced in {balanced_cases}; smallest nonzero |sum| seen {mp.nstr(smallest_nonzero, 5)}")

# ---- 2. the 12-hour examples ----------------------------------------------------------------------
def pat(marks, M=12): return sorted(pattern_exact(marks, M))
print("2. pair 0,6 balances exactly at", pat([0, 6]), "(page: 12 and 4, not 2, 3, 6)")
for d in (2, 3, 6):
    print(f"   at {d}: hour 6 is {mpf(6)/d} turns on from hour 0 (a whole number of turns = same spot)")
print("   at 4: hour 6 is", mpf(6) / 4, "turns on (opposite)")
print("   triangle 1,5,9 balances exactly at", pat([1, 5, 9]), "(page: 12, 6 and 3)")
print("   the five marks 0,6,1,5,9 balance exactly at", pat([0, 6, 1, 5, 9]), "(page: 12 and nowhere else)")
best12, _ = read_enum(12, 18)
for name, P in [("12 alone", {12}), ("4 and 12", {4, 12}), ("3 alone", {3})]:
    size, marks = best12[frozenset(P)]
    print(f"   pattern '{name}': least number over ALL markings with <= 18 marks = {size}; one such marking {marks}")
fewer = [m for s in range(1, 5) for m in combinations_with_replacement(range(12), s) if pattern_exact(m, 12) == frozenset({12})]
print(f"   markings with 1 to 4 marks (all {sum(math.comb(11 + s, s) for s in range(1, 5))}) that balance at 12 and nowhere else: {len(fewer)}  (page: it cannot be done with fewer than five)")
print("   marks 0,6 have pattern", pat([0, 6]), "; marks 0,1,2 have pattern", pat([0, 1, 2]))

# ---- 3. tiling ------------------------------------------------------------------------------------
def conv(A, B, M):
    c = [0] * M
    for a in A:
        for b in B: c[(a + b) % M] += 1
    return c
print("3. pair 0,6 turned by 0..5 covers the 12 hours with counts", conv([0, 6], range(6), 12))
def criterion_test(M, repeats):
    ds = [d for d in divisors(M) if d > 1]
    items = []
    gen = combinations_with_replacement if repeats else combinations
    maxsize = M
    for s in range(1, maxsize + 1):
        if M % s: continue                      # sizes that cannot multiply to M are counted separately below
        for A in gen(range(M), s):
            items.append((s, A, frozenset(d for d in ds if balances_exact(A, M, d))))
    pairs = tile = crit = both = 0
    full = frozenset(ds)
    bysize = {}
    for it in items: bysize.setdefault(it[0], []).append(it)
    for s, la in bysize.items():
        t = M // s
        for (_, A, PA) in la:
            for (_, B, PB) in bysize.get(t, []):
                pairs += 1
                c = conv(A, B, M)
                is_tile = all(x == 1 for x in c)
                is_crit = (PA | PB) == full     # sizes multiply to M here by construction
                tile += is_tile; crit += is_crit; both += (is_tile and is_crit)
    return pairs, tile, crit, both
for M, rep in [(4, False), (6, False), (8, False), (9, False), (10, False), (12, False), (4, True), (6, True), (8, True), (9, True), (10, True), (12, True)]:
    if rep and M == 12:
        # with repeats on 12 hours leave out the sizes 12 x 1 (1,352,078 markings of 12 marks): done separately below
        pass
    pairs, tile, crit, both = criterion_test(M, rep) if not (rep and M == 12) else (None,) * 4
    if pairs is None: continue
    print(f"   clock {M}, {'markings with repeats' if rep else 'sets'}: ordered pairs with sizes multiplying to {M}: {pairs}; tile: {tile}; criterion holds: {crit}; both: {both}; "
          f"{'criterion = tiling on every pair' if tile == crit == both else 'CRITERION FAILS'}")
# pairs whose sizes do not multiply to M can never tile (count the cover), and the criterion as worded requires the product: nothing to test.
