# Single facts quoted in the text, and the two extensions the referee proposes.
import sys, random, itertools
from fractions import Fraction as F
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from rlib import *

# (1) after Corollary N: n = 6, three elements, one in each class modulo 3, not all of the same parity:
#     half of the signings are bad at 3 or at 6; and D_3 = 2.
for B in itertools.product(range(6), repeat=3):
    if sorted(x % 3 for x in B) == [0, 1, 2] and len(set(x % 2 for x in B)) == 2:
        bl = bad_levels(list(B), 6)
        assert int((bl[3] | bl[6]).sum()) == 4 and D_rank([x % 3 for x in B], 3) == 2
print("(1) n = 6, one element in each class mod 3, not all of one parity: exactly half of the 8 signings are bad at 3 or 6; D_3 = 2")

# (2) section 6: class sizes (2,2,2) modulo 3: true share bad at 3 (j = 0) is 5/32
bl = bad_levels([0, 0, 1, 1, 2, 2], 3)
print("(2) class sizes (2,2,2) mod 3: share bad at 3 =", F(int(bl[3].sum()), 64))
assert F(int(bl[3].sum()), 64) == F(5, 32)

# (3) section 6: the seven points of Z_945 with first-order sum 33/32, and the 'designed' seven points of Z_315
def first_order(W, npr, dangerous_only=False, W2=None):
    fac = factorint(npr)
    lv = {p: live_levels(W, p, a) for p, a in fac.items()}
    tot = F(0)
    for e in divisors(npr):
        if e == 1:
            continue
        if all(i in lv[p] for p, i in factorint(e).items()):
            if dangerous_only:
                pw = powers_mod2(e)
                s = 0
                for w in (W2 if W2 is not None else W):
                    s ^= pw[w % e]
                if s:
                    continue
            tot += F(2, 2 ** D_rank(W, e))
    return tot
W945 = [141, 207, 318, 363, 490, 614, 786]
print("(3) Z_945, %s: sum over the live e of 2^(1-D_e) = %s ; over the live dangerous e: %s" % (W945, first_order(W945, 945), first_order(W945, 945, True)))
W315 = [69, 101, 138, 190, 191, 207, 280]
print("    Z_315, %s: %s ; live dangerous: %s" % (W315, first_order(W315, 315), first_order(W315, 315, True)))

# (4) m = 5 on moduli with a prime factor >= 7 and 15 | n (listed as open in the text): the live e have only the
#     primes 3 and 5 (a full group of p needs p elements), so the proof of Theorem D (iii) applies.  Brute force:
rnd = random.Random(9)
worst = F(1); cnt = 0; worst_first = F(0)
for trial in range(2500):
    n = rnd.choice([210, 420, 630, 1050, 330, 390, 2310])
    k, npr = split2(n)
    t = rnd.random()
    if t < 0.3:
        B = [rnd.randrange(n) for _ in range(5)]
    elif t < 0.6:      # one element in every class modulo 5, three classes modulo 3
        B = []
        for r in range(5):
            while True:
                x = rnd.randrange(n)
                if x % 5 == r and x % 3 == r % 3:
                    B.append(x); break
    else:              # one element in every class modulo 3, twins
        B = []
        for r in range(3):
            while True:
                x = rnd.randrange(n)
                if x % 3 == r:
                    B.append(x); break
        x = rnd.choice(B)
        B += [(x + n // 2) % n, (B[1] + rnd.choice([n // 3, n // 5, n // 7 if n % 7 == 0 else n // 2])) % n]
    W = [x % npr for x in B]
    for p in factorint(npr):
        if p >= 7:
            assert not live_levels(W, p, factorint(npr)[p])
    bl = bad_levels(B, n)
    anyb = np.zeros(32, dtype=bool)
    for d in bl:
        anyb |= bl[d]
    first = first_order(W, npr, True)
    assert first < 1
    good = 1 - F(int(anyb.sum()), 32)
    assert 1 - good <= first
    worst = min(worst, good); worst_first = max(worst_first, first); cnt += 1
print("(4) m = 5 on n in {210, 330, 390, 420, 630, 1050, 2310}: %d multisets, no prime >= 7 has a live level; share of bad signings <= sum over live dangerous e"
      " (largest such sum %s); least share of good signings %s" % (cnt, worst_first, worst))

# (5) Lemma Q with l >= 2: how often was it exercised?  Count on designed trees.
def dangerous(F_, q):
    pw = powers_mod2(q)
    s = 0
    for w in F_:
        s ^= pw[w % q]
    return s == 0
cnts = {}
for p, a in [(3, 4), (3, 5), (5, 3), (7, 2)]:
    for trial in range(400):
        # parities: every level dangerous -> all classes at every depth odd: the full group Z_{p^a} (one element each)
        # here: levels chosen at random
        levels = [i for i in range(1, a + 1) if rnd.random() < 0.7]
        par = {0: 1}
        for i in range(1, a + 1):
            new = {}
            q = p ** (i - 1)
            for c, b in par.items():
                if i in levels:
                    ch = [b] * p
                else:
                    ch = [rnd.randint(0, 1) for _ in range(p)]
                    if sum(ch) % 2 != b:
                        ch[rnd.randrange(p)] ^= 1
                for t in range(p):
                    if ch[t]:
                        new[c + t * q] = 1
                    elif rnd.random() < 0.1:
                        new[c + t * q] = 0
            par = new
        F_ = [c for c, b in par.items() for _ in range(1 if b else 2)]
        assert len(F_) % 2 == 1
        W = sorted(set(F_))
        l = 0
        for i in range(1, a + 1):
            if dangerous(F_, p ** i):
                l += 1
                assert live_level(W, p, i)
                assert D_rank(W, p ** i) >= (p - 1) * p ** (l - 1), (p, i, l)
                cnts[(p, l)] = cnts.get((p, l), 0) + 1
print("(5) Lemma Q on designed trees: dangerous prime powers by (p, l):", dict(sorted(cnts.items())))
print("OK")
