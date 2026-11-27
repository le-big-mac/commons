# t6_paper_examples.py -- the concrete claims made in the paper's subsection, checked with exact arithmetic.
import itertools, json, os
from core import *

# (a) "exactly Phi_6 among the divisors needs five elements; on Z_6 every such multiset has a repeated element, and on
#      Z_18 the set {0,1,2,4,10} will do"
g6, g18 = Group(6), Group(18)
print("(a) divisors > 1 of 18 dividing the mask of {0,1,2,4,10} on Z_18:", sorted(g18.pattern_of_set([0, 1, 2, 4, 10])))
least = None
allrep = True
nfive = 0
for t in range(1, 6):
    for comb in itertools.combinations_with_replacement(range(6), t):
        w = [0] * 6
        for y in comb:
            w[y] += 1
        if g6.pattern(w) == frozenset([6]):
            if least is None:
                least = t
            if t == 5:
                nfive += 1
                if max(w) == 1:
                    allrep = False
print("    least size of a multiset on Z_6 with exactly Phi_6:", least, "; multisets of 5 elements with exactly Phi_6:", nfive,
      "; every one has a repeated element:", allrep)
# sets on Z_18 with exactly Phi_6 among 2, 3, 6, 9, 18: least size
least18 = None
for t in range(1, 6):
    for comb in itertools.combinations(range(18), t):
        if g18.pattern_of_set(comb) == frozenset([6]):
            least18 = t
            break
    if least18:
        break
print("    least size of a set on Z_18 with exactly Phi_6 among the divisors > 1 of 18:", least18)

# (b) "on Z_2 the multiset with 0 four times and 1 twice has no cyclotomic divisor, and each of its six lifts to a set on
#      Z_8 gains Phi_4 or Phi_8"
g2, g8 = Group(2), Group(8)
print("(b) divisors (1 included) of the multiset (4, 2) on Z_2:", sorted(g2.pattern([4, 2], with_one=True)))
lifts = []
for odd in itertools.combinations([1, 3, 5, 7], 2):
    A = [0, 2, 4, 6] + list(odd)
    lifts.append((A, sorted(g8.pattern_of_set(A, with_one=True))))
for A, pat in lifts:
    print("    lift", A, "divisors:", pat)
print("    lifts:", len(lifts), "; each gains Phi_4 or Phi_8:", all((4 in pat) or (8 in pat) for _, pat in lifts))

# (c) "on Z_24 = Z_{12*2} the balanced pattern E = {1}, F = {2} of Z_12 ... has none": no set on Z_24 whose divisors,
#      among the divisors > 1 of 24, are exactly Phi_2, Phi_3, Phi_12
fn = 'census/set_24_T24.json'
if os.path.exists(fn):
    c = json.load(open(fn))
    hits = [(t, n) for t, d in c['count'].items() for key, n in d.items() if key == '2,3,12']
    print("(c) complete census of the sets on Z_24 (all sizes, sets containing 0: %d): sets with exactly Phi_2, Phi_3, Phi_12: %s"
          % (c['visited'], hits if hits else "none"))
    # for comparison: the same pattern among multisets on Z_12 is not empty by the theorem (18 elements); and patterns
    # that do occur on Z_24 at some size
    print("    number of different patterns of sets on Z_24:", len(set(k for d in c['count'].values() for k in d)))
else:
    print("(c) census of Z_24 not found")

# (d) the remark after the proposition: if every element has multiplicity r^j, the only set with these fibre counts is
#     the full preimage of the support, and its mask is divisible by EVERY Phi_d with d | N r^j, d not | N
tot = bad = 0
for (N, r, j) in [(1, 3, 1), (2, 3, 1), (3, 3, 1), (4, 3, 1), (6, 3, 1), (5, 3, 2), (6, 3, 2), (4, 5, 1), (6, 5, 1), (3, 5, 2),
                  (2, 7, 1), (6, 7, 1), (2, 7, 2), (10, 3, 1), (12, 3, 1)]:
    q = r ** j
    G = N * q
    g = Group(G)
    for k in range(1, N + 1):
        for supp in itertools.combinations(range(N), k):
            A = [x + N * u for x in supp for u in range(q)]
            pat = g.pattern_of_set(A)
            tot += 1
            if not all(d in pat for d in g.dgt1 if N % d != 0):
                bad += 1
print("(d) full preimages of supports: %d cases over 15 triples (N, r, j); with some new divisor missing: %d" % (tot, bad))
